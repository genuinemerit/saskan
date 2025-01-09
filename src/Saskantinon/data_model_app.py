"""

:module:    data_model_app.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.

Data models for core components of the app,
like frames, buttons, menus and links.

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

# =============================================================
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
# System Maintenance
# =============================================================
class Metadata:
    """Metadata augemnting the database's standard meta.
    Mainly field definitions.
    $$
    - meta_uid_pk: Primary key
    - name_space: [app|story]
    - model_name: name of the data model class
    - tbl_name: name of the SQL table
    - col_name: name of the SQL column
    - col_def: definition of the SQL column
    - delete_ts: date/time of virtual deletion
    $$
    """

    _tablename: str = "METADATA"
    meta_uid_pk: str = ""  # Primary key
    name_space: str = ""
    model_name: str = ""
    tbl_name: str = ""
    col_name: str = ""
    col_def: str = ""
    delete_ts: str = ""

    class Constraints:
        PK: str = "meta_uid_pk"
        ORDER: list = ["tbl_name ASC", "col_name ASC"]
        CK: dict = {"name_space": EntityType.NAME_SPACE}


class Backup(object):
    """Store metadata about DB backup, restore, archive, export.
    $$
    - bkup_uid_pk: Primary key
    - bkup_name: Name of the backup
    - bkup_dttm: Date and time of the backup
    - bkup_type: Type of backup, e.g., 'full', 'incremental'
    - file_from: Source file or directory
    - file_to: Destination file or directory
    - delete_dt: Date and time the record was deleted
    $$
    """

    _tablename: str = "BACKUP"
    bkup_uid_pk: str = ""  # Primary key
    bkup_name: str = ""
    bkup_dttm: str = ""
    bkup_type: str = ""
    file_from: str = ""
    file_to: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert attributes to OrderedDict."""
        return DM.cols_to_dict(Backup)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "bkup_uid_pk"
        ORDER: list = ["bkup_dttm DESC", "bkup_name ASC"]
        CK: dict = {"bkup_type": EntityType.BACKUP_TYPE}


class Texts(object):
    """Define static text strings used in the app GUI.
    - Language code of the text, eg, 'en', 'de', 'fr'
    - Name/ID/label of a text string, not unique. shared
      across languages..
    - Text string value.
    $$
    - text_uid_pk: Primary key, unique identifier for each text entry
    - lang_code: Language code of the text, e.g., en, de, fr
    - text_name: Name/ID/label of a text string, not unique, shared across languages
    - text_value: Text string value
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "TEXTS"
    text_uid_pk: str = ""
    lang_code: str = ""
    text_name: str = ""
    text_value: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Texts)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "text_uid_pk"
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["text_name ASC", "lang_code ASC"]


# If it turns out the be useful, may want to add an "APP" structure


class Frames(object):
    """Define the values for frames i.e., the outermost window.
    - Optionally may have info-bar and page-header

    $$
    - frame_uid_pk: Primary key, unique identifier for each frame entry
    - lang_code: Language code of the frame, e.g., en, de, fr
    - frame_id: Not unique, can be shared by apps, e.g., 'admin' or 'game'
    - frame_title: Title of the frame
    - frame_desc: Description of the frame
    - frame_w: Width of the frame
    - frame_h: Height of the frame
    - pg_hdr_x: X-coordinate of the page header
    - pg_hdr_y: Y-coordinate of the page header
    - pg_hdr_w: Width of the page header
    - pg_hdr_h: Height of the page header
    - pg_hdr_txt: Text displayed in the page header
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$
    """

    _tablename: str = "FRAMES"
    frame_uid_pk: str = ""
    lang_code: str = ""
    frame_id: str = ""
    frame_title: str = ""
    frame_desc: str = ""
    frame_w: float = 0.0
    frame_h: float = 0.0
    pg_hdr_x: float = 0.0
    pg_hdr_y: float = 0.0
    pg_hdr_w: float = 0.0
    pg_hdr_h: float = 0.0
    pg_hdr_txt: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Frames)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "frame_uid_pk"
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["frame_id ASC"]


class MenuBars(object):
    """Define dimensions for Menu Bars used in frames.
    - frame_id: Match to FRAMES record(s)

    $$
    - menu_bar_uid_pk: Primary key, unique identifier for each menu bar entry
    - frame_uid_fk: Foreign key referencing the frame's unique identifier
    - frame_id: Identifier to match with corresponding frame records
    - mbar_margin: Margin around the menu bar
    - mbar_h: Height of the menu bar
    - mbar_x: X-coordinate of the top-left corner relative to the frame
    - mbar_y: Y-coordinate of the top-left corner relative to the frame
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    There is no displayed text on this structure; it is a container.
    Its width (w) is derived from the width of the frame.
    Its top-left x, y is relative to the frame.
    """

    _tablename: str = "MENU_BARS"
    menu_bar_uid_pk: str = ""
    frame_uid_fk: str = ""
    frame_id: str = ""
    mbar_margin: float = 0.0
    mbar_h: float = 0.0
    mbar_x: float = 0.0
    mbar_y: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(MenuBars)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "menu_bar_uid_pk"
        FK: dict = {"frame_uid_fk": ("FRAMES", "frame_uid_pk")}
        ORDER: list = ["frame_id ASC"]


class Menus(object):
    """Define the values for Menus, i.e., name of a dropdown.

    $$
    - menu_uid_pk: Primary key, unique identifier for each menu entry
    - menu_bar_uid_fk: Foreign key referencing the associated menu bar
    - frame_id: Identifier to match with corresponding frame records
    - lang_code: Language code for the menu text
    - menu_id: Generic string label "ID" or key for menu
    - menu_name: Text string label for menu in designated language
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "MENUS"
    menu_uid_pk: str = ""
    menu_bar_uid_fk: str = ""
    frame_id: str = ""
    lang_code: str = ""
    menu_id: str = ""
    menu_name: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Menus)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "menu_uid_pk"
        FK: dict = {"menu_bar_uid_fk": ("MENU_BARS", "menu_bar_uid_pk")}
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["menu_id ASC", "lang_code ASC", "menu_name ASC"]


