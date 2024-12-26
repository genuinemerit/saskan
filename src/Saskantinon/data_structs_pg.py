"""
:module:    data_structs_pg.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
Define static constants and non-DB data structures
 which use pygame for rendering.
"""

from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

import data_structs as DS
import pygame as pg

from data_structs import ImageType

pg.init()  # Init PyGame for use in this module
AD = DS.AppDisplay()


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

    # PyGame Fonts
    # -------------------
    F_SANS_TINY = pg.font.SysFont(AD.FONT_SANS, AD.FONT_TINY_SZ)
    F_SANS_SM = pg.font.SysFont(AD.FONT_SANS, AD.FONT_SM_SZ)
    F_SANS_MED = pg.font.SysFont(AD.FONT_SANS, AD.FONT_MED_SZ)
    F_SANS_LG = pg.font.SysFont(AD.FONT_SANS, AD.FONT_LARGE_SZ)
    F_FIXED_LG = pg.font.SysFont(AD.FONT_FXD, AD.FONT_LARGE_SZ)
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


#  SIMPLE DATA STRUCTURES
# ============================


class Graphic(object):
    """An object for referencing an image file."""

    pg_surface: pg.Surface
    pg_rect: pg.Rect
    img_type: ImageType
    img_url: str = ""
    img_desc: str = ""
