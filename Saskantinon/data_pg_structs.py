"""
:module:    data_pg_structs.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
Define static constants and non-DB data structures
 which use pygame for rendering.
"""

from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401

from data_structs import ImageType, GroupStruct

import pygame as pg
pg.init()          # Init PyGame for use in this module


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
    FONT_FXD = 'Courier 10 Pitch'
    FONT_MED_SZ = 30
    FONT_SANS = 'DejaVu Sans'
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
    KEYMOD_NONE = 4096   # No modifier key pressed
    # Window and Clock objects
    # ---------------------------
    WIN_W = 0.0
    WIN_H = 0.0
    WIN_MID = 0.0
    WIN = None
    TIMER = None
    # In-Memory objects
    # ---------------------------
    MENUS: dict = {}
    LINKS: dict = {}
    INFO: dict = {}
    WINDOWS: dict = {}


#  SIMPLE DATA STRUCTURES
# ============================

class Graphic(object):
    """An object for referencing an image file."""
    import pygame as pg
    pg.init()          # Init PyGame for use in this module
    pg_surface: pg.Surface
    pg_rect: pg.Rect
    img_type: ImageType
    img_url: str = ''
    img_desc: str = ''


class PygameRect(object):
    """A simple structure for a pygame Rect object."""
    def __init__(self,
                 p_top_left: GroupStruct.CoordXY,
                 p_top_right: GroupStruct.CoordXY,
                 p_bottom_left: GroupStruct.CoordXY,
                 p_bottom_right: GroupStruct.CoordXY,
                 p_fill: bool = False,
                 # reference constant instead...
                 p_fill_color: pg.Color = pg.Color(0, 0, 0),
                 p_line_color: pg.Color = pg.Color(0, 0, 0),
                 p_line_width: float = 0.0):
        """
        Set abstract coordinates/location, and optionally
        fill and line attributes.
        :args:
        -- p_top_left: top left coordinate (x, y)
        -- p_top_right: top right (x, y)
        -- p_bottom_left: bottom left (x, y)
        -- p_bottom_right: bottom right (x, y)
        -- p_fill: fill the shape (True or False)
        -- p_fill_color: fill color (pygame color object)
        -- p_line_color: line color (pygame color object)
        -- p_line_width: line width (float)
        """
        self.coords =\
            self.set_coords(p_top_left,
                            p_top_right,
                            p_bottom_left,
                            p_bottom_right)
        self.fill =\
            self.set_fill(p_fill,
                          p_fill_color)
        self.line =\
            self.set_line(p_line_color,
                          p_line_width)
        self.box = self.set_pygame_rect()

    def set_rect(self) -> pg.Rect:
        """ Set pygame Rect object.
            (left, top, width, height)
        """
        return pg.Rect(self.coords['left'],
                       self.coords['top'],
                       self.coords['width'],
                       self.coords['height'])


class GamePlane(object):
    """
    A general purpose shape structure that is planar
    and rectangular, defining only the corners of a
    rectangular space relative to x,y coordinates in a
    containing coordinate system is useful for
    describing areas within a map or grid.

    Line and fill attributes may optonally be set.
    A pygame Rect object is derived from the corners.
    """
    def __init__(self,
                 p_top_left: GroupStruct.CoordXY,
                 p_top_right: GroupStruct.CoordXY,
                 p_bottom_left: GroupStruct.CoordXY,
                 p_bottom_right: GroupStruct.CoordXY,
                 p_fill: bool = False,
                 # reference constant instead...
                 p_fill_color: pg.Color = pg.Color(0, 0, 0),
                 p_line_color: pg.Color = pg.Color(0, 0, 0),
                 p_line_width: float = 0.0):
        """
        Set abstract coordinates/location, and optionally
        fill and line attributes.
        :args:
        -- p_top_left: top left coordinate (x, y)
        -- p_top_right: top right (x, y)
        -- p_bottom_left: bottom left (x, y)
        -- p_bottom_right: bottom right (x, y)
        -- p_fill: fill the shape (True or False)
        -- p_fill_color: fill color (pygame color object)
        -- p_line_color: line color (pygame color object)
        -- p_line_width: line width (float)
        """
        self.coords =\
            self.set_coords(p_top_left,
                            p_top_right,
                            p_bottom_left,
                            p_bottom_right)
        self.fill =\
            self.set_fill(p_fill,
                          p_fill_color)
        self.line =\
            self.set_line(p_line_color,
                          p_line_width)
        self.box = self.set_pygame_rect()

    def set_coords(self,
                   p_top_left,
                   p_top_right,
                   p_bottom_left,
                   p_bottom_right) -> dict:
        """ Set x,y coordinates/corner locations
        relative to a containing coordinate system.
        Derive the width and height of the plane and
        the integer x and y for top and left.
        """
        return {'top_left': p_top_left,
                'top_right': p_top_right,
                'bottom_left': p_bottom_left,
                'bottom_right': p_bottom_right,
                'left': p_top_left.x,
                'top': p_top_left.y,
                'width': p_top_right.x - p_top_left.x,
                'height': p_bottom_left.y - p_top_left.y}

    def set_fill(self,
                 p_fill,
                 p_fill_color) -> dict:
        """ Set attributes of the plane fill.
        """
        return {'is_filled': p_fill,
                'fill_color': p_fill_color}

    def set_line(self,
                 p_line_color,
                 p_line_width) -> dict:
        """ Set attributes of the plane line.
        """
        return {'line_color': p_line_color,
                'line_width': p_line_width}

    def set_pygame_rect(self) -> pg.Rect:
        """ Set pygame Rect object.
           (left, top, width, height)
        """
        return pg.Rect(self.coords['left'],
                       self.coords['top'],
                       self.coords['width'],
                       self.coords['height'])


