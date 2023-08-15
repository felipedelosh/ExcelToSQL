"""
FelipdelosH
2023

read a Excel file and get SQL query to insert all values
https://es.stackoverflow.com/questions/601539/insertar-excel-en-tabla-de-base-de-datos-sql-server-mediante-python

You need install PANDAS.
"""
import pandas as pd

# Vars
_PATH_EXCEL = "excel.csv" # Put file path here
_SQL_TABLE_NAME = "person"
_COL_NAMES = ['ID','Name','lastName','Age','Gender','Location'] # Put col names here
_VALUES_NAMES_FORMAT = str(_COL_NAMES).replace("[", "").replace("]", "").replace("\'", "")
_TYPES_ROWS = {'ID':int,'Name':str,'lastName':str,'Age':int,'Gender':str,'Location':str}
_DROP_HEADERS = True # if you need delete a headers of data

#Methods
def getDataInFormat(value, key_type_row):
    """
    Enter a STR and return int(), str(), bool() if key_type_row
    """
    # GET integer
    if _TYPES_ROWS[key_type_row] == int:
        return f"{value}"
    
    if _TYPES_ROWS[key_type_row] == float:
        return f"{value}"
    
    if _TYPES_ROWS[key_type_row] == str:
        return f"'{value}'"
    
    if _TYPES_ROWS[key_type_row] == bool:
        if str(value).lower() == "true" or value == "1":
            return "true"
        else:
            return "false"


# READ DATA
# pd.read_excel, pd.read_csv, pd.read_json... pd.read_xlsx
data = pd.read_csv(_PATH_EXCEL, sep="|", names=_COL_NAMES, encoding="utf-8")
# if delete a first row (col names)
if _DROP_HEADERS:
    data = data.drop(0)

print(f"YOU READ DE FILE: {_PATH_EXCEL}\nTHE TOP#5 DATA IS\n{data.head()}")

# Create a SQL
_SQLOUTPUT = ""
print("========GENERATE SQLFILE========")
for i in range(len(data)):
    _sqlValues = "" # Save here values of SQL
    _d = data.iloc[i] # Save in temp file
    counter_type = 0 # To macth a data with rigth type of sql insert
    for key_type_row in _TYPES_ROWS:
        _sqlValues = _sqlValues + getDataInFormat(_d[counter_type], key_type_row) + ","
        counter_type = counter_type + 1

    _sqlValues = _sqlValues[:-1] # Erase last comma
    _SQLOUTPUT = _SQLOUTPUT + f"insert into {_SQL_TABLE_NAME} ({_VALUES_NAMES_FORMAT}) values ({_sqlValues});\n"

print("========PROCCES IS OVER VIEW FILE: output.sql========")
with open("output.sql", "w", encoding="UTF-8") as f:
    f.write(_SQLOUTPUT)
