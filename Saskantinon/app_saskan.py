"""

:module:    app_saskantinon.py
:author:    GM (genuinemerit @ pm.me)

Saskan App GUI.  pygame version.

    Note:
    For scaling images, see: https://www.pygame.org/docs/ref/transform.html
    Example: scaled_image =\
        pygame.transform.scale(original_image, (new_width, new_height))

@DEV:
- Prototype basic game activities like:
    - map generation
    - avatar placement/movement
    - physics
    - sound and music
- Use pygame for everything.
- Go for more features, better performance than earler prototypes,
    but don't worry about interactiviity or complete game yet.
    Focus most on prototyping the windows and widgets.

    @TODO:
    - Refactor based on DB and data model implementations.
    - Implement auto-test scenarios.
"""

# trunk-ignore(bandit/B403)
# import pickle           # remove this eventually
import pygame as pg
import sys
import webbrowser

from copy import copy
from dataclasses import dataclass
from pprint import pprint as pp     # noqa: F401, format like pp for files
from pprint import pformat as pf    # noqa: F401, format like pp for files
from pygame.locals import *         # noqa: F401, F403

from data_base import DataBase
from data_pg_structs import PygColors, AppDisplay
from data_get import GetData
from method_files import FileMethods    # type: ignore
from method_shell import ShellMethods   # type: ignore

CLR = PygColors()
DSP = AppDisplay()
GD = GetData()
DB_CFG = GD.get_db_config()
DB = DataBase(DB_CFG)
FM = FileMethods()
SM = ShellMethods()

pg.init()


@dataclass(frozen=True)
class PG:

    FRM = GD.get_by_id('FRAMES', 'frame_id', 'saskan', DB_CFG)
    pg.display.set_caption(FRM['frame_title'])
    DSP.WIN_W = float(FRM['frame_w'])
    DSP.WIN_H = float(FRM['frame_h'])
    DSP.WIN_MID = (DSP.WIN_W / 2, DSP.WIN_H / 2)
    flags = pg.RESIZABLE
    DSP.WIN = pg.display.set_mode((DSP.WIN_W, DSP.WIN_H), flags)
    DSP.TIMER = pg.time.Clock()


