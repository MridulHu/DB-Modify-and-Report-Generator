import sqlite3
from datetime import datetime

conn = sqlite3.connect('C:/Project/db3.db')
cursor = conn.cursor()

cursor.execute('SELECT Sales_Rep_ID, Sales_Rep_Name, Value, Postcode FROM table1 ORDER BY Value DESC LIMIT 10')
top_salespersons = cursor.fetchall()

conn.close()

if top_salespersons:
    current_date = datetime.now().strftime('%Y-%m-%d')

    with open('C:/Project/top.txt', 'r') as file:
        template = file.read()

    content_to_write = template
    for i in range(10):
        Sales_Rep_ID = str(top_salespersons[i][0])
        Sales_Rep_Name = str(top_salespersons[i][1])
        Value = str(int(top_salespersons[i][2])) 
        Postcode = str(top_salespersons[i][3])

        content_to_write = content_to_write.replace(f'[ID{i+1}]', Sales_Rep_ID)
        content_to_write = content_to_write.replace(f'[Name{i+1}]', Sales_Rep_Name)
        content_to_write = content_to_write.replace(f'[Value{i+1}]', Value)
        content_to_write = content_to_write.replace(f'[Postcode{i+1}]', Postcode)

    with open('C:/Project/top_performers.txt', 'w') as file:
        file.write(content_to_write)

    print("The top_performers.txt file has been created successfully.")
else:
    print("No data found in the database.")
