"""

:module:    data_structs.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
Define static constants and non-DB data structures
  which do not rely on PyGame for rendering.
"""

from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

# from collections import OrderedDict
from enum import Enum


#  UNIQUE CONSTANTS / "TRUE" ENUMS
# ================================
class Colors(object):
    """Constants for CLI and PyGame colors.
    Reference class attributes directly.
    No need to instantiate this class.
    Remember to add the CL_END color at the end.
    """

    # CLI Colors and accents
    CL_BLUE = "\033[94m"
    CL_BOLD = "\033[1m"
    CL_CYAN = "\033[96m"
    CL_DARKCYAN = "\033[36m"
    CL_GREEN = "\033[92m"
    CL_PURPLE = "\033[95m"
    CL_RED = "\033[91m"
    CL_YELLOW = "\033[93m"

    CL_BOLD = "\033[1m"
    CL_UNDERLINE = "\033[4m"
    CL_PLAIN = "\033[22;24m"

    CL_END = "\033[0m"


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


class LogLevel:
    """Define valid logging levels."""

    CRITICAL: int = 50
    FATAL: int = 50
    ERROR: int = 40
    WARNING: int = 30
    NOTICE: int = 20
    INFO: int = 20
    DEBUG: int = 10
    NOTSET: int = 0


#  COMPLEX CONSTANTS
# ================================
class Astro:
    """
    Constants for astronomical and physics units and conversions.
    """

    class UniverseNames(Enum):
        COSMIC = "Cosmic"
        MYSTERIOUS = "Mysterious"
        ETERNAL = "Eternal"
        RADIANT = "Radiant"
        INFINITE = "Infinite"
        CELESTIAL = "Celestial"

    class GalacticClusterNames(Enum):
        RUNIC = "Runic"
        STARRY = "Starry"
        BRILLIANT = "Brilliant"
        BLESSED = "Blessed"
        OCEANIC = "Oceanic"

    class GalaxyNames(Enum):
        BRILLIANT = "Brilliant"
        LUSTROUS = "Lustrous"
        TWINKLING = "Twinkling"
        SILVERY = "Silvery"
        GALAXY = "Galaxy"

    class TimingPulsarNames(Enum):
        TIMER = "Timer"
        CHRONO = "Chrono"
        CLOCKWORK = "Clockwork"
        LIGHTHOUSE = "Lighthouse"
        BEACON = "Beacon"

    # Mass, matter, energy
    MASS_MATTER_ENERGY = {
        "DE": "dark energy",
        "DM": "dark matter",
        "BM": "baryonic matter",
        "LCLS": "luminosity class",
        "SMS": "solar mass",
        "SL": "solar luminosity",
    }

    # Objects, astronomical
    ASTRONOMICAL_OBJECTS = {
        "BH": "black hole",
        "GB": "galactic bulge",
        "GC": "galactic cluster",
        "GH": "galactic halo",
        "GX": "galaxy",
        "IG": "interstellar matter",
        "SC": "star cluster",
        "SCLS": "star class",
        "TP": "timing pulsar",
        "TU": "total universe",
        "XU": "external universe",
    }

    # Time-related, real world and saskan
    TIME_RELATED = {
        "GS": "galactic second",
        "GMS": "galactic millisecond",
        "PMS": "pulses per millisecond",
        "ET": "elapsed time",
        "GYR": "gavoran year",
        "GDY": "gavoran day",
    }

    # Rates, speeds, velocities
    RATES_SPEEDS = {
        "ER": "expansion rate",
        "UER": "universal expansion rate",
        "KSM": "km/s per Mpc",
        "PRO": "period of rotation",
        "PRV": "period of revolution",
        "PR": "pulse rate",
    }

    # Distance
    DISTANCE = {
        "AU": "astronomical unit",
        "GLY": "gigalight year",
        "GPC": "gigaparsec",
        "KPC": "kiloparsec",
        "LM": "light minute",
        "LS": "light second",
        "LY": "light year",
        "MPC": "megaparsec",
        "PC": "parsec",
    }

    # Area, volume
    AREA_VOLUME = {
        "GLY2": "square gigalight year",
        "GLY3": "cubic gigalight year",
        "GPC2": "square gigaparsec",
        "GPC3": "cubic gigaparsec",
        "PC2": "square parsec",
        "PC3": "cubic parsec",
        "LY2": "square light year",
        "LY3": "cubic light year",
    }

    # Constants
    CONSTANTS = {
        "U_MIN_RAD_GLY": 45.824,
        "U_MAX_RAD_GLY": 47.557,
        "U_MIN_AGE_GYR": 2.67e10,
        "U_MAX_AGE_GYR": 3.12e10,
        "U_AVG_MASS_KG": 1.5e53,
        "U_EXP_RATE": 73.3,
        "U_VOL_TO_MASS": 3.61441428e48,
        "U_DARK_ENERGY_PCT": 0.683,
        "U_DARK_MATTER_PCT": 0.274,
        "U_BARYONIC_PCT": 0.043,
    }

    # Conversions
    CONVERSIONS = {
        "AU_TO_KM": 1.495979e8,
        "AU_TO_LM": 5.2596e16,
        "AU_TO_LS": 0.002004004004,
        "AU_TO_LY": 0.00001581250799,
        "GLY_TO_LY": 1e9,
        "GPC_TO_GLY": 3.09,
        "GPC_TO_MPC": 1000.0,
        "KM_TO_AU": 0.000006684587122,
        "KPC_TO_MPC": 1000.0,
        "KPC_TO_PC": 1000.0,
        "LM_TO_AU": 0.00000000000002,
        "LM_TO_LS": 9460730472580800,
        "LM_TO_LY": 0.000000000000019,
        "LS_TO_AU": 499.004783676,
        "LS_TO_LM": 0.000000000000105,
        "LY_TO_AU": 63240.87,
        "LY_TO_GLY": 1e-9,
        "LY_TO_LM": 52596000000000000,
        "LY_TO_PC": 0.30659817672196,
        "MPC_TO_GPC": 0.001,
        "MPC_TO_KPC": 1000.0,
        "GLY_TO_PC": 3.262e6,
        "PC_TO_GLY": 3.065603923973023e-07,
        "PC_TO_KPC": 0.001,
        "PC_TO_LY": 3.261598,
    }


