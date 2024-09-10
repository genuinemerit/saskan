"""

:module:    data_model_app.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.

# x Convert g_ and t_ configs to database tables.
# x Convert the APP values on c_context.json to db tables.
# - Convert the schema files to db tables: services, ontology
# - Convert the time and scenes to db tables.
# - If needed, modify the geo and astro db tables per schema files
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
class Backup(object):
    """Store metadata about DB backup, restore, archive, export."""

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
        return DM.orm_to_dict(Backup)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"bkup_uid_pk": ["bkup_uid_pk"]}
        ORDER: list = ["bkup_dttm DESC", "bkup_name ASC"]
        CK: dict = {"bkup_type": EntityType.BACKUP_TYPE}


class Texts(object):
    """Define static text strings used in the app GUI.
    - Language code of the text, eg, 'en', 'de', 'fr'
    - Name/ID/label of a text string, not unique. shared
      across languages..
    - Text string value.
    """

    _tablename: str = "TEXTS"
    text_uid_pk: str = ""
    lang_code: str = ""
    text_name: str = ""
    text_value: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.orm_to_dict(Texts)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"text_uid_pk": ["text_uid_pk"]}
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["text_name ASC", "lang_code ASC"]


# If it turns out the be useful, may want to add an "APP" structure


class Frames(object):
    """Define the values for frames i.e., the outermost window.
    - Optionally may have info-bar and page-header
    - frame_id: not unique, can be shared by apps,
       e.g. 'admin' or 'game'
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
        return DM.orm_to_dict(Frames)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"frame_uid_pk": ["frame_uid_pk"]}
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["frame_id ASC"]


class MenuBars(object):
    """Define dimensions for Menu Bars used in frames.
    - frame_id: match to FRAMES record(s)
    There is no displayed text on this structure; it is a container.
    Its width (w) is derived from width of the frame.
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
        return DM.orm_to_dict(MenuBars)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"menu_bar_uid_pk": ["menu_bar_uid_pk"]}
        FK: dict = {"frame_uid_fk": ("FRAMES", "frame_uid_pk")}
        ORDER: list = ["frame_id ASC"]


class Menus(object):
    """Define the values for Menus, i.e, name of a dropdown.
    - menu_id: generic string label "ID" or key for menu
    - menu_name: text string label for menu in designated language
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
        return DM.orm_to_dict(Menus)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"menu_uid_pk": ["menu_uid_pk"]}
        FK: dict = {"menu_bar_uid_fk": ("MENU_BARS", "menu_bar_uid_pk")}
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["menu_id ASC", "lang_code ASC", "menu_name ASC"]


class MenuItems(object):
    """Define the values for Menu Items, i.e, each item on a Dropdown.
    - item_id: generic string label "ID" or key for menu item
    - item_name: text string label for menu in designated language
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
    enabled_default: bool = True
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.orm_to_dict(MenuItems)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"item_uid_pk": ["item_uid_pk"]}
        FK: dict = {"menu_uid_fk": ("MENUS", "menu_uid_pk")}
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["item_id ASC", "lang_code ASC", "item_name ASC"]


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
        return DM.orm_to_dict(Windows)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"win_uid_pk": ["win_uid_pk"]}
        FK: dict = {"frame_uid_fk": ("FRAMES", "frame_uid_pk")}
        CK: dict = {"lang_code": EntityType.LANG_CODE}
        ORDER: list = ["win_id ASC", "lang_code ASC"]


class Links(object):
    """Define the values for URIs used in the app.
    - link_name: displayed name for the link
    - link_value: URI to retrieve
    - link_icon: name of a file in app images directory
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
    link_icon: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.orm_to_dict(Links)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"link_uid_pk": ["link_uid_pk"]}
        CK: dict = {
            "link_protocol": EntityType.LINK_PROTOCOL,
            "lang_code": EntityType.LANG_CODE,
            "mime_type": EntityType.MIME_TYPE,
        }
        ORDER: list = ["frame_id ASC", "link_id ASC", "lang_code ASC"]


class ButtonSingle(object):
    """Define the values for binary buttons used in the app.
    - button_name: displayed name for the button
    - button_icon: name of a file in app images directory
      or empty string for no icon
    - button_key: key to press to activate button
    - x, y: position of top-left relative to window
    - enabled: True to enable, False to disable
    - help_text: text to display when mouse hovers over button
    - action: name of function to call when button is clicked
    """

    _tablename: str = "BUTTON_SINGLE"
    button_single_uid_pk: str = ""
    button_type: str = ""
    button_name: str = ""
    button_icon: str = ""
    button_key: str = ""
    frame_uid_fk: str = ""
    window_uid_fk: str = ""
    x: float = 0.0
    y: float = 0.0
    enabled: bool = True
    help_text: str = ""
    action: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.orm_to_dict(ButtonSingle)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"button_single_uid_pk": ["button_single_uid_pk"]}
        FK: dict = {
            "frame_uid_fk": ("FRAMES", "frame_uid_pk"),
            "window_uid_fk": ("WINDOWS", "window_uid_pk"),
        }
        CK: dict = {"button_type": EntityType.BUTTON_TYPE}
        ORDER: list = ["button_name ASC"]


class ButtonMulti(object):
    """Define values for multi-choice button group"""

    _tablename: str = "BUTTON_MULTI"
    button_multi_uid_pk: str = ""
    button_type: str = ""
    button_name: str = ""
    button_icon: str = ""
    frame_uid_fk: str = ""
    window_uid_fk: str = ""
    x: float = 0.0
    y: float = 0.0
    enabled: bool = True
    help_text: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.orm_to_dict(ButtonMulti)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"button_multi_uid_pk": ["button_multi_uid_pk"]}
        FK: dict = {
            "frame_uid_fk": ("FRAMES", "frame_uid_pk"),
            "window_uid_fk": ("WINDOWS", "window_uid_pk"),
        }
        CK: dict = {"button_type": EntityType.BUTTON_TYPE}
        ORDER: list = ["button_name ASC"]


class ButtonItem(object):
    """Define values for button item within a check or
    radio button group.
    """

    _tablename: str = "BUTTON_ITEM"
    button_item_uid_pk: str = ""
    button_multi_uid_fk: str = ""
    button_name: str = ""
    button_icon: str = ""
    button_order: int = 0
    button_action: str = ""
    is_enabled: bool = True
    help_text: str = ""
    delete_dt: str = ""

    def to_dict(self) -> dict:
        """Convert object to dict."""
        return DM.orm_to_dict(ButtonItem)

    def from_dict(self, p_dict: dict, p_row: int) -> dict:
        """Load DB SELECT results into memory."""
        return DM.orm_from_dict(self, p_dict, p_row)

    class Constraints(object):
        PK: dict = {"button_item_uid_pk": ["button_item_uid_pk"]}
        FK: dict = {"button_multi_uid_fk": ("BUTTON_MULTI", "button_multi_uid_pk")}
        ORDER: list = ["button_name ASC"]
