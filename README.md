# File-to-Database Converter with GUI

**Developed By:** Mridul Das

---

## Project Overview

This Python-based project provides a user-friendly **graphical interface** to convert files (Excel, Text, Word) into a **SQLite database** and vice versa. It also supports database **viewing, searching, modifying**, and **generating reports** — all within a single application.

---

## Features & Menu Options

The main menu offers the following functionalities:

1. **Excel to Database**
2. **Text / DOCX to Database**
3. **Modify Database**
4. **View Database**
5. **Search Database**
6. **Database to Excel**
7. **Generate Reports**
8. **Exit**

---

## Functional Workflow

### Excel to Database

- User selects the Excel file and the destination database file.
- If the database doesn’t exist, a new one can be created.
- On clicking **"Import to DB"**, the app confirms successful data import.

### Text or DOCX to Database

- User selects a `.txt` or `.docx` file and the destination `.db` file.
- After setup, click **"Convert to DB"** to initiate the process.

### View Database

- Browse for a `.db` file.
- The database opens in a full-screen view showing all records and headers.

### Search Functionality

- Choose whether to search by **postcode** or **name**.
- Partial or unordered text inputs are supported.
- Results are shown in a separate window, with an option to search again.

### Modify Database

- Choose an existing database file.
- Perform any of the following:
  - **Add** a new record (requires all fields)
  - **Modify** existing records
  - **Delete** a record (with confirmation and preview)
- Validation prevents duplicate entries or editing non-existent records.

### Database to Excel

- Select a `.db` file.
- Export its contents to `.xlsx` with one click.

### Generate Reports

- Automatically generate reports/letters using pre-existing templates.
- Column headers in templates are replaced with database values.

---

## Types of Reports

- **Top Performers Report**
- **Best Salesperson Report**

---

## Code Overview

Main GUI built using **PyQt5**.

### Dependencies

- `PyQt5`
- `sqlite3`
- `pandas`
- `subprocess`
- `os`
- `sys`

---

## Key Classes & Responsibilities

### `ExcelToSQLiteApp(QWidget)`

- Imports Excel data into SQLite.
- Includes UI for browsing files and database interaction.

### `DatabaseApp(QWidget)`

- Handles CRUD operations.
- Includes methods: `add_data`, `modify_data`, `delete_data`.

### `DatabaseViewer(QWidget)`

- Displays database contents in a table format.

### `FetchDataApp(QWidget)`

- Enables keyword-based database search and displays filtered results.

### `DBToExcel(QWidget)`

- Exports SQLite data into Excel format.

### `MainWindow(QMainWindow)`

- Main entry point.
- Provides button-based access to all features.
- Loads background image and manages navigation to each component.

---

## How to Run

```bash
python app.py
```

The main application window will open. Click the respective buttons to use the different features.

---

## Notes

- Ensure all required packages are installed:
  ```bash
  pip install PyQt5 pandas
  ```
- Update file paths and table names as needed.
- Error messages and validations help ensure smooth operation.