class Geog:
    """
    Constants for computations using various units and
    formulae for measures of distance at a human or fantasy
    planetary geographical scale.
    """

    # Distance Units
    DISTANCE_UNITS = {
        "CM": "centimeters",
        "FT": "feet",
        "GA": "gawos",  # saskan
        "IN": "inches",
        "KA": "katas",  # saskan
        "KM": "kilometers",
        "M": "meters",
        "MI": "miles",
        "MM": "millimeters",
        "NM": "nautical miles",
        "NOB": "nobs",  # saskan
        "THWAB": "thwabs",  # saskan
        "TWA": "twas",  # saskan
        "YUZA": "yuzas",  # saskan
    }

    # Area and Volume Units
    AREA_VOLUME_UNITS = {"M2": "square meters", "M3": "cubic meters"}

    # Geographical Distance
    GEOGRAPHICAL_DISTANCE = {"DGLAT": "degrees latitude", "DGLONG": "degrees longitude"}

    # Geographical Directions
    DIRECTIONS = {
        "LOC": "location",
        "N": "north",
        "E": "east",
        "S": "south",
        "W": "west",
        "NE": "northeast",
        "SE": "southeast",
        "SW": "southwest",
        "NW": "northwest",
        "NS": "north-south",
        "EW": "east-west",
    }

    # Metric/Imperial Conversions
    METRIC_IMPERIAL_CONVERSIONS = {
        "CM_TO_IN": 0.3937007874,
        "CM_TO_M": 0.01,
        "CM_TO_MM": 10.0,
        "FT_TO_IN": 12.0,
        "FT_TO_M": 0.3048,
        "IN_TO_CM": 2.54,
        "IN_TO_FT": 0.08333333333,
        "IN_TO_MM": 25.4,
        "KM_TO_M": 1000.0,
        "KM_TO_MI": 0.62137119223733,
        "KM_TO_NM": 0.539956803,
        "M_TO_CM": 100.0,
        "M_TO_FT": 3.280839895,
        "M_TO_KM": 0.001,
        "MI_TO_KM": 1.609344,
        "MI_TO_NM": 0.868976242,
        "MM_TO_CM": 0.1,
        "MM_TO_IN": 0.03937007874,
        "NM_TO_KM": 1.852,
        "NM_TO_MI": 1.150779448,
    }

    # Saskan/Metric Conversions
    SASKAN_METRIC_CONVERSIONS = {
        "CM_TO_NOB": 0.64,
        "GABO_TO_MI": 0.636,
        "GAWO_TO_KATA": 4.0,
        "GAWO_TO_KM": 1.024,
        "GAWO_TO_M": 1024.0,
        "IN_TO_NOB": 2.56,
        "KATA_TO_KM": 0.256,
        "KATA_TO_M": 256.0,
        "KATA_TO_MI": 0.159,
        "KATA_TO_THWAB": 4.0,
        "M_TO_NOB": 64.0,
        "M_TO_THWAB": 0.015625,
        "MM_TO_NOB": 0.0064,
        "NOB_TO_CM": 1.5625,
        "NOB_TO_IN": 0.390625,
        "NOB_TO_MM": 156.25,
        "THWAB_TO_KATA": 0.25,
        "THWAB_TO_M": 64.0,
        "THWAB_TO_TWA": 64.0,
        "TWA_TO_M": 1.00,
        "TWA_TO_NOB": 64.0,
        "TWA_TO_THWAB": 0.015625,
        "YUZA_TO_GABO": 4.0,
        "YUZA_TO_KM": 4.096,
        "YUZA_TO_M": 4096.0,
        "YUZA_TO_MI": 2.545,
    }

    # Geographical to Metric Conversions
    GEOGRAPHICAL_METRIC_CONVERSIONS = {"DGLAT_TO_KM": 80.0, "DGLONG_TO_KM": 112.0}


