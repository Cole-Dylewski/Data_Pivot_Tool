# Data Pivot Tool

A professional GUI application for converting data from horizontal (wide) to vertical (long) format. Built with Python, Tkinter, and pandas, this tool simplifies the process of reshaping datasets for analysis, reporting, and data processing workflows.

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Data Cleaning Options](#-data-cleaning-options)
- [File Format Support](#-file-format-support)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [License](#-license)

## Features

- **Intuitive GUI**: User-friendly interface built with Tkinter for easy data transformation
- **Flexible Key Field Selection**: Choose which columns to preserve as identifiers
- **Advanced Data Cleaning**: Multiple options to filter and clean data during conversion
- **Large File Support**: Handles large datasets efficiently with batch processing
- **Automatic File Splitting**: Automatically splits exports exceeding 999,999 records
- **Real-time Preview**: Preview converted data before exporting
- **Dual View Display**: Simultaneously view input and output data in scrollable tables
- **Memory Monitoring**: Track memory usage for both input and output datasets
- **Multiple Format Support**: Import from Excel (`.xlsx`) and CSV (`.csv`) files

## Requirements

- Python 3.6 or higher
- pandas
- openpyxl (for Excel file support)
- tkinter (usually included with Python)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Data_Pivot_Tool.git
   cd Data_Pivot_Tool
   ```

2. **Install required dependencies:**
   ```bash
   pip install pandas openpyxl
   ```

   Note: `tkinter` is typically included with Python installations. If you encounter issues, install it using your system's package manager:
   - **Ubuntu/Debian**: `sudo apt-get install python3-tk`
   - **macOS**: `brew install python-tk`
   - **Windows**: Usually pre-installed with Python

3. **Run the application:**
   ```bash
   python core.py
   ```

## Usage

### Step-by-Step Guide

1. **Load Your Data**
   - Click `File` → `Load` from the menu bar
   - Select your data file (`.xlsx` or `.csv` format)
   - The input data will be displayed in the top table

2. **Select Key Fields**
   - In the left panel, select the columns you want to preserve as key fields
   - These columns will remain as identifiers in the output
   - All other columns will be pivoted into rows

3. **Configure Data Cleaning Options** (Optional)
   - **Remove**: Enter a custom string value to remove from the dataset
   - **: 0**: Remove all zero values
   - **: NULL**: Remove all null/NaN values
   - **: -**: Remove dash (`-`) placeholder values
   - **: \***: Remove asterisk (`*`) placeholder values
   - **: Duplicates**: Remove duplicate rows (all values must be identical)

4. **Preview the Output**
   - Click `File` → `Preview` to see the converted data
   - Review the output in the bottom table
   - Check the status messages for record counts and memory usage

5. **Export the Data**
   - Click `File` → `Extract` to save the converted data
   - Choose a save location and filename
   - The file will be saved as CSV format
   - If the output exceeds 999,999 records, multiple split files will be created automatically

## How It Works

The application uses pandas' `melt()` function to transform data from wide to long format:

- **Input Format (Horizontal/Wide):**
  ```
  ID  | Name  | Jan | Feb | Mar
  ----|-------|-----|-----|-----
  1   | John  | 100 | 150 | 200
  2   | Jane  | 120 | 130 | 180
  ```

- **Output Format (Vertical/Long):**
  ```
  ID  | Name  | Code | Values
  ----|-------|------|-------
  1   | John  | Jan  | 100
  1   | John  | Feb  | 150
  1   | John  | Mar  | 200
  2   | Jane  | Jan  | 120
  2   | Jane  | Feb  | 130
  2   | Jane  | Mar  | 180
  ```

The transformation process:
1. Preserves selected key fields as identifier columns
2. Converts all other columns into a `Code` column (column names) and `Values` column (cell values)
3. Applies data cleaning filters as specified
4. Sorts the output by key fields
5. Removes duplicates if enabled

## Data Cleaning Options

| Option | Description |
|--------|-------------|
| **Remove** | Custom text field to remove specific string values matching your input |
| **: 0** | Removes all zero values from the dataset |
| **: NULL** | Removes all null/NaN values (pandas `pd.notnull()` check) |
| **: -** | Removes dash (`-`) characters used as placeholders |
| **: \*** | Removes asterisk (`*`) characters used as placeholders |
| **: Duplicates** | Removes rows where all values are identical (uses `drop_duplicates()`) |

## File Format Support

### Input Formats
- **Excel (`.xlsx`)**: Full support via `pandas.read_excel()`
- **CSV (`.csv`)**: Full support via `pandas.read_csv()`

### Output Format
- **CSV (`.csv`)**: All exports are saved as CSV files

### Large File Handling
- Files exceeding 999,999 records are automatically split into multiple files
- Split files are named: `filename 1 of N.csv`, `filename 2 of N.csv`, etc.
- A master file containing all records is also created

## Technical Details

### Architecture
- **GUI Framework**: Tkinter with ttk widgets
- **Data Processing**: pandas DataFrame operations
- **Batch Processing**: Large datasets are processed in chunks (10% increments) to manage memory
- **Memory Management**: Real-time memory usage tracking and reporting

### Performance
- Processes data in batches to optimize memory usage
- Displays up to 100 rows in preview tables for performance
- Efficient pandas operations for data transformation

### Key Functions
- `loadFile()`: Loads and parses input files
- `buildData()`: Performs the pivot transformation
- `buildPreview()`: Generates preview of converted data
- `exportData()`: Exports data to CSV with automatic splitting
- `removeValues()`: Applies data cleaning filters
- `buildTables()`: Renders data in tree view widgets

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [pandas](https://pandas.pydata.org/) for data manipulation
- GUI created with Python's [tkinter](https://docs.python.org/3/library/tkinter.html)

---

**Version**: 2.0  
**Last Updated**: 2024

For issues, questions, or suggestions, please open an issue on GitHub.
