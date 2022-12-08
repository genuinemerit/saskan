#!python
"""
:module:    saskan_eyes.py
:author:    GM (genuinemerit @ pm.me)
BoW Saskan App GUI.  pygame version.

See: ../design/pygame_notes.md
"""

import platform
import pygame as pg
import sys
import typing

from dataclasses import dataclass
from pprint import pprint as pp     # noqa: F401

from io_file import FileIO          # type: ignore
from io_wiretap import WireTap      # type: ignore

FI = FileIO()
WT = WireTap()
pg.init()


@dataclass(frozen=True)
class PG:
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
    PC_BLACK = pg.Color(0, 0, 0)
    PC_BLUE = pg.Color(0, 0, 255)
    PC_BLUEPOWDER = pg.Color(176, 224, 230)
    PC_GREEN = pg.Color(0, 255, 0)
    PC_PALEPINK = pg.Color(215, 198, 198)
    PC_RED = pg.Color(255, 0, 0)
    PC_WHITE = pg.Color(255, 255, 255)
    # PyGame Fonts
    F_SANS_12 = pg.font.SysFont('DejaVu Sans', 12)
    F_SANS_16 = pg.font.SysFont('DejaVu Sans', 16)
    F_SANS_18 = pg.font.SysFont('DejaVu Sans', 18)
    F_FIXED_18 = pg.font.SysFont('Courier 10 Pitch', 18)
    # PyGame Cursors
    CUR_ARROW = pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW)
    CUR_CROSS = pg.cursors.Cursor(pg.SYSTEM_CURSOR_CROSSHAIR)
    CUR_HAND = pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND)
    CUR_IBEAM = pg.cursors.Cursor(pg.SYSTEM_CURSOR_IBEAM)
    CUR_WAIT = pg.cursors.Cursor(pg.SYSTEM_CURSOR_WAIT)
    # Window / Canvas / Display
    pg.display.set_caption(FI.g["frame"]["ttl"])
    WIN_W = FI.g["frame"]["sz"]["w"]
    WIN_H = FI.g["frame"]["sz"]["h"]
    WIN_MID = (WIN_W / 2, WIN_H / 2)
    WIN = pg.display.set_mode((WIN_W, WIN_H))
    # Info Bar
    IBAR_X = FI.g["frame"]["ibar"]["x"]
    IBAR_Y = FI.g["frame"]["ibar"]["y"]
    IBAR_LOC = (IBAR_X, IBAR_Y)
    # Menu Bar
    # Note: MBAR_W is the width of each individual menu bar menu,
    # width of the total menu bar is cumulative of all menu bar menus.
    # To get more clever, may want to adjust the width of each menu
    # according to the size of its text.
    MBAR_X = FI.g["menus"]["bar"]["x"]
    MBAR_Y = FI.g["menus"]["bar"]["y"]
    MBAR_W = FI.g["menus"]["bar"]["w"]
    MBAR_H = FI.g["menus"]["bar"]["h"]
    MBAR_MARGIN = FI.g["menus"]["bar"]["margin"]
    MBAR_LOC = (MBAR_X, MBAR_Y)
    # Report Page Widgets
    HDR_LOC = (60, 40)      # LOC = Top-Left x, y
    PAGE_X = 60
    PAGE_Y = 60
    PAGE_MAX_LNS = 38    # max lines to display per column
    PAGE_V_OFF = 22      # vertical offset for each line of text
    PAGE_COLS = [(PAGE_X, PAGE_Y),
                 (WIN_W * 0.33, PAGE_Y),
                 (WIN_W * 0.67, PAGE_Y)]
    # Other
    KEYMOD_NONE = 4096
    TIMER = pg.time.Clock()


class MenuBar(object):
    """ Menu Bar items for the application.
    Define a surface for a clickable top-level menu bar item.
    Clicking on a menu bar item opens or closes a MenuItems.
    """
    def __init__(self,
                 p_name: str,
                 p_x_left: int):
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
        self.mbox = pg.Rect(p_x_left, PG.MBAR_Y,
                            PG.MBAR_W, PG.MBAR_H)
        self.mtxt = PG.F_SANS_12.render(
            self.text, True, PG.PC_BLUEPOWDER, PG.PC_BLACK)
        self.tbox = self.mtxt.get_rect()
        self.tbox.topleft =\
            (p_x_left + int((self.mbox.width - self.tbox.width) / 2),
             PG.MBAR_Y + PG.MBAR_MARGIN)

    def draw(self):
        """ Draw a Menu Bar item.
        """
        if self.is_selected:
            pg.draw.rect(PG.WIN, PG.PC_BLUEPOWDER, self.mbox, 2)
        else:
            pg.draw.rect(PG.WIN, PG.PC_BLUE, self.mbox, 2)
        PG.WIN.blit(self.mtxt, self.tbox)

    def clicked(self, p_mouse_loc) -> bool:
        """ Return True if mouse clicked on the mbox.
        """
        if self.mbox.collidepoint(p_mouse_loc):
            self.is_selected = not(self.is_selected)
            return True
        return False


