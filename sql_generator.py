#!/usr/bin/env python3
"""
CSV to SQL Converter
Converts CSV files to SQL INSERT statements for database table insertion.
"""

import csv
import argparse
import os
import sys
from typing import List, Dict, Any


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
    sql_lines.append("")

    # Generate INSERT statements
    for i, row in enumerate(data, 1):
        # Escape single quotes in values
        values = []
        for col in columns:
            value = row[col]
            if value is None or value == '':
                values.append('NULL')
            else:
                # Escape single quotes and wrap in quotes
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
  python sql_generator.py csv_input/data.csv
  python sql_generator.py csv_input/data.csv -o sql_output/output.sql
  python sql_generator.py csv_input/data.csv -t users -o sql_output/users_insert.sql

Note: By default, SQL files are saved to the sql_output/ folder.
        """
    )

    parser.add_argument('csv_file', help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output SQL file path (default: input_name.sql)')
    parser.add_argument('-t', '--table', default='table_name', help='Target table name (default: table_name)')

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.csv_file):
        print(f"Error: Input file '{args.csv_file}' does not exist.")
        sys.exit(1)

    # Generate output filename if not specified
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.csv_file))[0]
        args.output = f"sql_output/{base_name}.sql"

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Converting CSV file: {args.csv_file}")
    print(f"Target table: {args.table}")
    print(f"Output file: {args.output}")
    print("-" * 50)

    # Show folder structure info
    print("📁 Folder Structure:")
    print("   csv_input/     - Place your CSV files here")
    print("   sql_output/    - Generated SQL files go here")
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
    sql_content = generate_sql_inserts(data, args.table)

    # Write output file
    print("Writing SQL file...")
    write_sql_file(sql_content, args.output)

    print("Conversion completed successfully!")


if __name__ == "__main__":
    main()
