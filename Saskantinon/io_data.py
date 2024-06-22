"""

:module:    io_data.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

# import ast          # abstract syntax trees
import json
# import pendulum     # date and time
# import platform
import pygame as pg
import random
import string

# from os import path
# from pathlib import Path
from collections import OrderedDict
from openai import OpenAI
from pathlib import Path
from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401
# from typing import Tuple, Union

from io_db import DataBase
from io_file import FileIO
from io_shell import ShellIO

DB = DataBase()
FI = FileIO()
SI = ShellIO()

client = OpenAI()  # Init OpenAI for use in this module
pg.init()          # Init PyGame for use in this module


#  UNIQUE CONSTANTS / "TRUE" ENUMS
# ================================
class Colors(object):
    """Constants for CLI and PyGame colors.
    Reference class attributes directly.
    No need to instantiate this class.
    """
    # CLI Colors and accents
    CL_BLUE = '\033[94m'
    CL_BOLD = '\033[1m'
    CL_CYAN = '\033[96m'
    CL_DARKCYAN = '\033[36m'
    CL_END = '\033[0m'
    CL_GREEN = '\033[92m'
    CL_PURPLE = '\033[95m'
    CL_RED = '\033[91m'
    CL_YELLOW = '\033[93m'
    CL_UNDERLINE = '\033[4m'

    # PyGame Colors
    CP_BLACK = pg.Color(0, 0, 0)
    CP_BLUE = pg.Color(0, 0, 255)
    CP_BLUEPOWDER = pg.Color(176, 224, 230)
    CP_GRAY = pg.Color(80, 80, 80)
    CP_GRAY_DARK = pg.Color(20, 20, 20)
    CP_GREEN = pg.Color(0, 255, 0)
    CP_PALEPINK = pg.Color(215, 198, 198)
    CP_RED = pg.Color(255, 0, 0)
    CP_SILVER = pg.Color(192, 192, 192)
    CP_WHITE = pg.Color(255, 255, 255)


class ImageType(object):
    """Types of images.
    Reference class attributes directly.
    No need to instantiate this class."""
    JPG = "jpg"
    PNG = "png"
    GIF = "gif"
    BMP = "bmp"
    SVG = "svg"
    TIF = "tif"
    ICO = "ico"


# Probably want to define database tables to store
# name, location, other info regarding image, video,
# sound and possibly other types of resources (plug-ins,
# mods, external services, etc.)
# Also see list of things like regions, countries,
# provinces, cities, towns, villages, etc.


#  COMPLEX CONSTANTS
# ================================
class Astro(object):
    """Constants, including both lists and enums
    Astronomical and physics units and conversions.
    - Generally, can just refer directly to the lists.
    - But the class can also be made into a dict:
      `astro_dict = {k:v for k,v in Astro.__dict__.items()
                     if not k.startswith('__')}`
    """
    # universe names
    UNAME = [["Cosmic", "Mysterious", "Eternal", "Radiant",
             "Infinite", "Celestial"],
             ["Endless", "Magical", "Spectacular",
              "Mystical", "Enchanting"],
             ["Universe", "Cosmos", "Realm", "Dimension",
              "Oblivion", "Infinity"]]
    # galactic cluster names
    GCNAME = [["Runic", "Starry", "Brilliant",
               "Blessed", "Eternal", "Celestial"],
              ["Oceanic", "Wonderful", "Waving",
               "Milky", "Turning"],
              ["Way", "Home", "Heavens", "Lights",
               "Path", "Cluster"]]
    # galaxy names
    GXNAME = [["Brilliant", "Lustrous", "Twinkling",
               "Silvery", "Argent", "Glistening"],
              ["Way", "Trail", "Cloud", "Wave", "Skyway"],
              ["Galaxy", "Cluster", "Nebula", "Spiral",
               "Starfield",  "Cosmos", "Nebula",
               "Megacosm", "Space"]]
    # timing pulsar names
    TPNAME = [["Timer", "Chrono", "Clockwork",
              "Lighthouse", "Beacon", "Pendumlum"],
              ["Pulsar", "Star", "Nova", "Sentry", "Stupa"]]
    # mass, matter, energy
    DE = "dark energy"
    DM = "dark matter"
    BM = "baryonic matter"
    LCLS = "luminosity class"
    SMS = "solar mass"
    SL = "solar luminosity"
    # objects, astronomical
    BH = "black hole"
    GB = "galactic bulge"
    GC = "galactic cluster"
    GH = "galactic halo"
    GX = "galaxy"
    IG = "interstellar matter"
    SC = "star cluster"
    SCLS = "star class"
    TP = "timing pulsar"            # saskan
    TU = "total universe"           # saskan
    XU = "external universe"        # saskan
    # time-related, real world and saskan
    GS = "galactic second"          # 'galactic' second; saskan
    GMS = "galactic millisecond"    # 'galactic' millisecond; saskan
    PMS = "pulses per millisecond"  # 'galactic' second as # of pulses
    ET = "elapsed time"             # age, duration, time passed
    GYR = "gavoran year"            # saskan
    GDY = "gavoran day"             # saskan
    # rates, speeds, velocities
    ER = "expansion rate"           # of a volume
    UER = "universal expansion rate"
    KSM = "km/s per Mpc"            # km/s per Mpc
    PRO = "period of rotation"
    PRV = "period of revolution"
    PR = "pulse rate"
    # distance
    AU = "astronomical unit"     # distance from Fatune to Gavor
    GLY = "gigalight year"
    GPC = "gigaparsec"
    KPC = "kiloparsec"
    LM = "light minute"
    LS = "light second"
    LY = "light year"
    MPC = "megaparsec"
    PC = "parsec"
    # area, volume
    GLY2 = "square gigalight year"
    GLY3 = "cubic gigalight year"
    GPC2 = "square gigaparsec"
    GPC3 = "cubic gigaparsec"
    PC2 = "square parsec"
    PC3 = "cubic parsec"
    LY2 = "square light year"
    LY3 = "cubic light year"
    # constants
    U_MIN_RAD_GLY = 45.824
    U_MAX_RAD_GLY = 47.557
    U_MIN_AGE_GYR = 2.67e10
    U_MAX_AGE_GYR = 3.12e10
    U_AVG_MASS_KG = 1.5e53
    U_EXP_RATE = 73.3  # expansion rate in km/s per Mpc
    U_VOL_TO_MASS = 3.61441428e+48  # volume to mass multiplier
    U_DARK_ENERGY_PCT = 0.683       # dark energy percentage
    U_DARK_MATTER_PCT = 0.274       # dark matter percentage
    U_BARYONIC_PCT = 0.043          # baryonic matter percentage
    # conversions -- multiplicative in indicated direction
    # For `AA_TO_BB`, BB = AA * value
    # Example: `AU_TO_KM` means `KM = AU * 1.495979e+8`
    AU_TO_KM = 1.495979e+8        # astronomical units -> km
    AU_TO_LM = 5.2596e+16         # astro units -> light minutes
    AU_TO_LS = 0.002004004004     # astro units -> light seconds
    AU_TO_LY = 0.00001581250799   # astro units -> light years
    GLY_TO_LY = 1e+9              # gigalight years -> light years
    GPC_TO_GLY = 3.09             # gigaparsecs -> gigalight years
    GPC_TO_MPC = 1000.0           # gigaparsecs -> megaparsecs
    KM_TO_AU = 0.000006684587122  # kilometers -> astro units
    KPC_TO_MPC = 1000.0           # kiloparsecs -> megaparsecs
    KPC_TO_PC = 1000.0            # kiloparsecs -> parsecs
    LM_TO_AU = 0.00000000000002   # light minutes -> astro units
    LM_TO_LS = 9460730472580800   # light minutes -> light seconds
    LM_TO_LY = 0.000000000000019  # light minutes -> light years
    LS_TO_AU = 499.004783676      # light seconds -> astro units
    LS_TO_LM = 0.000000000000105  # light seconds -> light minutes
    LY_TO_AU = 63240.87           # light years -> astro units
    LY_TO_GLY = 1e-9              # light years -> gigalight years
    LY_TO_LM = 52596000000000000  # light years -> light minutes
    LY_TO_PC = 0.30659817672196   # light years -> parsecs
    MPC_TO_GPC = 0.001            # megaparsecs -> gigaparsecs
    MPC_TO_KPC = 1000.0           # megaparsecs -> kiloparsecs
    GLY_TO_PC = 3.262e6           # gigalight years -> parsecs
    PC_TO_GLY = 3.065603923973023e-07  # parsecs -> gigalight years
    PC_TO_KPC = 0.001             # parsecs -> kiloparsecs
    PC_TO_LY = 3.261598           # parsecs -> light years


class Geog(object):
    """Constants for computations using variety of units
    and formulae for measures of distance at a human or
    (fantasy) planetary geographical scale.
    """
    # distance
    CM = "centimeters"
    FT = "feet"
    GA = "gawos"        # saskan
    IN = "inches"
    KA = "katas"        # saskan
    KM = "kilometers"
    M = "meters"
    MI = "miles"
    MM = "millimeters"
    NM = "nautical miles"
    NOB = "nobs"        # saskan
    THWAB = "thwabs"    # saskan
    TWA = "twas"        # saskan
    YUZA = "yuzas"      # saskan
    # area, volume
    M2 = "square meters"
    M3 = "cubic meters"
    # distance, geographical
    DGLAT = "degrees latitude"
    DGLONG = "degrees longitude"
    # direction, geographical
    LOC = "location"
    N = "north"
    E = "east"
    S = "south"
    W = "west"
    NE = "northeast"
    SE = "southeast"
    SW = "southwest"
    NW = "northwest"
    NS = "north-south"
    EW = "east-west"
    # conversions - metric/imperial
    # conversions -- multiplicative in indicated direction
    # For `AA_TO_BB`, BB = AA * value
    # Example: `CM_TO_IN` means `CM = IN * 0.3937007874`
    CM_TO_IN = 0.3937007874      # centimeters -> inches
    CM_TO_M = 0.01               # centimeters -> meters
    CM_TO_MM = 10.0              # centimeters -> millimeters
    FT_TO_IN = 12.0              # feet -> inches
    FT_TO_M = 0.3048             # feet -> meters
    IN_TO_CM = 2.54              # inches -> centimeters
    IN_TO_FT = 0.08333333333     # inches -> feet
    IN_TO_MM = 25.4              # inches -> millimeters
    KM_TO_M = 1000.0             # kilometers -> meters
    KM_TO_MI = 0.62137119223733  # kilometers -> miles
    KM_TO_NM = 0.539956803       # kilometers -> nautical miles
    M_TO_CM = 100.0              # meters -> centimeters
    M_TO_FT = 3.280839895        # meters -> feet
    M_TO_KM = 0.001              # meters -> kilometers
    MI_TO_KM = 1.609344          # miles -> kilometers
    MI_TO_NM = 0.868976242       # miles -> nautical miles
    MM_TO_CM = 0.1               # millimeters -> centimeters
    MM_TO_IN = 0.03937007874     # millimeters -> inches
    NM_TO_KM = 1.852             # nautical miles -> kilometers
    NM_TO_MI = 1.150779448       # nautical miles -> miles
    # conversions - saskan/metric
    CM_TO_NOB = 0.64             # centimeters -> nobs
    GABO_TO_MI = 0.636           # gabos -> miles
    GAWO_TO_KATA = 4.0           # gawos -> kata
    GAWO_TO_KM = 1.024           # gawos -> kilometers
    GAWO_TO_M = 1024.0           # gawos -> meters
    IN_TO_NOB = 2.56             # inches -> nobs
    KATA_TO_KM = 0.256           # kata -> kilometers
    KATA_TO_M = 256.0            # kata -> meters
    KATA_TO_MI = 0.159           # ktaa -> miles
    KATA_TO_THWAB = 4.0          # kata -> thwabs
    M_TO_NOB = 64.0              # meters -> nobs
    M_TO_THWAB = 0.015625        # meters -> thwabs (1/64th)
    MM_TO_NOB = 0.0064           # millimeters -> nobs
    NOB_TO_CM = 1.5625           # nobs -> centimeters
    NOB_TO_IN = 0.390625         # nobs -> inches
    NOB_TO_MM = 156.25           # nobs -> millimeters
    THWAB_TO_KATA = 0.25         # thwabs -> kata
    THWAB_TO_M = 64.0            # thwabs -> meters
    THWAB_TO_TWA = 64.0          # thwabs -> twas
    TWA_TO_M = 1.00              # twas -> meters
    TWA_TO_NOB = 64.0            # twas -> nobs
    TWA_TO_THWAB = 0.015625      # twas -> thwabs (1/64th)
    YUZA_TO_GABO = 4.0           # yuzas -> gabos
    YUZA_TO_KM = 4.096           # yuzas -> kilometers
    YUZA_TO_M = 4096.0           # yuzas -> meters
    YUZA_TO_MI = 2.545           # yuzas -> miles
    # conversions, geographical to metric
    DGLAT_TO_KM = 111.2           # degree of latitutde -> kilometers
    DGLONG_TO_KM = 111.32         # degree of longitude -> kilometers
    KM_TO_DGLAT = 0.00898315284   # kilometers -> degree of latitude
    KM_TO_DGLONG = 0.00898311175  # kilometers -> degree of longitude


class Geom(object):
    """Constants assigned to meaningful abbreviations
    and names relating generically to geometry and physics.
    """
    # math, general geometry
    ABC = "(a, b, c)"
    ANG = "angle"
    AR = "area"
    BND = "bounding rectangle"
    CNT = "count"
    CON = "container"
    DC = "decimal"
    DI = "diameter"
    DIM = "dimensions"
    DIR = "direction"
    HT = "height"
    INT = "integer"
    LG = "length"
    PCT = "percent"
    PYR = ("pitch, yaw, roll")
    RD = "radius"
    ROT = "rotation"
    SAX = "semi-axes"
    SZ = "size"
    VE = "vector"
    VL = "volume"
    WD = "width"
    XY = "(x, y)"
    XYZD = "((x,x), (y,y), (z,z))"
    XYZ = "(x, y, z)"
    # geometry shapes
    BX = "pg_rect"
    CI = "circle"
    EL = "ellipsoid"
    RC = "rectangle"
    SH = "sphere"
    SHA = "shape"
    SP = "spiral"
    # weight. mass
    GM = "grams"
    KG = "kilograms"
    LB = "pounds"
    MS = "mass"
    OZ = "ounces"
    # energy
    AMP = "amperes (A)"
    OH = "ohms (Ω)"
    V = "volts (V)"
    WA = "watts (W)"
    # names, labels, qualities
    NM = "name"
    REL = "relative"
    SHP = "shape"


class AppDisplay(object):
    """Static values related to constructing GUI's.
    As long as pg.display is not called, nothing will be rendered.
    This needs to be modified once io_file is modified to read
    from the database.
    """
    # Typesetting
    # -------------------
    DASH16: str = "-" * 16
    FONT_FXD = 'Courier 10 Pitch'
    FONT_MED_SZ = 30
    FONT_SANS = 'DejaVu Sans'
    FONT_SM_SZ = 24
    FONT_TINY_SZ = 12
    LG_FONT_SZ = 36
    # PyGame Fonts
    # -------------------
    F_SANS_TINY = pg.font.SysFont(FONT_SANS, FONT_TINY_SZ)
    F_SANS_SM = pg.font.SysFont(FONT_SANS, FONT_SM_SZ)
    F_SANS_MED = pg.font.SysFont(FONT_SANS, FONT_MED_SZ)
    F_SANS_LG = pg.font.SysFont(FONT_SANS, LG_FONT_SZ)
    F_FIXED_LG = pg.font.SysFont(FONT_FXD, LG_FONT_SZ)
    # PyGame Cursors
    # -------------------
    CUR_ARROW = pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW)
    CUR_CROSS = pg.cursors.Cursor(pg.SYSTEM_CURSOR_CROSSHAIR)
    CUR_HAND = pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND)
    CUR_IBEAM = pg.cursors.Cursor(pg.SYSTEM_CURSOR_IBEAM)
    CUR_WAIT = pg.cursors.Cursor(pg.SYSTEM_CURSOR_WAIT)
    # PyGame Keyboard
    # -------------------
    KY_QUIT = (pg.K_q, pg.K_ESCAPE)
    KY_ANIM = (pg.K_F3, pg.K_F4, pg.K_F5)
    KY_DATA = (pg.K_a, pg.K_l)
    KY_RPT_TYPE = (pg.K_KP1, pg.K_KP2, pg.K_KP3)
    KY_RPT_MODE = (pg.K_UP, pg.K_RIGHT, pg.K_LEFT)
    # Game Platform
    # -------------------
    INFO = pg.display.Info()
    FRAME = "game_frame"  # --> c_frame.json
    MENUS = "game_menus"  # --> c_menus.json
    # PLATFORM = (
    #     FI.F[FRAME]["dsc"] +
    #     #  " | " + platform.platform() +
    #     #  " | " + platform.architecture()[0] +
    #     f" | monitor (w, h): {INFO.current_w}, {INFO.current_h}" +
    #     " | Python " + platform.python_version() +
    #     " | Pygame " + pg.version.ver)
    # Window/overall frame for Game
    # -----------------------------
    WIN_W = round(INFO.current_w * 0.9)
    WIN_H = round(INFO.current_h * 0.9)
    WIN_MID = (WIN_W / 2, WIN_H / 2)
    # pg.display.set_caption(FI.F[FRAME]["ttl"])
    KEYMOD_NONE = 4096
    TIMER = pg.time.Clock()
    # Don't do display.set_mode() command in data structure
    # It launches the pygame rendering environment
    # Move this to Saskan game module or a rendering module -->
    #    `WIN = pg.display.set_mode((WIN_W, WIN_H))`
    # Menu bar for Game
    # -------------------
    MBAR_X = WIN_W * 0.01
    MBAR_Y = WIN_H * 0.005
    MBAR_H = WIN_H * 0.04
    # MBAR_W = 240 if (WIN_W - (MBAR_X * 2)) / len(FI.M[MENUS]["menu"]) > 240\
    #     else (WIN_W - (MBAR_X * 2)) / len(FI.M[MENUS]["menu"])
    MBAR_MARGIN = 6
    # Game Map (grid) window size for Saskan game
    # -------------------------------------------
    # GAMEMAP_TTL = FI.W["game_windows"]["gamemap"]["ttl"]
    GAMEMAP_X = int(round(WIN_W * 0.01))
    GAMEMAP_Y = int(round(WIN_H * 0.06))
    GAMEMAP_W = int(round(WIN_W * 0.8))
    GAMEMAP_H = int(round(WIN_H * 0.9))
    # Console window for Saskan app
    # -------------------------------
    # CONSOLE = FI.W["game_windows"]["console"]
    CONSOLE_X = int(round(GAMEMAP_X + GAMEMAP_W + 20))
    CONSOLE_Y = GAMEMAP_Y
    CONSOLE_W = int(round(WIN_W * 0.15))
    CONSOLE_H = GAMEMAP_H
    CONSOLE_BOX = pg.Rect(CONSOLE_X, CONSOLE_Y,
                          CONSOLE_W, CONSOLE_H)
    # For now, the header/title on CONSOLE is static
    # CONSOLE_TTL_TXT = FI.W["game_windows"]["console"]["ttl"]
    # CONSOLE_TTL_IMG =\
    #     F_SANS_MED.render(CONSOLE_TTL_TXT, True,
    #                       Colors.CP_BLUEPOWDER,
    #                       Colors.CP_BLACK)
    # CONSOLE_TTL_BOX = CONSOLE_TTL_IMG.get_rect()
    # CONSOLE_TTL_BOX.topleft = (CONSOLE_X + 5, CONSOLE_Y + 5)
    # Info Bar for Saskan app
    IBAR_LOC = (GAMEMAP_X, int(round(WIN_H * 0.97)))
    # Help Pages -- external web pages, displayed in a browser
    # WHTM = FI.U["uri"]["help"]


#  SIMPLE DATA STRUCTURES
# ============================
class Struct(object):
    """Base class for data structures made of a
    simple group of attritubes. Structures
    have default values, but are mutable.
    Instantiate as sub-class object with no parameters.
    User assigns values directly.
    For example:
        CRI = Struct.ColumnRowIndex()
        CRI.r = 3
        CRI.c = 5
    """

    class ColumnRowIndex(object):
        """Structure for column and row indexes."""
        r: int = 0
        c: int = 0

    class MatrixUpDown(object):
        """Structure for z-up and z-down indexes."""
        u: int = 0
        d: int = 0

    class WidthHeight(object):
        """Structure for width and height measures."""
        w: float = 0.0
        h: float = 0.0

    class CoordXYZ(object):
        """Structure for x, y, z coordinates."""
        x: float = 0.0
        y: float = 0.0
        z: float = 0.0

    class CoordXY(object):
        """Structure for x, y coordinates."""
        x: float = 0.0
        y: float = 0.0

    class AxesABC(object):
        """Structure for a, b, c axes."""
        a: float = 0.0
        b: float = 0.0
        c: float = 0.0

    class PitchYawRollAngle(object):
        """Structure for pitch, yaw,, roll angles."""
        pitch: float = 0.0
        yaw: float = 0.0
        roll: float = 0.0

    class GameRect(object):
        """Simple structure for defining rectangles.
        This provides a way to store the minimal set of
        values needed. See GamePlane and pg.Rect for more
        complex rectangle structures.
        """
        x: float = 0.0
        y: float = 0.0
        w: float = 0.0
        h: float = 0.0

    class GameLatLong(object):
        """Structure for game latitude and longitude.
        Game lat and long refer to fantasy world locations.
        Cannot use standard Earth-based geo-loc modules.

        Latitudes and longitudes are in decimal degrees.
        Lat north is positive; south is negative.
        East, between the fantasy-planet equivalent of
        universal meridien and international date line,
        is positive; west is negative.
        """
        latiutde_dg: float = 0.0
        longitude_dg: float = 0.0

    class GameGeoLocation(object):
        """
        This is a general-purpose, high level geo-location
        data structure, planar and rectangular.
        Use degrees as the specifier for locations.
        Then compute km or other physical dimensions
        based on scaling to a grid when rendering.

        Provide rough altitudes (average, min and max) meters,
        to give a general sense of the 3rd dimension.
        Detail heights and depths in specialized data structures.

        For astronomical, underwater or other "3D" spaces,
        see Game3DLocation class (below), keeping in mind that
        3D rendering is beyond the capabilities of a Python-
        driven game.
        """
        latitude_north_dg: float = 0.0
        latitude_south_dg: float = 0.0
        longitude_east_dg: float = 0.0
        longitude_west_dg: float = 0.0
        avg_altitude_m: float = 0.0
        max_altitude_m: float = 0.0
        min_altitude_m: float = 0.0

    class Game3DLocation(object):
        """
        This is a general-purpose, high level 3D location/shape
        container structure, box-shaped, that is, six adjoining
        rectangles with parallel sides.  Use x, y, z coordinates
        which can be mapped to whatever units are needed. For
        example, in a Universe, the x,y,z coordinates might refer
        to mega-parsecs, whereas in an Undersea world they might
        refer to kilometers.
        The box is defined as an x,y,z origin point, which can
        be conceived of visually as the upper-left, foremost
        corner of the box. The box is then defined by w, h and d =
        lateral dimensions in the x, y and z directions.
        """
        origin_x: float = 0.0
        origin_y: float = 0.0
        origin_z: float = 0.0
        width_x: float = 0.0
        height_y: float = 0.0
        depth_z: float = 0.0

    class Graphic(object):
        """A data structure for referencing an image file."""
        pg_surface: pg.Surface
        pg_rect: pg.Rect
        img_type: ImageType
        img_url: str = ''
        img_desc: str = ''


#  COMPLEX DATA STRUCTURES
#  =============================
class EntityType(object):
    """Constants:
    - This entire class can be made into a dict:
      `entity_dict = {k:v for k,v in EntityType.__dict__.items()
                      if not k.startswith('__')}`
    """
    ASTRO_DIRECTION = ['prograde', 'retrograde']
    ASTRO_LOCATION = ['inner', 'outer', 'multiple']
    ASTRO_SHAPE = ['ellipsoid', 'spherical']
    BACKUP_TYPE = ["archive", "backup", "compressed",
                   "export", "encrypted"]
    CHAR_SET_TYPE = ['alphabet', 'abjad', 'abugida',
                     'syllabary', 'ideogram']
    CLUSTER_SHAPE = ['ellipsoid', 'spherical']
    DENSITY = ['sparse', 'dense']
    DATA_FORMATS = ["csv", "json", "xml", "xls", "xlsx",
                    "txt", "html", "pdf", "doc", "docx",
                    "txt", "ods", "sql", "dbf", "db",
                    "sqlite", "mdb", "accdb", "zip",
                    "tar", "gz"]
    FREQUENCY = ['rare', 'occasional', 'frequent']
    GLOSS_TYPE = ['word', 'phrase', 'map', 'picture', 'diagram',
                  'data', 'software', 'sound', 'video']
    HEMISPHERE_TYPE = ['north', 'south']
    INTENSITY = ['low', 'medium', 'high']
    LAKE_SIZE = ['small', 'medium', 'large']
    LAKE_TYPE = ['lake', 'reservoir', 'pond', 'pool',
                 'loch',
                 'hot spring', 'swamp', 'marsh',
                 'mill pond',
                 'oxbow lake', 'spring', 'sinkhole',
                 'acquifer', 'vernal pool', 'wadi']
    LAND_BODY_TYPE = ['island', 'continent', 'sub-continent',
                      'region']
    LAND_LAND_RELATION_TYPE = ['borders', 'overlaps',
                               'contains', 'contained by']
    LAND_OCEAN_RELATION_TYPE = ['borders', 'overlaps',
                                'contains', 'contained by']
    LEAP_RULE = ['add_to_start_of_nth_month',
                 'add_to_end_of_nth_month', 'add_special_month']
    LINK_CATEGORY = ['help']
    LUMINOSITY_CLASS = ['I', 'II', 'III', 'IV', 'V']
    MAP_TOUCH_TYPE = ['contains', 'is_contained_by', 'borders',
                      'overlaps', 'informs', 'layers_above',
                      'layers_below']
    MAP_TYPE = ['geo', 'astro', 'underwater',
                'underground',
                'informational', 'political']
    OCEAN_BODY_TYPE = ['fjord', 'sea', 'ocean',
                       'harbor', 'lagoon', 'bay',
                       'gulf', 'sound', 'bight',
                       'delta', 'estuary', 'strait',
                       'ice field', 'ice sheet',
                       'ice shelf', 'iceberg',
                       'ice floe', 'ice pack',
                       'roadstead', 'tidal pool',
                       'salt marsh']
    OCEAN_HAZARD = ['tsunami', 'typhoon', 'volcano',
                    'tide', 'storm', 'whirlpool',
                    'current', 'undertow', 'rip tide',
                    'reef']
    OCEAN_FEATURE = ['atoll', 'coral reef', 'seamount',
                     'trench', 'volcanic vent',
                     'hydrothermal vent', 'tide pool',
                     'mangrove', 'kelp forest',
                     'coral bed', 'sargasso',
                     'gyre', 'upwelling',
                     'downwelling', 'eddy',
                     'thermocline', 'halocline',
                     'polar ice cap', 'ice shelf']
    OCEAN_WAVE_TYPE = ['low', 'medium', 'high', 'none']
    ORBITAL_SHAPE = ['circular', 'elliptical']
    RELATIVE_SIZE = ['small', 'medium', 'large']
    RIVER_FEATURE = ['delta', 'bridge', 'crossing',
                     'footbridge', 'pier', 'marina',
                     'boathouse', 'habitat']
    RIVER_HAZARD = ['rapids', 'wreckage', 'sandbar',
                    'waterfall', 'shallow',
                    'dam', 'weir', 'habitat']
    RIVER_TYPE = ['perrenial', 'periodic', 'episodic',
                  'exotic', 'tributary', 'distributary',
                  'underground', 'aqueduct', 'canal',
                  'rapids', 'winding', 'stream',
                  'glacier']
    RIVER_NAV_TYPE = ["small craft", "large craft",
                      "none"]
    SEASON_TYPE = ['winter', 'spring', 'summer', 'fall'
                   'all', 'winter-spring', 'spring-summer',
                   'summer-fall', 'fall-winter']
    SPECTRAL_CLASS = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    STABILITY = ['stable', 'unstable']
    WATER_TYPE = ['freshwater', 'saline', 'brackish']
    APP_CATEGORY = ['admin', 'game']
    WORLD_TYPE = ['habitable', 'gas giant', 'rocky',
                  'desert', 'oceanic', 'ice planet',
                  'molten', 'other']


class GamePlane(object):
    """
    A general purpose shape structure that is planar
    and rectangular, defining only the corners of a
    rectangular space relative to x,y coordinates in a
    containing coordinate system is useful for
    describing areas within a map or grid.

    Line and fill attributes may optonally be set.
    A pygame Rect object is derived from the corners.
    """
    def __init__(self,
                 p_top_left: Struct.CoordXY,
                 p_top_right: Struct.CoordXY,
                 p_bottom_left: Struct.CoordXY,
                 p_bottom_right: Struct.CoordXY,
                 p_fill: bool = False,
                 p_fill_color: pg.Color = pg.Color(0, 0, 0),
                 p_line_color: pg.Color = pg.Color(0, 0, 0),
                 p_line_width: float = 0.0):
        """
        Set abstract coordinates/location, and optionally
        fill and line attributes.
        :args:
        -- p_top_left: top left coordinate (x, y)
        -- p_top_right: top right (x, y)
        -- p_bottom_left: bottom left (x, y)
        -- p_bottom_right: bottom right (x, y)
        -- p_fill: fill the shape (True or False)
        -- p_fill_color: fill color (pygame color object)
        -- p_line_color: line color (pygame color object)
        -- p_line_width: line width (float)
        """
        self.coords =\
            self.set_coords(p_top_left,
                            p_top_right,
                            p_bottom_left,
                            p_bottom_right)
        self.fill =\
            self.set_fill(p_fill,
                          p_fill_color)
        self.line =\
            self.set_line(p_line_color,
                          p_line_width)
        self.box = self.set_pygame_rect()

    def set_coords(self,
                   p_top_left,
                   p_top_right,
                   p_bottom_left,
                   p_bottom_right) -> dict:
        """ Set x,y coordinates/corner locations
        relative to a containing coordinate system.
        Derive the width and height of the plane and
        the integer x and y for top and left.
        """
        return {'top_left': p_top_left,
                'top_right': p_top_right,
                'bottom_left': p_bottom_left,
                'bottom_right': p_bottom_right,
                'left': p_top_left.x,
                'top': p_top_left.y,
                'width': p_top_right.x - p_top_left.x,
                'height': p_bottom_left.y - p_top_left.y}

    def set_fill(self,
                 p_fill,
                 p_fill_color) -> dict:
        """ Set attributes of the plane fill.
        """
        return {'is_filled': p_fill,
                'fill_color': p_fill_color}

    def set_line(self,
                 p_line_color,
                 p_line_width) -> dict:
        """ Set attributes of the plane line.
        """
        return {'line_color': p_line_color,
                'line_width': p_line_width}

    def set_pygame_rect(self) -> pg.Rect:
        """ Set pygame Rect object.
           (left, top, width, height)
        """
        return pg.Rect(self.coords['left'],
                       self.coords['top'],
                       self.coords['width'],
                       self.coords['height'])


class GameGridData(object):
    """
    PSet up a matrix of cells within a grid, both to direct
    rendering, and to store data within each cell. The drawing
    data is 2D oriented, but the data-content supports 3D,
    like a layer cake or slices of a scan.

    Specs for rendering grid and cells have two inputs:
    - number of rows and columns -- init params
    - grid placement in map-window is defined in AppDisplay
    For smaller cells, assign more rows and columns to the grid.
    For bigger cells, assign fewer rows and columns.

    - Supports 3 dimensions in layered fashion.
    - To use as a 2D grid, set p_z values to zero.
    """
    def __init__(self,
                 p_cols: int = 1,
                 p_rows: int = 1,
                 p_z_up: int = 0,
                 p_z_down: int = 0):
        """
        Number of cells in matrix:
        :args:
        -- p_cols: number of columns ("vertical" or N-S cells)
        -- p_rows: number of rows ("horizontal" or E-W cells)
        -- p_z_up: number of "up" cells
        -- p_z_down: number of "down" cells
        Location of grid-box in map window is set in AppDisplay.
        """
        x_offset = int(round(AppDisplay.GAMEMAP_W * 0.01))
        y_offset = int(round(AppDisplay.GAMEMAP_H * 0.02))
        self.visible = False
        self.plane, self.box =\
            self._set_grid_rects(x_offset, y_offset)
        self.grid_size =\
            self.set_grid_size(p_cols, p_rows, p_z_up, p_z_down)
        self.cell_size = self.set_cell_size(x_offset, y_offset)
        self.grid_lines = self.set_grid_lines(x_offset, y_offset)
        self.grid_data = self.set_grid_data()

    def _set_grid_rects(self,
                        x_offset: int,
                        y_offset: int) -> tuple:
        """ Set GamePlane and pygame Rect objects for the grid.
        These help place and render the grid as a whole. Since inputs
        are set by the constant structure 'AppDisplay', this method is
        treated as "internal".
        Assumes a 2D rendering of each "z-layer" of the grid.
        Default z-layer is the zero-layer.
        No attempt to provide skew for 3D rendering.
        :returns:
        - (grid_rect, grid_rect_pygame): tuple of GamePlane and pygame Rect
        """
        x = AppDisplay.GAMEMAP_X + x_offset
        y = AppDisplay.GAMEMAP_Y + y_offset
        w = AppDisplay.GAMEMAP_W
        h = AppDisplay.GAMEMAP_H
        game_plane = GamePlane(
            p_top_left=Struct.CoordXY(x, 0),
            p_top_right=Struct.CoordXY(w, 0),
            p_bottom_left=Struct.CoordXY(x, h),
            p_bottom_right=Struct.CoordXY(w, h))
        grid_rect_pygame = pg.Rect(x, y, w, h)
        return (game_plane, grid_rect_pygame)

    def set_grid_size(self,
                      p_cols,
                      p_rows,
                      p_z_up,
                      p_z_down) -> dict:
        """ Set x, y and z dimensions for the grid based on inputs.
        That is, how many cells are contained in the grid/matrix.
        In this method, a 3D matrix is supported. Here, z-dimension is
        handled separately for "up" and "down", rather than using
        positive and negative values.
        :returns:
        - {rc, zz}: dict of column/row and up/down dimensions
        """
        rc = Struct.ColumnRowIndex()
        rc.r = p_cols
        rc.c = p_rows
        zz = Struct.MatrixUpDown()
        zz.z_up = p_z_up
        zz.z_down = p_z_down
        return {'rc': rc, 'zz': zz}

    def set_cell_size(self,
                      x_offset: int,
                      y_offset: int) -> dict:
        """ Set width, height in pixels of a single cell.
        Support placement and rendering of cells within the grid.
        In this case width and height refer to sizes within the
        z-zero plane, that is, "height" is in the sense of a 2D grid,
        not in the sense of the z-directions of the 3D grid.

        At this point, a "cell" is a rectangle, not a cube.
        :returns:
        {w, h}: width, height of each cell
        """
        w = int(round(AppDisplay.GAMEMAP_W - x_offset) /
                self.grid_size['rc'].c)
        h = int(round(AppDisplay.GAMEMAP_H - y_offset) /
                self.grid_size['rc'].r)
        return {'w': w, 'h': h}

    def set_grid_lines(self,
                       x_offset: int,
                       y_offset: int) -> dict:
        """ Set dimensions, location, of the cell lines.
        Support placement and rendering of the cells.  Again,
        this refers solely to a "flat" plane. No attempt to provide
        a 3D rendering. Only store the coordinates of the
        top-left starting-point for the lines, the width of the
        horizontal lines, and the height of the vertical lines.
        Handle placement of remaining lines in a rendering method.
        :returns:
        {x, y, w, h}: x, y of first line,
                      width of horizontal lines,
                      height of vertical lines
        """
        x = int(round(self.box.x + x_offset))
        y = int(round(self.box.y + y_offset))
        w = self.cell_size['w'] * self.grid_size['rc'].c
        h = self.cell_size['h'] * self.grid_size['rc'].r
        return {'x': x, 'y': y, 'w': w, 'h': h}

    def set_grid_data(self) -> dict:
        """Define a structure that holds cell data of various types.
        Then assign a copy of that structure to each cell in the grid,
        including the z directions, which here are keyed as positive (up)
        and negative (down).
        Might be more efficient to initialize to empty dicts or None?
        """
        grid_matrix = dict()
        cell_data = {
            'fill': False,
            'fill_color': Colors.CP_BLACK,
            'line_color': Colors.CP_BLACK,
            'text': '',
            'img': Struct.Graphic,
            'state_data': {}
        }
        for r in range(self.grid_size['rc'].r + 1):
            grid_matrix[r] = dict()
            for c in range(self.grid_size['rc'].c + 1):
                grid_matrix[r][c] = dict()
                for z in range(self.grid_size['zz'].z_up + 1):
                    grid_matrix[r][c][z] = dict()
                    grid_matrix[r][c][z] = cell_data
                for d in range(self.grid_size['zz'].z_down + 1):
                    z = d * -1
                    grid_matrix[r][c][z] = dict()
                    grid_matrix[r][c][z] = cell_data
        return grid_matrix


#  GAME-RELATED BASIC DATA ALGORTIHMS
# ===================================
class CompareRect(object):
    """
    Compare (pygame) rectangles:
    - Check for containment
    - Check for intersections (overlap, collision/union)
    - Check for adjacency/borders (clipline)
    - Check for equality/sameness
    """

    def __init__(self):
        pass

    def rect_contains(self,
                      p_box_a: pg.Rect,
                      p_box_b: pg.Rect) -> bool:
        """Determine if rectangle A contains rectangle B.
        use pygame contains
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        if p_box_a.contains(p_box_b):
            return True
        else:
            return False

    def rect_overlaps(self,
                      p_box_a: pg.Rect,
                      p_box_b: pg.Rect) -> bool:
        """Determine if rectangle A and rectangle B overlap.
        xxx use pygame colliderect xxx
        use pygame union
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        # if p_box_a.colliderect(p_box_b):
        if p_box_a.union(p_box_b):
            return True
        else:
            return False

    def rect_borders(self,
                     p_rect_a: pg.Rect,
                     p_rect_b: pg.Rect) -> bool:
        """Determine if rectangle A and rectangle B share a border.
        use pygame clipline
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        if p_rect_a.clipline(p_rect_b):
            return True
        else:
            return False

    def rect_same(self,
                  p_rect_a: pg.Rect,
                  p_rect_b: pg.Rect) -> bool:
        """Determine if rectangle A and rectangle B occupy exactly
        the same space.
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        if p_rect_a.topright == p_rect_b.topright and \
           p_rect_a.bottomleft == p_rect_b.bottomleft:
            return True
        else:
            return False


# =============================================================
# DB/ORM table definitions
#
# The following models are used to create SQLITE tables and
#   standard/generic SQL commands (INSERT, UPDATE, SELECT).
# All fields must have a default value.
# A sub-class identifies:
# - SQLITE constraints,
# - GROUPed types derived from data types defined above,
# - sort order for SELECT queries.
# =======================================================

# =============================================================
# Abstracted methods for ORM objects
# =============================================================
def _orm_to_dict(ORM: object) -> dict:
    """Convert object to an OrderedDict.
    This ensures order of attributes matches SQL order in DB.
    :args:
    - ORM object
    """
    all_vars = OrderedDict(vars(ORM))
    public_vars = OrderedDict({k: v for k, v in all_vars.items()
                               if not k.startswith('_') and
                               k not in ('Constraints',
                                         'to_dict', "from_dict")})
    return {all_vars['_tablename']: public_vars}


def _orm_from_dict(ORM: object,
                   p_dict: dict,
                   p_row: int) -> dict:
    """
    Load DB SELECT results into memory.
    Set object attributes from dict of listed values
    and return a regular dict of with populated values.
    :args:
    - ORM object
    - p_dict: dict of lists of values
    - p_row: row number of the lists of values to use
    """
    batch_rec =\
        {k: v for k, v in dict(ORM.to_dict()[ORM._tablename]).items()
         if k not in ("_tablename", "to_dict", "from_dict")}
    for k, v in batch_rec.items():
        setattr(ORM._tablename, k, p_dict[k][p_row])
        batch_rec[k] = getattr(ORM._tablename, k)
    return batch_rec


# =============================================================
# System Maintenance
# @DEV:
#  - Consider adding a version ID to support programmatic
#    prototyping, undo's and so on.
# =============================================================
class Backup(object):
    """Store metadata about DB backup, restore, archive, export.
    """
    _tablename: str = "BACKUP"
    bkup_uid_pk: str = ''       # Primary key
    bkup_name: str = ''
    bkup_dttm: str = ''
    bkup_type: str = ''
    file_from: str = ''
    file_to: str = ''

    def to_dict(self) -> dict:
        """Convert attributes to OrderedDict. """
        return _orm_to_dict(Backup)

    def from_dict(self,
                  p_dict: dict,
                  p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"bkup_uid_pk": ["bkup_uid_pk"]}
        ORDER: list = ["bkup_dttm DESC", "bkup_name ASC"]
        CK: dict = {"bkup_type": EntityType.BACKUP_TYPE}


# =============================================================
# Game Construction
# x Convert g_ and t_ configs to database tables.
# x Convert the APP values on c_context.json to db tables.
# - Convert the schema files to db tables: services, ontology
# - Convert the time and scenes to db tables.
# - If needed, modify the geo and astro db tables per schema files
# =============================================================

class AppConfig(object):
    """Define the APP configuration values.
    - app root, bin, and mem directories
    - app directories
        - cfg, data, img, py, db, sch
    - may need to keep or dup some values for bootstrap
    """
    _tablename: str = "APP_CONFIG"
    config_uid_pk: str = ''
    version_id: str = ''
    root_dir: str = ''
    bin_dir: str = ''
    mem_dir: str = ''
    cfg_dir: str = ''
    dat_dir: str = ''
    img_dir: str = ''
    py_dir: str = ''
    db_dir: str = ''
    sch_dir: str = ''
    log_dat: str = ''
    mon_dat: str = ''
    dbg_dat: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(AppConfig)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"config_uid_pk": ["config_uid_pk"]}
        ORDER: list = ["version_id ASC"]


class Texts(object):
    """Define static text strings used in the game.
    - Text string UID PK - unique for text string + language
    - Real-world language of the text, eg, 'en', 'de', 'fr'.
    - Name of a text string, not unique since it can be repeated
      in different languages.
    - Text string value.
    """
    _tablename: str = "TEXTS"
    text_uid_pk: str = ''
    lang_code: str = ''
    text_name: str = ''
    text_value: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Texts)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"text_uid_pk": ["text_uid_pk"]}
        ORDER: list = ["text_name ASC", "lang_code ASC"]


class Frames(object):
    """Define the values for frames i.e., the outermost window.
    - Optionally may have size, info-bar and page-header
    - frame_name: name of app or sub-app that uses the frame,
       e.g. 'admin' or 'game'
    """
    _tablename: str = "FRAMES"
    frame_uid_pk: str = ''
    lang_uid_fk: str = ''
    app_catg: str = ''
    version_id: str = ''
    frame_name: str = ''
    frame_title: str = ''
    frame_desc: str = ''
    size_w: float = 0.0
    size_h: float = 0.0
    ibar_x: float = 0.0
    ibar_y: float = 0.0
    pg_hdr_x: float = 0.0
    pg_hdr_y: float = 0.0
    pg_hdr_w: float = 0.0
    pg_hdr_h: float = 0.0
    pg_hdr_txt: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Frames)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"frame_uid_pk": ["frame_uid_pk"]}
        FK: dict = {"lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        CK: dict = {"app_catg": EntityType.APP_CATEGORY}
        ORDER: list = ["app_catg ASC", "frame_name ASC", "version_id ASC"]


class Windows(object):
    """Define the values for screens within the game.
    - Window UID PK - unique for window
    - Version ID
    - Window category: admin, game, etc.
    - Window name
    - Window title
    - x, y, w, h, margin
    """
    _tablename: str = "WINDOWS"
    win_uid_pk: str = ''
    frame_uid_fk: str = ''
    lang_uid_fk: str = ''
    version_id: str = ''
    win_name: str = ''
    win_title: str = ''
    win_x: float = 0.0
    win_y: float = 0.0
    win_w: float = 0.0
    win_h: float = 0.0
    win_margin: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Windows)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"win_uid_pk": ["win_uid_pk"]}
        FK: dict = {"frame_uid_fk": ("FRAMES", "frame_uid_pk"),
                    "lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        ORDER: list = ["win_name ASC", "version_id ASC"]


class Links(object):
    """Define the values for URIs used in the app.
    """
    _tablename: str = "LINKS"
    link_uid_pk: str = ''
    version_id: str = ''
    lang_uid_fk: str = ''
    link_catg: str = ''
    link_name: str = ''
    link_value: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Links)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"link_uid_pk": ["link_uid_pk"]}
        FK: dict = {"lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        CK: dict = {"link_catg": EntityType.LINK_CATEGORY}
        ORDER: list = ["link_catg ASC", "link_name ASC", "version_id ASC"]


class MenuBars(object):
    """Define the values for Menu Bars (dimensions only) used in the game.
    - menu_bar_name: what app or sub-app uses this menu bar,
       e.g., 'admin' or 'game'
    """
    _tablename: str = "MENU_BARS"
    menu_bar_uid_pk: str = ''
    frame_uid_fk: str = ''
    version_id: str = ''
    menu_bar_name: str = ''
    link_value: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(MenuBars)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"menu_bar_uid_pk": ["menu_bar_uid_pk"]}
        FK: dict = {"frame_uid_fk": ("FRAMES", "frame_uid_pk")}
        ORDER: list = ["menu_bar_name ASC", "version_id ASC"]


class Menus(object):
    """Define the values for Menus, i.e, name of a dropdown.
    - menu_id: generic string label "ID" or key for menu
    - menu_name: text string label for menu in designated language
    """
    _tablename: str = "MENUS"
    menu_uid_pk: str = ''
    menu_bar_uid_fk: str = ''
    lang_uid_fk: str = ''
    version_id: str = ''
    menu_id: str = ''
    menu_name: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Menus)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"menu_uid_pk": ["menu_uid_pk"]}
        FK: dict = {"menu_bar_uid_fk": ("MENU_BARS", "menu_bar_uid_pk"),
                    "lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        ORDER: list = ["menu_id ASC", "menu_name ASC"]


class MenuItems(object):
    """Define the values for Menu Items, i.e, each item on a menu.
    - item_id: generic string label "ID" or key for menu item
    - item_name: text string label for menu in designated language
    """
    _tablename: str = "MENU_ITEMS"
    item_uid_pk: str = ''
    menu_uid_fk: str = ''
    lang_uid_fk: str = ''
    version_id: str = ''
    item_id: str = ''
    item_order: int = 0
    item_name: str = ''
    help_text: str = ''
    enabled_default: bool = True

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(MenuItems)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"item_uid_pk": ["item_uid_pk"]}
        FK: dict = {"menu_uid_fk": ("MENUS", "menu_uid_pk"),
                    "lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        ORDER: list = ["item_id ASC", "item_name ASC"]


# =============================================================
# Game Astronomy
# =============================================================
class Universe(object):
    """Define qualities of a game Universe.
    This is the highest, broadest container in the game model.
    A Universe may contain multiple Galactic Clusters.
    It is conceptualized as a sphere.
    """
    _tablename: str = "UNIVERSE"
    univ_uid_pk: str = ''
    univ_name: str = ''
    radius_gly: float = 0.0
    volume_gly3: float = 0.0
    volume_pc3: float = 0.0
    age_gyr: float = 0.0
    expansion_rate_kmpsec_per_mpc: float = 0.0
    total_mass_kg: float = 0.0
    dark_energy_kg: float = 0.0
    dark_matter_kg: float = 0.0
    baryonic_matter_kg: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Universe)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"univ_uid_pk": ["univ_uid_pk"]}
        ORDER: list = ["univ_name ASC"]


class ExternalUniv(object):
    """The External Universe just defines qualities of the Game
    Universe that lie outside of the "playable" Universe. An External
    Universe is always 1:1 to a Universe. It has no shape, only mass.
    """
    _tablename: str = "EXTERNAL_UNIVERSE"
    external_univ_uid_pk: str = ''
    univ_uid_fk: str = ''
    external_univ_name: str = ''
    mass_kg: float = 0.0
    dark_energy_kg: float = 0.0
    dark_matter_kg: float = 0.0
    baryonic_matter_kg: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(ExternalUniv)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"external_univ_uid_pk": ["external_univ_uid_pk"]}
        FK: dict = {"univ_uid_fk": ("UNIVERSE", "univ_uid_pk")}
        ORDER: list = ["external_univ_name ASC"]


class GalacticCluster(object):
    """The Galactic Cluster defines a section of the Game Universe
    in which a particular game instance is played. A Galactic Cluster
    is contained by one Universe and it may contain multiple Galaxies.
    Conceptualized as a bulging shape, usually ellipsoid, centered in
    a boundary box.

    @DEV:
    - This and following models use GROUPed data structures. Those
      are not supported natively in SQLite. Consider simplifying and
      just defining columns in the model that are not GROUPed.
    - An alternative would be to convert the grouped set back into
      the data structure object when reading from the DB.
    """
    _tablename: str = "GALACTIC_CLUSTER"
    galactic_cluster_uid_pk: str = ''
    univ_uid_fk: str = ''
    galactic_cluster_name: str = ''
    center_from_univ_center_gly: Struct.CoordXYZ = Struct.CoordXYZ()
    boundary_gly: Struct.Game3DLocation = Struct.Game3DLocation()
    cluster_shape: str = 'ellipsoid'
    shape_pc: Struct.CoordXYZ = Struct.CoordXYZ()
    shape_axes: Struct.AxesABC = Struct.AxesABC()
    shape_rot: Struct.PitchYawRollAngle = Struct.PitchYawRollAngle()
    volume_pc3: float = 0.0
    mass_kg: float = 0.0
    dark_energy_kg: float = 0.0
    dark_matter_kg: float = 0.0
    baryonic_matter_kg: float = 0.0
    timing_pulsar_pulse_per_ms: float = 0.0
    timing_pulsar_loc_gly: Struct.CoordXYZ = Struct.CoordXYZ()

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(GalacticCluster)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"galactic_cluster_uid_pk": ["galactic_cluster_uid_pk"]}
        FK: dict = {"univ_uid_fk": ("UNIVERSE", "univ_uid_pk")}
        CK: dict = {"cluster_shape": EntityType.CLUSTER_SHAPE}
        GROUP: dict = {"center_from_univ_center_gly": Struct.CoordXYZ,
                       "boundary_gly": Struct.Game3DLocation,
                       "shape_pc": Struct.CoordXYZ,
                       "shape_axes": Struct.AxesABC,
                       "shape_rot":  Struct.PitchYawRollAngle,
                       "timing_pulsar_loc_gly": Struct.CoordXYZ}
        ORDER: list = ["galactic_cluster_name ASC"]


class Galaxy(object):
    """The Galaxy defines a section of the Galactic Cluster in
    which a particular game instance is played. A Galaxy is contained
    by a Galactic Cluster and it may contain multiple Star-Systems.
    Conceptualized as a sphere, centered in a boundary box.
    It has a bulge, typically ellipsoid, in the center and a star
    field area, also ellipsoid, but can include matter outside the
    star field, all the way to edge of its halo.

    Test data geenration via AI keeps crapping out on this one,
    the AI generation actually seems OK, but when I do the eval to
    turn it into code, it barfs on the "z" coordinate of the
    center_from_univ_center_kpc_z. I don't know why. It looks
    correct to me, assigned it a float value of, for example, 15.0
    The SQL identifies these as NUMERIC fields.

    An almost identical "grouped" structure is used in GalacticCluster
    and its data was generated and applied without any problem. Hmmm..
    I guess what I am seeing in the debug displays is that, instead of
    pulling the entire set of values into the test_set, it is breaking
    it into sub-sets. Like there are too many line breaks left after
    scrubbing? Nah..  I think I got it.  At some point I am stripping a
    comma that should not be stripped, when it precedes a line break.
    """
    _tablename: str = "GALAXY"
    galaxy_uid_pk: str = ''
    galactic_cluster_uid_fk: str = ''
    galaxy_name: str = ''
    relative_size: str = 'medium'
    center_from_univ_center_kpc: Struct.CoordXYZ = Struct.CoordXYZ()
    halo_radius_pc: float = 0.0
    boundary_pc: Struct.Game3DLocation = Struct.Game3DLocation()
    volume_gpc3: float = 0.0
    mass_kg: float = 0.0
    bulge_shape: str = 'ellipsoid'
    bulge_center_from_center_ly: Struct.CoordXYZ = Struct.CoordXYZ()
    bulge_dim_axes: Struct.AxesABC = Struct.AxesABC()
    bulge_dim_rot: Struct.PitchYawRollAngle = Struct.PitchYawRollAngle()
    bulge_black_hole_mass_kg: float = 0.0
    bulge_volume_ly3: float = 0.0
    bulge_total_mass_kg: float = 0.0
    star_field_shape: str = 'ellipsoid'
    star_field_dim_from_center_ly: Struct.CoordXYZ = Struct.CoordXYZ()
    star_field_dim_axes: Struct.AxesABC = Struct.AxesABC()
    star_field_dim_rot: Struct.PitchYawRollAngle = Struct.PitchYawRollAngle()
    star_field_vol_ly3: float = 0.0
    star_field_mass_kg: float = 0.0
    interstellar_mass_kg: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Galaxy)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"galaxy_uid_pk": ["galaxy_uid_pk"]}
        FK: dict = {"galactic_cluster_uid_fk":
                    ("GALACTIC_CLUSTER",
                     "galactic_cluster_uid_pk")}
        CK: dict = {"relative_size": EntityType.RELATIVE_SIZE,
                    "bulge_shape": EntityType.ASTRO_SHAPE,
                    "star_field_shape": EntityType.ASTRO_SHAPE}
        GROUP: dict = {"center_from_univ_center_kpc": Struct.CoordXYZ,
                       "boundary_pc": Struct.Game3DLocation,
                       "bulge_center_from_center_ly": Struct.CoordXYZ,
                       "bulge_dim_axes": Struct.AxesABC,
                       "bulge_dim_rot": Struct.PitchYawRollAngle,
                       "star_field_dim_from_center_ly": Struct.CoordXYZ,
                       "star_field_dim_axes": Struct.AxesABC,
                       "star_field_dim_rot": Struct.PitchYawRollAngle}
        ORDER: list = ["galaxy_name ASC"]


"""
Notes for generating star systems, planets, and other objects.

