#!python
"""Saskan Apps file installation procedure.
:module:    boot_saskan.py
:class:     SaskanBoot/0
:author:    GM <genuinemerit @ pm.me>

Configure and boot Saskantinon and Saskantinize databases.
Development project only. Not part of installed package.

From project directory if Makefile is being used:
- make boot

From project directory:
- mamba activate saskan
- python src/Saskantinon/boot_saskan.py

Assume that python programs are always executed from the
main project directory. Manage any paths with that in mind.

@DEV:
- One install program, with distinct config inputs & params for
  the two apps. This is data-driven and writes only to the database.
-  Config files and database constructor modules like this one are
   part of the project, but exclude them from the PyPI package.

- Regarding packaging and distribution:
  The database and SQL DML files can be stored in the PyPI package.
  Could also store the DB and other non-python resources on GitHub
  or elsewhere and then have the program pull them down from there if
  they are not present locally.

  Need to get clear on how to refresh files on PyPI with a release.

  See: https://www.turing.com/kb/7-ways-to-include-non-python-files-into-python-package  # noqa E501
    Can def generate the database and store it as part of the PyPI package,
  as an included file. Like with docs and other non-python resoources.
  We can make actions to pulls the resources from GitHub if desired.
  Presumably all will be deployed in a manner consistent with the project, e.,g under
  the /db directory in the project-level directory.
  See manifest.in file. See dist folder, how the docs are included at the
  level above the python src folders. Access them using `../` in the path
  from the python programs?

- When I get back to the service architecture...
- Prototype/test using haproxy to load balance servers.
- Simplify the proliferation of ports. Shouldn't need so many.
"""
import json
from os import path
from pprint import pprint as pp  # noqa: F401

from data_base import DataBase
from data_get import GetData
from data_model_app import AppConfig
from data_model_tool import InitGameDB
from data_set import SetData
from method_configs import ConfigMethods
from method_files import FileMethods
from method_shell import ShellMethods

