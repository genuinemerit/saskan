"""

:module:    data_model_story.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.

Data models for story-related components of the app,
like maps, languages, settings, characters and so on.

- Use the `$$ .. $$` docstring formatting. It is specific to defining/extracting metadata.
  Metadata is defined in the comment blocks, separated by '$$'.
  Don't use quotes or apostrophes inside metadata definitions.
- Metadata is extracted from the data model classes by the DataBase() class to
  provide definitions stored in the METADATA table. It is defined in the
  doctrings of each model class, using the following syntax:
    $$
    - field_name: description of the field
    - field_name: description of the field
    $$

- Store files and images in the database as BLOBs, not as external files.
  Modify the data models to include BLOBs for images, sounds and included files where appropriate.

- Do NOT use an __init__ method in data model classes. We never instantiate them.
  The data types and default values are extracted directly by the DataBase() class
  reading the "magic" __dict__ attribute of the classes.

- UID - system-generated unique identifier, the only type of value used for a PK or FK.
        - When a record is marked deleted, its replacement gets a new UID.
        - A UID PK is unique across the entire database.
        - A UID FK always points to a UID PK and is never null.
- ID - a string that, in combo with a blank delete_dt, or with blank delete_dt and lang_code,
        uniquely identifies a record in a table. Note that ID is not necessarily unqiue
        within a table, but is unique within a table for a given lang_code + blank delete_dt.
- NAME - Similar to ID, but content is lang-specific and is for display purposes. The NAME
        is _not_ necessarily unique in a table across lang codes. For example, the word
        "closet" can be used for both English and Spanish. It is also possible that the
        NAME value can be volatile, whereas the ID value should never change. Note that the
        _name suffix may also be used in other situations where appropriate. It is not always
        a lang-specific display/label value.
"""

from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

import data_model as DM
from data_structs import EntityType
from method_files import FileMethods
from method_shell import ShellMethods

FM = FileMethods()
SM = ShellMethods()


# =============================================================
# Abstract Maps and Grids
# =============================================================
class MapRect():
    """
    Map is a rectangle (2d). Typically used for geographic maps.
    Rectangle units are in degrees latitude and degrees longitude.
    Can contain, overlap, border other Map_Rect structures.
    Can be associated with granular Grid data tables, such as:
    - geography (continents, regions, mountains, hills, rivers,
      lakes, seas, oceans, etc.)
    - political boundaries (countries, provinces, states, counties, etc.)
    - roads, paths, trails, waterways, bodies of water, etc.
    - cities, towns, villages, neighborhoods, etc.
    - other points of interest (ruins, temples, etc.)
    - natural resources (mines, quarries, etc.)
    - demographics (population density, etc.)
    3 shapes: rectangle, box, sphere.
    6 types (can be of any shape):
        "geo", "astro", "underwater", "underground", "info", "political"

    $$
    - map_rect_uid_pk: Primary key, unique identifier for each map rectangle
    - map_shape: Shape of the map area (e.g., rectangle, box, sphere)
    - map_type: Type of map area (e.g., geo, astro, underwater)
    - map_id: ID of the map rectangle
    - lang_code: Language code for the map rectangle
    - map_name: Displayable name of the map rectangle
    - map_desc: Description of the map rectangle
    - north_lat: Northern latitude boundary of the map rectangle
    - south_lat: Southern latitude boundary of the map rectangle
    - east_lon: Eastern longitude boundary of the map rectangle
    - west_lon: Western longitude boundary of the map rectangle
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """
    _tablename: str = "MAP_RECT"
    map_rect_uid_pk: str = ""
    map_shape: str = ""
    map_type: str = ""
    map_id: str = ""
    lang_code: str = ""
    map_name: str = ""
    map_desc: str = ""
    north_lat: float = 0.0
    south_lat: float = 0.0
    east_lon: float = 0.0
    west_lon: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(MapRect)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "map_rect_uid_pk"
        CK: dict = {"map_shape": EntityType.MAP_SHAPE, "map_type": EntityType.MAP_TYPE}
        ORDER: list = ["map_name ASC"]


class MapBox(MapRect):
    """
    Map is a box (3D). Typically used for geographic or city/building maps.
    x, y units are in degrees latitude and degrees longitude.
    z units are in meters and are provided in two directions: up and down.
    They should reflect the maximum meters in each direction.
    Can contain, overlap, border other Map_Rect structures.
    Can be associated with granular Grid data tables.

    $$
    - map_box_uid_pk: Primary key, unique identifier for each map box
    - map_shape: Shape of the map area (e.g., box)
    - map_type: Type of map area (e.g., geo, astro, underwater)
    - map_id: ID of the map box
    - lang_code: Language code for the map box
    - map_name: Name of the map box
    - map_desc: Description of the map box
    - north_lat: Northern latitude boundary of the map box
    - south_lat: Southern latitude boundary of the map box
    - east_lon: Eastern longitude boundary of the map box
    - west_lon: Western longitude boundary of the map box
    - up_m: Maximum meters upwards from the base level
    - down_m: Maximum meters downwards from the base level
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "MAP_BOX"
    map_box_uid_pk: str = ""
    map_shape: str = ""
    map_type: str = ""
    map_id: str = ""
    lang_code: str = ""
    map_name: str = ""
    map_desc: str = ""
    north_lat: float = 0.0
    south_lat: float = 0.0
    east_lon: float = 0.0
    west_lon: float = 0.0
    up_m: float = 0.0
    down_m: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(MapBox)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "map_box_uid_pk"
        CK: dict = {"map_shape": EntityType.MAP_SHAPE, "map_type": EntityType.MAP_TYPE}
        ORDER: list = ["map_name ASC"]


class MapSphere(MapRect):
    """
    Map is a sphere (3D). Typically used for astronomical maps.
    May also be useful for defining floating islands, undersea regions, etc.
    - Units may vary quite a lot, from meters to parsec.
    Can contain, overlap, border other Map_Sphere structures.
    The sphere is considered to reside within the constraints of a parent
    Map_Rect structure. The point of origin is the center of the sphere.
    For geo-maps, it is expressed at latitudinal and longitudinal coordinates,
    plus a positive or negative z value. For astro-maps, the origin is in
    whatever coordinate system is used for the map. Likely that is defined
    within the Grid data.

    @DEV:
    - See if we can tweak this class to support ellipsoids.
    - Should just be matter of providing a second set of axes.
    - Nah. Should make it a separate class, to be consistent.

    $$
    - map_sphere_uid_pk: Primary key, unique identifier for each map sphere
    - map_shape: Shape of the map area (e.g., sphere)
    - map_type: Type of map area (e.g., geo, astro, underwater)
    - map_id: ID of the map box
    - lang_code: Language code for the map box
    - map_name: Name of the map sphere
    - map_desc: Description of the map sphere
    - origin_lat: Latitudinal coordinate of the sphere's origin
    - origin_lon: Longitudinal coordinate of the sphere's origin
    - z_value: Z coordinate value, indicating height or depth from a reference point
    - unit_of_measure: Unit of measure used for dimensions (e.g., meters, parsecs)
    - sphere_radius: Radius of the sphere
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "MAP_SPHERE"
    map_sphere_uid_pk: str = ""
    map_shape: str = ""
    map_type: str = ""
    map_id: str = ""
    lang_code: str = ""
    map_name: str = ""
    map_desc: str = ""
    origin_lat: float = 0.0
    origin_lon: float = 0.0
    z_value: float = 0.0
    unit_of_measure: str = ""
    sphere_radius: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(MapSphere)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "map_sphere_uid_pk"
        CK: dict = {
            "map_shape": EntityType.MAP_SHAPE,
            "map_type": EntityType.MAP_TYPE,
            "unit_of_measure": EntityType.MEASURE_TYPE,
        }
        ORDER: list = ["map_name ASC"]


class Grid():
    """
    The Grid structure defines dimensions of a Map for story-telling
    rendering, drawing and referencing purposes. It defines a matrix,
    a kind of 3D spreadsheet laid over a Map structure. Rather than geo
    dimensions, a grid of data cells, rows, and columns.

    The Grid itself only defines the dimensions of the matrix; it does
    not store data in the cells. If a Grid or Grid cell needs to be mapped
    to Pygame pixel or some story-telling or mapping dimension like km,
    that is handled algorithmically.

    Dimensions are defined as x=col=east-west, y=row=north-south and
    zu=up-from-zeroth-row, zd=down-from-zeroth-row. The cnt is the number
    of rows, cols or z-layers. So if only layer, then zu and zd = 0.

    Grid Cells are identified in the GridCell table, which holds an FK to
    the Grid table.  Values for each cell are stored in the GridCellValue table.

    Grids are always associated with one or more MAP_* tables.

    There is nothing displayable about the grid that is language-specific,
    so it has an ID, but not a NAME or a LANG_CODE.

    $$
    - grid_uid_pk: Primary key, unique identifier for each grid
    - grid_id: ID of the grid
    - x_col_cnt: Number of columns (east-west direction)
    - y_row_cnt: Number of rows (north-south direction)
    - z_up_cnt: Number of layers above the zeroth row
    - z_down_cnt: Number of layers below the zeroth row
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "GRID"
    grid_uid_pk: str = ""
    grid_id: str = ""
    x_col_cnt: int = 0
    y_row_cnt: int = 0
    z_up_cnt: int = 0
    z_down_cnt: int = 0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Grid)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "grid_uid_pk"
        ORDER: list = ["grid_id ASC"]


class GridCell():
    """
    The GridCell structure defines a given data cell within a Grid.
    The grid_cell_name is an optional descriptive name for a cell.
    The grid_cell-id is its x/y/z location in the Grid matrix,
    where a positive z is up and negative z is down. x and y locations
    are zero-based and begin in the "lower-left" or "south-west" or
    "front-left" corner of the Grid. In the ID field, the values are
    stored in the form of a python tuple, e.g., (3, 4, -2).
    Each individual index is stored as an integer.

    There can be zero to many name:value type of data associated
    with a given grid. Fairly open-ended. Those values are defined
    in the GridCellValue table, which holds an FK to the GridCell.

    $$
    - grid_cell_uid_pk: Primary key, unique identifier for each grid cell
    - grid_uid_fk: Foreign key linking to the Grid table
    - grid_id: Name of the grid this cell belongs to
    - lang_code: Language code for the grid cell
    - grid_cell_name: Optional descriptive name for the grid cell
    - x_col_ix: Zero-based column index (east-west direction)
    - y_row_ix: Zero-based row index (north-south direction)
    - z_up_down_ix: Index indicating vertical position (positive for up, negative for down)
    - grid_cell_id: Tuple representing the x, y, z location in the Grid matrix
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "GRID_CELL"
    grid_cell_uid_pk: str = ""
    grid_uid_fk: str = ""
    grid_id: str = ""
    lang_code: str = ""
    grid_cell_name: str = ""
    x_col_ix: int = 0
    y_row_ix: int = 0
    z_up_down_ix: int = 0
    grid_cell_id: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(GridCell)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "grid_cell_uid_pk"
        FK: dict = {"grid_uid_fk": ("GRID", "grid_uid_pk")}
        ORDER: list = ["grid_cell_name ASC"]


