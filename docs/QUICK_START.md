# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Create Configuration File
```bash
python sql_generator.py --create-config
```
This creates `config_sample.json` - copy it to `config.json` and edit as needed.

### 2. Edit Your Config (Optional)
```json
{
  "default_table_name": "my_table",
  "sql_dialect": "mysql",
  "verbose": false
}
```

### 3. Run with Simple Commands
```bash
# Basic usage (uses config.json)
python sql_generator.py data.csv

# Quick preset for fast processing
python sql_generator.py --preset quick data.csv

# Interactive mode for one-time setup
python sql_generator.py --interactive data.csv
```

## 🎯 Presets (Choose Your Workflow)

- **`--preset quick`** - Fast processing, less output
- **`--preset detailed`** - Verbose output, includes CREATE TABLE
- **`--preset minimal`** - Minimal output, largest batches

## 📁 File Structure
```
your_project/
├── config.json          # Your settings (create this, not tracked in Git)
├── csv_input/           # Put CSV files here
├── sql_output/          # SQL files generated here
└── sql_generator.py     # The script
```

## 🔧 Common Config Options
```json
{
  "default_table_name": "users",
  "sql_dialect": "sqlserver",
  "batch_size": 1000,
  "verbose": false
}
```

That's it! No more long command lines. 🎉

## 💡 Note
- `config.json` is excluded from Git - each user generates their own
- `config_sample.json` is tracked in Git as a template for the team
- Your personal settings stay local and won't interfere with others
