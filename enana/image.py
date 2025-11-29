import base64
import io
from enum import Enum
from typing import List

from PIL import Image as PILImage

from .painter import Painter
from .widget import Widget


class ImageSize(Enum):
    COVER = "cover"
    CONTAIN = "contain"
    DEFAULT = "default"


class Image(Widget):
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
        加载图片，支持http(s)、file和base64格式

        Returns:
            PILImage.Image: 加载的图片对象
        """
        if self._url.startswith("http://") or self._url.startswith("https://"):
            # 从网络加载图片
            import requests

            response = requests.get(self._url)
            response.raise_for_status()
            return PILImage.open(io.BytesIO(response.content)).convert("RGBA")
        elif self._url.startswith("file://"):
            # 从本地文件加载图片
            file_path = self._url[7:]
            return PILImage.open(file_path).convert("RGBA")
        elif self._url.startswith("data:image/"):
            # 从base64加载图片
            base64_data = self._url.split(",")[1]
            image_data = base64.b64decode(base64_data)
            return PILImage.open(io.BytesIO(image_data)).convert("RGBA")
        else:
            # 默认当作本地文件路径处理
            return PILImage.open(self._url).convert("RGBA")

    @property
    def painters(self) -> List[Painter]:
        from .painter import ImagePainter

        # 使用类型断言确保类型安全
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