class GridInfo():
    """
    The GridInfo structure holds information that belongs
    to a given cell within a grid.

        - info_data: list of dicts of grid info data:
                    {grid_info_id: str, grid_info_name: str,
                     grid_info_int: int, grid_info_float: float,
                     grid_info_str: str, grid_info_json: str,
                     grid_info_img_path: str, grid_info_img: bytes/blob})

    $$
    - grid_info_uid_pk: Primary key, unique ID for each grid info record
    - grid_uid_fk: Foreign key linking to the Grid table
    - grid_cell_uid_fk: Foreign key linking to the GridCell table
    - grid_id: Name of the grid this information belongs to
    - grid_cell_name: Name of grid cell this info is associated with
    - grid_info_id: Short universal descriptive tag for the cell value
    - lang_code: Language code for the grid info
    - grid_info_name: Label for value, providing context or description
    - grid_info_int: (optional) Integer value for the cell
    - grid_info_float: (optional) Float value for the cell
    - grid_info_str: (optional) String value for the cell
    - grid_info_json: (optional) JSON string value for the cell
    - grid_info_img_path: (optional) Path to image object for the cell
    - grid_info_img: (optional) Image object for the cell, stored as a BLOB
    - delete_dt: Deletion date, when the record was marked for deletion
    $$

    """

    _tablename: str = "GRID_INFO"
    grid_info_uid_pk: str = ""
    grid_uid_fk: str = ""
    grid_cell_uid_fk: str = ""
    grid_id: str = ""
    grid_cell_name: str = ""
    grid_info_id: str = ""
    lang_code: str = ""
    grid_info_name: str = ""
    grid_info_int: int = 0
    grid_info_float: float = 0.0
    grid_info_str: str = ""
    grid_info_json: str = ""
    grid_info_img_path: str = ""
    grid_info_img: bytes = b""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(GridInfo)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "grid_info_uid_pk"
        FK: dict = {
            "grid_cell_uid_fk": ("GRID_CELL", "grid_cell_uid_pk"),
            "grid_uid_fk": ("GRID", "grid_uid_pk"),
        }
        ORDER: list = ["grid_info_name ASC"]


class CrossAssociation():
    """
    Generic model for associative keys.
    - TBL_* (n) <--> TBL_* (n)
    The "touch type" reads in direction 1-->2.
        For example, 1-contains-2, 1-is_contained_by-2, etc.

    Tables are linked by UIDs, not by ID or NAME. However, it uses
      VFKs so we can use this structure for any two types of tables,
      mixing different types. The designation `_vfk` indicates a virtual FK.
    The links are verified in python code rather than by SQLite.
    The linked table names are provided as columns. The names of
    the linked UID columns are implied.

    $$
    - cross_x_uid_pk: Primary key, unique ID for each association
    - uid_1_table: Table name of the first table in the association
    - uid_1_vfk: VFK to first table UID in the association
    - uid_2_table: Table name of the second table in the association
    - uid_2_vfk: VFK to second table UID in the association
    - touch_type: Describes the relationship type between the two records,
        such as contains, is_contained_by
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    @DEV:
    - This is an unusual approach. Typically there would be a separate
      association table for every possible many-to-many relation between two specific
      tables. Having a single association table that is generic for all type of
      associations may provide better flexibility at the cost/risk of slightly more complexity.
      If this creates a shit-show, then go back to using table-specific association tables.
    """
    _tablename: str = "CROSS_X"
    cross_x_uid_pk: str = ""
    uid_1_table: str = ""
    uid_1_vfk: str = ""
    uid_2_table: str = ""
    uid_2_vfk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(CrossAssociation)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "cross_x_uid_pk"
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}


class MapXMap():
    """
    Associative keys --
    - MAP_* (n) <--> MAP_* (n)
    The "touch type" reads in direction 1-->2.
    For example, 1-contains-2, 1-is_contained_by-2, etc.

    Use VFKs so we can use this structure for any type of map, mixing
    different types. The designation `_vfk` indicates a virtual FK.
    The link is verified in python code rather than by SQLite.

    $$
    - map_x_map_uid_pk: Primary key, unique ID for each map-to-map association
    - map_uid_1_table: Table name of the first map in the association
    - map_uid_1_vfk: VFK to first map in the association
    - map_uid_2_table: Table name of the second map in the association
    - map_uid_2_vfk: VFK to second map in the association
    - touch_type: Describes the relationship type between the two maps, such as
        contains, is_contained_by
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """
    _tablename: str = "MAP_X_MAP"
    map_x_map_uid_pk: str = ""
    map_uid_1_table: str = ""
    map_uid_1_vfk: str = ""
    map_uid_2_table: str = ""
    map_uid_2_vfk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(MapXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "map_x_map_uid_pk"
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}


class GridXMap():
    """
    Associative keys --
    - GRIDs (n) <--> MAPs (n)
    FK field is indexed for the Grid association,
    but the Map FK is handled algorithmically so that this
    can be used on multiple types of MAP_* tables.

    $$
    - grid_x_map_uid_pk: Primary key, unique identifier for
      each grid-to-map association
    - grid_uid_fk: Foreign key representing the associated grid, indexed for performance
    - map_uid_vfk: Virtual foreign key representing the associated map,
      adaptable for various MAP_* tables
    - delete_dt: Deletion date, indicating when the record was
      marked for deletion
    $$
    """

    _tablename: str = "GRID_X_MAP"
    grid_x_map_uid_pk: str = ""
    grid_uid_fk: str = ""
    map_uid_vfk: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(GridXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "grid_x_map_uid_pk"
        FK: dict = {"grid_uid_fk": ("GRID", "grid_uid_pk")}


# =============================================================
# Semantics and Languages
# =============================================================
class CharSet():
    """
    Description of a set of characters used in a language.
    Provide the name of a font. We'll define where fonts
    get stored in the app tree elsewhere, like the boot
    configuration. The font name is generic. It may encompass
    multiple types of font files, e.g, tff, otf, dfont, etc.

    A character set is a set of characters, also called glyphs.
    In the game context, they are associated with game languages,
    which may be of the following types with respect to how they
    use glyphs:
    - alphabet
    - abjad
    - abugida
    - syllabary
    - ideogram

    An alphabet represents consonants and vowels each
    separately as individual letters.

    An abjad represents only consonants as distinct letters;
    vowels are represented as diacritics. In some cases, the
    vowels may be omitted entirely, and are implied from
    context.

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

    Since char sets are not displayed, per se, in the game, they
    don't have a lang_code or a name. THe font_name acts like an ID.
    For now, providing description of the font only in English.

    $$
    - char_set_uid_pk: Primary key, unique ID for each character set
    - font_name: Name of the font associated with the character set,
      supports multiple font file types
    - char_set_type: Type of the character set, default is 'alphabet',
      can be 'abjad', 'abugida', 'syllabary', or 'ideogram'
    - char_set_desc: Description of the character set, providing
      additional context or details
    - delete_dt: Deletion date, indicating when the record was
      marked for deletion
    $$

    """

    _tablename: str = "CHAR_SET"
    char_set_uid_pk: str = ""
    font_name: str = ""
    char_set_type: str = "alphabet"
    char_set_desc: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(CharSet)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "char_set_uid_pk"
        CK: dict = {"char_set_type": EntityType.CHAR_SET_TYPE}
        ORDER: list = ["font_name ASC"]


class CharMember():
    """
    Describe individual characters in a character set.
    Where the character is not represented in Unicode, a reference
    to a picture or a binary of the image of the character is stored,
    along with name and description. Member types are defined by
    the type of writing system (character set) they belong to. Further
    categorizations are possible for numerics, punctuation, and so on.

    $$
    - char_member_uid_pk: Primary key, unique identifier for each character member
    - char_set_uid_fk: Foreign key referencing the character set this member belongs to
    - char_member_name: Name of the character member
    - char_member_image: Binary data representing the image of
      the character if not available in Unicode
    - char_member_path: File path to the image or representation of the character
    - char_member_desc: Description providing additional details about the character member
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "CHAR_MEMBER"
    char_member_uid_pk: str = ""
    char_set_uid_fk: str = ""
    char_member_name: str = ""
    char_member_image: bytes = b""
    char_member_path: str = ""
    char_member_desc: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(CharMember)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "char_member_uid_pk"
        FK: dict = {"char_set_uid_fk": ("CHAR_SET", "char_set_uid_pk")}
        ORDER: list = ["char_member_name ASC"]


# Pick up here. Note that no SET methods have been defined yet
# for the following classes, except for association tables, which
# are biw handled generically. However, all X classes need to be
# modified to include a touch_type column.


class LangFamily():
    """
    Describe basic features of a language family, without getting too
    complicated.
    - desc: overview
    - phonetics: how the language sounds, e.g. guttural, nasal, etc.
    - cultural influences: e.g. from other languages, or from
      historical events, migration patterns, etc.

    $$
        - lang_family_uid_pk: Primary key, unique identifier for each language family
        - char_set_uid_fk: Foreign key referencing the character set used by the language family
        - lang_family_name: Name of the language family
        - lang_family_desc: Description of the language family
        - phonetics: Description of the phonetics of the language family
        - cultural_influences: Description of the cultural influences on the language family
        - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LANG_FAMILY"
    lang_family_uid_pk: str = ""
    char_set_uid_fk: str = ""
    lang_family_name: str = ""
    lang_family_desc: str = ""
    phonetics: str = ""
    cultural_influences: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LangFamily)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lang_family_uid_pk"
        FK: dict = {"char_set_uid_fk": ("CHAR_SET", "char_set_uid_pk")}
        ORDER: list = ["lang_family_name ASC"]


