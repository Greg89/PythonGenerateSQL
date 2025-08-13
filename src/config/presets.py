"""
Preset configuration management for SQL Generator.
Handles predefined configurations for common use cases.
"""

from typing import Dict, Any


class PresetManager:
    """
    Manages preset configurations for different workflows.

    Single Responsibility: Preset management only
    Open/Closed: Easy to add new presets
    """

    PRESETS = {
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

    @classmethod
    def get_preset(cls, preset_name: str) -> Dict[str, Any]:
        """
        Get preset configuration by name.

        Args:
            preset_name: Name of the preset

        Returns:
            Preset configuration dictionary

        Raises:
            ValueError: If preset name is invalid
        """
        if preset_name not in cls.PRESETS:
            available = ', '.join(cls.PRESETS.keys())
            raise ValueError(f"Unknown preset '{preset_name}'. Available: {available}")

        return cls.PRESETS[preset_name].copy()

    @classmethod
    def list_presets(cls) -> Dict[str, str]:
        """
        List all available presets with descriptions.

        Returns:
            Dictionary mapping preset names to descriptions
        """
        return {
            "quick": "Fast processing, less verbose, larger batches",
            "detailed": "Verbose output, smaller batches, includes CREATE TABLE",
            "minimal": "Minimal output, largest batches, no CREATE TABLE"
        }

    @classmethod
    def apply_preset(cls, config: Dict[str, Any], preset_name: str) -> Dict[str, Any]:
        """
        Apply preset to existing configuration.

        Args:
            config: Base configuration
            preset_name: Name of preset to apply

        Returns:
            Updated configuration
        """
        preset = cls.get_preset(preset_name)
        config.update(preset)
        print(f"🎯 Applied '{preset_name}' preset")
        return config

    @classmethod
    def add_preset(cls, name: str, preset_config: Dict[str, Any]) -> None:
        """
        Add a new preset configuration.

        Args:
            name: Name of the new preset
            preset_config: Preset configuration
        """
        cls.PRESETS[name] = preset_config.copy()
        print(f"✅ Added new preset: {name}")

    @classmethod
    def remove_preset(cls, name: str) -> None:
        """
        Remove a preset configuration.

        Args:
            name: Name of the preset to remove

        Raises:
            ValueError: If preset name is invalid
        """
        if name not in cls.PRESETS:
            raise ValueError(f"Preset '{name}' does not exist")

        if name in ["quick", "detailed", "minimal"]:
            raise ValueError(f"Cannot remove built-in preset '{name}'")

        del cls.PRESETS[name]
        print(f"✅ Removed preset: {name}")
