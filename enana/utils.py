import os
import sys
import typing
from typing import Any, Tuple

from PIL import ImageFont


def always_true(x: int | float, y: int | float) -> bool:
    """
    始终返回True的函数，用于Painter的func参数

    Args:
        x: x坐标
        y: y坐标

    Returns:
        bool: 始终返回True
    """
    return True


def always_false(x: int | float, y: int | float) -> bool:
    """
    始终返回False的函数，用于Painter的func参数

    Args:
        x: x坐标
        y: y坐标

    Returns:
        bool: 始终返回False
    """
    return False


def hex_to_rgba(hex_color: int) -> Tuple[int, int, int, int]:
    """
    将16进制颜色字符串转换为RGBA元组

    Args:
        hex_color: 16进制颜色 0xRRGGBBAA

    Returns:
        Tuple[int, int, int, int]: RGBA元组，每个值范围为0-255
    """
    r = (hex_color >> 24) & 0xFF
    g = (hex_color >> 16) & 0xFF
    b = (hex_color >> 8) & 0xFF
    a = hex_color & 0xFF
    return r, g, b, a


def get_font(font: Any, font_size: int) -> ImageFont.FreeTypeFont:
    """
    获取字体对象，支持直接传入字体对象或字体名称

    Args:
        font: 字体对象或字体名称
        font_size: 字体大小

    Returns:
        ImageFont.FreeTypeFont: 字体对象
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
                # 在非Windows平台上，使用默认字体
                font_obj = ImageFont.load_default()
        except Exception:
            # 如果所有尝试都失败，回退到默认字体
            font_obj = ImageFont.load_default()
    return font_obj


if typing.TYPE_CHECKING:
    from .widget import Widget


def from_json(json: dict) -> "Widget":
    """
    从JSON字典创建Widget对象

    Args:
        json: JSON字典，符合widget.schema.json

    Returns:
        Widget: 对应的Widget对象
    """
    if "type" not in json:
        raise ValueError("Widget JSON must have a 'type' field")

    # 辅助函数：处理padding、margin和border_radius的不同格式
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