class Language():
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

    $$
        - lang_uid_pk: Primary key, unique identifier for each language
        - lang_family_uid_fk: Foreign key referencing the language family this language belongs to
        - lang_name: Name of the language
        - lang_desc: Description of the language
        - gramatics: Description of the gramatics of the language
        - lexicals: Description of the lexicals of the language
        - social_influences: Description of the social influences on the language
        - word_formations: Description of the word formations of the language
        - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LANGUAGE"
    lang_uid_pk: str = ""
    lang_family_uid_fk: str = ""
    lang_name: str = ""
    lang_desc: str = ""
    gramatics: str = ""
    lexicals: str = ""
    social_influences: str = ""
    word_formations: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Language)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lang_uid_pk"
        FK: dict = {"lang_family_uid_fk": ("LANG_FAMILY", "lang_family_uid_pk")}
        ORDER: list = ["lang_name ASC"]


class LangDialect():
    """
    Describe basic features of a dialect, without getting too
    complicated.

    $$
        - dialect_uid_pk: Primary key, unique identifier for each dialect
        - lang_uid_fk: Foreign key referencing the language this dialect belongs to
        - dialect_name: Name of the dialect
        - dialect_desc: Description of the dialect
        - divergence_factors: Description of the divergence factors of the dialect
        - syncretic_factors: Description of the syncretic factors of the dialect
        - preservation_factors: Description of the preservation factors of the dialect
        - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LANG_DIALECT"
    dialect_uid_pk: str = ""
    lang_uid_fk: str = ""
    dialect_name: str = ""
    dialect_desc: str = ""
    divergence_factors: str = ""
    syncretic_factors: str = ""
    preservation_factors: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LangDialect)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "dialect_uid_pk"
        FK: dict = {"lang_uid_fk": ("LANGUAGE", "lang_uid_pk")}
        ORDER: list = ["dialect_name ASC"]


class GlossCommon():
    """
    The common glossary is in the "common" language, e.g. English.
    It serves as the 'Rosetta Stone' for all other languages, first
    for in-game ones. It can also be used for real world languages, or
    as the top-level 'parent' for a cascade of info; for example, when
    there are multiple types of glossary items associated with a subject.
    The primary key of a GlossCommon row is the FK reference for related
    Glossary items. In other words, many(Glossary) --> 1(GlossCommon).

    $$
        - gloss_common_uid_pk: Primary key, unique identifier for each common glossary item
        - dialect_uid_fk: Foreign key referencing the dialect this glossary item belongs to
        - gloss_type: Type of the glossary item
        - gloss_name: Name of the glossary item
        - gloss_value: Value of the glossary item
        - gloss_uri: URI of the glossary item
        - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "GLOSS_COMMON"
    gloss_common_uid_pk: str = ""
    dialect_uid_fk: str = ""
    gloss_type: str = ""
    gloss_name: str = ""
    gloss_value: str = ""
    gloss_uri: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(GlossCommon)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "gloss_common_uid_pk"
        FK: dict = {"dialect_uid_fk": ("LANG_DIALECT", "dialect_uid_pk")}
        CK: dict = {"gloss_type": EntityType.GLOSS_TYPE}
        ORDER: list = ["gloss_name ASC"]


class Glossary():
    """
    The glossary is a multi-lingual dictionary as well an extension
    for the GlossCommon items.

    $$
        - glossary_uid_pk: Primary key, unique identifier for each glossary item
        - gloss_common_uid_fk: Foreign key referencing the common glossary item
        - dialect_uid_fk: Foreign key referencing the dialect this glossary item belongs to
        - gloss_type: Type of the glossary item
        - gloss_name: Name of the glossary item
        - gloss_value: Value of the glossary item
        - gloss_uri: URI of the glossary item
        - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "GLOSSARY"
    glossary_uid_pk: str = ""
    gloss_common_uid_fk: str = ""
    dialect_uid_fk: str = ""
    gloss_type: str = ""
    gloss_name: str = ""
    gloss_value: str = ""
    gloss_uri: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Glossary)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "glossary_uid_pk"
        FK: dict = {
            "gloss_common_uid_fk": ("GLOSS_COMMON", "gloss_common_uid_pk"),
            "dialect_uid_fk": ("LANG_DIALECT", "dialect_uid_pk"),
        }
        CK: dict = {"gloss_type": EntityType.GLOSS_TYPE}
        ORDER: list = ["gloss_name ASC"]


# =============================================================
# Game Astronomy
# =============================================================
class Universe():
    """Define qualities of a game Universe.
    This is the highest, broadest container in the game model.
    A Universe may contain multiple Galactic Clusters.
    It is conceptualized for now as a sphere.

    $$
    - univ_uid_pk: Primary key, unique identifier for each universe
    - univ_name: Name of the universe
    - radius_gly: Radius of the universe in gigalightyears
    - volume_gly3: Volume of the universe in gigalightyears cubed
    - volume_pc3: Volume of the universe in parsecs cubed
    - age_gyr: Age of the universe in gigayears
    - expansion_rate_kmpsec_per_mpc: Expansion rate of the universe in km/sec per megaparsec
    - total_mass_kg: Total mass of the universe in kilograms
    - dark_energy_kg: Amount of dark energy in the universe in kilograms
    - dark_matter_kg: Amount of dark matter in the universe in kilograms
    - baryonic_matter_kg: Amount of baryonic matter in the universe in kilograms
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "UNIVERSE"
    univ_uid_pk: str = ""
    univ_name: str = ""
    radius_gly: float = 0.0
    volume_gly3: float = 0.0
    volume_pc3: float = 0.0
    age_gyr: float = 0.0
    expansion_rate_kmpsec_per_mpc: float = 0.0
    total_mass_kg: float = 0.0
    dark_energy_kg: float = 0.0
    dark_matter_kg: float = 0.0
    baryonic_matter_kg: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Universe)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "univ_uid_pk"
        ORDER: list = ["univ_name ASC"]


class ExternalUniv():
    """The External Universe defines qualities of the Game Universe
    which lie outside of the "playable" Universe. An External
    Universe is always 1:1 to a Universe. It has no shape, only mass.

    $$
    - external_univ_uid_pk: Primary key, unique identifier for each external universe
    - univ_uid_fk: Foreign key linking to the Universe table
    - external_univ_name: Name of the external universe
    - mass_kg: Mass of the external universe in kilograms
    - dark_energy_kg: Amount of dark energy in the external universe in kilograms
    - dark_matter_kg: Amount of dark matter in the external universe in kilograms
    - baryonic_matter_kg: Amount of baryonic matter in the external universe in kilograms
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "EXTERNAL_UNIVERSE"
    external_univ_uid_pk: str = ""
    univ_uid_fk: str = ""
    external_univ_name: str = ""
    mass_kg: float = 0.0
    dark_energy_kg: float = 0.0
    dark_matter_kg: float = 0.0
    baryonic_matter_kg: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(ExternalUniv)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "external_univ_uid_pk"
        FK: dict = {"univ_uid_fk": ("UNIVERSE", "univ_uid_pk")}
        ORDER: list = ["external_univ_name ASC"]


class GalacticCluster():
    """The Galactic Cluster defines a section of the Game Universe
    in which a particular game instance is played. A Galactic Cluster
    is contained by one Universe and it may contain multiple Galaxies.
    Conceptualized as a bulging shape, usually ellipsoid, centered in
    a boundary box.

    $$
    - galactic_cluster_uid_pk: Primary key, unique identifier for each galactic cluster
    - univ_uid_fk: Foreign key linking to the Universe table
    - galactic_cluster_name: Name of the galactic cluster
    - center_from_univ_center_gly_x: X coordinate of the center of the cluster in gigalightyears
    - center_from_univ_center_gly_y: Y coordinate of the center of the cluster in gigalightyears
    - center_from_univ_center_gly_z: Z coordinate of the center of the cluster in gigalightyears
    - boundary_gly_x: X coordinate of the boundary of the cluster in gigalightyears
    - boundary_gly_y: Y coordinate of the boundary of the cluster in gigalightyears
    - boundary_gly_z: Z coordinate of the boundary of the cluster in gigalightyears
    - cluster_shape: Shape of the cluster, default is 'ellipsoid'
    - shape_pc_x: X coordinate of the shape of the cluster in parsecs
    - shape_pc_y: Y coordinate of the shape of the cluster in parsecs
    - shape_pc_z: Z coordinate of the shape of the cluster in parsecs
    - shape_axes_a: Length of the major axis of the cluster in parsecs
    - shape_axes_b: Length of the minor axis of the cluster in parsecs
    - shape_axes_c: Length of the tertiary axis of the cluster in parsecs
    - shape_rot_pitch: Pitch rotation of the cluster in degrees
    - shape_rot_yaw: Yaw rotation of the cluster in degrees
    - shape_rot_roll: Roll rotation of the cluster in degrees
    - volume_pc3: Volume of the cluster in parsecs cubed
    - mass_kg: Mass of the cluster in kilograms
    - dark_energy_kg: Amount of dark energy in the cluster in kilograms
    - dark_matter_kg: Amount of dark matter in the cluster in kilograms
    - baryonic_matter_kg: Amount of baryonic matter in the cluster in kilograms
    - timing_pulsar_pulse_per_ms: Timing of the pulsar pulse in milliseconds
    - timing_pulsar_loc_gly_x: X coordinate of the pulsar location in gigalightyears
    - timing_pulsar_loc_gly_y: Y coordinate of the pulsar location in gigalightyears
    - timing_pulsar_loc_gly_z: Z coordinate of the pulsar location in gigalightyears
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "GALACTIC_CLUSTER"
    galactic_cluster_uid_pk: str = ""
    univ_uid_fk: str = ""
    galactic_cluster_name: str = ""

    # Expanded GroupStruct attributes
    center_from_univ_center_gly_x: float = 0.0
    center_from_univ_center_gly_y: float = 0.0
    center_from_univ_center_gly_z: float = 0.0
    boundary_gly_x: float = 0.0
    boundary_gly_y: float = 0.0
    boundary_gly_z: float = 0.0
    cluster_shape: str = "ellipsoid"
    shape_pc_x: float = 0.0
    shape_pc_y: float = 0.0
    shape_pc_z: float = 0.0
    shape_axes_a: float = 0.0
    shape_axes_b: float = 0.0
    shape_axes_c: float = 0.0
    shape_rot_pitch: float = 0.0
    shape_rot_yaw: float = 0.0
    shape_rot_roll: float = 0.0
    volume_pc3: float = 0.0
    mass_kg: float = 0.0
    dark_energy_kg: float = 0.0
    dark_matter_kg: float = 0.0
    baryonic_matter_kg: float = 0.0
    timing_pulsar_pulse_per_ms: float = 0.0
    timing_pulsar_loc_gly_x: float = 0.0
    timing_pulsar_loc_gly_y: float = 0.0
    timing_pulsar_loc_gly_z: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(GalacticCluster)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "galactic_cluster_uid_pk"
        FK: dict = {"univ_uid_fk": ("UNIVERSE", "univ_uid_pk")}
        CK: dict = {"cluster_shape": EntityType.CLUSTER_SHAPE}
        ORDER: list = ["galactic_cluster_name ASC"]