class GameMenu(object):
    """Manage Menu objects. Populate DSP.MENUS.
    Define a surface for clickable top-level menu bar members,
    drop-down menus associated with them, and items on each menu.
    Clicking on a menu bar member opens or closes a Menu.
    Clicking on Menu Item triggers an event or sets a status and
      may also close Menu.
    """
    def __init__(self):
        """Initialize the GameMenu object MNU.
        Store menu data and rendering info in DSP.MENUS.
        """
        self.set_menu_bars()
        self.set_menu_items()
        self.draw_menu_bar()
        self.draw_menu_items()

    def set_menu_bars(self) -> dict:
        """
        - Set up menu bars and menus names in DSP.MENUS.
        - Compute rendering info for menu bar members.
          Center menu text; align spacing to text width.

        - pg.Rect(left, top, width, height)  = ((x,y),(w,h))
        - txt = menu name rendered in pyg font
        - tbox = measure for text, not used in rendering
        - mb_box = pg rect around text + margin
        - ib_box = bounding box of menu's items
        """
        def get_menu_bar_data():
            """Retrieve menu bar and menu data from data base.
            """
            mbar_rec = GD.get_by_id(
                'MENU_BARS', 'frame_uid_fk',
                PG.FRM['frame_uid_pk'], DB_CFG)
            menu_rec = GD.get_by_id(
                'MENUS', 'menu_bar_uid_fk',
                mbar_rec['menu_bar_uid_pk'], DB_CFG,
                p_first_only=False)
            DSP.MENUS =\
                {m['menu_id']:
                    {'name': m['menu_name'],
                     'uid': m['menu_uid_pk'],
                     'selected': False, 'txt': '',
                     'tbox': None, 'mb_box': None,
                     'ib_box': None, 'mitems': {}}
                    for m in menu_rec}
            return mbar_rec

        def set_menu_bar_rendering(mbar_rec: dict):
            """Computer rendering boxes for menu bar.
            The mb_box is the box around the text. It gets renedered as a rect.
            The tbox defines the destination rec in a blit() command, so it is
              to be defined to be centered inside the mb_box.
            The txt is the surface for the blit() command.
            """
            x = mbar_rec['mbar_x']
            for m_ix, m_id in enumerate(list(DSP.MENUS.keys())):
                DSP.MENUS[m_id]['txt'] = DSP.F_SANS_SM.render(
                    DSP.MENUS[m_id]['name'],
                    True, CLR.CP_BLUEPOWDER, CLR.CP_GRAY_DARK)
                tbox = DSP.MENUS[m_id]['txt'].get_rect()
                mb_box = pg.Rect(tbox)
                mb_box.x = x
                mb_box.y = mbar_rec['mbar_y']
                mb_box.h = mbar_rec['mbar_h'] * 1.5
                mb_box.w *= 1.5
                DSP.MENUS[m_id]['mb_box'] = mb_box
                tbox.center = mb_box.center
                DSP.MENUS[m_id]['tbox'] = tbox
                x += mb_box.width

        # ====== set_menu_bars method ======
        mbar_rec = get_menu_bar_data()
        set_menu_bar_rendering(mbar_rec)

    def set_menu_items(self):
        """
        - Get menu item datea from DB and put into DSP.MENUS.
        - Compute rendering info for menu items.
        - mi_box: pg rect around tbox + margin for each item
        """
        def get_menu_item_data():
            """Retrieve menu iitem data from data base."""
            for menu_id, mnu in DSP.MENUS.items():
                mitm_recs =\
                    GD.get_by_id('MENU_ITEMS', 'menu_uid_fk',
                                 mnu['uid'], DB_CFG, p_first_only=False)
                for mi in mitm_recs:
                    id = mi['item_id']
                    DSP.MENUS[menu_id]['mitems'][id]: dict = {
                        "order": mi['item_order'],
                        "name": mi['item_name'],
                        "key_binding": mi['key_binding'],
                        "enabled": mi['enabled_default'],
                        'txt_enabled': None,
                        'txt_disabled': None,
                        'mi_box': None,
                        'uid': mi['item_uid_pk']}
                DSP.MENUS[menu_id]['mitems'] =\
                    SM.convert_dict_to_ordered_dict(
                        DSP.MENUS[menu_id]['mitems'])

        def set_menu_item_rendering():
            """Compute rendering boxes for menu items."""
            for mn_id, menu in DSP.MENUS.items():
                for mi_id, m_item in menu['mitems'].items():
                    item_k = DSP.MENUS[mn_id]['mitems'][mi_id]
                    item_k['txt_enabled'] = DSP.F_SANS_SM.render(
                        m_item['name'], True, CLR.CP_BLUEPOWDER,
                        CLR.CP_GRAY_DARK)
                    item_k['txt_disabled'] = DSP.F_SANS_SM.render(
                        m_item['name'], True, CLR.CP_BLUEPOWDER,
                        CLR.CP_GRAY_DARK)
                    tbox = item_k['txt_enabled'].get_rect()
                    mi_box = pg.Rect(tbox)
                    mi_box.x = DSP.MENUS[mn_id]['mb_box'].left
                    mi_box.h = tbox.h * 1.5
                    mi_box.w = tbox.w * 1.5
                    mi_box.y = DSP.MENUS[mn_id]['mb_box'].bottom + 12 +\
                        (mi_box.h * m_item['order'])
                    item_k['mi_box'] = mi_box
                    tbox.x += 12
                    item_k['tbox'] = tbox

        def set_menu_items_bounding_box():
            """Compute bounding box for menu items.
            It should be as wide as the widest menu item and
            and tall as the total height of all items."""
            pass
            for mn_id, menu in DSP.MENUS.items():
                widest_w = 0.0
                total_h = 0.0
                for mi_id, m_item in menu['mitems'].items():
                    widest_w = max(widest_w, m_item['mi_box'].width)
                    total_h += m_item['mi_box'].height
                DSP.MENUS[mn_id]['ib_box'] = pg.Rect(
                    menu['mb_box'].left,
                    menu['mb_box'].bottom,
                    widest_w, total_h)

        # ========= set_menu_items() method ====
        get_menu_item_data()
        set_menu_item_rendering()
        set_menu_items_bounding_box()

    def draw_menu_bar(self):
        """ Draw each each of the Menus on the Menu Bar.
        Redraw on every refresh. First everything in unselected mode.
        Then selected, draw box using green box).
        Only one (or none) menus can be selected.
        """
        for mb_i, mb_v in DSP.MENUS.items():
            box_color = CLR.CP_BLUEPOWDER if mb_v['selected'] is False\
                else CLR.CP_GREEN
            pg.draw.rect(DSP.WIN, box_color, mb_v['mb_box'], width=2)
            DSP.WIN.blit(mb_v["txt"], mb_v["tbox"])

    def draw_menu_items(self):
        """ Draw menu items for the selected menu bar, if there is
          one selected.
        Draw the bounding box, then blit each menu item using
          the text surface that matches its current status.
        :attr:
        - mn_id: id of the clicked menu
        """
        for mb_i, mb_v in DSP.MENUS.items():
            if mb_v['selected'] is True:
                pg.draw.rect(DSP.WIN, CLR.CP_GRAY_DARK,
                             DSP.MENUS[mb_i]["ib_box"], 0)
                for mi_k, mi_v in DSP.MENUS[mb_i]["mitems"].items():
                    if mi_v["enabled"]:
                        DSP.WIN.blit(mi_v["txt_enabled"], mi_v["mi_box"])
                    else:
                        DSP.WIN.blit(mi_v["txt_disabled"], mi_v["mi_box"])

    def click_mbar(self,
                   p_mouse_loc: tuple) -> str:
        """
        If clicked, toggle 'selected' attribute of menu.
        And make sure all others are set to 'False'.
        :attr:
        - p_mouse_loc: tuple (number: x, number: y)
        """
        mb_i_clicked = ''
        for mb_i, mb_v in DSP.MENUS.items():
            if mb_v["mb_box"].collidepoint(p_mouse_loc):
                mb_i_clicked = mb_i
                if DSP.MENUS[mb_i]['selected'] is True:
                    DSP.MENUS[mb_i]['selected'] = False
                else:
                    DSP.MENUS[mb_i]['selected'] = True
                for mb_i, mb_v in DSP.MENUS.items():
                    if mb_i != mb_i_clicked:
                        DSP.MENUS[mb_i]['selected'] = False
                break

    def click_mitem(self,
                    p_mouse_loc: tuple) -> tuple:
        """ For currently selected menu:
        - Set all menu items in the list to unselected.
        - See which, if any, menu item was clicked.
        - If an item is now selected, set other items on the list to not
          selected and also set the bar member to not selected.

        :attr:
        - p_mouse_loc: tuple of mouse location
        :return:
        - (str, str) id's of selected/clicked menu and menu item or None
        """
        mb_mi_clicked = ("", "")
        for mn_k, mb_v in DSP.MENUS.items():
            if mb_v['selected'] is True:
                for mi_k, mi_v in mb_v["mitems"].items():
                    DSP.MENUS[mn_k]["mitems"][mi_k]["selected"] = False
                    if mi_v['mi_box'].collidepoint(p_mouse_loc):
                        mb_mi_clicked = (mn_k, mi_k)
                        if DSP.MENUS[mn_k]["mitems"][mi_k]["enabled"]:
                            DSP.MENUS[mn_k]["mitems"][mi_k]["selected"] = True
                        DSP.MENUS[mn_k]["selected"] = False
                        for mi_k, mi_v in mb_v["mitems"].items():
                            if mi_k != mb_mi_clicked[1]:
                                DSP.MENUS[mn_k]["mitems"][mi_k]["selected"] =\
                                    False
                        break
        return mb_mi_clicked

    def set_menus_state(self,
                        mb_k: str,
                        mi_ky: str,
                        p_use_default: bool = False):
        """Set the enabled state of identified menu item and/or
           set the enabled status of dependent menu items.
        Dependent menu items are always in the same menu list as the
           selected menu item.
        :attr:
        - mb_k: str - menu bar key
        - mi_ky: str - menu item key
        - p_use_default: bool - use default enabled value if True

        @TODO:
        - Simplify this. Get rid of it if not being used.
        """
        self.mitems[mb_k][mi_ky]["enabled"] = False
        txt_color = CLR.CP_GRAY
        # Set enabled status of identified item
        if p_use_default:
            if ("default" in list(self.mitems[mb_k][mi_ky].keys()) and
                self.mitems[mb_k][mi_ky]["default"] == "enabled") or\
               "default" not in list(self.mitems[mb_k][mi_ky].keys()):
                self.mitems[mb_k][mi_ky]["enabled"] = True
                txt_color = CLR.CP_BLUEPOWDER
            # Set text color and content of identified item
            self.mitems[mb_k][mi_ky]["mi_text"] =\
                DSP.F_SANS_SM.render(self.mitems[mb_k][mi_ky]["name"],
                                     True, txt_color, CLR.CP_GRAY_DARK)
        else:
            # Default selected item to enabled status
            self.mitems[mb_k][mi_ky]["enabled"] = True
            self.mitems[mb_k][mi_ky]["mi_text"] =\
                DSP.F_SANS_SM.render(self.mitems[mb_k][mi_ky]["name"],
                                     True, CLR.CP_BLUEPOWDER, CLR.CP_GRAY_DARK)
            # Identify dependent menu items and modify their enabled status
            if "disable" in list(self.mitems[mb_k][mi_ky].keys()):
                for dep_ky in self.mitems[mb_k][mi_ky]["disable"]:
                    self.mitems[mb_k][dep_ky]["enabled"] = False
                    self.mitems[mb_k][dep_ky]["mi_text"] =\
                        DSP.F_SANS_SM.render(self.mitems[mb_k][dep_ky]["name"],
                                             True, CLR.CP_GRAY,
                                             CLR.CP_GRAY_DARK)
            if "enable" in list(self.mitems[mb_k][mi_ky].keys()):
                for dep_ky in self.mitems[mb_k][mi_ky]["enable"]:
                    self.mitems[mb_k][dep_ky]["enabled"] = True
                    self.mitems[mb_k][dep_ky]["mi_text"] =\
                        DSP.F_SANS_SM.render(self.mitems[mb_k][dep_ky]["name"],
                                             True, CLR.CP_BLUEPOWDER,
                                             CLR.CP_GRAY_DARK)


