"""

:module:    data_set.py
:class:     SetData/0
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

# import json
import data_model_app as DMA
import data_model_story as DMS

from method_files import FileMethods
from method_shell import ShellMethods
from collections import OrderedDict
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401
from data_base import DataBase
from data_get import GetData
from data_structs import Colors

FM = FileMethods()
SM = ShellMethods()
GD = GetData()


class SetDataError(Exception):
    """Custom error class for SetData errors."""
    pass


class SetData():
    """
    Provide methods for setting data in the database.
    Generic DB IO methods are in the data_base module.
    This module is for more complex/bespoke use cases.

    @TODO:
    - Add method for loading WIDGETS table from config data,
      after defining the WIDGETS data model.
    - Once the Admin front-end is more defined, many of the methods
      for setting data on the Story models can likely be added here.
    """

    def __init__(self):
        """
        Initialize a new instance of the SetData class.
        """
        self.CONTEXT = FM.get_json_file("static/context/context.json")
        self.USERDATA = FM.get_json_file("static/context/userdata.json")
        self.DB = DataBase(self.CONTEXT)

    def _prep_data_set(self, data_model: object, use_config=True) -> tuple:
        """
        Prepare data sets for a given table, based on data model and
        its related JSON boot->config file, if requested.
        Return a prepared set of things to help optimize SET operations

        :param data_model: An instance of a data model class.
        :param use_config: bool - Use a JSON config file if True.
        :returns: A tuple containing:
                  - Table name (str)
                  - Table data (dict) from JSON configuration or empty dict
                  - Column names for the selected model (ordered dict)
        """
        # Extract table name
        tbl_nm = data_model._tablename
        if use_config:
            # Retrieve configuration file path
            config_path = self.CONTEXT["cfg"].get(tbl_nm.lower(), "")
            # Load table data from JSON file if a valid config path provided
            tbl_data = FM.get_json_file(config_path) if config_path else {}
            if not tbl_data:
                print(f"{Colors.CL_YELLOW}WARNING{Colors.CL_END}: " +
                      f"No config data found for {tbl_nm} at {config_path}.")
        else:
            tbl_data: dict = {}
        # Convert model to an ordered dictionary of tbl_cols
        tbl_cols = OrderedDict(data_model.to_dict()[tbl_nm])
        return (tbl_nm, tbl_data, tbl_cols)

    def _virtual_delete(self, p_table_nm: str, p_rec: dict) -> bool:
        """
        Mark a record as deleted by setting the delete_dt column to the current time.
        :param p_table_nm: Name of the table to update.
        :param p_rec: Dict of current record values.
        :return: True if the operation is successful, False otherwise.
        """
        rec = p_rec.copy()
        rec["delete_dt"] = SM.get_iso_time_stamp()
        uid_key = f"{p_table_nm}_uid_pk".lower()
        uid = rec[uid_key]
        del rec[uid_key]
        return self.DB.execute_update(p_table_nm, uid, tuple(rec.values()))

    def _set_insert(self, p_table_name: str, p_del_match: dict, t_cols) -> bool:
        """Code shared by the set_rect_maps, set_box_maps, and set_sphere_maps methods.
        :param p_table_name: str - Name of the table to update.
        :param p_del_match: dict - Dictionary of values to match on for virtual delete/update.
        :param t_cols: dict - Dictionary of column values for the map.
        """
        existing_data = GD.get_by_match(p_table_name, p_del_match)
        if existing_data and not self._virtual_delete(p_table_name, existing_data):
            raise SetDataError(f"{Colors.CL_RED}Error applying virtual delete " +
                               f"on {p_table_name}{Colors.CL_END}.")
        if not self.DB.execute_insert(p_table_name, (SM.get_uid(), tuple(t_cols.values()))):
            raise SetDataError(f"{Colors.CL_RED}Error inserting data " +
                               f"into {p_table_name}{Colors.CL_END}.")
        return True

    def set_texts(self) -> bool:
        """
        Retrieve config file and use it to populate designated table.
        In some configs each line of the file relates to a single record on DB.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.Texts())
        language_code = self.CONTEXT["lang"]
        for text_name, text_value in table_data.items():
            t_cols = table_cols.copy()
            t_cols.pop("text_uid_pk")
            t_cols.update(
                {
                    "lang_code": language_code,
                    "text_name": text_name,
                    "text_value": text_value,
                    "delete_dt": "",
                }
            )
            del_match = {"lang_code": language_code, "text_name": text_name}
            self._set_insert(table_name, del_match, t_cols)
        return True

    def set_frames(self) -> bool:
        """
        Populate the FRAMES table using config data.
        A "frame" is the highest-level container, named like "saskan" or "admin".
        Some config files have multiple layers of data, with values are grouped by ID.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.Frames())
        for frame_id, frame_config in table_data.items():
            t_cols = table_cols.copy()
            t_cols.pop("frame_uid_pk")
            t_cols.update(
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
            del_match = {"frame_id": frame_id}
            self._set_insert(table_name, del_match, t_cols)
        return True

    def set_menu_bars(self) -> bool:
        """
        Populate the MENU_BARS table using configuration data for all frames.
        Fail if natural link to FRAMES is not found.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.MenuBars())
        for frame_id, mb_config in table_data.items():
            linked_data = GD.get_by_match("FRAMES", {"frame_id": frame_id})
            if not linked_data:
                raise SetDataError(f"{Colors.CL_RED}Link to FRAMES not found.{Colors.CL_END}")
            t_cols = table_cols.copy()
            t_cols.pop("menu_bar_uid_pk")
            t_cols.update(
                {
                    "frame_uid_fk": linked_data["frame_uid_pk"],
                    "frame_id": frame_id,
                    "mbar_margin": mb_config["menu_bars"]["margin"],
                    "mbar_h": mb_config["menu_bars"]["h"],
                    "mbar_x": mb_config["menu_bars"]["x"],
                    "mbar_y": mb_config["menu_bars"]["y"],
                    "delete_dt": "",
                }
            )
            del_match = {"frame_id": frame_id}
            self._set_insert(table_name, del_match, t_cols)
        return True

    def set_menus(self) -> bool:
        """
        Populate the MENUS table using configuration data for all frames.
        Some config files have two levels of identifiers, like "frame_id" and "menu_id".
        Fail if natural link to MENU_BARS is not found.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.Menus())
        for frame_id, menu_config in table_data.items():
            linked_data = GD.get_by_match("MENU_BARS", {"frame_id": frame_id})
            if not linked_data:
                raise SetDataError(f"{Colors.CL_RED}Link to MENU_BARS not found.{Colors.CL_END}")
            for menu_id, vals in menu_config.items():
                t_cols = table_cols.copy()
                t_cols.pop("menu_uid_pk")
                t_cols.update(
                    {
                        "menu_bar_uid_fk": linked_data["menu_bar_uid_pk"],
                        "frame_id": frame_id,
                        "lang_code": self.CONTEXT["lang"],
                        "menu_id": menu_id,
                        "menu_name": vals["name"],
                        "delete_dt": "",
                    }
                )
                del_match = {"frame_id": frame_id, "menu_id": menu_id}
                self._set_insert(table_name, del_match, t_cols)
        return True

    def set_menu_items(self) -> bool:
        """
        Populate the MENU_ITEMS table using menus configuration data for all frames.
        Fail if natural link to MENUS is not found.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.MenuItems())
        for frame_id, mi_config in table_data.items():
            for menu_id, mi_vals in mi_config.items():
                linked_data = GD.get_by_match("MENUS", {"frame_id": frame_id, "menu_id": menu_id})
                if not linked_data:
                    raise SetDataError(f"{Colors.CL_RED}Link to MENUS not found.{Colors.CL_END}")
                lang_code = (linked_data["lang_code"] if "lang_code" in linked_data else "en")
                item_order = 0
                for item_id, item_vals in mi_vals.items():
                    t_cols = table_cols.copy()
                    help_text = (item_vals["help_text"] if "help_text" in item_vals.keys() else "")
                    enabled_by_default = (item_vals["enabled"]
                                          if "enabled" in item_vals.keys() else True)
                    t_cols.pop("item_uid_pk")
                    t_cols.update(
                        {
                            "menu_uid_fk": linked_data["menu_uid_pk"],
                            "lang_code": lang_code,
                            "frame_id": frame_id,
                            "item_id": item_id,
                            "item_order": item_order,
                            "item_name": item_vals["name"],
                            "key_binding": item_vals["key_b"],
                            "help_text": help_text,
                            "enabled_by_default": enabled_by_default,
                            "delete_dt": "",
                        }
                    )
                    del_match = {"menu_uid_fk": linked_data["menu_uid_pk"], "item_id": item_id}
                    self._set_insert(table_name, del_match, t_cols)
                    item_order += 1
        return True

    def set_windows(self) -> bool:
        """
        Populate WINDOWS table using configuration data for all frames.
        Fail if natural link to FRAMES is not found.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.Windows())
        for frame_id, win_config in table_data.items():
            linked_data = GD.get_by_match("FRAMES", {"frame_id": frame_id})
            if not linked_data:
                raise SetDataError(f"{Colors.CL_RED}Link to FRAMES not found.{Colors.CL_END}")
            for win_id, win_vals in win_config.items():
                t_cols = table_cols.copy()
                t_cols.pop("win_uid_pk")
                t_cols.update(
                    {
                        "frame_uid_fk": linked_data["frame_uid_pk"],
                        "frame_id": frame_id,
                        "lang_code": win_vals["lang_code"],
                        "win_id": win_id,
                        "win_title": win_vals["title"],
                        "win_margin": win_vals["margin"],
                        "delete_dt": "",
                    }
                )
                del_match = {"frame_uid_fk": linked_data["frame_uid_pk"], "win_id": win_id}
                self._set_insert(table_name, del_match, t_cols)
        return True

    def set_links(self) -> bool:
        """
        Populate LINKS table using configuration data for all frames.
        Fail if natural link to FRAMES is not found.
        :return: True if all operations succeed; Raises error otherwise.
        @DEV:
        - Load icon images into DB as a BLOB
        """
        table_name, table_data, table_cols = self._prep_data_set(DMA.Links())
        for frame_id, link_config in table_data.items():
            linked_data = GD.get_by_match("FRAMES", {"frame_id": frame_id})
            if not linked_data:
                raise SetDataError(f"{Colors.CL_RED}Link to FRAMES not found.{Colors.CL_END}")
            for link_id, link_vals in link_config.items():
                t_cols = table_cols.copy()
                t_cols.pop("link_uid_pk")
                link_uri = (
                    self.CONTEXT[link_vals["uri"].split("%")[1]]
                    if "%" in link_vals["uri"] else link_vals["uri"]
                )
                t_cols.update(
                    {
                        "lang_code": self.CONTEXT["lang"],
                        "link_id": link_id,
                        "frame_id": frame_id,
                        "link_protocol": link_vals["protocol"],
                        "mime_type": link_vals["mime_type"],
                        "link_name": link_vals["name"],
                        "link_uri": link_uri,
                        "link_icon": link_vals["icon"],
                        "link_icon_path": link_vals["icon_path"],
                        "delete_dt": "",
                    }
                )
                del_match = {"frame_id": frame_id, "link_id": link_id}
                self._set_insert(table_name, del_match, t_cols)
        return True

    # Story-related Tables
    # ====================

    def set_rect_maps(self) -> bool:
        """Define rectangular maps for game use.
        Using hard-coded values for now. Eventually, these will be defined in a config file,
        maybe also via a GUI or CLI.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, _, table_cols = self._prep_data_set(DMS.MapRect(), False)
        map_name = "Saskan Lands Political Regions"
        t_cols = table_cols.copy()
        t_cols.pop("map_rect_uid_pk")
        t_cols.update(
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
        del_match = {"map_name": map_name}
        return self._set_insert(table_name, del_match, t_cols)

    def set_box_maps(self) -> bool:
        """Define a box (3D-ish, layered) maps for game use.
        Using hard-coded values for now. Eventually, these will be defined in a config file,
        maybe also via a GUI or CLI.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, _, table_cols = self._prep_data_set(DMS.MapBox(), False)
        map_name = "Saskan Lands Geography"
        t_cols = table_cols.copy()
        t_cols.pop("map_box_uid_pk")
        t_cols.update(
            {
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
        del_match = {"map_name": map_name}
        return self._set_insert(table_name, del_match, t_cols)

    def set_sphere_maps(self) -> bool:
        """Define spherical maps for game use.
        Using hard-coded values for now. Eventually, these will be defined in a config file,
        maybe also via a GUI or CLI.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, _, table_cols = self._prep_data_set(DMS.MapSphere(), False)
        map_name = "Gavor-Havorra Planetary Map"
        t_cols = table_cols.copy()
        t_cols.pop("map_sphere_uid_pk")
        t_cols.update(
            {
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
        )
        del_match = {"map_name": map_name}
        return self._set_insert(table_name, del_match, t_cols)

    def set_grids(self) -> bool:
        """Define Grids structures for game use.
        Using hard-coded values for now. Eventually, these will be defined in a config file,
        maybe also via a GUI or CLI.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, _, table_cols = self._prep_data_set(DMS.Grid(), False)
        grid_name = "30x_40y_30zu_30zd"
        table_cols.pop("grid_uid_pk")
        table_cols.update(
            {
                "grid_name": grid_name,
                "x_col_cnt": 30,
                "y_row_cnt": 40,
                "z_up_cnt": 30,
                "z_down_cnt": 30,
                "delete_dt": "",
            }
        )
        del_match = {"grid_name": grid_name}
        return self._set_insert(table_name, del_match, table_cols)
        return True

    def set_grid_cells(self) -> bool:
        """Define a set of Grid Cells for game use. This data uniquely identifies
        a cell in a grid by its x, y, and z coordinates, an ID, and a Name.
        Additional detailed content can be added to the GRID_INFO table.
        Fail if natural key to GRID is not found.

        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, _, table_cols = self._prep_data_set(DMS.GridCell(), False)
        grid_name = "30x_40y_30zu_30zd"
        grid_data = [
            {"grid_cell_name": "Selaron Town", "x_col_ix": 25, "y_row_ix": 12, "z_up_down_ix": 0},
            {"grid_cell_name": "Morilly Town", "x_col_ix": 15, "y_row_ix": 23, "z_up_down_ix": 0},
            {"grid_cell_name": "Wildwind Town", "x_col_ix": 12, "y_row_ix": 27, "z_up_down_ix": 0},
        ]
        linked_data = GD.get_by_match("GRID", {"grid_name": grid_name})
        if not linked_data:
            raise SetDataError(f"{Colors.CL_RED}Link to GRID not found.{Colors.CL_END}")
        for cells in grid_data:
            cell_cols = table_cols.copy()
            grid_cell_id = (
                f"{cells['x_col_ix']}x_"
                + f"{cells['y_row_ix']}y_"
                + f"{cells['z_up_down_ix']}z"
            )
            cell_cols.pop("grid_cell_uid_pk")
            cell_cols.update(
                {
                    "grid_uid_fk": linked_data["grid_uid_pk"],
                    "grid_name": grid_name,
                    "grid_cell_name": cells["grid_cell_name"],
                    "x_col_ix": cells["x_col_ix"],
                    "y_row_ix": cells["y_row_ix"],
                    "z_up_down_ix": cells["z_up_down_ix"],
                    "grid_cell_id": grid_cell_id,
                    "delete_dt": "",
                }
            )
            del_match = {"grid_name": grid_name, "grid_cell_id": grid_cell_id}
            self._set_insert(table_name, del_match, cell_cols)
        return True

    def set_grid_infos(self) -> bool:
        """Define a set of Grid Info records for game use.
        Fail if natural keys to GRID and GRID_CELL are not found.
        :return: True if all operations succeed; Raises error otherwise.
        @DEV:
        - If an image path is provided, then load the image into the DB as a BLOB.
        """
        table_name, _, table_cols = self._prep_data_set(DMS.GridInfo(), False)
        grid_name = "30x_40y_30zu_30zd"
        linked_grid_data = GD.get_by_match("GRID", {"grid_name": grid_name})
        if not linked_grid_data:
            raise SetDataError(f"{Colors.CL_RED}Link to GRID not found.{Colors.CL_END}")

        info_data = [
            {'grid_info_id': "town", 'grid_info_name': "Seaport Town",
             'grid_info_img_path': "static/images/seaport_icon.jpg"},
            {'grid_info_id': "town", 'grid_info_name': "Riverside Town",
             'grid_info_img_path': "static/images/rivertown_icon.jpg"},
            {'grid_info_id': "town", 'grid_info_name': "Walled Town",
             'grid_info_img_path': "static/images/walledtown_icon.jpg"},
        ]
        for info_ix, grid_cell_name in enumerate(["Selaron Town", "Morilly Town", "Wildwind Town"]):
            linked_cell_data = GD.get_by_match("GRID_CELL", {"grid_cell_name": grid_cell_name})
            if not linked_cell_data:
                raise SetDataError(f"{Colors.CL_RED}Link to GRID_CELL not found.{Colors.CL_END}")

            info_cols = table_cols.copy()
            info_cols.pop("grid_info_uid_pk")
            info = info_data[info_ix]
            int_val = 0 if "grid_info_int" not in info else info["grid_info_int"]
            float_val = 0.0 if "grid_info_float" not in info else info["grid_info_float"]
            str_val = "" if "grid_info_str" not in info else info["grid_info_str"]
            json_val = "" if "grid_info_json" not in info else info["grid_info_json"]
            img_path = "" if "grid_info_img_path" not in info else info["grid_info_img_path"]
            img_val = b"" if "grid_info_img" not in info else info["grid_info_img"]
            info_cols.update(
                {
                    "grid_uid_fk": linked_grid_data["grid_uid_pk"],
                    "grid_cell_uid_fk": linked_cell_data["grid_cell_uid_pk"],
                    "grid_name": grid_name,
                    "grid_cell_name": grid_cell_name,
                    "grid_info_id": info["grid_info_id"],
                    "grid_info_name": info["grid_info_name"],
                    "grid_info_int": int_val,
                    "grid_info_float": float_val,
                    "grid_info_str": str_val,
                    "grid_info_json": json_val,
                    "grid_info_img_path": img_path,
                    "grid_info_img": img_val,
                    "delete_dt": "",
                }
            )
            del_match = {"grid_name": grid_name, "grid_cell_name": grid_cell_name}
            self._set_insert(table_name, del_match, info_cols)
        return True

    def set_cross_x(self, p_x_values: dict) -> bool:
        """
        Generic method for setting values in an association table.
        Define assoociation for an _X_ (association) table record using UIDs.
        Fail if either associated UID is not found.
        :param p_model: object - Data model object for an association table.
        :param p_x_values: dict - Dictionary of values, in this format:
                    {<uid_col_nm_1>: <uid_1_value>,
                     <uid_col_nm_2>: <uid_2_value>,
                     "touch_type": <touch_type_value> (optional)}
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, _, table_cols = self._prep_data_set(DMS.CrossAssociation(), False)
        # Derive linked table names from linked PK column names
        link_uids = list(p_x_values.keys())[:2]
        link_tables = [k.split("_uid")[0].upper() for k in link_uids]
        # Validate FK links
        for k_ix, uid in enumerate(link_uids):
            if not GD.get_by_match(link_tables[k_ix], {uid: p_x_values[uid]}):
                raise SetDataError(
                    f"{Colors.CL_RED}ERROR{Colors.CL_END}: Link to {link_tables[k_ix]} not found."
                )

        t_cols = table_cols.copy()
        t_cols.pop(f"{table_name}_uid_pk".lower())
        touch_type = p_x_values["touch_type"] if "touch_type" in p_x_values else ""
        t_cols.update(
            {
                "uid_1_table": link_tables[0],
                "uid_1_vfk": p_x_values[link_uids[0]],
                "uid_2_table": link_tables[1],
                "uid_2_vfk": p_x_values[link_uids[1]],
                "touch_type": touch_type,
                "delete_dt": "",
            }
        )
        del_match = {
            "uid_1_vfk": p_x_values[link_uids[0]],
            "uid_2_vfk": p_x_values[link_uids[1]],
        }
        self._set_insert(table_name, del_match, t_cols)
        return True

    def set_char_sets(self) -> bool:
        """Define sets of Character records for game use.
        :return: True if all operations succeed; Raises error otherwise.
        """
        table_name, _, table_cols = self._prep_data_set(DMS.CharSet(), False)
        charsets: list = [
            {
                "type": "abugida",
                "font_name": "EibarTraditional",
                "desc": "Eibar is the most widely spoken language in Saskantinon, particularly "
                + "in the northern and western regions. It is the language of power due to "
                + "its use by Fatunik scribes and as the official language of the region. "
                + "Over time, Eibar has become diverse, incorporating various accents and "
                + "influences from different regions",
            },
            {
                "type": "abugida",
                "font_name": "EibarRider",
                "desc": "Rider Eibar is the dialect used in the United Rider Provinces except "
                + "for Eelan, and some adjoining areas. It uses a few additional characters "
                + "to represent sounds not found in the traditional Eibar abugida. But it is "
                + "not different enough to be considered a separate language.",
            },
            {
                "type": "abugida",
                "font_name": "EibarWestern",
                "desc": "Western Eibar is the dialect used in Eelan province and in High Weir. "
                + "It uses several additional characters to represent sounds not found in the "
                + "traditional Eibar abugida. But it is not different enough to be considered a "
                + "separate language.",
            },
            {
                "type": "abugida",
                "font_name": "EibarEastern",
                "desc": "Eastern Eibar is the dialect used in the Runes of Bye, Mobalbeshqi "
                + "and the Kahila Lands. It uses several additional characters to represent "
                + "sounds not found in the traditional Eibar abugida. But it is not different "
                + "enough to be considered a separate language.",
            },
            {
                "type": "abugida",
                "font_name": "EibarqBasic",
                "desc": "Basic Eibarq is spoken in the easternmost areas of Saskantinon, "
                + "including parts of Pavanarune, and in Kahilakol, Kahilabequa, Mobalbesq, "
                + "Byerung (that is, the Runes of Bye) and in the Ny Lands. While mutually "
                + "intelligible with Eibar to a large degree, Eibarq exhibits very distinct "
                + "phonemes and idiomatic expressions rooted in non-huum modes of utterance. "
                + "It is favored by non-huum-looking individuals who want to emphasize their "
                + "distinction, and it includes many alternative phrasings and slang that differ "
                + "from standard Eibar, as well as an entirely distinctive abuigida where many "
                + "characters map directly to the Eibar characters, but many others do not.",
            },
        ]
        for cs in charsets:
            cs_cols = table_cols.copy()
            cs_cols.pop("char_set_uid_pk")
            cs_cols.update(
                {
                    "font_name": cs["font_name"],
                    "char_set_type": cs["type"],
                    "char_set_desc": cs["desc"],
                    "delete_dt": "",
                }
            )
            del_match = {"font_name": cs["font_name"]}
            self._set_insert(table_name, del_match, cs_cols)

        return True
