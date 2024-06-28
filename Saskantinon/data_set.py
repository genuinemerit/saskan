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
from data_model_app import AppConfig, Frames, Texts

SM = ShellMethods()
FM = FileMethods()
AC = AppConfig()
FRM = Frames()
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
    Not much point to this class, but it's here for now.
    """
    def __init__(self):
        """
        Initialize a new instance of the GetData class.
        """
        pass

    def _prep_set(self,
                  MODEL: object,
                  DB_CFG: dict,
                  p_config_path: str = None) -> tuple:
        """
        Prep SQL and config templates for selected table.
        :args:
        - MODEL: object - instance of data model class
        - DB_CFG: dict of DB config values
        - p_config_path: full path to config file or None
        """
        DB = DataBase(DB_CFG)
        sql = f"INSERT_{MODEL._tablename}"
        config = FM.get_json_file(p_config_path) \
            if p_config_path is not None else None
        cols = OrderedDict(MODEL.to_dict()[MODEL._tablename])
        return (DB, sql, config, cols)

    def set_app_config(self,
                       DB_CFG: dict):
        """
        Set data on the AppConfig table using hard-coded values.
        Note: This will fail if the SQL file is not already in place.
        :args:
        - DB_CFG: dict of DB config values
        """
        DB, sql, config, cols =\
            self._prep_set(AC, DB_CFG)
        cols['config_uid_pk'] = SM.get_uid()
        cols['version_id'] = '0.1'
        cols['root_dir'] = "/home/dave/saskan"
        cols['mem_dir'] = "/dev/shm"
        cols['cfg_dir'] = "config"
        cols['dat_dir'] = "data"
        cols['html_dir'] = "web"
        cols['img_dir'] = "images"
        cols['snd_dir'] = "sounds"
        cols['py_dir'] = "python"
        cols['db_dir'] = "sql"
        cols['log_dir'] = "log"
        cols['mon_dir'] = "monitor"
        cols['dbg_dir'] = "debug"
        DB.execute_insert(sql, tuple(cols.values()))
        print("* APP_CONFIG record intialized.")

    def set_texts(self,
                  BOOT: dict,
                  DB_CFG: dict):
        """
        Get the config text file that matches the requested
        language. Use as input to populate TEXTS table.
        :args:
        - BOOT: dict of boot values
        - DB_CFG: dict of DB config values
        """
        config_p = path.join(BOOT['git_source'], 'config',
                             f"texts_{BOOT['language']}.json")
        DB, sql, config, cols =\
            self._prep_set(TX, DB_CFG, config_p)
        for tx_name, tx_value in config.items():
            cols['text_uid_pk'] = SM.get_uid()
            cols['lang_code'] = BOOT['language']
            cols['text_name'] = tx_name
            cols['text_value'] = tx_value
            DB.execute_insert(sql, tuple(cols.values()))
        print("* TEXTS table intialized.")

    def set_frames(self,
                   BOOT: dict,
                   DB_CFG: dict):
        """
        Get the schema file for frames. Generate FRAMES data.
        :args:
        - BOOT: dict of boot values
        - DB_CFG: dict of DB config values
        """
        config_p = path.join(BOOT['git_source'], 'config', "frames.json")
        DB, sql, config, cols =\
            self._prep_set(FRM, DB_CFG, config_p)
        for frame_id, v in config.items():
            cols['frame_uid_pk'] = SM.get_uid()
            cols['frame_id'] = frame_id
            cols['version_id'] = '0.1'
            cols['lang_code'] = BOOT['language']
            cols['frame_title'] = v['title']
            cols['frame_desc'] = v['desc']
            cols['size_w'] = v['size_w']
            cols['size_h'] = v['size_h']
            cols['ibar_x'] = v['ibar_x']
            cols['ibar_y'] = v['ibar_y']
            cols['pg_hdr_x'] = v['pg_hdr_x']
            cols['pg_hdr_y'] = v['pg_hdr_y']
            cols['pg_hdr_w'] = v['pg_hdr_w']
            cols['pg_hdr_h'] = v['pg_hdr_h']
            cols['pg_hdr_txt'] = v['pg_hdr_text']
            DB.execute_insert(sql, tuple(cols.values()))
        print("* FRAMES table intialized.")
