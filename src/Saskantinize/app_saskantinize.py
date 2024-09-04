#!python
"""
:module:    app_saskantinize.py
:author:    GM (genuinemerit @ pm.me)

Saskanantinize App GUI.  pygame/sqlite version.
Saskantinize is the admin controller and manager app
for Saskantinon.

@DEV:
- All config data is moved to the DB by the time we use
  this module. Need to set up config data for the 'Admin' app:
  Frames, Menus, etc. on the DB. This is done using data_set.py
  which reads config data files and writes it to the DB.
- That, in turn, is executed (currently) by install_saskan.py,
  which presently reads in data only for 'saskan' and not
  'admin'.
- Need to decide if saskan and admin will always be installed
  together. I think yes is the right answer, ultimately, tho
  it will nice if I can set up the Makefile to be able to work
  on one or the other, or both, at a time.
- In any case, the underlying code, like data_set is the same
  for saskan and admin. Avoid duplicating code. Just pass in
  a parameter to indicate which app is being installed.
- Also consider creating yet another app speicifically to
  handle the install and set-up tasks. This is separate from
  either Saskantinize or Saskantinon.
- It may also be worthwhile to treat backend and some middleware
  as separate apps. This will allow for more flexibility in
  future, especially at the data level.
- See if basic set up of menus and windows can be genericized
  between Saskanantinon and Saskantinize. If the only difference
  is the name of the config data to read in, there is no point
  in duplicating the code.
- Add interactive functions calling the Analysis class.
- Add functions to modify parameters for Analysis graphs, reports.
- Work on better ways of displaying graphs.
- Work on better ways of displaying reports.
"""

import platform
import sys
import webbrowser
from dataclasses import dataclass
from pprint import pformat as pf  # noqa: F401, format like pp for files
from pprint import pprint as pp  # noqa: F401, format like pp for files

import pygame as pg
import Saskantinon.data_structs as DS  # noqa: F401
import Saskantinon.data_structs_pg as DSP  # noqa: F401

from Saskantinon.data_base import DataBase  # noqa: F401
from Saskantinon.data_get import GetData    # noqa: F401
from Saskantinon.method_files import FileMethods  # noqa: F401
from Saskantinon.method_shell import ShellMethods  # noqa: F401

CLR = DSP.PygColors()
APD = DSP.AppDisplay()
FM = FileMethods()
GD = GetData()
DB_CFG = GD.get_db_config()
DB = DataBase(DB_CFG)

pg.init()


@dataclass(frozen=True)
class PG:

    FRM = GD.get_by_id("FRAMES", "frame_id", "admin", DB_CFG)
    pg.display.set_caption(FRM["frame_title"])
    APD.WIN_W = float(FRM["frame_w"])
    APD.WIN_H = float(FRM["frame_h"])
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


class AdminMenu(object):
    """Manage Menu objects. Populate PG.MENUS.
    Define a surface for clickable top-level menu bar members,
    drop-down menus associated with them, and items on each menu.
    Clicking on a menu bar member opens or closes a Menu.
    Clicking on Menu Item triggers an event or sets a status and
      may also close Menu.
    @DEV:
    - Distinguish between 'ssakan' and 'admin' menus.
    """

    def __init__(self):
        """Initialize the AdminMenu object MNU.
        Store menu data and rendering info in PG.MENUS.
        """
        self.set_menu_bars()
        # self.set_menu_items()
        # self.draw_menu_bar()
        # self.draw_menu_items()

    def set_menu_bars(self) -> dict:
        """
        - Set up menu bars and menus names in PG.MENUS.
        - Compute rendering info for menu bar members.
          Center menu text; align spacing to text width.
        """

        def get_menu_bar_data():
            """Retrieve menu bar and menu data from data base."""
            mbar_rec = GD.get_by_id(
                "MENU_BARS", "frame_uid_fk", PG.FRM["frame_uid_pk"], DB_CFG
            )
            menu_rec = GD.get_by_id(
                "MENUS",
                "menu_bar_uid_fk",
                mbar_rec["menu_bar_uid_pk"],
                DB_CFG,
                p_first_only=False,
            )
            PG.MENUS = {
                m["menu_id"]: {
                    "name": m["menu_name"],
                    "uid": m["menu_uid_pk"],
                    "selected": False,
                    "txt": "",
                    "tbox": None,
                    "mb_box": None,
                    "ib_box": None,
                    "mitems": {},
                }
                for m in menu_rec
            }
            return mbar_rec

        def set_menu_bar_rendering(mbar_rec: dict):
            """Computer rendering boxes for menu bar.
            The mb_box is the box around the text. It gets renedered as a rect.
            The tbox defines the destination rec in a blit() command, so it is
              to be defined to be centered inside the mb_box.
            The txt is the surface for the blit() command.
            """
            x = mbar_rec["mbar_x"]
            for m_ix, m_id in enumerate(list(PG.MENUS.keys())):
                PG.MENUS[m_id]["txt"] = APD.F_SANS_SM.render(
                    PG.MENUS[m_id]["name"], True, CLR.CP_BLUEPOWDER, CLR.CP_GRAY_DARK
                )
                tbox = PG.MENUS[m_id]["txt"].get_rect()
                mb_box = pg.Rect(tbox)
                mb_box.x = x
                mb_box.y = mbar_rec["mbar_y"]
                mb_box.h = mbar_rec["mbar_h"] * 1.5
                mb_box.w *= 1.5
                PG.MENUS[m_id]["mb_box"] = mb_box
                tbox.center = mb_box.center
                PG.MENUS[m_id]["tbox"] = tbox
                x += mb_box.width

        # ====== set_menu_bars method ======
        mbar_rec = get_menu_bar_data()
        set_menu_bar_rendering(mbar_rec)


