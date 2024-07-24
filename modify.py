import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGroupBox, QRadioButton, QMessageBox, QGridLayout, QFileDialog, QInputDialog
)

class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Database Operations')
        self.database_path = self.get_database_file_path()
        self.table_name = 'table1'  # Fixed table name
        self.initUI()

    def get_database_file_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select Database File", "",
                                                  " Database Files (*.db *.sqlite *.sqlite3);;All Files (*)",
                                                  options=options)
        return filename

    def initUI(self):
        layout = QVBoxLayout()

        operation_group = QGroupBox('Select an operation:')
        self.add_radio = QRadioButton('Add')
        self.modify_radio = QRadioButton('Modify')
        self.delete_radio = QRadioButton('Delete')

        operation_layout = QVBoxLayout()
        operation_layout.addWidget(self.add_radio)
        operation_layout.addWidget(self.modify_radio)
        operation_layout.addWidget(self.delete_radio)
        operation_group.setLayout(operation_layout)
        layout.addWidget(operation_group)

        input_group = QGroupBox('Input Fields:')
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel('Postcode:'), 0, 0)
        self.postcode_entry = QLineEdit()
        grid_layout.addWidget(self.postcode_entry, 0, 1)
        grid_layout.addWidget(QLabel('Sales Rep ID:'), 1, 0)
        self.sales_rep_id_entry = QLineEdit()
        grid_layout.addWidget(self.sales_rep_id_entry, 1, 1)
        grid_layout.addWidget(QLabel('Sales Rep Name:'), 2, 0)
        self.sales_rep_name_entry = QLineEdit()
        grid_layout.addWidget(self.sales_rep_name_entry, 2, 1)
        grid_layout.addWidget(QLabel('Year:'), 3, 0)
        self.year_entry = QLineEdit()
        grid_layout.addWidget(self.year_entry, 3, 1)
        input_group.setLayout(grid_layout)
        layout.addWidget(input_group)

        execute_button = QPushButton('Execute')
        execute_button.clicked.connect(self.button_click)
        layout.addWidget(execute_button)

        self.setLayout(layout)

    def button_click(self):
        choice = None
        if self.add_radio.isChecked():
            choice = 1
        elif self.modify_radio.isChecked():
            choice = 2
        elif self.delete_radio.isChecked():
            choice = 3

        postcode = self.postcode_entry.text()
        sales_rep_id = self.sales_rep_id_entry.text()
        sales_rep_name = self.sales_rep_name_entry.text()
        year = self.year_entry.text()

        if choice == 1:  # Add operation
            if postcode and sales_rep_id and sales_rep_name and year:
                try:
                    self.add_data(int(postcode), sales_rep_id, sales_rep_name, int(year))
                except Exception as e:
                    self.show_message("Error", f"Error inserting record: {str(e)}")
            else:
                self.show_message("Error", "Please fill in all fields.")
        elif choice == 2:  # Modify operation
            if postcode:
                if sales_rep_id:
                    self.modify_data('Sales_Rep_ID', sales_rep_id, int(postcode))
                elif sales_rep_name:
                    self.modify_data('Sales_Rep_Name', sales_rep_name, int(postcode))
                elif year:
                    self.modify_data('Year', int(year), int(postcode))
                else:
                    self.show_message("Error", "Please fill in Postcode and one other field to modify.")
            else:
                self.show_message("Error", "Please fill in Postcode.")
        elif choice == 3:  # Delete operation
            if postcode:
                try:
                    self.delete_data(int(postcode))
                except Exception as e:
                    self.show_message("Error", f"Error deleting record: {str(e)}")
            else:
                self.show_message("Error", "Please fill in Postcode.")

    def add_data(self, postcode, sales_rep_id, sales_rep_name, year):
        try:
            db = sqlite3.connect(self.database_path) 
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM '{self.table_name}' WHERE Postcode = ?", (postcode,))
            existing_record = cursor.fetchone()
            if existing_record:
                self.show_message("Error", "Postcode already exists. Please use a different postcode.")
                return
            sql = f"INSERT INTO '{self.table_name}' (Postcode, Sales_Rep_ID, Sales_Rep_Name, Year) VALUES (?, ?, ?, ?)"
            val = (postcode, sales_rep_id, sales_rep_name, year)
            cursor.execute(sql, val)
            db.commit()
            self.show_message("Success", "Details inserted")
        except Exception as e:
            self.show_message("Error", f"Error inserting record: {str(e)}")
        finally:
            db.close()

    def modify_data(self, field, new_value, postcode):
        try:
            db = sqlite3.connect(self.database_path)
            cursor = db.cursor()
            sql = f"UPDATE '{self.table_name}' SET {field} = ? WHERE Postcode = ?"
            val = (new_value, postcode)
            cursor.execute(sql, val)
            db.commit()
            self.show_message("Success", "Record updated")
        finally:
            db.close()

    def delete_data(self, postcode):
        try:
            db = sqlite3.connect(self.database_path)
            cursor = db.cursor()
            sql_select = f"SELECT * FROM '{self.table_name}' WHERE Postcode = ?"
            val = (postcode,)
            cursor.execute(sql_select, val)
            row = cursor.fetchone()
            if not row:
                self.show_message("Error", "No record found with the given Postcode.")
                return
            confirmation = QMessageBox.question(self, 'Confirmation', f"Are you sure you want to delete this record?\n{str(row)}",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                sql_delete = f"DELETE FROM '{self.table_name}' WHERE Postcode = ?"
                cursor.execute(sql_delete, val)
                db.commit()
                self.show_message("Success", f"{cursor.rowcount} record(s) deleted.")
        finally:
            db.close()

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = DatabaseApp()
    ex.show()
    sys.exit(app.exec_())
