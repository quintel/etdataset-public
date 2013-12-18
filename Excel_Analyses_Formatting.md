## Formatting Excel workbooks / Research Data Analyses

### Analysis Content 
All analyses should have the following sheets (in the given order). The
sequence "introduction slides, assumption, dashboard" should not be
interrupted.
- Introduction slides (gray slides)
- Cover sheet - general info and legend of color coding and font 
 - Changelog - date of change, change, version number
 - Contents - a complete list of all sheets in the workbook (including keynote style description)
 - Introduction 
  - What is the goal of the analysis?
  - What needs to be done by the user?
  - General intro to the ETM. 
 - Dataflow - A visualization of the dataflow (see below)
 - Assumptions
  - Explicitly state all modeling assumptions. 
  - List all assumptions that are asked for in the Dashboard
  - List the aggregation of IEA energy carriers to ETM energy carriers as performed in the analysis (sheet Fuel aggregation)
- Dashboard (yellow)
 - Contains buttons for automatic import/export (VBA macros)
 - Asks for user input
 - Displays mismatches and checks
- Results (bright red)
 - Results of calculations. These sheets usually comprise applications and technology splits as well as 
- Calculations (bright blue)
 - sort these in a 'drill down' approach. Display the sheet that is closest to the results first. In consequence, the fuel aggregation sheet should be one of the last sheets. 
- CSV files (purple)
 - all sheets have to be named "csv_...". They will be exported by a VBA script (see below). 

### General formatting 
All analyses have to 'look and feel' the same. Use the
same color theme as the existing analyses.  The dataflow and manner of
displaying results and calculations should be as homogeneous as possible.

#### Layout of Dataflow 
The dataflow should give a clear indication of "what
data is used where? To produce what?". Make sure that all sheets, especially
the calculations sheets are properly reflected in the dataflow. The output
CSVs should be grouped sensibly.  Also see [issue #98](https://github.com/quintel/rdr/issues/98). 
Check existing dataflow sheets, copy to new analysis and adjust.

#### Layout of Dashboard 
The Dashboard is placed next to assumptions sheet.
There are strict rules about the contents of each column. Especially, column E
needs to hold user input, and column O needs to hold the key to that input
(used in automatic export of dashboard values). See [issue #100](https://github.com/quintel/rdr/issues/100) Link cells that contain
'year', 'country', 'workbook version' etc. as much as possible. Make sure that
updating workbooks is easy (functions and links can automatically read the
latest date and version number from the change log etc.).

#### Formatting cells and sheets 
We want use as little colors as possible,
because they might not display correctly in older Excel versions or on
different machines.

Cells are formatted in regular black font in general. Intermediate results can
be italicized. Main results (of a sheet) should be bold.  Cell names are
displayed in italics.  Input cells have a thick black boarder around them.

##### Tables  
Tables have a thick black boarder around them.  The header row
is bold. Sectors are not bold, but underlined. Multiple rows that belong to a
group of items have ‘no cell filling color’, which makes the grey lines
visible and adds to readability. The rest of the table has ‘white’ cell
background color.

##### Number formats
Dates: enter a date in the format dd/mm/yyyy. Excel
should display this as “August 12, 2013” (copy format from old analysis…).
Percentages: Most importantly, use a uniform number format. Percentages are
generally displayed as 26.8%.  Energy demand: Energy demand should always be
in TJ. Use the “thousands separator” and use an appropriate amount of
decimals. E.g. 16,279.

Significant digits are not a concern as long as cells are properly linked. The
VBA script will export all digits (not what is ‘visible’).

Only sheets and checks have background colors.  Stick to the following color
code (or look at an existing analysis):
 
#### Linking Cells 
##### General 
Do not use VLOOKUP. Make use of ‘names’. Do
not use a name for every variable, but only name important and frequently used
variables. The use of names has to be transparent. Explicitly write down the
name of a cell where it is defined.

##### In calculations 
Do not link to cells outside of the currents sheet in
any calculation / formula. Please use a name if linking to a cell outside the
active sheet. Preferably, display the relevant data (redundant information) on
the active slide and link to those repetitive cells in the calculation.

Only if checks are calculated, these rules can be interpreted more liberally,
as they are not part of the main calculation, which has to be as transparent
as possible.

**Summarizing:** 
- do not name anything in the "input sheets" (i.e. energy balance and auto-producer tables)
- name all hard-coded numbers (e.g. 3.6) (on the assumption sheet). 
- Use names in calculations (formulas) that refers to another sheet
- try to avoid this as much as possible by "repeating" values on the sheet where the calculation takes place and only link cells 
- do not name cells that are only linked to in CSV output sheets
Also see [issue #92](https://github.com/quintel/rdr/issues/92). 

#### Checks 
All checks should be displayed on the Dashboard. 
If useful, checks should also be shown (redundant) on the actual sheet where the check might fail.
- do inputs add up to 100% (critical)
- Some values may not be negative.
- Some fuel demands may not exceed certain ranges (critical)
- Carriers aggregated correctly? This is a check on the fuel aggregation sheet that checks if all fuels in EB have been aggregated to an ETM carrier. (critical)
- Have all inputs been filled in?
- Are all critical checks positive?
- is the energy balance pasted correctly? (critical) Come up with some kind of check that would detect if the EB has moved be a column or row. For example, I use the following check in the residence analysis: Sum(all carriers in subsectors)==Total of subsector displayed in the energy balance
- are there rows or carriers in the IEA data that is not considered in the analysis (this may be relevant for other countries)? 

Checks should be formatted in the following way
- the text of critical checks should be bold
- the 'to do' advice of a failing checks should become invisible IF the check passes

Also see [issue #99](https://github.com/quintel/rdr/issues/99). 

### Naming of CSV files 
All CSV files that are exported form the analysis need to have certain name. 
- parent / child shares CSV files are called `<converter name_parent_share>` or `<converter name_child_share>`
- primary production CSVs (time curves) are called `<carrier>_time_curve`
- there are two versions of the `corrected_energy_balance_step_1/2`
- there are two versions of the `central_electricity_production_step_1/2`
- there also is a table containing final demands in the metal analysis (used in industry analysis) 
- ...

### VBA script / macro functionality 
All analyses contain "buttons" on the Dashboard that activate certain macros. 
- All sheets that shall be exported automatically, have to be named (sheet name) `csv_.....`. The CSV file will be saved under the name provided in cell A1. A macro will delete the first row of the sheet and save the rest as a CSV file.  Also see [issue #86](https://github.com/quintel/rdr/issues/86).
- There are buttons that allow for the automatic import of energy balances and more
- There are buttons for saving/loading dashboard values. 
github.com/quintel/rdr/issues/127) for a list of naming conventions for buttons. 

#### Macro buttons
**No** macros are assigned to the buttons themselves. The will be assigned automatically by the VBA script of the analysis manager. The VBA script recognizes buttons by their 'name'. Therefore, the text that is displayed on the button itself is not relevant for the execution of the macro. 
Give the buttons the right names, please check [issue #127](https://github.com/quintel/rdr/issues/127).Use a clear layout of the buttons, make sure they get pressed in the right order. 

#### General formatting tricks 
It is often handy to make use of line breaks in
certain cells (for example, the 'notes' cell).  Hold down the Option and
Command keys while pressing Return.

##### Macros: 
The following tricks are neat to maintain Excel cell names:

Executing the following lines in a macro will delete all names that are
currently defined in a workbook 
````
For Each n In ActiveWorkbook.Names 
n.Delete
Next n
````

New names can easily be defined with the Insert/Name/Create command. (this
requires the names to be adjacent to the cells "to be named")

