"""

:module:    get_data.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401

from method_files import FileMethods
from database import DataBase

FM = FileMethods()


class GetData(object):
    """
    Provide methods for reading data from the database.
    Generic DB IO methods are in the io_db module.
    These methods are specifcally associated with data
    models defined in the data_model module. It may also be
    useful to either define views in SQLlite or to use
    this class to effectively create views.
    """
    def __init__(self):
        """
        Initialize a new instance of the GetData class.
        """
        pass

    def _get_by_value(self,
                      p_table_nm: str,
                      p_match: dict,
                      DB_CFG: dict):
        """
        Get data from the DB table by one or two specific values.
        :args:
        - p_table_nm: name of the table to query
        - p_match: dict of col-name:value pairs to match (max of 2)
        - DB_CFG: database configuration data
        :returns:
        - data: non-ordered dict of data from the table or None
        """
        def _get_one_value():
            data: dict = {}
            m_col = list(p_match.keys())[0]
            m_val = list(p_match.values())[0]
            if m_col in list(data_rows.keys()):
                for row_num, col_val in enumerate(data_rows[m_col]):
                    if col_val == m_val:
                        break
                for c_nm, c_val in data_rows.items():
                    data[c_nm] = c_val[row_num]
            return data

        def _get_two_values():
            data: dict = {}
            data_row_cnt = len(data_rows[list(data_rows.keys())[0]])
            m_col = list(p_match.keys())
            m_val = list(p_match.values())
            data_k = list(data_rows.keys())
            if m_col[0] in data_k and m_col[1] in data_k:
                for row_num in range(data_row_cnt):
                    if data_rows[m_col[0]][row_num] == m_val[0] \
                            and data_rows[m_col[1]][row_num] == m_val[1]:
                        break
                for c_nm, c_val in data_rows.items():
                    data[c_nm] = c_val[row_num]
            return data

        if FM.is_file_or_dir(DB_CFG['main_db']):
            DB = DataBase(DB_CFG)
            data_rows = DB.execute_select_all(p_table_nm)
            if len(p_match) == 1:
                data = _get_one_value()
            elif len(p_match) == 2:
                data = _get_two_values()
            else:
                data: None
                print("WARN: Can only match on 1 or 2 values.")
        return data

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
        """
        data = self._get_by_value('APP_CONFIG',
                                  {'version_id': DB_CFG['version']},
                                  DB_CFG)
        return data

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
        - db row: unordered dict of data that was requested else None
        """
        data = self._get_by_value('TEXTS',
                                  {'lang_code': p_lang_code,
                                   'text_name': p_text_name},
                                  DB_CFG)
        return data['text_value']