class MenuItems(object):
    """Define one or more MenuItem associated with a MenuBar.
    Clicking on a menu bar item triggers a function and sets
    visibility of the MenuItems to False.
    """
    def __init__(self,
                 p_mitm_list: list,
                 p_mbar: MenuBar):
        """ Initialize Menu Items.
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
        self.mbox = pg.Rect(p_mbar.mbox.left,
                            p_mbar.mbox.bottom,
                            p_mbar.mbox.width,
                            p_mbar.mbox.height * self.item_cnt)
        self.mitems = []
        for mx, mi_nm in enumerate(p_mitm_list):
            mtxt = PG.F_SANS_12.render(
                mi_nm, True, PG.PC_BLUEPOWDER, PG.PC_BLACK)
            tbox = pg.Rect(self.mbox.left + PG.MBAR_MARGIN,
                           ((self.mbox.top + (PG.MBAR_H * mx)) +
                            PG.MBAR_MARGIN),
                           PG.MBAR_W, PG.MBAR_H)
            self.mitems.append({'mtxt': mtxt, 'tbox': tbox, 'text': mi_nm})

    def draw(self):
        """ Draw the list of Menu Items.
        """
        if self.is_visible:
            pg.draw.rect(PG.WIN, PG.PC_BLUEPOWDER, self.mbox, 2)
            for mi in self.mitems:
                PG.WIN.blit(mi['mtxt'], mi['tbox'])

    def clicked(self,
                p_mouse_loc):
        """ Return name of clicked menu item or None.
        If clicked on a menu item, set visibility of its container to False.

        @DEV:
        - The tbox coordinates are relative to the mbox.
        - The mouse_loc is relative to the window.
        - Need to convert mouse_loc to mbox coordinates or vice-versa.
        """
        for mi in self.mitems:
            pp(("Examining for click:", mi))
            pp(("mi['tbox']:", mi['tbox']))
            pp(("p_mouse_loc:", p_mouse_loc))
            if mi['tbox'].collidepoint(p_mouse_loc):
                print(f"Menu Item clicked!: {mi['text']}")
                self.is_visible = False
                return mi['text']
        return None


class MenuGroup(object):
    """Define a group object for menu bars and menu items.
    Reference menus by name and associate menu bar with its items.
    """
    def __init__(self):
        self.mbars: dict = dict()
        self.mitms: dict = dict()
        self.current_bar = None
        self.current_item = None

    def add_bar(self,
                p_mbar: MenuBar):
        """Add a MenuBar to the collection."""
        self.mbars[p_mbar.text] = p_mbar

    def add_item(self,
                 p_mitms: MenuItems):
        """Add a MenuItems to the collection."""
        self.mitms[p_mitms.name] = p_mitms


class PageHeader(object):
    """Set text for header.
    HDR is a widget drawn at top of the window.
    """

    def __init__(self,
                 p_hdr_txt: str = ""):
        """ Initialize PageHeader. """
        self.img = PG.F_SANS_18.render(p_hdr_txt, True,
                                       PG.PC_BLUEPOWDER, PG.PC_BLACK)
        self.box = self.img.get_rect()
        self.box.topleft = PG.HDR_LOC

    def draw(self):
        """ Draw PageHeader. """
        PG.WIN.blit(self.img, self.box)


class InfoBar(object):
    """Info Bar item.
    It is located across bottom of window.
    """

    def __init__(self,
                 p_text: str = ""):
        """ Initialize Info Bar. """
        if p_text == "":
            self.text = (
                "Python: " + platform.python_version() +
                " | Pygame: " + pg.version.ver +
                " | OS: " + platform.platform())
        else:
            self.text = p_text
        self.itxt = PG.F_SANS_12.render(
            self.text, True, PG.PC_BLUEPOWDER, PG.PC_BLACK)
        self.ibox = self.itxt.get_rect()
        self.ibox.topleft = PG.IBAR_LOC

    def draw(self,
             p_frame_cnt_mode: bool = False,
             p_frame_cnt: int = 0,
             p_mouse_loc: tuple = (0, 0)):
        """ Draw Info Bar.
        Optionally draw frame count and mouse location.

        :args:
        - p_frame_cnt_mode: (bool) True to display frame counter
        - p_frame_cnt: (int) Frame counter value
        - p_mouse_loc: (tuple) Mouse location (x, y)
        """
        PG.WIN.blit(self.itxt, self.ibox)
        if p_frame_cnt_mode is True:
            genimg = PG.F_SANS_12.render(
                "Generation: " + str(p_frame_cnt) +
                "    |    Mouse: " + str(p_mouse_loc),
                True, PG.PC_BLUEPOWDER, PG.PC_BLACK)
            PG.WIN.blit(genimg,
                        genimg.get_rect(topleft=(PG.WIN_W * 0.67,
                                                 PG.IBAR_Y)))


class TextInput(pg.sprite.Sprite):
    """Define and handle a text input widget.
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
        self.t_box = pg.Rect(p_x, p_y, p_w, p_h)
        self.t_value = ""
        self.t_font = PG.F_FIXED_18
        self.t_color = PG.PC_GREEN
        self.text = self.t_font.render(self.t_value, True, self.t_color)
        self.is_selected = False

    def draw(self):
        """ Place text in the widget, centered in the box.
        This has the effect of expanding the text as it is typed
        in both directions. Draw the surface (box). Then blit the text.
        """
        self.pos = self.text.get_rect(center=(self.t_box.x + self.t_box.w / 2,
                                              self.t_box.y + self.t_box.h / 2))
        if self.is_selected:
            pg.draw.rect(PG.WIN, PG.PC_BLUEPOWDER, self.t_box, 2)
        else:
            pg.draw.rect(PG.WIN, PG.PC_BLUE, self.t_box, 2)
        PG.WIN.blit(self.text, self.pos)

    def clicked(self, p_mouse_loc) -> bool:
        """ Return True if mouse is clicked in the widget.
        """
        if self.t_box.collidepoint(p_mouse_loc):
            self.is_selected = not(self.is_selected)
            return True
        return False

    def update_text(self, p_text: str):
        """ Update text value.
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
        self.current = None     # ID currently-selected text input widget.


class SaskanEyes(object):
    """PyGame GUI for controlling Saskantinon functions.
    Initiated and executed by __main__.
    """
    def __init__(self, *args, **kwargs):
        """
        Refresh shared data space.
        Initialize counters, modes, trackers, widgets.
        Execute the main event loop.
        """
        FI.pickle_saskan()
        WT.log_module(__file__, __name__, self)

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
        self.IBAR = InfoBar('')
        # Menu bars and items
        self.MEG = MenuGroup()
        moff = 0
        for _, mn in FI.g["menus"]["menu"].items():
            self.MEG.add_bar(MenuBar(mn["nm"],
                                     PG.MBAR_X + (PG.MBAR_W * moff)))
            moff += 1
            mil = [mi['nm'] for _, mi in mn["items"].items()]
            self.MEG.add_item(MenuItems(mil, self.MEG.mbars[mn["nm"]]))

        # Test log message
        WT.log_msg("info", "Mouse location: " + str(self.mouse_loc))
        # Test log report
        # WT.dump_log()

        # Make it go!
        self.main_loop()

    # Keyboard Event Handlers
    # ==============================================================
    @typing.no_type_check
    def check_exit_app(self, event: pg.event.Event):
        """Handle exit if one of the exit modes is triggered.
        This is triggered by the ESC key or `X`ing the window.

        :args:
        - event: (pg.event.Event) event to handle
        """
        if (event.type == pg.QUIT or
                (event.type == pg.KEYUP and
                    event.key in self.QUIT_KY)):
            pg.quit()
            sys.exit()

    # Event Routers
    # ==============================================================
    def track_state(self):
        """Keep track of the state of the app on each frame.

        Sets:
        - mouse_loc: get current mouse location
        - cursor: if no text input box is activated, set to default
        - frame_cnt: increment if not in a freeze mode
        """
        self.mouse_loc = pg.mouse.get_pos()

        # if self.TIG.current is None:
        #     pg.mouse.set_cursor(pg.cursors.Cursor())

        if self.frame_cnt_mode is True and self.freeze_mode is False:
            self.frame_cnt += 1

    def refresh_screen(self):
        """Refresh the screen with the current state of the app.
        30 milliseconds between each frame is the normal framerate.
        To go into slow motion, add a wait here. Don't change the framerate.
        """
        PG.WIN.fill(PG.PC_BLACK)
        self.IBAR.draw()
        for m_nm, mbar in self.MEG.mbars.items():
            mbar.draw()
            self.MEG.mitms[m_nm].draw()

        # for txtin in self.TIG:
        #     txtin.draw()
        # self.PHDR.draw()
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
        while True:
            self.track_state()

            for event in pg.event.get():
                self.check_exit_app(event)

            if self.freeze_mode is False:
                self.refresh_screen()


# Run program
if __name__ == '__main__':
    """Run program."""
    SaskanEyes()
