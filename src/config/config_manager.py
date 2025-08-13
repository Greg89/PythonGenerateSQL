"""
Configuration management for SQL Generator.
Handles loading, saving, and managing configuration files.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """
    Manages configuration loading, saving, and validation.

    Single Responsibility: Configuration management only
    Open/Closed: Easy to extend with new config options
    """

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

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Optional path to configuration file
        """
        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default.

        Returns:
            Configuration dictionary
        """
        config = self.DEFAULT_CONFIG.copy()

        # Try to load from specified config file
        if self.config_file and os.path.exists(self.config_file):
            config = self._load_from_file(self.config_file, config)

        # Try to load from default config location
        elif os.path.exists("config.json"):
            config = self._load_from_file("config.json", config)

        return config

    def _load_from_file(self, file_path: str, base_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load configuration from a specific file.

        Args:
            file_path: Path to configuration file
            base_config: Base configuration to update

        Returns:
            Updated configuration dictionary
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                base_config.update(user_config)
                print(f"📋 Loaded configuration from: {file_path}")
        except Exception as e:
            print(f"⚠️  Warning: Could not load config file {file_path}: {e}")
            print("   Using default configuration")

        return base_config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value

    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.

        Args:
            updates: Dictionary of updates
        """
        self._config.update(updates)

    def save(self, config_file: Optional[str] = None) -> None:
        """
        Save configuration to file.

        Args:
            config_file: Optional path to save configuration
        """
        file_path = config_file or "config.json"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            print(f"💾 Configuration saved to: {file_path}")
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")

    def create_sample_config(self, output_file: str = "config_sample.json") -> None:
        """
        Create a sample configuration file.

        Args:
            output_file: Path to save sample configuration
        """
        sample_config = {
            **self.DEFAULT_CONFIG,
            "custom_settings": {
                "example_feature": "value",
                "another_option": True
            }
        }

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(sample_config, f, indent=2, ensure_ascii=False)
            print(f"📝 Sample configuration file created: {output_file}")
            print("   Copy this to config.json and modify as needed")
        except Exception as e:
            print(f"❌ Error creating sample configuration: {e}")

    @property
    def config(self) -> Dict[str, Any]:
        """
        Get the current configuration.

        Returns:
            Configuration dictionary
        """
        return self._config.copy()

    def validate(self) -> bool:
        """
        Validate configuration values.

        Returns:
            True if configuration is valid
        """
        # Add validation logic here as needed
        return True
