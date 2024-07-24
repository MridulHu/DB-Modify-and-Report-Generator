import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QMessageBox, QDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import sqlite3
from datetime import datetime

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate Letters and Files")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowOpacity(1.0)
        self.initUI()

    def set_background_image(self, image_path):
        palette = self.palette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def initUI(self):
        layout = QVBoxLayout(self)

        self.label_instruction = QLabel("\n")
        self.label_instruction.setStyleSheet('font-size: 18px;')
        layout.addWidget(self.label_instruction)

        self.btn_generate_top_performers = QPushButton("Generate Top Performers Report")
        self.btn_generate_top_performers.setStyleSheet('font-size: 18px; background: none;')
        self.btn_generate_top_performers.setFixedSize(300, 35)
        self.btn_generate_top_performers.clicked.connect(self.generate_top_performers_file)
        layout.addWidget(self.btn_generate_top_performers, alignment=Qt.AlignCenter)

        self.btn_generate_best_salesperson = QPushButton("Generate Best Salesperson Report")
        self.btn_generate_best_salesperson.setStyleSheet('font-size: 18px; background: none;')
        self.btn_generate_best_salesperson.setFixedSize(300, 35)
        self.btn_generate_best_salesperson.clicked.connect(self.generate_best_salesperson_file)
        layout.addWidget(self.btn_generate_best_salesperson, alignment=Qt.AlignCenter)

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setStyleSheet('font-size: 18px; background: none;')
        self.btn_exit.setFixedSize(300, 35)
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit, alignment=Qt.AlignCenter)

        self.label_output = QLabel("")
        self.label_output.setStyleSheet('font-size: 18px;')
        layout.addWidget(self.label_output)

        self.text_edit_output = QTextEdit()
        self.text_edit_output.setStyleSheet('font-size: 18px;')
        self.text_edit_output.setReadOnly(True)
        layout.addWidget(self.text_edit_output)

        self.setLayout(layout)
        self.showMaximized()
        self.set_background_image("C:/Project/background.jpg")

    def generate_top_performers_file(self):
        try:
            conn = sqlite3.connect('C:/Project/db3.db')
            cursor = conn.cursor()

            cursor.execute('SELECT Sales_Rep_ID, Sales_Rep_Name, Value, Postcode FROM table1 ORDER BY Value DESC LIMIT 10')
            top_salespersons = cursor.fetchall()

            conn.close()

            if top_salespersons:
                current_date = datetime.now().strftime('%Y-%m-%d')

                with open('C:/Project/top.txt', 'r') as file:
                    template = file.read()

                content_to_write = template
                for i in range(10):
                    Sales_Rep_ID = str(top_salespersons[i][0])
                    Sales_Rep_Name = str(top_salespersons[i][1])
                    Value = str(int(top_salespersons[i][2]))
                    Postcode = str(top_salespersons[i][3])

                    content_to_write = content_to_write.replace(f'[ID{i + 1}]', Sales_Rep_ID)
                    content_to_write = content_to_write.replace(f'[Name{i + 1}]', Sales_Rep_Name)
                    content_to_write = content_to_write.replace(f'[Value{i + 1}]', Value)
                    content_to_write = content_to_write.replace(f'[Postcode{i + 1}]', Postcode)

                with open('C:/Project/top_performers.txt', 'w') as file:
                    file.write(content_to_write)

                self.label_output.setText("The top_performers.txt file has been created successfully.")
                self.display_file_content('C:/Project/top_performers.txt')
            else:
                self.label_output.setText("No data found in the database.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def generate_best_salesperson_file(self):
        try:
            conn = sqlite3.connect('C:/Project/db3.db')
            cursor = conn.cursor()

            cursor.execute('SELECT Sales_Rep_Name, Postcode, Year, Value, Sales_Rep_ID FROM table1 ORDER BY Value DESC LIMIT 1')
            best_salesperson = cursor.fetchone()

            conn.close()

            if best_salesperson:
                Sales_Rep_Name, Postcode, Year, Value, Sales_Rep_ID = best_salesperson

                current_date = datetime.now().strftime('%Y-%m-%d')

                with open('C:/Project/best.txt', 'r') as file:
                    content = file.read()

                content = content.replace('[Sales_Rep_Name]', str(Sales_Rep_Name))
                content = content.replace('[Postcode]', str(Postcode))
                content = content.replace('[Year]', str(Year))
                content = content.replace('[Value]', str(int(Value)))
                content = content.replace('[Sales_Rep_ID]', str(Sales_Rep_ID))
                content = content.replace('[Date]', current_date)

                with open('C:/Project/best_updated.txt', 'w') as file:
                    file.write(content)

                self.label_output.setText("The best_updated.txt file has been created successfully.")
                self.display_file_content('C:/Project/best_updated.txt')
            else:
                self.label_output.setText("No data found in the database.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_file_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            self.text_edit_output.setPlainText(file_content)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
