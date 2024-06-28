#!python
"""Saskan Apps file installation procedure.
:module:    install_app.py
:class:     SaskanInstall/0
:author:    GM <genuinemerit @ pm.me>

(saskan) sudo ~/../Saskantinon/saskan_install
or from python terminal session:
- comment out the main() call.
- from saskan_install import SaskanInstall
- SI = SaskanInstall()

N.B.:
- If running from python terminal, it will request sudo password.
- If running from bash script, must run it under sudo account.

@DEV:
- If/when I get back to the service architecture...
- Prototype/test using haproxy to load balance servers.
- Simplify the proliferation of ports. I shouldn't need so many.
"""
import json

from os import path
from pprint import pprint as pp  # noqa: F401

from methods_shell import ShellMethods
from methods_files import FileMethods
from saskan_io.get_data import GetData
from saskan_io.set_data import SetData

SM = ShellMethods()
FM = FileMethods()
GD = GetData()
SD = SetData()


class InstallApp(object):
    """Configure and install Saskan apps.

    @DEV:
    - Create servers, clients, queues, load balancers and so on.
    """

    def __init__(self):
        """Initialize database, directories and files."""
        print("\n\nSaskan Installer tasks...")
        self.install_bootstrap_data()
        self.BOOT = self.get_bootstrap()
        self.DB_CFG = self.get_db_config()
        print("* Bootstrap data and basic app dirs installed.")
        self.install_database(self.DB_CFG)
        SD.set_app_config(self.DB_CFG)
        SD.set_texts(self.BOOT, self.DB_CFG)
        self.DIR = GD.get_app_config(self)
        self.verify_system_dirs()
        self.install_app_dirs()
        self.install_app_files()
        # NEXT: install other database tables,
        # using SetData / GetData calls. Probably
        # use json files from the git Schema directory
        # to do this in most cases. May be some opportunities
        # to use ChatGPT or other AI tools to automate some
        # of the work. Also experiment with using CLI
        # interfaces and maybe even GUI interfaces to drive
        # some of the story-telling aspects. Start with the
        # the most static stuff -- the GUI configuration data,
        # then move into the story-/world-building stuff.
        """
        Come back to service architecture later.
        It is interesting, but a big rabbit hole
         to go down!  When I'm ready, investigate
         using HAProxy to manage the service architecture.
        # self.set_ports()
        # self.save_svc_config()
        # self.create_load_bals()
        # self.install_load_bals()
        # self.start_servers(svc)
        # self.start_clients()
        # FM.pickle_saskan(self.APP)
        """

    # Helpers
    # ==============================================================

    # Bootstrap and database set-up
    # ==============================================================

    def install_bootstrap_data(self):
        """
        Create basic app directories if needed.
        Write bootstrap data to app directory.
        @DEV:
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
        FM.write_file(path.join(config_d, "b_bootstrap.json"), boot_j)

    def set_bootstrap(self) -> dict:
        """Read bootstap config data from APP config dir.
        :returns:
        - (dict) Bootstrap values as python dict else None.
        """
        cfg = dict()
        try:
            cfg = self.get_json_file(path.join(
                SM.get_cwd_home(),
                "saskan/config/b_bootstrap.json"))
            return cfg
        except Exception as err:
            print(err)
            return None

    def set_db_config(self) -> dict:
        """Set the database configuration from bootstrap data.
        :returns:
        - (dict) DB config values as python dict else None."""
        cfg = dict()
        try:
            cfg["sql"] = path.join(SM.get_cwd_home(),
                                   self.BOOT['app_dir'],
                                   self.BOOT['db_dir'])
            cfg["main_db"] = path.join(cfg["sql"], self.BOOT['main_db'])
            cfg["version"] = self.BOOT['db_version']
            cfg["bkup_db"] = path.join(cfg["sql"], self.BOOT['bkup_db'])
            return cfg
        except Exception as err:
            print(err)
            return None

    def install_database(self):
        """Copy SQL files to app sql directory.
        This will delete any existing copies of the SQL files and
          database and replace with new ones.
        """
        from database import DataBase
        DB = DataBase(self.DB_CFG)
        from io_data import InitGameDB
        IGDB = InitGameDB()
        IGDB.create_sql(DB)
        IGDB.boot_db(DB)
        print("* Database installed.")

    def verify_system_dirs(self):
        """Verify standard bash directory exists.
        - /usr/local/bin
        Verify standard in-memory directory exists.
        - /dev/shm
        :args:
        - FI: current instance of FileIO class.
        """
        for sys_dir in ("bin_dir", "mem_dir"):
            files = FM.scan_dir(FM.DIR[sys_dir])
            if files in ([], None):
                txt = GetData.get_text("en", "err_file")
                raise Exception(f"{txt} {FM.DIR[sys_dir]}")
        print("* System directories verified.")

    def install_app_dirs(self):
        """Create remaining app directories.
        In case they already exist, clean them out.
        :args:
        - FI: current instance of FileIO class.
        """
        def _wipe_and_remove():
            a_files = FM.scan_dir(app_dir)
            if a_files is not None:
                # wipe and remove if already exists
                a_files += "/*"
                txt = GetData.get_text("en", "err_process")
                ok, result = SM.run_cmd([f"sudo rm -rf {a_files}"])
                if not ok:
                    raise Exception(f"{txt} {result}")
                ok, result = SM.run_cmd([f"sudo rmdir {app_dir}"])
                if not ok:
                    raise Exception(f"{txt} {result}")

        for a_dir in ('dat_dir', 'dbg_dat', 'img_dir',
                      'log_dat', 'mon_dat', 'py_dir', 'sch_dir'):
            app_dir = path.join(FM.DIR['root_dir'], FM.DIR[a_dir])
            _wipe_and_remove()
            FM.make_dir(app_dir)
            FM.make_executable(app_dir)
            FM.make_executable(app_dir)
            FM.make_writable(app_dir)
        print("* Other app directories installed.")

    def install_app_files(self,):
        """Copy app files to app directory.
        For python files, don't copy the install module.
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
                "_install" not in str(f)
            ]
            if py_files is not None:
                for f in py_files:
                    FM.copy_one_file(f, app_dir)

        git_dir = path.join(self.BOOT['git_source'], "html")
        app_dir = path.join(self.DIR['root_dir'], self.DIR['dat_dir'])
        _copy_files()
        git_dir = path.join(self.BOOT['git_source'], "images")
        app_dir = path.join(self.DIR['root_dir'], self.DIR['img_dir'])
        _copy_files()
        git_dir = self.BOOT['git_source']
        app_dir = path.join(self.DIR['root_dir'], self.DIR['py_dir'])
        _copy_python_files()
        print("* App files installed.")


if __name__ == "__main__":
    SI = InstallApp()
