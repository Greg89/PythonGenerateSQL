# SQL Generator - Clean Architecture Guide

## 🏗️ **Architecture Overview**

The SQL Generator has been completely refactored following **SOLID principles** and **clean code practices**. This new structure makes it easy to add features, maintain code, and understand the system.

## 📁 **New Project Structure**

```
PythonGenerateSQL/
├── src/                          # Source code package
│   ├── __init__.py              # Package initialization
│   ├── app.py                   # Main application orchestrator
│   ├── config/                  # Configuration management
│   │   ├── __init__.py
│   │   ├── config_manager.py    # Configuration loading/saving
│   │   └── presets.py          # Preset configurations
│   ├── data/                    # Data handling
│   │   ├── __init__.py
│   │   └── csv_reader.py        # CSV file operations
│   ├── sql/                     # SQL generation
│   │   ├── __init__.py
│   │   └── sql_generator.py     # SQL generation logic
│   ├── utils/                   # Utilities
│   │   ├── __init__.py
│   │   └── file_manager.py      # File operations
│   └── cli/                     # Command line interface
│       ├── __init__.py
│       └── cli_manager.py       # CLI management
├── main.py                      # New main entry point
├── sql_generator.py             # Old monolithic script (kept for reference)
├── config_sample.json           # Sample configuration
└── .gitignore                   # Git exclusions
```

## 🎯 **SOLID Principles Implementation**

### **1. Single Responsibility Principle (SRP)**
Each class has **one reason to change**:

- **`ConfigManager`** - Only handles configuration
- **`CSVReader`** - Only handles CSV file operations
- **`SQLGenerator`** - Only generates SQL
- **`FileManager`** - Only handles file operations
- **`CLIManager`** - Only handles command line interface
- **`SQLGeneratorApp`** - Only orchestrates the workflow

### **2. Open/Closed Principle (OCP)**
Classes are **open for extension, closed for modification**:

```python
# Easy to add new SQL dialects without changing existing code
class OracleDialect(SQLDialect):
    def format_value(self, value, null_values):
        # Oracle-specific implementation
        pass

# Add to generator
sql_generator.add_dialect("oracle", OracleDialect)
```

### **3. Liskov Substitution Principle (LSP)**
Subtypes are **interchangeable** with their base types:

```python
# Any SQLDialect implementation can be used
dialects = [SQLServerDialect(), MySQLDialect(), PostgreSQLDialect()]
for dialect in dialects:
    sql_generator.dialect = dialect  # All work the same way
```

### **4. Interface Segregation Principle (ISP)**
Clients don't depend on **interfaces they don't use**:

```python
# CSVReader only exposes methods needed for CSV operations
csv_reader.read_file(file_path)      # ✅ Needed
csv_reader.get_column_info(data)     # ✅ Needed
csv_reader.format_sql()              # ❌ Not needed - not exposed
```

### **5. Dependency Inversion Principle (DIP)**
High-level modules don't depend on **low-level modules**:

```python
# SQLGenerator depends on SQLDialect abstraction, not concrete implementations
class SQLGenerator:
    def __init__(self, dialect: SQLDialect):  # ✅ Depends on abstraction
        self.dialect = dialect

# Not: self.dialect = SQLServerDialect()  # ❌ Depends on concrete class
```

## 🔧 **Key Design Patterns**

### **1. Strategy Pattern (SQL Dialects)**
```python
# Different SQL dialects as interchangeable strategies
dialects = {
    "sqlserver": SQLServerDialect,
    "mysql": MySQLDialect,
    "postgresql": PostgreSQLDialect
}
```

### **2. Factory Pattern (Component Creation)**
```python
# Application creates components based on configuration
def _initialize_components(self, args):
    self.csv_reader = CSVReader(
        auto_detect_encoding=self.config_manager.get('auto_detect_encoding')
    )
```

### **3. Template Method Pattern (Workflow)**
```python
# Main workflow is defined in the base class
def run(self):
    self._initialize_components(args)      # ✅ Hook for subclasses
    self._process_csv_file(args)          # ✅ Hook for subclasses
```

## 🚀 **Adding New Features**

### **Adding a New SQL Dialect**
1. **Create dialect class**:
```python
class OracleDialect(SQLDialect):
    def format_value(self, value, null_values):
        # Oracle-specific logic
        pass

    def create_table_statement(self, table_name, columns):
        # Oracle-specific CREATE TABLE
        pass
```

2. **Register with generator**:
```python
sql_generator.add_dialect("oracle", OracleDialect)
```

### **Adding a New Configuration Option**
1. **Add to DEFAULT_CONFIG** in `ConfigManager`
2. **Update config_sample.json**
3. **Add to interactive mode** in `CLIManager` (if needed)
4. **Add to presets** in `PresetManager` (if needed)

### **Adding a New File Format**
1. **Create new reader class** (e.g., `ExcelReader`)
2. **Implement common interface**
3. **Update `FileManager`** to handle new extensions
4. **Update CLI** to support new format

## 📊 **Benefits of New Architecture**

### **Maintainability**
- **Single responsibility** - Easy to find and fix issues
- **Clear separation** - Changes don't affect unrelated code
- **Consistent patterns** - Predictable code structure

### **Extensibility**
- **Add new SQL dialects** without touching existing code
- **Add new file formats** by implementing interfaces
- **Add new presets** by extending preset manager

### **Testability**
- **Unit testing** - Each class can be tested in isolation
- **Mocking** - Easy to mock dependencies
- **Integration testing** - Clear component boundaries

### **Team Collaboration**
- **Multiple developers** can work on different components
- **Clear interfaces** - Easy to understand what each class does
- **Version control** - Changes are isolated and trackable

## 🔄 **Migration from Old Script**

### **Old Way (Monolithic)**
```python
# Everything in one file - hard to maintain
def main():
    # 200+ lines of mixed responsibilities
    # Hard to test individual parts
    # Difficult to add new features
    pass
```

### **New Way (Clean Architecture)**
```python
# Clear separation of concerns
class SQLGeneratorApp:
    def run(self):
        # Orchestrates components - doesn't do the work
        self._initialize_components(args)
        self._process_csv_file(args)

# Each component handles its own responsibility
csv_reader.read_file(file_path)      # CSV operations
sql_generator.generate_inserts(data) # SQL generation
file_manager.write_file(content)     # File operations
```

## 🎯 **Usage Examples**

### **Basic Usage**
```bash
# Same interface, cleaner implementation
python main.py data.csv
python main.py --preset quick data.csv
python main.py --interactive data.csv
```

### **Programmatic Usage**
```python
from src.app import SQLGeneratorApp

app = SQLGeneratorApp()
app.run()  # Same as command line

# Access components for custom workflows
csv_reader = app.get_csv_reader()
sql_generator = app.get_sql_generator()
```

## 🔮 **Future Enhancements**

With this architecture, you can easily add:

- **New SQL dialects** (Oracle, SQLite, etc.)
- **New input formats** (Excel, JSON, XML)
- **New output formats** (JSON, YAML, etc.)
- **Database connections** (direct DB insertion)
- **Batch processing** (multiple files)
- **Data validation** (schema checking)
- **Performance optimization** (streaming, parallel processing)

## 💡 **Best Practices**

1. **Keep classes focused** - One responsibility per class
2. **Use interfaces** - Depend on abstractions, not concretions
3. **Follow naming conventions** - Clear, descriptive names
4. **Add documentation** - Docstrings for all public methods
5. **Write tests** - Each component should be testable
6. **Version control** - Small, focused commits

This new architecture transforms your script from a **monolithic file** into a **professional, maintainable application** that follows industry best practices! 🎉
