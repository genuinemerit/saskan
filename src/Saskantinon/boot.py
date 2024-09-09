#!python
"""Saskan Apps file installation procedure.
:module:    boot.py
:class:     SaskanBoot/0
:author:    GM <genuinemerit @ pm.me>

Configure and boot databases.
Run "boot.py" to create, initialize databases.
Use methods to locate them.

From project directory if Makefile is being used:
- make boot

From project directory:
- mamba activate saskan
- python src/Saskantinon/boot.py

Assume that python programs are always executed from the
main project directory. Manage any paths with that in mind.

@DEV:
- Data-driven. Creates DBs and writes to databases.
- The sqlite database files and SQL DML files should be stored in the
  PyPI package, but DDL files and JSON config files can be excluded.
- When I get back to the service architecture...
    - Prototype/test using haproxy to load balance servers.
    - Simplify the proliferation of ports. Shouldn't need so many.
"""
import json
from pprint import pprint as pp  # noqa: F401

from data_base import DataBase
from data_model import DataModel

# from data_set import SetData
from method_files import FileMethods

FM = FileMethods()
# SD = SetData()


class BootSaskan(object):
    """Configure and boot Saskantinon and Saskantinize.
    (Re-)generate SQL files.
    (Re-)create and populate database(s).

    @DEV:
    - Organize things neatly. Think functionally.
    - Use data and params to drive similar functions.
    - Later, create servers, clients, queues, load balancers and so on.
    - If there is anything that needs to happen unique to a local machine,
      then it doesn't belong here; rather in a StartUp class.
    - Next, more work with maps and grids
    - Then, Actors and Scenes
    """

    def __init__(self):
        """
        - Initialize database and load tables.
        - Set-up dimensions and structure of widgets, API's.
        - Apps GUI data...
        -   Maybe consider doing this in a separate class, or having
            variations for different platforms.
        -   For now, I only have a single algorithm for configuring
        -   the GUI components, but eventually that may change.
        - Load base data for world-building and story-telling.
        """
        self.STATIC_CONTEXT = "static/context/context.json"
        self.BOOT = self.boot_context()
        DM = DataModel()
        DB = DataBase(self.BOOT)
        DM.create_sql(DB)
        print("* DDL and DML SQL (re-)generateed.")
        DM.create_db(DB)
        print("* Databases (re-)generated.")
        """
        # Database Set-up
        frame_id = "saskan"
        SD.set_frames(frame_id, self.BOOT, self.DB_CFG)
        SD.set_menu_bars(frame_id, self.BOOT, self.DB_CFG)
        SD.set_menus(frame_id, self.BOOT, self.DB_CFG)
        SD.set_menu_items(frame_id, self.BOOT, self.DB_CFG)
        SD.set_windows(frame_id, self.BOOT, self.DB_CFG)
        SD.set_links(frame_id, self.BOOT, self.DB_CFG)
        # Game World data
        SD.set_maps(self.DB_CFG)
        SD.set_grids(self.DB_CFG)
        """

    def boot_context(self):
        """
        (Re-)create static context (boot) data file.
        This allows us to bootstrap the database and provides
        a way to recreate the context file if it is deleted.
        :writes: /static/context/context.json
        :returns: dict of context data
        """
        print("Context file (re-)generated.")
        boot: dict = {
            "db": "db",
            "ddl": "boot/ddl",
            "dml": "db/dml",
            "git": "https://github.com/genuinemerit/saskan-app/",
            "lang": "en",
            "saskan_db": "db/SASKAN.db",
            "saskan_bak": "db/SASKAN.bak",
            "wiki": "https://github.com/genuinemerit/saskan-wiki/",
        }
        FM.write_file(self.STATIC_CONTEXT, json.dumps(boot))
        return boot


if __name__ == "__main__":
    AI = BootSaskan()
