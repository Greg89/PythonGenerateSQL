"""
SQL generation for SQL Generator.
Handles conversion of CSV data to SQL INSERT statements.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class SQLDialect(ABC):
    """
    Abstract base class for SQL dialects.

    Open/Closed: Easy to add new SQL dialects
    """

    @abstractmethod
    def format_value(self, value: Any, null_values: List[str]) -> str:
        """Format a value for the specific SQL dialect."""
        pass

    @abstractmethod
    def create_table_statement(self, table_name: str, columns: List[str]) -> str:
        """Generate CREATE TABLE statement for the dialect."""
        pass


class SQLServerDialect(SQLDialect):
    """SQL Server specific dialect implementation."""

    def format_value(self, value: Any, null_values: List[str]) -> str:
        """Format value for SQL Server."""
        if (value is None or
            value == '' or
            str(value).strip() == '' or
            str(value).strip().upper() in null_values):
            return 'NULL'
        else:
            # Escape single quotes and wrap in quotes
            escaped_value = str(value).replace("'", "''")
            return f"'{escaped_value}'"

    def create_table_statement(self, table_name: str, columns: List[str]) -> str:
        """Generate CREATE TABLE statement for SQL Server."""
        lines = [
            "-- CREATE TABLE statement for temporary table",
            f"CREATE TABLE {table_name} ("
        ]

        # Add column definitions - allow NULL values
        column_defs = [f"    {col} NVARCHAR(MAX) NULL" for col in columns]
        lines.extend(column_defs)

        lines.extend([
            ");",
            "",
            "-- INSERT statements:",
            ""
        ])

        return '\n'.join(lines)


class MySQLDialect(SQLDialect):
    """MySQL specific dialect implementation."""

    def format_value(self, value: Any, null_values: List[str]) -> str:
        """Format value for MySQL."""
        if (value is None or
            value == '' or
            str(value).strip() == '' or
            str(value).strip().upper() in null_values):
            return 'NULL'
        else:
            # Escape single quotes and wrap in quotes
            escaped_value = str(value).replace("'", "\\'")
            return f"'{escaped_value}'"

    def create_table_statement(self, table_name: str, columns: List[str]) -> str:
        """Generate CREATE TABLE statement for MySQL."""
        lines = [
            "-- CREATE TABLE statement for temporary table",
            f"CREATE TABLE {table_name} ("
        ]

        # Add column definitions - allow NULL values
        column_defs = [f"    {col} TEXT NULL" for col in columns]
        lines.extend(column_defs)

        lines.extend([
            ");",
            "",
            "-- INSERT statements:",
            ""
        ])

        return '\n'.join(lines)


class PostgreSQLDialect(SQLDialect):
    """PostgreSQL specific dialect implementation."""

    def format_value(self, value: Any, null_values: List[str]) -> str:
        """Format value for PostgreSQL."""
        if (value is None or
            value == '' or
            str(value).strip() == '' or
            str(value).strip().upper() in null_values):
            return 'NULL'
        else:
            # Escape single quotes and wrap in quotes
            escaped_value = str(value).replace("'", "''")
            return f"'{escaped_value}'"

    def create_table_statement(self, table_name: str, columns: List[str]) -> str:
        """Generate CREATE TABLE statement for PostgreSQL."""
        lines = [
            "-- CREATE TABLE statement for temporary table",
            f"CREATE TABLE {table_name} ("
        ]

        # Add column definitions - allow NULL values
        column_defs = [f"    {col} TEXT NULL" for col in columns]
        lines.extend(column_defs)

        lines.extend([
            ");",
            "",
            "-- INSERT statements:",
            ""
        ])

        return '\n'.join(lines)


class SQLGenerator:
    """
    Generates SQL INSERT statements from CSV data.

    Single Responsibility: SQL generation only
    Open/Closed: Easy to add new SQL dialects
    Dependency Inversion: Depends on SQLDialect abstraction
    """

    DIALECTS = {
        "sqlserver": SQLServerDialect,
        "mysql": MySQLDialect,
        "postgresql": PostgreSQLDialect
    }

    def __init__(self, dialect: str = "sqlserver", batch_size: int = 100):
        """
        Initialize SQL generator.

        Args:
            dialect: SQL dialect to use
            batch_size: Number of rows per batch comment
        """
        self.dialect = self._get_dialect(dialect)
        self.batch_size = batch_size

    def _get_dialect(self, dialect_name: str) -> SQLDialect:
        """
        Get SQL dialect instance.

        Args:
            dialect_name: Name of the dialect

        Returns:
            SQL dialect instance

        Raises:
            ValueError: If dialect is not supported
        """
        if dialect_name not in self.DIALECTS:
            available = ', '.join(self.DIALECTS.keys())
            raise ValueError(f"Unsupported SQL dialect '{dialect_name}'. Available: {available}")

        return self.DIALECTS[dialect_name]()

    def generate_inserts(self, data: List[Dict[str, Any]], table_name: str,
                        null_values: Optional[List[str]] = None) -> str:
        """
        Generate SQL INSERT statements from CSV data.

        Args:
            data: List of dictionaries representing CSV rows
            table_name: Name of the target database table
            null_values: Values to treat as NULL

        Returns:
            SQL INSERT statements as a string
        """
        if not data:
            return "-- No data to insert"

        if null_values is None:
            null_values = ["", "NULL", "null", "None", "none"]

        # Get column names from the first row
        columns = list(data[0].keys())

        # Start building SQL
        sql_lines = self._generate_header(table_name, len(data))

        # Generate CREATE TABLE statement for temporary tables
        if table_name.startswith('#') and not table_name.startswith('##'):
            sql_lines.append(self.dialect.create_table_statement(table_name, columns))

        # Generate INSERT statements
        sql_lines.extend(self._generate_insert_statements(data, table_name, columns, null_values))

        return '\n'.join(sql_lines)

    def _generate_header(self, table_name: str, row_count: int) -> List[str]:
        """
        Generate SQL header comments.

        Args:
            table_name: Name of the table
            row_count: Number of rows

        Returns:
            List of header lines
        """
        return [
            f"-- Generated SQL INSERT statements for table: {table_name}",
            f"-- Total rows: {row_count}",
            "-- Note: Empty values are inserted as NULL (without quotes)",
            ""
        ]

    def _generate_insert_statements(self, data: List[Dict[str, Any]], table_name: str,
                                  columns: List[str], null_values: List[str]) -> List[str]:
        """
        Generate INSERT statements for all rows.

        Args:
            data: CSV data
            table_name: Table name
            columns: Column names
            null_values: Values to treat as NULL

        Returns:
            List of INSERT statements
        """
        sql_lines = []

        for i, row in enumerate(data, 1):
            # Handle values using the dialect
            values = [self.dialect.format_value(row[col], null_values) for col in columns]

            # Create INSERT statement
            columns_str = ', '.join(columns)
            values_str = ', '.join(values)
            insert_stmt = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"

            sql_lines.append(insert_stmt)

            # Add comment for every batch_size rows for readability
            if i % self.batch_size == 0:
                sql_lines.append(f"-- Processed {i} rows")

        return sql_lines

    def add_dialect(self, name: str, dialect_class: type) -> None:
        """
        Add a new SQL dialect.

        Args:
            name: Name of the dialect
            dialect_class: Dialect class (must inherit from SQLDialect)
        """
        if not issubclass(dialect_class, SQLDialect):
            raise ValueError(f"Dialect class must inherit from SQLDialect")

        self.DIALECTS[name] = dialect_class
        print(f"✅ Added new SQL dialect: {name}")

    def list_dialects(self) -> List[str]:
        """
        List all available SQL dialects.

        Returns:
            List of dialect names
        """
        return list(self.DIALECTS.keys())
