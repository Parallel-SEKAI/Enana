from math import ceil
from pathlib import Path
from typing import List, Tuple

from .generator import generate_image
from .widget import Widget


class DrawFunction:
    """
    可序列化的绘制函数类，用于在多进程环境中执行绘制操作
    """

    def __init__(self, painters: List, scale: float):
        self.painters = painters
        self.scale = scale

    def __call__(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        执行绘制操作

        Args:
            x: x坐标
            y: y坐标

        Returns:
            RGBA颜色元组
        """
        _x = x / self.scale
        _y = y / self.scale
        for painter in self.painters:
            if painter.paint(_x, _y):
                return painter.color
        return (0, 0, 0, 0)


class Page:
    def __init__(self, *, child: Widget):
        self.child: Widget = child

    def paint(self, *, scale: float = 1.0, filename: Path) -> None:
        painters = self.child.painters
        painters.sort(key=lambda x: x.z_index, reverse=True)

        # 创建可序列化的绘制函数对象
        draw = DrawFunction(painters, scale)

        print("\n".join([repr(painter) for painter in painters]))

        generate_image(
            func=draw,
            width=ceil(self.child.width * scale),
            height=ceil(self.child.height * scale),
            filename=filename,
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"
