import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox

class ExcelToSQLiteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Convert Excel to DB')
        self.setGeometry(100, 100, 500, 250)

        self.label_excel = QLabel('Select Excel file to import:', self)
        self.label_excel.setAlignment(Qt.AlignCenter)

        self.btn_select_file = QPushButton('Upload Excel File', self)
        self.btn_select_file.clicked.connect(self.select_excel_file)

        self.label_db = QLabel('Select or Create database file:', self)
        self.label_db.setAlignment(Qt.AlignCenter)

        self.btn_select_db = QPushButton('Name DB File', self)
        self.btn_select_db.clicked.connect(self.select_db_file)

        self.btn_import = QPushButton('Import to DB', self)
        self.btn_import.clicked.connect(self.import_to_sqlite)
        self.btn_import.setEnabled(False)  

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_excel)
        vbox.addWidget(self.btn_select_file)
        vbox.addWidget(self.label_db)
        vbox.addWidget(self.btn_select_db)
        vbox.addWidget(self.btn_import)

        self.setLayout(vbox)

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
        output_filepath, _ = QFileDialog.getSaveFileName(self, "Save Database File", "", "SQLite databases (*.db)")
        if output_filepath:
            self.db_path = output_filepath
            if not self.db_path.lower().endswith('.db'):
                self.db_path += '.db'  
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

            conn.execute(f"DROP TABLE IF EXISTS `{fixed_table_name}`")

            df.to_sql(fixed_table_name, conn, if_exists='append', index=False) 

            conn.commit()
            conn.close()

            QMessageBox.information(self, 'Success', 'Data imported successfully into SQLite.')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')

def main():
    try:
        app = QApplication(sys.argv)
        ex = ExcelToSQLiteApp()
        ex.show()
        sys.exit(app.exec_())

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