class MenuBar(object):
    """Menu Bar items for the application.
    Define a surface for a clickable top-level menu bar item.
    Clicking on a menu bar item opens or closes a MenuItems.
    """

    def __init__(self, p_name: str, p_x_left: int):
        """Initialize a Menu Bar object.
        = `text` is text content and UID for the menu bar item.
        - `mbox` is the bounding box for the menu bar item.
        - 'mtxt` is the image (surface) for rendering text.
        - 'tbox` is the bounding box for the text.

        :args:
        - p_name (str): text and UID for menu bar item.
        - p_x_left (int): x location for menu bar box.
        """
        self.is_selected = False
        self.text = p_name
        mbox_w = len(self.text) * 12
        self.mbox = pg.Rect(p_x_left, PG.MBAR_Y, mbox_w, PG.MBAR_H)
        self.mtxt = PG.F_SANS_12.render(
            self.text, True, CLR.CP_BLUEPOWDER, CLR.CP_BLACK
        )
        self.tbox = self.mtxt.get_rect()
        self.tbox.topleft = (
            p_x_left + int((self.mbox.width - self.tbox.width) / 2),
            PG.MBAR_Y + PG.MBAR_MARGIN,
        )

    def draw(self):
        """Draw a Menu Bar item."""
        if self.is_selected:
            pg.draw.rect(PG.WIN, CLR.CP_BLUEPOWDER, self.mbox, 2)
        else:
            pg.draw.rect(PG.WIN, CLR.CP_BLUE, self.mbox, 2)
        PG.WIN.blit(self.mtxt, self.tbox)

    def clicked(self, p_mouse_loc) -> bool:
        """Return True if mouse clicked on the mbox."""
        if self.mbox.collidepoint(p_mouse_loc):
            return True
        return False


class MenuItems(object):
    """Define one or more MenuItem associated with a MenuBar.
    Clicking on a menu bar item triggers a function and sets
    visibility of the MenuItems to False.
    """

    def __init__(self, p_mitm_list: list, p_mbar: MenuBar):
        """Initialize Menu Items.
        The container (mbox) surface holds all the items.
        Each MenuItem is clickable, per its bounding box (tbox).

        :args:
        - p_mitm_list (list): list of menu item names.
        - p_mbar (MenuBar): the parent MenuBar object

        Rect = (left, top, width, height)
        """
        self.name = p_mbar.text
        self.is_visible = False
        self.item_cnt = len(p_mitm_list)
        # Protoype of box to draw around  menu items.
        self.mbox = pg.Rect(
            p_mbar.mbox.left, p_mbar.mbox.bottom, 0, p_mbar.mbox.height * self.item_cnt
        )
        self.mitems = []
        for mx, mi in enumerate(p_mitm_list):
            mi_id = mi[0]
            mi_nm = mi[1]
            mtxt = PG.F_SANS_12.render(mi_nm, True, CLR.CP_BLUEPOWDER, CLR.CP_BLACK)
            mitm_w = mtxt.get_width() + (PG.MBAR_MARGIN * 2)
            # Box for each item in the menu item list.
            tbox = pg.Rect(
                self.mbox.left + PG.MBAR_MARGIN,
                ((self.mbox.top + (PG.MBAR_H * mx)) + PG.MBAR_MARGIN),
                mitm_w,
                PG.MBAR_H,
            )
            # Set mbox width equal to largest tbox width
            if tbox.width > self.mbox.width:
                self.mbox.width = tbox.width
            self.mitems.append({"id": mi_id, "mtxt": mtxt, "tbox": tbox, "text": mi_nm})

    def draw(self):
        """Draw the list of Menu Items."""
        if self.is_visible:
            pg.draw.rect(PG.WIN, CLR.CP_BLUEPOWDER, self.mbox, 2)
            for mi in self.mitems:
                PG.WIN.blit(mi["mtxt"], mi["tbox"])

    def clicked(self, p_mouse_loc):
        """Return id and name of clicked menu item or None."""
        for mi in self.mitems:
            if mi["tbox"].collidepoint(p_mouse_loc):
                return (mi["id"], mi["text"])
        return None


