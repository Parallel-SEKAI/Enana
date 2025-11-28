import time
from typing import Callable, Optional, Tuple


class Painter:
    def __init__(
        self,
        *,
        width: int | float,
        height: int | float,
        func: Callable[[int | float, int | float], bool],
        color: Tuple[int, int, int, int],
    ):
        self.width = width
        self.height = height
        self.func = func
        self.color = color
        self.z_index = time.time()
        self.offset_x: int | float = 0
        self.offset_y: int | float = 0

    def paint(self, x: int | float, y: int | float) -> bool:
        _x = x - self.offset_x
        _y = y - self.offset_y
        if _x < 0 or _x >= self.width or _y < 0 or _y >= self.height:
            return False
        return self.func(_x, _y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class TextPainter:
    def __init__(
        self,
        *,
        text: str,
        font: str = "Arial",
        font_size: int = 12,
        max_width: Optional[int] = None,
        color: Tuple[int, int, int, int],
    ):
        self.text = text
        self.max_width = max_width
        self.color = color

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"
