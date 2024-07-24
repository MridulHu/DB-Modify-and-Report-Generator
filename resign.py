import sqlite3
import os

# Function to fetch data from the database based on the postcode
def fetch_data(postcode):
    # Connect to the database
    conn = sqlite3.connect(r'C:\Project\database1.db')
    cursor = conn.cursor()
    
    # Execute the query
    cursor.execute("SELECT Postcode, Sales_Rep_ID, Sales_Rep_Name, Year FROM table1 WHERE Postcode = ?", (postcode,))
    
    # Fetch the data
    data = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    return data

# Function to update the resignation letter
def update_resignation_letter(letter_content, data):
    # Convert data to string
    postcode, sales_rep_id, sales_rep_name, year = map(str, data)
    
    # Replace placeholders with actual data
    updated_letter = letter_content.replace('Postcode', postcode)
    updated_letter = updated_letter.replace('Sales_Rep_ID', sales_rep_id)
    updated_letter = updated_letter.replace('Sales_Rep_Name', sales_rep_name)
    updated_letter = updated_letter.replace('Year', year)
    
    return updated_letter

def main():
    # Ask user for a specific postcode
    postcode = input("Please enter the specific postcode: ")
    
    # Fetch data from the database
    data = fetch_data(postcode)
    
    if data:
        # Read the original resignation letter
        with open(r'C:\Project\Resign.txt', 'r') as file:
            letter_content = file.read()
        
        # Update the resignation letter with the fetched data
        updated_letter = update_resignation_letter(letter_content, data)
        
        # Define the new file path
        new_file_path = r'C:\Project\Resign_Updated.txt'
        
        # Write the updated letter to a new file
        with open(new_file_path, 'w') as file:
            file.write(updated_letter)
        
        print(f"Updated resignation letter has been created at: {new_file_path}")
    else:
        print("No data found for the provided postcode.")

if __name__ == "__main__":
    main()
