"""
:module:    data_image_type.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
Define image types.
"""

from pprint import pformat as pf    # noqa: F401
from pprint import pprint as pp     # noqa: F401


class ImageType(object):
    """Types of images.
    Reference class attributes directly.
    No need to instantiate this class."""
    JPG = "jpg"
    PNG = "png"
    GIF = "gif"
    BMP = "bmp"
    SVG = "svg"
    TIF = "tif"
    ICO = "ico"
