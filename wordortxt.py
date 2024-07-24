import sys
import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from docx import Document

class FileToSQLiteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File to SQLite Converter')
        self.setGeometry(100, 100, 400, 200)
        self.showMaximized()

        # Set background image
        palette = self.palette()
        background_image = QPixmap('./background_image.jpg')
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.addStretch(1)

        self.select_file_button = QPushButton('          Upload TXT or DOCX File        ', self)
        self.select_file_button.setStyleSheet('font-size: 18px; background: none;')
        self.select_file_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_button)

        self.select_db_button = QPushButton('            Select or Create DB File          ', self)
        self.select_db_button.setStyleSheet('font-size: 18px; background: none;')
        self.select_db_button.clicked.connect(self.select_db)
        layout.addWidget(self.select_db_button)

        self.convert_button = QPushButton('         Convert to DB       ', self)
        self.convert_button.setStyleSheet('font-size: 18px; background: none;')
        self.convert_button.clicked.connect(self.convert_to_sqlite)
        layout.addWidget(self.convert_button)
        layout.addStretch(1)

        hbox_main = QHBoxLayout()
        hbox_main.addStretch(1)
        hbox_main.addLayout(layout)
        hbox_main.addStretch(1)
        self.setLayout(hbox_main)

        self.file_path = None
        self.db_path = None

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload TXT or DOCX File", "", "Text Files (*.txt);;Word Documents (*.docx)", options=options)
        if file_path:
            self.file_path = file_path
            QMessageBox.information(self, "File Selected", f"Selected file: {file_path}")

    def select_db(self):
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
        options = QFileDialog.Options()
        db_path, _ = QFileDialog.getSaveFileName(self, "Create Database File", "", "SQLite Database (*.db)", options=options)
        if db_path:
            if os.path.exists(db_path):
                reply = QMessageBox.question(
                    self, 'File Exists', 'The selected database file already exists. Do you want to replace it?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return

            self.db_path = db_path
            if not self.db_path.lower().endswith('.db'):
                self.db_path += '.db'
            QMessageBox.information(self, "Database Selected", f"Selected database: {self.db_path}")

    def open_db_file(self):
        options = QFileDialog.Options()
        db_path, _ = QFileDialog.getOpenFileName(self, "Select Database File", "", "SQLite Database (*.db)", options=options)
        if db_path:
            self.db_path = db_path
            QMessageBox.information(self, "Database Selected", f"Selected database: {db_path}")

    def convert_to_sqlite(self):
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No file selected.")
            return
        if not self.db_path:
            QMessageBox.critical(self, "Error", "No database selected.")
            return

        if self.file_path.endswith('.txt'):
            data = self.read_txt_file(self.file_path)
        elif self.file_path.endswith('.docx'):
            data = self.read_docx_file(self.file_path)
        else:
            QMessageBox.critical(self, "Error", "Unsupported file type.")
            return

        sales_rep_name = 'Jane'
        filtered_data = self.filter_and_split_data(data, sales_rep_name)

        if filtered_data.empty:
            QMessageBox.critical(self, "Error", f"No data found for sales representative {sales_rep_name}.")
            return

        self.create_sqlite_db(self.db_path, "table1", filtered_data)
        QMessageBox.information(self, "Success", f"Data from {self.file_path} has been successfully inserted into {self.db_path}.")

    def read_txt_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines

    def read_docx_file(self, file_path):
        doc = Document(file_path)
        lines = [para.text.strip() for para in doc.paragraphs]
        return lines

    def filter_and_split_data(self, data, sales_rep_name):
        df = pd.DataFrame(data, columns=['line'])
        df[['Postcode', 'Sales_Rep_ID', 'Sales_Rep_Name', 'Year']] = df['line'].str.split('\t', expand=True)
        filtered_df = df[df['Sales_Rep_Name'] == sales_rep_name]
        return filtered_df

    def create_sqlite_db(self, db_name, table_name, data):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS 'table1' (Postcode INTEGER PRIMARY KEY, Sales_Rep_ID INTEGER, Sales_Rep_Name TEXT, Year INTEGER)")

        for _, row in data.iterrows():
            cursor.execute(f"INSERT INTO 'table1' (Postcode, Sales_Rep_ID, Sales_Rep_Name, Year) VALUES (?, ?, ?, ?)", 
                           (row['Postcode'], row['Sales_Rep_ID'], row['Sales_Rep_Name'], row['Year']))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FileToSQLiteApp()
    ex.show()
    sys.exit(app.exec_())
