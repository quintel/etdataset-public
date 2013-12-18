#!/usr/bin/env python
#
#   Copyright information
#
# Copyright (C) 2010-2012 Dilshod Temirkhodjaev <tdilshod@gmail.com>
#
# Edit by Quintel Intelligence www.quintel.com, Jesse Kerkhoven
#
# This script is used to perform a 'git dif' on Excel files (binary).
# Check out the documentation on https://github.com/quintel/etdataset, 
# specifically: https://github.com/quintel/etdataset/blob/master/QI%20technical%20readme.md#for-quintel-employees-how-to-git-diff-excel-files
#
#   License
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Dilshod Temirkhodjaev <tdilshod@gmail.com>"
__license__ = "GPL-2+"

import datetime, zipfile, sys, os, re
import xml.parsers.expat
from xml.dom import minidom

# see also ruby-roo lib at: http://github.com/hmcgowan/roo
FORMATS = {
  'general' : 'float',
  '0' : 'float',
  '0.00' : 'float',
  '#,##0' : 'float',
  '#,##0.00' : 'float',
  '0%' : 'percentage',
  '0.00%' : 'percentage',
  '0.00e+00' : 'float',
  'mm-dd-yy' : 'date',
  'd-mmm-yy' : 'date',
  'd-mmm' : 'date',
  'mmm-yy' : 'date',
  'h:mm am/pm' : 'date',
  'h:mm:ss am/pm' : 'date',
  'h:mm' : 'time',
  'h:mm:ss' : 'time',
  'm/d/yy h:mm' : 'date',
  '#,##0 ;(#,##0)' : 'float',
  '#,##0 ;[red](#,##0)' : 'float',
  '#,##0.00;(#,##0.00)' : 'float',
  '#,##0.00;[red](#,##0.00)' : 'float',
  'mm:ss' : 'time',
  '[h]:mm:ss' : 'time',
  'mmss.0' : 'time',
  '##0.0e+0' : 'float',
  '@' : 'float',
  'yyyy\\-mm\\-dd' : 'date',
  'dd/mm/yy' : 'date',
  'hh:mm:ss' : 'time',
  "dd/mm/yy\\ hh:mm" : 'date',
  'dd/mm/yyyy hh:mm:ss' : 'date',
  'yy-mm-dd' : 'date',
  'd-mmm-yyyy' : 'date',
  'm/d/yy' : 'date',
  'm/d/yyyy' : 'date',
  'dd-mmm-yyyy' : 'date',
  'dd/mm/yyyy' : 'date',
  'mm/dd/yy hh:mm am/pm' : 'date',
  'mm/dd/yyyy hh:mm:ss' : 'date',
  'yyyy-mm-dd hh:mm:ss' : 'date',
}
STANDARD_FORMATS = {
  0 : 'general',
  1 : '0',
  2 : '0.00',
  3 : '#,##0',
  4 : '#,##0.00',
  9 : '0%',
  10 : '0.00%',
  11 : '0.00e+00',
  12 : '# ?/?',
  13 : '# ??/??',
  14 : 'mm-dd-yy',
  15 : 'd-mmm-yy',
  16 : 'd-mmm',
  17 : 'mmm-yy',
  18 : 'h:mm am/pm',
  19 : 'h:mm:ss am/pm',
  20 : 'h:mm',
  21 : 'h:mm:ss',
  22 : 'm/d/yy h:mm',
  37 : '#,##0 ;(#,##0)',
  38 : '#,##0 ;[red](#,##0)',
  39 : '#,##0.00;(#,##0.00)',
  40 : '#,##0.00;[red](#,##0.00)',
  45 : 'mm:ss',
  46 : '[h]:mm:ss',
  47 : 'mmss.0',
  48 : '##0.0e+0',
  49 : '@',
}

def xlsx2text(infilepath):
  #   override date/time format
  dateformat=None
  #   csv columns delimiter symbol
  delimiter=os.linesep
  #   skip empty lines
  skip_empty_lines=False
  
  try:
    ziphandle = zipfile.ZipFile(infilepath)
  except zipfile.BadZipfile:
    sys.stderr.write("Invalid xlsx file: " + infilepath + os.linesep)
    return
  try:
    shared_strings = parse(ziphandle, SharedStrings, "xl/sharedStrings.xml")
    styles = parse(ziphandle, Styles, "xl/styles.xml")
    workbook = parse(ziphandle, Workbook, "xl/workbook.xml")
    props = parse(ziphandle, Props, "docProps/core.xml")
        
    print "Last modified at " + props.date_modified + ", output with formula values"
    for s in workbook.sheets:
      sheetfile = ziphandle.open("xl/worksheets/sheet%i.xml" %s['id'], "r")
      sheet = Sheet(workbook, shared_strings, styles, sheetfile, s)
      sheet.set_dateformat(dateformat)
      sheet.set_skip_empty_lines(skip_empty_lines)
      sheet.set_use_formula(True)
      sheet.print_data()
      sheetfile.close()

    # do it again for values
    print "Last modified at " + props.date_modified + ", output with calculated values"
    for s in workbook.sheets:
      sheetfile = ziphandle.open("xl/worksheets/sheet%i.xml" %s['id'], "r")
      sheet = Sheet(workbook, shared_strings, styles, sheetfile, s)
      sheet.set_dateformat(dateformat)
      sheet.set_skip_empty_lines(skip_empty_lines)
      sheet.set_use_formula(False)
      sheet.print_data()
      sheetfile.close()


  finally:
    ziphandle.close()