class MenuItems(object):
    """Define the values for Menu Items, i.e., each item on a Dropdown.

    $$
    - item_uid_pk: Primary key, unique identifier for each menu item entry
    - menu_uid_fk: Foreign key referencing the associated menu
    - lang_code: Language code for the menu item text
    - frame_id: Identifier to match with corresponding frame records
    - item_id: Generic string label "ID" or key for menu item
    - item_order: Order of the item within the menu
    - item_name: Text string label for menu item in designated language
    - key_binding: Shortcut key binding for the menu item
    - help_text: Help text or description for the menu item
    - enabled_by_default: Boolean indicating if the item is enabled by default
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "MENU_ITEMS"
    item_uid_pk: str = ""
    menu_uid_fk: str = ""
    lang_code: str = ""
    frame_id: str = ""
    item_id: str = ""
    item_order: int = 0
    item_name: str = ""
    key_binding: str = ""
    help_text: str = ""
    enabled_by_default: bool = True
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(MenuItems)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "item_uid_pk"
        FK: dict = {"menu_uid_fk": ("MENUS", "menu_uid_pk")}
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["item_id ASC", "lang_code ASC", "item_name ASC"]


class Windows(object):
    """Define the values for screens within the game.

    $$
    - win_uid_pk: Primary key, unique identifier for each window entry
    - frame_uid_fk: Foreign key referencing the associated frame
    - frame_id: Identifier to match with corresponding frame records
    - lang_code: Language code for the window text
    - win_id: Generic string label "ID" or key for the window
    - win_title: Title of the window in designated language
    - win_margin: Margin size around the window
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "WINDOWS"
    win_uid_pk: str = ""
    frame_uid_fk: str = ""
    frame_id: str = ""
    lang_code: str = ""
    win_id: str = ""
    win_title: str = ""
    win_margin: float = 0.0
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Windows)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "win_uid_pk"
        FK: dict = {"frame_uid_fk": ("FRAMES", "frame_uid_pk")}
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["win_id ASC", "lang_code ASC"]