class HtmlDisplay(object):
    """Set content for display in external web browser.
    This class is instantiated as a global object named DSP.WHTM.
    Pass in a URI to display in the browser.
    """

    def __init__(self):
        """ Initialize Html Display.
        """
        link_recs = DB.execute_select_all('LINKS')
        pp((link_recs))
        for l_ix, link_id in enumerate(link_recs['link_id']):
            DSP.LINKS[link_id] =\
                {'name': link_recs['link_name'][l_ix],
                 'url': link_recs['link_protocol'][l_ix] +
                 '://' + link_recs['link_value'][l_ix]}
        pp((DSP.LINKS))

    def draw(self,
             p_link_id: str):
        """ Open web browser to display HTML resource.
        It opens subsequent items in the same browser window,
        in new tabs on my setup (Linux Ubuntu, Firefox browser)
        May behave differently on other systems.

        Args: (str) ID for link to display
        """
        webbrowser.open(DSP.LINKS[p_link_id]['url'])


class SetGameData(object):
    """Methods for inserting and updating values on SASKAN.db.
    Initially, just use these from the command line. Eventually,
    intergrate them into the GUI when it is useful.  Try to avoid
    going down a rat-hole of GUI features and functionality, like
    a "magical" editor that generates forms based on DB table
    definitions.  Keep it simple, stupid.  If the command line is
    too tiresome, then use a CSV file or JSON file to load data.

    Simple version:
    Basically just a wrapper for calls to the DataBase() class.
    - pull in a list of values, assume they are in correct order.
    - pull in a dict object, pickle it, and store it in a blob.

    Hmmm...
    Problem here is that this is a PyGame module. There is no CLI
    access as long as the game loop is running. So, I need to
    either define a separate module for data management (yes), or
    create a CLI-like interface in the GUI. The former is easier.
    I have done the latter previously and should be able to find
    some code to support that. But it makes for a more complex
    GUI and not one that most users would be familiar with.

    All of this gets moved to install and other modules.
    Only the GUI code should be in this module and simple, basic
    calls to pull in needed data and data structures.
    """
    def __init__(self):
        """Initialize the SetGameData object.
        It will be instantiated as SGDT, a global object.
        """
        pass

    @classmethod
    def insert_record(cls,
                      p_sql_nm: str,
                      p_values: list,
                      p_object: dict):
        """Insert a record to SASKAN.db.
        """
        DB.execute_insert(p_sql_nm, (p_values, pickle.dumps(p_object)))


