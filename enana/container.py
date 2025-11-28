from typing import List, Optional, Tuple

from .painter import Painter
from .typing import BorderRadius, Margin, Padding
from .widget import Widget


class Container(Widget):
    def __init__(
        self,
        *,
        width: Optional[int | float] = None,
        height: Optional[int | float] = None,
        color: Tuple[int, int, int, int] = (0, 0, 0, 0),
        padding: Optional[Padding] = None,
        margin: Optional[Margin] = None,
        border_radius: Optional[BorderRadius] = None,
        child: Optional[Widget] = None,
    ):
        self._width = self._original_width = width
        self._height = self._original_height = height
        self._color = color
        self._padding = padding or Padding.zero()
        self._margin = margin or Margin.zero()
        self._border_radius = border_radius or BorderRadius.zero()
        self._child = child

    def _paint_func(self, x: int | float, y: int | float) -> bool:
        assert self._width is not None
        assert self._height is not None
        width = self._original_width or (
            self._width - self._padding.horizontal
        )
        height = self._original_height or (
            self._height - self._padding.vertical
        )
        margin = self._margin
        border_radius = self._border_radius
        if (
            margin.left <= x < margin.left + width
            and margin.top <= y < margin.top + height
        ):
            if not border_radius:
                return True
            assert (
                border_radius.top_left
                == border_radius.top_right
                == border_radius.bottom_left
                == border_radius.bottom_right
            ), "border_radius must be the same on all sides"
            if (
                margin.left + border_radius.top_left
                <= x
                < margin.left + width - border_radius.top_right
            ):
                return True
            if (
                margin.top + border_radius.top_left
                <= y
                < margin.top + height - border_radius.bottom_left
            ):
                return True
            X = x - margin.left
            Y = y - margin.top
            if X <= border_radius.top_left and Y <= border_radius.top_left:
                return (X - border_radius.top_left) ** 2 + (
                    Y - border_radius.top_left
                ) ** 2 <= border_radius.top_left**2
            if (
                X >= width - border_radius.top_right
                and Y <= border_radius.top_right
            ):
                return (X - width + border_radius.top_right + 1) ** 2 + (
                    Y - border_radius.top_right
                ) ** 2 <= border_radius.top_right**2
            if (
                X >= width - border_radius.bottom_right
                and Y >= height - border_radius.bottom_right
            ):
                return (X - width + border_radius.bottom_right + 1) ** 2 + (
                    Y - height + border_radius.bottom_right + 1
                ) ** 2 <= border_radius.bottom_right**2
            if (
                X <= border_radius.bottom_left
                and Y >= height - border_radius.bottom_left
            ):
                return (X - border_radius.bottom_left) ** 2 + (
                    Y - height + border_radius.bottom_left + 1
                ) ** 2 <= border_radius.bottom_left**2
        return False

    @property
    def painters(self) -> List[Painter]:
        if self._width is None:
            if self._child is not None:
                self._width = (
                    self._child.width
                    + self._padding.horizontal
                    + self._margin.horizontal
                )
            else:
                self._width = (
                    self._padding.horizontal + self._margin.horizontal
                )
        if self._height is None:
            if self._child is not None:
                self._height = (
                    self._child.height
                    + self._padding.vertical
                    + self._margin.vertical
                )
            else:
                self._height = self._padding.vertical + self._margin.vertical

        painters = [
            Painter(
                width=self._width,
                height=self._height,
                func=self._paint_func,
                color=self._color,
            )
        ]
        if self._child is not None:
            for painter in self._child.painters:
                painter.offset_x += self._padding.left + self._margin.left
                painter.offset_y += self._padding.top + self._margin.top
                painters.append(painter)
        return painters
