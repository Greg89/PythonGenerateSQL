"""
Unified data file reading and processing for SQL Generator.
Handles CSV, TXT, XML, and JSON files with nested collection handling.
"""

import csv
import json
import sys
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Union
from pathlib import Path


class DataReader:
    """
    Handles multiple file format reading and data processing.

    Single Responsibility: File reading operations only
    Open/Closed: Easy to extend with new file formats
    """

    def __init__(self, auto_detect_encoding: bool = True):
        """
        Initialize data reader.

        Args:
            auto_detect_encoding: Whether to automatically detect encoding
        """
        self.auto_detect_encoding = auto_detect_encoding

    def read_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read file and return list of dictionaries based on file type.

        Args:
            file_path: Path to the file

        Returns:
            List of dictionaries where each dict represents a row

        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: For other reading errors
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File '{file_path}' not found.")

        file_extension = Path(file_path).suffix.lower()

        if file_extension == '.csv':
            return self._read_csv(file_path)
        elif file_extension == '.txt':
            return self._read_txt(file_path)
        elif file_extension == '.xml':
            return self._read_xml(file_path)
        elif file_extension == '.json':
            return self._read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def _read_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read CSV file and return list of dictionaries.

        Args:
            file_path: Path to the CSV file

        Returns:
            List of dictionaries representing CSV rows
        """
        if self.auto_detect_encoding:
            return self._read_csv_with_encoding_detection(file_path)
        else:
            return self._read_csv_with_encoding(file_path, 'utf-8')

    def _read_csv_with_encoding_detection(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read CSV file with automatic encoding detection.

        Args:
            file_path: Path to the CSV file

        Returns:
            List of dictionaries representing CSV rows
        """
        # Try UTF-8-BOM first to handle BOM characters
        try:
            return self._read_csv_with_encoding(file_path, 'utf-8-sig')
        except UnicodeDecodeError:
            # Fallback to regular UTF-8
            try:
                return self._read_csv_with_encoding(file_path, 'utf-8')
            except Exception as e:
                print(f"Error reading CSV file with UTF-8 encoding: {e}")
                sys.exit(1)

    def _read_csv_with_encoding(self, file_path: str, encoding: str) -> List[Dict[str, Any]]:
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

    def _read_txt(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read TXT file and return list of dictionaries.
        Assumes tab-separated or space-separated values.

        Args:
            file_path: Path to the TXT file

        Returns:
            List of dictionaries representing TXT rows
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

                if not lines:
                    return []

                # Try to detect separator (tab or space)
                first_line = lines[0].strip()
                if '\t' in first_line:
                    separator = '\t'
                else:
                    separator = ' '

                # Parse header and data
                header = [col.strip() for col in first_line.split(separator) if col.strip()]
                data = []

                for line in lines[1:]:
                    line = line.strip()
                    if line:
                        values = [val.strip() for val in line.split(separator)]
                        # Pad with empty strings if line is shorter than header
                        while len(values) < len(header):
                            values.append('')
                        # Truncate if line is longer than header
                        values = values[:len(header)]

                        row = dict(zip(header, values))
                        data.append(row)

                return self._clean_data(data)

        except Exception as e:
            raise Exception(f"Error reading TXT file: {e}")

    def _read_xml(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read XML file and return list of dictionaries.
        Handles only one level of nesting - nested collections are excluded.

        Args:
            file_path: Path to the XML file

        Returns:
            List of dictionaries representing XML rows
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            data = []

            # Look for repeating elements (like <user> tags)
            for child in root:
                if len(child) > 0:  # Has children
                    row = {}
                    for subchild in child:
                        if len(subchild) == 0:  # Direct child (not nested)
                            row[subchild.tag] = subchild.text or ''
                        else:  # Nested collection - set to NULL
                            row[subchild.tag] = None
                    if row:  # Only add if we have data
                        data.append(row)
                elif len(child) == 0 and child.text and child.text.strip():  # Leaf element with text
                    # Single element case
                    row = {child.tag: child.text.strip()}
                    data.append(row)

            return self._clean_data(data)

        except Exception as e:
            raise Exception(f"Error reading XML file: {e}")

    def _read_json(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read JSON file and return list of dictionaries.
        Handles only one level of nesting - nested collections are excluded.

        Args:
            file_path: Path to the JSON file

        Returns:
            List of dictionaries representing JSON rows
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

                if isinstance(json_data, list):
                    # Array of objects
                    data = []
                    for item in json_data:
                        if isinstance(item, dict):
                            flattened_item = self._flatten_json_object(item)
                            data.append(flattened_item)
                    return self._clean_data(data)
                elif isinstance(json_data, dict):
                    # Single object or object with arrays
                    flattened_item = self._flatten_json_object(json_data)
                    return self._clean_data([flattened_item])
                else:
                    raise ValueError("JSON must contain objects or arrays of objects")

        except Exception as e:
            raise Exception(f"Error reading JSON file: {e}")

    def _flatten_json_object(self, obj: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        """
        Flatten JSON object, excluding nested collections.

        Args:
            obj: JSON object to flatten
            parent_key: Parent key for nested objects

        Returns:
            Flattened object with nested collections set to NULL
        """
        flattened = {}

        for key, value in obj.items():
            new_key = f"{parent_key}_{key}" if parent_key else key

            if isinstance(value, dict):
                # Nested object - flatten it
                nested = self._flatten_json_object(value, new_key)
                flattened.update(nested)
            elif isinstance(value, list):
                # Nested collection - set to NULL
                flattened[new_key] = None
            else:
                # Simple value
                flattened[new_key] = value

        return flattened

    def _clean_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clean data by removing BOM and invisible characters.

        Args:
            data: Raw data

        Returns:
            Cleaned data
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
        Get information about data columns.

        Args:
            data: Data

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
        Validate data structure.

        Args:
            data: Data to validate

        Returns:
            True if data is valid
        """
        if not data:
            return False

        # For XML and JSON, different rows might have different columns due to nested data
        # We'll normalize all rows to have the same columns by adding missing keys with None
        if len(data) > 1:
            all_keys = set()
            for row in data:
                all_keys.update(row.keys())

            # Normalize all rows to have the same columns
            for row in data:
                for key in all_keys:
                    if key not in row:
                        row[key] = None

        return True

    def get_row_count(self, data: List[Dict[str, Any]]) -> int:
        """
        Get the number of rows in the data.

        Args:
            data: Data

        Returns:
            Number of rows
        """
        return len(data)

    def get_sample_rows(self, data: List[Dict[str, Any]], count: int = 5) -> List[Dict[str, Any]]:
        """
        Get sample rows from data.

        Args:
            data: Data
            count: Number of sample rows to return

        Returns:
            List of sample rows
        """
        if not data:
            return []

        return data[:min(count, len(data))]

    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported file formats.

        Returns:
            List of supported file extensions
        """
        return ['.csv', '.txt', '.xml', '.json']
