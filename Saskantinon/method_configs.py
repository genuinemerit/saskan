#!python

"""File utilities.

module:    method_configs.py
class:     ConfigMethods/0
author:    GM <genuinemerit @ pm.me>
"""

from os import path
from pprint import pprint as pp  # noqa: F401

from method_shell import ShellMethods
from method_files import FileMethods

SM = ShellMethods()
FM = FileMethods()


class ConfigMethods(object):
    """Config IO utilities.
    """

    def __init__(self):
        """Initialize FileIO object.
        """
        self.BOOT = self.set_bootstrap()
        self.DB_CFG = self.set_db_config()

    def get_configs(self) -> tuple:
        """Get configs from bootstrap file.
        :returns:
        - (tuple) Bootstrap and DB config values.
        """
        return (self.BOOT, self.DB_CFG)

    def set_bootstrap(self) -> dict:
        """Set bootstap config data from APP config dir.
        :returns:
        - (dict) Bootstrap values as python dict else None.
        """
        cfg = dict()
        try:
            cfg = FM.get_json_file(path.join(
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
