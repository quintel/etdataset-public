import openpyxl
import pandas as pd
import xlwings as xw
from pathlib import Path


class ApplicationShares():
    """
    Load the application shares by transforming the 
    PBL referentieverbruiken data
    """
    def __init__(self, geo_id):
        self.geo_id = geo_id

        
    def call(self):
        # Initialise the path to the application shares data by PBL
        path = Path(__file__).parents[2] / f"data" / "raw" / f"pbl_referentieverbruiken_{self.geo_id}.xlsx"
        
        # Load the relevant sheet ("Resultaten gemeente") into a dataframe
        # The first four rows should be combined into a multi-header
        # wb = openpyxl.load_workbook(path, data_only=True)
        wb = xw.Book(path)
        ws = wb.sheets["Resultaten gemeente"]

        # Close the workbook
        wb.close()
        
        # df = pd.DataFrame(ws.values)
        # df = pd.read_excel(path, sheet_name="Resultaten gemeente", freeze_panes=None, header=[0,1,2,3])
        
        return ws
        
        
        
        