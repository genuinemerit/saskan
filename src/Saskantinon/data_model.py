"""

:module:    data_model.py
:author:    GM (genuinemerit @ pm.me)

Data Management middleware.
Standalone methods. No class object is defined.

=============================================================
DB/DM table definitions

Data models are used to create SQLITE tables and
standard/generic SQL commands (INSERT, UPDATE, SELECT).
See:
- data_model_app.py: for application widgets data.
- data_model_story.py: for story/game/scenario data.
All fields must have a default value.

A sub-class identifies:
- SQLITE constraints, e.g. PRIMARY KEY, FOREIGN KEY, CHECKs
- Sort order for SELECT queries.

This module provides standalone methods for creating SQL files and running
DDL commands to create the tables in the database.
It also provides translators for displaying SQL results or
column names as a full dictionary, rather than as a dict of lists,
which is the default data structure returned by SELECT scripts.

# @DEV:
# Define database tables to store name, location, other info
# regarding image, video, sound and possibly other types of resources
# Probably will want to break modules into more sub-categories.
    More to come on the story side of things:
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
=======================================================
"""

from collections import OrderedDict
from pathlib import Path
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401
from method_files import FileMethods
from method_shell import ShellMethods
from data_structs import Colors

import data_model_app as DMA
import data_model_story as DMS

FM = FileMethods()
SM = ShellMethods()


# =============================================================
# Utilities for Data Model objects
# =============================================================
def cols_to_dict(DM: object) -> dict:
    """
    Convert data model object to an OrderedDict.
    Returned attributes match SQL order in the database.

    :param DM: Data model object
    :return: Dictionary with table name as key and public attributes as value
    """
    # Create an OrderedDict excluding private and specific public methods or attributes
    public_vars = OrderedDict(
        (k, v)
        for k, v in vars(DM).items()
        if not k.startswith("_") and k not in {"Constraints", "to_dict", "from_dict"}
    )

    # Return dictionary with the table name from '_tablename' attribute as the key
    return {getattr(DM, "_tablename", "unknown_table"): public_vars}


def rec_to_dict(DM: object, p_dict: dict, p_row: int) -> dict:
    """
    Return a regular dict with populated values for one row of data.

    :param DM: Instantiated data model object
    :param p_dict: Dictionary containing lists of values (e.g., from a SELECT)
    :param p_row: Row number of the lists of values to return
    :return: Dictionary with column names as keys and corresponding row values
    """
    # Create a dictionary of public attributes using cols_to_dict()
    table_name = getattr(DM, "_tablename", "unknown_table")
    rec = cols_to_dict(DM).get(table_name, {})

    # Populate the record with values from p_dict for the specified row
    rec.update((col, v_list[p_row]) for col, v_list in p_dict.items())

    return rec


class CreateSQLError(Exception):
    """Custom error class for BootError errors."""
    pass


# =======================================================
# DB/DM DDL Calls
# - Create DDL and DML SQL files
# - Create SQLITE database and tables
# =======================================================
def create_sql(DB: object) -> bool:
    """
    Pass data object to create SQL files.
    Delete all existing SQL before creating new ones.

    :param DB: Current instance of the DB object.
    :return: True if successful, False otherwise
    """
    # Combine DDL and DML directories for efficient processing
    directories = [DB.DDL, DB.DML]

    # Delete all *.sql files in specified directories
    for directory in directories:
        for sql_file in FM.scan_dir(directory, "*.sql"):
            FM.delete_file(sql_file)

    # Define data models for processing with their respective categories
    # Metadata table must be the first table in the list
    data_models = {
        "app": [
            DMA.Metadata,
            DMA.Backup,
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
        ],
        "story": [
            DMS.MapRect,
            DMS.MapBox,
            DMS.MapSphere,
            DMS.Grid,
            DMS.GridCell,
            DMS.GridInfo,
            DMS.MapXMap,
            DMS.GridXMap,
            DMS.CharSet,
            DMS.CharMember,
            DMS.LangFamily,
            DMS.Language,
            DMS.LangDialect,
            DMS.GlossCommon,
            DMS.Glossary,
            DMS.Universe,
            DMS.ExternalUniv,
            DMS.GalacticCluster,
            DMS.Galaxy,
            DMS.StarSystem,
            DMS.World,
            DMS.Moon,
            DMS.Lake,
            DMS.LakeXMap,
            DMS.River,
            DMS.RiverXMap,
            DMS.OceanBody,
            DMS.OceanBodyXMap,
            DMS.OceanBodyXRiver,
            DMS.LandBody,
            DMS.LandBodyXMap,
            DMS.LandBodyXLandBody,
            DMS.LandBodyXOceanBody,
            DMS.SolarYear,
            DMS.Season,
            DMS.LunarYear,
            DMS.LunarYearXMoon,
            DMS.SolarCalendar,
            DMS.LunarCalendar,
            DMS.Month,
            DMS.LunarCalendarXMonth,
            DMS.SolarCalendarXMonth,
            DMS.WeekTime,
            DMS.LunarCalendarXWeekTime,
            DMS.SolarCalendarXWeekTime,
            DMS.DayTime,
            DMS.WeekTimeXDayTime,
        ],
    }
    # Generate SQL for each model category
    for category, models in data_models.items():
        for model in models:
            success = DB.generate_sql(model, category)
            if not success:
                fail = (f"{Colors.CL_RED}Error generating SQL for model {model}" +
                        f" in category {category}{Colors.CL_END}")
                raise CreateSQLError(fail)
                return False

    print(f"{Colors.CL_DARKCYAN}{Colors.CL_BOLD}SQL files generated.{Colors.CL_END}")
    return True


def create_db(DB: object, p_backup: bool = True) -> bool:
    """
    Drop and recreate empty all DB tables.
    This is a destructive operation.
    - Back up and archive DB if it exists.
    - Always make a new .ARCV file.
    - Overlay existing .BAK if it exists.
    - Do not wipe out existing archived DB's.
    - Logged records appear in .BAK, not in refreshed .DB
    :param DB: Instantied DataBase() Class.
    :param p_backup: Booean flag. If True, backup and archive the .DB
    :return: True if successful, False otherwise
    """
    if p_backup:
        bkup_path = Path(DB.SASKAN_BAK)
        if bkup_path.exists():
            DB.archive_db(DB.SASKAN_BAK)
            print(f"{Colors.CL_DARKCYAN}Backup DB was archived{Colors.CL_END}")
        db_path = Path(DB.SASKAN_DB)
        if db_path.exists():
            DB.backup_db(db_path, DB.SASKAN_BAK)
            print(f"{Colors.CL_DARKCYAN}Main DB was backed up{Colors.CL_END}")
    # Use a single call to execute_ddl with concatenated SQL lists
    drop_sql_list = [str(sql.name) for sql in FM.scan_dir(DB.DDL, "DROP*")]
    create_sql_list = [str(sql.name) for sql in FM.scan_dir(DB.DDL, "CREATE*")]
    # Execute DROP statements without foreign key constraints
    ok = DB.execute_ddl(drop_sql_list, p_foreign_keys_on=False)
    if ok:
        print(f"{Colors.CL_DARKCYAN}Database tables dropped.{Colors.CL_END}")
        # Execute CREATE statements with foreign key constraints
        ok = DB.execute_ddl(create_sql_list, p_foreign_keys_on=True)
        if ok:
            print(f"{Colors.CL_DARKCYAN}{Colors.CL_BOLD}Database tables created.{Colors.CL_END}")
    return ok
