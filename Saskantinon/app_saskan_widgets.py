"""
:module:    app_saskan_widgets.py
:author:    GM (genuinemerit @ pm.me)

Saskan Game module for managing console widgets,
 including buttons, text edits, etc.
"""

from copy import copy
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

import pygame as pg
from data_structs_pg import AppDisplay, PygColors

APD = AppDisplay()
CLR = PygColors()

pg.init()


class Widgets(object):
    """
    Decide if it is better to have a single class for all widgets,
    or if this is like the factory / consolidator of widget objectss.
    """

    def __init__(self):
        """Create WIDGETS object."""
        pass

    def create_widgets(
        self,
        WINDOWS: object,
        MAPS: object,
        GRIDS: object,
        p_map_name: str = None,
        p_grid_name: str = None,
    ):
        """ """
        pass

    def set_label_name(self, p_attr: dict):
        """Set text for a label (l) and name (n), but no type (t) value.
           Example: "type" attribute
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.APD.CONSOLE[n]["txt"] (list): strings to render as text
        """
        for t in [APD.DASH16, f"{p_attr['label']}:", f"  {p_attr['name']}"]:
            rec = copy(self.CONSOLE_REC)
            rec["txt"] = t
            self.CONSOLE_TEXT.append(rec)

    def set_label_name_type(self, p_attr: dict):
        """Set text for a label (l), a name (n), and a type (t).
           Example: "contained_by" attribute
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.APD.CONSOLE[n]["txt"] (list): strings to render as text
        """
        for t in [
            APD.DASH16,
            f"{p_attr['label']}:",
            f"  {p_attr['name']}",
            f"  {p_attr['type']}",
        ]:
            rec = copy(self.CONSOLE_REC)
            rec["txt"] = t
            self.CONSOLE_TEXT.append(rec)

    def set_proper_names(self, p_attr: dict):
        """Set text for a "name" attribute, which refers to proper
            names. Required value is indexed by "common". Optional
            set of names in various game languages or dialects have
            "other" in key.
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.APD.CONSOLE[n]["txt"] (list): strings to render as text
        """
        for t in [APD.DASH16, f"{p_attr['label']}:", f"  {p_attr['common']}"]:
            rec = copy(self.CONSOLE_REC)
            rec["txt"] = t
            self.CONSOLE_TEXT.append(rec)
        if "other" in p_attr.keys():
            for k, v in p_attr["other"].items():
                rec = copy(self.CONSOLE_REC)
                rec["txt"] = f"    {k}: {v}"
                self.CONSOLE_TEXT.append(rec)

    def set_map_attr(self, p_attr: dict):
        """Set text for a "map" attribute, referring to game-map data.
           Examples: "distance" or "location" expressed in
              kilometers, degrees, or other in-game measures
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.APD.CONSOLE[n]["txt"] (list): strings to render as text
        """
        ky = (
            "distance"
            if "distance" in p_attr.keys()
            else "location" if "location" in p_attr.keys() else None
        )
        if ky is not None:
            sub_k = (
                ["height", "width"]
                if ky == "distance"
                else ["top", "bottom", "left", "right"]
            )
            rec = copy(self.CONSOLE_REC)
            rec["txt"] = APD.DASH16
            self.CONSOLE_TEXT.append(rec)
            rec = copy(self.CONSOLE_REC)
            rec["txt"] = f"{p_attr[ky]['label']}:"
            self.CONSOLE_TEXT.append(rec)
            for s in sub_k:
                rec = copy(self.CONSOLE_REC)
                rec["txt"] = (
                    f"  {p_attr[ky][s]['label']}:  "
                    + f"{p_attr[ky][s]['amt']} "
                    + f"{p_attr[ky]['unit']}"
                )
                self.CONSOLE_TEXT.append(rec)

    def set_contains_attr(self, p_attr: dict):
        """Set text for a "contains" attribute, referring to things
            contained by another object.
            Examples: "sub-region", "movement" (i.e, movement paths)
        :attr:
        - p_attr (dict): name-value pairs to format
        :sets:
        - self.APD.CONSOLE[n]["txt"] (list): strings to render as text
        """
        rec = copy(self.CONSOLE_REC)
        rec["txt"] = APD.DASH16
        self.CONSOLE_TEXT.append(rec)
        rec = copy(self.CONSOLE_REC)
        rec["txt"] = f"{p_attr['label']}:"
        self.CONSOLE_TEXT.append(rec)

        if "sub-region" in p_attr.keys():
            rec = copy(self.CONSOLE_REC)
            rec["txt"] = f"  {p_attr['sub-region']['label']}:"
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
            attr = {k: v for k, v in p_attr["movement"].items() if k != "label"}
            for _, v in attr.items():
                rec = copy(self.CONSOLE_REC)
                rec["txt"] = f"    {v['label']}:"
                self.CONSOLE_TEXT.append(rec)
                for n in v["names"]:
                    rec = copy(self.CONSOLE_REC)
                    rec["txt"] = f"      {n}"
                    self.CONSOLE_TEXT.append(rec)

    # Data rendering methods for APD.CONSOLE
    # ==================================
    def render_text_lines(self):
        """
        Store rendering objects for lines of APD.CONSOLE text.
        After rendering the img from txt, set the box for the img.
        Then adjust topleft of the box according to line number.
        """
        print("render_text_lines()...")

        x = APD.CONSOLE_TTL_BOX.x
        y = APD.CONSOLE_TTL_BOX.y + APD.FONT_MED_SZ

        for ix, val in enumerate(self.CONSOLE_TEXT):
            txt = val["txt"]
            self.CONSOLE_TEXT[ix]["img"] = APD.F_SANS_TINY.render(
                txt, True, CLR.CP_BLUEPOWDER, CLR.CP_BLACK
            )
            self.CONSOLE_TEXT[ix]["box"] = self.CONSOLE_TEXT[ix]["img"].get_rect()
            self.CONSOLE_TEXT[ix]["box"].topleft = (
                x,
                y + ((APD.FONT_TINY_SZ + 2) * (ix + 1)),
            )

    def set_console_text(self):
        """Format text lines for display in APD.CONSOLE.
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
        pass

        """
        if self.DATASRC["catg"] == "geo":
            ci = FM.G[self.DATASRC["catg"]][self.DATASRC["item"]]

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
        """


class TextInput(pg.sprite.Sprite):
    """Define and handle a text input widget.
    Use this to get directions, responses from player
    until I have graphic or voice methods available.
    Expand on this to create GUI control buttons, etc.

    Move this to app_saskan_widgets.py

    @DEV:
    - Expand the data model and DB to hold widgets:
    - text input
    - buttons
    - text display
    - video display and so on
    """

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
        # self.t_rect = REC.make_rect(p_y, p_x, p_w, p_h)
        # self.t_box = self.t_rect["box"]
        self.t_value = ""
        self.t_font = APD.F_FIXED_LG
        self.t_color = CLR.CP_GREEN
        self.text = self.t_font.render(self.t_value, True, self.t_color)
        self.is_selected = False

    def update_text(self, p_text: str):
        """Update text value.
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
        """Return True if mouse is clicked in the widget."""
        if self.t_box.collidepoint(p_mouse_loc):
            self.is_selected = not (self.is_selected)
            return True
        return False

    def draw(self):
        """Place text in the widget, centered in the box.
        This has the effect of expanding the text as it is typed
        in both directions. Draw the surface (box). Then blit the text.
        """
        self.pos = self.text.get_rect(
            center=(self.t_box.x + self.t_box.w / 2, self.t_box.y + self.t_box.h / 2)
        )
        if self.is_selected:
            pg.draw.rect(APD.WIN, CLR.CP_BLUEPOWDER, self.t_box, 2)
        else:
            pg.draw.rect(APD.WIN, CLR.CP_BLUE, self.t_box, 2)
        APD.WIN.blit(self.text, self.pos)


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
        self.current = None  # ID currently-selected text input widget.
