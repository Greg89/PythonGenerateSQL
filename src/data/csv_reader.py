"""
CSV file reading and processing for SQL Generator.
Handles CSV file operations with encoding detection and data cleaning.
"""

import csv
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path


class CSVReader:
    """
    Handles CSV file reading and data processing.

    Single Responsibility: CSV file operations only
    Open/Closed: Easy to extend with new CSV formats
    """

    def __init__(self, auto_detect_encoding: bool = True):
        """
        Initialize CSV reader.

        Args:
            auto_detect_encoding: Whether to automatically detect encoding
        """
        self.auto_detect_encoding = auto_detect_encoding

    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read CSV file and return list of dictionaries.

        Args:
            file_path: Path to the CSV file

        Returns:
            List of dictionaries where each dict represents a row

        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: For other reading errors
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File '{file_path}' not found.")

        if self.auto_detect_encoding:
            return self._read_with_encoding_detection(file_path)
        else:
            return self._read_with_encoding(file_path, 'utf-8')

    def _read_with_encoding_detection(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read CSV file with automatic encoding detection.

        Args:
            file_path: Path to the CSV file

        Returns:
            List of dictionaries representing CSV rows
        """
        # Try UTF-8-BOM first to handle BOM characters
        try:
            return self._read_with_encoding(file_path, 'utf-8-sig')
        except UnicodeDecodeError:
            # Fallback to regular UTF-8
            try:
                return self._read_with_encoding(file_path, 'utf-8')
            except Exception as e:
                print(f"Error reading CSV file with UTF-8 encoding: {e}")
                sys.exit(1)

    def _read_with_encoding(self, file_path: str, encoding: str) -> List[Dict[str, Any]]:
        """
        Read CSV file with specific encoding.

        Args:
            file_path: Path to the CSV file
            encoding: File encoding to use

        Returns:
            List of dictionaries representing CSV rows
        """
        try:
            with open(file_path, 'r', newline='', encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]

                if not data:
                    return []

                # Clean column names and data
                return self._clean_data(data)

        except Exception as e:
            raise Exception(f"Error reading CSV file with {encoding} encoding: {e}")

    def _clean_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clean CSV data by removing BOM and invisible characters.

        Args:
            data: Raw CSV data

        Returns:
            Cleaned CSV data
        """
        cleaned_data = []

        for row in data:
            cleaned_row = {}
            for key, value in row.items():
                # Remove BOM (U+FEFF) and other invisible characters from column names
                cleaned_key = key.strip().replace('\ufeff', '')
                cleaned_row[cleaned_key] = value
            cleaned_data.append(cleaned_row)

        return cleaned_data

    def get_column_info(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get information about CSV columns.

        Args:
            data: CSV data

        Returns:
            Dictionary with column information
        """
        if not data:
            return {"count": 0, "names": [], "sample_values": {}}

        columns = list(data[0].keys())
        sample_values = {col: data[0][col] for col in columns}

        return {
            "count": len(columns),
            "names": columns,
            "sample_values": sample_values
        }

    def validate_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        Validate CSV data structure.

        Args:
            data: CSV data to validate

        Returns:
            True if data is valid
        """
        if not data:
            return False

        # Check if all rows have the same columns
        first_row_keys = set(data[0].keys())
        for row in data[1:]:
            if set(row.keys()) != first_row_keys:
                return False

        return True

    def get_row_count(self, data: List[Dict[str, Any]]) -> int:
        """
        Get the number of rows in the CSV data.

        Args:
            data: CSV data

        Returns:
            Number of rows
        """
        return len(data)

    def get_sample_rows(self, data: List[Dict[str, Any]], count: int = 5) -> List[Dict[str, Any]]:
        """
        Get sample rows from CSV data.

        Args:
            data: CSV data
            count: Number of sample rows to return

        Returns:
            List of sample rows
        """
        if not data:
            return []

        return data[:min(count, len(data))]
