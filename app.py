import subprocess
import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QPainter
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QLineEdit, QTextEdit, QGridLayout, QGroupBox,
    QRadioButton, QMainWindow
)
from report import MainWindow

# Excel to SQLite App
class ExcelToSQLiteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Convert Excel to DataBase')
        self.setGeometry(100, 100, 500, 300)
        self.showMaximized()

        # Set background image for the central widget
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(self.backgroundRole(), QBrush(QPixmap('./xtodb.jpg')))
        self.setPalette(p)

        self.label_excel = QLabel('Select Excel file to import:', self)
        self.label_excel.setAlignment(Qt.AlignCenter)
        self.label_excel.setStyleSheet('font-size: 18px;')

        self.btn_select_file = QPushButton('Upload Excel File', self)
        self.btn_select_file.setStyleSheet('font-size: 18px; background: none;')
        self.btn_select_file.clicked.connect(self.select_excel_file)

        self.label_db = QLabel('Select or Create database file:', self)
        self.label_db.setAlignment(Qt.AlignCenter)
        self.label_db.setStyleSheet('font-size: 18px;')

        self.btn_select_db = QPushButton('Select/Create DataBase File', self)
        self.btn_select_db.setStyleSheet('font-size: 18px; background: none;')
        self.btn_select_db.clicked.connect(self.select_db_file)

        self.btn_import = QPushButton('Import to DataBase', self)
        self.btn_import.setStyleSheet('font-size: 18px; background: none;')
        self.btn_import.clicked.connect(self.import_to_sqlite)
        self.btn_import.setEnabled(False)

        # Central widget layout
        vbox_center = QVBoxLayout()
        vbox_center.addStretch(1)
        vbox_center.addWidget(self.label_excel)
        vbox_center.addWidget(self.btn_select_file)
        vbox_center.addWidget(self.label_db)
        vbox_center.addWidget(self.btn_select_db)
        vbox_center.addWidget(self.btn_import)
        vbox_center.addStretch(1)

        hbox_main = QHBoxLayout()
        hbox_main.addStretch(1)
        hbox_main.addLayout(vbox_center)
        hbox_main.addStretch(1)

        self.setLayout(hbox_main)
        
    def select_excel_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Excel files (*.xlsx)")
        file_dialog.selectFile("*.xlsx")

        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.file_path = file_paths[0]
                self.label_excel.setText(f'Selected Excel file: {os.path.basename(self.file_path)}')
                self.check_import_enable()

    def select_db_file(self):
        reply = QMessageBox.question(
            self, 'Select or Create Database',
            'Do you want to create a new database file?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.create_db_file()
        else:
            self.open_db_file()

    def create_db_file(self):
        output_filepath, _ = QFileDialog.getSaveFileName(self, "Create Database File", "", "SQLite databases (*.db)")
        if output_filepath:
            if os.path.exists(output_filepath):
                reply = QMessageBox.question(
                    self, 'File Exists', 'The selected database file already exists. Do you want to replace it?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return

            self.db_path = output_filepath
            if not self.db_path.lower().endswith('.db'):
                self.db_path += '.db'
            self.label_db.setText(f'Selected DB file: {os.path.basename(self.db_path)}')
            self.check_import_enable()

    def open_db_file(self):
        output_filepath, _ = QFileDialog.getOpenFileName(self, "Select Database File", "", "SQLite databases (*.db)")
        if output_filepath:
            self.db_path = output_filepath
            self.label_db.setText(f'Selected DB file: {os.path.basename(self.db_path)}')
            self.check_import_enable()

    def check_import_enable(self):
        if hasattr(self, 'file_path') and hasattr(self, 'db_path'):
            self.btn_import.setEnabled(True)
        else:
            self.btn_import.setEnabled(False)

    def import_to_sqlite(self):
        try:
            fixed_table_name = 'table1'  

            df = pd.read_excel(self.file_path)

            conn = sqlite3.connect(self.db_path)

            conn.execute(f"DROP TABLE IF EXISTS {fixed_table_name}")

            df.to_sql(fixed_table_name, conn, if_exists='append', index=False) 

            conn.commit()
            conn.close()

            QMessageBox.information(self, 'Success', 'Data imported successfully into SQLite.')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')

# Database Operations App

import sqlite3

class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Database Operations')
        self.database_path = self.get_database_file_path()
        self.table_name = 'table1'
        self.initUI()
        self.showMaximized()

    def get_database_file_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select Database File", "",
                                                  "Database Files (*.db *.sqlite *.sqlite3);;All Files (*)",
                                                  options=options)
        return filename

    def initUI(self):
        layout = QVBoxLayout()
        layout.addStretch(1)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(self.backgroundRole(), QBrush(QPixmap('./modify.jpg')))
        self.setPalette(p)
        operation_group = QGroupBox('Select an operation:')
        operation_group.setStyleSheet('font-size: 18px;')
        self.add_radio = QRadioButton('Add')
        self.add_radio.setStyleSheet('font-size: 18px;')
        self.modify_radio = QRadioButton('Modify')
        self.modify_radio.setStyleSheet('font-size: 18px;')
        self.delete_radio = QRadioButton('Delete')
        self.delete_radio.setStyleSheet('font-size: 18px;')

        operation_layout = QVBoxLayout()
        operation_layout.addWidget(self.add_radio)
        operation_layout.addWidget(self.modify_radio)
        operation_layout.addWidget(self.delete_radio)
        operation_group.setLayout(operation_layout)
        layout.addWidget(operation_group)

        input_group = QGroupBox('Input Fields:')
        input_group.setStyleSheet('font-size: 18px;')
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

        self.execute_button = QPushButton('Execute')
        self.execute_button.setStyleSheet('font-size: 18px; background: none;')
        self.execute_button.clicked.connect(self.button_click)
        layout.addWidget(self.execute_button)

        layout.addStretch(1)

        hbox_main = QHBoxLayout()
        hbox_main.addStretch(1)
        hbox_main.addLayout(layout)
        hbox_main.addStretch(1)

        self.setLayout(hbox_main)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.button_click()

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
        elif choice == 2:
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
        elif choice == 3:
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
# Database Viewer App

class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Database Viewer')
        self.setGeometry(100, 100, 800, 600)  # Set initial window size
        self.showMaximized()
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet('font-size: 18px;')
        
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.text_edit)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Create exit button
        exit_button = QPushButton('Exit', self)
        exit_button.clicked.connect(self.close)

        # Add exit button to toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addWidget(exit_button)

        self.database_path = self.get_database_file_path()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.load_database_data(self.database_path)

    def get_database_file_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select Database File", "",
                                                  "Database Files (*.db *.sqlite *.sqlite3);;All Files (*)",
                                                  options=options)
        if filename:
            self.load_database_data(filename)
        return filename

    def load_database_data(self, db_path):
        try:
            self.database_path = db_path
            conn = sqlite3.connect(self.database_path)
            df = pd.read_sql_query("SELECT * FROM table1", conn)

            df = df.loc[(df != 0).any(axis=1)]

            if not df.empty:
                self.text_edit.clear()
                self.text_edit.append(f"Total rows after filtering: {len(df)}\n\n")
                self.text_edit.append(df.to_string(index=True))
            else:
                self.text_edit.clear()
                self.text_edit.append("No data found after filtering.")
        except Exception as e:
            self.text_edit.clear()
            self.text_edit.append(f"Error fetching data: {str(e)}")
        finally:
            conn.close()
            
