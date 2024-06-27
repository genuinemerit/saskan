"""

:module:    io_set_get_data.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
I expect this module to be called only by io_file methods.
It will provide methods for setting and getting data on
the database, but the distinction between DB and files should
not be a concern to higher level modules.
"""

# import json
# import pendulum     # date and time
# import random
# import string

from os import path
from collections import OrderedDict
# from pathlib import Path
from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401
# from typing import Tuple, Union

from io_shell import ShellIO
from io_db import DataBase

# re: io_data:
# For data models, import specific ones
# per need. For example, when setting or getting
# records relating to config data, import the
# io_data classes like AppConfig, Texts, Frames
# and so on
# When reading data from the DB, there are two
# layers to consider:
# 1. Pull records in and filtering them; this is
#    done using io_db and io_data classes.
# 2. Translate into object formats when needed
#    to be used in the app; in this case, will
#    import io_data classes like GamePlane and Struct

SI = ShellIO()


class ComputeData(object):
    """
    Provide methods for setting data as the result of
    calculations, algorithms or AI calls.
    """
    def __init__(self):
        """
        Initialize a new instance of the ComputeData class.
        """
        pass


class SetData(object):
    """
    Provide methods for setting data in the database
    based on inputs.
    Until there is a front-end for editing Db content,
    this module will support:
    1. Hard-coded set-up methods (no inputs)
    2. Read inputs as call parameters
    3. Read from files
    4. Read inputs from terminal
    """
    def __init__(self):
        """
        Initialize a new instance of the GetData class.
        """
        pass

    def set_app_config(self,
                       FI: object):
        """
        Set data on the AppConfig table using hard-coded values.
        Note: This will fail if the SQL file is not already in place.
        :args:
        - FI: current instance of FileIO
        """
        DB = DataBase(FI.DB_CFG)
        sql = 'INSERT_APP_CONFIG'
        from io_data import AppConfig
        AC = AppConfig()
        data = OrderedDict(AC.to_dict()['APP_CONFIG'])
        data['config_uid_pk'] = SI.get_uid()
        data['version_id'] = '0.1'
        data['root_dir'] = "/home/dave/saskan"
        data['bin_dir'] = "/usr/local/bin"
        data['mem_dir'] = "/dev/shm"
        data['cfg_dir'] = "config"
        data['dat_dir'] = "data"
        data['img_dir'] = "images"
        data['py_dir'] = "python"
        data['db_dir'] = "sql"
        data['sch_dir'] = "schema"
        data['log_dat'] = "saskan_log"
        data['mon_dat'] = "saskan_mon"
        data['dbg_dat'] = "saskan_dbg"
        DB.execute_insert(sql, tuple(data.values()))
        print("* APP_CONFIG record intialized.")

    def set_texts(self,
                  FI: object,):
        """
        Get the config text file that matches the requested
        language. Use as input to populate TEXTS table.
        :args:
        - FI: current instance of FileIO
        """
        DB = DataBase(FI.DB_CFG)
        sql = 'INSERT_TEXTS'
        texts_j = path.join(FI.BOOT['git_source'], 'config',
                            f"t_texts_{FI.BOOT['language']}.json")
        texts = FI.get_json_file(texts_j)
        from io_data import Texts
        TX = Texts()
        data = OrderedDict(TX.to_dict()['TEXTS'])
        for tx_name, tx_value in texts.items():
            data['text_uid_pk'] = SI.get_uid()
            data['lang_code'] = FI.BOOT['language']
            data['text_name'] = tx_name
            data['text_value'] = tx_value
            DB.execute_insert(sql, tuple(data.values()))
        print(f"* TEXTS table intialized for <{FI.BOOT['language']}>")


class GetData(object):
    """
    Provide methods for reading data from the database.
    Generic DB IO methods are in the io_db module.
    These methods are specifcally associated with data
    models defined in the io_data module. It may also be
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
                      FI: object):
        """
        Get data from the DB table by one or two specific values.
        :args:
        - p_table_nm: name of the table to query
        - p_match: dict of col-name:value pairs to match (max of 2)
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

        if FI.is_file_or_dir(FI.DB_CFG['main_db']):
            DB = DataBase(FI.DB_CFG)
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
                       FI: object):
        """
        Get data from the AppConfig table, filtering for
          record that contains desired version id. If DB
          does not exist, return None. Version ID is set
          in the DB config metadata.
        :args:
        - FI : object: current FileIO instance
        :returns:
        - db row: unordered dict of data that was requested else None
        """
        data = self._get_by_value('APP_CONFIG',
                                  {'version_id': FI.DB_CFG['version']},
                                  FI)
        return data

    def get_text(self,
                 p_lang_code: str,
                 p_text_name: str,
                 FI: object):
        """
        Get data from the Texts table, filtering for
          text name and language code.
        :args:
        - p_lang_code (str): language code
        - p_text_name (str): text name
        - FI : object: current FileIO instance
        :returns:
        - db row: unordered dict of data that was requested else None
        """
        data = self._get_by_value('TEXTS',
                                  {'lang_code': p_lang_code,
                                   'text_name': p_text_name},
                                  FI)
        return data['text_value']
