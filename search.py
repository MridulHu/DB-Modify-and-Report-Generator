import sqlite3
a=int(input("Enter the post number:"))
conn = sqlite3.connect('C:/Project/database1.db')
mycursor = conn.cursor()
mycursor.execute('SELECT * FROM "table" WHERE Postcode=?', (a,))
myresult = mycursor.fetchone()
columns = [description[0] for description in mycursor.description]
print(columns)
print(myresult)
mycursor.close()
conn.close()