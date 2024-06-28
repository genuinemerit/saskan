"""

:module:    data_set.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

from os import path
from collections import OrderedDict
from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401

from method_shell import ShellMethods
from method_files import FileMethods
from data_base import DataBase
from data_model import AppConfig, Texts

SM = ShellMethods()
FM = FileMethods()
AC = AppConfig()
TX = Texts()


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
                       DB_CFG: dict):
        """
        Set data on the AppConfig table using hard-coded values.
        Note: This will fail if the SQL file is not already in place.
        :args:
        - DB_CFG: dict of DB config values
        """
        DB = DataBase(DB_CFG)
        sql = 'INSERT_APP_CONFIG'
        data = OrderedDict(AC.to_dict()['APP_CONFIG'])
        data['config_uid_pk'] = SM.get_uid()
        data['version_id'] = '0.1'
        data['root_dir'] = "/home/dave/saskan"
        data['mem_dir'] = "/dev/shm"
        data['cfg_dir'] = "config"
        data['dat_dir'] = "data"
        data['html_dir'] = "web"
        data['img_dir'] = "images"
        data['snd_dir'] = "sounds"
        data['py_dir'] = "python"
        data['db_dir'] = "sql"
        data['log_dir'] = "log"
        data['mon_dir'] = "monitor"
        data['dbg_dir'] = "debug"
        DB.execute_insert(sql, tuple(data.values()))
        print("* APP_CONFIG record intialized.")

    def set_texts(self,
                  BOOT: dict,
                  DB_CFG: dict):
        """
        Get the config text file that matches the requested
        language. Use as input to populate TEXTS table.
        :args:
        - BOOT: dict of boot values
        """
        DB = DataBase(DB_CFG)
        sql = 'INSERT_TEXTS'
        texts_j = path.join(BOOT['git_source'], 'config',
                            f"t_texts_{BOOT['language']}.json")
        texts = FM.get_json_file(texts_j)
        data = OrderedDict(TX.to_dict()['TEXTS'])
        for tx_name, tx_value in texts.items():
            data['text_uid_pk'] = SM.get_uid()
            data['lang_code'] = BOOT['language']
            data['text_name'] = tx_name
            data['text_value'] = tx_value
            DB.execute_insert(sql, tuple(data.values()))
        print(f"* TEXTS table intialized for <{BOOT['language']}>")
