import sqlite3
from datetime import datetime, timedelta

def get_sales_rep_details_by_post_code(db_path, post_code):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT Sales_Rep_Name, Sales_Rep_ID FROM table1 WHERE Postcode = ?", (post_code,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {"name": result[0], "id": result[1]}
    else:
        print("No details found for Post Code:", post_code)
        return None

def generate_leave_letter(file_path, db_path, post_code, start_date, leave_days):

    details = get_sales_rep_details_by_post_code(db_path, post_code)
    
    if details is None:
        return
    
    sales_rep_name = details["name"]
    sales_rep_id = str(details["id"])

    with open(file_path, 'r') as file:
        leave_letter = file.read()
    
    start_date_obj = datetime.strptime(start_date, '%d/%m/%y')
    end_date_obj = start_date_obj + timedelta(days=leave_days - 1)
    end_date = end_date_obj.strftime('%d/%m/%y')

    print(f"Calculated end date: {end_date}")
    
    leave_letter = leave_letter.replace('[Sales_Rep_Name]', sales_rep_name)
    leave_letter = leave_letter.replace('[Your Sales Rep ID]', sales_rep_id)
    leave_letter = leave_letter.replace('[Your Post Code]', post_code)
    leave_letter = leave_letter.replace('[30/06/24]', start_date)
    leave_letter = leave_letter.replace('[end_date]', end_date)
    leave_letter = leave_letter.replace('[Postcode]', post_code)
    
    output_file_path = file_path.replace('.txt', '_filled.txt')
    with open(output_file_path, 'w') as file:
        file.write(leave_letter)
    
    print(f"Leave letter generated and saved to {output_file_path}")

post_code = input("Enter Post Code: ")
start_date = input("Enter start date (dd/mm/yy): ")
leave_days = int(input("Enter number of leave days: "))

template_file_path = 'C:/Project/leave.txt'
database_file_path = 'C:/Project/database1.db'

generate_leave_letter(template_file_path, database_file_path, post_code, start_date, leave_days)