class Galaxy():
    """The Galaxy defines a section of the Galactic Cluster in
    which a particular game instance is played. A Galaxy is contained
    by a Galactic Cluster and it may contain multiple Star-Systems.
    Conceptualized as a sphere, centered in a boundary box.
    It has a bulge, typically ellipsoid, in the center and a star
    field area, also ellipsoid, but can include matter outside the
    star field, all the way to edge of its halo.
    x,y,z coordinates are relative to the Galactic Cluster unless otherwise noted.

    $$
    - galaxy_uid_pk: Primary key, unique identifier for each galaxy
    - galactic_cluster_uid_fk: Foreign key linking to the Galactic Cluster table
    - galaxy_name: Name of the galaxy
    - relative_size: Relative size of the galaxy, default is 'medium'
    - center_from_univ_center_kpc_x: X coordinate of the center of the galaxy in kiloparsecs
    - center_from_univ_center_kpc_y: Y coordinate of the center of the galaxy in kiloparsecs
    - center_from_univ_center_kpc_z: Z coordinate of the center of the galaxy in kiloparsecs
    - halo_radius_pc: Radius of the halo of the galaxy in parsecs
    - boundary_pc_x: X coordinate of the boundary of the galaxy in parsecs
    - boundary_pc_y: Y coordinate of the boundary of the galaxy in parsecs
    - boundary_pc_z: Z coordinate of the boundary of the galaxy in parsecs
    - volume_gpc3: Volume of the galaxy in gigaparsecs cubed
    - mass_kg: Mass of the galaxy in kilograms
    - bulge_shape: Shape of the bulge of the galaxy, default is 'ellipsoid'
    - bulge_center_from_center_ly_x: X coordinate of the center of the bulge
        from the center of the galaxy in lightyears
    - bulge_center_from_center_ly_y: Y coordinate of the center of the bulge
        from the center of the galaxy in lightyears
    - bulge_center_from_center_ly_z: Z coordinate of the center of the bulge
        from the center of the galaxy in lightyears
    - bulge_dim_axes_a: Length of the major axis of the bulge in lightyears
    - bulge_dim_axes_b: Length of the minor axis of the bulge in lightyears
    - bulge_dim_axes_c: Length of the tertiary axis of the bulge in lightyears
    - bulge_dim_rot_pitch: Pitch rotation of the bulge in degrees
    - bulge_dim_rot_yaw: Yaw rotation of the bulge in degrees
    - bulge_dim_rot_roll: Roll rotation of the bulge in degrees
    - bulge_black_hole_mass_kg: Mass of the black hole in the bulge in kilograms
    - bulge_volume_ly3: Volume of the bulge in lightyears cubed
    - bulge_total_mass_kg: Total mass of the bulge in kilograms
    - star_field_shape: Shape of the star field of the galaxy, default is 'ellipsoid'
    - star_field_dim_from_center_ly_x: X coordinate of the center of the star field
        from the center of the galaxy in lightyears
    - star_field_dim_from_center_ly_y: Y coordinate of the center of the star field
        from the center of the galaxy in lightyears
    - star_field_dim_from_center_ly_z: Z coordinate of the center of the star field
        from the center of the galaxy in lightyears
    - star_field_dim_axes_a: Length of the major axis of the star field in lightyears
    - star_field_dim_axes_b: Length of the minor axis of the star field in lightyears
    - star_field_dim_axes_c: Length of the tertiary axis of the star field in lightyears
    - star_field_dim_rot_pitch: Pitch rotation of the star field in degrees
    - star_field_dim_rot_yaw: Yaw rotation of the star field in degrees
    - star_field_dim_rot_roll: Roll rotation of the star field in degrees
    - star_field_vol_ly3: Volume of the star field in lightyears cubed
    - star_field_mass_kg: Mass of the star field in kilograms
    - interstellar_mass_kg: Mass of
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "GALAXY"
    galaxy_uid_pk: str = ""
    galactic_cluster_uid_fk: str = ""
    galaxy_name: str = ""
    relative_size: str = "medium"
    center_from_univ_center_kpc_x: float = 0.0
    center_from_univ_center_kpc_y: float = 0.0
    center_from_univ_center_kpc_z: float = 0.0
    halo_radius_pc: float = 0.0
    boundary_pc_x: float = 0.0
    boundary_pc_y: float = 0.0
    boundary_pc_z: float = 0.0
    volume_gpc3: float = 0.0
    mass_kg: float = 0.0
    bulge_shape: str = "ellipsoid"
    bulge_center_from_center_ly_x: float = 0.0
    bulge_center_from_center_ly_y: float = 0.0
    bulge_center_from_center_ly_z: float = 0.0
    bulge_dim_axes_a: float = 0.0
    bulge_dim_axes_b: float = 0.0
    bulge_dim_axes_c: float = 0.0
    bulge_dim_rot_pitch: float = 0.0
    bulge_dim_rot_yaw: float = 0.0
    bulge_dim_rot_roll: float = 0.0
    bulge_black_hole_mass_kg: float = 0.0
    bulge_volume_ly3: float = 0.0
    bulge_total_mass_kg: float = 0.0
    star_field_shape: str = "ellipsoid"
    star_field_dim_from_center_ly_x: float = 0.0
    star_field_dim_from_center_ly_y: float = 0.0
    star_field_dim_from_center_ly_z: float = 0.0
    star_field_dim_axes_a: float = 0.0
    star_field_dim_axes_b: float = 0.0
    star_field_dim_axes_c: float = 0.0
    star_field_dim_rot_pitch: float = 0.0
    star_field_dim_rot_yaw: float = 0.0
    star_field_dim_rot_roll: float = 0.0
    star_field_vol_ly3: float = 0.0
    star_field_mass_kg: float = 0.0
    interstellar_mass_kg: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Galaxy)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "galaxy_uid_pk"
        FK: dict = {
            "galactic_cluster_uid_fk": ("GALACTIC_CLUSTER", "galactic_cluster_uid_pk")
        }
        CK: dict = {
            "relative_size": EntityType.RELATIVE_SIZE,
            "bulge_shape": EntityType.ASTRO_SHAPE,
            "star_field_shape": EntityType.ASTRO_SHAPE,
        }
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


class StarSystem():
    """A Star System is a collection of planets, moons, and other objects.
    Usually it has one star, but it can have multiple stars.
    In most cases, we are only interested in star systems that include
    at least one habitable planet, but we can include others.
    Conceptualized as a bulging shape, usually ellipsoid, centered in
    a boundary box.
    x,y,z coordinates are relative to the Galaxy unless otherwise noted.

    $$
    - star_system_uid_pk: Primary key, unique identifier for each star system
    - galaxy_uid_fk: Foreign key linking to the Galaxy table
    - star_system_name: Name of the star system
    - is_black_hole: Indicates if the star system contains a black hole
    - is_pulsar: Indicates if the star system contains a pulsar
    - boundary_pc_x: X coordinate of the boundary of the star system in parsecs
    - boundary_pc_y: Y coordinate of the boundary of the star system in parsecs
    - boundary_pc_z: Z coordinate of the boundary of the star system in parsecs
    - volume_pc3: Volume of the star system in parsecs cubed
    - mass_kg: Mass of the star system in kilograms
    - system_shape: Shape of the star system, default is 'ellipsoid'
    - center_from_galaxy_center_pc_x: X coordinate of the center of the star system
        from the center of the galaxy in parsecs
    - center_from_galaxy_center_pc_y: Y coordinate of the center of the star system
        from the center of the galaxy in parsecs
    - center_from_galaxy_center_pc_z: Z coordinate of the center of the star system
        from the center of the galaxy in parsecs
    - system_dim_axes_a: Length of the major axis of the star system in parsecs
    - system_dim_axes_b: Length of the minor axis of the star system in parsecs
    - system_dim_axes_c: Length of the tertiary axis of the star system in parsecs
    - system_dim_rot_pitch: Pitch rotation of the star system in degrees
    - system_dim_rot_yaw: Yaw rotation of the star system in degrees
    - system_dim_rot_roll: Roll rotation of the star system in degrees
    - relative_size: Relative size of the star system, default is 'medium'
    - spectral_class: Spectral class of the star, default is 'G'
    - aprox_age_gyr: Approximate age of the star system in gigayears
    - luminosity_class: Luminosity class of the star, default is 'V'
    - frequency_of_flares: Frequency of solar flares, default is 'rare'
    - intensity_of_flares: Intensity of solar flares, default is 'low'
    - frequency_of_comets: Frequency of comets, default is 'rare'
    - unbound_planets_cnt: Number of unbound planets in the star system
    - orbiting_planets_cnt: Number of planets orbiting the star
    - inner_habitable_boundary_au: Inner boundary of the habitable zone in astronomical units
    - outer_habitable_boundary_au: Outer boundary of the habitable zone in astronomical units
    - planetary_orbits_shape: Shape of the planetary orbits, default is 'circular'
    - orbital_stability: Stability of the planetary orbits, default is 'stable'
    - asteroid_belt_density: Density of the asteroid belt, default is 'sparse'
    - asteroid_belt_loc: Location of the asteroid belt, default is 'inner'
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "STAR_SYSTEM"
    star_system_uid_pk: str = ""
    galaxy_uid_fk: str = ""
    star_system_name: str = ""
    is_black_hole: bool = False
    is_pulsar: bool = False
    boundary_pc_x: float = 0.0
    boundary_pc_y: float = 0.0
    boundary_pc_z: float = 0.0
    volume_pc3: float = 0.0
    mass_kg: float = 0.0
    system_shape: str = "ellipsoid"
    center_from_galaxy_center_pc_x: float = 0.0
    center_from_galaxy_center_pc_y: float = 0.0
    center_from_galaxy_center_pc_z: float = 0.0
    system_dim_axes_a: float = 0.0
    system_dim_axes_b: float = 0.0
    system_dim_axes_c: float = 0.0
    system_dim_rot_pitch: float = 0.0
    system_dim_rot_yaw: float = 0.0
    system_dim_rot_roll: float = 0.0
    relative_size: str = "medium"
    spectral_class: str = "G"
    aprox_age_gyr: float = 0.0
    luminosity_class: str = "V"
    frequency_of_flares: str = "rare"
    intensity_of_flares: str = "low"
    frequency_of_comets: str = "rare"
    unbound_planets_cnt: int = 0
    orbiting_planets_cnt: int = 0
    inner_habitable_boundary_au: float = 0.0
    outer_habitable_boundary_au: float = 0.0
    planetary_orbits_shape: str = "circular"
    orbital_stability: str = "stable"
    asteroid_belt_density: str = "sparse"
    asteroid_belt_loc: str = "inner"
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(StarSystem)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "star_system_uid_pk"
        FK: dict = {"galaxy_uid_fk": ("GALAXY", "galaxy_uid_pk")}
        CK: dict = {
            "relative_size": EntityType.RELATIVE_SIZE,
            "spectral_class": EntityType.SPECTRAL_CLASS,
            "luminosity_class": EntityType.LUMINOSITY_CLASS,
            "system_shape": EntityType.ASTRO_SHAPE,
            "planetary_orbits_shape": EntityType.ORBITAL_SHAPE,
            "orbital_stability": EntityType.STABILITY,
            "asteroid_belt_density": EntityType.DENSITY,
            "asteroid_belt_loc": EntityType.ASTRO_LOCATION,
            "frequency_of_flares": EntityType.FREQUENCY,
            "intensity_of_flares": EntityType.INTENSITY,
            "frequency_of_comets": EntityType.FREQUENCY,
        }
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

