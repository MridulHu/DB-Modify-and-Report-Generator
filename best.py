import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QMessageBox, QDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import sqlite3
from datetime import datetime

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate Letter")
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

        self.btn_generate_leave = QPushButton("Generate Leave Letter")
        self.btn_generate_leave.setStyleSheet('font-size: 18px; background: none;')
        self.btn_generate_leave.setFixedSize(300, 35)
        self.btn_generate_leave.clicked.connect(self.generate_leave_letter)
        layout.addWidget(self.btn_generate_leave, alignment=Qt.AlignCenter)

        self.btn_generate_resign = QPushButton("Generate Resignation Letter")
        self.btn_generate_resign.setStyleSheet('font-size: 18px; background: none;')
        self.btn_generate_resign.setFixedSize(300, 35)
        self.btn_generate_resign.clicked.connect(self.generate_resignation_letter)
        layout.addWidget(self.btn_generate_resign, alignment=Qt.AlignCenter)

        self.btn_generate_top_performers = QPushButton("Generate Top Performers File")
        self.btn_generate_top_performers.setStyleSheet('font-size: 18px; background: none;')
        self.btn_generate_top_performers.setFixedSize(300, 35)
        self.btn_generate_top_performers.clicked.connect(self.generate_top_performers_file)
        layout.addWidget(self.btn_generate_top_performers, alignment=Qt.AlignCenter)

        self.btn_generate_best_salesperson = QPushButton("Generate Best Salesperson File")
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

    def generate_leave_letter(self):
        dialog = LeaveDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.label_output.setText(f"Leave letter generated at: {dialog.generated_file_path}")
            self.display_file_content(dialog.generated_file_path)

    def generate_resignation_letter(self):
        dialog = ResignationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.label_output.setText(f"Updated resignation letter created at: {dialog.updated_file_path}")
            self.display_file_content(dialog.updated_file_path)

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


class LeaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate Leave Letter")
        self.setGeometry(200, 200, 500, 300)
        self.setWindowOpacity(1.0)

        self.initUI()
        self.generated_file_path = None

    def initUI(self):
        layout = QVBoxLayout(self)

        self.label_post_code = QLabel("Enter Post Code:")
        layout.addWidget(self.label_post_code)
        self.input_post_code = QLineEdit()
        layout.addWidget(self.input_post_code)

        self.label_start_date = QLabel("Enter start date (dd/mm/yy):")
        layout.addWidget(self.label_start_date)
        self.input_start_date = QLineEdit()
        layout.addWidget(self.input_start_date)

        self.label_leave_days = QLabel("Enter number of leave days:")
        layout.addWidget(self.label_leave_days)
        self.input_leave_days = QLineEdit()
        layout.addWidget(self.input_leave_days)

        self.btn_generate = QPushButton("Generate")
        self.btn_generate.setStyleSheet('font-size: 18px; background: none;')
        self.btn_generate.setFixedSize(300, 35)
        self.btn_generate.clicked.connect(self.generate_leave)
        layout.addWidget(self.btn_generate, alignment=Qt.AlignCenter)

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setStyleSheet('font-size: 18px; background: none;')
        self.btn_exit.setFixedSize(300, 35)
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit, alignment=Qt.AlignCenter)

        self.label_output = QLabel("")
        layout.addWidget(self.label_output, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def generate_leave(self):
        post_code = self.input_post_code.text()
        start_date = self.input_start_date.text()
        leave_days = int(self.input_leave_days.text())

        try:
            generated_file_path = generate_leave_letter('C:/Project/Leave.txt', 'C:/Project/db3.db', post_code, start_date, leave_days)
            self.generated_file_path = generated_file_path
            self.label_output.setText(f"Leave letter generated at: {generated_file_path}")
            self.accept()  # Close the dialog and return QDialog.Accepted
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class ResignationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate Resignation Letter")
        self.setGeometry(200, 200, 500, 300)
        self.setWindowOpacity(1.0)

        self.initUI()
        self.updated_file_path = None

    def initUI(self):
        layout = QVBoxLayout(self)

        self.label_post_code = QLabel("Enter Post Code:")
        layout.addWidget(self.label_post_code)
        self.input_post_code = QLineEdit()
        layout.addWidget(self.input_post_code)

        self.btn_generate = QPushButton("Generate")
        self.btn_generate.setStyleSheet('font-size: 18px; background: none;')
        self.btn_generate.setFixedSize(300, 35)
        self.btn_generate.clicked.connect(self.generate_resignation)
        layout.addWidget(self.btn_generate, alignment=Qt.AlignCenter)

        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setStyleSheet('font-size: 18px; background: none;')
        self.btn_exit.setFixedSize(300, 35)
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit, alignment=Qt.AlignCenter)

        self.label_output = QLabel("")
        layout.addWidget(self.label_output, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def generate_resignation(self):
        post_code = self.input_post_code.text()
        data = fetch_data(post_code)

        if data:
            try:
                with open(r'C:\Project\Resign.txt', 'r') as file:
                    letter_content = file.read()
                updated_letter = update_resignation_letter(letter_content, data)
                new_file_path = r'C:\Project\Resign_Updated.txt'
                with open(new_file_path, 'w') as file:
                    file.write(updated_letter)
                self.updated_file_path = new_file_path
                self.label_output.setText(f"Updated resignation letter created at: {new_file_path}")
                self.accept()  # Close the dialog and return QDialog.Accepted
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", f"No data found for Post Code: {post_code}")


def fetch_data(postcode):
    conn = sqlite3.connect(r'C:\Project\database1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Postcode, Sales_Rep_ID, Sales_Rep_Name, Year FROM table1 WHERE Postcode = ?", (postcode,))
    data = cursor.fetchone()
    conn.close()
    return data


def update_resignation_letter(letter_content, data):
    postcode, sales_rep_id, sales_rep_name, year = map(str, data)
    updated_letter = letter_content.replace('Postcode', postcode)
    updated_letter = updated_letter.replace('Sales_Rep_ID', sales_rep_id)
    updated_letter = updated_letter.replace('Sales_Rep_Name', sales_rep_name)
    updated_letter = updated_letter.replace('Year', year)
    return updated_letter


def generate_leave_letter(file_path, db_path, post_code, start_date, leave_days):
    details = get_sales_rep_details_by_post_code(db_path, post_code)
    if details is None:
        raise ValueError(f"No details found for Post Code: {post_code}")

    sales_rep_name = details["name"]
    sales_rep_id = str(details["id"])

    with open(file_path, 'r') as file:
        leave_letter = file.read()

    start_date_obj = datetime.strptime(start_date, '%d/%m/%y')
    end_date_obj = start_date_obj + timedelta(days=leave_days - 1)
    end_date = end_date_obj.strftime('%d/%m/%y')

    leave_letter = leave_letter.replace('[Sales_Rep_Name]', sales_rep_name)
    leave_letter = leave_letter.replace('[Your Sales Rep ID]', sales_rep_id)
    leave_letter = leave_letter.replace('[Your Post Code]', post_code)
    leave_letter = leave_letter.replace('[30/06/24]', start_date)
    leave_letter = leave_letter.replace('[end_date]', end_date)
    leave_letter = leave_letter.replace('[Postcode]', post_code)

    output_file_path = file_path.replace('.txt', '_filled.txt')

    with open(output_file_path, 'w') as file:
        file.write(leave_letter)

    return output_file_path


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


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
