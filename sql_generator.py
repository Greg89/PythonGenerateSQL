#!/usr/bin/env python3
"""
CSV to SQL Converter
Converts CSV files to SQL INSERT statements for database table insertion.
"""

import csv
import argparse
import os
import sys
import json
from typing import List, Dict, Any
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "input_directory": "csv_input",
    "output_directory": "sql_output",
    "default_table_name": "table_name",
    "auto_detect_encoding": True,
    "batch_size": 100,
    "include_create_table": True,
    "sql_dialect": "sqlserver",  # sqlserver, mysql, postgresql
    "date_format": "YYYY-MM-DD",
    "null_values": ["", "NULL", "null", "None", "none"],
    "max_rows_per_file": 10000,
    "verbose": True
}

def load_config(config_file: str = None) -> Dict[str, Any]:
    """
    Load configuration from file or create default.

    Args:
        config_file (str): Path to configuration file

    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()

    # Try to load from specified config file
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                config.update(user_config)
                print(f"📋 Loaded configuration from: {config_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not load config file {config_file}: {e}")
            print("   Using default configuration")

    # Try to load from default config location
    elif os.path.exists("config.json"):
        try:
            with open("config.json", 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                config.update(user_config)
                print(f"📋 Loaded configuration from: config.json")
        except Exception as e:
            print(f"⚠️  Warning: Could not load default config.json: {e}")

    return config

def save_config(config: Dict[str, Any], config_file: str = "config.json") -> None:
    """
    Save configuration to file.

    Args:
        config (Dict[str, Any]): Configuration to save
        config_file (str): Path to save configuration
    """
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"💾 Configuration saved to: {config_file}")
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")

def create_sample_config() -> None:
    """Create a sample configuration file."""
    sample_config = {
        "input_directory": "csv_input",
        "output_directory": "sql_output",
        "default_table_name": "table_name",
        "auto_detect_encoding": True,
        "batch_size": 100,
        "include_create_table": True,
        "sql_dialect": "sqlserver",
        "date_format": "YYYY-MM-DD",
        "null_values": ["", "NULL", "null", "None", "none"],
        "null_values": ["", "NULL", "null", "None", "none"],
        "max_rows_per_file": 10000,
        "verbose": True,
        "custom_settings": {
            "example_feature": "value",
            "another_option": True
        }
    }

    save_config(sample_config, "config_sample.json")
    print("📝 Sample configuration file created: config_sample.json")
    print("   Copy this to config.json and modify as needed")

def apply_preset(config: Dict[str, Any], preset_name: str) -> Dict[str, Any]:
    """
    Apply a named preset configuration.

    Args:
        config (Dict[str, Any]): Base configuration
        preset_name (str): Name of preset to apply

    Returns:
        Dict[str, Any]: Modified configuration
    """
    presets = {
        "quick": {
            "verbose": False,
            "batch_size": 1000,
            "include_create_table": False,
            "max_rows_per_file": 5000
        },
        "detailed": {
            "verbose": True,
            "batch_size": 50,
            "include_create_table": True,
            "max_rows_per_file": 1000
        },
        "minimal": {
            "verbose": False,
            "batch_size": 5000,
            "include_create_table": False,
            "max_rows_per_file": 50000
        }
    }

    if preset_name in presets:
        config.update(presets[preset_name])
        print(f"🎯 Applied '{preset_name}' preset")
    else:
        print(f"⚠️  Unknown preset '{preset_name}'. Available: {', '.join(presets.keys())}")

    return config

def interactive_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Interactive configuration mode.

    Args:
        config (Dict[str, Any]): Base configuration

    Returns:
        Dict[str, Any]: Modified configuration
    """
    print("🔧 Interactive Configuration Mode")
    print("Press Enter to keep current values, or type new values:")

    try:
        # Table name
        new_table = input(f"Table name [{config['default_table_name']}]: ").strip()
        if new_table:
            config['default_table_name'] = new_table

        # SQL dialect
        new_dialect = input(f"SQL dialect [{config['sql_dialect']}]: ").strip()
        if new_dialect in ['sqlserver', 'mysql', 'postgresql']:
            config['sql_dialect'] = new_dialect

        # Batch size
        new_batch = input(f"Batch size [{config['batch_size']}]: ").strip()
        if new_batch.isdigit():
            config['batch_size'] = int(new_batch)

        # Verbose mode
        verbose_input = input(f"Verbose mode [{config['verbose']}]: ").strip().lower()
        if verbose_input in ['true', 'false', 'yes', 'no']:
            config['verbose'] = verbose_input in ['true', 'yes']

        print("✅ Configuration updated!")

    except KeyboardInterrupt:
        print("\n⚠️  Configuration cancelled, using defaults")

    return config


