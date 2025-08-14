# Data to SQL Converter

A Python program that converts CSV, TXT, XML, and JSON files to SQL INSERT statements for easy database table insertion.

## Features

- Converts CSV, TXT, XML, and JSON files to SQL INSERT statements
- **Smart folder detection** - automatically finds data files in `input/` folder
- **Organized output** - saves SQL files to `output/` folder by default
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
# Show available data files
python main.py

# Process a data file (auto-detects input/ folder)
python main.py input.csv

# Process different file formats
python main.py data.txt
python main.py config.xml
python main.py users.json

# This will create output/input.sql with INSERT statements for a table named `table_name`
```

### Advanced Usage

```bash
# Specify custom table name
python main.py input.csv -t users

# Use temporary table (SQL Server) - automatically generates CREATE TABLE
python main.py input.csv -t #temp_users

# Specify custom output file
python main.py input.csv -o output/users_insert.sql

# Specify both table name and output file
python main.py input.csv -t #temp_users -o output/temp_users.sql

# Use explicit paths
python main.py input/input.csv -o output/output.sql
```

### Command Line Options

- `csv_file`: Input CSV file path (optional, defaults to showing available files)
- `-o, --output`: Output SQL file path (optional, defaults to input_name.sql)
- `-t, --table`: Target table name (optional, defaults to 'table_name')
  - Supports temporary table names with `#` (e.g., `#temp_table`)
  - Supports regular table names (e.g., `users`, `products`)
  - Global temporary tables (##) are not supported
- `-c, --config`: Configuration file path (optional, defaults to config.json)
- `--create-config`: Create sample configuration file
- `--interactive`: Run in interactive mode for guided operation
- `--preset`: Use named preset (quick, detailed, minimal)

## Example

### Input Data (sample_data.csv)
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
- Automatically detects column names from file headers (CSV, TXT) or structure (XML, JSON)
- Handles BOM (Byte Order Mark) characters and other invisible Unicode characters
- Escapes single quotes in text values
- Converts empty strings to NULL
- Handles all data types as strings (safe for most databases)
- Intelligently flattens nested objects while excluding collections

### Output Format
- Clean, readable SQL statements
- Progress comments every 100 rows for large files
- Proper SQL syntax with semicolons
- Header comments with table name and row count

### Error Handling
- File not found errors
- File format parsing errors (CSV, TXT, XML, JSON)
- Output file write errors
- Graceful error messages and exit codes

## Testing

The repository includes sample data files for testing:

```bash
# Test CSV format
python main.py sample_data.csv -t test_users

# Test TXT format
python main.py sample_data.txt -t txt_users

# Test XML format
python main.py sample_data.xml -t xml_users

# Test JSON format
python main.py sample_data.json -t json_users
```

These will generate SQL files with INSERT statements for the respective tables.

## Supported File Formats

The converter now supports multiple file formats:

### CSV Files
- Standard comma-separated values
- Automatic encoding detection (UTF-8, UTF-8-BOM)
- Handles BOM characters and invisible Unicode characters

### TXT Files
- Tab-separated or space-separated values
- Automatic separator detection
- First line treated as header

### XML Files
- Single level of nesting supported
- Nested collections are excluded (set to NULL)
- Direct child elements are extracted as columns

### JSON Files
- Single level of nesting supported
- Nested collections are excluded (set to NULL)
- Supports both single objects and arrays of objects
- Nested objects are flattened with underscore-separated keys

### Nested Collection Handling
For XML and JSON files, the converter implements intelligent nested data handling:
- **Direct properties**: Extracted normally as columns
- **Nested objects**: Flattened with underscore-separated keys
- **Nested collections**: Excluded and set to NULL
- **Parent columns**: Preserved but with NULL values for nested collections

## New Features

### Configuration Management
```bash
# Create a sample configuration file
python main.py --create-config

# Use a specific configuration file
python main.py -c my_config.json

# Use a preset configuration
python main.py --preset quick
python main.py --preset detailed
python main.py --preset minimal
```

### Interactive Mode
```bash
# Run in interactive mode for guided operation
python main.py --interactive
```

### Advanced Usage Examples
```bash
# Show available data files without processing
python main.py

# Process different file formats with custom config and table name
python main.py data.csv -c production.json -t production_users
python main.py users.xml -c production.json -t production_users
python main.py config.json -c production.json -t production_users

# Use interactive mode with preset
python main.py --interactive --preset quick
```

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

### File Format Issues
- **TXT files**: Ensure first line contains headers, use consistent separators (tab or space)
- **XML files**: Ensure single level of nesting, nested collections will be excluded
- **JSON files**: Ensure single level of nesting, nested collections will be excluded

## Limitations

- All values are treated as strings (you may need to cast to appropriate types in your database)
- Large data files will generate large SQL files
- No support for batch INSERT statements (one INSERT per row)
- XML and JSON support limited to single level of nesting
- Nested collections are excluded and set to NULL

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is open source and available under the MIT License.
