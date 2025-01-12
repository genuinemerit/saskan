"""

:module:    data_get.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

from method_files import FileMethods
from data_base import DataBase
from data_structs import Colors as DSC
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

FM = FileMethods()


class GetData:
    """
    Provide bespoke methods for reading data from the database.
    Generic DB IO methods are in the data_base module.
    """

    def __init__(self):
        """
        Initialize a new instance of the GetData class.
        """
        self.CONTEXT = FM.get_json_file("static/context/context.json")
        self.USERDATA = FM.get_json_file("static/context/userdata.json")
        self.DB = DataBase(self.CONTEXT)

    def _get_by_value(
        self, p_table_nm: str, p_match: dict, DB: object, p_first_only: bool = True
    ):
        """
        "PRIVATE" method to get data from the DB table by selecting on one or two values.

        Get data from the DB table by selecting on one or two values.
        For example, if matching on uid_pk, just pass the one value.
        In cases where more than one record might be matched, default is to
          return only the first one. If multiple records are expected, then
          set p_first_only to False.
        :args:
        - p_table_nm: name of the table to query
        - p_match: dict of col-name:value pairs to match (max of 2)
        - DB: instance of DataBase() class
        - p_first_only: return only the first row that matches
        :returns:
        - rows: list of non-ordered dicts of data from the table, or [],
          or just one non-ordered dict if p_first_only is True
        """

    def get_by_match(self, p_table_nm: str, p_match: dict, p_first_only: bool = True):
        """
        Get data from a DB table by selecting on one, two or three columns.
        The most common scenarios are:
        - Match on one column: p_match = {"col_name": value}, returning n rows.
        - Match on two columns: p_match = {"col1": val1, "col2": val2}, usually a natural
           key like an ID field, plus a blank value for delete_dt, returning one row.
        - Match on three columns: p_match = {"col1": val1, "col2": val2, "col3": val3},
            returning one row. Typically used for a natural key plus a lang-code and a
            blank value for delete_dt.
        :param p_table_nm: Name of the table to query
        :param p_match: Dict of col-name:value pairs to match on. Max of 3.
        :param p_first_only: Return only the first row that matches
        :return: List of non-ordered dicts of data from the table, or [], if no match
                 found or p_first_only is False; or one non-ordered dict if p_first_only is True
        @DEV:
        - This logic will probably work for any number of matching columns, but let's keep
          it contained to 3 for now.
        """

        def _match_values(data_rows, match_cols, match_vals):
            rows = []
            for row_num in range(len(data_rows[match_cols[0]])):
                if all(
                    data_rows[col][row_num] == val
                    for col, val in zip(match_cols, match_vals)
                ):
                    row = {c_nm: c_val[row_num] for c_nm, c_val in data_rows.items()}
                    rows.append(row)
            return rows

        data_rows = self.DB.execute_select_all_clean(p_table_nm)
        match_cols, match_vals = list(p_match.keys()), list(p_match.values())

        if len(match_cols) not in [1, 2, 3]:
            print(f"{DSC.CL_YELLOW}WARN{DSC.CL_END}: Can only match on 1, 2 or 3 values.")
            return []

        data = _match_values(data_rows, match_cols, match_vals)
        return data[0] if p_first_only and data else data

    def get_text(self, p_lang_code: str, p_text_id: str, DB_CFG: dict) -> str:
        """
        Specialized method to get text data from the TEXT_DATA table.
        :param p_lang_code: Language code
        :param p_text_id: Text name
        :param DB_CFG: Dict of DB config data
        :return: value of the 'text_value' column
        """
        row = self.get_by_match(
            "TEXT_DATA", {"lang_code": p_lang_code, "text_id": p_text_id}
        )
        return str(row["text_value"]) if row else ""

    def get_check_constraints(self, param_val: str):
        """
        Get CONSTRAINTs for a table column
        :param param_val: table_name:column_name
        """
        table_name, col_name = param_val.split(":")
        return self.DB.get_check_constraint_values(table_name.upper(), col_name.lower())