class GameData(object):
    """Get and set resources displayed in GAMEMAP and DSP.CONSOLE.
    This class is instantiated as GDAT, a global object.
    Notes:
    - "txt" refers to a string of text.
    - "img" refers to a PyGame image object rendered from txt.
    - "box" refers to a PyGame rectangle object around img.
    @DEV:
    - Layers of data, zoom-in, zoom-out, other views
    - Ee.g.: a region, a town and environs, a village, a scene, star map
    - GUI controls for scroll, zoom, pan, select-move, etc
    - Event trigger conditions / business rules

    - This class is quite large. Let's think about 3 classes:
        - GameData: load data for use in GAMEMAP and DSP.CONSOLE
        - SetConsole: prep data, incl. widget definitions, for DSP.CONSOLE
        - SetGameMap: align data to grid for scaling, zooming
    - And refactor as needed to use io_data and DB structures.
    - Definitely break out into multiple classes.

    @DEV:
    - Nearly all of this will be replaced. Keeping it here now
      for reference. We have data structures and DB tables
      for everything now. Should not need to define so many
      complex data structures in this module.
    """
    def __init__(self):
        """Dynamically loaded data for GAMEMAP and DSP.CONSOLE.
        Values are displayed in DSP.CONSOLE but refer to GAMEMAP.
        For DSP.GRID, static values are read in from PG, then
           data is extended here.
        """
        self.DATASRC = {"actv": False,
                        "catg": None,
                        "item": None}
        self.CONSOLE_REC = {"txt": "",
                            "img": None,
                            "box": None}
        self.CONSOLE_TEXT: list = list()
        self.MAP_BOX = None

    def make_grid_key(self,
                      p_col: int,
                      p_row: int) -> str:
        """Convert integer coordinates to string key
           for use in the .grid["G"] (grid data) matrix.
        :args:
        - p_col: int, column number
        - p_row: int, row number
        :returns:
        - str, key for specific grid-cell record, in "0n_0n" format
        """
        return f"{str(p_col).zfill(2)}_{str(p_row).zfill(2)}"

    # Data load methods
    # The current version of these methods assumes a
    #   specific pattern of name:value pairs in data sources.

    # Modify to read from database and io_data structures instead.
    # =================


    def set_label_name(self,
                       p_attr: dict):
        """Set text for a label (l) and name (n), but no type (t) value.
           Example: "type" attribute
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.DSP.CONSOLE[n]["txt"] (list): strings to render as text
        """
        for t in [DSP.DASH16,
                  f"{p_attr['label']}:",
                  f"  {p_attr['name']}"]:
            rec = copy(self.CONSOLE_REC)
            rec['txt'] = t
            self.CONSOLE_TEXT.append(rec)

    def set_label_name_type(self,
                            p_attr: dict):
        """Set text for a label (l), a name (n), and a type (t).
           Example: "contained_by" attribute
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.DSP.CONSOLE[n]["txt"] (list): strings to render as text
        """
        for t in [DSP.DASH16,
                  f"{p_attr['label']}:",
                  f"  {p_attr['name']}",
                  f"  {p_attr['type']}"]:
            rec = copy(self.CONSOLE_REC)
            rec['txt'] = t
            self.CONSOLE_TEXT.append(rec)

    def set_proper_names(self,
                         p_attr: dict):
        """Set text for a "name" attribute, which refers to proper
            names. Required value is indexed by "common". Optional
            set of names in various game languages or dialects have
            "other" in key.
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.DSP.CONSOLE[n]["txt"] (list): strings to render as text
        """
        for t in [DSP.DASH16,
                  f"{p_attr['label']}:",
                  f"  {p_attr['common']}"]:
            rec = copy(self.CONSOLE_REC)
            rec['txt'] = t
            self.CONSOLE_TEXT.append(rec)
        if "other" in p_attr.keys():
            for k, v in p_attr["other"].items():
                rec = copy(self.CONSOLE_REC)
                rec['txt'] = f"    {k}: {v}"
                self.CONSOLE_TEXT.append(rec)

    def set_map_attr(self,
                     p_attr: dict):
        """Set text for a "map" attribute, referring to game-map data.
           Examples: "distance" or "location" expressed in
              kilometers, degrees, or other in-game measures
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.DSP.CONSOLE[n]["txt"] (list): strings to render as text
        """
        ky = "distance" if "distance" in p_attr.keys() else\
            "location" if "location" in p_attr.keys() else None
        if ky is not None:
            sub_k = ["height", "width"] if ky == "distance" else\
                ["top", "bottom", "left", "right"]
            rec = copy(self.CONSOLE_REC)
            rec['txt'] = DSP.DASH16
            self.CONSOLE_TEXT.append(rec)
            rec = copy(self.CONSOLE_REC)
            rec["txt"] =\
                f"{p_attr[ky]['label']}:"
            self.CONSOLE_TEXT.append(rec)
            for s in sub_k:
                rec = copy(self.CONSOLE_REC)
                rec["txt"] =\
                    f"  {p_attr[ky][s]['label']}:  " +\
                    f"{p_attr[ky][s]['amt']} " +\
                    f"{p_attr[ky]['unit']}"
                self.CONSOLE_TEXT.append(rec)

    def set_contains_attr(self,
                          p_attr: dict):
        """Set text for a "contains" attribute, referring to things
            contained by another object.
            Examples: "sub-region", "movement" (i.e, movement paths)
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.DSP.CONSOLE[n]["txt"] (list): strings to render as text
        """
        rec = copy(self.CONSOLE_REC)
        rec["txt"] = DSP.DASH16
        self.CONSOLE_TEXT.append(rec)
        rec = copy(self.CONSOLE_REC)
        rec["txt"] = f"{p_attr['label']}:"
        self.CONSOLE_TEXT.append(rec)

        if "sub-region" in p_attr.keys():
            rec = copy(self.CONSOLE_REC)
            rec["txt"] =\
                f"  {p_attr['sub-region']['label']}:"
            self.CONSOLE_TEXT.append(rec)
            for n in p_attr["sub-region"]["names"]:
                rec = copy(self.CONSOLE_REC)
                rec["txt"] = f"    {n}"
                self.CONSOLE_TEXT.append(rec)

        if "movement" in p_attr.keys():
            # roads, waterways, rivers and lakes
            rec = copy(self.CONSOLE_REC)
            rec["txt"] = f"  {p_attr['movement']['label']}:"
            self.CONSOLE_TEXT.append(rec)
            attr = {k: v for k, v in p_attr["movement"].items()
                    if k != "label"}
            for _, v in attr.items():
                rec = copy(self.CONSOLE_REC)
                rec["txt"] = f"    {v['label']}:"
                self.CONSOLE_TEXT.append(rec)
                for n in v["names"]:
                    rec = copy(self.CONSOLE_REC)
                    rec["txt"] = f"      {n}"
                    self.CONSOLE_TEXT.append(rec)

    # Data rendering methods for DSP.CONSOLE
    # ==================================
    def render_text_lines(self):
        """
        Store rendering objects for lines of DSP.CONSOLE text.
        After rendering the img from txt, set the box for the img.
        Then adjust topleft of the box according to line number.
        """
        print('render_text_lines()...')

        x = DSP.CONSOLE_TTL_BOX.x
        y = DSP.CONSOLE_TTL_BOX.y + DSP.FONT_MED_SZ

        pp(("self.CONSOLE_TEXT: ", self.CONSOLE_TEXT))

        for ix, val in enumerate(self.CONSOLE_TEXT):
            txt = val["txt"]
            self.CONSOLE_TEXT[ix]["img"] =\
                DSP.F_SANS_TINY.render(txt, True,
                                       CLR.CP_BLUEPOWDER,
                                       CLR.CP_BLACK)
            self.CONSOLE_TEXT[ix]["box"] =\
                self.CONSOLE_TEXT[ix]["img"].get_rect()
            self.CONSOLE_TEXT[ix]["box"].topleft =\
                (x, y + ((DSP.FONT_TINY_SZ + 2) * (ix + 1)))

            pp(("ix: ", ix, "self.CONSOLE_TEXT[ix]: ", self.CONSOLE_TEXT[ix]))

    def set_console_text(self):
        """Format text lines for display in DSP.CONSOLE.
        - "catg" identifies source of config data to format.
        - "item" identifies type of data to format.

        @TODO:
        - Move the geo data, etc. into a database.
        - May want to revisit, optimize the methods for formatting
          different types of data. Maybe even store img and box
          objects in the DB, rather than rendering them here?
            - Nah. This only gets called once per data source, when
              the user clicks on a menu item. No point in persisting to DB.
        - Use config files only for install-level customizations, overrides.
        """
        self.CONSOLE_TEXT.clear()
        # Contents

        pp((self.DATASRC["catg"], self.DATASRC["item"]))

        if self.DATASRC["catg"] == "geo":
            ci = FM.G[self.DATASRC["catg"]][self.DATASRC["item"]]

            pp((ci))

            if "type" in ci.keys():
                self.set_label_name(ci["type"])
            if "contained_by" in ci.keys():
                self.set_label_name_type(ci["contained_by"])
            if "name" in ci.keys():
                self.set_proper_names(ci["name"])
            if "map" in ci.keys():
                self.set_map_attr(ci["map"])
            if "contains" in ci.keys():
                self.set_contains_attr(ci["contains"])
            self.render_text_lines()

    def compute_map_scale(self,
                          p_attr: dict):
        """Compute scaling, position for the map and grid.
        :attr:
        - p_attr (dict): 'map' data for the "Saskan Lands" region from
            the saskan_geo.json file.
        :sets:
        - DSP.GRID['map']: map km dimensions and scaling factors

        - Get km dimensions for entire map rectangle
        - Reject maps that are too big
        - Divide g km by m km to get # of grid-cells for map box
            - This should be a float.
        - Multiply # of grid-cells in the map box by px per grid-cell
          to get line height and width in px for the map box.
        - Center 'map' in the 'grid'; by grid count, by px

        @DEV
        - Debug, refactor to use io_data structures and eventually
            DB structures for dynamic grid/map mapping.
        - Instead of just snapping the "map" as defined here onto
          the GameGrid structure, think about how to pull in map
          data from the database and align it to the grid.
        - Also consider that the grid settings should also be
          pulled in from a database record.
        - Take some time here to get it working.
        """
        err = ""
        map = {'ln': dict(),
               'cl': dict()}
        # Evaluate map line lengths in kilometers
        map['ln']['km'] =\
            {'w': round(int(p_attr["distance"]["width"]["amt"])),
             'h': round(int(p_attr["distance"]["height"]["amt"]))}
        if map['ln']['km']['w'] > DSP.G_LNS_KM_W:
            err = f"Map km w {map['w']} > grid km w {DSP.G_LNS_KM_W}"
        if map['ln']['km']['h'] > DSP.G_LNS_KM_H:
            err = f"Map km h {map['h']} > grid km h {DSP.G_LNS_KM_H}"
        if err != "":
            raise ValueError(err)
        # Verified that the map rect is smaller than the grid rect.
        # Compute a ratio of map to grid.
        # Divide map km w, h by grid km w, h
        map['ln']['ratio'] =\
            {'w': round((map['ln']['km']['w'] / DSP.G_LNS_KM_W), 4),
             'h': round((map['ln']['km']['h'] / DSP.G_LNS_KM_H), 4)}
        # Compute map line dimensions in px
        # Multiply grid line px w, h by map ratio w, h
        map['ln']['px'] =\
            {'w': int(round(DSP.G_LNS_PX_W * map['ln']['ratio']['w'])),
             'h': int(round(DSP.G_LNS_PX_H * map['ln']['ratio']['h']))}
        # The map rect needs to be centered in the grid rect.
        #  Compute the offset of the map rect from the grid rect.
        #  Compute topleft of the map in relation to topleft of the grid.
        #  The map top is offset from grid top by half the px difference
        #  between grid height and map height.
        #  The map left is offset from grid left by half the px difference
        #  between grid width and map width.
        # Then adjusted once more for offset of the grid from the window.
        map['ln']['px']['left'] =\
            int(round((DSP.G_LNS_PX_W - map['ln']['px']['w']) / 2) +
                DSP.GRID_OFFSET_X)
        map['ln']['px']['top'] =\
            int(round((DSP.G_LNS_PX_H - map['ln']['px']['h']) / 2) +
                     (DSP.GRID_OFFSET_Y * 4))  # not sure why, but I need this
        DSP.GRID["map"] = map

    def set_map_grid_collisions(self):
        """ Store collisions between DSP.GRIDS and 'map' box.
        """
        cells = {k: v for k, v in DSP.GRID.items() if k != "map"}
        for ck, crec in cells.items():
            DSP.GRID[ck]["is_inside"] = False
            DSP.GRID[ck]["overlaps"] = False
            if CR.rect_contains(
                    DSP.GRID["map"]["box"], crec["box"]):
                DSP.GRID[ck]["is_inside"] = True
            elif CR.rect_overlaps(
                    DSP.GRID["map"]["box"], crec["box"]):
                DSP.GRID[ck]["overlaps"] = True

    # Set "map" dimensions and other content in DSP.GRIDS
    # =================================================
    def set_gamemap_dims(self,
                         p_attr: dict):
        """This method handles placing/creating/drawing map displays
           over the "grid" on the GAMEMAP display.
        :attr:
        - p_attr (dict): game map name-value pairs from geo config data
            For example, 'map' data for the "Saskan Lands" region from
            the saskan_geo.json file.

        - Compute ratio, offsets of map to g_ width & height.
        - Define saskan rect and pygame box for the map
        - Do collision checks between the map box and grid cells
        """
        self.compute_map_scale(p_attr)
        map_px = DSP.GRID["map"]["ln"]["px"]
        DSP.GRID["map"]["s_rect"] = CR.make_rect(map_px["top"],
                                                 map_px["left"],
                                                 map_px["w"],
                                                 map_px["h"])
        DSP.GRID["map"]["box"] =\
            DSP.GRID["map"]["s_rect"]["pg_rect"]
        self.set_map_grid_collisions()

    def set_map_grid(self):
        """
        Based on currently selected .DATASRC["catg"] and .DATASRC["item"]:
        - assign values to DSP.GRIDS for "map".
        Note:
        - For now, only "geo" data (saskan_geo.json) is handled
        """
        if self.DATASRC["catg"] == "geo":
            data = FM.G[self.DATASRC["catg"]][self.DATASRC["item"]]
            if "map" in data.keys():
                self.set_gamemap_dims(data["map"])


