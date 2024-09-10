#!python
"""Saskan Apps file installation procedure.
:module:    boot.py
:class:     SaskanBoot/0
:author:    GM <genuinemerit @ pm.me>

Create SQL, databases and populate with base app and story data.
N.B. - Python modules are executed from project directory.
       Manage paths with that in mind.

@DEV:
- When I get back to the service architecture...
    - Prototype/test using haproxy to load balance servers.
    - Reduce proliferation of ports. Shouldn't need that many.
"""
import json
from pprint import pprint as pp  # noqa: F401

from data_base import DataBase
from data_model import DataModel

from data_set import SetData
from method_files import FileMethods

FM = FileMethods()
SD = SetData()


class BootSaskan(object):
    """Configure and boot Saskantinon and Saskantinize.
    (Re-)generate SQL files.
    (Re-)create and populate database(s).
    """

    def __init__(self):
        """
        - Initialize database and load tables.
        - Load base data for frames, widgets, buttons, API's.
        - Load base data for world-building and story-telling.
        """
        self.CONTEXT_FILE_PATH = "static/context/context.json"
        self.CONTEXT = self.boot_context()
        self.DB = DataBase(self.CONTEXT)

    def boot_saskan(self):
        self.boot_database()
        self.boot_app_data()
        # self.boot_story_data()

    def boot_context(self):
        """
        (Re-)create static context data file.
        This allows us to bootstrap the database and recreate
        the context file in case it got deleted.
        :writes: /static/context/context.json
        :returns: dict of context data
        """
        context: dict = {
            "cfg": {},
            "db": "db",
            "ddl": "boot/ddl",
            "dml": "db/dml",
            "git": "https://github.com/genuinemerit/saskan-app/",
            "lang": "en",
            "saskan_db": "db/SASKAN.db",
            "saskan_bak": "db/SASKAN.bak",
            "wiki": "https://github.com/genuinemerit/saskan-wiki/",
        }
        for cfg in ["frames", "links", "menus", "texts",
                    "widgets", "windows"]:
            context["cfg"][cfg] = "boot/config/" + cfg + ".json"
        FM.write_file(self.CONTEXT_FILE_PATH, json.dumps(context))
        return context

    def boot_database(self):
        """
        Create SQL files and SQLite3 database.
        :write:  /boot/ddl/*.sql and /db/dml/*.sql
        :writes: /db/SASKAN.db and /db/SASKAN.bak
        """
        DM = DataModel()
        DM.create_db(self.DB)
        print("Database (backed up and re-)created.")
        DM.create_sql(self.DB)
        print("SQL files (re-)generated.")

    def boot_app_data(self):
        """
        Populate database tables for GUI, API's, etc.
        :write:  /db/SASKAN.db
        """
        SD.set_frames("saskan", self.CONTEXT)
        SD.set_frames("admin", self.CONTEXT)
        SD.set_texts(self.CONTEXT)
        SD.set_menu_bars("saskan", self.CONTEXT)
        SD.set_menu_bars("admin", self.CONTEXT)
        """
        SD.set_menus(frame_id, self.CONTEXT, self.DB_CFG)
        SD.set_menu_items(frame_id, self.CONTEXT, self.DB_CFG)
        SD.set_windows(frame_id, self.CONTEXT, self.DB_CFG)
        SD.set_links(frame_id, self.CONTEXT, self.DB_CFG)
        """
        print("App data populated.")

    def boot_story_data(self):
        """
        Populate database tables for game, story, world-building.
        :write:  /db/SASKAN.db
        """
        SD.set_maps(self.DB_CFG)
        SD.set_grids(self.DB_CFG)
        print("Story data populated.")


if __name__ == "__main__":
    BS = BootSaskan()
    BS.boot_saskan()
