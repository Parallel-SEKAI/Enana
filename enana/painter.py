import time
from typing import Callable, Optional, Tuple

from PIL import Image as PILImage

from .utils import always_false


class Painter:
    def __init__(
        self,
        *,
        width: int | float,
        height: int | float,
        func: Callable[[int | float, int | float], bool],
        color: Tuple[int, int, int, int],
    ):
        self.width = width
        self.height = height
        self.func = func
        self.color = color
        self.z_index = time.time()
        self.offset_x: int | float = 0
        self.offset_y: int | float = 0

    def paint(self, x: int | float, y: int | float) -> bool:
        _x = x - self.offset_x
        _y = y - self.offset_y
        if _x < 0 or _x >= self.width or _y < 0 or _y >= self.height:
            return False
        return self.func(_x, _y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class TextPainter(Painter):
    def __init__(
        self,
        *,
        text: str,
        font: str = "Arial",
        font_size: int = 12,
        max_width: Optional[int] = None,
        color: Tuple[int, int, int, int],
    ):
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
    def __init__(
        self,
        *,
        image: PILImage.Image,
        width: int | float,
        height: int | float,
        size: Optional[object] = None,
    ):
        from .image import ImageSize

        super().__init__(
            width=width,
            height=height,
            func=always_false,
            color=(0, 0, 0, 0),
        )
        self.image = image
        # 处理不同类型的size参数
        if isinstance(size, str):
            self.size = ImageSize(size)
        elif isinstance(size, ImageSize):
            self.size = size
        else:
            self.size = ImageSize.DEFAULT
        # 移除初始化时对_resize_image方法的调用
        # self._resized_image = self._resize_image()

    def _resize_image(self, scale: float = 1.0) -> PILImage.Image:
        """
        根据size参数和scale因子调整图片大小

        Args:
            scale: 缩放比例

        Returns:
            PILImage.Image: 调整大小后的图片对象
        """
        from .image import ImageSize

        img_width, img_height = self.image.size
        # 应用scale因子到目标宽度和高度
        target_width, target_height = self.width * scale, self.height * scale

        if self.size == ImageSize.DEFAULT:
            # 不调整大小，直接返回原图
            return self.image.resize(
                (int(img_width * scale), int(img_height * scale)),
                PILImage.Resampling.LANCZOS,
            )
        elif self.size == ImageSize.COVER:
            # 保持比例，覆盖整个目标区域
            scale_factor = max(
                target_width / img_width, target_height / img_height
            )
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            resized = self.image.resize(
                (new_width, new_height), PILImage.Resampling.LANCZOS
            )
            # 裁剪到目标大小
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            right = left + target_width
            bottom = top + target_height
            return resized.crop((left, top, right, bottom))
        elif self.size == ImageSize.CONTAIN:
            # 保持比例，适应目标区域
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
