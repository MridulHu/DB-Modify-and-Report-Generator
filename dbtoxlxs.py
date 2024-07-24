import sys
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QLineEdit, QMessageBox


class FileConversionDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DB to XLSX Converter(MD)')

        self.layout = QVBoxLayout()

        self.label = QLabel("Click below to select a database file:")
        self.layout.addWidget(self.label)

        self.db_button = QPushButton('Select DB File')
        self.db_button.clicked.connect(self.selectDBFile)
        self.layout.addWidget(self.db_button)

        self.db_filepath_label = QLabel("")
        self.layout.addWidget(self.db_filepath_label)

        self.table_name = 'table1' 

        self.convert_button = QPushButton('Convert to XLSX')
        self.convert_button.clicked.connect(self.convertToXLSX)
        self.layout.addWidget(self.convert_button)

        self.save_filepath_label = QLabel("")
        self.layout.addWidget(self.save_filepath_label)

        self.setLayout(self.layout)

    def selectDBFile(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Select DB File", "", "All Files (*);;Database Files (*.db)", options=options)
        if filename:
            self.db_filepath_label.setText(filename)
            self.db_filepath = filename

    def convertToXLSX(self):
        if hasattr(self, 'db_filepath'):
            db_filepath = self.db_filepath

            try:
                conn = sqlite3.connect(db_filepath)
                df = pd.read_sql(f"SELECT * FROM {self.table_name}", conn)
                output_filepath, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")
                if output_filepath:
                    df.to_excel(output_filepath, index=False)   
                    self.save_filepath_label.setText(f"File saved: {output_filepath}")
                else:
                    self.save_filepath_label.setText("File save canceled")
            except Exception as e:
                self.save_filepath_label.setText(f"Error converting file: {str(e)}")
        else:
            self.save_filepath_label.setText("Please select a database file first")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FileConversionDialog()
    dialog.show()
    sys.exit(app.exec_())