class MenuGroup(object):
    """Define a group object for menu bars and menu items.
    Reference menus by name and associate menu bar with its items.
    """

    def __init__(self):
        self.mbars: dict = dict()
        self.mitems: dict = dict()
        self.current_bar = None
        self.current_item = None

    def add_bar(self, p_mbar: MenuBar):
        """Add a MenuBar to the collection."""
        self.mbars[p_mbar.text] = p_mbar

    def add_item(self, p_mitems: MenuItems):
        """Add a MenuItems to the collection."""
        self.mitems[p_mitems.name] = p_mitems


class PageHeader(object):
    """Set text for header.
    HDR is a widget drawn at top of the window.
    """

    def __init__(self, p_hdr_text: str):
        """Initialize PageHeader."""
        self.img = PG.F_SANS_18.render(
            p_hdr_text, True, CLR.CP_BLUEPOWDER, CLR.CP_BLACK
        )
        self.box = self.img.get_rect()
        self.box.topleft = PG.PHDR_LOC

    def draw(self):
        """Draw PageHeader."""
        PG.WIN.blit(self.img, self.box)


class HtmlDisplay(object):
    """Set content for display in external web browser."""

    def __init__(self):
        """Initialize Html Display.

        @DEV
        - Maybe look into ways of configuring browser window.
        """
        pass

    def draw(self, p_help_uri: str):
        """Open web browser to display HTML resource.

        Args: (str) UTI to HTML file to display in browser.
        """
        webbrowser.open(p_help_uri)
        # webbrowser.open_new_tab(p_help_uri)


class InfoBar(object):
    """Info Bar item.
    It is located across bottom of window.
    """

    def __init__(self, p_text: str = ""):
        """Initialize Info Bar."""
        if p_text == "":
            self.text = (
                "Python: "
                + platform.python_version()
                + " | Pygame: "
                + pg.version.ver
                + " | OS: "
                + platform.platform()
            )
        else:
            self.text = p_text
        self.itxt = APD.F_SANS_TINY.render(
            self.text, True, CLR.CP_BLUEPOWDER, CLR.CP_BLACK
        )
        self.ibox = self.itxt.get_rect()
        self.ibox.topleft = PG.IBAR_LOC

    def draw(
        self,
        p_frame_cnt_mode: bool = False,
        p_frame_cnt: int = 0,
        p_mouse_loc: tuple = (0, 0),
    ):
        """Draw Info Bar.
        Optionally draw frame count and mouse location.

        :args:
        - p_frame_cnt_mode: (bool) True to display frame counter
        - p_frame_cnt: (int) Frame counter value
        - p_mouse_loc: (tuple) Mouse location (x, y)
        """
        PG.WIN.blit(self.itxt, self.ibox)
        if p_frame_cnt_mode is True:
            genimg = PG.F_SANS_12.render(
                "Generation: "
                + str(p_frame_cnt)
                + "    |    Mouse: "
                + str(p_mouse_loc),
                True,
                CLR.CP_BLUEPOWDER,
                CLR.CP_BLACK,
            )
            PG.WIN.blit(genimg, genimg.get_rect(topleft=(PG.WIN_W * 0.67, PG.IBAR_Y)))

