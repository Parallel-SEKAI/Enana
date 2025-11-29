from typing import List, Optional, Tuple

from PIL import Image, ImageDraw

from .painter import Painter, TextPainter
from .utils import get_font
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
        # 获取实际文本宽度和高度
        self._width, self._height = self._calculate_text_size()

    def _calculate_text_size(self) -> Tuple[int, int]:
        """
        计算文本的实际宽度和高度，支持自动换行

        Returns:
            Tuple[int, int]: 文本的实际宽度和高度
        """
        # 创建一个临时图像用于测量文本
        temp_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(temp_img)

        # 获取字体对象
        font_obj = get_font(self._font, self._font_size)

        # 计算单行文本高度
        line_height = int(
            draw.textbbox((0, 0), "A", font=font_obj)[3]
            - draw.textbbox((0, 0), "A", font=font_obj)[1]
        )
        line_height = int(line_height * 1.5)  # 行高系数

        # 如果没有设置max_width或文本宽度小于max_width，直接返回单行尺寸
        if self._max_width is None:
            bbox = draw.textbbox((0, 0), self._text, font=font_obj)
            width = int(bbox[2] - bbox[0])
            height = line_height
            return width, height

        # 实现自动换行
        words = self._text.split()
        if not words:
            return 0, line_height

        lines = []
        current_line = words[0]

        for word in words[1:]:
            # 测试当前行加上下一个单词的宽度
            test_line = f"{current_line} {word}"
            test_bbox = draw.textbbox((0, 0), test_line, font=font_obj)
            test_width = int(test_bbox[2] - test_bbox[0])

            if test_width <= self._max_width:
                # 如果加上下一个单词后宽度仍在限制内，继续添加
                current_line = test_line
            else:
                # 否则，当前行结束，开始新行
                lines.append(current_line)
                current_line = word

        # 添加最后一行
        lines.append(current_line)

        # 计算最终宽度和高度
        final_width = self._max_width
        final_height = len(lines) * line_height

        return final_width, final_height

    @property
    def painters(self) -> List[Painter]:
        return [
            TextPainter(
                text=self._text,
                font=self._font,
                font_size=self._font_size,
                max_width=self._max_width,
                color=self._color,
            )
        ]
