import os
import sys
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
