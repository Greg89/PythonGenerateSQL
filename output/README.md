# SQL Output Folder

This folder contains the generated SQL INSERT statements from your CSV files.

## Purpose
- Generated SQL files are automatically saved here
- Keeps your output organized and separate from input data
- SQL files are ready to use in your database applications

## Contents
- SQL files with INSERT statements for database tables
- Each file corresponds to a processed CSV file
- Files are named based on the input CSV filename

## Usage
1. Run the generator with one of these methods:
   - `python sql_generator.py` (shows available CSV files)
   - `python sql_generator.py your_file.csv` (auto-detects folders)
   - `python sql_generator.py csv_input/your_file.csv` (explicit path)
2. SQL file will be automatically created here
3. Use the generated SQL in your database management tool

## File Format
- Standard SQL INSERT statements
- One INSERT per row from the CSV
- Properly escaped values and clean column names
- Compatible with most SQL databases

## Example
```
sql_output/
├── README.md
├── sample_data.sql
├── users.sql
└── products.sql
```

## Note
SQL files in this folder are ignored by Git to avoid uploading generated files to version control.