In some cases, it may be easier to generate the data using an
AI-assisted algorithm, then design the DB tables based on that.
"""


class World():
    """
    A World is a planet within a Star System. It may be habitable or not.
    A World is associated with one Star System, and multiple Worlds can be
    associated with one Star System.

    A number of the attributes are just left as text descriptions at this
    point in order to avoid too much complexity. These will be replaced
    with more specific attributes as the game model is further developed.

    $$
    - world_uid_pk: Primary key, unique identifier for each world
    - star_system_uid_fk: Foreign key referencing the Star System table
    - world_name: Name of the world
    - world_type: Type of the world, default is 'habitable'
    - obliquity_dg: Axial tilt of the world in degrees
    - distance_from_star_au: Distance from the star in astronomical units
    - distance_from_star_km: Distance from the star in kilometers
    - radius_km: Radius of the world in kilometers
    - mass_kg: Mass of the world in kilograms
    - gravity_m_per_s_per_s: Gravity of the world in meters per second squared
    - orbit_gdy: Orbital period of the world in galactic days
    - orbit_gyr: Orbital period of the world in galactic years
    - is_tidally_locked: Indicates if the world is tidally locked
    - rotation_gdy: Rotation period of the world in galactic days
    - rotation_direction: Direction of rotation, default is 'prograde'
    - orbit_direction: Direction of orbit, default is 'prograde'
    - moons_cnt: Number of moons orbiting the world
    - world_desc: Description of the world
    - atmosphere: Composition of the atmosphere
    - sky_color: Color of the sky
    - biosphere: Presence of life forms
    - sentients: Presence of intelligent life
    - climate: Climate of the world
    - tech_level: Technological level of the world
    - terrain: Terrain of the world
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "WORLD"
    world_uid_pk: str = ""
    star_system_uid_fk: str = ""
    world_name: str = ""
    world_type: str = "habitable"
    obliquity_dg: float = 0.0  # a/k/a axial tilt
    distance_from_star_au: float = 0.0
    distance_from_star_km: float = 0.0
    radius_km: float = 0.0
    mass_kg: float = 0.0
    gravity_m_per_s_per_s: float = 0.0
    orbit_gdy: float = 0.0
    orbit_gyr: float = 0.0
    is_tidally_locked: bool = False
    rotation_gdy: float = 0.0
    rotation_direction: str = "prograde"
    orbit_direction: str = "prograde"
    moons_cnt: int = 0
    world_desc: str = ""
    atmosphere: str = ""
    sky_color: str = "blue"
    biosphere: str = ""
    sentients: str = ""
    climate: str = ""
    tech_level: str = ""
    terrain: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(World)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "world_uid_pk"
        FK: dict = {"star_system_uid_fk": ("STAR_SYSTEM", "star_system_uid_pk")}
        CK: dict = {
            "world_type": EntityType.WORLD_TYPE,
            "rotation_direction": EntityType.ASTRO_DIRECTION,
            "orbit_direction": EntityType.ASTRO_DIRECTION,
        }
        ORDER: list = ["world_name ASC"]


class Moon():
    """
    A Moon is any type of permanent satellite around a World that
    is large enough to be seen from the planet.
    A Moon is associated with one World, and multiple Moons can be
    associated with one World.

    $$
    - moon_uid_pk: Primary key, unique identifier for each moon
    - world_uid_fk: Foreign key referencing the World table
    - moon_name: Name of the moon in "Common" language glossary
    - moon_desc: Description of the moon
    - moon_lore: Lore of the moon
    - center_from_world_center_km: Distance from the center of the world in kilometers
    - mass_kg: Mass of the moon in kilograms
    - radius_km: Radius of the moon in kilometers
    - obliquity_dg: Axial tilt of the moon in degrees
    - is_tidally_locked: Indicates if the moon is tidally locked
    - rotation_direction: Direction of rotation, default is 'prograde'
    - orbit_direction: Direction of orbit, default is 'prograde'
    - orbit_world_days: Orbital period of the moon in world days
    - rotation_world_days: Rotation period of the moon in world days
    - initial_velocity: Initial velocity of the moon in meters per second
    - angular_velocity: Angular velocity of the moon in radians per second
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "MOON"
    moon_uid_pk: str = ""
    world_uid_fk: str = ""
    moon_name: str = ""
    moon_desc: str = ""
    moon_lore: str = ""
    center_from_world_center_km: float = 0.0
    mass_kg: float = 0.0
    radius_km: float = 0.0
    obliquity_dg: float = 0.0  # a/k/a axial tilt
    is_tidally_locked: bool = True
    rotation_direction: str = "prograde"
    orbit_direction: str = "prograde"
    orbit_world_days: float = 0.0
    rotation_world_days: float = 0.0
    initial_velocity: float = 0.0
    angular_velocity: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Moon)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "moon_uid_pk"
        FK: dict = {"world_uid_fk": ("WORLD", "world_uid_pk")}
        CK: dict = {
            "rotation_direction": EntityType.ASTRO_DIRECTION,
            "orbit_direction": EntityType.ASTRO_DIRECTION,
        }
        ORDER: list = ["moon_name ASC"]


# =============================================================
# Time
# =============================================================
class SolarYear():
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
      the year. Typically this is 1. But some game cultures
      count multiple solar years as 1 "year" on their calendar.
      And they don't account for leap days/years in the same way.

    $$
    - solar_year_uid_pk: Primary key, unique identifier for each solar year
    - world_uid_fk: Foreign key linking to the World table
    - lang_uid_fk: Foreign key linking to the Language table
    - solar_year_key: Key for the solar year
    - version_id: Version of the solar year
    - solar_year_name: Name of the solar year
    - solar_year_desc: Description of the solar year
    - solar_year_span: Number of solar revolutions in the year
    - days_in_solar_year: Number of days in the solar year
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "SOLAR_YEAR"
    solar_year_uid_pk: str = ""
    world_uid_fk: str = ""
    lang_uid_fk: str = ""
    solar_year_key: str = ""
    version_id: str = ""
    solar_year_name: str = ""
    solar_year_desc: str = ""
    solar_year_span: float = 0.0
    days_in_solar_year: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(SolarYear)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "solar_year_uid_pk"
        FK: dict = {
            "world_uid_fk": ("WORLD", "world_uid_pk"),
            "lang_uid_fk": ("LANGUAGE", "lang_uid_pk"),
        }
        ORDER: list = ["solar_year_key ASC"]


class Season():
    """
    A Season defines the length of a season as proportion of a Solar year.
    It is categoriezed as one or more of the four seasons in common
    use on Earth, which are defined as a type category.
    Seaons also vary depending on which hemisphere they relate
    to, also defined as a type.
    Names of seasons are handled as virtual foreign keys to a common
    glossary item, which means they are optional and and not enforced
    by a foreign key constraint.
    - years_in_season: Number of years in the season. This is
      typically close to 0.25, but can be any value. If it is greater
      than 1, this indicates that a season is longer than a year, which
      is bizarre but may be possible in some fantastic game settings.

    $$
    - season_uid_pk: Primary key, unique identifier for each season
    - solar_year_uid_fk: Foreign key linking to the Solar Year table
    - gloss_common_uid_vfk: Virtual foreign key linking to the Common Glossary table
    - season_type: Type of the season
    - hemisphere_type: Hemisphere of the season
    - years_in_season: Number of years in the season
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "SEASON"
    season_uid_pk: str = ""
    solar_year_uid_fk: str = ""
    gloss_common_uid_vfk: str = ""
    season_type: str = ""
    hemisphere_type: str = ""
    years_in_season: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Season)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "season_uid_pk"
        FK: dict = {"solar_year_uid_fk": ("SOLAR_YEAR", "solar_year_uid_pk")}
        CK: dict = {
            "season_type": EntityType.SEASON_TYPE,
            "hemisphere_type": EntityType.HEMISPHERE_TYPE,
        }
        ORDER: list = ["season_uid_pk ASC", "season_type ASC"]