AC = AppConfig()
CM = ConfigMethods()
SM = ShellMethods()
FM = FileMethods()
GD = GetData()
SD = SetData()


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

        - Next -- basic futzing with maps and grids
        - Then -- some implementations of scenes
        - Consider data structures for Actors and Scenes
        - Come back to service architecture later.
        - It is interesting, but a big rabbit hole!
        - Look at HAProxy to manage service architecture.
    - It may work better to include the "boot" resources under the
      Saskantinon directory, but exclude them from the PyPI package.
    """

    def __init__(self):
        """
        - Initialize database and load tables.
        - Load data for world-buidling and story-telling.
        - Set-up dimensions and structure of widgets, API's.
        - "Environment" set up:
        -   This is no longer a good idea.
        -   The user runtime will be the same for all users.
        -   It should be under user space, not 'sudo' so that
            the user can run the program as a non-root user and
            database, possilby other files, can be updated.
        - Don't want to configure a special directory structure
            that is any different from what is delivered from PyPI.
        - Apps GUI data...
        -   Consider doing this in a separate class.
        -   For now, I only have a single algorithm for configuring
        -   the GUI components, but eventually that may change based
        -   on the local environment.  In either case, it might be
        -   cleaner to have a separate class for GUI configuration.
        """
        # Environment Set-up
        self.boot_context()
        """
        self.BOOT, self.DB_CFG = CM.get_configs()
        self.install_database()
        SD.set_app_config(self.DB_CFG)
        SD.set_texts(self.BOOT, self.DB_CFG)
        self.DIR = GD.get_app_config(self.DB_CFG)
        self.verify_system_dirs()
        self.install_app_dirs()
        self.install_app_files()
        # Save DB_CFG to a file.
        self.save_db_config(self.BOOT, self.DB_CFG)

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
        Create context data to /db folder.
        """
        context_data: dict = {
            "admin_db": "ADMIN.db",
            "cfg": "boot/config",
            "db": "db",
            "ddl": "boot/ddl",
            "dml": "db/dml",
            "git": "https://github.com/genuinemerit/saskan-app/",
            "lang": "en",
            "saskan_db": "SASKAN.db",
            "wiki": "https://github.com/genuinemerit/saskan-wiki/",
        }
        context_j = json.dumps(context_data)
        # app_d = path.join(SM.get_cwd_home(), context_data["app_dir"])
        # config_d = path.join(app_d, "config")
        # sql_d = path.join(app_d, "sql")
        # FM.make_dir(app_d)
        # FM.make_dir(config_d)
        # FM.make_dir(sql_d)
        pp(("context json:", context_j))
        print(f"Current working directory: {SM.get_cwd()}")
        context_f = path.join("static/context", "context.json")
        FM.write_file(context_f, context_j)
        print(f"* Context file created: {context_f}")

    def install_database(self):
        """Copy SQL files to app sql directory.
        This will delete any existing copies of the SQL files and
          database and replace with new ones.
        """
        DB = DataBase(self.DB_CFG)
        IGDB = InitGameDB()
        IGDB.create_sql(DB)
        IGDB.boot_db(DB)
        print("* Database installed.")

    def verify_system_dirs(self):
        """
        Verify standard in-memory directory exists.
        - /dev/shm
        """
        for sys_dir in ["mem_dir"]:
            files = FM.scan_dir(self.DIR[sys_dir])
            if files in ([], None):
                txt = GD.get_text("en", "err_file", self.DB_CFG)
                raise Exception(f"{txt} {self.DIR[sys_dir]}")
        print("* System directories verified.")

    def install_app_dirs(self):
        """Create remaining app directories.
        In case they already exist, clean them out.
        """

        def _wipe_and_remove():
            a_files = FM.scan_dir(app_dir)
            if a_files is not None:
                # wipe and remove if already exists
                a_files += "/*"
                txt = GD.get_text("en", "err_process", self.DB_CFG)
                ok, result = SM.run_cmd([f"sudo rm -rf {a_files}"])
                if not ok:
                    raise Exception(f"{txt} {result}")
                ok, result = SM.run_cmd([f"sudo rmdir {app_dir}"])
                if not ok:
                    raise Exception(f"{txt} {result}")

        a_dirs = [
            d
            for d in list(AC.to_dict()["APP_CONFIG"].keys())
            if "_dir" in d and d not in ["mem_dir", "root_dir"]
        ]
        for d in a_dirs:
            app_dir = path.join(self.DIR["root_dir"], self.DIR[d])
            _wipe_and_remove()
            FM.make_dir(app_dir)
            FM.make_executable(app_dir)
            FM.make_executable(app_dir)
            FM.make_writable(app_dir)
        print("* Other app directories installed.")

    def install_app_files(self):
        """Copy app files to app directory.
        For python files, don't copy the install modules.
        """

        def _copy_files():
            files = FM.scan_dir(git_dir)
            if files is not None:
                for f in files:
                    FM.copy_one_file(f, app_dir)

        def _copy_python_files():
            files = FM.scan_dir(git_dir)
            py_files = [
                f for f in files if str(f).endswith(".py")
                and "install" not in str(f)
            ]
            if py_files is not None:
                for f in py_files:
                    FM.copy_one_file(f, app_dir)

        git_dir = path.join(self.BOOT["git_source"], "html")
        app_dir = path.join(self.DIR["root_dir"], self.DIR["html_dir"])
        _copy_files()
        git_dir = path.join(self.BOOT["git_source"], "images")
        app_dir = path.join(self.DIR["root_dir"], self.DIR["img_dir"])
        _copy_files()
        git_dir = self.BOOT["git_source"]
        app_dir = path.join(self.DIR["root_dir"], self.DIR["py_dir"])
        _copy_python_files()
        print("* App files installed.")

    def save_db_config(self, BOOT: dict, DB_CFG: dict):
        """Save database configuration to app config file."""
        db_cfg_j = json.dumps(DB_CFG)
        cfg_d = path.join(SM.get_cwd_home(), BOOT["app_dir"], "config")
        FM.write_file(path.join(cfg_d, "db_config.json"), db_cfg_j)
        print("* DB config file created.")


if __name__ == "__main__":
    AI = BootSaskan()