class Links(object):
    """Define the values for URIs used in the app.

    $$
    - link_uid_pk: Primary key, unique identifier for each link entry
    - lang_code: Language code associated with the link
    - link_id: Identifier for the specific link
    - frame_id: Identifier for the frame associated with the link
    - link_protocol: Protocol type (e.g., HTTP, HTTPS) used by the link
    - mime_type: MIME type specifying the nature of the link content
    - link_name: Descriptive name of the link
    - link_value: The actual URI or address represented by the link
    - link_icon: Icon representing the link visually (stored as BLOB)
    - link_icon_path: Path to the icon file
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "LINKS"
    link_uid_pk: str = ""
    lang_code: str = ""
    link_id: str = ""
    frame_id: str = ""
    link_protocol: str = ""
    mime_type: str = ""
    link_name: str = ""
    link_value: str = ""
    link_icon: bytes = b""
    link_icon_path: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(Links)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "link_uid_pk"
        CK: dict = {
            "link_protocol": EntityType.LINK_PROTOCOL,
            "lang_code": EntityType.LANG_CODE,
            "mime_type": EntityType.MIME_TYPE,
        }
        ORDER: list = ["frame_id ASC", "link_id ASC", "lang_code ASC"]


class ButtonSingle(object):
    """Define the values for binary buttons used in the app.

    $$
    - button_single_uid_pk: Primary key, unique identifier for each button entry
    - button_type: Type of button (e.g., submit, reset)
    - button_name: Displayed name for the button
    - button_icon: Binary data representing the button's icon image
    - button_icon_path: Path to the icon file in the app images directory
    - button_key: Key to press to activate the button
    - frame_uid_fk: Foreign key linking to the associated frame
    - window_uid_fk: Foreign key linking to the associated window
    - left_x: X-coordinate position of top-left corner relative to the window
    - top_y: Y-coordinate position of top-left corner relative to the window
    - enabled_by_default: True to enable, False to disable the button
    - help_text: Text to display when the mouse hovers over the button
    - action: Name of the function to call when the button is clicked
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "BUTTON_SINGLE"
    button_single_uid_pk: str = ""
    button_type: str = ""
    button_name: str = ""
    button_icon: bytes = b""
    button_icon_path: str = ""
    button_key: str = ""
    frame_uid_fk: str = ""
    window_uid_fk: str = ""
    left_x: float = 0.0
    top_y: float = 0.0
    enabled_by_default: bool = True
    help_text: str = ""
    action: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(ButtonSingle)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "button_single_uid_pk"
        FK: dict = {
            "frame_uid_fk": ("FRAMES", "frame_uid_pk"),
            "window_uid_fk": ("WINDOWS", "window_uid_pk"),
        }
        CK: dict = {"button_type": EntityType.BUTTON_TYPE}
        ORDER: list = ["button_name ASC"]


class ButtonMulti(object):
    """Define values for multi-choice button group.

    $$
    - button_multi_uid_pk: Primary key, unique identifier for each button group entry
    - button_type: Type of button group (e.g., radio, checkbox)
    - button_name: Displayed name for the button group
    - button_icon: Binary data representing the button group's icon image
    - button_icon_path: Path to the icon file in the app images directory
    - frame_uid_fk: Foreign key linking to the associated frame
    - window_uid_fk: Foreign key linking to the associated window
    - x: X-coordinate position of top-left corner relative to the window
    - y: Y-coordinate position of top-left corner relative to the window
    - enabled_by_default: True to enable, False to disable the button group
    - help_text: Text to display when the mouse hovers over the button group
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "BUTTON_MULTI"
    button_multi_uid_pk: str = ""
    button_type: str = ""
    button_name: str = ""
    button_icon: bytes = b""
    button_icon_path: str = ""
    frame_uid_fk: str = ""
    window_uid_fk: str = ""
    left_x: float = 0.0
    top_y: float = 0.0
    enabled_by_default: bool = True
    help_text: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(ButtonMulti)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "button_multi_uid_pk"
        FK: dict = {
            "frame_uid_fk": ("FRAMES", "frame_uid_pk"),
            "window_uid_fk": ("WINDOWS", "window_uid_pk"),
        }
        CK: dict = {"button_type": EntityType.BUTTON_TYPE}
        ORDER: list = ["button_name ASC"]


class ButtonItem(object):
    """Define values for button item within a check or radio button group.

    $$
    - button_item_uid_pk: Primary key, unique identifier for each button item
    - button_multi_uid_fk: Foreign key linking to the associated multi-choice button group
    - button_name: Displayed name for the button item
    - button_icon: Binary data representing the button item's icon image
    - button_icon_path: Path to the icon file in the app images directory
    - button_order: Integer defining the display order of the button item within the group
    - button_action: Action or command executed when the button is pressed
    - enabled_by_default: True to enable, False to disable the button item by default
    - is_enabled: Indicates if the button item is currently enabled
    - help_text: Text to display when the mouse hovers over the button item
    - delete_dt: Deletion date, indicating when the record was marked for deletion
    $$

    """

    _tablename: str = "BUTTON_ITEM"
    button_item_uid_pk: str = ""
    button_multi_uid_fk: str = ""
    button_name: str = ""
    button_icon: bytes = b""
    button_icon_path: str = ""
    button_order: int = 0
    button_action: str = ""
    enabled_by_default: bool = True
    is_enabled: bool = True
    help_text: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.cols_to_dict(ButtonItem)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.rec_to_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: str = "button_item_uid_pk"
        FK: dict = {"button_multi_uid_fk": ("BUTTON_MULTI", "button_multi_uid_pk")}
        ORDER: list = ["button_name ASC"]
