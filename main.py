#!/usr/bin/env python3
"""
CSV to SQL Converter - Main Entry Point
Converts CSV files to SQL INSERT statements for database table insertion.

"""

from src.app import SQLGeneratorApp


def main():
    """Main entry point for the SQL Generator application."""
    app = SQLGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()
