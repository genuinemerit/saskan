"""
:module:    app_saskan_gamemap.py
:author:    GM (genuinemerit @ pm.me)

Saskan Game module for managing game map.
"""

from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

import pygame as pg
from data_structs_pg import Graphic, PygColors

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

    def create_gamemap(
        self,
        WINDOWS: object,
        MAPS: object,
        GRIDS: object,
        p_map_name: str = None,
        p_grid_id: str = None,
    ):
        """
        :args:
        - WINDOWS (dict) -- PG.WINDOWS
        - MAPS (dict) -- PG.MAPS
        - GRIDS (dict) -- PG.GRIDS
        - p_map_name (str) -- name of map to load
        - p_grid_id (str) -- name of grid to load

        Default to first MAP and GRID if no name provided.
        Add an extra row and column at the top, bottom, left and right
          for showing grid reference numbers, scale keys, etc.
        Also remember to draw a line at the top and bottom of the grid,
          and on both left and right sides.
        :return:
        -  GRIDS (dict) -- updated GRIDS dict
        """
        p_map_name = p_map_name or list(MAPS.keys())[0]
        p_grid_id = p_grid_id or list(GRIDS.keys())[0]
        W = WINDOWS["gamemap"]
        G = GRIDS[p_grid_id]
        GRIDS[p_grid_id] = self.set_grid_lines(W, G)
        GRIDS[p_grid_id]["cells"] = self.set_grid_matrix(W, G)
        return GRIDS

    def set_grid_lines(self, W: dict, G: dict) -> dict:
        """
        Set grid lines for drawing.
        Define dimensions for drawing the grid cells, including
          the 2 extra rows and columns for grid reference numbers.
        :args:
        - W (dict) -- PG.WINDOWS
        - G (dict) -- PG.GRIDS
        :returns:
        - G (dict) -- updated GRIDS dict
        """
        G["x"] = int(round(W["w_box"].left + 6))
        G["y"] = int(round(W["w_box"].top + 6))
        G["w"] = int(round(W["w_box"].width - 12))
        G["h"] = int(round(W["w_box"].height - 12))
        G["cell_w"] = round((G["w"] / (G["col_cnt"] + 2)), 2)
        G["cell_h"] = round((G["h"] / (G["row_cnt"] + 2)), 2)
        G["h_lines"] = []
        G["v_lines"] = []
        y = G["y"]
        for r in range(0, G["row_cnt"] + 3):
            G["h_lines"].append(((G["x"], round(y, 2)), (G["x"] + G["w"], round(y, 2))))
            y += G["cell_h"]
        x = G["x"]
        for c in range(0, G["col_cnt"] + 3):
            G["v_lines"].append(((round(x, 2), G["y"]), (round(x, 2), G["y"] + G["h"])))
            x += G["cell_w"]
        return G

    def set_grid_matrix(self, W: dict, G: dict) -> dict:
        """Set up matrix of records for each cell in  grid.
        For now, 2D only.
        :args:
        - W (dict) -- PG.WINDOWS
        - G (dict) -- PG.GRIDS
        :return:
        - matrix (dict) -- matrix of cell records
        """

        def create_matrix():
            """
            - assign key and data rec to all cells in matrix
            """
            cell_rec = {
                "is_ref": False,
                "fill": False,
                "fill_color": PygColors.CP_BLACK,
                "line_color": PygColors.CP_BLACK,
                "x": 0,
                "y": 0,
                "w": 0,
                "h": 0,
                "c_box": None,
                "img": Graphic,
                "map_data": {},
                "txt": "",
                "t_box": None,
            }
            r_n = G["row_cnt"] + 1
            c_n = G["col_cnt"] + 1
            matrix: dict = {}
            for r in range(0, r_n + 1):
                for c in range(0, c_n + 1):
                    key = f"{str(r).zfill(2)}, {str(c).zfill(2)}"
                    matrix[key] = cell_rec.copy()
                    matrix[key]["is_ref"] = (
                        True if (r in (0, r_n) or c in (0, c_n)) else False
                    )
            return (matrix, r_n, c_n)

        def set_matrix_data(matrix_data: tuple) -> dict:
            """
            - as col increases, increment x
            - as row increases, increment y
            - the "edge" cells show the row and column numbers
            - top and bottom rows display column numbers
            - left and right columns display row numbers
            """
            matrix, r_n, c_n = matrix_data
            x = G["x"]
            y = G["y"]
            for key, m_v in matrix.items():
                r, c = [int(k) for k in key.split(", ")]
                matrix[key]["x"] = round((x + (c * G["cell_w"])), 2)
                matrix[key]["y"] = round((y + (r * G["cell_h"])), 2)
                matrix[key]["w"] = G["cell_w"]
                matrix[key]["h"] = G["cell_h"]
                matrix[key]["c_box"] = pg.Rect(
                    matrix[key]["x"], matrix[key]["y"], G["cell_w"], G["cell_h"]
                )
                if m_v["is_ref"]:
                    matrix[key]["fill"] = True
                    matrix[key]["fill_color"] = PygColors.CP_WHITE
                    if (
                        (r == 0 and (c in (0, c_n)))
                        or (c == 0 and (r in (0, r_n)))
                        or (r == r_n and c == c_n)
                    ):
                        matrix[key]["txt"] = "."
                    elif r in (0, r_n):
                        matrix[key]["txt"] = str(c)
                    elif c in (0, c_n):
                        matrix[key]["txt"] = str(r)
            return matrix

        # set_grid_matrix()  main
        # ==================================
        matrix = set_matrix_data(create_matrix())

        return matrix

    def compute_map_scale(self, p_attr: dict, DSP: object):
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
        map = {"ln": dict(), "cl": dict()}
        # Evaluate map line lengths in kilometers
        map["ln"]["km"] = {
            "w": round(int(p_attr["distance"]["width"]["amt"])),
            "h": round(int(p_attr["distance"]["height"]["amt"])),
        }
        if map["ln"]["km"]["w"] > DSP.G_LNS_KM_W:
            err = f"Map km w {map['w']} > grid km w {DSP.G_LNS_KM_W}"
        if map["ln"]["km"]["h"] > DSP.G_LNS_KM_H:
            err = f"Map km h {map['h']} > grid km h {DSP.G_LNS_KM_H}"
        if err != "":
            raise ValueError(err)
        # Verified that the map rect is smaller than the grid rect.
        # Compute a ratio of map to grid.
        # Divide map km w, h by grid km w, h
        map["ln"]["ratio"] = {
            "w": round((map["ln"]["km"]["w"] / DSP.G_LNS_KM_W), 4),
            "h": round((map["ln"]["km"]["h"] / DSP.G_LNS_KM_H), 4),
        }
        # Compute map line dimensions in px
        # Multiply grid line px w, h by map ratio w, h
        map["ln"]["px"] = {
            "w": int(round(DSP.G_LNS_PX_W * map["ln"]["ratio"]["w"])),
            "h": int(round(DSP.G_LNS_PX_H * map["ln"]["ratio"]["h"])),
        }
        # The map rect needs to be centered in the grid rect.
        #  Compute the offset of the map rect from the grid rect.
        #  Compute topleft of the map in relation to topleft of the grid.
        #  The map top is offset from grid top by half the px difference
        #  between grid height and map height.
        #  The map left is offset from grid left by half the px difference
        #  between grid width and map width.
        # Then adjusted once more for offset of the grid from the window.
        map["ln"]["px"]["left"] = int(
            round((DSP.G_LNS_PX_W - map["ln"]["px"]["w"]) / 2) + DSP.GRID_OFFSET_X
        )
        map["ln"]["px"]["top"] = int(
            round((DSP.G_LNS_PX_H - map["ln"]["px"]["h"]) / 2) + (DSP.GRID_OFFSET_Y * 4)
        )  # not sure why, but I need this
        DSP.GRID["map"] = map


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

    def rect_contains(self, p_box_a: pg.Rect, p_box_b: pg.Rect) -> bool:
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

    def rect_overlaps(self, p_box_a: pg.Rect, p_box_b: pg.Rect) -> bool:
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

    def rect_borders(self, p_rect_a: pg.Rect, p_rect_b: pg.Rect) -> bool:
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

    def rect_same(self, p_rect_a: pg.Rect, p_rect_b: pg.Rect) -> bool:
        """Determine if rectangle A and rectangle B occupy exactly
        the same space.
        :args:
        - p_box_a: (pygame.Rect) rectangle A
        - p_box_b: (pygame.Rect) rectangle B
        """
        if (
            p_rect_a.topright == p_rect_b.topright
            and p_rect_a.bottomleft == p_rect_b.bottomleft
        ):
            return True
        else:
            return False