class TextInput(pg.sprite.Sprite):
    """Define and handle a text input widget."""

    def __init__(self, p_x: int, p_y: int, p_w: int = 100, p_h: int = 50):
        """
        Define text input widget.

        :args:
        - p_x: (int) x-coordinate of top left corner
        - p_y: (int) y-coordinate of top left corner
        - p_w: (int) width of text input widget
        - p_h: (int) height of text input widget
        """
        super().__init__()
        self.t_box = pg.Rect(p_x, p_y, p_w, p_h)
        self.t_value = ""
        self.t_font = PG.F_FIXED_18
        self.t_color = CLR.CP_GREEN
        self.text = self.t_font.render(self.t_value, True, self.t_color)
        self.is_selected = False

    def draw(self):
        """Place text in the widget, centered in the box.
        This has the effect of expanding the text as it is typed
        in both directions. Draw the surface (box). Then blit the text.
        """
        self.pos = self.text.get_rect(
            center=(self.t_box.x + self.t_box.w / 2, self.t_box.y + self.t_box.h / 2)
        )
        if self.is_selected:
            pg.draw.rect(PG.WIN, CLR.CP_BLUEPOWDER, self.t_box, 2)
        else:
            pg.draw.rect(PG.WIN, CLR.CP_BLUE, self.t_box, 2)
        PG.WIN.blit(self.text, self.pos)

    def clicked(self, p_mouse_loc) -> bool:
        """Return True if mouse is clicked in the widget."""
        if self.t_box.collidepoint(p_mouse_loc):
            self.is_selected = not (self.is_selected)
            return True
        return False

    def update_text(self, p_text: str):
        """Update text value.
        If text is too wide for the widget, truncate it.
        - `self.value` is the current value of the text string.
        - `self.text` is the rendered text surface.
        It actually gets updated in the `draw` method.

        :args:
        - p_text: (str) Newest version of text to render.
        """
        temp_txt = self.t_font.render(p_text, True, self.t_color)
        if temp_txt.get_rect().width > (self.t_box.w - 10):
            p_text = p_text[:-1]
            temp_txt = self.t_font.render(p_text, True, self.t_color)
        self.t_value = p_text
        self.text = temp_txt


class TextInputGroup(pg.sprite.Group):
    """Define a group object.
    A pygame group is basically a list of objects.
    Customized from the multiple sprites tracker to track text input widgets.
    The `current` attribute holds the currently-selected txtin widget.
    Conversely, the textinput object itself has an `is_selected` attribute
    that is True if it is the currently-selected txtin widget.
    If no textinput object is selected, then `current` is None and no
    txtin object has is_selected == True.
    """

    def __init__(self):
        super().__init__()
        self.current = None  # ID currently-selected text input widget.


