"""

:module:    data_model.py
:author:    GM (genuinemerit @ pm.me)

Data Management middleware.
"""

from collections import OrderedDict
from pathlib import Path
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

import data_model_app as DMA
import data_model_world as DMW
from method_files import FileMethods
from method_shell import ShellMethods

FM = FileMethods()
SM = ShellMethods()

# =============================================================
# DB/DM table definitions
#
# The data models are used to create SQLITE tables and
#   standard/generic SQL commands (INSERT, UPDATE, SELECT).
# All fields must have a default value.
# A sub-class identifies:
# - SQLITE constraints,
# - GROUPed types derived from data types defined above,
# - sort order for SELECT queries.
# This module provides the generic tools for running DDL commands.
#
# Moved test data set-up methods into a separate module,
# under the test directory.
#
# @DEV:
# Define database tables to store name, location, other info
# regarding image, video, sound and possibly other types of resources
# (plug-ins, mods, external services, etc.).
# Also regions, countries, provinces, cities, towns, villages, scenes, etc.
# May want to break this module up into data categories.
# =======================================================


# =============================================================
# Abstracted methods for Data Model objects
# =============================================================
def orm_to_dict(DM: object) -> dict:
    """Convert data model object to an OrderedDict.
    Returned attributes order will match SQL order in the database.
    :args:
    - DM object
    """
    all_vars = OrderedDict(vars(DM))
    public_vars = OrderedDict(
        {
            k: v
            for k, v in all_vars.items()
            if not k.startswith("_")
            and k not in ("Constraints", "to_dict", "from_dict")
        }
    )
    return {all_vars["_tablename"]: public_vars}


def orm_from_dict(DM: object, p_dict: dict, p_row: int) -> dict:
    """
    Load DB SELECT results into memory.
    Set data model attributes from dict of listed values
    and return a regular dict with populated values.
    :args:
    - DM - instantiatd data model object
    - p_dict: dict of lists of values
    - p_row: row number of the lists of values to use
    """
    batch_rec = {
        k: v
        for k, v in dict(DM.to_dict()[DM._tablename]).items()
        if k not in ("_tablename", "to_dict", "from_dict")
    }
    for k, v in batch_rec.items():
        setattr(DM._tablename, k, p_dict[k][p_row])
        batch_rec[k] = getattr(DM._tablename, k)
    return batch_rec


# =======================================================
# DB/DM Calls
# - Create SQL files
# - Create SQLITE tables
# =======================================================
class DataModel(object):
    """Methods to:
    - Create set of SQL files to manage the game database.
    - Boot the database by running the SQL files.
    More:
      - roads
      - paths
      - trails
      - sea lanes
      - mountains
      - hills
      - mines
      - quarries
      - caverns
      - forests
      - undersea domains
      - populations
      - belief systems
      - countries (over time...)
      - federations
      - provinces
      - towns
      - counties, cantons and departments
      - towns
      - villages
      - estates and communes
      - tribal lands
      - neighborhoods and precincts
      - farms and fields
      - ruins
      - temples
      - scenes
      - buildingsmountains, spacecraft, buildings, etc.
    """

    def __init__(self):
        """Initialize the InitGameDatabase object."""
        pass

    def create_sql(self, DB: object):
        """Pass data object to create SQL files.
        :args:
        - DB - current instance of the DB object.
        """
        # data_model_app
        for model in [
            DMA.Backup,
            DMA.AppConfig,
            DMA.Texts,
            DMA.Frames,
            DMA.MenuBars,
            DMA.Menus,
            DMA.MenuItems,
            DMA.Windows,
            DMA.Links,
            DMA.ButtonSingle,
            DMA.ButtonMulti,
            DMA.ButtonItem,
        ]:
            DB.generate_sql(model)
        # data_model_world
        for model in [
            DMW.Universe,
            DMW.ExternalUniv,
            DMW.GalacticCluster,
            DMW.Galaxy,
            DMW.StarSystem,
            DMW.World,
            DMW.Moon,
            DMW.Map,
            DMW.MapXMap,
            DMW.Grid,
            DMW.GridXMap,
            DMW.CharSet,
            DMW.CharMember,
            DMW.LangFamily,
            DMW.Language,
            DMW.LangDialect,
            DMW.GlossCommon,
            DMW.Glossary,
            DMW.Lake,
            DMW.LakeXMap,
            DMW.River,
            DMW.RiverXMap,
            DMW.OceanBody,
            DMW.OceanBodyXMap,
            DMW.OceanBodyXRiver,
            DMW.LandBody,
            DMW.LandBodyXMap,
            DMW.LandBodyXLandBody,
            DMW.LandBodyXOceanBody,
            DMW.SolarYear,
            DMW.Season,
            DMW.LunarYear,
            DMW.LunarYearXMoon,
            DMW.SolarCalendar,
            DMW.LunarCalendar,
            DMW.Month,
            DMW.LunarCalendarXMonth,
            DMW.SolarCalendarXMonth,
            DMW.WeekTime,
            DMW.LunarCalendarXWeekTime,
            DMW.SolarCalendarXWeekTime,
            DMW.DayTime,
            DMW.WeekTimeXDayTime,
        ]:
            DB.generate_sql(model)

    def create_db(
        self,
        DB: object,
        p_backup: bool = True,
    ):
        """
        Drop and recreate empty all DB tables.
        This is a destructive operation.
        - Backs up and archives DB if it exists.
        - Always makes a new .ARCV file.
        - Overlays existing .BAK if it exists.
        - Does not wipe out existing archived DB's.
        - Logged records appear in .BAK, not in refreshed .DB
        :args:
        - DB - instantiation of the DataBase() Class.
        - p_backup: bool. If True, backup and archive the .DB

        @DEV:
        - See test/test_data_model_tool.py for examples of
            populating test data.
        """
        if p_backup:
            file_path = Path(DB.SASKAN_DB)
            if file_path.exists():
                DB.backup_db(DB.SASKAN_DB, DB.SASKAN_BAK)
                DB.archive_db(DB.SASKAN_DB)

        sql_list = [sql.name for sql in FM.scan_dir(DB.DDL, "DROP*")]
        DB.execute_ddl(sql_list, p_foreign_keys_on=False)
        sql_list = [sql.name for sql in FM.scan_dir(DB.DDL, "CREATE*")]
        DB.execute_ddl(sql_list, p_foreign_keys_on=True)
