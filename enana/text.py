from typing import List, Optional, Tuple

from PIL import Image, ImageDraw

from .painter import Painter, TextPainter
from .utils import get_font
from .widget import Widget


class Text(Widget):
    """
    A text widget for displaying text content.

    Args:
        text: The text content to display.
        font: The font name to use.
        font_size: The font size in points.
        max_width: The maximum width of the text before wrapping.
        color: The text color in RGBA format.
    """

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
        # Calculate the actual text width and height
        self._width, self._height = self._calculate_text_size()

    def _calculate_text_size(self) -> Tuple[int, int]:
        """
        Calculate the actual width and height of the text, supporting automatic line wrapping.

        Returns:
            Tuple[int, int]: The actual width and height of the text.
        """
        # Create a temporary image for measuring text
        temp_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(temp_img)

        # Get font object
        font_obj = get_font(self._font, self._font_size)

        # Calculate single line height
        line_height = int(
            draw.textbbox((0, 0), "A", font=font_obj)[3]
            - draw.textbbox((0, 0), "A", font=font_obj)[1]
        )
        line_height = int(line_height * 1.5)  # Line height coefficient

        # If no max_width is set or text width is less than max_width, return single line size
        if self._max_width is None:
            bbox = draw.textbbox((0, 0), self._text, font=font_obj)
            width = int(bbox[2] - bbox[0])
            height = line_height
            return width, height

        # Implement automatic line wrapping
        words = self._text.split()
        if not words:
            return 0, line_height

        lines = []
        current_line = words[0]

        for word in words[1:]:
            # Test the width of current line plus the next word
            test_line = f"{current_line} {word}"
            test_bbox = draw.textbbox((0, 0), test_line, font=font_obj)
            test_width = int(test_bbox[2] - test_bbox[0])

            if test_width <= self._max_width:
                # If adding the next word still fits within the max_width, continue
                current_line = test_line
            else:
                # Otherwise, end the current line and start a new one
                lines.append(current_line)
                current_line = word

        # Add the last line
        lines.append(current_line)

        # Calculate final width and height
        final_width = self._max_width
        final_height = len(lines) * line_height

        return final_width, final_height

    @property
    def painters(self) -> List[Painter]:
        """
        Get the list of painters for this text widget.

        Returns:
            A list of Painter objects that will be used to render this text.
        """
        return [
            TextPainter(
                text=self._text,
                font=self._font,
                font_size=self._font_size,
                max_width=self._max_width,
                color=self._color,
            )
        ]