For a simplified star system generation algorithm that balances storytelling
and basic simulation, consider the following critical data elements:

    Star Type:
        Spectral Class: O, B, A, F, G, K, M (from hottest to coolest).
        O - Blue
        B - Blue-White
        A - White
        F - Yellow-White
        G - Yellow (like the Sun)
        K - Orange
        M - Red
        Luminosity: Brightness of the star.
        I - Supergiant = 1000-10000Ls
        II - Bright Giant = 100-1000Ls
        III - Giant = 10-100Ls
        IV - Subgiant = 1-10Ls
        V - Main Sequence = ~1Ls (Ls = Luminosity of the Sun)

    Planetary Orbits:
        Habitable Zone: Distance range from the star where conditions could
        support liquid water.
        Distribution of Planets: Inner rocky planets, outer gas giants.
        Orbital Eccentricity: How elliptical or circular the orbits are.

    Planetary Characteristics:
        Size and Mass: Determines gravity and atmosphere retention.
        Atmosphere Composition: Essential for life support.
        Surface Conditions: Temperature, pressure, and climate.
        Axial Tilt: Influences seasons and climate variations.
        Natural Satellites: Presence of moons.

    Asteroid Belts and Comets:
        Distribution: Inner, outer, or multiple belts.
        Density: Sparse or dense with potential impact events.

    Star System Dynamics:
        Binary/Multiple Star Systems:
          Presence of companion stars.
        Stability: Long-term stability of planetary orbits.
        Age of the Star: Influences the evolution of planets
        and potential for life.
            Spectral types O, B, and A represent "young" stars.
                years? 1-10 million years
            Spectral types F, G, and K represent
            "middle-aged" stars.
                years? 1-10 billion years
            Spectral type M represents "old" stars.
                years? 1-10 trillion years

    Exotic Elements:
        Presence of Anomalies: Unusual phenomena, e.g.,
        pulsars, black holes.
        Unstable Conditions: Solar flares, intense radiation.

    Historical Events:
        Past Catastrophes: Previous asteroid impacts, major
        events.
        Evolutionary Factors: Historical conditions affecting
        life evolution.

    Special Conditions:
        Tidally Locked Planets: Planets with one side
        permanently facing the star.
        Rogue Planets: Unbound to any star.

    Metadata for Storytelling:
        Dominant Species: If there is intelligent life, their
        characteristics.
        Cultural Factors: Influences on civilizations.
        Current State: Technological level, conflicts,
        alliances.

    Visual Characteristics:
        Sky Colors: Affected by atmospheric composition.
        Day/Night Lengths: Influences daily life.
