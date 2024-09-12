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
import shutil
import sqlite3 as sq3
from collections import OrderedDict
from copy import copy
from os import path
from pprint import pprint as pp  # noqa: F401

import pendulum
from method_files import FileMethods
from method_shell import ShellMethods

FM = FileMethods()
SM = ShellMethods()


class DataBase(object):
    """Support Sqlite3 database setup, usage, maintenance."""

    def __init__(self, p_context: dict):
        """Initialize DataBase object."""
        self.DB = p_context["db"]
        self.DDL = p_context["ddl"]
        self.DML = p_context["dml"]
        self.SASKAN_DB = p_context["saskan_db"]
        self.SASKAN_BAK = p_context["saskan_bak"]
        self.db_conn = None

    # Generate SQL files from data models
    # ===========================================
    def set_sql_data_type(
        self, p_col_nm: str, p_def_value: object, p_constraints: dict
    ) -> str:
        """
        Convert default value data type to SQLITE data type.
        :args:
        - p_col_nm (str) column name
        - p_def_value (object) default value
        - p_constraints (dict) Dict of constraints for the table
        :returns:
        - (str) SQLITE data type
        """
        sql = ""
        if "JSON" in p_constraints.keys() and p_col_nm in p_constraints["JSON"]:
            sql = " JSON"
        else:
            field_type = type(p_def_value).__name__
            data_types = {
                "str": " TEXT",
                "bool": " BOOLEAN",
                "float": " NUMERIC",
                "int": " INTEGER",
            }
            sql = data_types.get(field_type, " TEXT")
        return sql

    def set_sql_default(self, p_def_value: object, p_data_type: str) -> str:
        """
        Extract SQL default value from data object.
        :args:
        - p_def_value (object) value object
        - p_data_type (str) SQLITE data type
        :returns:
        - (str) SQLITE SQL DEFAULT clause
        """
        sql = ""
        col_default = str(p_def_value).strip()
        if col_default == "True":
            col_default = "1"
        elif col_default == "False":
            col_default = "0"
        elif p_data_type not in ("INTEGER", "NUMERIC"):
            col_default = f"'{col_default}'"
        sql = f" DEFAULT {col_default}"
        return sql

    def set_sql_comment(self, p_def_value: object) -> str:
        """
        Convert constraint annotations to SQLITE COMMENT.
        :args:
        - p_def_value (object) may be a class-object value
          if so, then add a comment
        :returns:
        - (str) SQLITE COMMENT
        """
        sql = ""
        for data_type in ["rect", "pg", "color", "surface"]:
            if data_type in str(p_def_value):
                sql += f",   -- {str(p_def_value)} object"
        return sql

    def set_sql_column_group(
        self, p_col_nm: str, p_constraints: dict, p_col_names: list
    ) -> tuple:
        """
        Generate SQL CREATE TABLE code from a data model
        for specialized data types, by splitting them into separate
        columns grouped with a similar name.
        @DEV:
        - Denigrated. Try to avoid having to do this.
        :args:
        - p_col_nm (str) Name of customized data objects
        - p_constraints (dict) Dict of constraints for the table
        - p_col_names (list) List of column names already processed
        :returns: tuple of:
        - (str) One or more lines of SQL code
        - (list) Updated list of column names already processed
        """
        sql = ""
        if "GROUP" in p_constraints and p_col_nm in p_constraints["GROUP"]:
            group_class = copy(p_constraints["GROUP"][p_col_nm])
            sql += f"-- GROUP {p_col_nm}: {str(group_class)}\n"
            sub_model = {
                k: v for k, v in group_class.__dict__.items() if not k.startswith("_")
            }
            for k, v in sub_model.items():
                g_col_nm = f"{p_col_nm}_{k}"
                p_col_names.append(g_col_nm)
                sql += f"{g_col_nm}"
                data_type = self.set_sql_data_type(g_col_nm, v, p_constraints)
                sql += data_type
                sql += self.set_sql_default(v, data_type.split(" ")[1])
                sql += self.set_sql_comment(v)
                sql += ",\n"
        return (sql, p_col_names)

    def set_sql_foreign_keys(self, p_constraints: dict) -> str:
        """
        Generate SQL FOREIGN KEY code from data model.
        :args:
        - p_constraints (dict) Dict of constraints for the table
        :returns:
        - (str) One or more lines of SQL code
        """
        sql = ""
        foreign_keys = p_constraints.get("FK", {})
        for col, ref in foreign_keys.items():
            table_name, column_name = ref[0], ref[1]
            sql += (
                f"FOREIGN KEY ({col}) REFERENCES {table_name}"
                + f"({column_name}) ON DELETE CASCADE,\n"
            )
        return sql

    def set_sql_primary_key(self, p_constraints: dict) -> str:
        """
        Generate SQL PRIMARY KEY code from a data model.
        It is possible to create a composite PK, but know that a
        single Key is generated. This can create problems when
        creating a Foreign Key relationship.  Best to use UIDs instead
        and just have single column = UID = PK.
        :args:
        @DEV:
        - Kind of a kludge here, where we accept composities, but
          only select the first one in the list for the PK. Probably
          cleaner to just say, "single-column PK's only".
        - p_constraints (dict) Dict of constraints for the table
        :returns:
        - (str) One or more lines of SQL code
        """
        primary_key = p_constraints.get("PK")
        if primary_key:
            uid_pk = list(primary_key.keys())[0]
            sql = f"PRIMARY KEY ({uid_pk}),\n"
        else:
            sql = ""
        return sql

    def set_sql_check_constraints(self, p_constraints: dict) -> str:
        """
        Convert CHECK constraint annotations to a SQLITE CHECK rule
        that validates against a list of allowed values, similar to ENUM.
        For example:
        CHECK (col_name IN ('val1', 'val2', 'val3'))
        :args:
        - p_constraints (dict) Dict of constraints for the table
        :returns:
        - (str) SQLITE CHECK rule
        """
        check_constraints = p_constraints.get("CK", {})
        sql = ""
        for ck_col, ck_vals in check_constraints.items():
            ck_vals = ["'" + str(v) + "'" for v in ck_vals]
            check_values = ", ".join(map(str, ck_vals))
            sql += f"CHECK ({ck_col} IN ({check_values})),\n"
        return sql

    def generate_create_sql(
        self, p_table_nm: str, p_constraints: dict, p_col_fields: dict
    ) -> list:
        """
        Generate SQL CREATE TABLE code from data model.
        :args:
        - p_table_name (str) Name of table to create SQL for
        - p_constraints (dict) Dict of constraints for the table
        - p_col_fields (dict) Dict of column fields, default values
        :writes:
        - SQL file to [APP]/sql/CREATE_[p_table_name].sql
        :returns:
        - (list) List of column names
        """
        col_names = []
        sqlns = []

        for col_nm, def_value in p_col_fields.items():
            sql, col_names = self.set_sql_column_group(col_nm, p_constraints, col_names)

            if not sql:
                col_names.append(col_nm)
                data_type_sql = self.set_sql_data_type(col_nm, def_value, p_constraints)
                default_sql = self.set_sql_default(
                    def_value, data_type_sql.split(" ")[1]
                )
                comment_sql = self.set_sql_comment(def_value)
                sql = f"{col_nm}{data_type_sql}{default_sql}{comment_sql},\n"

            sqlns.append(sql)

        sqlns.append(self.set_sql_check_constraints(p_constraints))
        sqlns.append(self.set_sql_foreign_keys(p_constraints))
        sqlns.append(self.set_sql_primary_key(p_constraints))
        sqlns[-1] = sqlns[-1][:-2]

        sql = f"CREATE TABLE IF NOT EXISTS {p_table_nm} " + f"(\n{''.join(sqlns)});\n"
        FM.write_file(path.join(self.DDL, f"CREATE_{p_table_nm}.sql"), sql)

        return col_names

    def generate_drop_sql(self, p_table_name: str):
        """
        Generate SQL DROP TABLE code.
        :args:
        - p_table_name (str) Name of table to drop
        :writes:
        - SQL file to [APP]/sql/DROP_[p_table_name].sql
        """
        sql = f"DROP TABLE IF EXISTS {p_table_name};\n"
        file_path = path.join(self.DDL, f"DROP_{p_table_name}.sql")
        FM.write_file(file_path, sql)

    def generate_insert_sql(self, p_table_name: str, p_col_names: list):
        """
        Generate SQL INSERT code.
        :args:
        - p_table_name (str) Name of table to insert into
        - p_col_names (list) List of column names for the table
        :writes:
        - SQL file to [APP]/sql/INSERT_[p_table_name].sql
        """
        placeholders = ", ".join(["?" for _ in p_col_names])
        columns = ",\n".join(p_col_names)
        sql = (
            f"INSERT INTO {p_table_name} (\n{columns}) " + f"VALUES ({placeholders});\n"
        )
        file_path = path.join(self.DML, f"INSERT_{p_table_name}.sql")
        FM.write_file(file_path, sql)

    def generate_select_all_sql(
        self, p_table_name: str, p_constraints: dict, p_col_names: list
    ):
        """
        Generate SQL SELECT ALL code.
        :args:
        - p_table_name (str) Name of table to select from
        - p_constraints (dict) Dict of constraints for the table
        - p_col_names (list) List of column names for the table
        :writes:
        - SQL file to [APP]/sql/SELECT_ALL_[p_table_name].sql
        """
        columns = ",\n".join(p_col_names)
        sql = f"SELECT {columns}\nFROM {p_table_name}"

        if "ORDER" in p_constraints:
            order_by = ", ".join(p_constraints["ORDER"])
            sql += f"\nORDER BY {order_by}"

        sql += ";\n"

        file_path = path.join(self.DML, f"SELECT_ALL_{p_table_name}.sql")
        FM.write_file(file_path, sql)

    def generate_select_pk_sql(
        self, p_table_name: str, p_constraints: dict, p_col_names: list
    ):
        """
        Generate SQL SELECT WHERE = [PK] code.
        :args:
        - p_table_name (str) Name of table to select from
        - p_constraints (dict) Dict of constraints for the table
        - p_col_names (list) List of column names for the table
        :writes:
        - SQL file to [APP]/sql/SELECT_BY_PK_[p_table_name].sql
        @DEV:
        - Simplify if we go with "one PK column only" rule
        """
        pk_conditions = " AND ".join([f"{col}=?" for col in p_constraints["PK"]])
        sql = (
            f"SELECT {', '.join(p_col_names)}\n"
            + f"FROM {p_table_name}\nWHERE {pk_conditions}"
        )

        if "ORDER" in p_constraints:
            order_by = ", ".join(p_constraints["ORDER"])
            sql += f"\nORDER BY {order_by}"

        sql += ";\n"

        file_path = path.join(self.DML, f"SELECT_BY_PK_{p_table_name}.sql")
        FM.write_file(file_path, sql)

    def generate_update_sql(
        self, p_table_name: str, p_constraints: dict, p_col_names: list
    ):
        """
        Generate SQL UPDATE code.
        - If more than one PK, then use AND logic in the WHERE clause
        :args:
        - p_table_name (str) Name of table to update
        - p_constraints (dict) Dict of constraints for the table
        - p_col_names (list) Dict of column names for the table
        :writes:
        - SQL file to [APP]/sql/UPDATE_[p_table_name].sql
        @DEV:
        - Simplify if we go with "one PK column only" rule
        """
        pk_conditions = " AND ".join([f"{col}=?" for col in p_constraints["PK"]])
        set_columns = ",\n".join(
            [f"{col}=?" for col in p_col_names if col not in p_constraints["PK"]]
        )

        sql = (
            f"UPDATE {p_table_name} SET\n{set_columns}\n" + f"WHERE {pk_conditions};\n"
        )

        file_path = path.join(self.DML, f"UPDATE_{p_table_name}.sql")
        FM.write_file(file_path, sql)

    def generate_delete_sql(self, p_table_name: str, p_constraints: dict):
        """
        Generate SQL DELETE code.
        - If more than one PK, then use AND logic in the WHERE clause
        :args:
        - p_table_name (str) Name of table to delete from
        - p_constraints (dict) Dict of constraints for the table
        :writes:
        - SQL file to [APP]/sql/DELETE_[p_table_name].sql
        @DEV:
        - Simplify if we go with "one PK column only" rule
        """
        pk_conditions = " AND ".join([f"{col}=?" for col in p_constraints["PK"]])
        sql = f"DELETE FROM {p_table_name}\nWHERE {pk_conditions};\n"
        file_path = path.join(self.DDL, f"DELETE_{p_table_name}.sql")
        FM.write_file(file_path, sql)

    def generate_sql(self, p_data_model: object):
        """
        Generate full set of SQL code from a data model.
        :args:
        - p_data_model: data model class object
        """
        constraints = {
            k: v
            for k, v in p_data_model.Constraints.__dict__.items()
            if not k.startswith("_")
        }
        table_name = p_data_model._tablename
        model = {
            k: v
            for k, v in p_data_model.__dict__.items()
            if not k.startswith("_")
            and k not in ("to_dict", "from_dict", "Constraints")
        }
        col_names = self.generate_create_sql(table_name, constraints, model)

        if "MAP" in table_name:
            print(f"\ngenerate_sql() for {table_name}")
            pp(("p_data_model:", p_data_model))
            pp(("p_data_model.__dict__:", p_data_model.__dict__))
            pp(("p_data_model.__init__:", p_data_model.__init__))
            pp(("p_data_model.__dict__.items():", p_data_model.__dict__.items()))
            pp(("p_data_model.__init__.items():", p_data_model.__init__.items()))
            pp(("constraints:", constraints))
            pp(("model: ", model))
            pp(("col_names: ", col_names))

        self.generate_drop_sql(table_name)
        self.generate_insert_sql(table_name, col_names)
        self.generate_select_all_sql(table_name, constraints, col_names)
        self.generate_select_pk_sql(table_name, constraints, col_names)
        self.generate_update_sql(table_name, constraints, col_names)
        self.generate_delete_sql(table_name, constraints)

    # DataBase Connections
    # ===========================================

    def __set_fk_pragma(self, p_foreign_keys_on: bool):
        """Set the foreign_keys pragma to ON or OFF
        FK's should be ignored when a table is dropped.
        This could potentially cause problems so keep an eye on it.
        As long as dropping, re-creating the entire DB, should be OK.
        :args:
        - p_foreign_keys_on (bool): If True, set foreign_keys to on
        """
        if p_foreign_keys_on is True:
            self.db_conn.execute("PRAGMA foreign_keys = ON;")
        else:
            self.db_conn.execute("PRAGMA foreign_keys = OFF;")

    def disconnect_db(self):
        """Close cursors and drop DB connection to self object."""
        if hasattr(self, "db_conn") and self.db_conn is not None:
            try:
                self.cur.close()
                self.db_conn.close()
            except RuntimeWarning:
                pass
        self.db_conn = None

    def connect_db(self, p_db_nm: str, p_foreign_keys_on: bool = True):
        """Open DB connection to SASKAN.db.
        Create a DB file at the specified location
          if one does not already exist.
        Set foreign key pragma ON by default.
        N.B. - If doing a DROP, set to OFF.
        :sets:
        - db_conn: the database connection
        - foreign_keys PRAGMA on or off
        - cur: cursor for the connection
        :args:
        - p_db_nm (str): Name of DB to connect to.
            This should always be "SASKAN.db", but I am making it a
            parameter in case I want to define another DB at some point.
            May eventually want to be able to read from the backup or
            archive databases too.
        - p_foreign_keys_on (bool): default True
        """
        self.disconnect_db()
        try:
            self.db_conn = sq3.connect(p_db_nm)
        except Exception as err:
            raise (err)
        self.__set_fk_pragma(p_foreign_keys_on)
        self.cur: sq3.Cursor = self.db_conn.cursor()

    # SQL Helpers
    # ===========================================
    def get_sql_file(self, p_sql_loc: str, p_sql_nm: str) -> str:
        """Read SQL from named file.
        :args:
        - p_sql_nm (str) Name of  SQL file in [APP]/sql
        :returns:
        - (str) Content of the SQL file
        """
        sql_nm = p_sql_nm.replace(".sql", "").replace(".SQL", "")
        sql_nm = sql_nm.upper() + ".sql"
        sql_path = path.join(p_sql_loc, sql_nm)
        SQL: str = FM.get_file(sql_path)
        if SQL == "":
            raise Exception(f"SQL file {sql_nm} is empty.")
        return SQL

    def get_db_columns(self, p_tbl_nm: str = "", p_sql_select: str = "") -> list:
        """For currently open connection and cursor, for the
        specified SQL SELECT file, return a list of the table's
        column names.
        :args:
        - p_tbl_nm (str) Optional. If provided, use this instead
          of scanning the SQL code.
        - p_sql_select (str) Optional.
            Text content of a well-structured SQL SELECT file,
            where table name is the last word in the
          first line. Use this if p_tbl_nm is not provided.
        :returns:
        - (list) of column names for the table
        """
        if p_tbl_nm in (None, ""):
            tbl_nm = p_sql_select.split("FROM ")[1].split()[0].rstrip(",;")
        else:
            tbl_nm = p_tbl_nm
        self.cur.execute(f"PRAGMA table_info({tbl_nm})")
        cols = self.cur.fetchall()
        col_nms = [c[1] for c in cols]
        return col_nms

    def set_dict_from_cursor(self, p_cols: list) -> OrderedDict:
        """
        Translate current cursor contents into a dict of lists
        :args:
        - p_cols (list) List of column names
        :return:
        - (OrderedDict )dict of lists, with column names as keys
          and in same order as listed in table-column order.
        """
        result = OrderedDict().fromkeys(p_cols)
        FETCH = self.cur.fetchall()  # list of tuples
        for row in FETCH:
            for i, col in enumerate(p_cols):
                if result[col] is None:
                    result[col] = list()
                result[col].append(row[i])
        return result

    # Executing Raw SQL
    # ===========================================
    def execute_sql(self, p_sql_code: str, p_foreign_keys_on: bool):
        """Run SQL passed in as a string.
        @DEV:
        - This is potentially a very dangerous call.
        - May want to do something like write a key to
          /tmp or /dev/shm, pass it in here so it can be verified.
        :args:
        - p_sql_nm (str): Name of external SQL file
        - p_foreign_keys_on (bool): Set foreign key pragma ON or OFF.
        """
        result = None
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        sql = p_sql_code.strip()
        if sql.upper().startswith("SELECT"):
            if (
                "DROP" in sql.upper()
                or "INSERT" in sql.upper()
                or "UPDATE" in sql.upper()
                or "DELETE" in sql.upper()
                or "PRAGMA" in sql.upper()
            ):
                raise Exception("SQL code refused.")
            else:
                self.cur.execute(sql)
                cols: list = self.get_db_columns(p_sql_select=sql)
                data: list = [r for r in self.cur.fetchall()]

                if len(data) == 0:
                    result: dict = {col: [] for col in cols}
                else:
                    result: dict = {
                        col: [row[i] for row in data] for i, col in enumerate(cols)
                    }
                self.disconnect_db()
        else:
            raise Exception("SQL code refused.")
        return result

    # Executing SQL Scripts
    # ===========================================
    def execute_select_all(self, p_table_nm: str) -> dict:
        """Run a SQL SELECT_ALL* script. No dynamic parameters.
           Return data as a dict of lists.
        :args:
        - p_table_nm (str): Name of SQL table
        :returns:
        - (dict) Dict of lists, {col_nms: [data values]}
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        sql: str = self.get_sql_file(self.DML, f"SELECT_ALL_{p_table_nm.upper()}")
        cols: list = self.get_db_columns(p_sql_select=sql)
        self.cur.execute(sql)
        data: list = [r for r in self.cur.fetchall()]
        if len(data) == 0:
            result: dict = {col: [] for col in cols}
        else:
            result: dict = {col: [row[i] for row in data] for i, col in enumerate(cols)}
        self.disconnect_db()
        return result

    def execute_select_by(self, p_sql_nm: str, p_pk_values: list) -> dict:
        """Run a SQL SELECT_BY script using parameters
           to select (by primary key).
           Return data as a dict of lists.
        :args:
        - p_sql_nm (str): Name of external SQL file
        - p_pk_values (list): Primary key values to match on.
            Must be listed in correct order.
        :returns:
        - (dict) Dict of lists, {col_nms: [data values]}
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        sql: str = self.get_sql_file(self.DML, p_sql_nm)
        cols: list = self.get_db_columns(p_sql_select=sql)
        self.cur.execute(sql, p_pk_values)
        data: list = [r for r in self.cur.fetchall()]
        if len(data) == 0:
            result: dict = {col: [] for col in cols}
        else:
            result: dict = {col: [row[i] for row in data] for i, col in enumerate(cols)}
        self.disconnect_db()
        return result

    def execute_ddl(self, p_sql_list: list, p_foreign_keys_on: bool):
        """Run one or more static SQL DROP or CREATE script.
        DELETEs have a separate method.
        N.B. - If DROP statements, set p_foreign_keys_on to False.
        - SQL names must be passed in as a list, even if just one script.
        - No dynamic parameters.
        - Executed as one transaction. If anything fails, all roll back.
        :args:
        - p_sql_nm (str): Name of external SQL file
        - p_foreign_keys_on (bool): Set foreign key pragma ON or OFF.
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on)
        try:
            self.cur.execute("BEGIN")
            for p_sql_nm in p_sql_list:
                sql = self.get_sql_file(self.DDL, p_sql_nm)
                self.cur.execute(sql)
            self.db_conn.commit()
        except sq3.Error as e:
            # Rollback the transaction if any operation fails
            self.db_conn.rollback()
            print("Rolled back.", e)
            print(f"Transaction failed on processing of:  {p_sql_nm}...")
            pp(("sql code: ", sql))
        finally:
            self.disconnect_db()

    def execute_insert(self, p_sql_nm: str, p_values: tuple):
        """Run a single SQL INSERT command which uses dynamic values,
           that is, assigned as parameters rather than hard-coded in script.
           Values are the column names in specified order.
           For now assume that:
            - Expect full list of values satisfying one row
            - caller knows what values to provide and in what order
        :args:
        - p_sql_nm (str): Name of external SQL file
        - p_values (tuple): n-tuple of values to insert
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        SQL = self.get_sql_file(self.DML, p_sql_nm)

        # print("\nDataBase: execute_insert")
        # print(f"SQL: {SQL}")
        # print(f"p_values: {p_values}")

        self.cur.execute(SQL, p_values)
        self.db_conn.commit()
        self.disconnect_db()

    def execute_update(self, p_sql_nm: str, p_key_val: str, p_values: tuple):
        """Run a SQL UPDATE file which uses dynamic values.
           Key value is the matching condition for WHERE clause (prim key).
           Values are the column names in specified order.
           For now I will assume that:
            - UPDATEs will always expect full list of values
            - caller knows what values to provide and in what order
        :args:
        - p_sql_nm (str): Name of external SQL file
        - p_key_val (str): Value of primary key to match on
        - p_values (tuple): n-tuple of values to update
        """
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        SQL = self.get_sql_file(self.DML, p_sql_nm)
        self.cur.execute(SQL, p_values + (p_key_val,))
        self.db_conn.commit()
        self.disconnect_db()

    def execute_delete(self, p_sql_nm: str, p_key_vals: list):
        """Run a SQL DELETE file which uses key values (primary key)
           for WHERE clause (prim key).
           For now I will assume that:
            - caller knows what values to provide and in what order
        :args:
        - p_sql_nm (str): Name of external SQL file
        - p_key_vals (list): Value of primary key(s) to match on

        @DEV:
        - There is not an equivalent in hofin::io_db, so need to
          review this. May need to tweak it to include setting
          p_foreign_keys_on to True.
        """
        if isinstance(p_key_vals, str):
            p_key_vals = [p_key_vals]
        self.connect_db(self.SASKAN_DB, p_foreign_keys_on=True)
        SQL = self.get_sql_file(self.DDL, p_sql_nm)
        self.cur.execute(SQL, p_key_vals)
        if self.db_conn is not None:
            self.db_conn.commit()
        self.disconnect_db()

    # Backup, Archive and Restore
    # ===========================================

    def backup_table_exists(self) -> bool:
        """Verify that the BACKUP table exists."""
        self.connect_db(self.SASKAN_DB)
        self.cur.execute(
            "SELECT name FROM sqlite_master " + "WHERE type='table' AND name='BACKUP'"
        )
        table_exists = self.cur.fetchone() is not None
        self.disconnect_db()
        return table_exists

    def backup_db(self, p_db: str, p_bak: str):
        """Copy specified main DB file to backup location.
        If the main database exists but BACKUP table not created
        yet then this will fail in the execute_insert() call.
        """
        if self.backup_table_exists():
            bkup_dttm = pendulum.now().format("YYYYMMDD_HHmmss")
            self.execute_insert(
                "INSERT_BACKUP",
                (
                    SM.get_uid(),
                    f"Backup {bkup_dttm}",
                    bkup_dttm,
                    "backup",
                    p_db,
                    p_bak,
                    "",
                ),
            )
        shutil.copyfile(p_db, p_bak)

    def archive_db(self, p_db: str):
        """Copy main main DB file to archive location."""
        arcv_dttm = pendulum.now().format("YYYYMMDD_HHmmss")
        arcv_nm = p_db.replace(".db", "_") + arcv_dttm + ".arcv"
        if self.backup_table_exists():
            self.execute_insert(
                "INSERT_BACKUP",
                (
                    SM.get_uid(),
                    f"Archive {arcv_dttm}",
                    arcv_dttm,
                    "archive",
                    p_db,
                    arcv_nm,
                    "",
                ),
            )
        shutil.copyfile(p_db, arcv_nm)

    def restore_db(self):
        """Copy backup DB file to main location.
        @DEV:
        - Pass name of backup and main files to use.
        """
        if self.backup_table_exists():
            bkup_dttm = pendulum.now().format("YYYYMMDD_HHmmss")
            self.execute_insert(
                "INSERT_BACKUP",
                (
                    SM.get_uid(),
                    f"Restore {bkup_dttm}",
                    bkup_dttm,
                    "restore",
                    self.DB_BKUP,
                    self.DB,
                    "",
                ),
            )
        shutil.copyfile(self.DB_BKUP, self.DB)
