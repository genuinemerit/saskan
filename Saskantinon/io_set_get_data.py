"""

:module:    io_set_get_data.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

# import json
# import pendulum     # date and time
# import random
# import string

# from os import path
from collections import OrderedDict
# from pathlib import Path
from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401
# from typing import Tuple, Union

from io_db import DataBase
# For data models, import specific ones
# per need. For example, when setting or getting
# records relating to config data, import the
# io_data classes like AppConfig, Texts, Frames
# and so on
# When reading data from the DB, there are two
# layers to consider:
# 1. Pull records in and filtering them; this is
#    done using io_db and io_data classes.
# 2. Translate into object formats when needed
#    to be used in the app; in this case, will
#    import io_data classes like GamePlane and Struct
from io_shell import ShellIO

DB = DataBase()
SI = ShellIO()


class ComputeData(object):
    """
    Provide methods for setting data as the result of
    calculations, algorithms or AI calls.
    """
    def __init__(self):
        """
        Initialize a new instance of the ComputeData class.
        """
        pass


class SetDBData(object):
    """
    Provide methods for setting data in the database
    based on inputs.
    Until there is a front-end for editing Db content,
    this module will support:
    1. Hard-coded set-up methods (no inputs)
    2. Read inputs as call parameters
    3. Read from files
    4. Read inputs from terminal
    """
    def __init__(self):
        """
        Initialize a new instance of the GetData class.
        """
        pass

    def set_app_config(self,
                       p_return: bool = False):
        """
        Set data on the AppConfig table.
        @DEV:
        - Set the Config file to contain only the UID or maybe
          the version ID (or both)?
        - Hmmm... bootstrap will need to know where the DB is,
          so don't really need anything else except maybe some
          version numbers?
        """
        sql = 'INSERT_APP_CONFIG'
        from io_data import AppConfig
        AC = AppConfig()
        data = OrderedDict(AC.to_dict()['APP_CONFIG'])
        data['config_uid_pk'] = SI.get_uid()
        data['version_id'] = 0
        data['root_dir'] = "/home/dave/saskan"
        data['bin_dir'] = "/usr/local/bin"
        data['mem_dir'] = "/dev/shm"
        data['cfg_dir'] = "config"
        data['dat_dir'] = "data"
        data['img_dir'] = "images"
        data['py_dir'] = "python"
        data['db_dir'] = "sql"
        data['sch_dir'] = "schema"
        data['log_dat'] = "saskan_log"
        data['mon_dat'] = "saskan_mon"
        data['dbg_dat'] = "saskan_dbg"
        DB.execute_insert(sql, tuple(data.values()))
        if p_return:
            GET = GetDBData()
            return GET.get_app_config(data['config_uid_pk'])
        else:
            return None


class GetDBData(object):
    """
    Provide methods for reading data from the database.
    Generic DB IO methods are in the io_db module.
    These methods are specifcally associated with data
    models defined in the io_data module. It may also be
    useful to either define views in SQLlite or to use
    this class to effectively create views.
    """
    def __init__(self):
        """
        Initialize a new instance of the GetData class.
        """
        pass

    def get_app_config(self,
                       p_config_uid: str):
        """
        Get data from the AppConfig table.
        """
        sql = 'SELECT_BY_PK_APP_CONFIG'
        app_config_data = DB.execute_select_by(sql, [p_config_uid])
        return app_config_data
