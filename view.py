import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog

class DatabaseViewerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MD Database Viewer')
        self.initUI()

    def initUI(self):
        self.label = QLabel('Enter SQLite database file location:')
        self.entry = QLineEdit()
        self.button_browse = QPushButton('Browse')
        self.button_view = QPushButton('View Database')
        self.result_text = QTextEdit()
        self.table_entry = QLineEdit()
        self.table_name = 'table1'  # Fixed table name

        layout_entry = QHBoxLayout()
        layout_entry.addWidget(self.entry)
        layout_entry.addWidget(self.button_browse)

        layout_table_entry = QHBoxLayout()


        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_view)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.label)
        layout_main.addLayout(layout_entry)
        layout_main.addLayout(layout_table_entry)
        layout_main.addLayout(layout_buttons)
        layout_main.addWidget(self.result_text)

        self.setLayout(layout_main)

        self.button_browse.clicked.connect(self.browse_db_file)
        self.button_view.clicked.connect(self.view_database)
        self.entry.returnPressed.connect(self.view_database)  

    def browse_db_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('SQLite Database (*.db *.sqlite *.db3)')
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.entry.setText(file_path)

    def view_database(self):
        db_file = self.entry.text()

        if not db_file:
            QMessageBox.critical(self, 'Error', 'Please enter a database file location.')
            return

        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (self.table_name,))
            table_exists = cursor.fetchone()

            if not table_exists:
                QMessageBox.information(self, 'Info', f'Table "{self.table_name}" not found in the database.')
                conn.close()
                return

            result_text = ""

            columns = cursor.execute(f"PRAGMA table_info({self.table_name});").fetchall()
            column_names = [col[1] for col in columns]
            result_text += f"{', '.join(column_names)}\n"

            rows = cursor.execute(f"SELECT * FROM {self.table_name};").fetchall()
            for row in rows:
                result_text += ', '.join(map(str, row)) + "\n"
            result_text += "\n"

            conn.close()

            self.result_text.setPlainText(result_text)

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error', f'Error accessing database: {e}')

def main():
    app = QApplication(sys.argv)
    window = DatabaseViewerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
