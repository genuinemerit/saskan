"""

:module:    data_set.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""
import random
import secrets

from collections import OrderedDict
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

import data_model_app as DMA
import data_model_story as DMS
from data_base import DataBase
from data_get import GetData
from data_structs import EntityType
from method_files import FileMethods
from method_shell import ShellMethods

GD = GetData()
SHM = ShellMethods()
FLM = FileMethods()


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
        config_path = p_context['cfg'][config_name] if config_name in p_context['cfg'] else ""
        table_data = FLM.get_json_file(config_path) if config_path else {}
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

    def set_rect_maps(self, p_context: dict):
        """Define a rectangular map for game use.
        :args:
        - p_context: dict of context values"""
        DB, sql, _, cols = self._prep_set(DMS.MapRect(), p_context)
        cols["map_rect_uid_pk"] = SHM.get_uid()
        cols["map_shape"] = "rectangle"
        cols["map_type"] = "political"
        cols["map_name"] = "Saskan Lands Political Regions"
        cols["map_desc"] = "Borders and names of the regions and provinces of Saskantinon."
        cols["north_lat"] = 39.7392
        cols["west_lon"] = -104.9902
        cols["south_lat"] = 23.5696
        cols["east_lon"] = -86.335
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))

    def set_box_maps(self, p_context: dict):
        """Define a box map for game use.
        :args:
        - p_context: dict of context values"""
        DB, sql, _, cols = self._prep_set(DMS.MapBox(), p_context)
        cols["map_box_uid_pk"] = SHM.get_uid()
        cols["map_shape"] = "box"
        cols["map_type"] = "geo"
        cols["map_name"] = "Saskan Lands Geography"
        cols["map_desc"] = "Elevation, mountains, hills, lakes, rivers, and streams."
        cols["north_lat"] = 39.7392
        cols["west_lon"] = -104.9902
        cols["south_lat"] = 23.5696
        cols["east_lon"] = -86.335
        cols["up_m"] = 4400.0
        cols["down_m"] = 4300.0
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))

    def set_sphere_maps(self, p_context: dict):
        """Define a box map for game use.
        :args:
        - p_context: dict of context values"""
        DB, sql, _, cols = self._prep_set(DMS.MapSphere(), p_context)
        cols["map_sphere_uid_pk"] = SHM.get_uid()
        cols["map_shape"] = "sphere"
        cols["map_type"] = "geo"
        cols["map_name"] = "Gavor-Havorra Planetary Map"
        cols["map_desc"] = "Continets, oceans, and land masses of Gavor-Havorra."
        cols["origin_lat"] = 0.0
        cols["origin_lon"] = 0.0
        cols["z_value"] = 0.0
        cols["unit_of_measure"] = "KM"
        cols["sphere_radius"] = 6371.0
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))

    def set_grids(self, p_context: dict):
        """Define a Grids for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_set(DMS.Grid(), p_context)
        cols["grid_uid_pk"] = SHM.get_uid()
        cols["grid_name"] = "30x_40y_30zu_30zd"
        cols["x_col_cnt"] = 30
        cols["y_row_cnt"] = 40
        cols["z_up_cnt"] = 30
        cols["z_down_cnt"] = 30
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))
        self.GRID_UID[cols["grid_name"]] = cols["grid_uid_pk"]

    def set_grid_cells(self, p_context: dict):
        """Define a set of Grid Cells for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_set(DMS.GridCell(), p_context)
        # Read records to get UID for GRID instead of storing them
        for grid_name in self.GRID_UID:
            grid = GD.get_by_id("GRID", "grid_uid_pk", self.GRID_UID[grid_name], DB)
            for n in range(1, 11):
                cols["grid_cell_uid_pk"] = SHM.get_uid()
                cols["grid_uid_fk"] = grid["grid_uid_pk"]
                cols["grid_cell_name"] = f"Test Cell {n}"
                cols["x_col_ix"] = random.randint(0, grid["x_col_cnt"] - 1)
                cols["y_row_ix"] = random.randint(0, grid["y_row_cnt"] - 1)
                cols["z_up_down_ix"] = random.randint((grid["z_down_cnt"] - 1) * -1,
                                                      grid["z_up_cnt"] - 1)
                cols["grid_cell_id"] = (f"{cols['x_col_ix']}x_" +
                                        f"{cols['y_row_ix']}y_" +
                                        f"{cols['z_up_down_ix']}z")
                cols["delete_dt"] = ""
                DB.execute_insert(sql, tuple(cols.values()))

    def set_grid_infos(self, p_context: dict):
        """Define a set of Grid Info records for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_set(DMS.GridInfo(), p_context)
        cells = DB.execute_select_all("GRID_CELL")
        for n in range(0, len(cells["grid_cell_uid_pk"])):
            cols["grid_info_uid_pk"] = SHM.get_uid()
            cols["grid_cell_uid_fk"] = cells["grid_cell_uid_pk"][n]
            cols["grid_info_id"] = f"Test Info ID {n}"
            cols["grid_info_data_type"] = random.choice(EntityType.DATA_TYPE)
            cols["grid_info_name"] = f"Test Info Name {n}"
            cols["grid_info_value"] = random.randint(1, 1000)\
                if cols["grid_info_data_type"] in ("INT", "FLOAT")\
                else secrets.token_bytes(10)
            cols["delete_dt"] = ""
            DB.execute_insert(sql, tuple(cols.values()))

    def set_map_x_maps(self, p_context: dict):
        """Define a set of Map_x_Map records for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_set(DMS.MapXMap(), p_context)
        rects = DB.execute_select_all("MAP_RECT")
        boxes = DB.execute_select_all("MAP_BOX")
        spheres = DB.execute_select_all("MAP_SPHERE")
        for r in range(0, len(rects["map_rect_uid_pk"])):
            for b in range(0, len(boxes["map_box_uid_pk"])):
                cols["map_x_map_uid_pk"] = SHM.get_uid()
                cols["map_uid_1_fk"] = rects["map_rect_uid_pk"][r]
                cols["map_uid_2_fk"] = boxes["map_box_uid_pk"][b]
                cols["touch_type"] = random.choice(EntityType.MAP_TOUCH_TYPE)
                cols["delete_dt"] = ""
                DB.execute_insert(sql, tuple(cols.values()))
        for b in range(0, len(boxes["map_box_uid_pk"])):
            for s in range(0, len(spheres["map_sphere_uid_pk"])):
                cols["map_x_map_uid_pk"] = SHM.get_uid()
                cols["map_uid_1_fk"] = boxes["map_box_uid_pk"][b]
                cols["map_uid_2_fk"] = spheres["map_sphere_uid_pk"][s]
                cols["touch_type"] = random.choice(EntityType.MAP_TOUCH_TYPE)
                cols["delete_dt"] = ""
                DB.execute_insert(sql, tuple(cols.values()))
