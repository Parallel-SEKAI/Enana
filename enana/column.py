from typing import List, Optional, Tuple

from .container import Container
from .painter import Painter
from .typing import BorderRadius, Margin, Padding
from .widget import Widget


class Column(Container):
    """
    A vertical layout widget that arranges its children in a column.

    Args:
        width: The width of the column.
        height: The height of the column.
        color: The background color of the column in RGBA format.
        padding: The padding inside the column.
        margin: The margin outside the column.
        border_radius: The border radius of the column.
        children: The list of child widgets to be arranged vertically.
    """

    def __init__(
        self,
        *,
        width: Optional[int | float] = None,
        height: Optional[int | float] = None,
        color: Tuple[int, int, int, int] = (0, 0, 0, 0),
        padding: Optional[Padding] = None,
        margin: Optional[Margin] = None,
        border_radius: Optional[BorderRadius] = None,
        children: Optional[List[Widget]] = None,
    ):
        super().__init__(
            width=width,
            height=height,
            color=color,
            padding=padding,
            margin=margin,
            border_radius=border_radius,
            child=None,
        )
        self._children = children or []

    @property
    def width(self) -> int | float:
        """
        Get the width of the column.

        If the width is not explicitly set, it will be calculated based on the maximum width of its children.

        Returns:
            The width of the column.
        """
        if self._width is None:
            max_child_width = max(
                (child.width for child in self._children), default=0
            )
            self._width = (
                max_child_width
                + self._padding.horizontal
                + self._margin.horizontal
            )
        return self._width

    @property
    def height(self) -> int | float:
        """
        Get the height of the column.

        If the height is not explicitly set, it will be calculated based on the sum of heights of its children.

        Returns:
            The height of the column.
        """
        if self._height is None:
            total_child_height = sum(
                (child.height for child in self._children), 0
            )
            self._height = (
                total_child_height
                + self._padding.vertical
                + self._margin.vertical
            )
        return self._height

    @property
    def painters(self) -> List[Painter]:
        """
        Get the list of painters for this column.

        Returns:
            A list of Painter objects that will be used to render this column.
        """
        # Ensure dimensions are calculated
        width = self.width
        height = self.height

        # Create container painter
        painters = [
            Painter(
                width=width,
                height=height,
                func=self._paint_func,
                color=self._color,
            )
        ]

        # Calculate position for each child and add their painters
        current_y = self._padding.top + self._margin.top
        for child in self._children:
            for painter in child.painters:
                painter.offset_x += self._padding.left + self._margin.left
                painter.offset_y += current_y
                painters.append(painter)
            current_y += child.height

        return painters
