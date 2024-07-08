"""

:module:    data_structs.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
Define static constants and non-DB data structures.
"""

from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401

import pygame as pg
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
    DGLAT_TO_KM = 80.0            # degree of latitutde -> kilometers
    DGLONG_TO_KM = 112.0          # degree of longitude -> kilometers


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
    LANG_CODE = ['en']
    LEAP_RULE = ['add_to_start_of_nth_month',
                 'add_to_end_of_nth_month', 'add_special_month']
    LINK_PROTOCOL = ['https', 'http', 'ftp', 'sftp', 'ssh', 'wc']
    LUMINOSITY_CLASS = ['I', 'II', 'III', 'IV', 'V']
    MAP_TOUCH_TYPE = ['contains', 'is_contained_by', 'borders',
                      'overlaps', 'informs', 'layers_above',
                      'layers_below']
    MAP_TYPE = ['geo', 'astro', 'underwater',
                'underground', 'informational', 'political']
    MEASURE_TYPE = ['AU', 'GLY', 'GPC', 'KPC', 'LM', 'LS', 'LY',
                    'MPC', 'CM', 'FT', 'GA', 'IN', 'KA', 'KM', 'M',
                    'MI', 'MM', 'NM', 'NOB', 'THWAB', 'TWA',
                    'YUZA', 'DGLAT', 'DGLONG']
    MIME_TYPE = ['image/png', 'image/jpeg', 'image/gif',
                 'image/svg+xml', 'image/tiff', 'image/bmp',
                 'image/webp', 'text/plain', 'text/html',
                 'text/css', 'text/csv', 'text/xml',
                 'text/javascript', 'application/pdf',
                 'application/json', 'application/xml',
                 'audio/mpeg', 'audio/wav', 'audio/ogg',
                 'video/mp4', 'video/ogg', 'video/webm']
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
    WORLD_TYPE = ['habitable', 'gas giant', 'rocky',
                  'desert', 'oceanic', 'ice planet',
                  'molten', 'other']
