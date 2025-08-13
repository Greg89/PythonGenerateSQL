# CSV to SQL Converter

A Python program that converts CSV files to SQL INSERT statements for easy database table insertion.

## Features

- Converts CSV files to SQL INSERT statements
- **Smart folder detection** - automatically finds CSV files in `csv_input/` folder
- **Organized output** - saves SQL files to `sql_output/` folder by default
- **Flexible table naming** - supports regular tables and temporary tables (with `#`)
- Handles data type conversion and escaping
- Supports custom table names
- Generates clean, readable SQL output
- Handles empty values and NULLs appropriately
- Progress indicators for large files
- Command-line interface with helpful options

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed on your system
3. No additional package installation required

## Usage

### Basic Usage

```bash
# Show available CSV files
python sql_generator.py

# Process a CSV file (auto-detects csv_input/ folder)
python sql_generator.py input.csv

# This will create sql_output/input.sql with INSERT statements for a table named `table_name`
```

### Advanced Usage

```bash
# Specify custom table name
python sql_generator.py input.csv -t users

# Use temporary table (SQL Server) - automatically generates CREATE TABLE
python sql_generator.py input.csv -t #temp_users

# Specify custom output file
python sql_generator.py input.csv -o sql_output/users_insert.sql

# Specify both table name and output file
python sql_generator.py input.csv -t #temp_users -o sql_output/temp_users.sql

# Use explicit paths
python sql_generator.py csv_input/input.csv -o sql_output/output.sql
```

### Command Line Options

- `csv_file`: Input CSV file path (required)
- `-o, --output`: Output SQL file path (optional, defaults to input_name.sql)
- `-t, --table`: Target table name (optional, defaults to 'table_name')
  - Supports temporary table names with `#` (e.g., `#temp_table`)
  - Supports regular table names (e.g., `users`, `products`)
  - Global temporary tables (##) are not supported

## Example

### Input CSV (sample_data.csv)
```csv
id,name,email,age,city
1,John Doe,john.doe@email.com,30,New York
2,Jane Smith,jane.smith@email.com,25,Los Angeles
3,Bob Johnson,bob.johnson@email.com,35,Chicago
```

### Generated SQL

#### Regular Table
```sql
-- Generated SQL INSERT statements for table: users
-- Total rows: 3

INSERT INTO users (id, name, email, age, city) VALUES ('1', 'John Doe', 'john.doe@email.com', '30', 'New York');
INSERT INTO users (id, name, email, age, city) VALUES ('2', 'Jane Smith', 'jane.smith@email.com', '25', 'Los Angeles');
INSERT INTO users (id, name, email, age, city) VALUES ('3', 'Bob Johnson', 'bob.johnson@email.com', '35', 'Chicago');
```

#### Temporary Table
```sql
-- Generated SQL INSERT statements for table: #temp_users
-- Total rows: 3

-- CREATE TABLE statement for temporary table
CREATE TABLE #temp_users (
    id NVARCHAR(MAX),
    name NVARCHAR(MAX),
    email NVARCHAR(MAX),
    age NVARCHAR(MAX),
    city NVARCHAR(MAX)
);

-- INSERT statements:

INSERT INTO #temp_users (id, name, email, age, city) VALUES ('1', 'John Doe', 'john.doe@email.com', '30', 'New York');
INSERT INTO #temp_users (id, name, email, age, city) VALUES ('2', 'Jane Smith', 'jane.smith@email.com', '25', 'Los Angeles');
INSERT INTO #temp_users (id, name, email, age, city) VALUES ('3', 'Bob Johnson', 'bob.johnson@email.com', '35', 'Chicago');
```

## Features

### Data Handling
- Automatically detects column names from CSV header
- Handles BOM (Byte Order Mark) characters and other invisible Unicode characters
- Escapes single quotes in text values
- Converts empty strings to NULL
- Handles all data types as strings (safe for most databases)

### Output Format
- Clean, readable SQL statements
- Progress comments every 100 rows for large files
- Proper SQL syntax with semicolons
- Header comments with table name and row count

### Error Handling
- File not found errors
- CSV parsing errors
- Output file write errors
- Graceful error messages and exit codes

## Testing

The repository includes a sample CSV file (`sample_data.csv`) for testing:

```bash
python sql_generator.py sample_data.csv -t test_users
```

This will generate `sample_data.sql` with INSERT statements for the `test_users` table.

## Database Compatibility

The generated SQL is compatible with most SQL databases including:
- MySQL
- PostgreSQL
- SQLite
- SQL Server (including temporary tables with `#`)
- Oracle

### Temporary Tables
- **SQL Server**: Supports `#temp_table` (local temporary tables)
  - Automatically generates CREATE TABLE statements with NVARCHAR(MAX) columns
  - Global temporary tables (##) are not supported
- **Other databases**: Use regular table names or database-specific temporary table syntax

## Troubleshooting

### BOM Characters (U+FEFF)
If you encounter SQL parsing errors mentioning "Zero Width No-Break Space - U+FEFF", this program automatically handles these invisible Unicode characters that commonly appear in CSV files exported from Excel or other applications.

### Column Name Issues
The program automatically cleans column names by removing invisible characters and trimming whitespace to ensure clean SQL generation.

## Limitations

- All values are treated as strings (you may need to cast to appropriate types in your database)
- Large CSV files will generate large SQL files
- No support for batch INSERT statements (one INSERT per row)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is open source and available under the MIT License.
