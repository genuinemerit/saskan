"""

:module:    data_get.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

from os import path
from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401

from data_base import DataBase
from method_files import FileMethods    # type: ignore
from method_shell import ShellMethods   # type: ignore

FM = FileMethods()
SM = ShellMethods()


class GetData(object):
    """
    Provide methods for reading data from the database.
    Generic DB IO methods are in the io_db module.
    These methods are specifcally associated with data
    models defined in the data_model* modules. It may be
    useful to either define views in SQLlite or to use
    this class to effectively create views.
    """
    def __init__(self):
        """
        Initialize a new instance of the GetData class.
        """
        pass

    def get_db_config(self):
        """
        Get the database configuration data.
        :returns:
        - DB_CFG: dict of database configuration data
        """
        DB_CFG = FM.get_json_file(path.join(
            SM.get_cwd_home(),
            "saskan/config/db_config.json"))
        return DB_CFG

    def _get_by_value(self,
                      p_table_nm: str,
                      p_match: dict,
                      DB_CFG: dict,
                      p_first_only: bool = True):
        """
        Get data from the DB table by one or two specific values.
        :args:
        - p_table_nm: name of the table to query
        - p_match: dict of col-name:value pairs to match (max of 2)
        - DB_CFG: database configuration data
        - p_first_only: return only the first row
        :returns:
        - data: non-ordered dict of data from the table or None
        """
        def _match_one_value():
            rows = []
            data: dict = {}
            m_col = list(p_match.keys())[0]
            m_val = list(p_match.values())[0]
            if m_col in list(data_rows.keys()):
                for row_num, col_val in\
                  enumerate(data_rows[m_col]):
                    if col_val == m_val:
                        for c_nm, c_val in data_rows.items():
                            data[c_nm] = c_val[row_num]
                        rows.append(data)
                        data: dict = {}
            return rows

        def _match_two_values():
            rows = []
            data: dict = {}
            data_row_cnt = len(data_rows[list(data_rows.keys())[0]])
            m_col = list(p_match.keys())
            m_val = list(p_match.values())
            data_k = list(data_rows.keys())
            if m_col[0] in data_k and m_col[1] in data_k:
                for row_num in range(data_row_cnt):
                    if data_rows[m_col[0]][row_num] == m_val[0] \
                            and data_rows[m_col[1]][row_num] == m_val[1]:
                        for c_nm, c_val in data_rows.items():
                            data[c_nm] = c_val[row_num]
                        rows.append(data)
                        data: dict = {}
            return rows

        from method_files import FileMethods
        FM = FileMethods()
        if FM.is_file_or_dir(DB_CFG['main_db']):
            DB = DataBase(DB_CFG)
            data_rows = DB.execute_select_all(p_table_nm)
            if len(p_match) == 1:
                rows = _match_one_value()
            elif len(p_match) == 2:
                rows = _match_two_values()
            else:
                rows: None
                print("WARN: Can only match on 1 or 2 values.")
        if p_first_only:
            rows = rows[0]
        return rows

    def get_app_config(self,
                       DB_CFG: dict):
        """
        Get data from the AppConfig table, filtering for
          record that contains desired version id. If DB
          does not exist, return None. Version ID is set
          in the DB config metadata.
        :args:
        - DB_CFG : dict of DB config data
        :returns:
        - db row: unordered dict of data that was requested else None
        @DEV:
        - Eventually mod this into a generic 'get_by_version' method.
        """
        row = self._get_by_value(
            'APP_CONFIG', {'version_id': DB_CFG['version']},
            DB_CFG)
        return row

    def get_text(self,
                 p_lang_code: str,
                 p_text_name: str,
                 DB_CFG: dict):
        """
        Get data from the Texts table, filtering for
          text name and language code.
        :args:
        - p_lang_code (str): language code
        - p_text_name (str): text name
        - DB_CFG : dict of DB config data
        :returns:
        - data: value of the 'text_value' column
        """
        row = self._get_by_value('TEXTS',
                                 {'lang_code': p_lang_code,
                                  'text_name': p_text_name},
                                 DB_CFG)
        return row['text_value']

    def get_by_id(self,
                  p_tbl_nm: str,
                  p_id_nm: str,
                  p_id_val: str,
                  DB_CFG: dict,
                  p_first_only: bool = True) -> dict:
        """
        Use this to retrieve all columns, rows from any table
        by matching on its `id` (as opposed to its `uid_pk`).
        @DEV:
        - May eventually have to deal with multiple rows returned.
        :args:
        - p_tbl_nm (str): table name
        - p_id_nm (str): name of id column
        - p_id_val (str): id value
        - DB_CFG : dict of DB config data
        - p_first_only (bool): return only the first row
        :returns:
        - data: unordered dict of all columns in the table
        """
        rows = self._get_by_value(p_tbl_nm,
                                  {p_id_nm: p_id_val},
                                  DB_CFG, p_first_only)
        return rows
