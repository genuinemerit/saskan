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

import platform
import pygame as pg
import sys
import webbrowser

from dataclasses import dataclass
from pprint import pprint as pp     # noqa: F401, format like pp for files
from pprint import pformat as pf    # noqa: F401, format like pp for files
from pygame.locals import *         # noqa: F401, F403

from app_saskan_gamemap import GameMap, CompareRect
from data_base import DataBase
from data_structs_pg import PygColors, AppDisplay
from data_get import GetData
from method_files import FileMethods    # type: ignore
from method_shell import ShellMethods   # type: ignore

CLR = PygColors()
APD = AppDisplay()
REC = CompareRect()
GAMEMAP = GameMap()

FM = FileMethods()
SM = ShellMethods()

GD = GetData()
DB_CFG = GD.get_db_config()
DB = DataBase(DB_CFG)

pg.init()


@dataclass(frozen=True)
class PG:

    FRM = GD.get_by_id('FRAMES', 'frame_id', 'saskan', DB_CFG)
    pg.display.set_caption(FRM['frame_title'])
    APD.WIN_W = float(FRM['frame_w'])
    APD.WIN_H = float(FRM['frame_h'])
    APD.WIN_MID = (APD.WIN_W / 2, APD.WIN_H / 2)
    flags = pg.RESIZABLE
    APD.WIN = pg.display.set_mode((APD.WIN_W, APD.WIN_H), flags)
    APD.TIMER = pg.time.Clock()
    # In-Memory Global storage objects
    # May eventually want to store as DB BLOBS or JSON,
    # or as permanent or semi-permanent pickeled files.
    # --------------------------------------------------
    MENUS = {}
    LINKS = {}
    INFO = {}
    WINDOWS = {}
    MAPS = {}
    GRIDS = {}


