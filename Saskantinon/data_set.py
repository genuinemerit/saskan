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
from data_get import GetData
from data_model_app import AppConfig, Frames, Texts
from data_model_app import MenuBars, Menus, MenuItems
from data_model_app import Windows, Links

GD = GetData()
SHM = ShellMethods()
FLM = FileMethods()
APC = AppConfig()
TXT = Texts()
FRM = Frames()
MNB = MenuBars()
MNU = Menus()
MNI = MenuItems()
WIN = Windows()
LNK = Links()


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
        config = FLM.get_json_file(p_config_path) \
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
            self._prep_set(APC, DB_CFG)
        cols['config_uid_pk'] = SHM.get_uid()
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
        print("* APP_CONFIG record initialized.")

    def get_config_path(self,
                        BOOT: object,
                        p_config_nm: str):
        """Return path to specified config file.
        """
        return (path.join(BOOT['git_source'], 'config',
                          f"{p_config_nm}.json"))

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
        config_p = self.get_config_path(
            BOOT, f"texts_{BOOT['language']}")
        DB, sql, config, cols =\
            self._prep_set(TXT, DB_CFG, config_p)
        for tx_name, tx_value in config.items():
            cols['text_uid_pk'] = SHM.get_uid()
            cols['lang_code'] = BOOT['language']
            cols['text_name'] = tx_name
            cols['text_value'] = tx_value
            DB.execute_insert(sql, tuple(cols.values()))
        print("* TEXTS table initialized.")

    def set_frames(self,
                   p_frame_id: str,
                   BOOT: dict,
                   DB_CFG: dict):
        """
        Get the schema file for frames. Generate FRAMES data.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - BOOT: dict of boot values
        - DB_CFG: dict of DB config values
        """
        config_p = self.get_config_path(BOOT, "frames")
        DB, sql, config, cols =\
            self._prep_set(FRM, DB_CFG, config_p)
        for frame_id, v in {f: v for f, v in config.items()
                            if f == p_frame_id}.items():
            cols['frame_uid_pk'] = SHM.get_uid()
            cols['frame_id'] = frame_id
            cols['version_id'] = BOOT['db_version']
            cols['lang_code'] = BOOT['language']
            cols['frame_title'] = v['title']
            cols['frame_desc'] = v['desc']
            cols['frame_w'] = v['frame_w']
            cols['frame_h'] = v['frame_h']
            cols['ibar_x'] = v['ibar_x']
            cols['ibar_y'] = v['ibar_y']
            cols['pg_hdr_x'] = v['pg_hdr_x']
            cols['pg_hdr_y'] = v['pg_hdr_y']
            cols['pg_hdr_w'] = v['pg_hdr_w']
            cols['pg_hdr_h'] = v['pg_hdr_h']
            cols['pg_hdr_txt'] = v['pg_hdr_text']
            DB.execute_insert(sql, tuple(cols.values()))
        print(f"* FRAMES table initialized for {p_frame_id}.")

    def set_menu_bars(self,
                      p_frame_id: str,
                      BOOT: dict,
                      DB_CFG: dict):
        """
        Get the config file for menus. Generate MENU_BARS data.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - BOOT: dict of boot values
        - DB_CFG: dict of DB config values
        Should fail if FK to FRAMES is not found..
        """
        config_p = self.get_config_path(BOOT, "menus")
        DB, sql, config, cols =\
            self._prep_set(MNB, DB_CFG, config_p)
        for frame_id, v in {f: v for f, v in config.items()
                            if f == p_frame_id}.items():
            cols['menu_bar_uid_pk'] = SHM.get_uid()

            data = GD.get_by_id('FRAMES', 'frame_id',
                                frame_id, DB_CFG)
            cols['frame_uid_fk'] = data['frame_uid_pk']
            cols['lang_code'] = data['lang_code']
            cols['version_id'] = BOOT['db_version']
            cols['frame_id'] = frame_id

            mb_v = v["menu_bar"]
            cols['mbar_margin'] = mb_v['margin']
            cols['mbar_h'] = mb_v['h']
            cols['mbar_x'] = mb_v['x']
            cols['mbar_y'] = mb_v['y']
            DB.execute_insert(sql, tuple(cols.values()))
        print(f"* MENU_BARS table initialized for {p_frame_id}.")

    def set_menus(self,
                  p_frame_id: str,
                  BOOT: dict,
                  DB_CFG: dict):
        """
        Get the config file for menus. Generate MENUS data.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - BOOT: dict of boot values
        - DB_CFG: dict of DB config values
        Should fail if FK to MENU_BARS is not found.
        """
        config_p = self.get_config_path(BOOT, "menus")
        DB, sql, config, cols =\
            self._prep_set(MNU, DB_CFG, config_p)
        for frame_id, v in {f: v for f, v in config.items()
                            if f == p_frame_id}.items():

            data = GD.get_by_id("MENU_BARS", 'frame_id',
                                frame_id, DB_CFG)
            cols['menu_bar_uid_fk'] = data['menu_bar_uid_pk']
            cols['lang_code'] = data['lang_code']
            cols['version_id'] = BOOT['db_version']
            cols['frame_id'] = frame_id

            for mnu_id, val in v["menus"].items():
                cols['menu_uid_pk'] = SHM.get_uid()
                cols['menu_id'] = mnu_id
                cols['menu_name'] = val['name']
                DB.execute_insert(sql, tuple(cols.values()))
        print(f"* MENUS table initialized for {p_frame_id}.")

    def set_menu_items(self,
                       p_frame_id: str,
                       BOOT: dict,
                       DB_CFG: dict):
        """
        Get the config file for menu items.
        Generate MENU_ITEMS data.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - BOOT: dict of boot values
        - DB_CFG: dict of DB config values
        Should fail if FK to MENUS is not found.
        """
        config_p = self.get_config_path(BOOT, "menus")
        DB, sql, config, cols =\
            self._prep_set(MNI, DB_CFG, config_p)
        for frame_id, v in {f: v for f, v in config.items()
                            if f == p_frame_id}.items():
            for mnu_id, val in v["menus"].items():
                data = GD.get_by_id("MENUS", 'menu_id',
                                    mnu_id, DB_CFG)
                cols['menu_uid_fk'] = data['menu_uid_pk']
                cols['lang_code'] = data['lang_code']
                cols['version_id'] = BOOT['db_version']
                cols['frame_id'] = frame_id
                order = 0
                for mnu_itm_id, mi_v in val["items"].items():
                    cols['item_uid_pk'] = SHM.get_uid()
                    cols['item_id'] = mnu_itm_id
                    cols['item_order'] = order
                    cols['item_name'] = mi_v['name']
                    cols['key_binding'] = mi_v['key_b']
                    cols['help_text'] = mi_v['help_text']\
                        if 'help_text' in mi_v else ""
                    cols['enabled_default'] = mi_v['enabled']\
                        if 'enabled' in mi_v else True
                    order += 1
                    DB.execute_insert(sql, tuple(cols.values()))
        print(f"* MENU_ITEMS table initialized for {p_frame_id}.")

    def set_windows(self,
                    p_frame_id: str,
                    BOOT: dict,
                    DB_CFG: dict):
        """
        Get the config file for windows. Generate WINDOWS data.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - BOOT: dict of boot values
        - DB_CFG: dict of DB config values
        Should fail if FK to MENUS is not found.
        """
        config_p = self.get_config_path(BOOT, "windows")
        DB, sql, config, cols =\
            self._prep_set(WIN, DB_CFG, config_p)
        for frame_id, v in {f: v for f, v in config.items()
                            if f == p_frame_id}.items():
            data = GD.get_by_id("FRAMES", 'frame_id',
                                frame_id, DB_CFG)
            cols['frame_uid_fk'] = data['frame_uid_pk']
            cols['frame_id'] = frame_id
            cols['version_id'] = BOOT['db_version']
            for win_id, val in v.items():
                cols['win_uid_pk'] = SHM.get_uid()
                cols['lang_code'] = val['lang_code']
                cols['win_id'] = win_id
                cols['win_title'] = val['title']
                cols['win_x'] = val['x']
                cols['win_y'] = val['y']
                cols['win_h'] = val['h']
                cols['win_w'] = val['w']
                cols['win_margin'] = val['margin']
                DB.execute_insert(sql, tuple(cols.values()))
        print(f"* WINDOWS table initialized for {p_frame_id}.")

    def set_links(self,
                  p_frame_id: str,
                  BOOT: dict,
                  DB_CFG: dict):
        """
        Get the config file for links. Generate LINKS data.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - BOOT: dict of boot values
        - DB_CFG: dict of DB config values
        """
        config_p = self.get_config_path(BOOT, "links")
        DB, sql, config, cols =\
            self._prep_set(LNK, DB_CFG, config_p)
        for frame_id, v in {f: v for f, v in config.items()
                            if f == p_frame_id}.items():
            cols["frame_id"] = frame_id
            cols["version_id"] = "0.1"
            cols["lang_code"] = v["lang_code"]
            for lnk_id, val in v["links"].items():
                cols['link_uid_pk'] = SHM.get_uid()
                cols['link_id'] = lnk_id
                cols['link_protocol'] = val['protocol']
                cols['mime_type'] = val['mime_type']
                cols['link_name'] = val['name']
                cols['link_value'] = val['value']
                cols['link_icon'] = val['icon']
                DB.execute_insert(sql, tuple(cols.values()))
        print("* LINKS table initialized.")