class Geom:
    """
    Constants assigned to meaningful abbreviations and names relating
    generically to geometry and physics.
    """

    # Math and General Geometry
    MATH_GEOMETRY = {
        "ABC": "(a, b, c)",
        "ANG": "angle",
        "AR": "area",
        "BND": "bounding rectangle",
        "CNT": "count",
        "CON": "container",
        "DC": "decimal",
        "DI": "diameter",
        "DIM": "dimensions",
        "DIR": "direction",
        "HT": "height",
        "INT": "integer",
        "LG": "length",
        "PCT": "percent",
        "PYR": "pitch, yaw, roll",
        "RD": "radius",
        "ROT": "rotation",
        "SAX": "semi-axes",
        "SZ": "size",
        "VE": "vector",
        "VL": "volume",
        "WD": "width",
        "XY": "(x, y)",
        "XYZD": "((x,x), (y,y), (z,z))",
        "XYZ": "(x, y, z)",
    }

    # Geometry Shapes
    GEOMETRY_SHAPES = {
        "BX": "pg_rect",
        "CI": "circle",
        "EL": "ellipsoid",
        "RC": "rectangle",
        "SH": "sphere",
        "SHA": "shape",
        "SP": "spiral",
    }

    # Weight and Mass
    WEIGHT_MASS = {
        "GM": "grams",
        "KG": "kilograms",
        "LB": "pounds",
        "MS": "mass",
        "OZ": "ounces",
    }

    # Energy
    ENERGY = {
        "AMP": "amperes (A)",
        "OH": "ohms (Ω)",
        "V": "volts (V)",
        "WA": "watts (W)",
    }

    # Names, Labels, Qualities
    NAMES_LABELS_QUALITIES = {"NM": "name", "REL": "relative", "SHP": "shape"}


