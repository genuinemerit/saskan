#!python

"""File utilities.

module:    method_configs.py
class:     ConfigMethods/0
author:    GM <genuinemerit @ pm.me>
"""

from os import path
from pprint import pprint as pp  # noqa: F401

from methods_shell import ShellMethods
from io_get_data import GetData

SM = ShellMethods()
GD = GetData()


class ConfigMethods(object):
    """Config IO utilities.
    """

    def __init__(self):
        """Initialize FileIO object.
        """
        self.BOOT = self.get_bootstrap()
        self.DB_CFG = self.get_db_config()
        self.DIR = GD.get_app_config(self)

    def get_bootstrap(self) -> dict:
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

    def get_db_config(self) -> dict:
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
