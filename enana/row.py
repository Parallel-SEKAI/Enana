from typing import List, Optional, Tuple

from .container import Container
from .painter import Painter
from .typing import BorderRadius, Margin, Padding
from .widget import Widget


class Row(Container):
    """
    A horizontal layout widget that arranges its children in a row.

    Args:
        width: The width of the row.
        height: The height of the row.
        color: The background color of the row in RGBA format.
        padding: The padding inside the row.
        margin: The margin outside the row.
        border_radius: The border radius of the row.
        children: The list of child widgets to be arranged horizontally.
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
        Get the width of the row.

        If the width is not explicitly set, it will be calculated based on the sum of widths of its children.

        Returns:
            The width of the row.
        """
        if self._width is None:
            total_child_width = sum(
                (child.width for child in self._children), 0
            )
            self._width = (
                total_child_width
                + self._padding.horizontal
                + self._margin.horizontal
            )
        return self._width

    @property
    def height(self) -> int | float:
        """
        Get the height of the row.

        If the height is not explicitly set, it will be calculated based on the maximum height of its children.

        Returns:
            The height of the row.
        """
        if self._height is None:
            max_child_height = max(
                (child.height for child in self._children), default=0
            )
            self._height = (
                max_child_height
                + self._padding.vertical
                + self._margin.vertical
            )
        return self._height

    @property
    def painters(self) -> List[Painter]:
        """
        Get the list of painters for this row.

        Returns:
            A list of Painter objects that will be used to render this row.
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
        current_x = self._padding.left + self._margin.left
        for child in self._children:
            for painter in child.painters:
                painter.offset_x += current_x
                painter.offset_y += self._padding.top + self._margin.top
                painters.append(painter)
            current_x += child.width

        return painters