#Data Search

class FetchDataApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search DataBase')
        self.background_image = QPixmap('image.jpg')
        self.initUI()

    def initUI(self):
        self.db_location = None
        self.table_name = 'table1'
        self.showMaximized()

        layout = QVBoxLayout()
        radio_layout = QHBoxLayout()

        layout.addStretch(1)
        radio_layout.addStretch(1)
        select_db_button = QPushButton('Select Database')
        select_db_button.setStyleSheet('font-size: 18px;')
        select_db_button.clicked.connect(self.select_database)
        layout.addWidget(select_db_button)

        self.postcode_radio = QRadioButton('Search by Postcode')
        self.postcode_radio.setStyleSheet('font-size: 18px;')
        self.sales_rep_radio = QRadioButton('Search by Sales Rep Name')
        self.sales_rep_radio.setStyleSheet('font-size: 18px;')

        self.postcode_radio.setChecked(True)
        self.search_option = 'postcode'
        self.postcode_radio.toggled.connect(lambda: self.radio_button_checked('postcode'))
        self.sales_rep_radio.toggled.connect(lambda: self.radio_button_checked('sales_rep'))

        radio_layout.addWidget(self.postcode_radio)
        radio_layout.addWidget(self.sales_rep_radio)
        radio_layout.addLayout(layout)

        self.postcode_label = QLabel('Enter Postcode:')
        self.postcode_label.setStyleSheet('font-size: 18px;')
        layout.addWidget(self.postcode_label)
        self.postcode_input = QLineEdit()
        self.postcode_input.setStyleSheet('font-size: 18px;')
        layout.addWidget(self.postcode_input)
        self.postcode_input.returnPressed.connect(self.fetch_data)

        self.sales_rep_label = QLabel('Enter Sales Rep Name:')
        self.sales_rep_label.setStyleSheet('font-size: 18px;')
        layout.addWidget(self.sales_rep_label)
        self.sales_rep_input = QLineEdit()
        self.sales_rep_input.setStyleSheet('font-size: 18px;')
        layout.addWidget(self.sales_rep_input)
        self.sales_rep_input.returnPressed.connect(self.fetch_data)

        search_button = QPushButton('Search')
        search_button.setStyleSheet('font-size: 18px;')
        search_button.clicked.connect(self.fetch_data)
        layout.addWidget(search_button)
        radio_layout.addStretch(1)
        layout.addStretch(1)
        self.setLayout(radio_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.fetch_data()

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
        self.db_location, _ = QFileDialog.getOpenFileName(self, "Select SQLite database file", "./", "SQLite Database Files (*.db)", options=options)

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

# DB to Excel App
class DBToExcel(QWidget):
    def __init__(self):
        super().__init__()
        self.background_image = QPixmap('xtodb.jpg')
        self.initUI()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

    def initUI(self):
        self.setWindowTitle('Export DB to Excel')
        self.setGeometry(100, 100, 500, 300)
        self.showMaximized()

        self.label_db = QLabel('              Select database file:           ', self)
        self.label_db.setAlignment(Qt.AlignCenter)
        self.label_db.setStyleSheet('font-size: 18px;')

        self.btn_select_db = QPushButton('               Select DB File              ', self)
        self.btn_select_db.setStyleSheet('font-size: 18px;')
        self.btn_select_db.clicked.connect(self.select_db_file)

        self.btn_export = QPushButton('             Export to Excel              ', self)
        self.btn_export.setStyleSheet('font-size: 18px;')
        self.btn_export.clicked.connect(self.export_to_excel)
        self.btn_export.setEnabled(False)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.label_db)
        vbox.addWidget(self.btn_select_db)
        vbox.addWidget(self.btn_export)
        vbox.addStretch(1)

        hbox_main = QHBoxLayout()
        hbox_main.addStretch(1)
        hbox_main.addLayout(vbox)
        hbox_main.addStretch(1)
        self.setLayout(hbox_main)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.btn_export.isEnabled():
                self.export_to_excel()

    def select_db_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Database files (*.db *.sqlite *.sqlite3)")
        file_dialog.selectFile("*.db")

        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.db_path = file_paths[0]
                self.label_db.setText(f'Selected DB file: {os.path.basename(self.db_path)}')
                self.btn_export.setEnabled(True)

    def export_to_excel(self):
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM table1", conn)
            conn.close()

            file_name, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel files (*.xlsx)")
            if file_name:
                if not file_name.lower().endswith('.xlsx'):
                    file_name += '.xlsx'
                df.to_excel(file_name, index=False)
                QMessageBox.information(self, 'Success', 'Data exported successfully to Excel.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Database Tools')
        self.setGeometry(100, 100, 300, 200)

        btn_excel_to_db = QPushButton('Excel to DataBase', self)
        btn_excel_to_db.setStyleSheet('font-size: 18px;')
        btn_excel_to_db.setFixedSize(300, 35)  

        btn_execute_script = QPushButton('Upload Text or Docx', self)
        btn_execute_script.setStyleSheet('font-size: 18px;')
        btn_execute_script.setFixedSize(300, 35)

        btn_db_operations = QPushButton('Modify DataBase', self)
        btn_db_operations.setStyleSheet('font-size: 18px;')
        btn_db_operations.setFixedSize(300, 35)

        btn_db_viewer = QPushButton('DataBase Viewer', self)
        btn_db_viewer.setStyleSheet('font-size: 18px;')
        btn_db_viewer.setFixedSize(300, 35)

        btn_db_to_excel = QPushButton('DataBase to Excel', self)
        btn_db_to_excel.setStyleSheet('font-size: 18px;')
        btn_db_to_excel.setFixedSize(300, 35)

        btn_fetch_data = QPushButton('Search DataBase', self)
        btn_fetch_data.setStyleSheet('font-size: 18px;')
        btn_fetch_data.setFixedSize(300, 35)

        btn_generate_letters = QPushButton('Generate Report', self)
        btn_generate_letters.setStyleSheet('font-size: 18px;')
        btn_generate_letters.setFixedSize(300, 35)

        btn_exit = QPushButton('Exit', self)
        btn_exit.setStyleSheet('font-size: 18px;')
        btn_exit.setFixedSize(300, 35)

        btn_excel_to_db.clicked.connect(self.open_excel_to_db)
        btn_execute_script.clicked.connect(self.execute_external_script)
        btn_db_operations.clicked.connect(self.open_db_operations)
        btn_db_viewer.clicked.connect(self.open_db_viewer)
        btn_db_to_excel.clicked.connect(self.open_db_to_excel)
        btn_fetch_data.clicked.connect(self.open_fetch_data)
        btn_generate_letters.clicked.connect(self.open_letter_generation)
        btn_exit.clicked.connect(self.close)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addStretch(1) 
        vbox.addWidget(btn_excel_to_db)
        vbox.addWidget(btn_execute_script)
        vbox.addWidget(btn_db_operations)
        vbox.addWidget(btn_db_viewer)
        vbox.addWidget(btn_fetch_data)  
        vbox.addWidget(btn_db_to_excel)
        vbox.addWidget(btn_generate_letters)
        vbox.addWidget(btn_exit)
        vbox.addStretch(1)  

        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.showMaximized()

        self.set_background_image("./background_image.jpg")

    def set_background_image(self, image_path):
        palette = self.palette()
        pixmap = QPixmap(image_path)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def open_excel_to_db(self):
        self.excel_to_db_app = ExcelToSQLiteApp()
        self.excel_to_db_app.show()

    def open_db_operations(self):
        self.db_operations_app = DatabaseApp()
        self.db_operations_app.show()

    def open_db_viewer(self):
        self.db_viewer_app = DatabaseViewer()
        self.db_viewer_app.show()

    def open_db_to_excel(self):
        self.db_to_excel_app = DBToExcel()
        self.db_to_excel_app.show()

    def open_fetch_data(self):
        self.fetch_data_app = FetchDataApp()
        self.fetch_data_app.show()
    
    def open_letter_generation(self):
        self.letter_generation_app = MainWindow() 
        self.letter_generation_app.show()

    def execute_external_script(self):
        try:
            subprocess.run(['python', 'wordortxt.py'])
        except Exception as e:
            print(f"Error executing external script: {e}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainApp()
    demo.show()
    sys.exit(app.exec_())