class InfoBar(object):
    """Info Bar object.
    Deafault text is system info.
    Show status text if it is turned on.
    """
    def __init__(self):
        """ Initialize Info Bar. """
        self.info_status = {
            "frozen": True,
            "frame_cnt": 0,
            "mouse_loc": (0, 0),
            "grid_loc": ""}

    def set_ibar_status_text(self):
        """ Set Info Bar status text. """
        self.status_text = (
            "Frame: " + str(self.info_status["frame_cnt"]) +
            "    | Mouse: " + str(self.info_status["mouse_loc"]) +
            "    | Grid: " + str(self.info_status["grid_loc"]))

    def draw(self):
        """ Draw Info Bar.
        Set and draw the Info Bar text.
        Draw the info bar text, optionally including status info.
        """
        text = DSP.PLATFORM + "   | " + self.status_text
        self.itxt = DSP.F_SANS_SM.render(text, True, CLR.CP_BLUEPOWDER,
                                         CLR.CP_BLACK)
        self.ibox = self.itxt.get_rect()
        self.ibox.topleft = DSP.IBAR_LOC
        DSP.WIN.blit(self.itxt, self.ibox)


class GameConsole(object):
    """Draw the Game Console window.
    Display game data like score, map descriptions, etc.
    Instantiated as global object DSP.CONSOLE.

    Note:
    - Objects were rendered, boxed in GDAT and PG classes.
    @DEV:
    - Eventually extend to handle text input fields and/or GUI controls.
    - Keep this distinct from GameData() class, which handles data and
      rendering. Methods will grow more complex to handle game play.
    """

    def __init__(self):
        """ Initialize GameConsole.
        """
        pass

    def draw(self):
        """ Draw DSP.CONSOLE rectange and blit its title text img.
        - Blit txt imgs for current data in CONSOLE_TEXT.
        """
        # Draw container rect and header.
        pg.draw.rect(DSP.WIN, CLR.CP_BLACK, DSP.CONSOLE_BOX, 0)
        DSP.WIN.blit(DSP.CONSOLE_TTL_IMG, DSP.CONSOLE_TTL_BOX)
        # Draw lines of text
        for txt in GDAT.CONSOLE_TEXT:
            DSP.WIN.blit(txt["img"], txt["box"])