def parse(ziphandle, klass, filename):
  instance = klass()
  if filename in ziphandle.namelist():
    f = ziphandle.open(filename, "r")
    instance.parse(f)
    f.close()
  return instance



class Workbook:
  def __init__(self):
    self.sheets = []
    self.date1904 = False

  def parse(self, filehandle):
    workbookDoc = minidom.parseString(filehandle.read())
    if len(workbookDoc.firstChild.getElementsByTagName("fileVersion")) == 0:
      self.appName = 'unknown'
    else:
      self.appName = workbookDoc.firstChild.getElementsByTagName("fileVersion")[0]._attrs['appName'].value
    try:
      self.date1904 = workbookDoc.firstChild.getElementsByTagName("workbookPr")[0]._attrs['date1904'].value.lower().strip() != "false"
    except:
      pass

    sheets = workbookDoc.firstChild.getElementsByTagName("sheets")[0]
    for sheetNode in sheets.getElementsByTagName("sheet"):
      attrs = sheetNode._attrs
      name = attrs["name"].value
      if self.appName == 'xl':
        if attrs.has_key('r:id'): id = int(attrs["r:id"].value[3:])
        else: id = int(attrs['sheetId'].value)
      else:
        if attrs.has_key('sheetId'): id = int(attrs["sheetId"].value)
        else: id = int(attrs['r:id'].value[3:])
      self.sheets.append({'name': name, 'id': id})

class Props:
  def __init__(self):
    self.date_created = ""
    self.date_modified = ""
    self.date1904 = False

  def parse(self, filehandle):
    workbookDoc = minidom.parseString(filehandle.read())
    self.date_created =  workbookDoc.firstChild.getElementsByTagName("dcterms:created")[0].firstChild.nodeValue
    self.date_modified =  workbookDoc.firstChild.getElementsByTagName("dcterms:modified")[0].firstChild.nodeValue

class Styles:
    def __init__(self):
        self.numFmts = {}
        self.cellXfs = []

    def parse(self, filehandle):
        styles = minidom.parseString(filehandle.read()).firstChild
        # numFmts
        numFmtsElement = styles.getElementsByTagName("numFmts")
        if len(numFmtsElement) == 1:
            for numFmt in numFmtsElement[0].childNodes:
                numFmtId = int(numFmt._attrs['numFmtId'].value)
                formatCode = numFmt._attrs['formatCode'].value.lower().replace('\\', '')
                self.numFmts[numFmtId] = formatCode
        # cellXfs
        cellXfsElement = styles.getElementsByTagName("cellXfs")
        if len(cellXfsElement) == 1:
            for cellXfs in cellXfsElement[0].childNodes:
                if (cellXfs.nodeName != "xf"):
                    continue
                numFmtId = int(cellXfs._attrs['numFmtId'].value)
                self.cellXfs.append(numFmtId)

class SharedStrings:
    def __init__(self):
        self.parser = None
        self.strings = []
        self.si = False
        self.t = False
        self.rPh = False
        self.value = ""

    def parse(self, filehandle):
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.CharacterDataHandler = self.handleCharData
        self.parser.StartElementHandler = self.handleStartElement
        self.parser.EndElementHandler = self.handleEndElement
        self.parser.ParseFile(filehandle)

    def handleCharData(self, data):
        if self.t:
            self.value+= data

    def handleStartElement(self, name, attrs):
        if name == 'si':
            self.si = True
            self.value = ""
        elif name == 't' and self.rPh:
            self.t = False
        elif name == 't' and self.si:
            self.t = True
        elif name == 'rPh':
            self.rPh = True

    def handleEndElement(self, name):
        if name == 'si':
            self.si = False
            self.strings.append(self.value)
        elif name == 't':
            self.t = False
        elif name == 'rPh':
            self.rPh = False

