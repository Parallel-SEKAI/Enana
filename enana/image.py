import base64
import io
from enum import Enum
from typing import List

from PIL import Image as PILImage

from .painter import Painter
from .widget import Widget


class ImageSize(Enum):
    """
    Enum for image sizing modes.

    - COVER: Resize the image to cover the entire container, cropping if necessary.
    - CONTAIN: Resize the image to fit within the container, maintaining aspect ratio.
    - DEFAULT: Use the original image size without resizing.
    """

    COVER = "cover"
    CONTAIN = "contain"
    DEFAULT = "default"


class Image(Widget):
    """
    An image widget for displaying images.

    Args:
        url: The URL of the image, supports http(s), file, and base64 formats.
        width: The width of the image container.
        height: The height of the image container.
        size: The image sizing mode, defaults to DEFAULT.
    """

    def __init__(
        self,
        *,
        url: str,
        width: int | float,
        height: int | float,
        size: ImageSize = ImageSize.DEFAULT,
    ):
        self._url = url
        self._width = width
        self._height = height
        self._size = size
        self._image = self._load_image()

    def _load_image(self) -> PILImage.Image:
        """
        Load an image from various sources.

        Supports http(s) URLs, local files, and base64 encoded images.

        Returns:
            PILImage.Image: The loaded image object.
        """
        if self._url.startswith("http://") or self._url.startswith("https://"):
            # Load image from network
            import requests

            response = requests.get(self._url)
            response.raise_for_status()
            return PILImage.open(io.BytesIO(response.content)).convert("RGBA")
        elif self._url.startswith("file://"):
            # Load image from local file
            file_path = self._url[7:]
            return PILImage.open(file_path).convert("RGBA")
        elif self._url.startswith("data:image/"):
            # Load image from base64
            base64_data = self._url.split(",")[1]
            image_data = base64.b64decode(base64_data)
            return PILImage.open(io.BytesIO(image_data)).convert("RGBA")
        else:
            # Default to local file path
            return PILImage.open(self._url).convert("RGBA")

    @property
    def painters(self) -> List[Painter]:
        """
        Get the list of painters for this image widget.

        Returns:
            A list of Painter objects that will be used to render this image.
        """
        from .painter import ImagePainter

        # Use type assertion to ensure type safety
        width: int | float = self._width  # type: ignore
        height: int | float = self._height  # type: ignore

        return [
            ImagePainter(
                image=self._image,
                width=width,
                height=height,
                size=self._size,
            )
        ]
