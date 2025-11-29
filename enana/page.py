from math import ceil
from pathlib import Path
from typing import List, Tuple

from .generator import draw_image, draw_text, generate_image
from .painter import ImagePainter, TextPainter
from .widget import Widget


class DrawFunction:
    """
    A serializable drawing function class for executing drawing operations in a multiprocessing environment.
    """

    def __init__(self, painters: List, scale: float):
        """
        Initialize the DrawFunction.

        Args:
            painters: List of painters to use for drawing.
            scale: Scale factor for the drawing.
        """
        self.painters = painters
        self.scale = scale

    def __call__(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Execute the drawing operation.

        Args:
            x: x-coordinate
            y: y-coordinate

        Returns:
            RGBA color tuple
        """
        _x = x / self.scale
        _y = y / self.scale
        for painter in self.painters:
            if painter.paint(_x, _y) and all(painter.color):
                return painter.color
        return (0, 0, 0, 0)


class Page(Widget):
    """
    A page widget that serves as the root container for UI elements.
    """

    def __init__(self, *, child: Widget):
        """
        Initialize the Page.

        Args:
            child: The child widget to be rendered on the page.
        """
        self.child: Widget = child

    @classmethod
    def from_json(cls, json: dict) -> "Page":
        """
        Create a Page object from a JSON dictionary.

        Args:
            json: JSON dictionary, conforming to page.schema.json

        Returns:
            Page: The corresponding Page object
        """
        widget = super().from_json(json)
        assert isinstance(widget, Page)
        return widget

    def paint(self, *, scale: float = 1.0, filename: Path) -> None:
        """
        Paint the page to an image file.

        Args:
            scale: Scale factor for the image, defaults to 1.0.
            filename: Path to save the generated image.
        """
        painters = self.child.painters
        painters.sort(key=lambda x: x.z_index, reverse=True)

        # Create a serializable drawing function object
        draw = DrawFunction(painters, scale)

        # print("\n".join([repr(painter) for painter in painters]))

        generate_image(
            func=draw,
            width=ceil(self.child.width * scale),
            height=ceil(self.child.height * scale),
            filename=filename,
        )

        for text_painter in painters:
            if isinstance(text_painter, TextPainter):
                draw_text(
                    image=filename,
                    text=text_painter.text,
                    position=(
                        int(text_painter.offset_x * scale),
                        int(text_painter.offset_y * scale),
                    ),
                    color=text_painter.color,
                    font=text_painter.font,
                    font_size=int(text_painter.font_size * scale),
                    max_width=(
                        int(text_painter.max_width * scale)
                        if text_painter.max_width is not None
                        else None
                    ),
                )

        for image_painter in painters:
            if isinstance(image_painter, ImagePainter):
                draw_image(
                    image=filename,
                    image_painter=image_painter,
                    scale=scale,
                )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"