"""


class StarSystem(object):
    """A Star System is a collection of planets, moons, and other objects.
    Usually it has one star, but it can have multiple stars.
    In most cases, we are only interested in star systems that include
    at least one habitable planet, but we can include others.
    Conceptualized as a bulging shape, usually ellipsoid, centered in
    a boundary box.
    """
    _tablename: str = "STAR_SYSTEM"
    star_system_uid_pk: str = ''
    galaxy_uid_fk: str = ''
    star_system_name: str = ''
    is_black_hole: bool = False
    is_pulsar: bool = False
    boundary_pc: Struct.Game3DLocation = Struct.Game3DLocation()
    volume_pc3: float = 0.0
    mass_kg: float = 0.0
    system_shape: str = 'ellipsoid'
    center_from_galaxy_center_pc: Struct.CoordXYZ = Struct.CoordXYZ()
    system_dim_axes: Struct.AxesABC = Struct.AxesABC()
    system_dim_rot: Struct.PitchYawRollAngle = Struct.PitchYawRollAngle()
    relative_size: str = 'medium'
    spectral_class: str = 'G'
    aprox_age_gyr: float = 0.0
    luminosity_class: str = 'V'
    frequency_of_flares: str = 'rare'
    intensity_of_flares: str = 'low'
    frequency_of_comets: str = 'rare'
    unbound_planets_cnt: int = 0
    orbiting_planets_cnt: int = 0
    inner_habitable_boundary_au: float = 0.0
    outer_habitable_boundary_au: float = 0.0
    planetary_orbits_shape: str = 'circular'
    orbital_stability: str = 'stable'
    asteroid_belt_density: str = 'sparse'
    asteroid_belt_loc: str = 'inner'

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(StarSystem)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"star_system_uid_pk": ["star_system_uid_pk"]}
        FK: dict = {"galaxy_uid_fk": ("GALAXY", "galaxy_uid_pk")}
        CK: dict = {"relative_size": EntityType.RELATIVE_SIZE,
                    "spectral_class": EntityType.SPECTRAL_CLASS,
                    'luminosity_class': EntityType.LUMINOSITY_CLASS,
                    "system_shape": EntityType.ASTRO_SHAPE,
                    "planetary_orbits_shape": EntityType.ORBITAL_SHAPE,
                    "orbital_stability": EntityType.STABILITY,
                    "asteroid_belt_density": EntityType.DENSITY,
                    'asteroid_belt_loc': EntityType.ASTRO_LOCATION,
                    "frequency_of_flares": EntityType.FREQUENCY,
                    "intensity_of_flares": EntityType.INTENSITY,
                    "frequency_of_comets": EntityType.FREQUENCY}
        GROUP: dict = {"boundary_pc": Struct.Game3DLocation,
                       "center_from_galaxy_center_pc": Struct.CoordXYZ,
                       "system_dim_axes": Struct.AxesABC,
                       "system_dim_rot": Struct.PitchYawRollAngle}
        ORDER: list = ["star_system_name ASC"]


"""
Planetary charts, indicating the path of 'wanderers' and their
'congruences', and so on as seen from the perspective of a given
world, will be tracked on a separate DB table or set of tables.
Such charts would include the path of comets and rogue planets,
unless I decide to track those on yet another table or set of tables.

