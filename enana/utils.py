import os
import sys
import typing
from typing import Any, Tuple

from PIL import ImageFont


def always_true(x: int | float, y: int | float) -> bool:
    """
    A function that always returns True, used for Painter's func parameter

    Args:
        x: x-coordinate
        y: y-coordinate

    Returns:
        bool: Always returns True
    """
    return True


def always_false(x: int | float, y: int | float) -> bool:
    """
    A function that always returns False, used for Painter's func parameter

    Args:
        x: x-coordinate
        y: y-coordinate

    Returns:
        bool: Always returns False
    """
    return False


def hex_to_rgba(hex_color: int) -> Tuple[int, int, int, int]:
    """
    Convert a hexadecimal color integer to an RGBA tuple

    Args:
        hex_color: Hexadecimal color in 0xRRGGBBAA format

    Returns:
        Tuple[int, int, int, int]: RGBA tuple with values ranging from 0-255
    """
    r = (hex_color >> 24) & 0xFF
    g = (hex_color >> 16) & 0xFF
    b = (hex_color >> 8) & 0xFF
    a = hex_color & 0xFF
    return r, g, b, a


def get_font(font: Any, font_size: int) -> ImageFont.FreeTypeFont:
    """
    Get a font object, supporting both direct font objects and font names

    Args:
        font: Font object or font name
        font_size: Font size in points

    Returns:
        ImageFont.FreeTypeFont: Font object
    """
    font_obj: Any
    try:
        # Check if font is already a font object
        if hasattr(font, "getbbox"):
            # Already a font object, use it directly
            font_obj = font
        else:
            # Try to load the specified font
            font_obj = ImageFont.truetype(font, font_size)
    except OSError:
        # If the specified font fails, try to find a fallback font
        try:
            # Try common Windows fonts
            if sys.platform == "win32":
                # Try to find Arial or a similar font
                font_files = [
                    "arial.ttf",
                    "calibri.ttf",
                    "times.ttf",
                    "verdana.ttf",
                ]
                font_obj = None
                for font_file in font_files:
                    try:
                        font_path = os.path.join(
                            r"C:\Windows\Fonts", font_file
                        )
                        font_obj = ImageFont.truetype(font_path, font_size)
                        break
                    except OSError:
                        continue
                # If no Windows font found, use default font
                if font_obj is None:
                    font_obj = ImageFont.load_default()
            else:
                # On non-Windows platforms, use the default font
                font_obj = ImageFont.load_default()
        except Exception:
            # If all attempts fail, fall back to the default font
            font_obj = ImageFont.load_default()
    return font_obj


if typing.TYPE_CHECKING:
    from .widget import Widget


