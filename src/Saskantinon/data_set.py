"""

:module:    data_set.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

from collections import OrderedDict
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

import data_model_app as DMA
import data_model_story as DMS
from data_base import DataBase
from data_get import GetData
from method_files import FileMethods
from method_shell import ShellMethods

GD = GetData()
SHM = ShellMethods()
FLM = FileMethods()

MAP_R = DMS.MapRect()
MAP_B = DMS.MapBox()
MAP_S = DMS.MapSphere()
MXM = DMS.MapXMap()
GRID = DMS.Grid()
GXM = DMS.GridXMap()


class SetData(object):
    """
    Provide methods for setting data in the database
    based on inputs.
    Until there is a front-end for editing Db content,
    this module will support:
    1. Hard-coded set-up methods (no inputs)
    2. Read inputs as call parameters
    3. Read from files <-- preferrred, JSON files in boot/config
    4. Read inputs from terminal
    """

    def __init__(self):
        """
        Initialize a new instance of the SetData class.
        """
        self.MAP_UID: dict = {}
        self.GRID_UID: dict = {}

    def _prep_set(self, DATA_MODEL: object, p_context: dict) -> tuple:
        """
        Prep SQL and config templates for selected table.
        :args:
        - MODEL: object - instance of a data model class
        - p_context: dict of static context values
        N.B. - config data for MENUS, MENU_BARS and MENU_ITEMS in menus.json
        :returns: ((tuple) DB class instance, INSERT SQL, table_data,
                           ordered dict of columns for selected model)
        """
        insert_sql = f"INSERT_{DATA_MODEL._tablename}"
        model_name = DATA_MODEL._tablename.lower()
        config_name = "menus" if "menu" in model_name else model_name
        config_path = p_context['cfg'][config_name]
        table_data = FLM.get_json_file(config_path)
        table_cols = OrderedDict(DATA_MODEL.to_dict()[DATA_MODEL._tablename])
        return (DataBase(p_context), insert_sql, table_data, table_cols)

    # App Scaffolding Tables

    def set_texts(self, p_context: dict):
        """
        Get the config text file that matches the requested
        language. Use as input to populate TEXTS table.
        N.B. - Texts are in (American) English by default.
        All items on the TEXTS table have a language-code and a
         generic "text_name" attribute.
        :args:
        - p_context: dict of context values
        """
        DB, sql, config, cols = self._prep_set(DMA.Texts(), p_context)
        for tx_name, tx_value in config.items():
            cols["text_uid_pk"] = SHM.get_uid()
            cols["lang_code"] = p_context["lang"]
            cols["text_name"] = tx_name
            cols["text_value"] = tx_value
            DB.execute_insert(sql, tuple(cols.values()))

    def set_frames(self, p_frame_id: str, p_context: dict):
        """
        Get config json for frames. Populate FRAMES table.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - p_context: dict of context values
        """
        DB, sql, config, cols = self._prep_set(DMA.Frames(), p_context)
        for frame_id, v in {f: v for f, v in config.items() if f == p_frame_id}.items():
            cols["frame_uid_pk"] = SHM.get_uid()
            cols["frame_id"] = frame_id
            cols["lang_code"] = p_context["lang"]
            cols["frame_title"] = v["title"]
            cols["frame_desc"] = v["desc"]
            cols["frame_w"] = v["frame_w"]
            cols["frame_h"] = v["frame_h"]
            cols["pg_hdr_x"] = v["pg_hdr_x"]
            cols["pg_hdr_y"] = v["pg_hdr_y"]
            cols["pg_hdr_w"] = v["pg_hdr_w"]
            cols["pg_hdr_h"] = v["pg_hdr_h"]
            cols["pg_hdr_txt"] = v["pg_hdr_text"]
            DB.execute_insert(sql, tuple(cols.values()))

    def set_menu_bars(self, p_frame_id: str, p_context: dict):
        """
        Get the data for menus. Populate MENU_BARS table.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - p_context: dict of context values
        Fail if FK to FRAMES is not found.
        """
        DB, sql, config, cols = self._prep_set(DMA.MenuBars(), p_context)
        for frame_id, v in {f: v for f, v in config.items() if f == p_frame_id}.items():
            cols["menu_bar_uid_pk"] = SHM.get_uid()

            data = GD.get_by_id("FRAMES", "frame_id", frame_id, DB)
            cols["frame_uid_fk"] = data["frame_uid_pk"]
            cols["frame_id"] = frame_id

            mb_v = v["menu_bar"]
            cols["mbar_margin"] = mb_v["margin"]
            cols["mbar_h"] = mb_v["h"]
            cols["mbar_x"] = mb_v["x"]
            cols["mbar_y"] = mb_v["y"]
            DB.execute_insert(sql, tuple(cols.values()))

    def set_menus(self, p_frame_id: str, p_context: dict):
        """
        Get the config file for menus. Generate MENUS data.
        N.B. - All menus are in American English by default.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - p_context: dict of context values
        Fail if FK to MENU_BARS is not found.
        """
        DB, sql, config, cols = self._prep_set(DMA.Menus(), p_context)
        for frame_id, v in {f: v for f, v in config.items() if f == p_frame_id}.items():

            data = GD.get_by_id("MENU_BARS", "frame_id", frame_id, DB)
            cols["menu_bar_uid_fk"] = data["menu_bar_uid_pk"]
            cols["lang_code"] = p_context["lang"]
            cols["frame_id"] = frame_id

            for mnu_id, val in v["menus"].items():
                cols["menu_uid_pk"] = SHM.get_uid()
                cols["menu_id"] = mnu_id
                cols["menu_name"] = val["name"]
                DB.execute_insert(sql, tuple(cols.values()))

    def set_menu_items(self, p_frame_id: str, p_context: dict):
        """
        Get the config file for menu items.
        Generate MENU_ITEMS data.
        N.B. - All menus items are in American English by default.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - p_context: dict of context values
        Fail if FK to MENUS is not found.
        """
        DB, sql, config, cols = self._prep_set(DMA.MenuItems(), p_context)
        for frame_id, v in {f: v for f, v in config.items() if f == p_frame_id}.items():
            for mnu_id, val in v["menus"].items():
                data = GD.get_by_id("MENUS", "menu_id", mnu_id, DB)
                cols["menu_uid_fk"] = data["menu_uid_pk"]
                cols["lang_code"] = p_context["lang"]
                cols["frame_id"] = frame_id
                order = 0
                for mnu_itm_id, mi_v in val["items"].items():
                    cols["item_uid_pk"] = SHM.get_uid()
                    cols["item_id"] = mnu_itm_id
                    cols["item_order"] = order
                    cols["item_name"] = mi_v["name"]
                    cols["key_binding"] = mi_v["key_b"]
                    cols["help_text"] = mi_v["help_text"] if "help_text" in mi_v else ""
                    cols["enabled_default"] = (
                        mi_v["enabled"] if "enabled" in mi_v else True
                    )
                    order += 1
                    DB.execute_insert(sql, tuple(cols.values()))

    def set_windows(self, p_frame_id: str, p_context: dict):
        """
        Get the config file for windows. Generate WINDOWS data.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - p_context: dict of context values
        Fail if FK to FRAMES is not found.
        """
        DB, sql, config, cols = self._prep_set(DMA.Windows(), p_context)
        for frame_id, v in {f: v for f, v in config.items() if f == p_frame_id}.items():
            data = GD.get_by_id("FRAMES", "frame_id", frame_id, DB)
            cols["frame_uid_fk"] = data["frame_uid_pk"]
            cols["frame_id"] = frame_id
            for win_id, val in v.items():
                cols["win_uid_pk"] = SHM.get_uid()
                cols["lang_code"] = p_context["lang"]
                cols["win_id"] = win_id
                cols["win_title"] = val["title"]
                cols["win_margin"] = val["margin"]
                DB.execute_insert(sql, tuple(cols.values()))

    def set_links(self, p_frame_id: str, p_context: dict):
        """
        Get the config file for links. Generate LINKS data.
        :args:
        - p_frame_id: str - name of app, e.g. 'saskan' or 'admin'
        - p_context: dict of context values
        """
        DB, sql, config, cols = self._prep_set(DMA.Links(), p_context)
        for frame_id, v in {f: v for f, v in config.items() if f == p_frame_id}.items():
            cols["frame_id"] = frame_id
            cols["lang_code"] = p_context["lang"]
            for lnk_id, val in v["links"].items():
                cols["link_uid_pk"] = SHM.get_uid()
                cols["link_id"] = lnk_id
                cols["link_protocol"] = val["protocol"]
                cols["mime_type"] = val["mime_type"]
                cols["link_name"] = val["name"]
                # Make this a generic function if it gets repeated
                if "%" in val["value"]:
                    cfg = val["value"].split("%")[1]
                    cols["link_value"] = p_context[cfg]
                else:
                    cols["link_value"] = val["value"]
                cols["link_icon"] = val["icon"]
                DB.execute_insert(sql, tuple(cols.values()))

    # Story-related Tables

    def set_maps(self, DB_CFG: dict):
        """Define a variety of maps for game use."""
        DB, sql, config, cols = self._prep_set(DMS._Map(), DB_CFG)
        cols["map_uid_pk"] = SHM.get_uid()
        cols["version_id"] = "0.1"
        cols["map_name"] = "Saskan Lands Regions"
        cols["map_type"] = "political"
        cols["unit_of_measure"] = "KM"
        cols["origin_2d_lat"] = 39.7392
        cols["origin_2d_lon"] = -104.9902
        cols["width_e_w_2d"] = 1800.0
        cols["height_n_s_2d"] = 1350.0
        cols["avg_alt_m"] = 452.0
        cols["min_alt_m"] = 1.0
        cols["max_alt_m"] = 2875.0
        cols["origin_3d_x"] = 0
        cols["origin_3d_y"] = 0
        cols["origin_3d_z"] = 0
        cols["width_3d"] = 0
        cols["height_3d"] = 0
        cols["depth_3d"] = 0
        DB.execute_insert(sql, tuple(cols.values()))
        self.MAP_UID[cols["map_name"]] = cols["map_uid_pk"]
        print("* MAP records initialized.")

    def set_grids(self, DB_CFG: dict):
        """Define a variety of grids for game use.
        Identify Map association/s for each grid.
        """
        DB, sql, config, cols = self._prep_set(GRID, DB_CFG)
        cols["grid_uid_pk"] = SHM.get_uid()
        cols["version_id"] = "0.1"
        cols["grid_name"] = "30r_40c"
        cols["row_cnt"] = 30
        cols["col_cnt"] = 40
        cols["z_up_cnt"] = 0
        cols["z_down_cnt"] = 0
        DB.execute_insert(sql, tuple(cols.values()))
        self.GRID_UID[cols["grid_name"]] = cols["grid_uid_pk"]

        DB, sql, config, cols = self._prep_set(GXM, DB_CFG)
        cols["grid_x_map_uid_pk"] = SHM.get_uid()
        cols["grid_uid_fk"] = self.GRID_UID["30r_40c"]
        cols["map_uid_fk"] = self.MAP_UID["Saskan Lands Regions"]
        DB.execute_insert(sql, tuple(cols.values()))
        print("* GRID and GRID_X_MAP records initialized.")
