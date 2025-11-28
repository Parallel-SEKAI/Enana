from typing import Tuple


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
