from GSheets_TSDB import SheetsDB

db1    = SheetsDB(db_name = "New",folder_name = "Warehouse")
table1 = db1.get_table(table_name = "Table")

named_range_list = table1.get_named_ranges()
print(named_range_list)

for i in range(5):
  head = table1.append(
      row_data = [
          "=NOW()",
          "one",
          "two",
          "thee"
      ]
  )

table1.search(
  named_range = "date_20220730", 
  query       = "pin"
)

table1.update(
    row_id   = 10,
    row_data = ["i","was","updated"]
)

table1.pop(
    row_id = 3,
)




