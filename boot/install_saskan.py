#!python
"""Saskan Apps file installation procedure.
:module:    install_saskan.py
:class:     SaskanInstall/0
:author:    GM <genuinemerit @ pm.me>

Command line installer.
From local git repo, Saskantinon directory:
- mamba activate sasaken
- python install_saskan.py

@DEV:
- Refactor to install only 'saskan' components
- Maybe install 'saskantinize' separately, but like
  it is a plug-in, sort of, for saskan. In other words,
  they can use the same directories and database, but
  have different configs, data records, GUI components,
  and maybe a few other things.

  I think one install program, with distinct config
  inputs makes more sense.

- If/when I get back to the service architecture...
- Prototype/test using haproxy to load balance servers.
- Simplify the proliferation of ports. I shouldn't need so many.
- Execute this is as part of install in Makefile:
  `make install_saskantinon`?

- Do we just combine the pip install and the local
  app configuration steps into one make action? Yes,
  I think so, though make it be available to break it into
  sub-steps. Should not need to require the user to
  run steps other than pip install, if possible.
  Not sure. Feels like a chicken and egg problem.

  Is it an option to generate the database and store it
  as part of the PyPI package? How about storing the DB
  and other (non-python) resources on GitHub (or elsewhere)
  and then have the program pull them down from there if
  they are not present locally?

  Yes, see: https://www.turing.com/kb/7-ways-to-include-non-python-files-into-python-package
  I think we generate the database and store it as part of the PyPI package,
  but as an included file. Same with docs and other non-python resoources.
  We can also have a make action that pulls the resources from GitHub if desired.
  Presumably they will all be deployed in a manner consistent with the dev project?

  This implies that the config files and database constructor are part of the
  development project, but not part of the PyPI package. See manifest.in file.
  See in the dist folder, how the docs are included at the level above the python app
  folders. Presumably I can access them using `../` in the path.
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


class SaskanInstall(object):
    """Configure and install Saskan apps.

    @DEV:
    - Create servers, clients, queues, load balancers and so on.
    """

    def __init__(self):
        """Initialize database, directories and files.
        Then set-up dimensions and structure of apps, api's.
        Finally, load data for world-buidling and story-telling.

        # May be some opportunities to use AI tools.
        # Experiment with using CLI interfaces and
        #   GUI interfaces to drive story-telling.
        # Start with static app config data, then work on
        #   world-building stuff.
        #
        # Next -- basic futzing with maps and grids
        # Then -- some implementations of scenes
        # At some point, take a break to consider data
        #  structures for Actors and Scenes
        #
        # Come back to service architecture later.
        # It is interesting, but a big rabbit hole
        #  to go down!  When I'm ready, investigate
        #  using HAProxy to manage the service architecture.
        """
        # Environment Set-up
        self.install_bootstrap_data()
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
        # Apps GUI data
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

    def install_bootstrap_data(self):
        """
        Create basic app directories if needed.
        Write bootstrap data to app directory.
        """
        boot_data: dict = {
            "app_dir": "saskan",
            "db_dir": "sql",
            "db_version": "0.1",
            "git_source": "/home/dave/Dropbox/GitHub/saskan-app/Saskantinon",
            "language": "en",
            "main_db": "SASKAN.db",
            "bkup_db": "SASKAN.bak",
        }
        boot_j = json.dumps(boot_data)
        app_d = path.join(SM.get_cwd_home(), boot_data["app_dir"])
        config_d = path.join(app_d, "config")
        sql_d = path.join(app_d, "sql")
        FM.make_dir(app_d)
        FM.make_dir(config_d)
        FM.make_dir(sql_d)
        FM.write_file(path.join(config_d, "bootstrap.json"), boot_j)
        print("* Bootstrap file created.")

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
                f for f in files if str(f).endswith(".py") and "install" not in str(f)
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
    AI = SaskanInstall()
