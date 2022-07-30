import pygsheets
import numpy as np
import datetime as dt 
import pytz as tz
import time

PRINT_ENABLED = True

class SheetsTable:

    name = None 
    head = None
    wks  = None
    head = None

    def __init__(self,
        table_name,
        sheet_object,
    ):
        self.table_name  = table_name
        self.wks         = sheet_object.worksheet_by_title(table_name) 
        self.refresh()

    def get_named_ranges(self):
        return self.wks.get_named_ranges()

    def get_named_range(self, 
        named_range
    ):
        return self.wks.get_named_range(named_range)

    def refresh(self):
        # {'tableRange': <GridRange 'Sheet1'!A1:E28>, 'updates': {'updatedRange': <GridRange 'Sheet1'!A29:AX1021>, 'updatedCells': 1, 'updatedColumns': 1, 'updatedRows': 1}}
        resp = self.wks.append_table([""])
        if 'tableRange' in resp and resp['tableRange'] != '':
            self.head       = resp['tableRange'].end[0]   
        else:
            self.head = 0

    def get_head(self,
        worksheet
    ):
        wks = self.sheet_object.worksheet_by_title(worksheet)
        wks.append_table(["hello","this","is"])
        return
    
    def check_exists(self,
        named_range
    ):
        try:
            self.wks.get_named_range(
                named_range
            )
        except Exception as e:
            return False

        return True

    def append(self,
        row_data
    ):
        resp = self.wks.append_table(row_data)

        date = str(dt.datetime.now(tz.timezone('US/Eastern')).date()).replace("-","")
        key  = f"date_{date}"
        exists = self.check_exists(key)

        if exists:
            range_object = self.wks.get_named_range(
                name = key
            )
            start_coords = (range_object.start_addr)
            end_coords   = (range_object.end_addr)
            end_coords   = (end_coords[0]+1,end_coords[1])

            self.wks.delete_named_range(
                name = key, 
            )
            self.wks.create_named_range(
                name  = key,
                start = start_coords,
                end   = end_coords
            )
        else: 
            start_coords = (self.head+1, 0)
            end_coords   = (self.head+1, len(row_data))
            self.wks.create_named_range(
                name  = key,
                start = start_coords,
                end   = end_coords
            )

        self.head = resp['updates']['updatedRange'].end[0]
        time.sleep(1)
        return self.head
    
    def update(self, row_id,
        row_data
    ):
        self.wks.update_values(f'A{row_id}', [row_data])
        return 
    
    # def delete(self, row_id):
    #     self.wks.update_values(f'A{row_id}', [["",""]])
    #     return 

    def pop(self, 
        row_id = None
    ):
        if row_id == None: row_id = self.head

        self.wks.delete_rows(row_id, number=1)
        self.refresh()
        return 
    
    def search(self, 
        named_range,
        query
    ):
        dimensions = self.wks.get_named_range(named_range)
        start_addr = (dimensions.start_addr)
        end_addr   = (dimensions.end_addr)
        print(start_addr[0], end_addr[0]), 
        print(start_addr[1], end_addr[1])
        var = self.wks.find(
            pattern = query,
            cols=(start_addr[1], end_addr[1]), 
            rows=(start_addr[0], end_addr[0])
        )
        print(var)

class SheetsDB(object):

    tables         = None
    google_client  = None
    sheet_object   = None

    """
    Initializes google sheets file (or if exists, create one)
    :param p1: 
    :param p2: 
    """
    def __init__(self, 
        db_name,        
        folder_name
    ):

        try:     self.google_client = pygsheets.authorize()
        except:  raise Exception("[ERROR] client_secret.json -> Missing ")

        try:    
            self.sheet_object = self.google_client.open(db_name)
            self.tables       = self.sheet_object.worksheets()

        except Exception as e: 
            self.sheet_object = self.google_client.create(
                title       = db_name,
                folder_name = folder_name
            )

        if PRINT_ENABLED: print(f"[*] _{db_name}_ is loaded")

    def get_table(self, 
        table_name
    ):
        try:
            table_object = SheetsTable(
                table_name,
                sheet_object  = self.sheet_object
            )
        except:
            self.sheet_object.add_worksheet(
                title=table_name
            )
            table_object = SheetsTable(
                table_name,
                sheet_object  = self.sheet_object
            )

        # if table_name not in self.tables: raise Exception("Table not in Database!")
        
        return table_object

    