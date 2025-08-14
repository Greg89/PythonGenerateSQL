# Data Input Folder

This folder is for storing data files (CSV, TXT, XML, JSON) that you want to convert to SQL INSERT statements.

## Purpose
- Place your data files here before running the SQL generator
- Keep your input data organized and separate from generated output
- Data files in this folder will be processed by `main.py`

## Usage
1. Copy or move your data files into this folder
2. Run the generator with one of these methods:
   - `python main.py` (shows available files)
   - `python main.py your_file.csv` (auto-detects input/ folder)
   - `python main.py input/your_file.csv` (explicit path)
3. The program automatically reads from this folder

## File Requirements
- **CSV files**: Should have headers in the first row, UTF-8 encoding (BOM characters are automatically handled)
- **TXT files**: Should have headers in the first row, tab or space separated, UTF-8 encoding
- **XML files**: Should have a single level of nesting, nested collections are excluded
- **JSON files**: Should have a single level of nesting, nested collections are excluded
- **Supported formats**: `.csv`, `.txt`, `.xml`, `.json`

## Example
```
input/
├── README.md
├── sample_data.csv
├── users.csv
├── products.txt
├── config.xml
└── data.json
```

## Note
Data files in this folder are ignored by Git to avoid uploading data files to version control.