class GameGridData(object):
    """
    PSet up a matrix of cells within a grid, both to direct
    rendering, and to store data within each cell. The drawing
    data is 2D oriented, but the data-content supports 3D,
    like a layer cake or slices of a scan.

    Specs for rendering grid and cells have two inputs:
    - number of rows and columns -- init params
    - grid placement in map-window is defined in AppDisplay
    For smaller cells, assign more rows and columns to the grid.
    For bigger cells, assign fewer rows and columns.

    - Supports 3 dimensions in layered fashion.
    - To use as a 2D grid, set p_z values to zero.
    """
    def __init__(self,
                 p_cols: int = 1,
                 p_rows: int = 1,
                 p_z_up: int = 0,
                 p_z_down: int = 0):
        """
        Number of cells in matrix:
        :args:
        -- p_cols: number of columns ("vertical" or N-S cells)
        -- p_rows: number of rows ("horizontal" or E-W cells)
        -- p_z_up: number of "up" cells
        -- p_z_down: number of "down" cells
        Location of grid-box in map window is set in AppDisplay.
        """
        x_offset = int(round(AppDisplay.GAMEMAP_W * 0.01))
        y_offset = int(round(AppDisplay.GAMEMAP_H * 0.02))
        self.visible = False
        self.plane, self.box =\
            self._set_grid_rects(x_offset, y_offset)
        self.grid_size =\
            self.set_grid_size(p_cols, p_rows, p_z_up, p_z_down)
        self.cell_size = self.set_cell_size(x_offset, y_offset)
        self.grid_lines = self.set_grid_lines(x_offset, y_offset)
        self.grid_data = self.set_grid_data()

    def _set_grid_rects(self,
                        x_offset: int,
                        y_offset: int) -> tuple:
        """ Set GamePlane and pygame Rect objects for the grid.
        These help place and render the grid as a whole. Since inputs
        are set by the constant structure 'AppDisplay', this method is
        treated as "internal".
        Assumes a 2D rendering of each "z-layer" of the grid.
        Default z-layer is the zero-layer.
        No attempt to provide skew for 3D rendering.
        :returns:
        - (grid_rect, grid_rect_pygame): tuple of GamePlane and pygame Rect
        """
        x = AppDisplay.GAMEMAP_X + x_offset
        y = AppDisplay.GAMEMAP_Y + y_offset
        w = AppDisplay.GAMEMAP_W
        h = AppDisplay.GAMEMAP_H
        game_plane = GamePlane(
            p_top_left=GroupStruct.CoordXY(x, 0),
            p_top_right=GroupStruct.CoordXY(w, 0),
            p_bottom_left=GroupStruct.CoordXY(x, h),
            p_bottom_right=GroupStruct.CoordXY(w, h))
        grid_rect_pygame = pg.Rect(x, y, w, h)
        return (game_plane, grid_rect_pygame)

    def set_grid_size(self,
                      p_cols,
                      p_rows,
                      p_z_up,
                      p_z_down) -> dict:
        """ Set x, y and z dimensions for the grid based on inputs.
        That is, how many cells are contained in the grid/matrix.
        In this method, a 3D matrix is supported. Here, z-dimension is
        handled separately for "up" and "down", rather than using
        positive and negative values.
        :returns:
        - {rc, zz}: dict of column/row and up/down dimensions
        """
        rc = GroupStruct.ColumnRowIndex()
        rc.r = p_cols
        rc.c = p_rows
        zz = GroupStruct.MatrixUpDown()
        zz.z_up = p_z_up
        zz.z_down = p_z_down
        return {'rc': rc, 'zz': zz}

    def set_cell_size(self,
                      x_offset: int,
                      y_offset: int) -> dict:
        """ Set width, height in pixels of a single cell.
        Support placement and rendering of cells within the grid.
        In this case width and height refer to sizes within the
        z-zero plane, that is, "height" is in the sense of a 2D grid,
        not in the sense of the z-directions of the 3D grid.

        At this point, a "cell" is a rectangle, not a cube.
        :returns:
        {w, h}: width, height of each cell
        """
        w = int(round(AppDisplay.GAMEMAP_W - x_offset) /
                self.grid_size['rc'].c)
        h = int(round(AppDisplay.GAMEMAP_H - y_offset) /
                self.grid_size['rc'].r)
        return {'w': w, 'h': h}

    def set_grid_lines(self,
                       x_offset: int,
                       y_offset: int) -> dict:
        """ Set dimensions, location, of the cell lines.
        Support placement and rendering of the cells.  Again,
        this refers solely to a "flat" plane. No attempt to provide
        a 3D rendering. Only store the coordinates of the
        top-left starting-point for the lines, the width of the
        horizontal lines, and the height of the vertical lines.
        Handle placement of remaining lines in a rendering method.
        :returns:
        {x, y, w, h}: x, y of first line,
                      width of horizontal lines,
                      height of vertical lines
        """
        x = int(round(self.box.x + x_offset))
        y = int(round(self.box.y + y_offset))
        w = self.cell_size['w'] * self.grid_size['rc'].c
        h = self.cell_size['h'] * self.grid_size['rc'].r
        return {'x': x, 'y': y, 'w': w, 'h': h}

    def set_grid_data(self) -> dict:
        """Define a structure that holds cell data of various types.
        Then assign a copy of that structure to each cell in the grid,
        including the z directions, which here are keyed as positive (up)
        and negative (down).
        Might be more efficient to initialize to empty dicts or None?
        """
        grid_matrix = dict()
        cell_data = {
            'fill': False,
            'fill_color': PygColors.CP_BLACK,
            'line_color': PygColors.CP_BLACK,
            'text': '',
            'img': Graphic,
            'state_data': {}
        }
        for r in range(self.grid_size['rc'].r + 1):
            grid_matrix[r] = dict()
            for c in range(self.grid_size['rc'].c + 1):
                grid_matrix[r][c] = dict()
                for z in range(self.grid_size['zz'].z_up + 1):
                    grid_matrix[r][c][z] = dict()
                    grid_matrix[r][c][z] = cell_data
                for d in range(self.grid_size['zz'].z_down + 1):
                    z = d * -1
                    grid_matrix[r][c][z] = dict()
                    grid_matrix[r][c][z] = cell_data
        return grid_matrix