class Sheet:
    def __init__(self, workbook, sharedString, styles, filehandle,info):
        self.parser = None
        self.sharedString = None
        self.styles = None

        self.in_sheet = False
        self.in_row = False
        self.in_cell = False
        self.in_cell_value = False
        self.in_cell_formula = False

        self.columns = {}
        self.rowNum = None
        self.colType = None
        self.s_attr = None
        self.formula = ""
        self.data = None
        

        self.dateformat = None
        self.skip_empty_lines = False
        self.use_formula = False
        
        self.filehandle = filehandle
        self.workbook = workbook
        self.sharedStrings = sharedString.strings
        self.styles = styles
        
        self.info = info

    def set_dateformat(self, dateformat):
        self.dateformat = dateformat

    def set_skip_empty_lines(self, skip):
        self.skip_empty_lines = skip
        
    def set_use_formula(self, formula):
        self.use_formula = formula

    def print_data(self):
        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.CharacterDataHandler = self.handleCharData
        self.parser.StartElementHandler = self.handleStartElement
        self.parser.EndElementHandler = self.handleEndElement
        self.parser.ParseFile(self.filehandle)

    def handleCharData(self, data):
        if self.in_cell_value:
            self.collected_string+= data
            self.data = self.collected_string
            if self.colType == "s": # shared string
                self.data = self.sharedStrings[int(self.data)]
            elif self.colType == "b": # boolean
                self.data = (int(data) == 1 and "TRUE") or (int(data) == 0 and "FALSE") or data
            elif self.s_attr:
                s = int(self.s_attr)

                # get cell format
                format = None
                xfs_numfmt = self.styles.cellXfs[s]
                if self.styles.numFmts.has_key(xfs_numfmt):
                    format = self.styles.numFmts[xfs_numfmt]
                elif STANDARD_FORMATS.has_key(xfs_numfmt):
                    format = STANDARD_FORMATS[xfs_numfmt]
                # get format type
                if format and FORMATS.has_key(format):
                    format_type = FORMATS[format]
                    try:
                        if format_type == 'date': # date/time
                            if self.workbook.date1904:
                                date = datetime.datetime(1904, 01, 01) + datetime.timedelta(float(self.data))
                            else:
                                date = datetime.datetime(1899, 12, 30) + datetime.timedelta(float(self.data))
                            if self.dateformat:
                                # str(dateformat) - python2.5 bug, see: http://bugs.python.org/issue2782
                                self.data = date.strftime(str(self.dateformat))
                            else:
                                dateformat = format.replace("yyyy", "%Y").replace("yy", "%y"). \
                                  replace("hh:mm", "%H:%M").replace("h", "%H").replace("%H%H", "%H").replace("ss", "%S"). \
                                  replace("d", "%e").replace("%e%e", "%d"). \
                                  replace("mmmm", "%B").replace("mmm", "%b").replace(":mm", ":%M").replace("m", "%m").replace("%m%m", "%m"). \
                                  replace("am/pm", "%p")
                                self.data = date.strftime(str(dateformat)).strip()
                        elif format_type == 'time': # time
                            self.data = str(float(self.data) * 24*60*60)
                        elif format_type == 'float' and ('E' in self.data or 'e' in self.data):
                            self.data = ("%f" %(float(self.data))).rstrip('0').rstrip('.')
                    except (ValueError, OverflowError):
                        # invalid date format
                        pass
        elif self.in_cell_formula:
          self.formula = self.formula + data
        
        # at prefix
        prefix = self.colNum + self.rowNum + ' '
        
        if self.use_formula:
          if self.formula:
            self.data = prefix + self.formula
          else:
            self.data = ""
        else:
          self.data = prefix + self.data

    def handleStartElement(self, name, attrs):
        if self.in_row and name == 'c':
            self.colType = attrs.get("t")
            self.s_attr = attrs.get("s")
            cellId = attrs.get("r")
            if cellId:
                self.colNum = cellId[:len(cellId)-len(self.rowNum)]
                self.colIndex = 0
            else:
                self.colIndex+= 1
            self.formula = ""
            self.data = ""
            self.in_cell = True
        elif self.in_cell and (name == 'v' or name == 'is'):
            self.in_cell_value = True
            self.collected_string = ""
        elif self.in_cell and name == 'f':
           self.in_cell_formula = True
        elif self.in_sheet and name == 'row' and attrs.has_key('r'):
            self.rowNum = attrs['r']
            self.in_row = True
            self.columns = {}
            self.spans = None
            if attrs.has_key('spans'):
                self.spans = [int(i) for i in attrs['spans'].split(":")]
        elif name == 'sheetData':
            self.in_sheet = True

    def handleEndElement(self, name):
        if self.in_cell and name == 'v':
            self.in_cell_value = False
        elif self.in_cell and name == 'f':
           self.in_cell_formula = False
        elif self.in_cell and name == 'c':
            t = 0
            for i in self.colNum: t = t*26 + ord(i) - 64
            self.columns[t - 1 + self.colIndex] = self.data
            self.in_cell = False
        if self.in_row and name == 'row':
            if len(self.columns.keys()) > 0:
                d = [""] * (max(self.columns.keys()) + 1)
                for k in self.columns.keys():
                    d[k] = self.columns[k].encode("utf-8")
                if self.spans:
                    l = self.spans[0] + self.spans[1] - 1
                    if len(d) < l:
                        d+= (l - len(d)) * ['']
                # write line to csv
                if not self.skip_empty_lines or d.count('') != len(d):
                    sheet_name = self.info['name'].encode("utf-8")
                    for cell in d:
                        print sheet_name + ' ' + cell
            self.in_row = False
        elif self.in_sheet and name == 'sheetData':
            self.in_sheet = False

if __name__ == "__main__":

    if len(sys.argv) == 2:
      xlsx2text(sys.argv[1])
    else:
      sys.exit(2)                     