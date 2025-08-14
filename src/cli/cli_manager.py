"""
Command line interface management for SQL Generator.
Handles argument parsing and user interaction.
"""

import argparse
import sys
from typing import Dict, Any, Optional
from ..config import ConfigManager, PresetManager


class CLIManager:
    """
    Manages command line interface and user interaction.

    Single Responsibility: CLI operations only
    Open/Closed: Easy to extend with new CLI options
    """

    def __init__(self):
        """Initialize CLI manager."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create argument parser with all options.

        Returns:
            Configured argument parser
        """
        parser = argparse.ArgumentParser(
            description='Convert data files (CSV, TXT, XML, JSON) to SQL INSERT statements',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_help_epilog()
        )

        # Add arguments
        parser.add_argument('csv_file', nargs='?',
                          help='Input data file path (CSV, TXT, XML, JSON) (default: input/)')
        parser.add_argument('-o', '--output',
                          help='Output SQL file path (default: output/input_name.sql)')
        parser.add_argument('-t', '--table', default='table_name',
                          help='Target table name (default: table_name). Use #temp_name for temporary tables.')
        parser.add_argument('-c', '--config',
                          help='Configuration file path (default: config.json)')
        parser.add_argument('--create-config', action='store_true',
                          help='Create sample configuration file')
        parser.add_argument('--interactive', action='store_true',
                          help='Run in interactive mode')
        parser.add_argument('--preset',
                          help='Use named preset (quick, detailed, minimal)')

        return parser

    def _get_help_epilog(self) -> str:
        """
        Get help text epilog.

        Returns:
            Help text
        """
        return """
Examples:
  python main.py                                   # Shows available data files
  python main.py input/data.csv                   # Process specific CSV file
  python main.py data.csv                         # Process file (auto-prefix input/)
  python main.py input/users.xml                  # Process XML file
  python main.py config.json                      # Process JSON file
  python main.py -t users data.txt               # Specify table name
  python main.py -t #temp_users data.csv         # Use temporary table
  python main.py -o output.sql data.csv          # Specify output file
  python main.py --create-config                 # Create sample config file
  python main.py --interactive                   # Run in interactive mode
  python main.py --preset quick                  # Use quick preset

Notes:
  - Data files (CSV, TXT, XML, JSON) are automatically looked for in input/ folder
  - SQL files are automatically saved to output/ folder
  - Temporary tables (#) automatically generate CREATE TABLE statements
  - Global temporary tables (##) are not supported
  - Configuration file (config.json) can be used for persistent settings
  - Run without arguments to see available data files
        """

    def parse_arguments(self) -> argparse.Namespace:
        """
        Parse command line arguments.

        Returns:
            Parsed arguments
        """
        return self.parser.parse_args()

    def handle_create_config(self, config_manager: ConfigManager) -> None:
        """
        Handle --create-config argument.

        Args:
            config_manager: Configuration manager instance
        """
        config_manager.create_sample_config()
        sys.exit(0)

    def handle_preset(self, preset_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle --preset argument.

        Args:
            preset_name: Name of the preset
            config: Current configuration

        Returns:
            Updated configuration
        """
        try:
            return PresetManager.apply_preset(config, preset_name)
        except ValueError as e:
            print(f"⚠️  {e}")
            return config

    def interactive_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle interactive configuration mode.

        Args:
            config: Base configuration

        Returns:
            Updated configuration
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

    def show_available_files(self, data_files: list) -> None:
        """
        Show available data files.

        Args:
            data_files: List of data file names
        """
        if data_files:
            print("📁 Available data files in input/ folder:")
            for i, file in enumerate(data_files, 1):
                print(f"   {i}. {file}")
            print()
            print("Usage examples:")
            print(f"   python main.py input/{data_files[0]}")
            print(f"   python main.py input/your_file.csv")
            print()
            print("💡 Tip: Use 'python main.py --create-config' to generate configuration files")
        else:
            print("No data files found in input/ folder.")
            print("Please place data files (CSV, TXT, XML, JSON) in the input/ folder or specify a file path.")
            print()
            print("💡 Getting started:")
            print("   1. python main.py --create-config")
            print("   2. Copy config_sample.json to config.json and edit as needed")
            print("   3. Place your data files in input/ folder")
            print("   4. Run: python main.py your_file.csv")

    def show_folder_structure(self, input_dir: str, output_dir: str) -> None:
        """
        Show folder structure information.

        Args:
            input_dir: Input directory path
            output_dir: Output directory path
        """
        print("📁 Folder Structure:")
        print(f"   {input_dir}/     - Place your data files here (CSV, TXT, XML, JSON)")
        print(f"   {output_dir}/    - Generated SQL files go here")
        print("-" * 50)

    def show_processing_info(self, data_file: str, table_name: str, output_file: str) -> None:
        """
        Show processing information.

        Args:
            data_file: Input data file path
            table_name: Target table name
            output_file: Output SQL file path
        """
        print(f"Converting data file: {data_file}")
        print(f"Target table: {table_name}")
        print(f"Output file: {output_file}")
        print("-" * 50)

    def show_column_info(self, columns: list) -> None:
        """
        Show column information.

        Args:
            columns: List of column names
        """
        if columns:
            print("Columns detected:")
            for i, col in enumerate(columns, 1):
                print(f"  {i}. '{col}'")
            print()

    def show_help(self) -> None:
        """Show help information."""
        self.parser.print_help()
