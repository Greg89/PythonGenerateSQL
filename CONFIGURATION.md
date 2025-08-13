# Configuration Guide for SQL Generator

## Overview

The SQL Generator now supports multiple ways to configure parameters, making it much easier to use while maintaining flexibility for future features.

## Configuration Methods (in order of priority)

### 1. Configuration File (Recommended)
Create a `config.json` file in your project directory (this file is not tracked in Git):

```json
{
  "input_directory": "csv_input",
  "output_directory": "sql_output",
  "default_table_name": "users",
  "auto_detect_encoding": true,
  "batch_size": 100,
  "include_create_table": true,
  "sql_dialect": "sqlserver",
  "date_format": "YYYY-MM-DD",
  "null_values": ["", "NULL", "null", "None", "none"],
  "max_rows_per_file": 10000,
  "verbose": true
}
```

**Benefits:**
- Persistent settings across runs
- Easy to modify and version control
- No need to remember long command lines
- Easy to share configurations with team members

### 2. Presets
Use predefined configurations for common use cases:

```bash
python sql_generator.py --preset quick data.csv      # Fast processing
python sql_generator.py --preset detailed data.csv   # Verbose output
python sql_generator.py --preset minimal data.csv    # Minimal output
```

**Available Presets:**
- **quick**: Fast processing, less verbose, larger batches
- **detailed**: Verbose output, smaller batches, includes CREATE TABLE
- **minimal**: Minimal output, largest batches, no CREATE TABLE

### 3. Interactive Mode
Configure settings interactively:

```bash
python sql_generator.py --interactive data.csv
```

The script will prompt you for:
- Table name
- SQL dialect
- Batch size
- Verbose mode

### 4. Command Line Arguments
Override specific settings:

```bash
python sql_generator.py -t users -o output.sql data.csv
```

### 5. Environment Variables
Set environment variables for commonly used settings:

```bash
export SQL_GENERATOR_TABLE=users
export SQL_GENERATOR_OUTPUT_DIR=my_output
python sql_generator.py data.csv
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `input_directory` | string | `csv_input` | Directory containing CSV files |
| `output_directory` | string | `sql_output` | Directory for generated SQL files |
| `default_table_name` | string | `table_name` | Default table name for INSERT statements |
| `auto_detect_encoding` | boolean | `true` | Automatically detect CSV encoding |
| `batch_size` | integer | `100` | Number of rows per batch comment |
| `include_create_table` | boolean | `true` | Generate CREATE TABLE statements |
| `sql_dialect` | string | `sqlserver` | SQL dialect (sqlserver, mysql, postgresql) |
| `date_format` | string | `YYYY-MM-DD` | Date format for date columns |
| `null_values` | array | `["", "NULL", "null", "None", "none"]` | Values to treat as NULL |
| `max_rows_per_file` | integer | `10000` | Maximum rows to process per file |
| `verbose` | boolean | `true` | Enable verbose output |

## Getting Started

### 1. Create Sample Configuration
```bash
python sql_generator.py --create-config
```

This creates `config_sample.json` - copy it to `config.json` and modify as needed.

### 2. Basic Usage with Config
```bash
# With default config.json
python sql_generator.py data.csv

# With custom config file
python sql_generator.py -c my_config.json data.csv
```

### 3. Quick Preset
```bash
python sql_generator.py --preset quick data.csv
```

### 4. Interactive Setup
```bash
python sql_generator.py --interactive data.csv
```

## Adding New Features

When you want to add new features, simply:

1. **Add to DEFAULT_CONFIG** in the script
2. **Update config_sample.json**
3. **Add to interactive_config()** if it should be configurable interactively
4. **Add to presets** if it makes sense for different use cases

Example:
```python
# In DEFAULT_CONFIG
"new_feature": "default_value",
"another_option": True

# In interactive_config()
new_feature = input(f"New feature [{config['new_feature']}]: ").strip()
if new_feature:
    config['new_feature'] = new_feature
```

## Migration from Old Script

If you were using the old script with many command-line arguments:

**Old way:**
```bash
python sql_generator.py -t users -o output.sql --batch-size 1000 --verbose false data.csv
```

**New way:**
```bash
# Option 1: Use config file
python sql_generator.py data.csv

# Option 2: Use preset
python sql_generator.py --preset quick data.csv

# Option 3: Override specific settings
python sql_generator.py -t users -o output.sql data.csv
```

## Best Practices

1. **Use config.json for persistent settings** - Don't repeat the same arguments every time
2. **Use presets for different workflows** - Quick for development, detailed for production
3. **Use interactive mode for one-time changes** - Great for exploring options
4. **Keep config.json local** - Configuration files are excluded from Git (users generate their own)
5. **Keep config.json simple** - Only override what you need to change
6. **Share config_sample.json** - This template is tracked in Git for team reference

## Troubleshooting

### Config file not found
- Ensure `config.json` exists in the same directory as the script
- Check file permissions
- Use `--create-config` to generate a sample

### Preset not working
- Check preset name spelling (quick, detailed, minimal)
- Ensure preset name is lowercase

### Interactive mode issues
- Press Ctrl+C to cancel and use defaults
- Ensure your terminal supports input()

### Configuration conflicts
- Command line arguments override config file
- Config file overrides defaults
- Last specified wins