class LunarYear():
    """
    A Lunar Year is always associated with a World, within a
    given Star System. And with one __or more__ Moon cycles.
    Which of the World's moons are being referenced is
    hanlded by the LunarYearXMoons association table.

    Duration of each moon's revolution around the world and
    its relative position per other satellites will be handled
    by computations. The LunarYear table contains the total
    number of World days in the lunar year, whether it is based on
    a single satellite or a composite. The day is always in
    relation to the world's rotation w/r/t its sun.

    The Lunar Year is astronomical data and not a Calendar.
    The link to language is optional, a virtual foreign key, and is
    not enforced by a foreign key constraint.

    $$
    - lunar_year_uid_pk: Primary key, unique identifier for each lunar year
    - world_uid_fk: Foreign key linking to the World table
    - lang_uid_vfk: Virtual foreign key linking to the Language table
    - lunar_year_name: Name of the lunar year
    - lunar_year_desc: Description of the lunar year
    - days_in_lunar_year: Number of days in the lunar year
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LUNAR_YEAR"
    lunar_year_uid_pk: str = ""
    world_uid_fk: str = ""
    lang_uid_vfk: str = ""
    lunar_year_name: str = ""
    lunar_year_desc: str = ""
    days_in_lunar_year: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LunarYear)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lunar_year_uid_pk"
        FK: dict = {"world_uid_fk": ("WORLD", "world_uid_pk")}
        ORDER: list = ["lunar_year_key ASC"]


class LunarYearXMoon():
    """
    Associative keys --
    - LUNAR_YEARs (n) <--> MOONs (n)
    This table associates Lunar Year astro data with a specific moon.

    $$
    - lunar_year_x_moon_uid_pk: Primary key, unique identifier for each association
    - lunar_year_uid_fk: Foreign key linking to the Lunar Year table
    - moon_uid_fk: Foreign key linking to the Moon table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LUNAR_YEAR_X_MOON"
    lunar_year_x_moon_uid_pk: str = ""
    lunar_year_uid_fk: str = ""
    moon_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LunarYearXMoon)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lunar_year_x_moon_uid_pk"
        FK: dict = {
            "lunar_year_uid_fk": ("LUNAR_YEAR", "lunar_year_uid_pk"),
            "moon_uid_fk": ("MOON", "moon_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}


class SolarCalendar():
    """
    A Solar Calendar is a cultural artifact. It is associated with
    a Solar Year. The name of the calendar is defined as a virtual
    (optional) link to a common glossary item but is also recorded as text.
    Months, Weeks, Days, Hours, etc are defined in distinct tables
    that are associated with Solar and/or Lunar Calendars.

    - epoch_start_offset is the first year in this calendrical system,
      in relationship to the default "epoch start" year for the game.
      Need to figure out how/where to define the epoch start for a given world.

    $$
    - solar_calendar_uid_pk: Primary key, unique identifier for each solar calendar
    - solar_year_uid_fk: Foreign key linking to the Solar Year table
    - year_name_gloss_common_uid_vfk: Virtual foreign key linking to the Common Glossary table
    - season_start_uid_fk: Foreign key linking to the Season table
    - solar_calendar_name: Name of the solar calendar
    - solar_calendar_desc: Description of the solar calendar
    - epoch_start_offset: Offset from the epoch start year
    - months_in_year: Number of months in the year
    - watches_in_day: Number of watches in the day
    - hours_in_watch: Number of hours in the watch
    - minutes_in_hour: Number of minutes in the hour
    - seconds_in_minute: Number of seconds in the minute
    - leap_year: Number of leap years
    - leap_month: Number of leap months
    - leap_days: Number of leap days
    - leap_rule: Rule for handling leap years
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "SOLAR_CALENDAR"
    solar_calendar_uid_pk: str = ""
    solar_year_uid_fk: str = ""
    year_name_gloss_common_uid_vfk: str = ""
    season_start_uid_fk: str = ""
    solar_calendar_name: str = ""
    solar_calendar_desc: str = ""
    epoch_start_offset: int = 0
    months_in_year: int = 0
    watches_in_day: int = 0
    hours_in_watch: int = 0
    minutes_in_hour: int = 0
    seconds_in_minute: int = 0
    leap_year: int = 0
    leap_month: int = 0
    leap_days: int = 0
    leap_rule: str = "add_to_end_of_nth_month"
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(SolarCalendar)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "solar_calendar_uid_pk"
        FK: dict = {
            "solar_year_uid_fk": ("SOLAR_YEAR", "solar_year_uid_pk"),
            "season_start_uid_fk": ("SEASON", "season_uid_pk"),
        }
        CK: dict = {"leap_rule": EntityType.LEAP_RULE}
        ORDER: list = ["solar_calendar_id ASC"]


class LunarCalendar():
    """
    A Lunar Calendar is a cultural artifact associated with
    a Lunar Year. The name of the calendar is defined as an optional link to
    a common glossary item but is also recorded as text.

    $$
    - lunar_calendar_uid_pk: Primary key, unique identifier for each lunar calendar
    - lunar_year_uid_fk: Foreign key linking to the Lunar Year table
    - lunar_year_name_gloss_common_uid_vfk: Virtual foreign key linking to the Common Glossary table
    - lunar_calendar_name: Name of the lunar calendar
    - lunar_calendar_desc: Description of the lunar calendar
    - epoch_start_offset: Offset from the epoch start year
    - days_in_month: Number of days in the month
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LUNAR_CALENDAR"
    lunar_calendar_uid_pk: str = ""
    lunar_year_uid_fk: str = ""
    lunar_year_name_gloss_common_uid_vfk: str = ""
    lunar_calendar_name: str = ""
    lunar_calendar_desc: str = ""
    epoch_start_offset: int = 0
    days_in_month: int = 0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LunarCalendar)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lunar_calendar_uid_pk"
        FK: dict = {"lunar_year_uid_fk": ("LUNAR_YEAR", "lunar_year_uid_pk")}
        ORDER: list = ["lunar_calendar_id ASC"]


class Month():
    """
    A Month is associated with 1..n Calendars via an
    association table.
    - is_leap_day_month: true if the month contains leap day/s
    - is_leap_month: true if entire month is leap days

    $$
    - month_uid_pk: Primary key, unique identifier for each month
    - month_name_gloss_common_uid_vfk: Virtual foreign key linking to the Common Glossary table
    - month_name: Name of the month
    - days_in_month: Number of World days in the month
    - month_order: Ordinal number of the month
    - is_leap_day_month: Indicates if the month contains leap day/s
    - is_leap_month: Indicates if the entire month is leap days
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "MONTH"
    month_uid_pk: str = ""
    month_name_gloss_common_uid_vfk: str = ""
    month_name: str = ""
    days_in_month: int = 0
    month_order: int = 0
    is_leap_day_month: bool = False
    is_leap_month: bool = False
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Month)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "month_uid_pk"
        ORDER: list = ["month_id ASC"]


class SolarCalendarXMonth():
    """
    Associative keys --
    - SOLAR_CALENDARs (n) <--> MONTHs (n)
    This table associates Solar Calendar data with a set of Months.

    $$
    - solar_calendar_x_moon_uid_pk: Primary key, unique identifier for each association
    - solar_calendar_uid_fk: Foreign key linking to the Solar Calendar table
    - month_uid_fk: Foreign key linking to the Month table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "SOLAR_CALENDAR_X_MONTH"
    solar_calendar_x_moon_uid_pk: str = ""
    solar_calendar_uid_fk: str = ""
    month_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(SolarCalendarXMonth)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "solar_calendar_x_moon_uid_pk"
        FK: dict = {
            "solar_calendar_uid_fk": ("SOLAR_CALENDAR", "solar_calendar_uid_pk"),
            "month_uid_fk": ("MONTH", "month_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}


class LunarCalendarXMonth():
    """
    Associative keys --
    - LUNAR_CALENDARs (n) <--> MONTHs (n)
    This table associates Lunar Calendar data with a
    set of Months.

    $$
    - lunar_calendar_x_moon_uid_pk: Primary key, unique identifier for each association
    - lunar_calendar_uid_fk: Foreign key linking to the Lunar Calendar table
    - month_uid_fk: Foreign key linking to the Month table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LUNAR_CALENDAR_X_MONTH"
    lunar_calendar_x_moon_uid_pk: str = ""
    lunar_calendar_uid_fk: str = ""
    month_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LunarCalendarXMonth)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lunar_calendar_x_moon_uid_pk"
        FK: dict = {
            "lunar_calendar_uid_fk": ("LUNAR_CALENDAR", "lunar_calendar_uid_pk"),
            "month_uid_fk": ("MONTH", "month_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}


class WeekTime():
    """
    WeekTime is associated with 1..n Calendars via an
    association table.
    It describes any reckoning of days that is
    shorter than an average month. It is not necessarily
    the 7 days we are accustomed to. It could be a fortnight,
    a special 5 day week, or a 3 day holiday week.
    - week_time_order: optional; order of week if multiple different
      types of week in a month and they have an order
    - is_leap_week_time: true if the week contains only leap day/s

    $$
    - week_time_uid_pk: Primary key, unique identifier for each week time
    - week_time_name_gloss_common_uid_vfk: Virtual foreign key linking to the Common Glossary table
    - week_time_name: Name of the week time
    - week_time_desc: Description of the week time
    - days_in_week_time: Number of days in the week time
    - week_time_order: Order of the week time
    - is_leap_week_time: Indicates if the week time contains leap day/s
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "WEEK_TIME"
    week_time_uid_pk: str = ""
    week_time_name_gloss_common_uid_vfk: str = ""
    week_time_name: str = ""
    week_time_desc: str = ""
    days_in_week_time: int = 0
    week_time_order: int = 0
    is_leap_week_time: bool = False
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(WeekTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "week_time_uid_pk"
        ORDER: list = ["week_time_id ASC"]


class SolarCalendarXWeekTime():
    """
    Associative keys --
    - SOLAR_CALENDARs (n) <--> WEEK_TIMEs (n)
    This table associates Solar Calendar data with a set of Week Times.

    $$
    - solar_calendar_x_week_time_uid_pk: Primary key, unique identifier for each association
    - solar_calendar_uid_fk: Foreign key linking to the Solar Calendar table
    - week_time_uid_fk: Foreign key linking to the Week Time table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "SOLAR_CALENDAR_X_WEEK_TIME"
    solar_calendar_x_week_time_uid_pk: str = ""
    solar_calendar_uid_fk: str = ""
    week_time_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(SolarCalendarXWeekTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "solar_calendar_x_week_time_uid_pk"
        FK: dict = {
            "solar_calendar_uid_fk": ("SOLAR_CALENDAR", "solar_calendar_uid_pk"),
            "week_time_uid_fk": ("WEEK_TIME", "week_time_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}


class LunarCalendarXWeekTime():
    """
    Associative keys --
    - LUNAR_CALENDARs (n) <--> WEEK_TIMEs (n)
    This table associates Lunar Calendar data with a set of Week Times.

    $$
    - lunar_calendar_x_week_time_uid_pk: Primary key, unique identifier for each association
    - lunar_calendar_uid_fk: Foreign key linking to the Lunar Calendar table
    - week_time_uid_fk: Foreign key linking to the Week Time table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LUNAR_CALENDAR_X_WEEK_TIME"
    lunar_calendar_x_week_time_uid_pk: str = ""
    lunar_calendar_uid_fk: str = ""
    week_time_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LunarCalendarXWeekTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lunar_calendar_x_week_time_uid_pk"
        FK: dict = {
            "lunar_calendar_uid_fk": ("LUNAR_CALENDAR", "lunar_calendar_uid_pk"),
            "week_time_uid_fk": ("WEEK_TIME", "week_time_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}


class DayTime():
    """
    DayTime is associated with 1..n Weeks via an association table.
    It describes any reckoning of time construed in
    hours that is longer than one hour and not longer
    that a full day. It is not necessarily the 24 hours
    day we are accustomed to. It could be a 12 hour
    half-day, a 6 hour "watch" and so on.
    - day_time_number: order of day in a week
    - is_leap_day_time: true if the day is only a leap day

    $$
    - day_time_uid_pk: Primary key, unique identifier for each day time
    - day_time_name_gloss_common_uid_vfk: Virtual foreign key linking to the Common Glossary table
    - day_time_name: Name of the day time
    - day_time_desc: Description of the day time
    - hours_in_day_time: Number of hours in the day time
    - day_time_number: Order of the day in a week
    - is_leap_day_time: Indicates if the day time is only a leap day
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "DAY_TIME"
    day_time_uid_pk: str = ""
    day_time_name_gloss_common_uid_vfk: str = ""
    day_time_name: str = ""
    day_time_desc: str = ""
    hours_in_day_time: int = 0
    day_time_number: int = 0
    is_leap_day_time: bool = False
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(DayTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "day_time_uid_pk"
        ORDER: list = ["day_time_id ASC"]


class WeekTimeXDayTime():
    """
    Associative keys --
    - WEEK_TIMEs (n) <--> DAY_TIMEs (n)
    This table associates Week Time data with a set of Day Times.

    $$
    - week_time_x_day_time_uid_pk: Primary key, unique identifier for each association
    - week_time_uid_fk: Foreign key linking to the Week Time table
    - day_time_uid_fk: Foreign key linking to the Day Time table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "WEEK_TIME_X_DAY_TIME"
    week_time_x_day_time_uid_pk: str = ""
    week_time_uid_fk: str = ""
    day_time_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(WeekTimeXDayTime)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "week_time_x_day_time_uid_pk"
        FK: dict = {
            "week_time_uid_fk": ("WEEK_TIME", "week_time_uid_pk"),
            "day_time_uid_fk": ("DAY_TIME", "day_time_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}


# Next: Hours, Scenes, Locations, Buildings, Sets, Characters, Inventories,
#  Services, etc.
# Come back and add these (and maybe more) afer doing some more work on tying
# the front end and middle ware to the new database and data model, including
# generation of initial set-up data.


# =============================================================
# Game Geography
# =============================================================
class Lake():
    """
    Geographic features, e.g. lakes, rivers, mountains, are
    named by reference to a gloss_common_uid_pk.

    Geo features have a complex line defined by series of
    points, often defined by latitude and longitude.
    The more points, the more precise the curve or lines.
    Points stored as JSON with an undetermined length.
    SQL generator code identifies them via a classmethod
    constraint keyed by "JSON".' SQLite supports a JSON
    data type, but not sure yet what that buys us vs test or blob.

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

    $$
    - lake_uid_pk: Primary key, unique identifier for each lake
    - gloss_common_uid_vfk: Foreign key linking to the Common Glossary table
    - lake_name: Name of the lake
    - lake_shoreline_points_json: JSON of the lake shoreline points
    - lake_size: Size of the lake
    - water_type: Type of water
    - lake_type: Type of lake
    - is_tidal_influence: Indicates if the lake has tidal influence
    - lake_surface_m2: Surface area of the lake
    - max_depth_m: Maximum depth of the lake
    - avg_depth_m: Average depth of the lake
    - lake_altitude_m: Altitude of the lake
    - catchment_area_radius_m: Catchment area radius of the lake
    - lake_origin: Origin of the lake
    - flora_and_fauna: Flora and fauna of the lake
    - water_color: Color of the water
    - accessibility: Accessibility of the lake
    - special_features: Special features of the lake
    - lake_usage: Usage of the lake
    - lake_lore: Legends or myths of the lake
    - lake_history: History of the lake
    - conservation_status: Conservation status of the lake
    - current_conditions: Current conditions of the lake
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LAKE"
    lake_uid_pk: str = ""
    gloss_common_uid_vfk: str = ""
    lake_name: str = ""
    lake_shoreline_points_json: str = ""
    lake_size: str = "medium"
    water_type: str = "freshwater"
    lake_type: str = "lake"
    is_tidal_influence: bool = False
    lake_surface_m2: float = 0.0
    max_depth_m: float = 0.0
    avg_depth_m: float = 0.0
    lake_altitude_m: float = 0.0
    catchment_area_radius_m: float = 0.0
    lake_origin: str = ""
    flora_and_fauna: str = ""
    water_color: str = ""
    accessibility: str = ""
    special_features: str = ""
    lake_usage: str = ""
    lake_lore: str = ""
    lake_history: str = ""
    conservation_status: str = ""
    current_conditions: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Lake)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lake_uid_pk"
        JSON: list = ["lake_shoreline_points_json"]
        CK: dict = {
            "lake_size": EntityType.LAKE_SIZE,
            "water_type": EntityType.WATER_TYPE,
            "lake_type": EntityType.LAKE_TYPE,
        }
        ORDER: list = ["lake_uid_pk ASC"]


class LakeXMap():
    """
    Associative keys --
    - LAKEs (n) <--> MAPs (n)

    $$
    - lake_x_map_pk: Primary key, unique identifier for each association
    - lake_uid_fk: Foreign key linking to the Lake table
    - map_uid_fk: Foreign key linking to the Map table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LAKE_X_MAP"
    lake_x_map_pk: str = ""
    lake_uid_fk: str = ""
    map_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LakeXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "lake_x_map_pk"
        FK: dict = {
            "lake_uid_fk": ("LAKE", "lake_uid_pk"),
            "map_uid_fk": ("MAP", "map_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}
        ORDER: list = ["lake_uid_fk ASC", "map_uid_fk ASC"]


class River():
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

    $$
    - river_uid_pk: Primary key, unique identifier for each river
    - gloss_common_uid_vfk: Foreign key linking to the Common Glossary table
    - river_name: Name of the river
    - river_course_points_json: JSON of the river course points
    - river_bank_points_json: JSON of the river bank points
    - river_type: Type of river
    - avg_width_m: Average width of the river
    - avg_depth_m: Average depth of the river
    - total_length_km: Total length of the river
    - drainage_basin_km: Drainage basin of the river
    - avg_velocity_m_per_h: Average velocity of the river
    - gradient_m_per_km: Gradient of the river
    - river_hazards_json: JSON of the river hazards
    - river_features_json: JSON of the river features
    - river_nav_type: Type of river navigation
    - flora_and_fauna: Flora and fauna of the river
    - water_quality: Quality of the water
    - historical_events: Historical events of the river
    - current_conditions: Current conditions of the river
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "RIVER"
    river_uid_pk: str = ""
    gloss_common_uid_vfk: str = ""
    river_name: str = ""
    river_course_points_json: str = ""
    river_bank_points_json: str = ""
    river_type: str = "perrenial"
    avg_width_m: float = 0.0
    avg_depth_m: float = 0.0
    total_length_km: float = 0.0
    drainage_basin_km: float = 0.0
    avg_velocity_m_per_h: float = 0.0
    gradient_m_per_km: float = 0.0
    river_hazards_json: str = ""
    river_features_json: str = ""
    river_nav_type: str = "none"
    flora_and_fauna: str = ""
    water_quality: str = ""
    historical_events: str = ""
    current_conditions: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(River)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "river_uid_pk"
        CK: dict = {
            "river_type": EntityType.RIVER_TYPE,
            "river_nav_type": EntityType.RIVER_NAV_TYPE,
        }
        JSON: list = [
            "river_course_points_json",
            "river_bank_points_json",
            "river_hazards_json",
            "river_features_json",
        ]
        ORDER: list = ["river_uid_pk ASC"]


class RiverXMap():
    """
    Associative keys --
    - RIVERs (n) <--> MAPs (n)

    $$
    - river_x_map_uid_pk: Primary key, unique identifier for each association
    - river_uid_fk: Foreign key linking to the River table
    - map_uid_fk: Foreign key linking to the Map table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "RIVER_X_MAP"
    river_x_map_uid_pk: str = ""
    river_uid_fk: str = ""
    map_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(RiverXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "river_x_map_uid_pk"
        FK: dict = {
            "river_uid_fk": ("RIVER", "river_uid_pk"),
            "map_uid_fk": ("MAP", "map_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}
        ORDER: list = ["river_x_map_uid_pk ASC"]


class OceanBody():
    """For bodies of water associated with oceans.

    $$
    - ocean_body_uid_pk: Primary key, unique identifier for each ocean body
    - gloss_common_uid_vfk: Foreign key linking to the Common Glossary table
    - ocean_body_name: Name of the ocean body
    - body_shoreline_points_json: JSON of the body shoreline points
    - is_coastal: Indicates if the body is coastal
    - is_frozen: Indicates if the body is frozen
    - ocean_body_type: Type of ocean body
    - water_type: Type of water
    - is_tidal_influence: Indicates if the body has tidal influence
    - tidal_flows_per_day: Number of tidal flows per day
    - avg_high_tide_m: Average high tide
    - avg_low_tide_m: Average low tide
    - max_high_tide_m: Maximum high tide
    - ocean_wave_type: Type of ocean wave
    - body_surface_area_m2: Surface area of the body
    - body_surface_altitude_m: Altitude of the body
    - max_depth_m: Maximum depth of the body
    - avg_depth_m: Average depth of the body
    - ocean_hazards_json: JSON of the ocean hazards
    - ocean_features_json: JSON of the ocean features
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "OCEAN_BODY"
    ocean_body_uid_pk: str = ""
    gloss_common_uid_vfk: str = ""
    ocean_body_name: str = ""
    body_shoreline_points_json: str = ""
    is_coastal: bool = True
    is_frozen: bool = False
    ocean_body_type: str = ""
    water_type: str = ""
    is_tidal_influence: bool = False
    tidal_flows_per_day: int = 0
    avg_high_tide_m: float = 0.0
    avg_low_tide_m: float = 0.0
    max_high_tide_m: float = 0.0
    ocean_wave_type: str = ""
    body_surface_area_m2: float = 0.0
    body_surface_altitude_m: float = 0.0
    max_depth_m: float = 0.0
    avg_depth_m: float = 0.0
    ocean_hazards_json: str = ""
    ocean_features_json: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(OceanBody)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "ocean_body_uid_pk"
        CK: dict = {
            "ocean_body_type": EntityType.OCEAN_BODY_TYPE,
            "water_type": EntityType.WATER_TYPE,
            "ocean_wave_type": EntityType.OCEAN_WAVE_TYPE,
        }
        JSON: list = [
            "river_course_points_json",
            "river_bank_points_json",
            "ocean_hazards_json",
            "ocean_features_json",
        ]
        ORDER: list = ["ocean_body_uid_pk ASC"]


class OceanBodyXMap():
    """
    Associative keys --
    - OCEAN_BODY (n) <--> MAP (n)

    $$
    - ocean_body_x_map_uid_pk: Primary key, unique identifier for each association
    - ocean_body_uid_fk: Foreign key linking to the Ocean Body table
    - map_uid_fk: Foreign key linking to the Map table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "OCEAN_BODY_X_MAP"
    ocean_body_x_map_uid_pk: str = ""
    ocean_body_uid_fk: str = ""
    map_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(OceanBodyXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "ocean_body_x_map_uid_pk"
        FK: dict = {
            "ocean_body_uid_fk": ("OCEAN_BODY", "ocean_body_uid_pk"),
            "map_uid_fk": ("MAP", "map_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}
        ORDER: list = ["ocean_body_x_map_uid_pk ASC"]


class OceanBodyXRiver():
    """
    Associative keys --
    - OCEAN_BODY (n) <--> RIVER (n)

    $$
    - ocean_body_x_river_uid_pk: Primary key, unique identifier for each association
    - ocean_body_uid_fk: Foreign key linking to the Ocean Body table
    - river_uid_fk: Foreign key linking to the River table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "OCEAN_BODY_X_RIVER"
    ocean_body_x_river_uid_pk: str = ""
    ocean_body_uid_fk: str = ""
    river_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(OceanBodyXRiver)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "ocean_body_x_river_uid_pk"
        FK: dict = {
            "ocean_body_uid_fk": ("OCEAN_BODY", "ocean_body_uid_pk"),
            "river_uid_fk": ("RIVER", "river_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}
        ORDER: list = ["ocean_body_x_river_uid_pk ASC"]


class LandBody():
    """
    Use this for geographic features that are not water.
    Including: continents, islands, geographic regions.

    $$
    - land_body_uid_pk: Primary key, unique identifier for each land body
    - gloss_common_uid_vfk: Foreign key linking to the Common Glossary table
    - land_body_name: Name of the land body
    - body_landline_points_json: JSON of the land body line points
    - land_body_type: Type of land body
    - land_body_surface_area_m2: Surface area of the land body
    - land_body_surface_avg_altitude_m: Average altitude of the land body
    - max_altitude_m: Maximum altitude of the land body
    - min_altitude_m: Minimum altitude of the land body
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LAND_BODY"
    land_body_uid_pk: str = ""
    gloss_common_uid_vfk: str = ""
    land_body_name: str = ""
    body_landline_points_json: str = ""
    land_body_type: str = ""
    land_body_surface_area_m2: float = 0.0
    land_body_surface_avg_altitude_m: float = 0.0
    max_altitude_m: float = 0.0
    min_altitude_m: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LandBody)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "land_body_uid_pk"
        CK: dict = {"land_body_type": EntityType.LAND_BODY_TYPE}
        ORDER: list = ["land_body_uid_pk ASC"]


class LandBodyXMap():
    """
    Associative keys --
    - LAND_BODY (n) <--> MAP (n)

    $$
    - land_body_x_map_uid_pk: Primary key, unique identifier for each association
    - land_body_uid_fk: Foreign key linking to the Land Body table
    - map_uid_fk: Foreign key linking to the Map table
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LAND_BODY_X_MAP"
    land_body_x_map_uid_pk: str = ""
    land_body_uid_fk: str = ""
    map_uid_fk: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LandBodyXMap)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "land_body_x_map_uid_pk"
        FK: dict = {
            "land_body_uid_fk": ("LAND_BODY", "land_body_uid_pk"),
            "map_uid_fk": ("MAP", "map_uid_pk"),
        }
        CK: dict = {"touch_type": EntityType.TOUCH_TYPE}
        ORDER: list = ["land_body_x_map_uid_pk ASC"]


class LandBodyXLandBody():
    """
    Associative keys --
    - LAND_BODY (n) <--> LAND_BODY (n)
    - relation:
        - body 1 --> body 2

    $$
    - land_body_x_land_body_uid_pk: Primary key, unique identifier for each association
    - land_body_1_uid_fk: Foreign key linking to the Land Body table
    - land_body_2_uid_fk: Foreign key linking to the Land Body table
    - land_land_relation_type: Type of land-land relation
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LAND_BODY_X_LAND_BODY"
    land_body_x_land_body_uid_pk: str = ""
    land_body_1_uid_fk: str = ""
    land_body_2_uid_fk: str = ""
    land_land_relation_type: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LandBodyXLandBody)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "land_body_x_land_body_uid_pk"
        FK: dict = {
            "land_body_1_uid_fk": ("LAND_BODY", "land_body_uid_pk"),
            "land_body_2_uid_fk": ("LAND_BODY", "land_body_uid_pk"),
        }
        CK: dict = {
            "land_land_relation_type": EntityType.LAND_LAND_RELATION_TYPE,
            "touch_type": EntityType.TOUCH_TYPE,
        }
        ORDER: list = ["land_body_x_land_body_uid_pk ASC"]


class LandBodyXOceanBody():
    """
    Associative keys --
    - LAND_BODY (n) <--> OCEAN_BODY (n)

    $$
    - land_body_x_ocean_body_uid_pk: Primary key, unique identifier for each association
    - land_body_uid_fk: Foreign key linking to the Land Body table
    - ocean_body_uid_fk: Foreign key linking to the Ocean Body table
    - land_ocean_relation_type: Type of land-ocean relation
    - touch_type: Type of association
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "LAND_BODY_X_OCEAN_BODY"
    land_body_x_ocean_body_uid_pk: str = ""
    land_body_uid_fk: str = ""
    ocean_body_uid_fk: str = ""
    land_ocean_relation_type: str = ""
    touch_type: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(LandBodyXOceanBody)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints():
        PK: str = "land_body_x_ocean_body_uid_pk"
        FK: dict = {
            "land_body_uid_fk": ("LAND_BODY", "land_body_uid_pk"),
            "ocean_body_uid_fk": ("OCEAN_BODY", "ocean_body_uid_pk"),
        }
        CK: dict = {
            "land_ocean_relation_type": EntityType.LAND_OCEAN_RELATION_TYPE,
            "touch_type": EntityType.TOUCH_TYPE,
        }
        ORDER: list = ["land_body_x_ocean_body_uid_pk ASC"]
