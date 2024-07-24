import sqlite3

def modify_data(db, field, new_value, postcode):
    sql = f"UPDATE 'table' SET {field} = ? WHERE Postcode = ?"
    val = (new_value, postcode)
    db.execute(sql, val)
    db.commit()
    print("Record updated")

def delete_data(connection, postcode):
    cursor = connection.cursor()
    sql_select = "SELECT * FROM 'table' WHERE Postcode = ?"
    val = (postcode,)
    cursor.execute(sql_select, val)
    row = cursor.fetchone()
    if not row:
        print("No record found with the given Postcode.")
        return
    print("Are you sure you want to delete this record?")
    print(row)
    confirmation = input("Enter y to confirm deletion: ")
    if confirmation.lower() == 'y':
        sql_delete = "DELETE FROM 'table' WHERE Postcode = ?"
        cursor.execute(sql_delete, val)
        connection.commit()
        print(cursor.rowcount, "record(s) deleted.")
    else:
        print("Deletion canceled.")

print("1. ADD \n2. MODIFY \n3. DELETE")
choice = int(input("Enter your choice: "))

db_location = input("Enter the SQLite database file location (e.g., C:/Project/database1.db): ")

try:
    mydb = sqlite3.connect(db_location)
    mycursor = mydb.cursor()

    if choice == 1:
        b = int(input("Enter the Postcode: "))
        c = int(input("Enter the Sales_Rep_ID: "))
        d = input("Enter the Sales_Rep_Name: ")
        e = int(input("Enter the Year: "))
        sql = "INSERT INTO 'table' (Postcode, Sales_Rep_ID, Sales_Rep_Name, Year) VALUES (?, ?, ?, ?)"
        val = (b, c, d, e)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Details inserted.")

    elif choice == 2:
        b = int(input("Enter the Postcode to modify: "))
        print("1. Postcode \n2. Sales_Rep_ID \n3. Sales_Rep_Name \n4. Year")
        modify_choice = int(input("Enter your choice: "))
        if modify_choice in [1, 2, 3, 4]:
            new_value = input("Enter the new value: ")
            modify_fields = {1: 'Postcode', 2: 'Sales_Rep_ID', 3: 'Sales_Rep_Name', 4: 'Year'}
            modify_data(mydb, modify_fields[modify_choice], new_value, b)
        else:
            print("Invalid choice")

    elif choice == 3:
        b = int(input("Enter the Postcode to delete: "))
        delete_data(mydb, b)

    else:
        print("Incorrect Choice")

finally:
    mydb.close()
