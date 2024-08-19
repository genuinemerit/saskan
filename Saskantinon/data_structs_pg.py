"""
:module:    data_structs_pg.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
Define static constants and non-DB data structures
 which use pygame for rendering.
"""

from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

import pygame as pg
from data_structs import ImageType

pg.init()  # Init PyGame for use in this module


#  UNIQUE CONSTANTS / "TRUE" ENUMS
# ================================
class PygColors(object):
    """Constants for PyGame colors.
    Reference class attributes directly.
    No need to instantiate this class.
    """

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


class AppDisplay(object):
    """Static values related to constructing GUI's in PyGame.
    Object place-holdrss used for rendering.
    As long as pg.display is not called, nothing will be rendered.
    """

    # Typesetting
    # -------------------
    DASH16: str = "-" * 16
    FONT_FXD = "Courier 10 Pitch"
    FONT_MED_SZ = 30
    FONT_SANS = "DejaVu Sans"
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
    KEYMOD_NONE = 4096  # No modifier key pressed
    # Window and Clock objects
    # ---------------------------
    WIN_W = 0.0
    WIN_H = 0.0
    WIN_MID = 0.0
    WIN = None
    TIMER = None


#  SIMPLE DATA STRUCTURES
# ============================


class Graphic(object):
    """An object for referencing an image file."""

    pg_surface: pg.Surface
    pg_rect: pg.Rect
    img_type: ImageType
    img_url: str = ""
    img_desc: str = ""