#  GAME-RELATED BASIC DATA ALGORTIHMS
# ===================================
class CompareRect(object):
    """
    Compare pygame rectangles:
    - Check for containment
    - Check for intersections (overlap, collision/union)
    - Check for adjacency/borders (clipline)
    - Check for equality/sameness
    """

    def __init__(self):
        pass

    def rect_contains(self,
                      p_box_a: pg.Rect,
                      p_box_b: pg.Rect) -> bool:
        """Determine if rectangle A contains rectangle B.
        use pygame contains
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        if p_box_a.contains(p_box_b):
            return True
        else:
            return False

    def rect_overlaps(self,
                      p_box_a: pg.Rect,
                      p_box_b: pg.Rect) -> bool:
        """Determine if rectangle A and rectangle B overlap.
        xxx use pygame colliderect xxx
        use pygame union
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        # if p_box_a.colliderect(p_box_b):
        if p_box_a.union(p_box_b):
            return True
        else:
            return False

    def rect_borders(self,
                     p_rect_a: pg.Rect,
                     p_rect_b: pg.Rect) -> bool:
        """Determine if rectangle A and rectangle B share a border.
        use pygame clipline
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        if p_rect_a.clipline(p_rect_b):
            return True
        else:
            return False

    def rect_same(self,
                  p_rect_a: pg.Rect,
                  p_rect_b: pg.Rect) -> bool:
        """Determine if rectangle A and rectangle B occupy exactly
        the same space.
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        if p_rect_a.topright == p_rect_b.topright and \
           p_rect_a.bottomleft == p_rect_b.bottomleft:
            return True
        else:
            return False
