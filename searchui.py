import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog, QRadioButton, QHBoxLayout
from PyQt5.QtCore import Qt

class FetchDataApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search DataBase')
        self.initUI()

    def initUI(self):
        self.db_location = None
        self.table_name = 'table1'  

        layout = QVBoxLayout()

        select_db_button = QPushButton('Select Database')
        select_db_button.clicked.connect(self.select_database)
        layout.addWidget(select_db_button)

        self.postcode_radio = QRadioButton('Search by Postcode')
        self.sales_rep_radio = QRadioButton('Search by Sales Rep Name')

        self.postcode_radio.setChecked(True)  
        self.search_option = 'postcode' 
        self.postcode_radio.toggled.connect(lambda: self.radio_button_checked('postcode'))
        self.sales_rep_radio.toggled.connect(lambda: self.radio_button_checked('sales_rep'))

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.postcode_radio)
        radio_layout.addWidget(self.sales_rep_radio)
        layout.addLayout(radio_layout)

        self.postcode_label = QLabel('Enter Postcode:')
        layout.addWidget(self.postcode_label)
        self.postcode_input = QLineEdit()
        layout.addWidget(self.postcode_input)
        self.postcode_input.returnPressed.connect(self.fetch_data)

        self.sales_rep_label = QLabel('Enter Sales Rep Name:')
        layout.addWidget(self.sales_rep_label)
        self.sales_rep_input = QLineEdit()
        layout.addWidget(self.sales_rep_input)
        self.sales_rep_input.returnPressed.connect(self.fetch_data)

        search_button = QPushButton('Search')
        search_button.clicked.connect(self.fetch_data)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def radio_button_checked(self, option):
        if option == 'postcode':
            self.postcode_input.setEnabled(True)
            self.sales_rep_input.setEnabled(False)
            self.search_option = 'postcode'
        elif option == 'sales_rep':
            self.postcode_input.setEnabled(False)
            self.sales_rep_input.setEnabled(True)
            self.search_option = 'sales_rep'

    def select_database(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.db_location, _ = QFileDialog.getOpenFileName(self, "Select SQLite database file", "C:/Project/", "SQLite Database Files (*.db)", options=options)

    def fetch_data(self):
        if not self.db_location:
            QMessageBox.critical(self, "Error", "No database file selected.")
            return

        try:
            conn = sqlite3.connect(self.db_location)
            mycursor = conn.cursor()

            if self.search_option == 'postcode':
                postcode_text = self.postcode_input.text().strip()
                if not postcode_text.isdigit():
                    QMessageBox.critical(self, "Error", "Invalid postcode. Please enter a valid number.")
                    return
                postcode = int(postcode_text)
                query = f'SELECT * FROM "{self.table_name}" WHERE Postcode=?'
                mycursor.execute(query, (postcode,))
            
            elif self.search_option == 'sales_rep':
                sales_rep_name = self.sales_rep_input.text().strip()
                query = f'SELECT * FROM "{self.table_name}" WHERE Sales_Rep_Name LIKE ?'
                mycursor.execute(query, (f'%{sales_rep_name}%',))

            results = mycursor.fetchall()  
            
            columns = [description[0] for description in mycursor.description]
            
            mycursor.close()
            conn.close()

            if results:
                result_str = f"Table Name: {self.table_name}\n\n"
                if self.search_option == 'postcode':
                    result_str += f"Postcode: {postcode}\n\n"
                elif self.search_option == 'sales_rep':
                    result_str += f"Sales Rep Name: {sales_rep_name}\n\n"
                result_str += "Columns: " + ", ".join(columns) + "\n\n"
                result_str += "Results:\n"
                
                for result in results:
                    result_str += ", ".join(map(str, result)) + "\n"

                QMessageBox.information(self, "Query Result", result_str)
            else:
                QMessageBox.information(self, "Query Result", f"No data found in table '{self.table_name}' for the specified criteria.")
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"SQLite error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FetchDataApp()
    window.show()
    sys.exit(app.exec_())