class GameMap(object):
    """Define and handle the Game GUI "map" window.
    Draw the grid, the map, and (eventually) scenes, game widgets,
    GUI controls and so on mapped to the grid.

    Instantiated as global object GAMEMAP.

    Note:
    - Objects were rendered, boxed in GDAT and PG classes.
    - Collisions between map and grid cells are id'd in GDAT.
    """

    def __init__(self):
        """Initialize GameMap"""
        pass

    def draw_map(self):
        """Draw "grid" and "map" in GAMEMAP using PG, GDAT objects.
        """
        # Draw grid box with thick border
        pg.draw.rect(DSP.WIN, CLR.CP_SILVER, DSP.GRID_BOX, 5)
        # Draw grid lines      # vt and hz are: ((x1, y1), (x2, y2))
        for vt in DSP.G_LNS_VT:
            pg.draw.aalines(DSP.WIN, CLR.CP_WHITE, False, vt)
        for hz in DSP.G_LNS_HZ:
            pg.draw.aalines(DSP.WIN, CLR.CP_WHITE, False, hz)
        # Highlight grid squares inside or overlapping the map box
        for _, grec in GDAT.DSP.GRIDS.items():
            if "is_inside" in grec.keys() and grec["is_inside"]:
                pg.draw.rect(DSP.WIN, CLR.CP_WHITE, grec["box"], 0)
            elif "overlaps" in grec.keys() and grec["overlaps"]:
                pg.draw.rect(DSP.WIN, CLR.CP_SILVER, grec["box"], 0)
        # Draw map box with thick border
        if GDAT.MAP_BOX is not None:
            pg.draw.rect(DSP.WIN, CLR.CP_PALEPINK, GDAT.MAP_BOX, 5)

    def draw_hover_cell(self,
                        p_grid_loc: str):
        """
        Highlight/colorize grid-cell indicating grid that cursor is
        presently hovering over. When this method is called from
        refesh_screen(), it passes in a DSP.GRID key in p_grid_loc.
        :args:
        - p_grid_loc: (str) Column/Row key of grid to highlight,
            in "0n_0n" (col, row) format, using leading zeros.

        @DEV:
        - Provide options for highlighting in different ways.
        - Pygame colors can use an alpha channel for transparency, but..
            - See: https://stackoverflow.com/questions/6339057/
                    draw-a-transparent-rectangles-and-polygons-in-pygame
            - Transparency is not supported directly by draw()
            - Achieved using Surface alpha argument with blit()
        """
        if p_grid_loc != "":
            pg.draw.rect(DSP.WIN, CLR.CP_PALEPINK,
                         GDAT.DSP.GRIDS[p_grid_loc]["box"], 0)


