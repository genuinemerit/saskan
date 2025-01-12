#!python
"""Saskan Apps file installation procedure.
:module:    boot.py
:class:     SaskanBoot/0
:author:    GM <genuinemerit @ pm.me>

`Saskantinon`or `saskan`  = the game itself, the end-user interface
`Saskantinize` or `admin` = the world-building and admin tool

Create SQL, databases and populate with base app and story data.
Python modules are executed from project directory.
Manage paths with that in mind.

This one-time setup procedure creates DB, populates it with base data.
It is run in development mode. Everything generated here is eventually
packaged into the appfor distribution.

To run this script to set up the dev environment,
execute the following command from the project root / top-level directory:
    `python src/Saskantinon/boot.py` (to use default userdata path) OR
    `python src/Saskantinon/boot.py <userdata file path>`

@DEV:
- When I get back to the service architecture...
    - Prototype/test using haproxy to load balance servers.
    - Use haproxy to route to different servers based on URL.
    - Reduce proliferation of ports. Shouldn't need that many.
    - Start with a single port; add more only as needed.
    - Cleanly separate server and client code.
"""
import json
import sys
from pprint import pprint as pp  # noqa: F401
import data_model as DM

from data_base import DataBase
from data_set import SetData
from data_get import GetData

from method_files import FileMethods
from method_shell import ShellMethods
from data_structs import Colors

FM = FileMethods()
SM = ShellMethods()
SD = SetData()
GD = GetData()


class BootError(Exception):
    """Custom error class for BootError errors."""
    pass