def read_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Read CSV file and return list of dictionaries.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        List[Dict[str, Any]]: List of dictionaries where each dict represents a row
    """
    try:
        # Try to read with UTF-8-BOM first to handle BOM characters
        with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]

            # Clean column names by removing BOM and other invisible characters
            if data:
                cleaned_data = []
                for row in data:
                    cleaned_row = {}
                    for key, value in row.items():
                        # Remove BOM (U+FEFF) and other invisible characters from column names
                        cleaned_key = key.strip().replace('\ufeff', '')
                        cleaned_row[cleaned_key] = value
                    cleaned_data.append(cleaned_row)
                return cleaned_data
            return data

    except UnicodeDecodeError:
        # Fallback to regular UTF-8 if UTF-8-BOM fails
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]

                # Clean column names by removing BOM and other invisible characters
                if data:
                    cleaned_data = []
                    for row in data:
                        cleaned_row = {}
                        for key, value in row.items():
                            # Remove BOM (U+FEFF) and other invisible characters from column names
                            cleaned_key = key.strip().replace('\ufeff', '')
                            cleaned_row[cleaned_key] = value
                        cleaned_data.append(cleaned_row)
                    return cleaned_data
                return data

        except Exception as e:
            print(f"Error reading CSV file with UTF-8 encoding: {e}")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)


def generate_sql_inserts(data: List[Dict[str, Any]], table_name: str) -> str:
    """
    Generate SQL INSERT statements from CSV data.

    Args:
        data (List[Dict[str, Any]]): List of dictionaries representing CSV rows
        table_name (str): Name of the target database table

    Returns:
        str: SQL INSERT statements as a string
    """
    if not data:
        return "-- No data to insert"

    # Get column names from the first row
    columns = list(data[0].keys())

    # Start building SQL
    sql_lines = []
    sql_lines.append(f"-- Generated SQL INSERT statements for table: {table_name}")
    sql_lines.append(f"-- Total rows: {len(data)}")
    sql_lines.append("-- Note: Empty values are inserted as NULL (without quotes)")
    sql_lines.append("")

        # Generate CREATE TABLE statement for temporary tables
    if table_name.startswith('#') and not table_name.startswith('##'):
        sql_lines.append("-- CREATE TABLE statement for temporary table")
        sql_lines.append(f"CREATE TABLE {table_name} (")

        # Add column definitions - allow NULL values
        column_defs = []
        for col in columns:
            column_defs.append(f"    {col} NVARCHAR(MAX) NULL")

        sql_lines.append(',\n'.join(column_defs))
        sql_lines.append(");")
        sql_lines.append("")
        sql_lines.append("-- INSERT statements:")
        sql_lines.append("")

    # Generate INSERT statements
    for i, row in enumerate(data, 1):
        # Handle values - NULL for empty/None/"NULL" text, quoted strings for actual values
        values = []
        for col in columns:
            value = row[col]
            if (value is None or
                value == '' or
                str(value).strip() == '' or
                str(value).strip().upper() == 'NULL'):
                values.append('NULL')
            else:
                # Escape single quotes and wrap in quotes for actual values
                escaped_value = str(value).replace("'", "''")
                values.append(f"'{escaped_value}'")

        # Create INSERT statement
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        insert_stmt = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"

        sql_lines.append(insert_stmt)

        # Add comment for every 100 rows for readability
        if i % 100 == 0:
            sql_lines.append(f"-- Processed {i} rows")

    return '\n'.join(sql_lines)


def write_sql_file(sql_content: str, output_file: str) -> None:
    """
    Write SQL content to output file.

    Args:
        sql_content (str): SQL content to write
        output_file (str): Path to the output SQL file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        print(f"SQL file generated successfully: {output_file}")
    except Exception as e:
        print(f"Error writing SQL file: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments and execute conversion."""
    parser = argparse.ArgumentParser(
        description='Convert CSV file to SQL INSERT statements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sql_generator.py                           # Shows available CSV files
  python sql_generator.py csv_input/data.csv       # Process specific CSV file
  python sql_generator.py data.csv                 # Process file (auto-prefix csv_input/)
  python sql_generator.py -t users data.csv       # Specify table name
  python sql_generator.py -t #temp_users data.csv # Use temporary table
  python sql_generator.py -o output.sql data.csv  # Specify output file
  python sql_generator.py --create-config         # Create sample config file
  python sql_generator.py --interactive           # Run in interactive mode
  python sql_generator.py --preset quick          # Use quick preset

Notes:
  - CSV files are automatically looked for in csv_input/ folder (JSON files are excluded)
  - SQL files are automatically saved to sql_output/ folder
  - Temporary tables (#) automatically generate CREATE TABLE statements
  - Global temporary tables (##) are not supported
  - Configuration file (config.json) can be used for persistent settings
  - Run without arguments to see available CSV files
        """
    )

    parser.add_argument('csv_file', nargs='?', help='Input CSV file path (default: csv_input/)')
    parser.add_argument('-o', '--output', help='Output SQL file path (default: sql_output/input_name.sql)')
    parser.add_argument('-t', '--table', default='table_name',
                       help='Target table name (default: table_name). Use #temp_name for temporary tables.')
    parser.add_argument('-c', '--config', help='Configuration file path (default: config.json)')
    parser.add_argument('--create-config', action='store_true', help='Create sample configuration file')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--preset', help='Use named preset (quick, detailed, minimal)')

    args = parser.parse_args()

    # Handle configuration file creation
    if args.create_config:
        create_sample_config()
        sys.exit(0)

    # Load configuration
    config = load_config(args.config)

    # Handle presets
    if args.preset:
        config = apply_preset(config, args.preset)

    # Handle interactive mode
    if args.interactive:
        config = interactive_config(config)

    # Override config with command line arguments
    if args.table != 'table_name':
        config['default_table_name'] = args.table
    if args.output:
        config['output_directory'] = os.path.dirname(args.output) if os.path.dirname(args.output) else config['output_directory']

    # Handle default CSV file path
    if not args.csv_file:
        # Look for CSV files in csv_input folder
        csv_input_dir = config['input_directory']
        if os.path.exists(csv_input_dir):
            # Filter out JSON files and only show CSV files
            csv_files = [f for f in os.listdir(csv_input_dir) if f.endswith('.csv') and not f.endswith('.json')]
            if csv_files:
                print("📁 Available CSV files in csv_input/ folder:")
                for i, file in enumerate(csv_files, 1):
                    print(f"   {i}. {file}")
                print()
                print("Usage examples:")
                print(f"   python sql_generator.py csv_input/{csv_files[0]}")
                print(f"   python sql_generator.py csv_input/your_file.csv")
                print()
                print("💡 Tip: Use 'python sql_generator.py --create-config' to generate configuration files")
                sys.exit(0)
            else:
                print("No CSV files found in csv_input/ folder.")
                print("Please place CSV files in the csv_input/ folder or specify a file path.")
                print()
                print("💡 Getting started:")
                print("   1. python sql_generator.py --create-config")
                print("   2. Copy config_sample.json to config.json and edit as needed")
                print("   3. Place your CSV files in csv_input/ folder")
                print("   4. Run: python sql_generator.py your_file.csv")
                sys.exit(1)
        else:
            print("csv_input/ folder not found.")
            print("Please create the folder or specify a CSV file path.")
            sys.exit(1)

    # Auto-prepend input directory if path doesn't exist and doesn't already have input dir prefix
    input_dir = config['input_directory']
    if not os.path.exists(args.csv_file) and not args.csv_file.startswith(f"{input_dir}/") and not args.csv_file.startswith('./'):
        csv_input_path = f"{input_dir}/{args.csv_file}"
        if os.path.exists(csv_input_path):
            args.csv_file = csv_input_path
            print(f"📁 Auto-detected CSV file: {args.csv_file}")

    # Validate table name
    table_name = config['default_table_name']
    if table_name.startswith('##'):
        print("❌ Error: Global temporary tables (##) are not supported.")
        print("   Use local temporary tables (#) instead.")
        print("   Example: #temp_users (not ##global_temp_users)")
        sys.exit(1)

    # Check if input file exists
    if not os.path.exists(args.csv_file):
        print(f"Error: Input file '{args.csv_file}' does not exist.")
        print(f"Tried: {args.csv_file}")
        if not args.csv_file.startswith('csv_input/'):
            print(f"Also tried: csv_input/{args.csv_file}")
        sys.exit(1)

    # Generate output filename if not specified
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.csv_file))[0]
        args.output = f"{config['output_directory']}/{base_name}.sql"

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Converting CSV file: {args.csv_file}")
    print(f"Target table: {table_name}")
    print(f"Output file: {args.output}")
    print("-" * 50)

    # Show folder structure info
    print("📁 Folder Structure:")
    print(f"   {config['input_directory']}/     - Place your CSV files here (JSON files excluded)")
    print(f"   {config['output_directory']}/    - Generated SQL files go here")
    print("-" * 50)

    # Read CSV data
    print("Reading CSV file...")
    data = read_csv(args.csv_file)
    print(f"Found {len(data)} rows with {len(data[0]) if data else 0} columns")

    # Show column information
    if data:
        print("Columns detected:")
        for i, col in enumerate(data[0].keys(), 1):
            print(f"  {i}. '{col}'")
        print()

    # Generate SQL
    print("Generating SQL INSERT statements...")
    sql_content = generate_sql_inserts(data, table_name)

    # Write output file
    print("Writing SQL file...")
    write_sql_file(sql_content, args.output)

    print("Conversion completed successfully!")


if __name__ == "__main__":
    main()