class TextInput(pg.sprite.Sprite):
    """Define and handle a text input widget.
    Use this to get directions, responses from player
    until I have graphic or voice methods available.
    Expand on this to create GUI control buttons, etc.

    @DEV:
    - Expand the data model and DB to hold widgets:
    - text input
    - buttons
    - text display
    - video display and so on
    """
    def __init__(self,
                 p_x: int,
                 p_y: int,
                 p_w: int = 100,
                 p_h: int = 50):
        """
        Define text input widget.

        :args:
        - p_x: (int) x-coordinate of top left corner
        - p_y: (int) y-coordinate of top left corner
        - p_w: (int) width of text input widget
        - p_h: (int) height of text input widget
        """
        super().__init__()
        self.t_rect = CR.make_rect(p_y, p_x, p_w, p_h)
        self.t_box = self.t_rect["box"]
        self.t_value = ""
        self.t_font = DSP.F_FIXED_LG
        self.t_color = CLR.CP_GREEN
        self.text = self.t_font.render(self.t_value, True, self.t_color)
        self.is_selected = False

    def update_text(self, p_text: str):
        """ Update text value.
        If text is too wide for the widget, truncate it.
        - `self.value` is the current value of the text string.
        - `self.text` is the rendered text surface.
        It will gets refreshed in the `draw` method.

        :args:
        - p_text: (str) Text to render.
        """
        temp_txt = self.t_font.render(p_text, True, self.t_color)
        # shouldn't this be a while loop?...
        if temp_txt.get_rect().width > (self.t_box.w - 10):
            p_text = p_text[:-1]
            temp_txt = self.t_font.render(p_text, True, self.t_color)
        self.t_value = p_text
        self.text = temp_txt

    def clicked(self, p_mouse_loc) -> bool:
        """ Return True if mouse is clicked in the widget.
        """
        if self.t_box.collidepoint(p_mouse_loc):
            self.is_selected = not (self.is_selected)
            return True
        return False

    def draw(self):
        """ Place text in the widget, centered in the box.
        This has the effect of expanding the text as it is typed
        in both directions. Draw the surface (box). Then blit the text.
        """
        self.pos = self.text.get_rect(center=(self.t_box.x + self.t_box.w / 2,
                                              self.t_box.y + self.t_box.h / 2))
        if self.is_selected:
            pg.draw.rect(DSP.WIN, CLR.CP_BLUEPOWDER, self.t_box, 2)
        else:
            pg.draw.rect(DSP.WIN, CLR.CP_BLUE, self.t_box, 2)
        DSP.WIN.blit(self.text, self.pos)


class TextInputGroup(pg.sprite.Group):
    """Define a group object.
    A pygame group is a list of objects.
    This class is helpful for handling multiple input widgets, as in a form.

    Customized from the multiple sprites tracker to track text input widgets.
    The `current` attribute holds the currently-selected textinput widget.
    Conversely, the textinput object itself has an `is_selected` attribute
    that is True if it is the currently-selected one.
    If no textinput object is selected, then `current` is None and no
    textinput object has is_selected == True.

    @DEV:
    - Do I actually use this? How? Where? Example?
    """
    def __init__(self):
        super().__init__()
        self.current = None     # ID currently-selected text input widget.