# ====================================================
#  SASKAN ADMIN
# ====================================================
class SaskanAdmin(object):
    """PyGame GUI for controlling Saskantinon functions.
    Initiated and executed by __main__.
    """

    def __init__(self, *args, **kwargs):
        """
        Refresh shared data space.
        Initialize counters, modes, trackers, widgets.
        Execute the main event loop.
        """
        # FM.pickle_saskan(path.join("/home", Path.cwd().parts[2], FM.D["APP"]))
        # WT.log("info", "", __file__, __name__, self, sys._getframe())

        # Mouse tracking
        self.mouse_loc = (0, 0)
        # Keyboard assignments
        self.QUIT_KY: list = [pg.K_q, pg.K_ESCAPE]
        self.ANIM_KY: list = [pg.K_F3, pg.K_F4, pg.K_F5]
        self.DATA_KY: list = [pg.K_a, pg.K_l]
        self.RPT_TYPE_KY: list = [pg.K_KP1, pg.K_KP2, pg.K_KP3]
        self.RPT_MODE_KY: list = [pg.K_UP, pg.K_RIGHT, pg.K_LEFT]
        # Animation modes
        self.frame_cnt_mode = False
        self.frame_cnt = 0
        self.freeze_mode = False
        # Information bar
        self.IBAR = InfoBar("")
        # Menu bars and items
        self.MEG = MenuGroup()
        prev_x = PG.MBAR_X
        for _, mn in FM.G["menus"]["menu"].items():
            mn_nm = mn["nm"]
            self.MEG.add_bar(MenuBar(mn_nm, prev_x))
            prev_x = self.MEG.mbars[mn_nm].mbox.right
            mil = [(mi_id, mi["nm"]) for mi_id, mi in mn["items"].items()]
            self.MEG.add_item(MenuItems(mil, self.MEG.mbars[mn_nm]))
        # Page header
        self.PHDR = PageHeader(FM.G["frame"]["pg_hdr"]["default_text"])
        # External windows
        # webbrowser.register('firefox')
        self.WHTML = HtmlDisplay()

        # Test log message
        msg = "Mouse location: " + str(self.mouse_loc)
        # WT.log("info", msg, __file__, __name__, self, sys._getframe())
        # Test log report
        # WT.dump_log()

        # Make it go!
        self.main_loop()

    # Mouse Click Event Handlers
    # ==============================================================
    def do_select_mbar(self, p_mouse_loc):
        """Trap for a mouse click on a menu bar item.

        :args:
        - p_mouse_loc: (tuple) mouse location
        """
        self.MEG.current_bar is None
        self.MEG.current_item = None
        for m_nm, mbar in self.MEG.mbars.items():
            if mbar.clicked(p_mouse_loc):
                if mbar.is_selected:
                    # Hide bar and item list if currently selected.
                    mbar.is_selected = False
                    self.MEG.mitems[m_nm].is_visible = False
                else:
                    mbar.is_selected = True
                    # Hide any other visible item list.
                    for _, mitm in self.MEG.mitems.items():
                        mitm.is_visible = False
                    self.MEG.mitems[m_nm].is_visible = True
                    self.MEG.current_bar = mbar
            else:
                mbar.is_selected = False

    def do_select_mitem(self, p_mouse_loc):
        """Trap for a mouse click on a menu item.

        :args:
        - p_mouse_loc: (tuple) mouse location
        """
        item_nm = None
        self.MEG.current_item = None
        for _, ilist in self.MEG.mitems.items():
            if ilist.is_visible:
                item_nm = ilist.clicked(p_mouse_loc)
                if item_nm is not None:
                    self.MEG.current_item = ilist
        return item_nm

    # Keyboard and Menu Item Event Handlers
    # ==============================================================
    def exit_app(self):
        """Exit the app."""
        pg.quit()
        sys.exit()

    def handle_menu_event(self, p_menu_item):
        """Trigger an event based on menu item selection."""
        menu_nm = self.MEG.current_item.name
        m_item_id = p_menu_item[0]
        m_item_text = p_menu_item[1]
        print(menu_nm, m_item_id, m_item_text)
        if m_item_id == "exit":
            self.exit_app()
        elif "help" in m_item_id:
            if m_item_id == "pg_help":
                self.WHTML.draw(FM.G["uri"]["help"]["pygame"])
            elif m_item_id == "app_help":
                self.WHTML.draw(FM.G["uri"]["help"]["app"])
            elif m_item_id == "game_help":
                self.WHTML.draw(FM.G["uri"]["help"]["game"])

    def check_exit_app(self, event: pg.event.Event):
        """Handle exit if one of the exit modes is triggered.
        This is triggered by the Q key, ESC key or `X`ing the window.

        :args:
        - event: (pg.event.Event) event to handle
        """
        if event.type == pg.QUIT or (
            event.type == pg.KEYUP and event.key in self.QUIT_KY
        ):
            self.exit_app()

    # Loop Events
    # ==============================================================
    def track_state(self):
        """Keep track of the state of the app on each frame.

        Sets:
        - mouse_loc: get current mouse location
        - cursor: if no text input box is activated, set to default
        - frame_cnt: increment if not in a freeze mode
        """
        self.mouse_loc = pg.mouse.get_pos()

        # For managing text input boxes:
        # if self.TIG.current is None:
        #     pg.mouse.set_cursor(pg.cursors.Cursor())

        if self.frame_cnt_mode is True and self.freeze_mode is False:
            self.frame_cnt += 1

    def refresh_screen(self):
        """Refresh the screen with the current state of the app.
        30 milliseconds between each frame is the normal framerate.
        To go into slow motion, add a wait here. Don't change the framerate.
        """
        PG.WIN.fill(CLR.CP_BLACK)
        self.IBAR.draw()
        for m_nm, mbar in self.MEG.mbars.items():
            mbar.draw()
            self.MEG.mitems[m_nm].draw()

        self.PHDR.draw()

        # for txtin in self.TIG:
        #     txtin.draw()
        # self.PAGE.draw()

        pg.display.update()
        PG.TIMER.tick(30)

    # Main Loop
    # ==============================================================
    def main_loop(self):
        """Manage the event loop.
        - Handle window events (quit --> ESC or Q)
        - Handle animation events (F3, F4, F5)
        - Handle data load events (F7, F8)
        - Handle mouse events
        """
        # WT.log("info", "", __file__, __name__, self, sys._getframe())
        while True:
            self.track_state()

            for event in pg.event.get():
                self.check_exit_app(event)

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.do_select_mbar(self.mouse_loc)
                    menu_item = self.do_select_mitem(self.mouse_loc)
                    if self.MEG.current_item is not None:
                        self.handle_menu_event(menu_item)
                    # self.do_select_txtin(self.mouse_loc):

            if self.freeze_mode is False:
                self.refresh_screen()


# Run program
if __name__ == "__main__":
    """Run program."""
    MNU = AdminMenu()
    # WEB = HtmlDisplay()  # for Help/Link windows
    # IBAR = InfoBar()
    # WINS = Windows()
    # STG = Stage()
    # SaskanAdmin()
