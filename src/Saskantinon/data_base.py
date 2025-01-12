#! python
"""
Manage data for saskan-app using sqlite3.

:module:    data_base.py
:class:     DataBase/0
:author:    GM (genuinemerit @ pm.me)

Manage data for saskan_data app using sqlite3.
This is a backend module for handling calls to the DB.
For data models, see data_model_tool, _app, _world
For setting and getting data, see data_get, data_set
"""
import data_model as DM
import data_structs as DS
import pendulum
import shutil
import sqlite3 as sq3
import re

from method_files import FileMethods
from method_shell import ShellMethods
from collections import OrderedDict
from os import path
from pprint import pprint as pp  # noqa: F401

FM = FileMethods()
SM = ShellMethods()
DSC = DS.Colors()


class DataBase(object):
    """Support Sqlite3 database setup, usage, maintenance."""

    def __init__(self, p_context: dict):
        """Initialize DataBase object with configuration from context."""
        self._initialize_attributes(p_context)
        self.db_conn = None

    def _initialize_attributes(self, p_context: dict):
        """Set database-related attributes from the provided context."""
        self.DB = p_context.get("db")
        self.DDL = p_context.get("ddl")
        self.DML = p_context.get("dml")
        self.SASKAN_DB = p_context.get("saskan_db")
        self.SASKAN_BAK = p_context.get("saskan_bak")

    # Generate SQL files from data models
    # ===========================================
    def set_sql_data_type(
        self, p_col_nm: str, p_def_value: object, p_constraints: dict
    ) -> str:
        """
        Convert default value data type to SQLITE data type.
        :param p_col_nm: Column name.
        :param p_def_value: Default value.
        :param p_constraints: Dict of constraints for the table.
        :return: SQLITE data type.
        """
        # Check if JSON constraint applies to the column
        if p_constraints.get("JSON") and p_col_nm in p_constraints["JSON"]:
            return " JSON"

        # Map Python types to SQLite data types
        field_type = type(p_def_value).__name__
        data_types = {
            "str": " TEXT",
            "bool": " BOOLEAN",
            "float": " NUMERIC",
            "int": " INTEGER",
            "bytes": " BLOB",
        }

        # Return corresponding SQLite data type or default to TEXT
        return data_types.get(field_type, " TEXT")

    def set_sql_default(self, p_def_value: object, p_data_type: str) -> str:
        """
        Extract SQL default value from data object.

        :param p_def_value: Value object.
        :param p_data_type: SQLITE data type.
        :return: SQLITE SQL DEFAULT clause.
        """
        col_default = str(p_def_value).strip()

        # Convert boolean string to integer representation
        if col_default == "True":
            col_default = 1
        elif col_default == "False":
            col_default = 0

        # Quote default value unless it's a numeric type
        elif p_data_type not in {"INTEGER", "NUMERIC"}:
            col_default = f"'{col_default}'"

        return f" DEFAULT {col_default}"

    def set_sql_comment(self, p_def_value: object) -> str:
        """
        Convert constraint annotations to SQLITE COMMENT.

        :param p_def_value: May be a class-object value; if so, add a comment.
        :return: SQLITE COMMENT.
        """
        p_def_value_str = str(p_def_value)
        sql_comments = [
            f",   -- {p_def_value_str} object"
            for data_type in ["rect", "pg", "color", "surface"]
            if data_type in p_def_value_str
        ]

        return "".join(sql_comments)

    def set_sql_foreign_keys(self, p_constraints: dict) -> str:
        """
        Generate SQL FOREIGN KEY code from data model.

        :param p_constraints: Dict of constraints for the table.
        :return: One or more lines of SQL code.
        """
        foreign_keys = p_constraints.get("FK", {})
        sql_lines = [
            f"FOREIGN KEY ({col}) REFERENCES {table_name}({column_name}) ON DELETE CASCADE,"
            for col, (table_name, column_name) in foreign_keys.items()
        ]
        return "\n".join(sql_lines)

    def set_sql_primary_key(self, p_pk_uid: str = "") -> str:
        """
        Generate SQL PRIMARY KEY code from a data model.

        Although it is possible to create a Primary Key from composited
        values in SQLITE, a single Key value is actually generated. This
        can create confusion when trying to create a Foreign Key relationship
        to a table with such a key. So this app uses UIDs exclusively as PKs.
        This SQL generator expects a single input value as PK.

        :param p_pk_uid: Name of the PK/UID field for this table.
        :return: One or more lines of SQL code.
        """
        return f"PRIMARY KEY ({p_pk_uid}),\n" if p_pk_uid else ""

    def set_sql_check_constraints(self, p_constraints: dict) -> str:
        """
        Convert CHECK constraint annotations to a SQLITE CHECK rule
        that validates against a list of allowed values, similar to ENUM.

        For example:
        CHECK (col_name IN ('val1', 'val2', 'val3'))

        :param p_constraints: Dict of constraints for the table.
        :return: SQLITE CHECK rule.
        """
        check_constraints = p_constraints.get("CK", {})
        sql_lines = [
            f"CHECK ({ck_col} IN ({', '.join(map(repr, ck_vals))})),\n"
            for ck_col, ck_vals in check_constraints.items()
        ]
        return "".join(sql_lines)

    def generate_create_sql(
        self, p_table_nm: str, p_constraints: dict, p_col_fields: dict
    ) -> list:
        """
        Generate SQL CREATE TABLE code from data model.

        :param p_table_nm: Name of table to create SQL for.
        :param p_constraints: Dict of constraints for the table.
        :param p_col_fields: Dict of column fields, default values.
        :return: List of column names.
        """
        col_names = []
        sqlns = []

        for col_nm, def_value in p_col_fields.items():
            col_names.append(col_nm)
            data_type_sql = self.set_sql_data_type(col_nm, def_value, p_constraints)
            default_sql = self.set_sql_default(
                def_value, data_type_sql.split(" ")[1]
            )
            comment_sql = self.set_sql_comment(def_value)
            sql = f"{col_nm}{data_type_sql}{default_sql}{comment_sql},\n"

            sqlns.append(sql)

        sqlns.extend(
            [
                self.set_sql_check_constraints(p_constraints),
                self.set_sql_foreign_keys(p_constraints),
                self.set_sql_primary_key(p_constraints["PK"])[
                    :-2
                ],  # Remove trailing comma and newline
            ]
        )

        sql = f"CREATE TABLE IF NOT EXISTS {p_table_nm} (\n{''.join(sqlns)});\n"
        FM.write_file(path.join(self.DDL, f"CREATE_{p_table_nm}.sql"), sql)
        return col_names

    def generate_drop_sql(self, p_table_name: str) -> bool:
        """
        Generate SQL DROP TABLE code and write it to a specific file.

        :param p_table_name: Name of the table to drop.
        :return: Boolean flag indicating success/failure of the file writing operation.
        """
        sql = f"DROP TABLE IF EXISTS `{p_table_name}`;\n"
        file_path = path.join(self.DDL, f"DROP_{p_table_name}.sql")

        try:
            # Write the generated SQL to the specified file
            if not FM.write_file(file_path, sql):
                raise IOError(f"Failed to write SQL to {file_path}")
        except Exception as e:
            # Log the exception or handle it according to your application's needs
            print(f"An error occurred during SQL DROP generation: {SM.show_trace(e)}")
            return False

        return True

    def generate_insert_sql(self, p_table_name: str, p_col_names: list) -> bool:
        """
        Generate SQL INSERT code and write it to a specific file.

        :param p_table_name: Name of the table to insert into.
        :param p_col_names: List of column names for the table.
        :return: Boolean flag indicating success/failure of the file writing operation.
        """
        try:
            # Safely handle column names by enclosing them in backticks
            placeholders = ", ".join("?" for _ in p_col_names)
            columns = ",\n".join(f"`{col}`" for col in p_col_names)

            sql = (
                f"INSERT INTO `{p_table_name}` (\n{columns}) "
                + f"VALUES ({placeholders});\n"
            )

            # Use path.join assuming os.path is imported as path in this class
            file_path = path.join(self.DML, f"INSERT_{p_table_name}.sql")

            # Write the generated SQL to the specified file
            if not FM.write_file(file_path, sql):
                raise IOError(f"Failed to write SQL to {file_path}")

        except Exception as e:
            # Log the exception or handle it according to your application's needs
            print(f"An error occurred during SQL INSERT generation: {str(e)}")
            return False

        return True

    def generate_select_all_sql(
        self, p_table_name: str, p_constraints: dict, p_col_names: list
    ) -> bool:
        """
        Generate SQL SELECT ALL code and write it to a specific file.

        :param p_table_name: Name of the table to select from.
        :param p_constraints: Dict of constraints for the query, such as ordering.
        :param p_col_names: List of column names to be selected.
        :return: Boolean flag indicating success/failure of the file writing operation.
        """
        try:
            # Enclose column names in backticks to prevent issues with reserved keywords
            columns = ",\n".join(f"`{col}`" for col in p_col_names)
            sql = f"SELECT {columns}\nFROM `{p_table_name}`"

            # Add ORDER BY clause if it's present in constraints
            # Example of order constraint is...  ORDER: list = ["text_id ASC", "lang_code ASC"]
            # When generating the SQL, only the column name should be enclosed in backticks,
            # not the ASC or DESC keywords.
            if "ORDER" in p_constraints:
                order_by = ", ".join(
                    f"`{col.split()[0]}` {col.split()[1]}" for col in p_constraints["ORDER"]
                )
                sql += f"\nORDER BY {order_by}"

            sql += ";\n"

            # Use path.join assuming os.path is imported as path in this class
            file_path = path.join(self.DML, f"SELECT_ALL_{p_table_name}.sql")

            # Write the generated SQL to the specified file
            if not FM.write_file(file_path, sql):
                raise IOError(f"Failed to write SQL to {file_path}")

        except Exception as e:
            # Log the exception or handle it according to needs
            print(f"An error occurred during SQL SELECT generation: {str(e)}")
            return False

        return True

    def generate_select_all_clean_sql(
        self, p_table_name: str, p_constraints: dict, p_col_names: list
    ) -> bool:
        """
        Generate SQL SELECT ALL CLEAN code and write it to a specific file.

        :param p_table_name: Name of the table to select from.
        :param p_constraints: Dict of constraints for the query, such as ordering.
        :param p_col_names: List of column names to be selected.
        :return: Boolean flag indicating success/failure of the file writing operation.
        """
        try:
            # Enclose column names in backticks to handle reserved keywords safely.
            columns = ",\n".join(f"`{col}`" for col in p_col_names)
            sql = (
                f"SELECT {columns}\n"
                f"FROM `{p_table_name}`\n"
                "WHERE delete_dt IS NULL OR delete_dt = ''"
            )

            # Add ORDER BY clause if it's present in constraints.
            # Example of order constraint is...  ORDER: list = ["text_id ASC", "lang_code ASC"]
            # When generating the SQL, only the column name should be enclosed in backticks,
            # not the ASC or DESC keywords.
            if "ORDER" in p_constraints:
                order_by = ", ".join(
                    f"`{col.split()[0]}` {col.split()[1]}" for col in p_constraints["ORDER"]
                )
                sql += f"\nORDER BY {order_by}"

            sql += ";\n"

            # Use path.join assuming os.path is imported as path in this class.
            file_path = path.join(self.DML, f"SELECT_ALL_{p_table_name}_CLEAN.sql")

            # Write the generated SQL to the specified file.
            if not FM.write_file(file_path, sql):
                raise IOError(f"Failed to write SQL to {file_path}")

        except Exception as e:
            # Log or handle exception according to your application's needs.
            print(f"An error occurred during SQL SELECT generation: {str(e)}")
            return False

        return True

    def generate_select_pk_sql(
        self, p_table_name: str, p_constraints: dict, p_col_names: list
    ) -> bool:
        """
        Generate SQL SELECT WHERE = [PK] query and write it to a file.

        :param p_table_name: Name of the table to select from.
        :param p_constraints: Dict of constraints for the query,
           expects 'PK' key for primary key condition.
        :param p_col_names: List of column names to be included in the selection.
        :return: Boolean flag indicating success/failure of the file writing operation.
        """
        try:
            # Enclose column names in backticks for safe usage.
            columns = ", ".join(f"`{col}`" for col in p_col_names)
            table_name_quoted = f"`{p_table_name}`"
            pk_column_quoted = f"`{p_constraints['PK']}`"

            sql = (
                f"SELECT {columns}\n"
                f"FROM {table_name_quoted}\n"
                f"WHERE {pk_column_quoted} = ?"
            )

            # Add ORDER BY clause if applicable.
            if "ORDER" in p_constraints:
                order_by = ", ".join(f"`{col}`" for col in p_constraints["ORDER"])
                sql += f"\nORDER BY {order_by}"

            sql += ";\n"

            # Construct the file path using os.path (assumed imported as path).
            file_path = path.join(self.DML, f"SELECT_BY_PK_{p_table_name}.sql")

            # Write the generated SQL to the specified file.
            if not FM.write_file(file_path, sql):
                raise IOError(f"Failed to write SQL to {file_path}")

        except KeyError as e:
            # Handle missing keys specifically for better error reporting.
            print(f"Missing required constraint key: {str(e)}")
            return False

        except Exception as e:
            # Log or handle unexpected exceptions according to your application's needs.
            print(f"An error occurred during SQL SELECT generation: {str(e)}")
            return False

        return True

    def generate_update_sql(
        self, p_table_name: str, p_constraints: dict, p_col_names: list
    ) -> bool:
        """
        Generate SQL UPDATE query and write it to a file.
        - Assumes there is only ever one PK column.

        :param p_table_name: Name of the table to update.
        :param p_constraints: Dict of constraints for the query,
            expects 'PK' key for primary key condition.
        :param p_col_names: List of column names to be updated.
        :return: Boolean flag indicating success/failure of the file writing operation.
        """
        try:
            # Enclose table name in backticks for safe usage.
            table_name_quoted = f"`{p_table_name}`"

            # Extract the single primary key column.
            pk_column = p_constraints.get("PK")
            if not pk_column:
                raise KeyError("Primary key ('PK') must be specified in constraints.")

            # Generate SET clause excluding the PK column.
            set_columns = ",\n".join(
                f"`{col}`=?" for col in p_col_names if col != pk_column
            )

            # Construct the WHERE clause with the single PK.
            where_clause = f"`{pk_column}`=?"

            # Form the complete SQL statement.
            sql = (
                f"UPDATE {table_name_quoted} SET\n{set_columns}\n"
                f"WHERE {where_clause};\n"
            )

            # Construct the file path using os.path (assumed imported as path).
            file_path = path.join(self.DML, f"UPDATE_{p_table_name}.sql")

            # Write the generated SQL to the specified file.
            if not FM.write_file(file_path, sql):
                raise IOError(f"Failed to write SQL to {file_path}")

        except KeyError as e:
            # Handle missing keys specifically for better error reporting.
            print(f"Missing required constraint key: {str(e)}")
            return False

        except Exception as e:
            # Log or handle unexpected exceptions according to your application's needs.
            print(f"An error occurred during SQL UPDATE generation: {str(e)}")
            return False

        return True

    def generate_delete_sql(self, p_table_name: str, p_constraints: dict) -> bool:
        """
        Generate SQL DELETE code.
        - Assumes there is only one PK column.
        - Use this only for purging old virtually deleted records.
        :param p_table_name: Name of table to delete from
        :param p_constraints: Dict of constraints for the table
        :writes: SQL file to [APP]/ddl/DELETE_[p_table_name].sql
        :returns: Boolean flag True if successful, False otherwise.
        """
        try:
            # Enclose table name in backticks for safe usage.
            table_name_quoted = f"`{p_table_name}`"

            # Assume there is only one PK.
            pk_column = p_constraints.get("PK")

            # Validate that a PK constraint is provided.
            if not pk_column or not isinstance(pk_column, str):
                raise ValueError(
                    "A single primary key constraint must be provided as a string."
                )

            # Construct the SQL DELETE statement.
            sql = f"DELETE FROM {table_name_quoted}\nWHERE `{pk_column}`=?;\n"

            # Construct the file path using os.path (assumed imported as path).
            file_path = path.join(self.DDL, f"DELETE_{p_table_name}.sql")

            # Write the generated SQL to the specified file.
            if not FM.write_file(file_path, sql):
                raise IOError(f"Failed to write SQL to {file_path}")

            return True

        except Exception as e:
            # Log or handle unexpected exceptions according to your application's needs.
            print(f"An error occurred during SQL DELETE generation: {str(e)}")
            return False

    def parse_field_definitions(self, p_dm_doc: str) -> dict:
        """
        Parse field definitions from metadata in a data model's class-level docstring.
        :param p_dm_doc: Docstring from a data model class formatted as follows
          in order to identify metadata field descriptions:
            $$
            - field_name: field_description
            $$
        :returns: dict of field definitions
        """
        fields = OrderedDict()

        # Split the docstring once by "$$", focusing on the part after the first occurrence.
        *_, field_definitions = p_dm_doc.partition("$$")

        # Process each line in the field definitions section.
        for line in field_definitions.splitlines():
            line = line.strip()
            if line.startswith("- ") and ":" in line:
                # Split into field name and definition only once, expecting exactly one colon.
                field_nm, definition = map(str.strip, line[2:].split(":", 1))
                fields[field_nm] = definition

        return fields

    def generate_insert_metadata_sql(
        self, p_data_model: object, p_name_space: str
    ) -> bool:
        """
        Create or extend SQL INSERT_METADATA code.
        Read in the existing INSERT_METADATA.sql file if exists, else create one.
        Add new metadata based on reading the data model's docstring.
        :param p_data_model: Data model class object
        :param p_name_space: Name space of the data model class, e.g. 'app' or 'fin'
        :writes: SQL file to [APP]/ddl/CREATE_TABLE_[p_table_name].sql
        :returns: Boolean indicating success/failure.

        @DEV:
        - Fix this so that a comma is always added to the end of the VALUES line,
           even when it is the last item for a given table name.
        - Only replace the comma with a semi-colon on the penultimate line.
        """
        try:
            field_defs = self.parse_field_definitions(p_data_model.__doc__)
            if not field_defs:
                # There are no field definitions to process.
                return True

            sql_file_path = path.join(self.DDL, "INSERT_METADATA.sql")
            if FM.is_file_or_dir(sql_file_path):
                SQL = FM.get_file(sql_file_path)
                SQL = SQL.rstrip(";")  # Remove trailing semicolon if present
            else:
                # If the SQL file is empty, copy from template and remove placeholder
                FM.copy_one_file(
                    path.join(self.DML, "INSERT_METADATA.sql"), sql_file_path
                )
                SQL = FM.get_file(sql_file_path).replace("(?, ?, ?, ?, ?, ?, ?);", "")

            # Extend the SQL insert statement with new metadata fields
            for f_nm, f_def in field_defs.items():
                f_def = f_def.replace('"', "").replace("'", "")
                SQL += "\n"
                SQL += f'("{SM.get_uid()}", '
                SQL += f'"{p_name_space}", '
                SQL += f'"{p_data_model.__name__}", '
                SQL += f'"{p_data_model._tablename}", '
                SQL += f'"{f_nm}", '
                SQL += f'"{f_def}", '
                SQL += '""),'
            SQL = SQL[:-1] + ";"

            # Write the updated SQL back to the file
            # scrub the SQL to ensure that there is a comma at the end of every VALUES line
            # and that the last line ends with a semicolon.
            SQL = SQL.replace(")", "),").replace("),,", "),").replace("),;", ");")
            SQL = SQL.replace("), VAL", ") VAL")

            FM.write_file(sql_file_path, SQL)
            return True

        except Exception as e:
            # Log the exception or handle it as needed
            print(f"An error occurred: {SM.show_trace(e)}")
            return False

    def generate_sql(self, p_data_model: object, p_name_space: str) -> bool:
        """
        Generate a full set of SQL code from a data model, including specialized INSERT scripts
        to populate the metadata table.

        :param p_data_model: Data model class object.
        :param p_name_space: Namespace for the data model.
        :return: Boolean flag indicating success/failure of the process.
        """
        try:
            # Extract constraints and model attributes while avoiding private/undesired attributes
            constraints = {
                k: v
                for k, v in p_data_model.Constraints.__dict__.items()
                if not k.startswith("_")
            }
            table_name = p_data_model._tablename
            model_dict = {
                k: v
                for k, v in p_data_model.__dict__.items()
                if not k.startswith("_")
                and k not in ("to_dict", "from_dict", "Constraints")
            }
            # Generate create SQL and capture column names
            col_names = self.generate_create_sql(table_name, constraints, model_dict)

            # Method calls that rely on successful execution of prior steps
            # To help with debugging, may want to wrap these in a dict so I can print the keys
            operations = {
                "drop": lambda: self.generate_drop_sql(table_name),
                "insert": lambda: self.generate_insert_sql(table_name, col_names),
                "select_all": lambda: self.generate_select_all_sql(
                    table_name, constraints, col_names
                ),
                "select_all_clean": lambda: self.generate_select_all_clean_sql(
                    table_name, constraints, col_names
                ),
                "select_pk": lambda: self.generate_select_pk_sql(
                    table_name, constraints, col_names
                ),
                "update": lambda: self.generate_update_sql(
                    table_name, constraints, col_names
                ),
                "delete": lambda: self.generate_delete_sql(table_name, constraints),
                "insert_metadata": lambda: self.generate_insert_metadata_sql(
                    p_data_model, p_name_space
                ),
            }

            # Execute each operation and ensure all succeed
            for op_type, operation in operations.items():
                if not operation():
                    print(f"Call to generate {op_type} SQL for {table_name} failed.")
                    return False

        except Exception as e:
            # Log the exception or handle it according to your application's needs
            print(f"An error occurred during SQL generation. {SM.show_trace(e)}")
            return False

        return True

    # DataBase Connections
    # ===========================================

    def __set_fk_pragma(self, p_foreign_keys_on: bool):
        """'PRIVATE'
        Set the foreign_keys pragma to ON or OFF
        FK's should be ignored when a table is dropped.
        This could potentially cause problems so keep an eye on it.
        As long as dropping, re-creating the entire DB, should be OK.
        :param p_foreign_keys_on: If True, set foreign_keys to on
        """
        pragma_value = "ON" if p_foreign_keys_on else "OFF"
        self.db_conn.execute(f"PRAGMA foreign_keys = {pragma_value};")

    def disconnect_db(self):
        """Close cursors and drop DB connection to self object."""
        if hasattr(self, "db_conn") and self.db_conn is not None:
            try:
                if hasattr(self, "cur") and self.cur is not None:
                    self.cur.close()
                self.db_conn.close()
            except Exception as e:
                # Log or handle specific exceptions if needed
                print(f"An error occurred while closing the database: {e}")
            finally:
                self.db_conn = None

    def connect_db(self, p_db_nm: str, p_foreign_keys_on: bool = True) -> bool:
        """Open DB connection.

        Create a DB file at the specified location if one does not already exist.
        Set foreign key pragma ON by default. If doing a DROP, set to OFF.

        :param p_db_nm: Name of DB to connect to.
        :param p_foreign_keys_on: Default True
        :set db_conn: The database connection
        :set cur: Cursor for the connection
        """
        self.disconnect_db()

        try:
            self.db_conn = sq3.connect(p_db_nm)
            self.cur: sq3.Cursor = self.db_conn.cursor()

            # Set foreign keys pragma
            self.__set_fk_pragma(p_foreign_keys_on)

            return True  # Connection successful

        except sq3.Error as err:
            print(f"Database connection error: {err}")
            return False  # Connection failed

    # SQL Helpers
    # ===========================================
    def get_sql_file(self, p_sql_loc: str, p_sql_nm: str) -> str:
        """Read SQL from a named file.

        :param p_sql_loc: Location of the SQL file directory.
        :param p_sql_nm: Name of the SQL file in [APP]/sql.
        :return: Content of the SQL file.
        :raises FileNotFoundError: If the SQL file does not exist.
        :raises ValueError: If the SQL file is empty.
        """
        # Normalize and construct the SQL file name
        sql_nm = f"{p_sql_nm.rsplit('.', 1)[0].upper()}.sql"

        # Construct the full path to the SQL file
        sql_path = path.join(p_sql_loc, sql_nm)

        # Read the content of the SQL file
        try:
            SQL: str = FM.get_file(sql_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"SQL file {sql_nm} not found at location {p_sql_loc}."
            )

        # Check if the SQL content is empty
        if not SQL.strip():
            raise ValueError(f"SQL file {sql_nm} is empty.")

        return SQL

    def get_db_columns(self, p_tbl_nm: str = "", p_sql_select: str = "") -> list:
        """Retrieve a list of column names for a specified table.

        :param p_tbl_nm: Optional. If provided, use this instead of scanning the SQL code.
        :param p_sql_select: Optional. Text content of a well-structured SQL SELECT file,
                             where the table name is the last word in the first line.
                             Use this if p_tbl_nm is not provided.
        :return: List of column names for the table.
        :raises ValueError: If neither p_tbl_nm nor a valid table name from p_sql_select
            is provided.
        """
        # Determine the table name
        if not p_tbl_nm:
            try:
                tbl_nm = p_sql_select.split("FROM ")[1].split()[0].rstrip(",;")
            except (IndexError, AttributeError):
                raise ValueError(
                    "Table name could not be determined from p_sql_select."
                )
        else:
            tbl_nm = p_tbl_nm

        # Execute PRAGMA to retrieve column information
        self.cur.execute(f"PRAGMA table_info({tbl_nm})")
        cols = self.cur.fetchall()

        # Extract column names
        col_nms = [c[1] for c in cols]

        return col_nms

    def set_dict_from_cursor(self, p_cols: list) -> OrderedDict:
        """
        Translate current cursor contents into a dict of lists.

        :param p_cols: List of column names.
        :return: OrderedDict of lists, with column names as keys
                 and in the same order as listed in table-column order.
        """
        # Initialize OrderedDict with empty lists for each column
        result = OrderedDict((col, []) for col in p_cols)

        # Fetch all rows from the cursor
        fetch_all_rows = self.cur.fetchall()  # list of tuples

        # Populate the OrderedDict
        for row in fetch_all_rows:
            for col, value in zip(p_cols, row):
                result[col].append(value)

        return result

    # Executing Raw SQL
    # ===========================================
    def execute_sql(self, p_sql_code: str, p_foreign_keys_on: bool):
        """
        DENIGRATED -- potentially dangerous.

        # May want to do something like write a key to
        # /tmp or /dev/shm, pass it in here so it can be verified.

        Execute a SELECT SQL query passed in as a string.

        :param p_sql_code: The SQL code to be executed.
        :param p_foreign_keys_on: Set foreign key pragma ON or OFF.
        :raises Exception: If the SQL code is not a SELECT statement or contains unsafe operations.
        :return: A dictionary with column names as keys and lists of column data as values.
        """
        # Connect to the database
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=p_foreign_keys_on)

        # Prepare and validate SQL code
        sql = p_sql_code.strip()
        sql_upper = sql.upper()

        if not sql_upper.startswith("SELECT"):
            raise Exception("SQL code refused. Only SELECT statements are allowed.")

        # Check for potentially dangerous SQL operations
        forbidden_keywords = {"DROP", "INSERT", "UPDATE", "DELETE", "PRAGMA"}
        if any(keyword in sql_upper for keyword in forbidden_keywords):
            raise Exception("SQL code refused due to unsafe operations.")

        # Execute the SQL query
        self.cur.execute(sql)

        # Get column names and fetch data
        cols = self.get_db_columns(p_sql_select=sql)
        data = self.cur.fetchall()

        # Construct result dictionary
        result = (
            {col: [row[i] for row in data] for i, col in enumerate(cols)}
            if data
            else {col: [] for col in cols}
        )

        # Disconnect from the database
        self.disconnect_db()

        return result

    # Executing SQL Scripts
    # ===========================================
    def execute_select_all(self, p_table_nm: str) -> dict:
        """
        Run a SQL SELECT_ALL* script and return data as a dictionary of lists.
        This will return both virtually-deleted and non-deleted records.

        :param p_table_nm: Name of the SQL table.
        :return: Dictionary with column names as keys and lists of column data as values.
        """
        # Connect to the database
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)

        # Prepare SQL statement
        sql = self.get_sql_file(self.DML, f"SELECT_ALL_{p_table_nm.upper()}")

        # Get column names
        cols = self.get_db_columns(p_sql_select=sql)

        # Execute the SQL query and fetch data
        self.cur.execute(sql)
        data = self.cur.fetchall()

        # Construct result dictionary
        result = (
            {col: [row[i] for row in data] for i, col in enumerate(cols)}
            if data
            else {col: [] for col in cols}
        )

        # Disconnect from the database
        self.disconnect_db()

        return result

    def execute_select_all_clean(self, p_table_nm: str) -> dict:
        """
        Run a SQL SELECT_ALL_*_CLEAN script and return data as a dictionary of lists.
        This will return only recrods that have not been virtually deleted.

        :param p_table_nm: Name of the SQL table.
        :return: Dictionary with column names as keys and lists of column data as values.
        """
        # Connect to the database
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)

        # Prepare SQL statement
        sql = self.get_sql_file(self.DML, f"SELECT_ALL_{p_table_nm.upper()}_CLEAN")

        # Get column names
        cols = self.get_db_columns(p_sql_select=sql)

        # Execute the SQL query and fetch data
        self.cur.execute(sql)
        data = self.cur.fetchall()

        # Construct result dictionary
        result = (
            {col: [row[i] for row in data] for i, col in enumerate(cols)}
            if data
            else {col: [] for col in cols}
        )

        # Disconnect from the database
        self.disconnect_db()

        return result

    def execute_select_by(self, p_dmo: object, p_pk_value: str) -> dict:
        """
        Run a SQL SELECT_BY script using parameters to select by primary key,
        which is always the UID. Return data as a dictionary.

        :param p_dmo: Data model object for the table.
        :param p_pk_value: Primary key value to match on.
        :return: Dictionary with column names as keys and their corresponding data values.
        """
        # Connect to the database
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)

        # Prepare SQL statement
        sql = self.get_sql_file(self.DML, f"SELECT_BY_PK_{p_dmo._tablename}")

        # Retrieve column definitions from the data model
        rec = DM.cols_to_dict(p_dmo)[p_dmo._tablename]
        keys = list(rec.keys())

        # Execute the SQL query with primary key value
        self.cur.execute(
            sql, [p_pk_value]
        )  # Wrap p_pk_value in a list for SQL execution
        data = self.cur.fetchone()  # Fetch only one record since it's based on PK

        # Update record dictionary with fetched data
        if data:
            rec.update({keys[n]: value for n, value in enumerate(data)})

        # Disconnect from the database
        self.disconnect_db()

        return rec

    def execute_ddl(self, p_sql_list: list, p_foreign_keys_on: bool) -> bool:
        """
        Run one or more static SQL DROP or CREATE scripts.
        DELETEs have a separate method.

        - If these are DROP statements, then set p_foreign_keys_on to False.
        - SQL names must be passed in as a list, even if just one script.
        - No dynamic parameters.
        - Executed as one transaction. If anything fails, all roll back.
        - Will print error messages but not raise exceptions.

        :param p_sql_list: List of external SQL file names.
        :param p_foreign_keys_on: Set foreign key pragma ON or OFF.
        :return: True if transaction succeeds, False if it fails.
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on)
        try:
            self.cur.execute("BEGIN")
            for p_sql_nm in p_sql_list:
                sql = self.get_sql_file(self.DDL, p_sql_nm)
                self.cur.execute(sql)
            self.db_conn.commit()
            return True
        except sq3.Error as e:
            # Rollback the transaction if any operation fails
            self.db_conn.rollback()
            print(f"{DSC.CL_RED}{DSC.CL_BOLD}Rolled back: {e}{DSC.CL_END}")
            print(f"Transaction failed on processing of:{DSC.CL_END}{DSC.CL_YELLOW} {p_sql_nm}...")
            pp(("sql code: ", sql))
            print(f"{DSC.CL_END}")
            print(f"{DSC.CL_DARKCYAN}Processing continues...{DSC.CL_END}")
            return False
        finally:
            self.disconnect_db()

    def execute_insert(self, p_tbl_nm: str, p_values: tuple) -> bool:
        """
        Run a single SQL INSERT command with dynamic values as parameters.

        This method assumes:
        - A full list of values satisfying one row is passed in.
        - Caller knows what values to provide and in what order.

        If the insert fails, the method will print an error message and return False
        but will not raise an exception.

        :param p_tbl_nm: Name of database table.
        :param p_values: n-tuple of values to insert.
        :return: True if insertion succeeds, False otherwise.
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        SQL = self.get_sql_file(self.DML, f"INSERT_{p_tbl_nm}")
        try:
            # The p_values tuple structure may contain first the UID, then the rest
            # of the values enclosed in a sub-tuple.
            # For example: (UID, (val1, val2, val3, ...))
            # Or it may already be a flat tuple.
            # For an insert, we need to flatten this structure into a single-level
            # tuple to send to self.cur.execute() if it has a sub-tuple.
            # Otherwise, we can just use the p_values tuple as is.

            if isinstance(p_values[1], tuple):
                # Flatten the structure if the second element is a tuple
                flattened_values = (p_values[0], *p_values[1])
            else:
                # Use the original tuple as it is already flat
                flattened_values = p_values

            self.cur.execute(SQL, flattened_values)

            self.db_conn.commit()
            return True
        except sq3.Error as e:
            print(f"{DSC.CL_RED}{DSC.CL_BOLD}Error in execute_insert: {e}{DSC.CL_END}")
            print(f"{DSC.CL_YELLOW}SQL: {SQL}")
            print(f"values: {flattened_values}{DSC.CL_END}")
            print(f"{DSC.CL_DARKCYAN}Processing continues...{DSC.CL_END}")
            return False
        finally:
            self.disconnect_db()

    def execute_update(self, p_tbl_nm: str, p_key_val: str, p_values: tuple) -> bool:
        """
        Run a SQL UPDATE command with dynamic values.

        This method assumes:
        - A full list of values is passed in, not only the changed ones.
        - Caller knows what values to provide and in what order.

        :param p_tbl_nm: Name of table to update.
        :param p_key_val: Value of primary key (UID) to match on.
        :param p_values: n-tuple of values to update.
        :return: True if update succeeds, False otherwise.
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        SQL = self.get_sql_file(self.DML, f"UPDATE_{p_tbl_nm}")
        try:
            # Ensure p_key_val is added at the end for the WHERE clause
            self.cur.execute(SQL, p_values + (p_key_val,))
            self.db_conn.commit()
            return True
        except sq3.Error as e:
            print(f"{DSC.CL_RED}{DSC.CL_BOLD}Error in execute_update: {e}{DSC.CL_END}")
            print(f"SQL: {SQL}")
            print(f"p_values: {p_values}")
            return False
        finally:
            self.disconnect_db()

    def execute_delete(self, p_sql_nm: str, p_key_val: str) -> bool:
        """
        Run a SQL DELETE command using a key value (primary key) for the WHERE clause.

        This method is intended for physical purge processes.

        :param p_sql_nm: Name of the SQL file.
        :param p_key_val: Value of the primary key to match on.
        :return: True if delete succeeds, False otherwise.
        @DEV:
        - May need to set p_foreign_keys_on to False?
        - Will delete-cascade logic work in SQLite? Test this.
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        SQL = self.get_sql_file(self.DDL, p_sql_nm)
        try:
            self.cur.execute(SQL, (p_key_val,))
            self.db_conn.commit()
            return True
        except sq3.Error as e:
            print(f"Error in execute_delete: {e}")
            print(f"SQL: {SQL}")
            print(f"PK: {p_key_val}")
            return False
        finally:
            self.disconnect_db()

    def get_check_constraint_values(self, p_tbl_nm: str, p_col_nm: str) -> list:
        """
        Retrieve a list of valid CHECK constraint values for a given
        table and column by parsing the SQL code of the table.

        :param p_tbl_nm: Name of the table to check.
        :param p_col_nm: Name of the column to check.
        :return: List of valid CHECK constraint values or an empty list if none are found.
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        try:
            self.cur.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?;",
                (p_tbl_nm,),
            )
            row = self.cur.fetchone()
            if not row:
                return []

            sql = row[0]
            check_constraints = re.findall(r"CHECK\s*\(\s*([^)]*?)\)", sql)

            for constraint in check_constraints:
                if p_col_nm in constraint:
                    valid_values = re.findall(r"'(.*?)'", constraint)
                    if valid_values:
                        return valid_values

            return []
        finally:
            self.disconnect_db()

    # Backup, Archive and Restore
    # ===========================================

    def archive_db(self, p_db: str):
        """
        Copy a DB file to archive location.
        - The DB being archived might be main or backup.

        :param p_db: Path to database file to be archived.
        """
        # Generate a timestamp for the archive operation
        arcv_dttm = pendulum.now().format("YYYYMMDD_HHmmss")
        arcv_nm = p_db.replace(".db", "_") + arcv_dttm + ".arcv"

        # Perform the insert operation for the archive metadata
        self.execute_insert(
            "BACKUP",
            (
                SM.get_uid(),
                f"Archive {arcv_dttm}",
                arcv_dttm,
                "archive",
                str(p_db),
                arcv_nm,
                "",
            ),
        )

        # Copy the specified database file to the archive location
        shutil.copyfile(p_db, arcv_nm)

    def backup_db(self, p_db: str, p_bak: str):
        """
        Copy specified DB file to backup location.
        Generally this would be the main DB to a backup DB.
        - There is only ever one backup file.
        - The existing backup is overwritten. If desired, archive the backup
          before backing up the main DB.

        :param p_db: Path to specified database file
        :param p_bak: Path to backup database file

        @DEV:
        - May want to add a check to see if the backup file exists
        - Under some initial conditions this method could be called before
          the backup table is created. In this case we either need to create
          the backup table skip writing to it.
        """
        # Generate a timestamp for the backup operation
        bkup_dttm = pendulum.now().format("YYYYMMDD_HHmmss")

        # Perform the insert operation for the backup metadata
        self.execute_insert(
            "BACKUP",
            (
                SM.get_uid(),
                f"Backup {bkup_dttm}",
                bkup_dttm,
                "backup",
                str(p_db),
                p_bak,
                "",
            ),
        )

        # Copy the specified database file to the backup location
        shutil.copyfile(p_db, p_bak)

    def restore_db(self, p_restore: str):
        """
        Copy a backed up or archived DB file to main location.

        :param p_restore: Path to specified database file to restore from

        @DEV:
        - May need to add checks for existence of files and the backup table.
        """
        # Generate a timestamp for the restore operation
        restore_dttm = pendulum.now().format("YYYYMMDD_HHmmss")

        # Perform the insert operation for the restore metadata
        self.execute_insert(
            "BACKUP",
            (
                SM.get_uid(),
                f"Restore {restore_dttm}",
                restore_dttm,
                "restore",
                p_restore,
                self.DB,
                "",
            ),
        )

        # Copy the specified database file to the main database location
        shutil.copyfile(p_restore, self.DB)
