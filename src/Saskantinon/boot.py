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

from method_files import FileMethods as FM
from method_shell import ShellMethods as SM

SD = SetData()


class BootSaskan(object):
    """Configure and boot Saskantinon and Saskantinize.
    Generate SQL files.
    Create and populate database.
    """

    def __init__(self):
        """
        Initialize database and load necessary data.
        """
        self._initialize_file_paths()
        self.CONTEXT = self.boot_context()
        self.DB = DataBase(self.CONTEXT)

    def _initialize_file_paths(self):
        """Set up file paths for context and user data."""
        self.CONTEXT_FILE_PATH = "static/context/context.json"
        self.USERDATA_CONTEXT_FILE = "static/context/userdata.json"
        self.USERDATA_PATH = self.get_userdata_path()

    def get_userdata_path(self):
        """Get the user data path from arguments or use default."""
        if len(sys.argv) > 1:
            return sys.argv[1]

        return f"{SM.get_os_home()}/Documents/hofin_user_files"

    def boot_saskan(self):
        """Run all boot steps."""
        self.boot_database()
        self.boot_app_data()
        self.boot_story_data()

    def boot_context(self):
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
        for cfg in ["frames", "links", "menus", "texts", "widgets", "windows"]:
            context["cfg"][cfg] = "boot/config/" + cfg + ".json"
        FM.write_file(self.CONTEXT_FILE_PATH, json.dumps(context))
        return context

    def boot_database(self):
        """
        Create SQL files and initialize the SQLite3 database and tables.
        Writes to: /boot/ddl/*.sql, /db/dml/*.sql, /db/SASKAN.db, and /db/SASKAN.bak
        """
        if self._generate_sql_files():
            print("SQL files (re-)generated.")
            if self._initialize_database():
                print("Database created.")

    def _generate_sql_files(self):
        """Generate SQL files needed for database setup."""
        return DM.create_sql(self.DB)

    def _initialize_database(self):
        """Create the database and its tables."""
        return DM.create_db(self.DB)

    def boot_app_data(self):
        """
        Populate database tables for GUI, API's, etc.
        :write:  /db/SASKAN.db
        """
        self.DB.execute_ddl(
            ["DROP_METADATA", "CREATE_METADATA", "INSERT_METADATA"], False
        )

        if SD.set_texts(self.CONTEXT):
            print("TEXTS populated.")

        def populate_components(frame_id):
            components = [
                ("FRAMES", SD.set_frames),
                ("MENU_BARS", SD.set_menu_bars),
                ("MENUS", SD.set_menus),
                ("MENU_ITEMS", SD.set_menu_items),
                ("WINDOWS", SD.set_windows),
                ("LINKS", SD.set_links),
            ]

            for component_name, set_function in components:
                if set_function(frame_id, self.CONTEXT):
                    print(f"{component_name} populated for `{frame_id}` app.")

        for frame_id in ["saskan", "admin"]:
            populate_components(frame_id)

        print("App data populated.")

    def boot_story_data(self):
        """
        Populate database tables for game, story, and world-building.
        N.B. - For now this includes some meaningless test data.
        Modify that to use TEST modules or various types of data INIT modules.
        :write: /db/SASKAN.db
        """
        if not self._populate_maps():
            print("Failed to populate maps.")
            return

        if not self._populate_grids():
            print("Failed to populate grids.")
            return

        if not self._populate_cross_maps():
            print("Failed to populate cross maps.")
            return

        if not self._populate_story_data():
            print("Failed to populate story data.")
            return

    def _populate_maps(self):
        """Populate map-related data."""
        try:
            if not SD.set_rect_maps(self.CONTEXT):
                return False
            if not SD.set_box_maps(self.CONTEXT):
                return False
            if not SD.set_sphere_maps(self.CONTEXT):
                return False
            print("MAPS populated.")
            return True
        except Exception as e:
            print(f"Error populating maps: {e}")
            return False

    def _populate_grids(self):
        """Populate grid-related data."""
        try:
            if not SD.set_grids(self.CONTEXT):
                return False
            if not SD.set_grid_cells(self.CONTEXT):
                return False
            if not SD.set_grid_infos(self.CONTEXT):
                return False
            print("GRIDS populated.")
            return True
        except Exception as e:
            print(f"Error populating grids: {e}")
            return False

    def _populate_cross_maps(self):
        """Populate cross-map related data."""
        try:
            if not SD.set_map_x_maps(self.CONTEXT):
                return False
            if not SD.set_grid_x_maps(self.CONTEXT):
                return False
            print("MAP_X_MAP and GRID_X_MAP populated.")
            return True
        except Exception as e:
            print(f"Error populating cross maps: {e}")
            return False

    def _populate_story_data(self):
        """Populate character sets and other story data."""
        try:
            if not SD.set_char_sets(self.CONTEXT):
                return False
            print("Story data populated.")
            return True
        except Exception as e:
            print(f"Error populating story data: {e}")
            return False


if __name__ == "__main__":
    BS = BootSaskan()
    BS.boot_saskan()
