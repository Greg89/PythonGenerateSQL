"""
File management utilities for SQL Generator.
Handles file operations, validation, and directory management.
"""

import os
from typing import List, Optional
from pathlib import Path


class FileManager:
    """
    Manages file operations and validation.

    Single Responsibility: File operations only
    Open/Closed: Easy to extend with new file operations
    """

    def __init__(self, input_directory: str = "input", output_directory: str = "output"):
        """
        Initialize file manager.

        Args:
            input_directory: Directory containing input files
            output_directory: Directory for output files
        """
        self.input_directory = input_directory
        self.output_directory = output_directory

    def list_data_files(self, exclude_json: bool = False) -> List[str]:
        """
        List supported data files in the input directory.

        Args:
            exclude_json: Whether to exclude JSON files (default: False, now supported)

        Returns:
            List of supported data file names
        """
        if not os.path.exists(self.input_directory):
            return []

        supported_extensions = ['.csv', '.txt', '.xml', '.json']
        files = []
        for file in os.listdir(self.input_directory):
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                files.append(file)

        return sorted(files)

    def resolve_file_path(self, file_path: str) -> str:
        """
        Resolve file path, auto-prepending input directory if needed.

        Args:
            file_path: File path to resolve

        Returns:
            Resolved file path
        """
        # If path exists as-is, return it
        if os.path.exists(file_path):
            return file_path

        # If path already has input directory prefix, return as-is
        if file_path.startswith(f"{self.input_directory}/") or file_path.startswith('./'):
            return file_path

        # Try auto-prepending input directory
        auto_path = f"{self.input_directory}/{file_path}"
        if os.path.exists(auto_path):
            print(f"📁 Auto-detected data file: {auto_path}")
            return auto_path

        return file_path

    def validate_file_exists(self, file_path: str) -> bool:
        """
        Validate that a file exists.

        Args:
            file_path: Path to validate

        Returns:
            True if file exists
        """
        return os.path.exists(file_path)

    def generate_output_path(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        Generate output file path.

        Args:
            input_file: Input file path
            output_file: Optional explicit output file path

        Returns:
            Output file path
        """
        if output_file:
            return output_file

        # Generate from input file name
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        return f"{self.output_directory}/{base_name}.sql"

    def ensure_output_directory(self, output_file: str) -> None:
        """
        Ensure output directory exists.

        Args:
            output_file: Output file path
        """
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def write_file(self, content: str, file_path: str) -> None:
        """
        Write content to file.

        Args:
            content: Content to write
            file_path: Path to write to

        Raises:
            Exception: If writing fails
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 File written successfully: {file_path}")
        except Exception as e:
            raise Exception(f"Error writing file {file_path}: {e}")

    def validate_table_name(self, table_name: str) -> bool:
        """
        Validate table name.

        Args:
            table_name: Table name to validate

        Returns:
            True if table name is valid
        """
        # Check for global temporary tables (not supported)
        if table_name.startswith('##'):
            return False

        return True

    def get_file_info(self, file_path: str) -> dict:
        """
        Get information about a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file information
        """
        path = Path(file_path)
        return {
            "name": path.name,
            "stem": path.stem,
            "suffix": path.suffix,
            "size": path.stat().st_size if path.exists() else 0,
            "exists": path.exists()
        }

    def create_directory(self, directory: str) -> None:
        """
        Create directory if it doesn't exist.

        Args:
            directory: Directory path to create
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

    def is_supported_data_file(self, file_path: str) -> bool:
        """
        Check if file is a supported data file.

        Args:
            file_path: Path to check

        Returns:
            True if file is supported
        """
        supported_extensions = ['.csv', '.txt', '.xml', '.json']
        return any(file_path.lower().endswith(ext) for ext in supported_extensions)

    def get_relative_path(self, file_path: str, base_directory: str) -> str:
        """
        Get relative path from base directory.

        Args:
            file_path: Full file path
            base_directory: Base directory

        Returns:
            Relative path
        """
        try:
            return os.path.relpath(file_path, base_directory)
        except ValueError:
            return file_path
