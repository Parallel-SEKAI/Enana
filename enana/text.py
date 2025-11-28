from typing import List, Optional, Tuple

from .painter import Painter, TextPainter
from .widget import Widget


class Text(Widget):
    def __init__(
        self,
        *,
        text: str,
        font: str = "Arial",
        font_size: int = 12,
        max_width: Optional[int] = None,
        color: Tuple[int, int, int, int] = (0, 0, 0, 255),
    ):
        self._text = text
        self._font = font
        self._font_size = font_size
        self._max_width = max_width
        self._color = color

    @property
    def painters(self) -> List[Painter]:
        return []

    @property
    def text_painters(self) -> List[TextPainter]:
        return [
            TextPainter(
                text=self._text,
                font=self._font,
                font_size=self._font_size,
                max_width=self._max_width,
                color=self._color,
            )
        ]