# ====================================================
#  SASKAN GAME
# ====================================================
class SaskanGame(object):
    """PyGame GUI for controlling Saskantinon game functions.
    Initiated and executed by __main__.
    """
    def __init__(self, *args, **kwargs):
        """
        All major classes are instantiated in the main module
        prior to instantiating the SaskanGame class.
        Execute the main event loop.
        """
        self.MOUSEDOWN = False
        self.MOUSECLICKED = False

        self.main_loop()

    # Core Events
    # ==============================================================
    def exit_appl(self):
        """Exit the app cleanly.
        """
        pg.quit()
        sys.exit()

    def check_exit_appl(self,
                        event: pg.event.Event):
        """Handle exit via keyboard or screen-level exit modes:
        - Q key
        - ESC key
        - `X`ing the app screen.
        :args:
        - event: (pg.event.Event) event to handle

        @TODO:
        - Add call to data cleanup methods if/when needed.
        """
        if (event.type == pg.QUIT or
                (event.type == pg.KEYUP and
                    event.key in DSP.KY_QUIT)):
            self.exit_appl()

    def handle_menu_item_click(self,
                               menu_k: tuple):
        """Trigger an event based on menu item selection.

        :args:
        - menu_k: (tuple) menu bar and menu item keys
        """
        mn_k = menu_k[0]
        mi_k = menu_k[1]
        # mi_nm = MNU.mitems[mb_k][mi_k]["name"]
        if mn_k == "file" and mi_k == "exit":
            self.exit_appl()
        elif mn_k == "help":
            WEB.draw(mi_k)
        """
        elif mi_k == "start":
            GDAT.set_datasrc({"catg": 'geo',
                              "item": 'Saskan Lands',
                              "active": True})
            GDAT.set_console_text()
            GDAT.set_map_grid()
        # elif mi_k == "status":
        #     IBAR.info_status["on"] = not IBAR.info_status["on"]
        elif mi_k == "pause_resume":
            IBAR.info_status["frozen"] = not IBAR.info_status["frozen"]
        """

    # Loop Events
    # ==============================================================
    def track_grid(self):
        """Keep track of what grid mouse is over using DSP.G_LNS_VT,
           DSP.G_LNS_HZ to ID grid loc. May be a little faster than
           parsing thru each element of .grid["G"] matrix.
        Note:
        Since "L" defines lines, it has a count one greater than # of
          grids in each row or column.
        """
        mouse_loc = IBAR.info_status["mouse_loc"]
        IBAR.info_status["grid_loc"] = ""
        grid_col = -1
        # vt ande hz are: (x1, y1), (x2, y2)
        for i in range(0, DSP.GRID_COLS):
            vt = DSP.G_LNS_VT[i]
            if mouse_loc[0] >= vt[0][0] and\
               mouse_loc[0] <= vt[0][0] + DSP.GRID_CELL_PX_W:
                grid_col = i
                break
        grid_row = -1
        for i in range(0, DSP.GRID_ROWS):
            hz = DSP.G_LNS_HZ[i]
            if mouse_loc[1] >= hz[0][1] and\
               mouse_loc[1] <= hz[0][1] + DSP.GRID_CELL_PX_H:
                grid_row = i
                break
        if grid_row > -1 and grid_col > -1:
            IBAR.info_status["grid_loc"] =\
                GDAT.make_grid_key(grid_col, grid_row)

    def track_state(self):
        """Keep track of the state of the app on each frame.

        Sets:
        - mouse_loc: get current mouse location
        - frame_cnt: increment if tracking status and not in a freeze mode
        - cursor: if no text input box is activated, set to default
        """
        IBAR.info_status["mouse_loc"] = pg.mouse.get_pos()
        if IBAR.info_status["frozen"] is False:
            IBAR.info_status["frame_cnt"] += 1
        self.track_grid()

        # For managing text input boxes:
        # if self.TIG.current is None:
        #     pg.mouse.set_cursor(pg.cursors.Cursor())

    def refresh_screen(self):
        """Refresh the screen with the current state of the app.
        30 milliseconds between each frame is the normal framerate.
        To go into slow motion, add a wait here, but don't change
        the framerate.

        Frozen refers only to the game animation and time-based
        event developments. It has no effect on rendering of the
        game, console or info windows except that we stop incrementing
        the frame count, which is handled in track_state().
        """
        DSP.WIN.fill(CLR.CP_BLACK)
        MNU.draw_menu_bar()
        MNU.draw_menu_items()

        """
        # Display info content based on what is currently
        #  posted in the GameData object
        DSP.CONSOLE.draw()

        # Check, Draw info bar
        IBAR.set_ibar_status_text()
        IBAR.draw()

        # Draw the game map
        GAMEMAP.draw_map()
        GAMEMAP.draw_hover_cell(IBAR.info_status["grid_loc"])

        # for txtin in self.TIG:
        #     txtin.draw()
        # self.PAGE.draw()
        """

        pg.display.update()
        DSP.TIMER.tick(30)

    # Main Loop
    # ==============================================================
    def main_loop(self):
        """Manage the event loop.
        - Track the state of the app
        - Check for exit events
        - Handle menu click events
        - Handle text input events
        - Handle other click events
        - Refresh the screen
        """
        while True:
            # self.track_state()

            for event in pg.event.get():

                self.check_exit_appl(event)
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.MOUSEDOWN = True
                    self.MOUSECLICKED = False

                if event.type == pg.MOUSEBUTTONUP:
                    if self.MOUSEDOWN:
                        self.MOUSEDOWN = False
                        self.MOUSECLICKED = True

                if self.MOUSECLICKED:
                    self.MOUSECLICKED = False

                    MNU.click_mbar(pg.mouse.get_pos())
                    item_clicked = MNU.click_mitem(pg.mouse.get_pos())
                    if item_clicked[1] != '':
                        self.handle_menu_item_click(item_clicked)

                    # Handle text input events
                    # Will be mainly on the console window I think
                    # self.do_select_txtin(sIBAR.info_status["mouse_loc"])

                    # Handle game-window click events

            self.refresh_screen()


if __name__ == '__main__':
    """Cache data and resources in memory and launch the app."""
    MNU = GameMenu()
    WEB = HtmlDisplay()  # for Help/Link windows
    # GDAT = GameData()
    # IBAR = InfoBar()
    # DSP.CONSOLE = GameConsole()
    # GAMEMAP = GameMap()
    SaskanGame()