#  SIMPLE DATA STRUCTURES
# ============================
class GroupStruct(object):
    """Base class for data structures made of a
    simple group of attritubes. Structures
    have default values, but are mutable.
    Instantiate as sub-class object with no parameters.
    User assigns values directly.
    For example:
        CRI = GroupStruct.ColumnRowIndex()
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

    class GameGeo(object):
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
        see Game3DLoc class (below), keeping in mind that
        3D rendering is beyond the capabilities of a Python-
        driven game.
        North +, South -, East +, West -
        """

        lat_dg: float = 0.0
        long_dg: float = 0.0
        avg_alt_m: float = 0.0
        max_alt_m: float = 0.0
        min_alt_m: float = 0.0

    class Game3DLoc(object):
        """
        This is a general-purpose, high level 3D location/shape
        container structure, box-shaped, that is, six adjoining
        rectangles with parallel sides.  Use x, y, z coordinates
        which can be mapped to whatever units are needed. For
        example, in a Universe, the x,y,z coordinates might refer
        to mega-parsecs, whereas in an Undersea world they might
        refer to kilometers.
        The box is defined as an x,y,z origin point, which is the
        upper-left, foremost corner of the box in the default
        perspctive. The box is sized by w, h and d =
        lateral dimensions in the x (horiz), y (vert) and
        z (depth of field) directions.
        """

        origin_x: float = 0.0
        origin_y: float = 0.0
        origin_z: float = 0.0
        width_x: float = 0.0
        height_y: float = 0.0
        depth_z: float = 0.0


