# GSheets_TSDB-python
Making Google Sheets into a free Time-Series database! Built on top of nithinmurali/pygsheets, much thanks to him for the starting library.  

> Please enable the Sheets API in the google cloud developer console!

## Core features
- Use of Named Ranges as Time Indexes
- Time Ranges updated at every operation (append, pop, update)
- Querying data using date as key yields O(1) runtime (regardless of cell count) 
- Declarative naming scheme (sheets = databases, worksheets = tables)

## Original pygsheets package by nithinmurali
<https://github.com/nithinmurali/pygsheets>

# Functions
> Note: function names abstract Google Sheets as a database with tables!
- Opening a Database (creates one if doesn't exist)
```
db1 = SheetsDB(db_name = "New",folder_name = "Warehouse")
```

- Opening a table (creates one if doesn't exist)
```
table1 = db1.get_table(table_name = "Table")
```

- Table : append
```
head = table1.append(
    row_data = [
        "=NOW()",
        "one",
        "two",
        "thee"
    ]
)
```

- Table : update
```
table1.update(
    row_id   = 10,
    row_data = ["i","was","updated"]
)
```

- Table : pop
```
table1.pop(
    row_id = 3,
)
```

- Table : search 
```
table1.search(
  named_range = "date_20220730", 
  query       = "pin"
)
```

- Table : get_date 
```
To Be Continued ... 
```
