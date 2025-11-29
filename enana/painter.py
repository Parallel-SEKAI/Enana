import time
from typing import Callable, Optional, Tuple

from PIL import Image as PILImage

from .utils import always_false


class Painter:
    """
    Base class for all painters, responsible for rendering pixels.
    """

    def __init__(
        self,
        *,
        width: int | float,
        height: int | float,
        func: Callable[[int | float, int | float], bool],
        color: Tuple[int, int, int, int],
    ):
        """
        Initialize the Painter.

        Args:
            width: The width of the painting area.
            height: The height of the painting area.
            func: A function that determines if a pixel should be painted.
            color: The RGBA color to use for painting.
        """
        self.width = width
        self.height = height
        self.func = func
        self.color = color
        self.z_index = time.time()
        self.offset_x: int | float = 0
        self.offset_y: int | float = 0

    def paint(self, x: int | float, y: int | float) -> bool:
        """
        Determine if a pixel at the given coordinates should be painted.

        Args:
            x: The x-coordinate.
            y: The y-coordinate.

        Returns:
            True if the pixel should be painted, False otherwise.
        """
        _x = x - self.offset_x
        _y = y - self.offset_y
        if _x < 0 or _x >= self.width or _y < 0 or _y >= self.height:
            return False
        return self.func(_x, _y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class TextPainter(Painter):
    """
    Painter for rendering text.
    """

    def __init__(
        self,
        *,
        text: str,
        font: str = "Arial",
        font_size: int = 12,
        max_width: Optional[int] = None,
        color: Tuple[int, int, int, int],
    ):
        """
        Initialize the TextPainter.

        Args:
            text: The text to render.
            font: The font name to use.
            font_size: The font size in points.
            max_width: The maximum width before wrapping occurs.
            color: The RGBA color of the text.
        """
        super().__init__(
            width=0, height=0, func=always_false, color=(0, 0, 0, 0)
        )
        self.text = text
        self.font = font
        self.font_size = font_size
        self.max_width = max_width
        self.color = color

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class ImagePainter(Painter):
    """
    Painter for rendering images.
    """

    def __init__(
        self,
        *,
        image: PILImage.Image,
        width: int | float,
        height: int | float,
        size: Optional[object] = None,
    ):
        """
        Initialize the ImagePainter.

        Args:
            image: The PIL Image object to render.
            width: The width of the image area.
            height: The height of the image area.
            size: The sizing mode for the image.
        """
        from .image import ImageSize

        super().__init__(
            width=width,
            height=height,
            func=always_false,
            color=(0, 0, 0, 0),
        )
        self.image = image
        # Handle different types of size parameters
        if isinstance(size, str):
            self.size = ImageSize(size)
        elif isinstance(size, ImageSize):
            self.size = size
        else:
            self.size = ImageSize.DEFAULT
        # Remove the call to _resize_image during initialization
        # self._resized_image = self._resize_image()

    def _resize_image(self, scale: float = 1.0) -> PILImage.Image:
        """
        Resize the image based on the size parameter and scale factor.

        Args:
            scale: The scaling factor.

        Returns:
            PILImage.Image: The resized image object.
        """
        from .image import ImageSize

        img_width, img_height = self.image.size
        # Apply scale factor to target width and height
        target_width, target_height = self.width * scale, self.height * scale

        if self.size == ImageSize.DEFAULT:
            # Do not resize, return original image
            return self.image.resize(
                (int(img_width * scale), int(img_height * scale)),
                PILImage.Resampling.LANCZOS,
            )
        elif self.size == ImageSize.COVER:
            # Maintain aspect ratio, cover the entire target area
            scale_factor = max(
                target_width / img_width, target_height / img_height
            )
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            resized = self.image.resize(
                (new_width, new_height), PILImage.Resampling.LANCZOS
            )
            # Crop to target size
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height
            return resized.crop((left, top, right, bottom))
        elif self.size == ImageSize.CONTAIN:
            # Maintain aspect ratio, fit within target area
            scale_factor = min(
                target_width / img_width, target_height / img_height
            )
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            return self.image.resize(
                (new_width, new_height), PILImage.Resampling.LANCZOS
            )
        else:
            return self.image.resize(
                (int(img_width * scale), int(img_height * scale)),
                PILImage.Resampling.LANCZOS,
            )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"