#  COMPLEX DATA STRUCTURES
#  =============================
class EntityType(object):
    """Constants:
    - This entire class can be made into a dict:
      `entity_dict = {k:v for k,v in EntityType.__dict__.items()
                      if not k.startswith('__')}`
    """

    ASTRO_DIRECTION = ["prograde", "retrograde"]
    ASTRO_LOCATION = ["inner", "outer", "multiple"]
    ASTRO_SHAPE = ["ellipsoid", "spherical"]
    BACKUP_TYPE = ["archive", "backup", "compressed", "export", "encrypted"]
    BUTTON_TYPE = ["toggle", "check", "radio", "event"]
    CHAR_SET_TYPE = ["alphabet", "abjad", "abugida", "syllabary", "ideogram"]
    CLUSTER_SHAPE = ["ellipsoid", "spherical"]
    DENSITY = ["sparse", "dense"]
    DATA_FORMATS = [
        "csv",
        "json",
        "xml",
        "xls",
        "xlsx",
        "txt",
        "html",
        "pdf",
        "doc",
        "docx",
        "txt",
        "ods",
        "sql",
        "dbf",
        "db",
        "sqlite",
        "mdb",
        "accdb",
        "zip",
        "tar",
        "gz",
    ]
    DATA_TYPE = ["TEXT", "INT", "FLOAT", "JSON", "BLOB"]
    FREQUENCY = ["rare", "occasional", "frequent"]
    GLOSS_TYPE = [
        "word",
        "phrase",
        "map",
        "picture",
        "diagram",
        "data",
        "software",
        "sound",
        "video",
    ]
    HEMISPHERE_TYPE = ["north", "south"]
    INTENSITY = ["low", "medium", "high"]
    LAKE_SIZE = ["small", "medium", "large"]
    LAKE_TYPE = [
        "lake",
        "reservoir",
        "pond",
        "pool",
        "loch",
        "hot spring",
        "swamp",
        "marsh",
        "mill pond",
        "oxbow lake",
        "spring",
        "sinkhole",
        "acquifer",
        "vernal pool",
        "wadi",
    ]
    LAND_BODY_TYPE = ["island", "continent", "sub-continent", "region"]
    LAND_LAND_RELATION_TYPE = ["borders", "overlaps", "contains", "contained by"]
    LAND_OCEAN_RELATION_TYPE = ["borders", "overlaps", "contains", "contained by"]
    LANG_CODE = ["en"]
    LEAP_RULE = [
        "add_to_start_of_nth_month",
        "add_to_end_of_nth_month",
        "add_special_month",
    ]
    LINK_PROTOCOL = ["https", "http", "ftp", "sftp", "ssh", "wc"]
    LUMINOSITY_CLASS = ["I", "II", "III", "IV", "V"]
    MAP_SHAPE = ["rectangle", "box", "sphere"]
    MAP_TYPE = [
        "geo",
        "astro",
        "underwater",
        "underground",
        "info",
        "political",
    ]
    MEASURE_TYPE = [
        "AU",
        "GLY",
        "GPC",
        "KPC",
        "LM",
        "LS",
        "LY",
        "MPC",
        "CM",
        "FT",
        "GA",
        "IN",
        "KA",
        "KM",
        "M",
        "MI",
        "MM",
        "NM",
        "NOB",
        "THWAB",
        "TWA",
        "YUZA",
        "DGLAT",
        "DGLONG",
    ]
    MIME_TYPE = [
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/svg+xml",
        "image/tiff",
        "image/bmp",
        "image/webp",
        "text/plain",
        "text/html",
        "text/css",
        "text/csv",
        "text/xml",
        "text/javascript",
        "application/pdf",
        "application/json",
        "application/xml",
        "audio/mpeg",
        "audio/wav",
        "audio/ogg",
        "video/mp4",
        "video/ogg",
        "video/webm",
    ]
    NAME_SPACE = [
        "app",
        "story"
    ]
    OCEAN_BODY_TYPE = [
        "fjord",
        "sea",
        "ocean",
        "harbor",
        "lagoon",
        "bay",
        "gulf",
        "sound",
        "bight",
        "delta",
        "estuary",
        "strait",
        "ice field",
        "ice sheet",
        "ice shelf",
        "iceberg",
        "ice floe",
        "ice pack",
        "roadstead",
        "tidal pool",
        "salt marsh",
    ]
    OCEAN_HAZARD = [
        "tsunami",
        "typhoon",
        "volcano",
        "tide",
        "storm",
        "whirlpool",
        "current",
        "undertow",
        "rip tide",
        "reef",
    ]
    OCEAN_FEATURE = [
        "atoll",
        "coral reef",
        "seamount",
        "trench",
        "volcanic vent",
        "hydrothermal vent",
        "tide pool",
        "mangrove",
        "kelp forest",
        "coral bed",
        "sargasso",
        "gyre",
        "upwelling",
        "downwelling",
        "eddy",
        "thermocline",
        "halocline",
        "polar ice cap",
        "ice shelf",
    ]
    OCEAN_WAVE_TYPE = ["low", "medium", "high", "none"]
    ORBITAL_SHAPE = ["circular", "elliptical"]
    RELATIVE_SIZE = ["small", "medium", "large"]
    RIVER_FEATURE = [
        "delta",
        "bridge",
        "crossing",
        "footbridge",
        "pier",
        "marina",
        "boathouse",
        "habitat",
    ]
    RIVER_HAZARD = [
        "rapids",
        "wreckage",
        "sandbar",
        "waterfall",
        "shallow",
        "dam",
        "weir",
        "habitat",
    ]
    RIVER_TYPE = [
        "perrenial",
        "periodic",
        "episodic",
        "exotic",
        "tributary",
        "distributary",
        "underground",
        "aqueduct",
        "canal",
        "rapids",
        "winding",
        "stream",
        "glacier",
    ]
    RIVER_NAV_TYPE = ["small craft", "large craft", "none"]
    SEASON_TYPE = [
        "winter",
        "spring",
        "summer",
        "fall" "all",
        "winter-spring",
        "spring-summer",
        "summer-fall",
        "fall-winter",
    ]
    SPECTRAL_CLASS = ["O", "B", "A", "F", "G", "K", "M"]
    STABILITY = ["stable", "unstable"]
    TOUCH_TYPE = [
        "contains",
        "is_contained_by",
        "borders",
        "overlaps",
        "informs",
        "layers_above",
        "layers_below",
    ]
    WATER_TYPE = ["freshwater", "saline", "brackish"]
    WORLD_TYPE = [
        "habitable",
        "gas giant",
        "rocky",
        "desert",
        "oceanic",
        "ice planet",
        "molten",
        "other",
    ]


class AppDisplay:
    """Static values related to constructing GUI's in PyGame.
    Object place-holders used for rendering.
    """

    # Typesetting
    # -------------------
    DASH16: str = "-" * 16
    FONT_FXD = "Courier 10 Pitch"
    FONT_MED_SZ = 30
    FONT_SANS = "DejaVu Sans"
    FONT_SM_SZ = 24
    FONT_TINY_SZ = 12
    FONT_LARGE_SZ = 36
    # Window and Clock objects
    # ---------------------------
    WIN_W = 0.0
    WIN_H = 0.0
    WIN_MID = 0.0
    WIN = None
    TIMER = None