class GameMenu(object):
    """Manage Menu objects. Populate PG.MENUS.
    Define a surface for clickable top-level menu bar members,
    drop-down menus associated with them, and items on each menu.
    Clicking on a menu bar member opens or closes a Menu.
    Clicking on Menu Item triggers an event or sets a status and
      may also close Menu.
    @DEV:
    - Work on relationships between 'Start' and 'Restart'. They
      should be mutually exclusive. Maybe simplify to one item,
      like with Pause/Resume. Also consider calling it 'New Game'
      instead.
    """
    def __init__(self):
        """Initialize the GameMenu object MNU.
        Store menu data and rendering info in PG.MENUS.
        """
        self.set_menu_bars()
        self.set_menu_items()
        self.draw_menu_bar()
        self.draw_menu_items()

    def set_menu_bars(self) -> dict:
        """
        - Set up menu bars and menus names in PG.MENUS.
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
            PG.MENUS =\
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
            for m_ix, m_id in enumerate(list(PG.MENUS.keys())):
                PG.MENUS[m_id]['txt'] = APD.F_SANS_SM.render(
                    PG.MENUS[m_id]['name'],
                    True, CLR.CP_BLUEPOWDER, CLR.CP_GRAY_DARK)
                tbox = PG.MENUS[m_id]['txt'].get_rect()
                mb_box = pg.Rect(tbox)
                mb_box.x = x
                mb_box.y = mbar_rec['mbar_y']
                mb_box.h = mbar_rec['mbar_h'] * 1.5
                mb_box.w *= 1.5
                PG.MENUS[m_id]['mb_box'] = mb_box
                tbox.center = mb_box.center
                PG.MENUS[m_id]['tbox'] = tbox
                x += mb_box.width

        # ====== set_menu_bars method ======
        mbar_rec = get_menu_bar_data()
        set_menu_bar_rendering(mbar_rec)

    def set_menu_items(self):
        """
        - Get menu item datea from DB and put into PG.MENUS.
        - Compute rendering info for menu items.
        - mi_box: pg rect around tbox + margin for each item
        """
        def get_menu_item_data():
            """Retrieve menu iitem data from data base."""
            for menu_id, mnu in PG.MENUS.items():
                mitm_recs =\
                    GD.get_by_id('MENU_ITEMS', 'menu_uid_fk',
                                 mnu['uid'], DB_CFG, p_first_only=False)
                for mi in mitm_recs:
                    id = mi['item_id']
                    PG.MENUS[menu_id]['mitems'][id]: dict = {
                        "order": mi['item_order'],
                        "name": mi['item_name'],
                        "key_binding": mi['key_binding'],
                        "enabled": mi['enabled_default'],
                        'txt_enabled': None,
                        'txt_disabled': None,
                        'mi_box': None,
                        'uid': mi['item_uid_pk']}
                PG.MENUS[menu_id]['mitems'] =\
                    SM.convert_dict_to_ordered_dict(
                        PG.MENUS[menu_id]['mitems'])

        def set_menu_item_rendering():
            """Compute rendering boxes for menu items."""
            for mn_id, menu in PG.MENUS.items():
                for mi_id, m_item in menu['mitems'].items():
                    item_k = PG.MENUS[mn_id]['mitems'][mi_id]
                    item_k['txt_enabled'] = APD.F_SANS_SM.render(
                        m_item['name'], True, CLR.CP_BLUEPOWDER,
                        CLR.CP_GRAY_DARK)
                    item_k['txt_disabled'] = APD.F_SANS_SM.render(
                        m_item['name'], True, CLR.CP_BLUEPOWDER,
                        CLR.CP_GRAY_DARK)
                    tbox = item_k['txt_enabled'].get_rect()
                    mi_box = pg.Rect(tbox)
                    mi_box.x = PG.MENUS[mn_id]['mb_box'].left
                    mi_box.h = tbox.h * 1.5
                    mi_box.w = tbox.w * 1.5
                    mi_box.y = PG.MENUS[mn_id]['mb_box'].bottom + 12 +\
                        (mi_box.h * m_item['order'])
                    item_k['mi_box'] = mi_box
                    tbox.x += 12
                    item_k['tbox'] = tbox

        def set_menu_items_bounding_box():
            """Compute bounding box for menu items.
            It should be as wide as the widest menu item and
            and tall as the total height of all items."""
            pass
            for mn_id, menu in PG.MENUS.items():
                widest_w = 0.0
                total_h = 0.0
                for mi_id, m_item in menu['mitems'].items():
                    widest_w = max(widest_w, m_item['mi_box'].width)
                    total_h += m_item['mi_box'].height
                PG.MENUS[mn_id]['ib_box'] = pg.Rect(
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
        for mb_i, mb_v in PG.MENUS.items():
            box_color = CLR.CP_BLUEPOWDER if mb_v['selected'] is False\
                else CLR.CP_GREEN
            pg.draw.rect(APD.WIN, box_color, mb_v['mb_box'], width=2)
            APD.WIN.blit(mb_v["txt"], mb_v["tbox"])

    def draw_menu_items(self):
        """ Draw menu items for the selected menu bar, if there is
          one selected.
        Draw the bounding box, then blit each menu item using
          the text surface that matches its current status.
        :attr:
        - mn_id: id of the clicked menu
        """
        for mb_i, mb_v in PG.MENUS.items():
            if mb_v['selected'] is True:
                pg.draw.rect(APD.WIN, CLR.CP_GRAY_DARK,
                             PG.MENUS[mb_i]["ib_box"], 0)
                for mi_k, mi_v in PG.MENUS[mb_i]["mitems"].items():
                    if mi_v["enabled"]:
                        APD.WIN.blit(mi_v["txt_enabled"], mi_v["mi_box"])
                    else:
                        APD.WIN.blit(mi_v["txt_disabled"], mi_v["mi_box"])

    def click_mbar(self,
                   p_mouse_loc: tuple) -> str:
        """
        If clicked, toggle 'selected' attribute of menu.
        And make sure all others are set to 'False'.
        :attr:
        - p_mouse_loc: tuple (number: x, number: y)
        """
        mb_i_clicked = ''
        for mb_i, mb_v in PG.MENUS.items():
            if mb_v["mb_box"].collidepoint(p_mouse_loc):
                mb_i_clicked = mb_i
                if PG.MENUS[mb_i]['selected'] is True:
                    PG.MENUS[mb_i]['selected'] = False
                else:
                    PG.MENUS[mb_i]['selected'] = True
                for mb_i, mb_v in PG.MENUS.items():
                    if mb_i != mb_i_clicked:
                        PG.MENUS[mb_i]['selected'] = False
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
        for mn_k, mb_v in PG.MENUS.items():
            if mb_v['selected'] is True:
                for mi_k, mi_v in mb_v["mitems"].items():
                    PG.MENUS[mn_k]["mitems"][mi_k]["selected"] = False
                    if mi_v['mi_box'].collidepoint(p_mouse_loc):
                        mb_mi_clicked = (mn_k, mi_k)
                        if PG.MENUS[mn_k]["mitems"][mi_k]["enabled"]:
                            PG.MENUS[mn_k]["mitems"][mi_k]["selected"] = True
                        PG.MENUS[mn_k]["selected"] = False
                        for mi_k, mi_v in mb_v["mitems"].items():
                            if mi_k != mb_mi_clicked[1]:
                                PG.MENUS[mn_k]["mitems"][mi_k]["selected"] =\
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
                APD.F_SANS_SM.render(self.mitems[mb_k][mi_ky]["name"],
                                     True, txt_color, CLR.CP_GRAY_DARK)
        else:
            # Default selected item to enabled status
            self.mitems[mb_k][mi_ky]["enabled"] = True
            self.mitems[mb_k][mi_ky]["mi_text"] =\
                APD.F_SANS_SM.render(self.mitems[mb_k][mi_ky]["name"],
                                     True, CLR.CP_BLUEPOWDER, CLR.CP_GRAY_DARK)
            # Identify dependent menu items and modify their enabled status
            if "disable" in list(self.mitems[mb_k][mi_ky].keys()):
                for dep_ky in self.mitems[mb_k][mi_ky]["disable"]:
                    self.mitems[mb_k][dep_ky]["enabled"] = False
                    self.mitems[mb_k][dep_ky]["mi_text"] =\
                        APD.F_SANS_SM.render(self.mitems[mb_k][dep_ky]["name"],
                                             True, CLR.CP_GRAY,
                                             CLR.CP_GRAY_DARK)
            if "enable" in list(self.mitems[mb_k][mi_ky].keys()):
                for dep_ky in self.mitems[mb_k][mi_ky]["enable"]:
                    self.mitems[mb_k][dep_ky]["enabled"] = True
                    self.mitems[mb_k][dep_ky]["mi_text"] =\
                        APD.F_SANS_SM.render(self.mitems[mb_k][dep_ky]["name"],
                                             True, CLR.CP_BLUEPOWDER,
                                             CLR.CP_GRAY_DARK)


class HtmlDisplay(object):
    """Set content for display in external web browser.
    This class is instantiated as a global object named APD.WHTM.
    Pass in a URI to display in the browser.
    """

    def __init__(self):
        """ Initialize Html Display.
        """
        link_recs = DB.execute_select_all('LINKS')
        for l_ix, link_id in enumerate(link_recs['link_id']):
            PG.LINKS[link_id] =\
                {'name': link_recs['link_name'][l_ix],
                 'url': link_recs['link_protocol'][l_ix] +
                 '://' + link_recs['link_value'][l_ix]}

    def draw(self,
             p_link_id: str):
        """ Open web browser to display HTML resource.
        It opens subsequent items in the same browser window,
        in new tabs on my setup (Linux Ubuntu, Firefox browser)
        May behave differently on other systems.

        Args: (str) ID for link to display
        """
        webbrowser.open(PG.LINKS[p_link_id]['url'])


class InfoBar(object):
    """Info Bar object.  Deafault text is system info.
    Show status text if it is turned on.
    """
    def __init__(self):
        """ Initialize Info Bar.
        @DEV
        - Instead of hardcoding ibar_x and ibar_y, compute them
          based on FRM dimeensions.
        - Then do the same for gamemap and console.
        """
        PG.INFO = {
            "frozen": True,
            "frame_cnt": 0,
            "mouse_loc": (0, 0),
            "grid_loc": "",
            "content": ['', ''],
            "txt": [None, None],
            "if_box": [None, None]}
        line = (f"Platform: {platform.platform()}" +
                f"  |  Python: {platform.python_version()}" +
                f"  |  Pygame: {pg.version.ver}")
        PG.INFO['content'][0] = line
        PG.INFO['txt'][0] = (APD.F_SANS_SM.render(
            PG.INFO['content'][0], True, CLR.CP_BLUEPOWDER, CLR.CP_BLACK))
        PG.INFO['if_box'][0] = PG.INFO['txt'][0].get_rect()
        PG.INFO['if_box'][0].x = 60
        PG.INFO['if_box'][0].y = PG.FRM['frame_h'] - 120

    def draw_info_bar(self):
        """ Set Info Bar rendering and draw it.
        """
        line = (f"Frame: {PG.INFO['frame_cnt']}" +
                f"  |  Mouse: {PG.INFO['mouse_loc']}" +
                f"  |  Grid: {PG.INFO['grid_loc']}")
        PG.INFO['content'][1] = line
        PG.INFO['txt'][1] = (APD.F_SANS_SM.render(
            PG.INFO['content'][1], True, CLR.CP_BLUEPOWDER, CLR.CP_BLACK))
        PG.INFO['if_box'][1] = PG.INFO['txt'][1].get_rect()
        PG.INFO['if_box'][1].x = 60
        PG.INFO['if_box'][1].y = PG.INFO['if_box'][0].bottom + 6
        for i in (0, 1):
            APD.WIN.blit(PG.INFO['txt'][i], PG.INFO['if_box'][i])


class Windows(object):
    """Manage set-up and drawing of windows inside the screen.
    - Console window
    - Map window
    """
    def __init__(self):
        """ Initialize Windows."""
        self.set_window_dims()
        self.draw_windows()

    def set_window_dims(self):
        """Get window specs from database.
        Save in PG.WINDOWS.
        Next:
        - Compute location of window content.
        @DEV:
        - Consider using config to identify relative
          size and location of windows
        """
        def compute_wbox():
            """Compute window content ('wbox') size and location"""
            y = PG.MENUS[list(PG.MENUS.keys())[0]]['mb_box'].bottom + 120
            h = PG.INFO['if_box'][0].top - y - 60
            if win_id == 'gamemap':
                w = (APD.WIN_W * 0.70) + (2 * w_v["win_margin"])
                x = PG.MENUS[list(PG.MENUS.keys())[0]]['mb_box'].left
            elif win_id == 'console':
                w = (APD.WIN_W * 0.25) + (2 * w_v["win_margin"])
                x = APD.WIN_W - w - (2 * w_v["win_margin"])
            PG.WINDOWS[win_id]["w_box"] = pg.Rect(x, y, w, h)

        def compute_tbox():
            """Compute window title box ('tbox') size and location"""
            PG.WINDOWS[win_id]["txt"] =\
                APD.F_SANS_SM.render(
                    PG.WINDOWS[win_id]['title'],
                    True, CLR.CP_BLUEPOWDER, CLR.CP_GRAY_DARK)
            tbox = PG.WINDOWS[win_id]["txt"].get_rect()
            tbox = pg.Rect(tbox)
            tbox.center = PG.WINDOWS[win_id]["w_box"].center
            tbox.top = PG.WINDOWS[win_id]["w_box"].top - 60
            tbox.left = PG.WINDOWS[win_id]["w_box"].left
            PG.WINDOWS[win_id]["t_box"] = tbox

        win_recs = GD.get_by_id(
            'WINDOWS', 'frame_uid_fk',
            PG.FRM['frame_uid_pk'], DB_CFG,
            p_first_only=False)
        for w_v in win_recs:
            win_id = w_v["win_id"]
            PG.WINDOWS[win_id] =\
                {"uid": w_v["win_uid_pk"],
                 "title": w_v["win_title"],
                 "title_txt": w_v["win_title"],
                 "margin": w_v["win_margin"],
                 'w_box': None,
                 't_box': None}
            compute_wbox()
            compute_tbox()

    def draw_windows(self):
        """Draw the map and console windows.
        Next: also draw the window title.
        """
        for win_id, w_v in PG.WINDOWS.items():
            pg.draw.rect(APD.WIN, CLR.CP_GRAY_DARK,
                         w_v["w_box"], 6)
            APD.WIN.blit(w_v["txt"], w_v["t_box"])


class SaveGameData(object):
    """Methods for inserting and updating values on SASKAN.db.

    Replace this with writes/updates to the Database, most likely
    via calls to data_set.py mondule
    """
    def __init__(self):
        """Initialize the SaveGameData object.
        It will be instantiated as SGDT, a global object.
        """
        pass


class Stage(object):
    """Get resources used in the game/story windows to
       set the stage: maps, grids, related 'story' items describing
       places and settings. Define GUI structures for gamemap and console
       windows. The console window may eventually be replaced with some
       widget collections. Just putting them all in there for now.
    @DEV:
    - Selecting different MAP, GRID combinations.
    - Layers of data, zoom-in, zoom-out, other views
    - Ee.g.: a region, a town and environs, a village, a scene, star map
    - GUI controls for scroll, zoom, pan, select-move, etc
    - Event trigger conditions / business rules
    - Consider what additional menu items and/or widgets will help
       with selecting what MAP, GRID and other story-related items, as
       well as scrolling, zooming, panning, etc.
       - Selecting a map.
       - Zooming in/out.
       - Panning.
       - For "CONSOLE" start to think more in terms of "story" and "game"
         events that are triggered by the user and less about info-display.
         Ideally, most info is visible on the gameamp itself. Console would
         have buttons to select what info to display/overlay.
    - Eventually layer on classes for ACTOR, SCENE and PROP.
    """
    def __init__(self):
        """Create STG object."""
        pass

    def set_map(self,
                p_map_name: str = "Saskan Lands Regions"):
        """
        - Get requested MAP record(s) from the DB.
        - Store in MAPS
        - Get GRIDxMAP records for the MAP(s).
        - Get associated GRID records.
        - Store in GRIDS
        Default (for prototyping) is to load:
        - MAP: 'Saskan Lands Regions'
        - GRID: '30r_40c'
        @TODO:
        - Set up rendering for the MAP+GRID items:
            - For gamemap grid and contents
            - For console widgets
        """
        if p_map_name not in list(PG.MAPS.keys()):
            self.get_2d_map_data(p_map_name)
            self.get_2d_grid_data(p_map_name)
            PG.GRIDS = GAMEMAP.create_gamemap(
                PG.WINDOWS, PG.MAPS, PG.GRIDS)
            pp((PG.WINDOWS, PG.GRIDS))
        else:
            print("MAP and GRID data already loaded for", p_map_name)

    def get_2d_map_data(self,
                        p_map_name):
        """Retrieve MAP data from data base for specified name.
        """
        map_rec = GD.get_by_id(
            'MAP', 'map_name', 'Saskan Lands Regions', DB_CFG)
        grid_x_map_recs = GD.get_by_id(
            'GRID_X_MAP', 'map_uid_fk',
            map_rec['map_uid_pk'], DB_CFG, p_first_only=False)
        PG.MAPS =\
            {map_rec['map_name']:
                {'map_type': map_rec['map_type'],
                 'map_uid': map_rec['map_uid_pk'],
                 'units': map_rec['unit_of_measure'],
                 'dg_lat_top_left': map_rec['origin_2d_lat'],
                 'dg_lon_top_left': map_rec['origin_2d_lon'],
                 'width_e_w': map_rec['width_e_w_2d'],
                 'height_n_s': map_rec['height_n_s_2d'],
                 'avg_alt_m': map_rec['avg_alt_m'],
                 'min_alt_m': map_rec['min_alt_m'],
                 'max_alt_m': map_rec['max_alt_m'],
                 'grid_uids': [g['grid_uid_fk'] for g in grid_x_map_recs]}}

    def get_2d_grid_data(self,
                         p_map_name):
        """Retrieve GRID data from data base for all GRIDs associated
           with specified MAP.
        """
        grid_recs: list = []
        for grid_uid in PG.MAPS[p_map_name]['grid_uids']:
            g_recs = GD.get_by_id(
                'GRID', 'grid_uid_pk', grid_uid, DB_CFG,
                p_first_only=False)
            [grid_recs.append(rec) for rec in g_recs]
        PG.GRIDS =\
            {g['grid_name']:
                {'grid_uid': g['grid_uid_pk'],
                 'map_NAME': p_map_name,
                 'row_cnt': g['row_cnt'],
                 'col_cnt': g['col_cnt']}
                for g in grid_recs}

    def draw_gamemap(self,
                     p_grid_name: str = None):
        """Use modified PG.GRIDS data to draw the gamemap grid.
        Use PG.MAPS to layer information over the grid.
        Use whatever "story" related data to populate widgets and
         overlay to the map.
        If p_grid_name is None, default to first grid in PG.GRIDS.
        """
        p_grid_name = p_grid_name or list(PG.GRIDS.keys())[0]
        # Draw the grid.
        for (p1, p2) in PG.GRIDS[p_grid_name]['h_lines']:
            pg.draw.aaline(APD.WIN, CLR.CP_WHITE, p1, p2)
        for (p1, p2) in PG.GRIDS[p_grid_name]['v_lines']:
            pg.draw.aaline(APD.WIN, CLR.CP_WHITE, p1, p2)
        # Draw the reference numbers in the 0th row, the
        # nth row; in the 0th col and the nth col.
        # Too much math. Let's try this again. This time,
        # let's build out the collection of cells, as in the
        # previous prototype. Each cell will have a complete
        # set of coordinates, a reference number, and type
        # code indicating if the cell is on a reference row (0, n)
        # or column (0, n).
        # Instead of trying to compute the offsets here, we will
        # just plonk the 'tbox' in the center of the cell.


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
        - Q key, ESC key, `X`ing the app screen.
        :args:
        - event: (pg.event.Event) event to handle
        """
        if (event.type == pg.QUIT or
                (event.type == pg.KEYUP and
                    event.key in APD.KY_QUIT)):
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
        elif mn_k == "game":
            if mi_k == "start":
                STG.set_map()
                PG.INFO["frozen"] = False
            if mi_k == "pause_resume":
                PG.INFO["frozen"] = not PG.INFO["frozen"]
        """
        # elif mi_k == "status":
        # elif mi_k == "save":
        # elif mi_k == "test":
        """

    # Loop Events
    # ==============================================================
    def track_grid(self):
        """Keep track of what grid mouse is over using APD.G_LNS_VT,
           APD.G_LNS_HZ to ID grid loc. May be a little faster than
           parsing thru each element of .grid["G"] matrix.
        Note:
        Since "L" defines lines, it has a count one greater than # of
          grids in each row or column.
        """
        mouse_loc = IBAR.info_status["mouse_loc"]
        IBAR.info_status["grid_loc"] = ""
        grid_col = -1
        # vt ande hz are: (x1, y1), (x2, y2)
        for i in range(0, APD.GRID_COLS):
            vt = APD.G_LNS_VT[i]
            if mouse_loc[0] >= vt[0][0] and\
               mouse_loc[0] <= vt[0][0] + APD.GRID_CELL_PX_W:
                grid_col = i
                break
        grid_row = -1
        for i in range(0, APD.GRID_ROWS):
            hz = APD.G_LNS_HZ[i]
            if mouse_loc[1] >= hz[0][1] and\
               mouse_loc[1] <= hz[0][1] + APD.GRID_CELL_PX_H:
                grid_row = i
                break
        if grid_row > -1 and grid_col > -1:
            IBAR.info_status["grid_loc"] =\
                STG.make_grid_key(grid_col, grid_row)

    def refresh_screen(self):
        """Refresh the screen with the current state of the app.
        30 milliseconds between each frame is the normal framerate.
        To go into slow motion, add a wait here, but don't change
        the framerate.
        """
        PG.INFO["mouse_loc"] = pg.mouse.get_pos()
        if not PG.INFO["frozen"]:
            PG.INFO["frame_cnt"] += 1
        APD.WIN.fill(CLR.CP_BLACK)
        WINS.draw_windows()
        IBAR.draw_info_bar()
        MNU.draw_menu_items()
        if len(PG.GRIDS.keys()) > 0:
            STG.draw_gamemap()
        MNU.draw_menu_bar()

        """
        # Display info content based on what is currently
        #  posted in the Stage object
        APD.CONSOLE.draw()

        # Draw the game map
        GAMEMAP.draw_map()
        GAMEMAP.draw_hover_cell(IBAR.info_status["grid_loc"])

        # for txtin in self.TIG:
        #     txtin.draw()
        # self.PAGE.draw()
        """
        pg.display.update()
        APD.TIMER.tick(30)

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

                    # Handle console/widget events
                    # Handle text input events
                    # Will be mainly on the console window I think
                    # Thinkg of text inputs as WIDGETs.
                    # May want to add some buttons, other snazzy things.

                    # Handle game-map click events

            self.refresh_screen()


if __name__ == '__main__':
    """Cache data and resources in memory and launch the app."""

    # Classes used to manage the game
    # -------------------------------
    MNU = GameMenu()
    WEB = HtmlDisplay()  # for Help/Link windows
    IBAR = InfoBar()
    WINS = Windows()
    STG = Stage()
    SaskanGame()
