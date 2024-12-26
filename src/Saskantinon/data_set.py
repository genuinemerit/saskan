"""

:module:    data_set.py
:class:     SetData/0
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

import json
import random
import secrets
import method_files as FM
import method_shell as SM
import data_model_app as DMA
import data_model_story as DMS

from collections import OrderedDict
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401
from data_base import DataBase
from data_get import GetData
from data_structs import EntityType, Colors

GD = GetData()


class SetData:
    """
    Provide methods for setting data in the database.
    Generic DB IO methods are in the data_base module.
    This module is for more complex/bespoke use cases.

    @TODO:
    - Add method for loading WIDGETS table from config data,
      after defining the WIDGETS data model.
    """

    def __init__(self):
        """
        Initialize a new instance of the SetData class.
        """
        self.GRID_UID: dict = {}
        self.CONTEXT = FM.get_json_file("static/context/context.json")
        self.USERDATA = FM.get_json_file("static/context/userdata.json")
        self.DB = DataBase(self.CONTEXT)

    def boot_user_data(self, p_userdata_path: str = None) -> None:
        """
        Define root path for where user data files will be collected.
        If no valid path is provided, defaults to "~/Documents/hofin_userdata".

        @DEV:
        - This may not be useful in Sasakantinon. Pulled it in from Home-Finance app.

        :param p_userdata_path: Path to userdata files root directory or None.
        :writes: /static/context/userdata.json
        """
        default_path = "/Documents/hofin_userdata"
        home = SM.get_os_home()

        # Determine the absolute path for userdata
        if not p_userdata_path or not FM.is_file_or_dir(p_userdata_path):
            userdata_path = home + default_path
        else:
            userdata_path = FM.get_absolute_path(p_userdata_path)

        # Write userdata path to context file
        context_data = {"userdata_path": userdata_path}
        FM.write_file("static/context/userdata.json", json.dumps(context_data))
        print(f"{Colors.CL_GREEN}Userdata path set to{Colors.CL_END}: {userdata_path}")

        # Ensure the userdata directory exists
        if not FM.is_file_or_dir(userdata_path):
            FM.make_dir(userdata_path)

        # Update instance variables
        self.USERDATA = context_data

    def _virtual_delete(self, p_table_nm: str, p_rec: dict) -> bool:
        """
        Mark a record as deleted by setting the delete_dt column to the current time.
        :param p_table_nm: Name of the table to update.
        :param p_rec: Dict of current record values.
        :return: True if the operation is successful, False otherwise.
        """
        rec = p_rec.copy()
        rec["delete_dt"] = SM.get_iso_time_stamp()
        uid_key = f"{p_table_nm}_uid_pk"
        uid = rec[uid_key]
        del rec[uid_key]
        return self.DB.execute_update(p_table_nm, uid, tuple(rec.values()))

    # Template for an insert/update method where value/s passed in as string
    # Eventually these will have a CLI and/or GUI front-end to get the values

    def set_user_name(self, p_user_name: str) -> bool:
        """
        Set a user name.
        1) Mark previous record deleted on DB if it exists.
        2) Insert new record to DB table.

        :param p_user_name: user name or nickname
        :return: True if the operation is successful, False otherwise.

        @DEV:
        - Extend to handle other optional inputs like email, phone, etc.
                    data["user_name"][i],
                    data["user_email"][i],
                    data["user_phone"][i],
                    data["user_key"][i],
        @NB: This is a simple example. In a real app, this would likely
             be a more complex record. This is a place-holder. At present,
             no USER_NAME table or model is defined.
        """
        tbl_nm = "USER_NAME"
        # Attempt to delete existing record if it exists
        data = GD.get_by_match(tbl_nm, {"user_name": p_user_name})

        if data and not self._virtual_delete(tbl_nm, data[0]):
            return False

        # Insert new user name record
        return self.DB.execute_insert(
            tbl_nm, (SM.get_uid(), p_user_name, "", "", "", "")
        )

    # App Scaffolding Tables - DB tables pre-populated from Config data.

    def _prep_data_set(self, data_model: object) -> tuple:
        """
        Prepare data sets for a given table, based on data model and
        its related JSON boot->config file.

        :param DM: An instance of a data model class.
        :returns: A tuple containing:
                  - Table name (str)
                  - Table data (dict) from JSON configuration
                  - Column names for the selected model (ordered dict)
        """
        # Extract table name and determine configuration path
        tbl_nm = data_model._tablename
        # Retrieve configuration file path
        config_path = self.CONTEXT["cfg"].get(tbl_nm.lower(), "")
        # Load table data from JSON file if a valid configuration path is provided
        tbl_data = FM.get_json_file(config_path) if config_path else {}
        # Convert model to an ordered dictionary of tbl_cols
        tbl_cols = OrderedDict(data_model.to_dict()[tbl_nm])
        # Return a prepared set of things to help optimize SET operations
        return (tbl_nm, tbl_data, tbl_cols)

    # Config-sourced insert/update where each line of the config file is a record
    def set_texts(self) -> bool:
        """
        Retrieve a config file and use it to populate the designated table.
        and use it to populate the TEXTS table. Update existing entries
        or insert new ones based on their presence in the database.

        Some config files and tables, like `texts` and 'TEXTS` are very
        simple. Each line of the config file relates to a single record on DB.

        :param p_context: A dictionary containing context values.
        :return: True if all operations succeed, False otherwise.
        """
        DB, tbl_nm, tbl_data, tbl_cols = self._prep_data_set(DMA.Texts())
        language_code = self.CONTEXT["lang"]
        for text_name, text_value in tbl_data.items():
            tbl_cols.update(
                {
                    "lang_code": language_code,
                    "text_name": text_name,
                    "text_value": text_value,
                    "delete_dt": "",
                }
            )
            data = GD.get_by_match(
                tbl_nm, {"lang_code": language_code, "text_name": text_name}
            )
            if data and not self._virtual_delete(tbl_nm, data[0]):
                return False
            del tbl_cols["text_uid_pk"]
            if not self.DB.execute_insert(
                tbl_nm, (SM.get_uid(), tuple(tbl_cols.values()))
            ):
                return False
        return True

    # Config-sourced insert/update where config file has two layers of data:
    # 1) The natural key (but not a PK) which is the index for...
    # 2) the rest of the data to be inserted on that row.

    def set_frames(self) -> bool:
        """
        Populate the FRAMES table using configuration data for all frames.

        :return: bool - Returns True if the operation is successful for all frames,
                        otherwise False.
        """
        # Prepare the data set for the FRAMES table
        table_name, table_data, table_cols = self._prep_data_set(DMA.Frames())

        # Iterate over each frame configuration
        for frame_id, frame_config in table_data.items():

            existing_data = GD.get_by_match(table_name, {"frame_id": frame_id})
            if existing_data and not self._virtual_delete(table_name, existing_data[0]):
                return False

            table_cols.pop("frame_uid_pk")
            # Populate table columns with frame configuration
            table_cols.update(
                {
                    "frame_id": frame_id,
                    "lang_code": self.CONTEXT["lang"],
                    "frame_title": frame_config["title"],
                    "frame_desc": frame_config["desc"],
                    "frame_w": frame_config["frame_w"],
                    "frame_h": frame_config["frame_h"],
                    "pg_hdr_x": frame_config["pg_hdr_x"],
                    "pg_hdr_y": frame_config["pg_hdr_y"],
                    "pg_hdr_w": frame_config["pg_hdr_w"],
                    "pg_hdr_h": frame_config["pg_hdr_h"],
                    "pg_hdr_txt": frame_config["pg_hdr_text"],
                    "delete_dt": "",
                }
            )
            if not self.DB.execute_insert(
                table_name, (SM.get_uid(), tuple(table_cols.values()))
            ):
                return False

        return True

    def set_menu_bars(self) -> bool:
        """
        Populate the MENU_BARS table using configuration data for all frames.
        Fail if natural link to FRAMES is not found.
        :returns: bool - True if operation is successful for all frames, otherwise False.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.MenuBars())

        for frame_id, mb_config in table_data.items():

            data = GD.get_by_match("FRAMES", {"frame_id": frame_id})
            if not data:
                print(f"{Colors.CL_RED}ERROR{Colors.CL_END}: Link to FRAMES not found.")
                return False

            existing_data = GD.get_by_match(table_name, {"frame_id": frame_id})
            if existing_data and not self._virtual_delete(table_name, existing_data[0]):
                return False

            table_cols.pop("menu_bars_uid_pk")
            table_cols.update(
                {
                    "frame_uid_fk": data[0]["frame_uid_pk"],
                    "frame_id": frame_id,
                    "mbar_margin": mb_config["menu_bars"]["margin"],
                    "mbar_h": mb_config["menu_bars"]["h"],
                    "mbar_x": mb_config["menu_bars"]["x"],
                    "mbar_y": mb_config["menu_bars"]["y"],
                    "delete_dt": "",
                }
            )
            if not self.DB.execute_insert(
                table_name, (SM.get_uid(), tuple(table_cols.values()))
            ):
                return False

        return True

    # Config-sourced insert/update where config file has multiple layers of data
    #  belonging to different, but linked, tables.
    # 1) A high-level category, typically a frame_id like 'saskan' or 'admin', which has...
    # 2) mulitple sub-id's such as a menu_id, which has...
    # 3) a set of values to be inserted on that row to MENUS table, but which...
    # 4) can include a category name, like "items", which groups values to store
    #     on another, linked, record.

    def set_menus(self) -> bool:
        """
        Populate the MENUS table using configuration data for all frames.
        Fail if natural link to MENU_BARS is not found.
        :returns: bool - True if operation is successful for all frames, otherwise False.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.Menus())

        # Handle frame-level / linked values
        for frame_id, menu_config in table_data.items():

            linked_data = GD.get_by_match("MENU_BARS", {"frame_id": frame_id})
            if not linked_data:
                print(
                    f"{Colors.CL_RED}ERROR{Colors.CL_END}: Link to MENU_BARS not found."
                )
                return False

            # Hnadle values specific to a menu,
            # except for menu items, which are stored separately (see set_menu_items)
            for menu_id, vals in menu_config.items():
                existing_data = GD.get_by_match(
                    table_name, {"frame_id": frame_id, "menu_id": menu_id}
                )
                if existing_data and not self._virtual_delete(
                    table_name, existing_data[0]
                ):
                    return False

                table_cols.pop("menus_uid_pk")
                table_cols.update(
                    {
                        "frame_uid_fk": menu_config[0]["frame_uid_pk"],
                        "menu_bar_uid_fk": menu_config[0]["menu_bar_uid_pk"],
                        "lang_code": self.CONTEXT["lang"],
                        "menu_id": menu_id,
                        "Menu_name": vals["name"],
                        "delete_dt": "",
                    }
                )
                if not self.DB.execute_insert(
                    table_name, (SM.get_uid(), tuple(table_cols.values()))
                ):
                    return False

        return True

    def set_menu_items(self) -> bool:
        """
        Populate the MENU_ITEMS table using menus configuration data for all frames.
        Fail if natural link to MENUS is not found.
        :returns: bool - True if operation is successful for all frames, otherwise False.
        """

        table_name, table_data, table_cols = self._prep_data_set(DMA.MenuItems())

        # Handle frame-level / linked values
        for frame_id, menu_config in table_data.items():

            # Handle menu-level values
            for menu_id, menu_vals in menu_config["menus"].items():

                linked_data = GD.get_by_match(
                    "MENUS", {"lang_code": menu_vals["lang_code"], "menu_id": menu_id}
                )
                if not linked_data:
                    print(
                        f"{Colors.CL_RED}ERROR{Colors.CL_END}: Link to MENUS not found."
                    )
                    return False

                existing_data = GD.get_by_match(
                    table_name, {"menu_uid_fk": linked_data[0]["menu_uid_pk"]}
                )
                if existing_data and not self._virtual_delete(
                    table_name, existing_data[0]
                ):
                    return False

                # Handle item-level values
                item_order = 0
                for item_id, item_vals in menu_vals["items"].items():
                    table_cols.pop("item_uid_pk")
                    help_text = (
                        item_vals[item_id]["help_text"]
                        if "help_text" in item_vals[item_id]
                        else ""
                    )
                    enabled_default = (
                        item_vals[item_id]["enabled"]
                        if "enabled" in item_vals[item_id]
                        else True
                    )
                    table_cols.pop("item_uid_pk")
                    table_cols.update(
                        {
                            "menu_uid_fk": linked_data[0]["menu_uid_pk"],
                            "lang_code": menu_vals["lang_code"],
                            "frame_id": frame_id,
                            "item_id": item_id,
                            "item_order": item_order,
                            "item_name": item_vals[item_id]["name"],
                            "key_binding": item_vals[item_id]["key_b"],
                            "help_text": help_text,
                            "enabled_default": enabled_default,
                            "delete_dt": "",
                        }
                    )
                    item_order += 1
                    if not self.DB.execute_insert(
                        table_name, (SM.get_uid(), tuple(table_cols.values()))
                    ):
                        return False

        return True

    def set_windows(self) -> bool:
        """
        Populate WINDOWS table using configuration data for all frames.
        Fail if natural link to FRAMES is not found.
        :returns: bool - True if operation is successful for all windows, otherwise False.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.Windows())

        for frame_id, win_config in table_data.items():
            linked_data = GD.get_by_match("FRAMES", {"frame_id": frame_id})
            if not linked_data:
                print(f"{Colors.CL_RED}ERROR{Colors.CL_END}: Link to FRAMES not found.")
                return False

            for win_id, win_vals in win_config.items():
                existing_data = GD.get_by_match(
                    table_name,
                    {"frame_uid_fk": linked_data[0]["frame_uid_fk"], "win_id": win_id},
                )
                if existing_data and not self._virtual_delete(
                    table_name, existing_data[0]
                ):
                    return False

                table_cols.pop("win_uid_pk")
                table_cols.update(
                    {
                        "frame_uid_fk": linked_data[0]["frame_uid_fk"],
                        "frame_id": frame_id,
                        "lang_code": win_vals["lang_code"],
                        "win_id": win_id,
                        "win_title": win_vals["title"],
                        "win_margin": win_vals["margin"],
                        "delete_dt": "",
                    }
                )
                if not self.DB.execute_insert(
                    table_name, (SM.get_uid(), tuple(table_cols.values()))
                ):
                    return False

        return True

    def set_links(self) -> bool:
        """
        Populate LINKS table using configuration data for all frames.
        Fail if natural link to FRAMES is not found.
        :returns: bool - True if operation is successful for all Links, otherwise False.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.Links())
        for frame_id, link_config in table_data.items():
            linked_data = GD.get_by_match("FRAMES", {"frame_id": frame_id})
            if not linked_data:
                print(f"{Colors.CL_RED}ERROR{Colors.CL_END}: Link to FRAMES not found.")
                return False

            for link_id, link_vals in link_config.items():
                existing_data = GD.get_by_match(
                    table_name, {"frame_id": frame_id, "link_id": link_id}
                )
                if existing_data and not self._virtual_delete(
                    table_name, existing_data[0]
                ):
                    return False

                table_cols.pop("link_uid_pk")
                link_value = (
                    self.CONTEXT[link_vals["value"].split("%")[1]]
                    if "%" in link_vals["value"]
                    else link_vals["value"]
                )
                # after updating tables to handle BLOBs, this will need to be updated
                # to load the icon image from a file and store it in the DB
                table_cols.update(
                    {
                        "lang_code": self.CONTEXT["lang"],
                        "link_id": link_id,
                        "frame_id": frame_id,
                        "link_protocol": link_vals["protocol"],
                        "mime_type": link_vals["mime_type"],
                        "link_name": link_vals["name"],
                        "link_value": link_value,
                        "link_icon": link_vals["icon"],
                        "delete_dt": "",
                    }
                )
                if not self.DB.execute_insert(
                    table_name, (SM.get_uid(), tuple(table_cols.values()))
                ):
                    return False

        return True

    # Story-related Tables
    # At this point, there are not config data files for these types of tables.
    # For prototyping, they are hard-coded here.
    # Eventually, they will be populated either from a config file, a spreadsheet,
    # or a CLI or GUI front-end.

    def set_rect_maps(self) -> bool:
        """Define a rectangular map for game use."""
        table_name, _, table_cols = self._prep_data_set(DMA.MapRect())
        map_name = "Saskan Lands Political Regions"
        table_cols.pop("map_rect_uid_pk")
        table_cols.update(
            {
                "map_shape": "rectangle",
                "map_type": "political",
                "map_name": map_name,
                "map_desc": "Borders and names of the regions and provinces of Saskantinon.",
                "north_lat": 39.7392,
                "west_lon": -104.9902,
                "south_lat": 23.5696,
                "east_lon": -86.335,
                "delete_dt": "",
            }
        )
        existing_data = GD.get_by_match(table_name, {"map_name": map_name})
        if existing_data and not self._virtual_delete(table_name, existing_data[0]):
            return False
        if not self.DB.execute_insert(
            table_name, (SM.get_uid(), tuple(table_cols.values()))
        ):
            return False
        return True

    def set_box_maps(self) -> bool:
        """Define a box map for game use."""
        table_name, _, table_cols = self._prep_data_set(DMA.MapBox())
        map_name = "Saskan Lands Geography"
        table_cols.pop("map_box_uid_pk")
        table_cols.update(
            {
                "map_box_uid_pk": SM.get_uid(),
                "map_shape": "box",
                "map_type": "geo",
                "map_name": map_name,
                "map_desc": "Elevation, mountains, hills, lakes, rivers, and streams.",
                "north_lat": 39.7392,
                "west_lon": -104.9902,
                "south_lat": 23.5696,
                "east_lon": -86.335,
                "up_m": 4400.0,
                "down_m": 4300.0,
                "delete_dt": "",
            }
        )

        existing_data = GD.get_by_match(table_name, {"map_name": map_name})
        if existing_data and not self._virtual_delete(table_name, existing_data[0]):
            return False
        if not self.DB.execute_insert(SM.get_uid(), tuple(table_cols.values())):
            return False

        return True

    def set_sphere_maps(self) -> bool:
        """Define a spherical map for game use."""
        table_name, _, table_cols = self._prep_data_set(DMA.MapSphere())
        map_name = "Gavor-Havorra Planetary Map"
        table_cols.pop("map_sphere_uid_pk")
        table_cols.update = {
            "map_shape": "sphere",
            "map_type": "geo",
            "map_name": map_name,
            "map_desc": "Continents, oceans, and land masses of Gavor-Havorra.",
            "origin_lat": 0.0,
            "origin_lon": 0.0,
            "z_value": 0.0,
            "unit_of_measure": "KM",
            "sphere_radius": 6371.0,
            "delete_dt": "",
        }

        existing_data = GD.get_by_match(table_name, {"map_name": map_name})
        if existing_data and not self._virtual_delete(table_name, existing_data[0]):
            return False

        if not self.DB.execute_insert(SM.get_uid(), tuple(table_cols.values())):
            return False

        return True

    # Pick up here with re-factoring the rest of the methods

    def set_grids(self, p_context: dict):
        """Define a Grids for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_data_set(DMS.Grid(), p_context)
        cols["grid_uid_pk"] = SM.get_uid()
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
        DB, sql, _, cols = self._prep_data_set(DMS.GridCell(), p_context)
        # Read records to get UID for GRID instead of storing them
        for grid_name in self.GRID_UID:
            grid = GD.get_by_id("GRID", "grid_uid_pk", self.GRID_UID[grid_name], DB)
            for n in range(1, 11):
                cols["grid_cell_uid_pk"] = SM.get_uid()
                cols["grid_uid_fk"] = grid["grid_uid_pk"]
                cols["grid_cell_name"] = f"Test Cell {n}"
                cols["x_col_ix"] = random.randint(0, grid["x_col_cnt"] - 1)
                cols["y_row_ix"] = random.randint(0, grid["y_row_cnt"] - 1)
                cols["z_up_down_ix"] = random.randint(
                    (grid["z_down_cnt"] - 1) * -1, grid["z_up_cnt"] - 1
                )
                cols["grid_cell_id"] = (
                    f"{cols['x_col_ix']}x_"
                    + f"{cols['y_row_ix']}y_"
                    + f"{cols['z_up_down_ix']}z"
                )
                cols["delete_dt"] = ""
                DB.execute_insert(sql, tuple(cols.values()))

    def set_grid_infos(self, p_context: dict):
        """Define a set of Grid Info records for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_data_set(DMS.GridInfo(), p_context)
        cells = DB.execute_select_all("GRID_CELL")
        for n in range(0, len(cells["grid_cell_uid_pk"])):
            cols["grid_info_uid_pk"] = SM.get_uid()
            cols["grid_cell_uid_fk"] = cells["grid_cell_uid_pk"][n]
            cols["grid_info_id"] = f"Test Info ID {n}"
            cols["grid_info_data_type"] = random.choice(EntityType.DATA_TYPE)
            cols["grid_info_name"] = f"Test Info Name {n}"
            cols["grid_info_value"] = (
                random.randint(1, 1000)
                if cols["grid_info_data_type"] in ("INT", "FLOAT")
                else secrets.token_bytes(10)
            )
            cols["delete_dt"] = ""
            DB.execute_insert(sql, tuple(cols.values()))

    def set_map_x_maps(self, p_context: dict):
        """Define a set of Map_x_Map records for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_data_set(DMS.MapXMap(), p_context)
        rects = DB.execute_select_all("MAP_RECT")
        boxes = DB.execute_select_all("MAP_BOX")
        spheres = DB.execute_select_all("MAP_SPHERE")
        for r in range(0, len(rects["map_rect_uid_pk"])):
            for b in range(0, len(boxes["map_box_uid_pk"])):
                cols["map_x_map_uid_pk"] = SM.get_uid()
                cols["map_uid_1_fk"] = rects["map_rect_uid_pk"][r]
                cols["map_uid_2_fk"] = boxes["map_box_uid_pk"][b]
                cols["touch_type"] = random.choice(EntityType.MAP_TOUCH_TYPE)
                cols["delete_dt"] = ""
                DB.execute_insert(sql, tuple(cols.values()))
        for b in range(0, len(boxes["map_box_uid_pk"])):
            for s in range(0, len(spheres["map_sphere_uid_pk"])):
                cols["map_x_map_uid_pk"] = SM.get_uid()
                cols["map_uid_1_fk"] = boxes["map_box_uid_pk"][b]
                cols["map_uid_2_fk"] = spheres["map_sphere_uid_pk"][s]
                cols["touch_type"] = random.choice(EntityType.MAP_TOUCH_TYPE)
                cols["delete_dt"] = ""
                DB.execute_insert(sql, tuple(cols.values()))

    def set_grid_x_maps(self, p_context: dict):
        """Define a set of Grid_x_Map records for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_data_set(DMS.GridXMap(), p_context)

    def set_char_sets(self, p_context: dict):
        """Define sets of Character records for game use.
        :args:
        - p_context: dict of context values.
        """
        DB, sql, _, cols = self._prep_data_set(DMS.CharSet(), p_context)
        cols["char_set_uid_pk"] = SM.get_uid()
        cols["font_name"] = "EibarTraditional"
        cols["char_set_type"] = "abugida"
        cols["char_set_desc"] = (
            "Eibar is the most widely spoken language in Saskantinon, particularly in the northern and western regions. It is the language of power due to its use by Fatunik scribes and as the official language of the region. Over time, Eibar has become diverse, incorporating various accents and influences from different regions and immigrant populations. It is also commonly spoken in Byerung, especially among those involved in jurisprudence. Since it is an abugida, each character represents a consonant and a distinct vowel sound, which itself may be a dipthong. This means that dialects may include additional symbols."  # noqa E501
        )
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))

        cols["char_set_uid_pk"] = SM.get_uid()
        cols["font_name"] = "EibarRider"
        cols["char_set_type"] = "abugida"
        cols["char_set_desc"] = (
            "Rider Eibar is the dialect used in the United Rider Provinces except for Eelan, and some adjoining areas. It uses a few additional characters to represent sounds not found in the traditional Eibar abugida. But it is not different enough to be considered a separate language."  # noqa E501
        )
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))

        cols["char_set_uid_pk"] = SM.get_uid()
        cols["font_name"] = "EibarWestern"
        cols["char_set_type"] = "abugida"
        cols["char_set_desc"] = (
            "Western Eibar is the dialect used in Eelan province and in High Weir. It uses several additional characters to represent sounds not found in the traditional Eibar abugida. But it is not different enough to be considered a separate language."  # noqa E501
        )
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))

        cols["char_set_uid_pk"] = SM.get_uid()
        cols["font_name"] = "EibarEastern"
        cols["char_set_type"] = "abugida"
        cols["char_set_desc"] = (
            "Eastern Eibar is the dialect used in the Runes of Bye, Mobalbeshqi and the Kahila Lands. It uses several additional characters to represent sounds not found in the traditional Eibar abugida. But it is not different enough to be considered a separate language."  # noqa E501
        )
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))

        cols["char_set_uid_pk"] = SM.get_uid()
        cols["font_name"] = "EibarqBasic"
        cols["char_set_type"] = "abugida"
        cols["char_set_desc"] = (
            "Basic Eibarq is spoken in the easternmost areas of Saskantinon, including parts of Pavanarune, and in Kahilakol, Kahilabequa, Mobalbesq, Byerung (that is, the Runes of Bye) and in the Ny Lands. While mutually intelligible with Eibar to a large degree, Eibarq exhibits very distinct phonemes and idiomatic expressions rooted in non-huum modes of utterance. It is favored by non-huum-looking individuals who want to emphasize their distinction, and it includes many alternative phrasings and slang that differ from standard Eibar, as well as an entirely distinctive abuigida where many characters map directly to the Eibar characters, but many others do not."  # noqa E501
        )
        cols["delete_dt"] = ""
        DB.execute_insert(sql, tuple(cols.values()))
