#!python
"""Saskan Apps file installation procedure.
:module:    app_install.py
:class:     InstallApp/0
:author:    GM <genuinemerit @ pm.me>

Command line installer.
From local git repo, Saskantinon directory:
- mamba activate sasaken
- python install_app.py

@DEV:
- If/when I get back to the service architecture...
- Prototype/test using haproxy to load balance servers.
- Simplify the proliferation of ports. I shouldn't need so many.
"""
import json

from os import path
from pprint import pprint as pp  # noqa: F401

from method_configs import ConfigMethods
from method_shell import ShellMethods
from method_files import FileMethods
from data_get import GetData
from data_set import SetData
from data_base import DataBase
from data_model_app import AppConfig
from data_model_tool import InitGameDB

AC = AppConfig()
CM = ConfigMethods()
SM = ShellMethods()
FM = FileMethods()
GD = GetData()
SD = SetData()


class AppInstall(object):
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
        # Come back to service architecture later.
        # It is interesting, but a big rabbit hole
        #  to go down!  When I'm ready, investigate
        #  using HAProxy to manage the service architecture.
        # self.set_ports()
        # self.save_svc_config()
        # self.create_load_bals()
        # self.install_load_bals()
        # self.start_servers(svc)
        # self.start_clients()
        # FM.pickle_saskan(self.APP)
        """
        # Environment Set-up
        print("\n\nSaskan Installer tasks\n=================")
        self.install_bootstrap_data()
        self.BOOT, self.DB_CFG = CM.get_configs()
        print("* Bootstrap and DB config metadata defined:")
        pp((self.BOOT, self.DB_CFG))
        self.install_database()
        SD.set_app_config(self.DB_CFG)
        SD.set_texts(self.BOOT, self.DB_CFG)
        self.DIR = GD.get_app_config(self.DB_CFG)
        self.verify_system_dirs()
        self.install_app_dirs()
        self.install_app_files()

        # Apps GUI Set-up
        SD.set_frames(self.BOOT, self.DB_CFG)
        SD.set_menu_bars(self.BOOT, self.DB_CFG)
        SD.set_menus(self.BOOT, self.DB_CFG)
        SD.set_menu_items(self.BOOT, self.DB_CFG)
        SD.set_windows(self.BOOT, self.DB_CFG)
        SD.set_links(self.BOOT, self.DB_CFG)

    def install_bootstrap_data(self):
        """
        Create basic app directories if needed.
        Write bootstrap data to app directory.
        @DEV:
        - Should probably make this a git repo file.
        - It would be interesting to see if I can pull in the
          installable files directly from GitHub.
        - Make some of these values param inputs:
            - db_version
            - git_source
            - language
        """
        boot_data: dict = {
            "app_dir": "saskan",
            "db_dir": "sql",
            "db_version": "0.1",
            # "git_source": "https://github.com/genuinemerit/Saskantinon",
            "git_source": "/home/dave/Dropbox/GitHub/saskan-app/Saskantinon",
            "language": "en",
            "main_db": "SASKAN.db",
            "bkup_db": "SASKAN.bak"}
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

        a_dirs = [d for d in list(AC.to_dict()['APP_CONFIG'].keys())
                  if '_dir' in d and d not in ['mem_dir', 'root_dir']]
        for d in a_dirs:
            app_dir = path.join(self.DIR['root_dir'], self.DIR[d])
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
                f for f in files if str(f).endswith(".py") and
                "install" not in str(f)
            ]
            if py_files is not None:
                for f in py_files:
                    FM.copy_one_file(f, app_dir)

        git_dir = path.join(self.BOOT['git_source'], "html")
        app_dir = path.join(self.DIR['root_dir'], self.DIR['html_dir'])
        _copy_files()
        git_dir = path.join(self.BOOT['git_source'], "images")
        app_dir = path.join(self.DIR['root_dir'], self.DIR['img_dir'])
        _copy_files()
        git_dir = self.BOOT['git_source']
        app_dir = path.join(self.DIR['root_dir'], self.DIR['py_dir'])
        _copy_python_files()
        print("* App files installed.")


if __name__ == "__main__":
    AI = AppInstall()
