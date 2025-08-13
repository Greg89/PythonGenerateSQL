"""
Main application class for SQL Generator.
Orchestrates all components and manages the conversion workflow.
"""

import sys
from typing import Dict, Any, Optional
from .config import ConfigManager, PresetManager
from .data import CSVReader
from .sql import SQLGenerator
from .utils import FileManager
from .cli import CLIManager


class SQLGeneratorApp:
    """
    Main application class that orchestrates CSV to SQL conversion.

    Single Responsibility: Application orchestration
    Dependency Inversion: Depends on abstractions, not concrete implementations
    """

    def __init__(self):
        """Initialize the application."""
        self.cli_manager = CLIManager()
        self.config_manager = None
        self.file_manager = None
        self.csv_reader = None
        self.sql_generator = None

    def run(self) -> None:
        """
        Main application entry point.

        Raises:
            SystemExit: For normal program termination
        """
        try:
            # Parse command line arguments
            args = self.cli_manager.parse_arguments()

            # Handle configuration file creation
            if args.create_config:
                self.config_manager = ConfigManager()
                self.cli_manager.handle_create_config(self.config_manager)

            # Initialize components
            self._initialize_components(args)

            # Handle presets
            if args.preset:
                self.config_manager.config = self.cli_manager.handle_preset(
                    args.preset, self.config_manager.config
                )

            # Handle interactive mode
            if args.interactive:
                self.config_manager.config = self.cli_manager.interactive_config(
                    self.config_manager.config
                )

            # Override config with command line arguments
            self._override_config_with_args(args)

            # Handle no CSV file case
            if not args.csv_file:
                self._handle_no_csv_file()

            # Process CSV file
            self._process_csv_file(args)

        except KeyboardInterrupt:
            print("\n⚠️  Operation cancelled by user")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

    def _initialize_components(self, args) -> None:
        """
        Initialize application components.

        Args:
            args: Command line arguments
        """
        # Initialize configuration manager
        self.config_manager = ConfigManager(args.config)

        # Initialize file manager
        self.file_manager = FileManager(
            input_directory=self.config_manager.get('input_directory'),
            output_directory=self.config_manager.get('output_directory')
        )

        # Initialize CSV reader
        self.csv_reader = CSVReader(
            auto_detect_encoding=self.config_manager.get('auto_detect_encoding')
        )

        # Initialize SQL generator
        self.sql_generator = SQLGenerator(
            dialect=self.config_manager.get('sql_dialect'),
            batch_size=self.config_manager.get('batch_size')
        )

    def _override_config_with_args(self, args) -> None:
        """
        Override configuration with command line arguments.

        Args:
            args: Command line arguments
        """
        if args.table != 'table_name':
            self.config_manager.set('default_table_name', args.table)

        if args.output:
            output_dir = self.file_manager.get_relative_path(args.output, '.')
            if output_dir != args.output:
                self.config_manager.set('output_directory', output_dir)

    def _handle_no_csv_file(self) -> None:
        """
        Handle case when no CSV file is specified.

        Raises:
            SystemExit: To show available files and exit
        """
        csv_files = self.file_manager.list_csv_files()
        self.cli_manager.show_available_files(csv_files)

        if csv_files:
            sys.exit(0)
        else:
            sys.exit(1)

    def _process_csv_file(self, args) -> None:
        """
        Process the specified CSV file.

        Args:
            args: Command line arguments
        """
        # Resolve and validate file path
        csv_file = self.file_manager.resolve_file_path(args.csv_file)

        if not self.file_manager.validate_file_exists(csv_file):
            print(f"Error: Input file '{csv_file}' does not exist.")
            if not csv_file.startswith(self.file_manager.input_directory):
                print(f"Also tried: {self.file_manager.input_directory}/{args.csv_file}")
            sys.exit(1)

        # Validate table name
        table_name = self.config_manager.get('default_table_name')
        if not self.file_manager.validate_table_name(table_name):
            print("❌ Error: Global temporary tables (##) are not supported.")
            print("   Use local temporary tables (#) instead.")
            print("   Example: #temp_users (not ##global_temp_users)")
            sys.exit(1)

        # Generate output file path
        output_file = self.file_manager.generate_output_path(csv_file, args.output)
        self.file_manager.ensure_output_directory(output_file)

        # Show processing information
        self.cli_manager.show_processing_info(csv_file, table_name, output_file)
        self.cli_manager.show_folder_structure(
            self.file_manager.input_directory,
            self.file_manager.output_directory
        )

        # Read CSV data
        print("Reading CSV file...")
        data = self.csv_reader.read_file(csv_file)

        if not data:
            print("❌ Error: No data found in CSV file")
            sys.exit(1)

        # Validate data structure
        if not self.csv_reader.validate_data(data):
            print("❌ Error: Invalid CSV data structure")
            sys.exit(1)

        print(f"Found {self.csv_reader.get_row_count(data)} rows with {len(data[0])} columns")

        # Show column information
        column_info = self.csv_reader.get_column_info(data)
        self.cli_manager.show_column_info(column_info['names'])

        # Generate SQL
        print("Generating SQL INSERT statements...")
        sql_content = self.sql_generator.generate_inserts(
            data=data,
            table_name=table_name,
            null_values=self.config_manager.get('null_values')
        )

        # Write output file
        print("Writing SQL file...")
        self.file_manager.write_file(sql_content, output_file)

        print("Conversion completed successfully!")

    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration.

        Returns:
            Configuration dictionary
        """
        return self.config_manager.config if self.config_manager else {}

    def get_file_manager(self) -> Optional[FileManager]:
        """
        Get file manager instance.

        Returns:
            File manager instance or None
        """
        return self.file_manager

    def get_csv_reader(self) -> Optional[CSVReader]:
        """
        Get CSV reader instance.

        Returns:
            CSV reader instance or None
        """
        return self.csv_reader

    def get_sql_generator(self) -> Optional[SQLGenerator]:
        """
        Get SQL generator instance.

        Returns:
            SQL generator instance or None
        """
        return self.sql_generator