class BootSaskan():
    """Configure and boot Saskantinon and Saskantinize.
    Generate SQL files.
    Create and populate database.
    """

    def __init__(self):
        """
        Initialize database and load necessary data.
        """
        self._initialize_file_paths()
        self.CONTEXT = self._boot_context()
        self.DB = DataBase(self.CONTEXT)

    # Init methods, called from init

    def _get_userdata_path(self):
        """Get the user data path from arguments or use default."""
        if len(sys.argv) > 1:
            return sys.argv[1]
        return f"{SM.get_os_home()}/Documents/hofin_user_files"

    def _initialize_file_paths(self):
        """Set up file paths for context and user data."""
        self.CONTEXT_FILE_PATH = "static/context/context.json"
        self.USERDATA_CONTEXT_FILE = "static/context/userdata.json"
        self.USERDATA_PATH = self._get_userdata_path()

    def _boot_context(self):
        """
        Create static context data file.
        This allows us to bootstrap the database and recreate
        the context file in case it gets deleted.
        :writes: /static/context/context.json
        :returns: dict of context data
        """
        context: dict = {
            "cfg": {},
            "db": "db",
            "ddl": "boot/ddl",
            "dml": "db/dml",
            "fonts": "static/fonts",
            "git": "github.com/genuinemerit/saskan-app/",
            "images": "static/images",
            "lang": "en",
            "saskan_db": "db/SASKAN.db",
            "saskan_bak": "db/SASKAN.bak",
            "web": "static/web",
            "wiki": "github.com/genuinemerit/saskan-wiki/",
        }
        for cfg in ["frames", "menu_bars", "menus", "menu_items",
                    "texts", "widgets", "windows", "links"]:
            context["cfg"][cfg] = "boot/config/" + cfg + ".json"
        FM.write_file(self.CONTEXT_FILE_PATH, json.dumps(context))
        return context

    # Boot methods, called from main

    def boot_saskan(self):
        """Run all boot steps:
        - Create SQL files and initialize the SQLite3 database and tables.
          Writes to: /boot/ddl/*.sql, /db/dml/*.sql, /db/SASKAN.db, and /db/SASKAN.bak
        - Populate the database with base app and story data.
        """
        if DM.create_sql(self.DB):
            if DM.create_db(self.DB):
                self.boot_app_data()
                self.boot_story_data()
            else:
                print(f"{Colors.RED}Database creation failed{Colors.CL_END}")

    def boot_app_data(self):
        """
        Populate database tables for GUI, API's, etc.
        :write:  /db/SASKAN.db
        """
        if not self.DB.execute_ddl(["DROP_METADATA", "CREATE_METADATA", "INSERT_METADATA"], False):
            raise BootError(f"{Colors.CL_RED}Error populating METADATA{Colors.CL_END}")
        else:
            print(f"{Colors.CL_DARKCYAN}METADATA populated{Colors.CL_END}")
        components = [
            ("TEXTS", SD.set_texts),
            ("FRAMES", SD.set_frames),
            ("MENU_BARS", SD.set_menu_bars),
            ("MENUS", SD.set_menus),
            ("MENU_ITEMS", SD.set_menu_items),
            ("WINDOWS", SD.set_windows),
            ("LINKS", SD.set_links),
        ]
        for component_name, set_function in components:
            if set_function():
                print(f"{Colors.CL_DARKCYAN}{component_name} populated{Colors.CL_END}")
            else:
                raise BootError(f"{Colors.CL_RED}Error populating {component_name}{Colors.CL_END}")
        print(f"{Colors.CL_DARKCYAN}{Colors.CL_BOLD}App data populated\n{Colors.CL_END}")

    def boot_story_data(self):
        """
        Populate database tables for game, story, and world-building.
        N.B. - For now this includes some test data.
        @DEV:
        - Modify that to use TEST modules or some kind of data INIT modules.
        - Modify to use config files for static data.
        - Consider using alternative config files for different scenarios.
        - Consider implementing CLI-based inputs.
        - Consider using a GUI for data entry.
        :write: /db/SASKAN.db
        """
        self.populate_story_tables()
        self.populate_cross_x()
        self.populate_fonts_glossaries()
        print(f"{Colors.CL_DARKCYAN}{Colors.CL_BOLD}Story data populated\n{Colors.CL_END}")

    def populate_story_tables(self):
        """Populate various story tables. """
        components = [
            ("MAP_RECT", SD.set_rect_maps),
            ("MAP_BOX", SD.set_box_maps),
            ("MAP_SPHERE", SD.set_sphere_maps),
            ("GRID", SD.set_grids),
            ("GRID_CELL", SD.set_grid_cells),
            ("GRID_INFO", SD.set_grid_infos),
        ]
        for component_name, set_function in components:
            if set_function():
                print(f"{Colors.CL_DARKCYAN}{component_name} populated{Colors.CL_END}")
            else:
                raise BootError(f"{Colors.CL_RED}Error populating {component_name}{Colors.CL_END}")
        return True

    def populate_cross_x(self):
        """Populate cross-x (association, n-t-n) data, that is association tables.

        The set_cross_x method assumes that the caller knows the UID col names and
        the UID values of the rows being associated. For example, retrieve recs by map_name
        or grid_name (may rename that an ID, which would be more appropirate), that is, a
        natural key which should be unique in combination with a blank delete_dt. Retrieve
        the UIDs, then call the set_cross_x method with the UID col names, values and touch type.

        param values in call are a dict of values:
            {<uid_col_nm_1>: <uid_1_value>,
             <uid_col_nm_2>: <uid_2_value>,
             "touch_type": <touch_type_value> (optional)}
        """
        fail = f"{Colors.CL_RED}Error populating CROSS_X{Colors.CL_END}"
        map_rect_data = GD.get_by_match("MAP_RECT", {"map_name": "Saskan Lands Political Regions"})
        map_box_data = GD.get_by_match("MAP_BOX", {"map_name": "Saskan Lands Geography"})
        map_sphere_data = GD.get_by_match(
                          "MAP_SPHERE", {"map_name": "Gavor-Havorra Planetary Map"})
        grid_data = GD.get_by_match("GRID", {"grid_name": "30x_40y_30zu_30zd"})
        # This tests the default touch type of ""
        if not SD.set_cross_x({"map_rect_uid_pk": map_rect_data['map_rect_uid_pk'],
                               "map_box_uid_pk": map_box_data['map_box_uid_pk']}):
            raise BootError(fail)
        # This tests the virtual delete logic
        if not SD.set_cross_x({"map_rect_uid_pk": map_rect_data['map_rect_uid_pk'],
                               "map_box_uid_pk": map_box_data['map_box_uid_pk'],
                               "touch_type": "overlaps"}):
            raise BootError(fail)
        if not SD.set_cross_x({"map_sphere_uid_pk": map_sphere_data['map_sphere_uid_pk'],
                               "map_box_uid_pk": map_box_data['map_box_uid_pk'],
                               "touch_type": "contains"}):
            raise BootError(fail)
        if not SD.set_cross_x({"map_rect_uid_pk": map_rect_data['map_rect_uid_pk'],
                               "grid_uid_pk": grid_data['grid_uid_pk'],
                               "touch_type": "overlaps"}):
            raise BootError(fail)

        print(f"{Colors.CL_DARKCYAN}CROSS_X populated{Colors.CL_END}")
        return True

    def populate_fonts_glossaries(self):
        """Populate character set and glossary tables."""
        fail = f"{Colors.CL_RED}Error populating CHAR* or GLOSS* tables{Colors.CL_END}"
        if not SD.set_char_sets():
            raise BootError(fail)
        # print(f"{Colors.CL_DARKCYAN}CHAR_SET, CHAR_MEMBER, GLOSS_COMMMON " +
        #      f"and glossary populated{Colors.CL_END}")
        print(f"{Colors.CL_DARKCYAN}CHAR_SET populated{Colors.CL_END}")
        return True


if __name__ == "__main__":
    BS = BootSaskan()
    BS.boot_saskan()
