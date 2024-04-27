"""

:module:    io_data.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

import ast          # abstract syntax trees
import pendulum     # date and time
import platform
import pygame as pg

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
    PLATFORM = (
        FI.F[FRAME]["dsc"] +
        #  " | " + platform.platform() +
        #  " | " + platform.architecture()[0] +
        f" | monitor (w, h): {INFO.current_w}, {INFO.current_h}" +
        " | Python " + platform.python_version() +
        " | Pygame " + pg.version.ver)
    # Window/overall frame for Game
    # -----------------------------
    WIN_W = round(INFO.current_w * 0.9)
    WIN_H = round(INFO.current_h * 0.9)
    WIN_MID = (WIN_W / 2, WIN_H / 2)
    pg.display.set_caption(FI.F[FRAME]["ttl"])
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
    MBAR_W = 240 if (WIN_W - (MBAR_X * 2)) / len(FI.M[MENUS]["menu"]) > 240\
        else (WIN_W - (MBAR_X * 2)) / len(FI.M[MENUS]["menu"])
    MBAR_MARGIN = 6
    # Game Map (grid) window size for Saskan game
    # -------------------------------------------
    GAMEMAP_TTL = FI.W["game_windows"]["gamemap"]["ttl"]
    GAMEMAP_X = int(round(WIN_W * 0.01))
    GAMEMAP_Y = int(round(WIN_H * 0.06))
    GAMEMAP_W = int(round(WIN_W * 0.8))
    GAMEMAP_H = int(round(WIN_H * 0.9))
    # Console window for Saskan app
    # -------------------------------
    CONSOLE = FI.W["game_windows"]["console"]
    CONSOLE_X = int(round(GAMEMAP_X + GAMEMAP_W + 20))
    CONSOLE_Y = GAMEMAP_Y
    CONSOLE_W = int(round(WIN_W * 0.15))
    CONSOLE_H = GAMEMAP_H
    CONSOLE_BOX = pg.Rect(CONSOLE_X, CONSOLE_Y,
                          CONSOLE_W, CONSOLE_H)
    # For now, the header/title on CONSOLE is static
    CONSOLE_TTL_TXT = FI.W["game_windows"]["console"]["ttl"]
    CONSOLE_TTL_IMG =\
        F_SANS_MED.render(CONSOLE_TTL_TXT, True,
                          Colors.CP_BLUEPOWDER,
                          Colors.CP_BLACK)
    CONSOLE_TTL_BOX = CONSOLE_TTL_IMG.get_rect()
    CONSOLE_TTL_BOX.topleft = (CONSOLE_X + 5, CONSOLE_Y + 5)
    # Info Bar for Saskan app
    IBAR_LOC = (GAMEMAP_X, int(round(WIN_H * 0.97)))
    # Help Pages -- external web pages, displayed in a browser
    WHTM = FI.U["uri"]["help"]


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
    - Generally, can just refer directly to the lists.
    """
    DATA_FORMATS = ["csv", "json", "xml", "xls", "xlsx",
                    "txt", "html", "pdf", "doc", "docx",
                    "txt", "ods", "sql", "dbf", "db",
                    "sqlite", "mdb", "accdb", "zip",
                    "tar", "gz"]
    BACKUP_TYPE = ["archive", "backup", "compressed", "export",
                   "encrypted"]
    CLUSTER_SHAPE = ['ellipsoid', 'spherical']
    RELATIVE_SIZE = ['small', 'medium', 'large']
    ASTRO_SHAPE = ['ellipsoid', 'spherical']
    ORBITAL_SHAPE = ['circular', 'elliptical']
    SPECTRAL_CLASS = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    LUMINOSITY_CLASS = ['I', 'II', 'III', 'IV', 'V']
    STABILITY = ['stable', 'unstable']
    DENSITY = ['sparse', 'dense']
    ASTRO_LOCATION = ['inner', 'outer', 'multiple']
    FREQUENCY = ['rare', 'occasional', 'frequent']
    INTENSITY = ['low', 'medium', 'high']
    WORLD_TYPE = ['habitable', 'gas giant', 'rocky',
                  'desert', 'oceanic', 'ice planet',
                  'molten', 'other']
    ASTRO_DIRECTION = ['prograde', 'retrograde']
    MAP_TYPE = ['geo', 'astro', 'underwater', 'underground',
                'informational', 'political']
    MAP_TOUCH_TYPE = ['contains', 'is_contained_by', 'borders',
                      'overlaps', 'informs', 'layers_above',
                      'layers_below']


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
#  - Modify models to use UID PKs and FKs on all table models.
#  - Consider adding a version ID to support programmatic
#    prototyping, undo's and so on.
#  - For test data generation, try using ChatGPT prompts?
#  - Implement all of the CHECK enums as EntityType data structures.
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
    """
    _tablename: str = "GALAXY"
    galaxy_uid_pk: str = ''
    galactic_cluster_uid_fk: str = ''
    galaxy_namek: str = ''
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
    tidally_locked: bool = False
    rotation_gdy: float = 0.0
    rotation_direction: str = 'prograde'
    orbit_direction: str = 'prograde'
    moons_cnt: int = 0
    world_desc: str = ''
    atmosphere: str = ''
    sky_color: pg.Color = Colors.CP_BLUE
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
    tidally_locked: bool = True
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
        FK: dict = {"grid_uid_fk": ("GRID", "grid_uid_pk"),
                    "map_uid_fk": ("MAP", "map_uid_pk")}

# Once the above have been tested, refactored, then add
# more structures from io_data_old.py. The additional
# structures are designed to add specific types of informational
# overlays onto maps or worlds. For example, Rivers, Cities,
# Roads; or charts of celestial events like lunar cycles.


# =======================================================
# DB/ORM Calls
# - Create SQL files
# - Create SQLITE tables
# - @DEV - possibly move these to io_db?
# =======================================================
class InitGameDB(object):
    """Methods to:
    - Create set of SQL files to manage the game database.
    - Boot the database by running the SQL files.
    """

    def __init__(self):
        """Initialize the InitGameDatabase object.
        """
        pass

    def create_sql(self):
        """Pass data object to create SQL files."""
        for model in [Backup,
                      Universe, ExternalUniv,
                      GalacticCluster, Galaxy,
                      StarSystem, World, Moon,
                      Map, MapXMap, Grid, GridXMap]:
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
            for (sql, values) in [
                TD.test_backup_data(),
            ]:
                for v in values:
                    DB.execute_insert(sql, v)


class TestData(object):
    """
    Class for management of test data rows on database, elsewhere
    @DEV:
    - Let's see if we can get ChatGPT API to generate test data for us...

    """

    def __init__(self):
        """Initialize TestData object."""
        # self.batch_1_uid_pk = SI.get_key()
        pass

    def test_backup_data(self):
        """
        Create test data row(s) for the BACKUP table.
        :returns: tuple
        - SQL script to insert test data.
        - List of values to be inserted.
        @DEV:
        - Abstract the prompt creation and scrubbing of the
          returned text from the API so that we can use much
          the same logic for every table.
        - See if the CHECK rule can be extracted from the
          database metadata instead of hard-coding it in the
          prompt. If can't get it from DB metadata, then
          extract enums from either the SQL DDL (CREATE) code or
          (better probably) from the data object model.
        - When dealing with Foreign Keys, will need to
          provide the prompt with a list of valid PK values on
          the related table(s).
        """
        values: list = []
        # Hard-coded...
        values.append((SI.get_key(),
                       'Test Backup',
                       pendulum.now().to_iso8601_string(),
                       'backup',
                       'SASKAN.db', 'SASKAN.bak'))
        values.append((SI.get_key(),
                       'Test Archive',
                       pendulum.now().to_iso8601_string(),
                       'archive',
                       'SASKAN.bak', '...arcv'))
        # AI-generated...
        sql_file = DB.get_sql_file('INSERT_BACKUP')
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system",
                 "content": "You are a code developer, skilled in " +
                            "crafting test data for a relational database."},
                {"role": "user",
                 "content": "The BACKUP table on a sqlite database " +
                            f"is defined as follows: {sql_file} " +
                            "Using python syntax, make a list of values " +
                            "to insert into the BACKUP table. " +
                            "Omit response text other than python code. " +
                            "For bkup_type column, use only the following " +
                            "values: 'archive', 'backup', 'compressed', " +
                            "'export', 'encrypted'"}
            ]
        )
        text = completion.choices[0].message.content
        text = text.replace("```python\n", '')
        text = text.replace("```", '').replace("```\n", '')
        text = text.replace("backup_values = [\n", '')
        text = text.replace("backup_data = [\n", '')
        text = text.replace("data_to_insert = [\n", '')
        text = text.replace("]\n", '')
        lists = text.split(',\n')
        for k, itm in enumerate(lists):
            print(f"d_{k}-, {itm}")
            itm = itm.replace("\n", '').replace("\t", '').strip()
            print(f"d_{k}+, {itm}")
            data_set = ast.literal_eval(itm)
            pp(("e", data_set))
            values.append(data_set)
        pp(("values = ", values))
        return ('INSERT_BACKUP', values)