def from_json(json: dict) -> "Widget":
    """
    Create a Widget object from a JSON dictionary.

    Args:
        json: JSON dictionary, conforming to widget.schema.json

    Returns:
        Widget: The corresponding Widget object
    """
    if "type" not in json:
        raise ValueError("Widget JSON must have a 'type' field")

    # Helper functions: Handle different formats for padding, margin, and border_radius
    def _parse_padding(value):
        from .typing import Padding

        if isinstance(value, dict):
            return Padding(
                top=value.get("top", 0),
                right=value.get("right", 0),
                bottom=value.get("bottom", 0),
                left=value.get("left", 0),
            )
        elif isinstance(value, (int, float)):
            return Padding(
                top=value,
                right=value,
                bottom=value,
                left=value,
            )
        elif isinstance(value, list) and len(value) == 4:
            return Padding(
                top=value[0],
                right=value[1],
                bottom=value[2],
                left=value[3],
            )
        return None

    def _parse_margin(value):
        from .typing import Margin

        if isinstance(value, dict):
            return Margin(
                top=value.get("top", 0),
                right=value.get("right", 0),
                bottom=value.get("bottom", 0),
                left=value.get("left", 0),
            )
        elif isinstance(value, (int, float)):
            return Margin(
                top=value,
                right=value,
                bottom=value,
                left=value,
            )
        elif isinstance(value, list) and len(value) == 4:
            return Margin(
                top=value[0],
                right=value[1],
                bottom=value[2],
                left=value[3],
            )
        return None

    def _parse_border_radius(value):
        from .typing import BorderRadius

        if isinstance(value, dict):
            return BorderRadius(
                top_left=value.get("top_left", 0),
                top_right=value.get("top_right", 0),
                bottom_right=value.get("bottom_right", 0),
                bottom_left=value.get("bottom_left", 0),
            )
        elif isinstance(value, (int, float)):
            return BorderRadius(
                top_left=value,
                top_right=value,
                bottom_right=value,
                bottom_left=value,
            )
        elif isinstance(value, list) and len(value) == 4:
            return BorderRadius(
                top_left=value[0],
                top_right=value[1],
                bottom_right=value[2],
                bottom_left=value[3],
            )
        return None

    if json["type"] == "Page":
        from .page import Page

        if "child" not in json:
            raise ValueError("Page widget must have a child widget")
        return Page(
            child=from_json(json["child"]),
        )
    elif json["type"] == "Container":
        from .container import Container

        return Container(
            width=json.get("width"),
            height=json.get("height"),
            color=tuple(json.get("color", (0, 0, 0, 0))),
            padding=(
                _parse_padding(json["padding"]) if "padding" in json else None
            ),
            margin=_parse_margin(json["margin"]) if "margin" in json else None,
            border_radius=(
                _parse_border_radius(json["border_radius"])
                if "border_radius" in json
                else None
            ),
            child=from_json(json["child"]) if "child" in json else None,
        )
    elif json["type"] == "Column":
        from .column import Column

        if "children" not in json:
            raise ValueError("Column widget must have children")
        return Column(
            width=json.get("width"),
            height=json.get("height"),
            color=tuple(json.get("color", (0, 0, 0, 0))),
            padding=(
                _parse_padding(json["padding"]) if "padding" in json else None
            ),
            margin=_parse_margin(json["margin"]) if "margin" in json else None,
            border_radius=(
                _parse_border_radius(json["border_radius"])
                if "border_radius" in json
                else None
            ),
            children=[from_json(child) for child in json["children"]],
        )
    elif json["type"] == "Row":
        from .row import Row

        if "children" not in json:
            raise ValueError("Row widget must have children")
        return Row(
            width=json.get("width"),
            height=json.get("height"),
            color=tuple(json.get("color", (0, 0, 0, 0))),
            padding=(
                _parse_padding(json["padding"]) if "padding" in json else None
            ),
            margin=_parse_margin(json["margin"]) if "margin" in json else None,
            border_radius=(
                _parse_border_radius(json["border_radius"])
                if "border_radius" in json
                else None
            ),
            children=[from_json(child) for child in json["children"]],
        )
    elif json["type"] == "Text":
        from .text import Text

        if "text" not in json:
            raise ValueError("Text widget must have text content")
        return Text(
            text=json["text"],
            font=json.get("font", "Arial"),
            font_size=json.get("font_size", 12),
            max_width=json.get("max_width"),
            color=tuple(json.get("color", (0, 0, 0, 255))),
        )
    elif json["type"] == "Image":
        from .image import Image, ImageSize

        if "url" not in json:
            raise ValueError("Image widget must have a url")
        if "width" not in json:
            raise ValueError("Image widget must have a width")
        if "height" not in json:
            raise ValueError("Image widget must have a height")

        size = json.get("size", "default")
        size_enum = (
            ImageSize(size.lower())
            if isinstance(size, str)
            else ImageSize.DEFAULT
        )

        return Image(
            url=json["url"],
            width=json["width"],
            height=json["height"],
            size=size_enum,
        )
    raise ValueError(f"Unknown widget type: {json['type']}")
