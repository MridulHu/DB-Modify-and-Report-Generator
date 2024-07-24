import sqlite3
import pandas as pd

read_file= pd.read_excel("Sample1.xlsx")
read_file.to_csv ("Sample1.csv",index = None)

df=pd.read_csv(
    filepath_or_buffer='C:\Project\Sample1.csv',
    header=0
)
print(df)

connection = sqlite3.connect('C:\Project\database1.db')
df.to_sql('table', connection, if_exists='append', index=False)
connection.commit()
connection.close()