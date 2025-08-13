# CSV Input Folder

This folder is for storing CSV files that you want to convert to SQL INSERT statements.

## Purpose
- Place your CSV files here before running the SQL generator
- Keep your input data organized and separate from generated output
- CSV files in this folder will be processed by `sql_generator.py`

## Usage
1. Copy or move your CSV files into this folder
2. Run the generator with one of these methods:
   - `python sql_generator.py` (shows available files)
   - `python sql_generator.py your_file.csv` (auto-detects csv_input/ folder)
   - `python sql_generator.py csv_input/your_file.csv` (explicit path)
3. The program automatically reads from this folder

## File Requirements
- CSV files should have headers in the first row
- Files should be in UTF-8 encoding (BOM characters are automatically handled)
- Supported formats: `.csv`

## Example
```
csv_input/
├── README.md
├── sample_data.csv
├── users.csv
└── products.csv
```

## Note
CSV files in this folder are ignored by Git to avoid uploading data files to version control.