Tracking of seasons and accounting of calendars will also be
handled on separate tables.  The same is true for tracking
of eclipses and other astronomical events. In each case, such
"charts" are contained by a World object.
"""


class World(object):
    """
    A World is a planet within a Star System. It may be habitable or not.
    """
    _tablename: str = "WORLD"
    world_uid_pk: str = ''
    star_system_uid_fk: str = ''
    world_name: str = ''
    world_type: str = 'habitable'
    obliquity_dg: float = 0.0    # a/k/a axial tilt
    distance_from_star_au: float = 0.0
    distance_from_star_km: float = 0.0
    radius_km: float = 0.0
    mass_kg: float = 0.0
    gravity_m_per_s_per_s: float = 0.0
    orbit_gdy: float = 0.0
    orbit_gyr: float = 0.0
    is_tidally_locked: bool = False
    rotation_gdy: float = 0.0
    rotation_direction: str = 'prograde'
    orbit_direction: str = 'prograde'
    moons_cnt: int = 0
    world_desc: str = ''
    atmosphere: str = ''
    sky_color: str = 'blue'
    biosphere: str = ''
    sentients: str = ''
    climate: str = ''
    tech_level: str = ''
    terrain: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(World)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"world_uid_pk": ["world_uid_pk"]}
        FK: dict = {"star_system_uid_fk":
                    ("STAR_SYSTEM", "star_system_uid_pk")}
        CK: dict = {"world_type": EntityType.WORLD_TYPE,
                    "rotation_direction": EntityType.ASTRO_DIRECTION,
                    "orbit_direction": EntityType.ASTRO_DIRECTION}
        ORDER: list = ["world_name ASC"]


class Moon(object):
    """
    A Moon is any type of satellite around a World.
    A Moon is associated with one World, and multiple Moons can be
    associated with one World.
    """
    _tablename: str = "MOON"
    moon_uid_pk: str = ''
    world_uid_fk: str = ''
    moon_name: str = ''
    center_from_world_center_km: Struct.CoordXYZ
    mass_kg: float = 0.0
    radius_km: float = 0.0
    obliquity_dg: float = 0.0    # a/k/a axial tilt
    is_tidally_locked: bool = True
    rotation_direction: str = 'prograde'
    orbit_direction: str = 'prograde'
    orbit_world_days: float = 0.0
    rotation_world_days: float = 0.0
    initial_velocity: float = 0.0
    angular_velocity: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Moon)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"moon_uid_pk": ["moon_uid_pk"]}
        FK: dict = {"world_uid_fk": ("WORLD", "world_uid_pk")}
        CK: dict = {"rotation_direction": EntityType.ASTRO_DIRECTION,
                    "orbit_direction": EntityType.ASTRO_DIRECTION}
        GROUP: dict = {"center_from_world_center_km": Struct.CoordXYZ}
        ORDER: list = ["moon_name ASC"]


# =============================================================
# Time
# =============================================================
class SolarYear(object):
    """
    A Solar Year is always associated with a World, within a
    given Star System and that world's star is the reference.
    Indicate how leaps are handled in terms of fractional days.
    Revolution and rotation of the World
    can be computed based on World structure and does
    not need to be entered directly, though it may save
    a little processing to do so.
    This is astronomical data, not a Calendar definition.
    - solar_year_span: number of solar revolutions in
      the year. Typically this is 1. But I have cultures
      (terpins) that count as 1 "year" 4 solar years. This
      way they don't account for leap days/years in the
      same way.
    """
    _tablename: str = "SOLAR_YEAR"
    solar_year_uid_pk: str = ''
    world_uid_fk: str = ''
    lang_uid_fk: str = ''
    solar_year_key: str = ''
    version_id: str = ''
    solar_year_name: str = ''
    solar_year_desc: str = ''
    days_in_solar_year: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(SolarYear)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"solar_year_uid_pk": ["solar_year_uid_pk"]}
        FK: dict = {"world_uid_fk": ("WORLD", "world_uid_pk"),
                    "lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        ORDER: list = ["solar_year_key ASC", "version_id ASC"]


class Season(object):
    """
    A Season defines the length of a season as proportion
    of a Solar year.
    It is categoriezed as one or more of the seasons in common
    use on Earth, which are defined as a type category.
    Seaons also vary depending on which hemisphere they relate
    to, also defined as a type.
    Names of seasons are handled as foreign keys to a common
    glossary item.
    """
    _tablename: str = "SEASON"
    season_uid_pk: str = ''
    solar_year_uid_fk: str = ''
    gloss_common_uid_fk: str = ''
    version_id: str = ''
    season_type: str = ''
    hemisphere_type: str = ''
    years_in_season: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Season)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"season_uid_pk": ["season_uid_pk"]}
        FK: dict = {"solar_year_uid_fk": ("SOLAR_YEAR", "solar_year_uid_pk"),
                    "gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        CK: dict = {"season_type": EntityType.SEASON_TYPE,
                    "hemisphere_type": EntityType.HEMISPHERE_TYPE}
        ORDER: list = ["season_uid_pk ASC", "season_type ASC"]


class LunarYear(object):
    """
    A Lunar Year is always associated with a World, within a
    given Star System. And with one or more lunar cycles.

    Which of the World's moons are being referenced is
    hanlded by the LunarYearXMoons association table.

    Duration of each moon's revolution around the world and
    its relative position per other satellites will be handled
    by computations. The LunarYear table contains the total
    number of days in the lunar year, whether it is based on
    a single satellite or a comoposite. The day is always in
    relation to the world's rotation w/r/t iits sun.

    The Lunar Year is astronomical data and not a Calendar.
    """
    _tablename: str = "LUNAR_YEAR"
    lunar_year_uid_pk: str = ''
    world_uid_fk: str = ''
    lang_uid_fk: str = ''
    lunar_year_key: str = ''
    version_id: str = ''
    lunar_year_name: str = ''
    lunar_year_desc: str = ''
    days_in_lunar_year: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LunarYear)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lunar_year_uid_pk": ["lunar_year_uid_pk"]}
        FK: dict = {"world_uid_fk": ("WORLD", "world_uid_pk"),
                    "lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        ORDER: list = ["lunar_year_key ASC", "version_id ASC"]


class LunarYearXMoon(object):
    """
    Associative keys --
    - LUNAR_YEARs (n) <--> MOONs (n)
    This table associates Lunar Year astro data with a
    specific moon.
    """
    _tablename: str = "LUNAR_YEAR_X_MOON"
    lunar_year_x_moon_uid_pk: str = ''
    lunar_year_uid_fk: str = ''
    moon_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LunarYearXMoon)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lunar_year_x_moon_uid_pk":
                    ["lunar_year_x_moon_uid_pk"]}
        FK: dict = {"lunar_year_uid_fk": ("LUNAR_YEAR",
                    "lunar_year_uid_pk"),
                    "moon_uid_fk": ("MOON", "moon_uid_pk")}


class SolarCalendar(object):
    """
    A Solar Calendar is a cultural artifact. It is associated with
    a Solar Year. The name of the calendar is defined as a link to
    a common glossary item.
    - epoch_start_offset: the first year in this system, in relationship
      to the default "epoch start" year for the game. Need to figure
      out how/where to define the epoch start for a given world.
    Months, Weeks, Days, Hours, etc are defined in distinct tables
    that are associated with Solar and/or Lunar Calendars.
    """
    _tablename: str = "SOLAR_CALENDAR"
    solar_calendar_uid_pk: str = ''
    solar_year_uid_fk: str = ''
    year_name_gloss_common_uid_fk: str = ''
    season_start_uid_fk: str = ''
    solar_calendar_id: str = ''
    solar_calendar_desc: str = ''
    version_id: str = ''
    epoch_start_offset: int = 0
    months_in_year: int = 0
    watches_in_day: int = 0
    hours_in_watch: int = 0
    minutes_in_hour: int = 0
    seconds_in_minute: int = 0
    leap_year: int = 0
    leap_month: int = 0
    leap_days: int = 0
    leap_rule: str = 'add_to_end_of_nth_month'

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(SolarCalendar)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"solar_calendar_uid_pk": ["solar_calendar_uid_pk"]}
        FK: dict = {"solar_year_uid_fk":
                    ("SOLAR_YEAR", "solar_year_uid_pk"),
                    "year_name_gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk"),
                    "season_start_uid_fk":
                    ("SEASON", "season_uid_pk")}
        CK: dict = {"leap_rule": EntityType.LEAP_RULE}
        ORDER: list = ["solar_calendar_id ASC", "version_id ASC"]


class LunarCalendar(object):
    """
    A Lunar Calendar is a cultural artifact associated with
    a Lunar Year. The name of the calendar is defined as a link to
    a common glossary item.
    - epoch_start_offset: the first year in this system, in relationship
      to the default "epoch start" year for the game. Need to figure
      out how/where to define the epoch start for a given world.
    Months, Weeks, Days, Hours, etc are defined in distinct tables
    that are associated with Solar and/or Lunar Calendars.

    """
    _tablename: str = "LUNAR_CALENDAR"
    lunar_calendar_uid_pk: str = ''
    lunar_year_uid_fk: str = ''
    year_name_gloss_common_uid_fk: str = ''
    lunar_calendar_id: str = ''
    lunar_calendar_desc: str = ''
    version_id: str = ''
    epoch_start_offset: int = 0
    days_in_month: int = 0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LunarCalendar)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lunar_calendar_uid_pk": ["lunar_calendar_uid_pk"]}
        FK: dict = {"lunar_year_uid_fk":
                    ("LUNAR_YEAR", "lunar_year_uid_pk"),
                    "year_name_gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        ORDER: list = ["lunar_calendar_id ASC", "version_id ASC"]


class Month(object):
    """
    A Month is associated with 1..n Calendars via an
    association table.
    - is_leap_day_month: true if the month contains leap day/s
    - is_leap_month: true if entire month is leap days
    """
    _tablename: str = "MONTH"
    month_uid_pk: str = ''
    month_name_gloss_common_uid_fk: str = ''
    month_id: str = ''
    version_id: str = ''
    days_in_month: int = 0
    months_number: int = 0
    is_leap_day_month: bool = False
    is_leap_month: bool = False

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Month)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"month_uid_pk": ["month_uid_pk"]}
        FK: dict = {"month_name_gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        ORDER: list = ["month_id ASC", "version_id ASC"]


class SolarCalendarXMonth(object):
    """
    Associative keys --
    - SOLAR_CALENDARs (n) <--> MONTHs (n)
    This table associates Solar Calendar data with a
    set of Months.
    """
    _tablename: str = "SOLAR_CALENDAR_X_MONTH"
    solar_calendar_x_moon_uid_pk: str = ''
    solar_calendar_uid_fk: str = ''
    month_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(SolarCalendarXMonth)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"solar_calendar_x_moon_uid_pk":
                    ["solar_calendar_x_moon_uid_pk"]}
        FK: dict = {"solar_calendar_uid_fk": ("SOLAR_CALENDAR",
                    "solar_calendar_uid_pk"),
                    "month_uid_fk": ("MONTH", "month_uid_pk")}


class LunarCalendarXMonth(object):
    """
    Associative keys --
    - LUNAR_CALENDARs (n) <--> MONTHs (n)
    This table associates Lunar Calendar data with a
    set of Months.
    """
    _tablename: str = "LUNAR_CALENDAR_X_MONTH"
    lunar_calendar_x_moon_uid_pk: str = ''
    lunar_calendar_uid_fk: str = ''
    month_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LunarCalendarXMonth)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lunar_calendar_x_moon_uid_pk":
                    ["lunar_calendar_x_moon_uid_pk"]}
        FK: dict = {"lunar_calendar_uid_fk": ("LUNAR_CALENDAR",
                    "lunar_calendar_uid_pk"),
                    "month_uid_fk": ("MONTH", "month_uid_pk")}


class WeekTime(object):
    """
    WeekTime is associated with 1..n Calendars via an
    association table.
    It describes any reckoning of days that is
    shorter than an average month. It is not necessarily
    the 7 days we are accustomed to. It could be a fortnight,
    a special 5 day week, or a 3 day holiday week.
    - week_time_number: optional; order of week if multiples
    - is_leap_week_time: true if the week contains only leap day/s
    """
    _tablename: str = "WEEK_TIME"
    week_time_uid_pk: str = ''
    week_time_name_gloss_common_uid_fk: str = ''
    week_time_desc: str = ''
    week_time_id: str = ''
    version_id: str = ''
    days_in_week_time: int = 0
    week_time_number: int = 0
    is_leap_week_time: bool = False

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(WeekTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"week_time_uid_pk": ["week_time_uid_pk"]}
        FK: dict = {"week_time_name_gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        ORDER: list = ["week_time_id ASC", "version_id ASC"]


class SolarCalendarXWeekTime(object):
    """
    Associative keys --
    - SOLAR_CALENDARs (n) <--> WEEK_TIMEs (n)
    This table associates Solar Calendar data with a
    set of Week Times.
    """
    _tablename: str = "SOLAR_CALENDAR_X_WEEK_TIME"
    solar_calendar_x_week_time_uid_pk: str = ''
    solar_calendar_uid_fk: str = ''
    week_time_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(SolarCalendarXWeekTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"solar_calendar_x_week_time_uid_pk":
                    ["solar_calendar_x_week_time_uid_pk"]}
        FK: dict = {"solar_calendar_uid_fk": ("SOLAR_CALENDAR",
                    "solar_calendar_uid_pk"),
                    "week_time_uid_fk": ("WEEK_TIME", "week_time_uid_pk")}


class LunarCalendarXWeekTime(object):
    """
    Associative keys --
    - LUNAR_CALENDARs (n) <--> WEEK_TIMEs (n)
    This table associates Lunar Calendar data with a
    set of Week Times.
    """
    _tablename: str = "LUNAR_CALENDAR_X_WEEK_TIME"
    lunar_calendar_x_week_time_uid_pk: str = ''
    lunar_calendar_uid_fk: str = ''
    week_time_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LunarCalendarXWeekTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lunar_calendar_x_week_time_uid_pk":
                    ["lunar_calendar_x_week_time_uid_pk"]}
        FK: dict = {"lunar_calendar_uid_fk": ("LUNAR_CALENDAR",
                    "lunar_calendar_uid_pk"),
                    "week_time_uid_fk": ("WEEK_TIME", "week_time_uid_pk")}


class DayTime(object):
    """
    DayTime is associated with 1..n Weeks via an
    association table.
    It describes any reckoning of time construed in
    hours that is longer than one hour and not longer
    that a full day. It is not necessarily the 24 hours
    day we are accustomed to. It could be a 12 hour
    half-day, a 6 hour "watch" and so on.
    - day_time_number: order of day in a week
    - is_leap_day_time: true if the day is only a leap day
    """
    _tablename: str = "DAY_TIME"
    day_time_uid_pk: str = ''
    day_time_name_gloss_common_uid_fk: str = ''
    day_time_desc: str = ''
    day_time_id: str = ''
    version_id: str = ''
    hours_in_day_time: int = 0
    day_time_number: int = 0
    is_leap_day_time: bool = False

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(DayTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"day_time_uid_pk": ["day_time_uid_pk"]}
        FK: dict = {"day_time_name_gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        ORDER: list = ["day_time_id ASC", "version_id ASC"]


class WeekTimeXDayTime(object):
    """
    Associative keys --
    - WEEK_TIMEs (n) <--> DAY_TIMEs (n)
    This table associates Week Time data with a
    set of Day Times.
    """
    _tablename: str = "WEEK_TIME_X_DAY_TIME"
    week_time_x_day_time_uid_pk: str = ''
    week_time_uid_fk: str = ''
    day_time_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(WeekTimeXDayTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"week_time_x_day_time_uid_pk":
                    ["week_time_x_day_time_uid_pk"]}
        FK: dict = {"week_time_uid_fk": ("WEEK_TIME", "week_time_uid_pk"),
                    "day_time_uid_fk": ("DAY_TIME", "day_time_uid_pk")}


# Next: Hours, Scenes, Locations, Buildings, Sets, Characters, Inventories,
#  Services, etc.
# Come back and add these (and maybe more) afer doing some more work on tying
# the front end and middle ware to the new database and data model, including
# generation of initial set-up data. Maybe do some implementation on the
# financial app too.


# =============================================================
# Abstract Maps and Grids
# =============================================================
class Map(object):
    """
    Map is a rectangle or box.
    A map rectangle is defined as a game-world geo location.
    A map box is defined as an astronomical, undersea or underground
    3D location.

    This structure is for defining 'templates' of maps
        that lay over a grid. For example, there might be
        a map_name that is associated with provinces and
        a different one that is associated with regions.
        There could also be multiple variations of, say,
        county-level maps, depending on large or small.
    It will be associated with another table w/ more detailed info
    relating to things like:
        - geography (continents, regions, mountains, hills, rivers,
            lakes, seas, oceans, etc.)
        - political boundaries (countries, provinces, states, counties, etc.)
        - roads, paths, trails, waterways, bodies of water, etc.
        - cities, towns, villages, neighborhoods, etc.
        - other points of interest (ruins, temples, etc.)
        - natural resources (mines, quarries, etc.)
        - demographics (population density, etc.)

    - Maps can also contain other maps, overlap with other maps, border
      other maps, provide layers of information, or provide geo-layers
      associatd with other maps. These relationships are handled in
      the MapXMap table (see below)
    """
    _tablename: str = "MAP"
    map_uid_pk: str = ''
    map_name: str = ''
    map_type: str = ''
    geo_map_loc: Struct.GameGeoLocation = Struct.GameGeoLocation()
    three_d_map_loc: Struct.Game3DLocation = Struct.Game3DLocation()

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Map)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"map_uid_pk": ["map_uid_pk"]}
        CK: dict = {"map_type": EntityType.MAP_TYPE}
        GROUP: dict = {"geo_map_loc": Struct.GameGeoLocation,
                       "three_d_map_loc": Struct.Game3DLocation}
        ORDER: list = ["map_name ASC"]


class MapXMap(object):
    """
    Associative keys --
    - MAPs (n) <--> MAPs (n)
    The "touch type" should be read in direction 1-->2.
    For example, 1-contains-2, 1-is_contained_by-2, etc.
    """
    _tablename: str = "MAP_X_MAP"
    map_x_map_uid_pk: str = ''
    map_uid_1_fk: str = ''
    map_uid_2_fk: str = ''
    touch_type: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(MapXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"map_x_map_uid_pk": ["map_x_map_uid_pk"]}
        FK: dict = {"map_uid_1_fk": ("MAP", "map_uid_pk"),
                    "map_uid_2_fk": ("MAP", "map_uid_pk")}
        CK: dict = {"touch_type": EntityType.MAP_TOUCH_TYPE}


class Grid(object):
    """
    The "Grid" table defines the dimensions of a Map.

    Define the size of a grid (r, c), the dim of the cells (w, h, z)
    in PyGame px, and the dim of each cell in km (w, h) or m (z).
    The z layers are provided to track altitude, depth, or elevation
    for maps that provide z-level data.

    Associations with map(s) are handled in GridXMap table.

    @DEV:
    - Consider other grid shapes, such as hexagonal, triangular, etc.
    """
    _tablename: str = "GRID"
    grid_uid_pk: str = ''
    grid_name: str = ''
    row_cnt: int = 0
    col_cnt: int = 0
    z_up_cnt: int = 0
    z_down_cnt: int = 0
    width_px: float = 0.0
    height_px: float = 0.0
    width_km: float = 0.0
    height_km: float = 0.0
    z_up_m: float = 0.0
    z_down_m: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Grid)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"grid_uid_pk": ["grid_uid_pk"]}
        ORDER: list = ["grid_name ASC"]


class GridXMap(object):
    """
    Associative keys --
    - GRIDs (n) <--> MAPs (n)
    """
    _tablename: str = "GRID_X_MAP"
    grid_x_map_uid_pk: str = ''
    grid_uid_fk: str = ''
    map_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(GridXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"grid_x_map_uid_pk": ["grid_x_map_uid_pk"]}
        FK: dict = {"grid_uid_fk":
                    ("GRID", "grid_uid_pk"),
                    "map_uid_fk":
                    ("MAP", "map_uid_pk")}


# =============================================================
# Semantics and Languages
# =============================================================
class CharSet(object):
    """
    Description of a set of characters used in a language.
    An alphabet represents consonants and vowels each
    separately as individual letters.
    An abjad represents consonants only as distinct letters;
    vowels are represented as diacritics. In some cases, the
    vowels may be omitted entirely, and are implied from
    context .
    An abugida represents consonants as separate letters, but
    the glyph used also implies a “default” vowel, and deletion
    or change of vowel is represented with modifications of the
    glyph, in a fashion similar to diacritics, but not the same.
    A syllabary represents a syllable of the language - usually
    but not invariably in the form CV (consonant followed by
    vowel) - as a single glyph; there is no necessary
    relationship between glyphs that carry the same consonant,
    or the same vowel.
    Ideograms use a single - often complex - glyph to represent
    a word or concept. In some languages, the ideogram may
    actually be compound, with one portion signalling the
    pronunciation, and another portion signalling the meaning.
    """
    _tablename: str = "CHAR_SET"
    char_set_uid_pk: str = ''
    char_set_name: str = ''
    char_set_type: str = 'alphabet'
    char_set_desc: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(CharSet)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"char_set_uid_pk": ["char_set_uid_pk"]}
        CK: dict = {"char_set_type": EntityType.CHAR_SET_TYPE}
        ORDER: list = ["char_set_name ASC"]


class CharMember(object):
    """
    Describe individual characters in a character set.
    Where the character is not represented in Unicode, a reference
    to a picture of the characteris stored, along with name and
    description.
    Member types are defined by the type of writing system
    (character set) they belong to. Further categorizations
    are possible for numerics, punctuation, and so on.
    """
    _tablename: str = "CHAR_MEMBER"
    char_member_uid_pk: str = ''
    char_set_uid_fk: str = ''
    char_member_name: str = ''
    char_member_uri: str = ''
    char_member_desc: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(CharMember)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"char_member_uid_pk": ["char_member_uid_pk"]}
        FK: dict = {"char_set_uid_fk": ("CHAR_SET", "char_set_uid_pk")}
        ORDER: list = ["char_member_name ASC"]


class LangFamily(object):
    """
    Describe basic features of a language family, without getting too
    complicated.
    - desc: overview
    - phonetics: how the language sounds, e.g. guttural, nasal, etc.
    - cultural influences: e.g. from other languages, or from
      historical events, migration patterns, etc.
    """
    _tablename: str = "LANG_FAMILY"
    lang_family_uid_pk: str = ''
    char_set_uid_fk: str = ''
    lang_family_name: str = ''
    lang_family_desc: str = ''
    phonetics: str = ''
    cultural_influences: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LangFamily)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lang_family_uid_pk": ["lang_family_uid_pk"]}
        FK: dict = {"char_set_uid_fk": ("CHAR_SET", "char_set_uid_pk")}
        ORDER: list = ["lang_family_name ASC"]


class Language(object):
    """
    Describe basic features of a language, without getting too
    complicated.
    - desc: overiew
    - gramatics: how phrases are generally structured,
        e.g. subject-verb-object
    - lexicals: major sources of lexicon, for example, lots of
        words relating to the sea, or to the sky, or to the
        land, or to the stars, or to the gods, etc.
    - social influences: e.g. from other languages, or from
        class, trade, migration patterns, etc.
    - word formations:  how words are generally structured,
        e.g. single-syllable-only, consonant-vowel-consonant,
        multiples by prefix, etc.
    More possible features:
/*
lang_object structure:
{"glossary":
    {"phrase": "definition", ...},
 "lexicon":
    {"word": "definition", ...},
 "grammar":
    # the entire structure of a language, includes most of the
    following,
    # as well as things like rules for making plurals, etc.
    {"rule": "explanation", ...},
 "phonology":
   # distribtution of phonemes (sounds) in a language
    {"rule": "explanation", ...},
 "morphology":
   # how words are constructed from morphemes (smallest units
   of meaning)
    {"rule": "explanation", ...},
 "syntax":
    # how words are combined into phrases and sentences
    {"rule": "explanation", ...},
 "semantics":
    {"rule": "explanation", ...},
 "pragmatics":
   # how context affects meaning, for example, intention,
   social status, etc.
    {"rule": "explanation", ...},
 "orthography":
   # how a language is written, for example, alphabet,
   syllabary, etc.
    {"rule": "explanation", ...},
    {"letter": "pronunciation", ...},
 "phonotactics":
    # how sounds are combined into syllables and words
     {"rule": "explanation", ...},
    {"rule": "explanation", ...},
*/
    """
    _tablename: str = "LANGUAGE"
    lang_uid_pk: str = ''
    lang_family_uid_fk: str = ''
    lang_name: str = ''
    lang_desc: str = ''
    gramatics: str = ''
    lexicals: str = ''
    social_influences: str = ''
    word_formations: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Language)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lang_uid_pk": ["lang_uid_pk"]}
        FK: dict = {"lang_family_uid_fk":
                    ("LANG_FAMILY", "lang_family_uid_pk")}
        ORDER: list = ["lang_name ASC"]


class LangDialect(object):
    """
    Describe basic features of a dialect, without getting too
    complicated.
    - divergence_factors: how the dialect differs from the
      main language, e.g. pronunciation, vocabulary, etc.
    - syncretic_factors: how the dialect is similar to or borrows
      from neighboring languages, e.g. pronunciation, vocabulary, ..
    - preservation_factors: how the dialect preserves old features
      of the main language which are no longer standard
    """
    _tablename: str = "LANG_DIALECT"
    dialect_uid_pk: str = ''
    lang_uid_fk: str = ''
    dialect_name: str = ''
    dialect_desc: str = ''
    divergence_factors: str = ''
    syncretic_factors: str = ''
    preservation_factors: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LangDialect)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"dialect_uid_pk": ["dialect_uid_pk"]}
        FK: dict = {"lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        ORDER: list = ["dialect_name ASC"]


class GlossCommon(object):
    """
    The common glossary is in the "common" language, e.g. English.
    It serves as the 'Rosetta Stone' for all other languages, first
    for in-game ones. It can also be used for real world languages, or
    as the top-level 'parent' for a cascade of info; for example, when
    they are multiple types of glossary items associated with a subject.
    The primary key of a GlossCommon row is the FK reference for related
    Glossary items.
    - gloss_name (required): either a single word, or title for a longer entry
    - gloss type (required): a word, phrase, weblink, graphic, data, software
    - gloss_value (optional): the definition of the word, phrase, etc. or a
      longer glossary entry, for example, describing a feature of the game
    - gloss_uri (optional): a URI for the glossary entry, a web page,
      a local file or external software/plug-in, a sound file, etc.
    """
    _tablename: str = "GLOSS_COMMON"
    gloss_common_uid_pk: str = ''
    dialect_uid_fk: str = ''
    gloss_type: str = ''
    gloss_name: str = ''
    gloss_value: str = ''
    gloss_uri: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(GlossCommon)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"gloss_common_uid_pk": ["gloss_common_uid_pk"]}
        FK: dict = {"dialect_uid_fk": ("LANG_DIALECT", "dialect_uid_pk")}
        CK: dict = {"gloss_type": EntityType.GLOSS_TYPE}
        ORDER: list = ["gloss_name ASC"]


class Glossary(object):
    """
    The glossary is a multi-lingual dictionary as well an extension
    for the GlossCommon items.
    """
    _tablename: str = "GLOSSARY"
    glossary_uid_pk: str = ''
    gloss_common_uid_fk: str = ''
    dialect_uid_fk: str = ''
    gloss_type: str = ''
    gloss_name: str = ''
    gloss_value: str = ''
    gloss_uri: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Glossary)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"glossary_uid_pk": ["glossary_uid_pk"]}
        FK: dict = {"gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk"),
                    "dialect_uid_fk": ("LANG_DIALECT", "dialect_uid_pk")}
        CK: dict = {"gloss_type": EntityType.GLOSS_TYPE}
        ORDER: list = ["gloss_name ASC"]


# =============================================================
# Game Geography
# =============================================================
class Lake(object):
    """
    Geographic features, e.g. lakes, rivers, mountains, are
    named by reference to a gloss_common_uid_pk.

    Geo features have a complex line defined by series of
    points, often defined by latitude and longitude.
    The more points, the more precise the curve or lines.
    Points stored as JSON with an undetermined length.
    SQL generator code identifies them via a classmethod
    constraint keyed by "JSON".' SQLite supports a JSON
    data type, but not sure yet what that buys us.

    catchment_area_radius_m: area of land where rainfall is
    collected and drained into the lake. Not same as
    the area of the lake itself. For game purposes,
    assume it is a circle with a radius.

    accessibility: How easy it is to reach the lake, whether
    roads, trails, or settlements nearby. Can be quantified
    as a number, or a word, or a phrase.

    special_features: Unique or notable features, like
    islands, underwater caves, or geothermal activity

    lake_usage:  fishing, recreation, transportation,
    as a water source for nearby settlements. Expand to
    more attributes like resevoir.

    conservation_status: Efforts to protect or preserve

    current_conditions: quality, temperature, frozen, etc.

    JSON:
    lake_shorline_points: [GeogLatLong, ..]
    """
    _tablename: str = "LAKE"
    lake_uid_pk: str = ''
    gloss_common_uid_fk: str = ''
    lake_shoreline_points_json: str = ''
    lake_size: str = "medium"
    water_type: str = "freshwater"
    lake_type: str = "lake"
    is_tidal_influence: bool = False
    lake_surface_m2: float = 0.0
    max_depth_m: float = 0.0
    avg_depth_m: float = 0.0
    lake_altitude_m: float = 0.0
    catchment_area_radius_m: float = 0.0
    lake_origin: str = ''
    flora_and_fauna: str = ''
    water_color: str = ''
    accessibility: str = ''
    special_features: str = ''
    lake_usage: str = ''
    legends_or_myths: str = ''
    lake_history: str = ''
    conservation_status: str = ''
    current_conditions: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(Lake)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lake_uid_pk": ["lake_uid_pk"]}
        FK: dict = {"gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        JSON: list = ["lake_shoreline_points_json"]
        CK: dict = {"lake_size": EntityType.LAKE_SIZE,
                    "water_type": EntityType.WATER_TYPE,
                    "lake_type": EntityType.LAKE_TYPE}
        ORDER: list = ["lake_uid_pk ASC"]


class LakeXMap(object):
    """
    Associative keys --
    - LAKEs (n) <--> MAPs (n)
    """
    _tablename: str = "LAKE_X_MAP"
    lake_x_map_pk: str = ''
    lake_uid_fk: str = ''
    map_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LakeXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"lake_x_map_pk": "lake_x_map_pk"}
        FK: dict = {"lake_uid_fk":
                    ("LAKE", "lake_uid_pk"),
                    "map_uid_fk":
                    ("MAP", "map_uid_pk")}
        ORDER: list =\
            ["lake_uid_fk ASC", "map_uid_fk ASC"]


class River(object):
    """
    drainage_basin_m: Avg area of land where rainfall is
    collected and drained into river on each bank. For game
    purposes, number of meters from center of river.

    avg_velocity_m_per_h: Meters per hour on avg. This is
    not the same as the max velocity, which is likely to be
    much higher.

    @DEV:
    - For river/lake and river/river and river/waterbody
    associations, may need to define additional
    association tables; and those tables may need to
    have some types associated with them. We want to
    avoid having any "null" FK's, since they are not
    supported by SQLite and it is bad practice to
    manage FK's without DB-level support for them.

    JSON:
    river_course_points: [lat-long, ...]
    river_bank_points: [lat-long, ...]
    "hazards": [{"uid": int,
                 "type": EntityType.RIVER_HAZARD,
                 "loc": lat-long},
                ...],
    "features": [{"uid": int,
                  "type": EntityType.RIVER_FEATURE,
                   "loc": lat-long}, ...]
    """
    _tablename: str = "RIVER"
    river_uid_pk: str = ''
    gloss_common_uid_fk: str = ''
    river_course_points_json: str = ''
    river_bank_points_json: str = ''
    river_type: str = 'perrenial'
    avg_width_m: float = 0.0
    avg_depth_m: float = 0.0
    total_length_km: float = 0.0
    drainage_basin_km: float = 0.0
    avg_velocity_m_per_h: float = 0.0
    gradient_m_per_km: float = 0.0
    river_hazards_json: str = ''
    river_features_json: str = ''
    river_nav_type: str = 'none'
    flora_and_fauna: str = ''
    water_quality: str = ''
    historical_events: str = ''
    current_conditions: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(River)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"river_uid_pk": "river_uid_pk"}
        FK: dict = {"gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        CK: dict = {"river_type":
                    EntityType.RIVER_TYPE,
                    "river_nav_type":
                    EntityType.RIVER_NAV_TYPE}
        JSON: list = ["river_course_points_json",
                      "river_bank_points_json",
                      "river_hazards_json",
                      "river_features_json"]
        ORDER: list =\
            ["river_uid_pk ASC"]


class RiverXMap(object):
    """
    Associative keys --
    - RIVERs (n) <--> MAPs (n)
    """
    _tablename: str = "RIVER_X_MAP"
    river_x_map_uid_pk: str = ''
    river_uid_fk: str = ''
    map_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(RiverXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"river_x_map_uid_pk":
                    "river_x_map_uid_pk"}
        FK: dict = {"river_uid_fk":
                    ("RIVER", "river_uid_pk"),
                    "map_uid_fk":
                    ("MAP", "map_uid_pk")}
        ORDER: list =\
            ["river_x_map_uid_pk ASC"]


class OceanBody(object):
    """For bodies of water associated with oceans.
    """
    _tablename: str = "OCEAN_BODY"
    ocean_body_uid_pk: str = ''
    gloss_common_uid_fk: str = ''
    body_shoreline_points_json: str = ''
    is_coastal: bool = True
    is_frozen: bool = False
    ocean_body_type: str = ''
    water_type: str = ''
    is_tidal_influence: bool = False
    tidal_flows_per_day: int = 0
    avg_high_tide_m: float = 0.0
    avg_low_tide_m: float = 0.0
    max_high_tide_m: float = 0.0
    ocean_wave_type: str = ''
    body_surface_area_m2: float = 0.0
    body_surface_altitude_m: float = 0.0
    max_depth_m: float = 0.0
    avg_depth_m: float = 0.0
    ocean_hazards_json: str = ''
    ocean_features_json: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(OceanBody)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"ocean_body_uid_pk":
                    "ocean_body_uid_pk"}
        FK: dict = {"gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        CK: dict = {"ocean_body_type":
                    EntityType.OCEAN_BODY_TYPE,
                    "water_type":
                    EntityType.WATER_TYPE,
                    "ocean_wave_type":
                    EntityType.OCEAN_WAVE_TYPE}
        JSON: list = ["river_course_points_json",
                      "river_bank_points_json",
                      "ocean_hazards_json",
                      "ocean_features_json"]
        ORDER: list =\
            ["ocean_body_uid_pk ASC"]


class OceanBodyXMap(object):
    """
    Associative keys --
    - OCEAN_BODY (n) <--> MAP (n)
    """
    _tablename: str = "OCEAN_BODY_X_MAP"
    ocean_body_x_map_uid_pk: str = ''
    ocean_body_uid_fk: str = ''
    map_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(OceanBodyXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"ocean_body_x_map_uid_pk":
                    "ocean_body_x_map_uid_pk"}
        FK: dict = {"ocean_body_uid_fk":
                    ("OCEAN_BODY", "ocean_body_uid_pk"),
                    "map_uid_fk":
                    ("MAP", "map_uid_pk")}
        ORDER: list =\
            ["ocean_body_x_map_uid_pk ASC"]


class OceanBodyXRiver(object):
    """
    Associative keys --
    - OCEAN_BODY (n) <--> RIVER (n)
    """
    _tablename: str = "OCEAN_BODY_X_RIVER"
    ocean_body_x_river_uid_pk: str = ''
    ocean_body_uid_fk: str = ''
    river_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(OceanBodyXRiver)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"ocean_body_x_river_uid_pk":
                    "ocean_body_x_river_uid_pk"}
        FK: dict = {"ocean_body_uid_fk":
                    ("OCEAN_BODY", "ocean_body_uid_pk"),
                    "river_uid_fk":
                    ("RIVER", "river_uid_pk")}
        ORDER: list =\
            ["ocean_body_x_river_uid_pk ASC"]


class LandBody(object):
    """
    Use this for geographic features that are not water.
    Including: continents, islands, geographic regions.
    """
    _tablename: str = "LAND_BODY"
    land_body_uid_pk: str = ''
    gloss_common_uid_fk: str = ''
    body_landline_points_json: str = ''
    land_body_type: str = ''
    land_body_surface_area_m2: float = 0.0
    land_body_surface_avg_altitude_m: float = 0.0
    max_altitude_m: float = 0.0
    min_altitude_m: float = 0.0

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LandBody)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"land_body_uid_pk":
                    "land_body_uid_pk"}
        FK: dict = {"gloss_common_uid_fk":
                    ("GLOSS_COMMON", "gloss_common_uid_pk")}
        CK: dict = {"land_body_type":
                    EntityType.LAND_BODY_TYPE}
        ORDER: list =\
            ["land_body_uid_pk ASC"]


class LandBodyXMap(object):
    """
    Associative keys --
    - LAND_BODY (n) <--> MAP (n)
    """
    _tablename: str = "LAND_BODY_X_MAP"
    land_body_x_map_uid_pk: str = ''
    land_body_uid_fk: str = ''
    map_uid_fk: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LandBodyXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"land_body_x_map_uid_pk":
                    "land_body_x_map_uid_pk"}
        FK: dict = {"land_body_uid_fk":
                    ("LAND_BODY", "land_body_uid_pk"),
                    "map_uid_fk":
                    ("MAP", "map_uid_pk")}
        ORDER: list =\
            ["land_body_x_map_uid_pk ASC"]


class LandBodyXLandBody(object):
    """
    Associative keys --
    - LAND_BODY (n) <--> LAND_BODY (n)
    - relation:
        - body 1 --> body 2
    """
    _tablename: str = "LAND_BODY_X_LAND_BODY"
    land_body_x_land_body_uid_pk: str = ''
    land_body_1_uid_fk: str = ''
    land_body_2_uid_fk: str = ''
    land_land_relation_type: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LandBodyXLandBody)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"land_body_x_land_body_uid_pk":
                    "land_body_x_land_body_uid_pk"}
        FK: dict = {"land_body_1_uid_fk":
                    ("LAND_BODY", "land_body_uid_pk"),
                    "land_body_2_uid_fk":
                    ("LAND_BODY", "land_body_uid_pk")}
        CK: dict = {"land_land_relation_type":
                    EntityType.LAND_LAND_RELATION_TYPE}
        ORDER: list =\
            ["land_body_x_land_body_uid_pk ASC"]


class LandBodyXOceanBody(object):
    """
    Associative keys --
    - LAND_BODY (n) <--> OCEAN_BODY (n)
    """
    _tablename: str = "LAND_BODY_X_OCEAN_BODY"
    land_body_x_ocean_body_uid_pk: str = ''
    land_body_uid_fk: str = ''
    ocean_body_uid_fk: str = ''
    land_ocean_relation_type: str = ''

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return _orm_to_dict(LandBodyXOceanBody)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return _orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"land_body_x_ocean_body_uid_pk":
                    "land_body_x_ocean_body_uid_pk"}
        FK: dict = {"land_body_uid_fk":
                    ("LAND_BODY", "land_body_uid_pk"),
                    "ocean_body_uid_fk":
                    ("OCEAN_BODY", "ocean_body_uid_pk")}
        CK: dict = {"land_ocean_relation_type":
                    EntityType.LAND_OCEAN_RELATION_TYPE}
        ORDER: list =\
            ["land_body_x_ocean_body_uid_pk ASC"]


# =======================================================
# DB/ORM Calls
# - Create SQL files
# - Create SQLITE tables
# =======================================================
class InitGameDB(object):
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
        """Initialize the InitGameDatabase object.
        """
        pass

    def create_sql(self):
        """Pass data object to create SQL files."""
        for model in [Backup, Universe, ExternalUniv,
                      GalacticCluster, Galaxy,
                      StarSystem, World, Moon,
                      Map, MapXMap, Grid, GridXMap,
                      CharSet, CharMember, LangFamily,
                      Language, LangDialect,
                      GlossCommon, Glossary,
                      Lake, LakeXMap,
                      River, RiverXMap,
                      OceanBody, OceanBodyXMap,
                      OceanBodyXRiver,
                      LandBody, LandBodyXMap,
                      LandBodyXLandBody, LandBodyXOceanBody,
                      AppConfig, Texts, Frames, Windows,
                      Links, MenuBars, Menus, MenuItems,
                      SolarYear, Season,
                      LunarYear, LunarYearXMoon,
                      SolarCalendar, LunarCalendar,
                      Month, LunarCalendarXMonth,
                      SolarCalendarXMonth,
                      WeekTime, LunarCalendarXWeekTime,
                      SolarCalendarXWeekTime,
                      DayTime, WeekTimeXDayTime]:
            DB.generate_sql(model)

    def boot_db(self,
                p_create_test_data: bool = False,
                p_backup_archive: bool = False):
        """
        Drops and recreates empty all DB tables.
        This is a destructive operation.
        - Backup DB if it exists.
        - Overlay .BAK copy of DB.
        Do not wipe out any existing archived DB's.
        - Logged records appear in .BAK, not in the
          refreshed database.
        :args:
        - p_create_test_data: bool. If True, create test data.
        - p_backup_archive: bool. If True, archive DB.
        """
        if p_backup_archive:
            file_path = Path(DB.DB)
            if file_path.exists():
                DB.backup_db()
                DB.archive_db()

        sql_list = [sql.name for sql in FI.scan_dir(DB.DB_PATH, 'DROP*')]
        DB.execute_dml(sql_list, p_foreign_keys_on=False)
        sql_list = [sql.name for sql in FI.scan_dir(DB.DB_PATH, 'CREATE*')]
        DB.execute_dml(sql_list, p_foreign_keys_on=True)

        if p_create_test_data:
            TD = TestData()
            for data_model in [Backup, Universe,
                               Map, Grid, CharSet,
                               ExternalUniv, GalacticCluster,
                               MapXMap, GridXMap, CharMember,
                               Galaxy, StarSystem,
                               World, Moon, LangFamily,
                               Language, LangDialect,
                               GlossCommon, Glossary,
                               Lake, LakeXMap,
                               River, RiverXMap,
                               OceanBody, OceanBodyXMap,
                               OceanBodyXRiver,
                               LandBody, LandBodyXMap,
                               LandBodyXLandBody,
                               LandBodyXOceanBody,
                               AppConfig, Texts, Frames, Windows,
                               Links, MenuBars, Menus, MenuItems,
                               SolarYear, Season,
                               LunarYear, LunarYearXMoon,
                               SolarCalendar, LunarCalendar,
                               Month, LunarCalendarXMonth,
                               SolarCalendarXMonth,
                               WeekTime, LunarCalendarXWeekTime,
                               SolarCalendarXWeekTime,
                               DayTime, WeekTimeXDayTime]:
                sql, values = TD.make_algo_test_data(data_model)
                for v in values:
                    DB.execute_insert(sql, v)


class TestData(object):
    """
    Managem test data rows on database
    """

    def __init__(self):
        """Initialize TestData object."""
        self.test_data_rows = 1
        self.table_name: str = ''
        self.sql_cols: list = []
        self.num_cols: int = 0
        self.ck_constraints: dict = {}
        self.fk_constraints: dict = {}

# =============================================================
# Algorithm-based TestData objects
# =============================================================
# =============================================================
# Abstracted 'private' methods
# =============================================================
    def _get_data_model(self,
                        p_data_model: object) -> bool:
        """Get data model info from object and CREATE SQL file.
        :args:
        - p_data_model: object.
        :sets:
        - class level attributes
        """
        self.table_name = p_data_model._tablename.upper()
        sql_create = DB.get_sql_file(f"CREATE_{self.table_name}")
        sql_line = sql_create.split('\n')
        self.sql_cols = [line.strip()[:-1] for line in sql_line
                         if not line.startswith(
                            ('--', 'CREATE', 'CHECK',
                             'FOREIGN', 'PRIMARY'))]
        self.num_cols = len(self.sql_cols)
        constraints = {k: v for k, v
                       in p_data_model.Constraints.__dict__.items()
                       if not k.startswith('_')}
        self.ck_constraints = constraints.get('CK', {})
        self.fk_constraints = constraints.get('FK', {})
        return True

    def _get_name_value(self,
                        p_row_num: int) -> str:
        """Return test data value for a name field
        :args:
        - p_row_num: int. Row number.
        :returns: str
        """
        v = f"test_{self.table_name.lower()}_{p_row_num:04d}"
        return v

    def _get_file_value(self) -> str:
        """Return test data value for a file field
        :returns: str
        """
        v = SI.get_cwd_home() + '/' + SI.get_uid()[10:17] + '/' +\
            random.choice(['test_data', 'other', 'config', 'backup']) +\
            random.choice(['.txt', '.jpg', '.png', '.pdf', '.dat', '.xls'])
        return v

    def _get_astro_value(self) -> float:
        """Return test data value for a kg, gly, gly3, pc3 field
        :returns: float
        """
        v = random.randint(1, 100000000000) / 1000
        return v

    def _get_rate_value(self) -> float:
        """Return test data value for a rate
        :returns: float
        """
        v = random.randint(1, 10000) / 10
        return v

    def _get_degree_value(self) -> float:
        """Return test data value for a degree
        :returns: float
        """
        v = random.randint(1, 1801) / 10
        if (random.randint(0, 1) == 0):
            v = -v
        return v

    def _get_xyz_value(self) -> float:
        """Return test data value for meters or x, y, z dimensions
        :returns: float
        """
        v = random.randint(1, 300) / 10
        return v

    def _get_fk_value(self,
                      p_col_nm: str) -> list:
        """Return test data value for a foreign key field
        :args:
        - p_col_nm: str. Column name.
        - p_row_num: int. Row number.
        :returns:
        - value from another table
        """
        v = None
        for fk_col, (rel_table, pk_col) in self.fk_constraints.items():
            if fk_col == p_col_nm:
                rel_data = DB.execute_select_all(rel_table)
                v = rel_data[pk_col]
                break
        return v

    def _get_uri_value(self) -> str:
        """Return test data value for a uri field
        :returns: str
        """
        v = 'https://' + SI.get_host() + '/' + SI.get_uid()[10:17] + '/' +\
            random.choice(['map', 'ideogram', 'sound', 'webby', 'picture']) +\
            random.choice(['.html', '.jpg', '.wav', '.pdf', '.dat', '.csv'])
        return v

    def _get_points_value(self) -> str:
        """Return test data value for a points field
        :returns: json-formatted str
        """
        points = []
        num_points = random.randint(3, 20)
        for _ in range(num_points):
            latitude = random.uniform(-90, 90)
            longitude = random.uniform(-180, 180)
            points.append((latitude, longitude))
        return json.dumps(points)

    def _get_text_value(self) -> str:
        """Return generic text value
        :returns: str
        """
        v = ''.join(random.choices(string.ascii_letters +
                                   string.digits,
                                   k=random.randint(10, 30)))
        return v

    def _get_hazards_or_features(self,
                                 p_entity: EntityType) -> str:
        """Return made-up data using a *_hazards or
            *_features EntityType and the following
        JSON format:
        [{"uid": int,
          "type": EntityType.RIVER_HAZARD,
          "loc": lat-long},
          ...]
        """
        hazfeats = []
        num_hazfeats = random.randint(1, 10)
        for _ in range(num_hazfeats):
            hazfeat = {}
            hazfeat["uid"] = random.randint(1000, 9999)
            hazfeat["type"] = random.choice(p_entity)
            hazfeat["loc"] = (random.uniform(-90, 90),
                              random.uniform(-180, 180))
            hazfeats.append(hazfeat)
        return json.dumps(hazfeats)

# =============================================================
# 'Public' methods
# =============================================================
    def make_algo_test_data(self,
                            p_data_model: object) -> tuple:
        """
        Create test data row(s) for specified table.
        :args:
        - p_data_model: object. Data model object
        :returns: tuple
        - Name of SQL script to insert test data.
        - List of tuple of values to be inserted.
        """
        full_list: list = []
        self._get_data_model(p_data_model)

        print(f"\nGenerating test data for:  {self.table_name}...")

        for rx in range(self.test_data_rows):
            row_list: list = []
            for cx, col in enumerate(self.sql_cols):

                col_nm, col_type, _, col_default = col.split()
                row_list.append(col_default.replace("'", ""))

                if col_nm.endswith('_pk'):
                    row_list[cx] = SI.get_key()
                elif col_nm.endswith('_dttm'):
                    row_list[cx] = SI.get_iso_time_stamp()

                elif col_nm in self.ck_constraints.keys():
                    row_list[cx] = random.choice(self.ck_constraints[col_nm])
                elif col_nm in self.fk_constraints.keys():
                    row_list[cx] = random.choice(self._get_fk_value(col_nm))

                elif col_nm.startswith('file_'):
                    row_list[cx] = self._get_file_value()
                elif col_nm.startswith('is_'):
                    row_list[cx] = random.choice([0, 1])
                elif col_nm.startswith('river_features_'):
                    row_list[cx] =\
                        self._get_hazards_or_features(
                            EntityType.RIVER_FEATURE)
                elif col_nm.startswith('river_hazards_'):
                    row_list[cx] =\
                        self._get_hazards_or_features(
                            EntityType.RIVER_HAZARD)
                elif col_nm.startswith('ocean_features_'):
                    row_list[cx] =\
                        self._get_hazards_or_features(
                            EntityType.OCEAN_FEATURE)
                elif col_nm.startswith('ocean_hazards_'):
                    row_list[cx] =\
                        self._get_hazards_or_features(
                            EntityType.OCEAN_HAZARD)

                elif col_nm.endswith('_name'):
                    row_list[cx] = self._get_name_value(rx)
                elif col_nm.endswith('_uri'):
                    row_list[cx] = self._get_uri_value()
                elif col_nm.endswith('_dg'):
                    row_list[cx] = self._get_degree_value()
                elif col_nm.endswith('_cnt'):
                    row_list[cx] = random.randint(10, 100)
                elif col_nm.endswith('_au'):
                    row_list[cx] = random.randint(9, 50) / 10

                elif '_points_' in col_nm:
                    row_list[cx] = self._get_points_value()

                elif any(col_nm.endswith(suffix)
                         for suffix in ('_px', '_pulse_per_ms',
                                        '_days')):
                    row_list[cx] = random.randint(30, 10000)
                elif any(col_nm.endswith(suffix)
                         for suffix in ('_rate', '_per_mpc',
                                        '_per_s', '_velocity')):
                    row_list[cx] = self._get_rate_value()
                elif any(col_nm.endswith(suffix)
                         for suffix in ('_kg', '_gly', '_gpc', '_pc',
                                        '_ly3', '_gyr', '_pc3', '_gpc3',
                                        '_gly3')):
                    row_list[cx] = self._get_astro_value()
                elif any(col_nm.endswith(suffix)
                         for suffix in ('_km', '_m', '_x', '_cnt', '_y',
                                        '_z', '_a', '_b', '_c', '_pitch',
                                        '_yaw', '_roll', '_gdy')):
                    row_list[cx] = self._get_xyz_value()

                elif col_type == 'BOOLEAN':
                    row_list[cx] = random.choice([0, 1])
                elif col_type == 'TEXT':
                    row_list[cx] = self._get_text_value()
                elif col_type == 'NUMERIC':
                    row_list[cx] = random.randint(20, 1000) / 10

            full_list.append(tuple(row_list))
        return (f'INSERT_{self.table_name}', full_list)
