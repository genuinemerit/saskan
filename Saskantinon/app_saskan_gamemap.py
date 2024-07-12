"""
:module:    app_saskan_gamemap.py
:author:    GM (genuinemerit @ pm.me)

Saskan Game module for managing game map.
"""

from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401

from data_structs_pg import PygColors, Graphic

import pygame as pg
pg.init()


class GameMap(object):
    """
    Manage loading and handling of data in the gamemap
    window and related MAP, GRID, etc. data structures.

    Start by dealing only with 2D data.

    :args:
    -

    ==============
    old docs:
    PSet up a matrix of cells within a grid, both to direct
    rendering, and to store data within each cell. The drawing
    data is 2D oriented, but the data-content supports 3D,
    like a layer cake or slices of a scan.

    The basic idea is to have unified data structure for
    storing the union of GRID, MAP, and related data. To the
    extent this can be simplified, and we can use the data
    structures as passed in from the database, do it.

    Keep an eye on this class, but let's start with a simple
    collector like we have with MENUS, LINKS, WINDOWS and
    INFO.

    Specs for rendering grid and cells have two inputs:
    - number of rows and columns -- init params
    - grid placement in map-window is defined in AppDisplay
    For smaller cells, assign more rows and columns to the grid.
    For bigger cells, assign fewer rows and columns.

    - Supports 3 dimensions in layered fashion.
    - To use as a 2D grid, set p_z values to zero.
    ==============
    """
    def __init__(self):
        """Create GAMEMAP object."""
        pass

    def create_gamemap(self,
                       WINDOWS: object,
                       MAPS: object,
                       GRIDS: object,
                       p_map_name: str = None,
                       p_grid_name: str = None):
        """
        :args:
        - WINDOWS (dict) -- PG.WINDOWS
        - MAPS (dict) -- PG.MAPS
        - GRIDS (dict) -- PG.GRIDS
        - p_map_name (str) -- name of map to load
        - p_grid_name (str) -- name of grid to load

        Default to first MAP and GRID if no name provided.
        Add an extra row and column at the top, bottom, left and right
          for showing grid reference numbers, scale keys, etc.
        Also remember to draw a line at the top and bottom of the grid,
          and on both left and right sides.
        :return:
        -  GRIDS (dict) -- updated GRIDS dict
        """
        p_map_name = p_map_name or list(MAPS.keys())[0]
        p_grid_name = p_grid_name or list(GRIDS.keys())[0]
        GRIDS[p_grid_name] =\
            self.set_grid_lines(WINDOWS["gamemap"], GRIDS[p_grid_name])
        return GRIDS

    def set_grid_lines(self,
                       W: dict,
                       G: dict) -> dict:
        """
        Set grid lines for drawing.
        Define dimensions for drawing the grid cells, including
          the 2 extra rows and columns for grid reference numbers.
        """
        G['x'] = int(round(W['w_box'].left + 6))
        G['y'] = int(round(W['w_box'].top + 6))
        G['w'] = int(round(W['w_box'].width - 12))
        G['h'] = int(round(W['w_box'].height - 12))
        G['cell_w'] = round((G['w'] / (G['col_cnt'] + 2)), 2)
        G['cell_h'] = round((G['h'] / (G['row_cnt'] + 2)), 2)
        G['h_lines'] = []
        G['v_lines'] = []
        y = G['y']
        for r in range(0, G['row_cnt'] + 3):
            G['h_lines'].append(((G['x'], round(y, 2)),
                                 (G['x'] + G['w'], round(y, 2))))
            y += G['cell_h']
        x = G['x']
        for c in range(0, G['col_cnt'] + 3):
            G['v_lines'].append(((round(x, 2), G['y']),
                                 (round(x, 2), G['y'] + G['h'])))
            x += G['cell_w']
        return G

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

    def compute_map_scale(self,
                          p_attr: dict,
                          DSP: object):
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

    def draw_grid(self):
        """Draw "grid" and "map" in GAMEMAP using PG, STG objects.
        """
        # Draw grid box with thick border
        pg.draw.rect(APD.WIN, CLR.CP_SILVER, APD.GRID_BOX, 5)
        # Draw grid lines      # vt and hz are: ((x1, y1), (x2, y2))
        for vt in APD.G_LNS_VT:
            pg.draw.aalines(APD.WIN, CLR.CP_WHITE, False, vt)
        for hz in APD.G_LNS_HZ:
            pg.draw.aalines(APD.WIN, CLR.CP_WHITE, False, hz)
        # Highlight grid squares inside or overlapping the map box
        for _, grec in PG.GRIDS.items():
            if "is_inside" in grec.keys() and grec["is_inside"]:
                pg.draw.rect(APD.WIN, CLR.CP_WHITE, grec["box"], 0)
            elif "overlaps" in grec.keys() and grec["overlaps"]:
                pg.draw.rect(APD.WIN, CLR.CP_SILVER, grec["box"], 0)
        # Draw map box with thick border
        if STG.MAP_BOX is not None:
            pg.draw.rect(APD.WIN, CLR.CP_PALEPINK, STG.MAP_BOX, 5)

    def draw_hover_cell(self,
                        p_grid_loc: str):
        """
        Highlight/colorize grid-cell indicating grid that cursor is
        presently hovering over. When this method is called from
        refesh_screen(), it passes in a APD.GRID key in p_grid_loc.
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
            pg.draw.rect(APD.WIN, CLR.CP_PALEPINK,
                         STG.GRIDS[p_grid_loc]["box"], 0)


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
