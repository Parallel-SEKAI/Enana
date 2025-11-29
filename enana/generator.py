import multiprocessing
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple, Union

from PIL import Image, ImageDraw

from .painter import ImagePainter

try:
    # Get the number of CPU cores for multiprocessing
    CPU_COUNT = multiprocessing.cpu_count()
except NotImplementedError:
    # Default to 4 if the number of CPU cores cannot be determined
    CPU_COUNT = 4


def _generate_chunk(
    func: Callable[[int, int], Tuple[int, int, int, int]],
    y_start: int,
    y_end: int,
    width: int,
) -> List[Tuple[int, int, int, int]]:
    """
    Generates pixel data for a chunk of an image.

    Args:
        func: A function that takes x and y coordinates and returns an RGBA tuple.
        y_start: The starting y-coordinate of the chunk.
        y_end: The ending y-coordinate of the chunk.
        width: The width of the image.

    Returns:
        A list containing the RGBA values of all pixels in the chunk.
    """
    chunk_data = []
    # Iterate over each pixel in the chunk
    for y in range(y_start, y_end):
        for x in range(width):
            # Call the function to generate pixel data and add it to the list
            chunk_data.append(func(x, y))
    return chunk_data


def generate_image(
    func: Callable[[int, int], Tuple[int, int, int, int]],
    width: int,
    height: int,
    filename: Path,
) -> None:
    """
    Creates and saves an image in parallel using multiprocessing.

    Args:
        func: A function that takes x and y coordinates and returns an RGBA tuple.
        width: The width of the image.
        height: The height of the image.
        filename: The file path to save the image to.
    """
    # Create a process pool
    with multiprocessing.Pool(CPU_COUNT) as pool:
        # Calculate the height of each chunk
        chunk_size = height // CPU_COUNT
        # Create a list of tasks, where each task processes a chunk of the image
        tasks = [
            (func, i * chunk_size, (i + 1) * chunk_size, width)
            for i in range(CPU_COUNT)
        ]
        # Ensure the last task processes up to the bottom of the image
        tasks[-1] = (func, tasks[-1][1], height, width)
        # Execute the tasks in parallel using starmap
        results = pool.starmap(_generate_chunk, tasks)
    # Combine the pixel data from all chunks into a single list
    pixel_data = [pixel for chunk in results for pixel in chunk]
    # Create a new RGBA image
    img = Image.new("RGBA", (width, height))
    # Put the pixel data into the image
    img.putdata(pixel_data)
    # Save the image
    img.save(filename)


def draw_text(
    image: Path,
    text: str,
    position: Tuple[int, int],
    color: Tuple[int, int, int, int],
    font: Union[str, Any] = "Arial",
    font_size: int = 12,
    max_width: Optional[int] = None,
):
    # Open the image
    img = Image.open(image)
    # Get the image size
    width, height = img.size
    # Create a font object
    from .utils import get_font

    font_obj = get_font(font, font_size)
    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # 处理自动换行
    if max_width is None:
        # 如果没有设置max_width，直接绘制文本
        draw.text(position, text, font=font_obj, fill=color)
    else:
        # 实现自动换行绘制
        x, y = position

        # 计算单行文本高度
        line_height = int(
            draw.textbbox((0, 0), "A", font=font_obj)[3]
            - draw.textbbox((0, 0), "A", font=font_obj)[1]
        )
        line_height = int(line_height * 1.5)  # 行高系数

        # 分割单词
        words = text.split()
        if not words:
            return

        current_line = words[0]

        for word in words[1:]:
            # 测试当前行加上下一个单词的宽度
            test_line = f"{current_line} {word}"
            test_bbox = draw.textbbox((0, 0), test_line, font=font_obj)
            test_width = int(test_bbox[2] - test_bbox[0])

            if test_width <= max_width:
                # 如果加上下一个单词后宽度仍在限制内，继续添加
                current_line = test_line
            else:
                # 否则，绘制当前行并开始新行
                draw.text((x, y), current_line, font=font_obj, fill=color)
                y += line_height
                current_line = word

        # 绘制最后一行
        draw.text((x, y), current_line, font=font_obj, fill=color)

    # Save the image
    img.save(image)


def draw_image(
    image: Path,
    image_painter: "ImagePainter",
    scale: float,
):
    """
    在图片上绘制另一个图片

    Args:
        image: 目标图片路径
        image_painter: ImagePainter对象，包含要绘制的图片和相关参数
        scale: 缩放比例
    """
    # 打开目标图片
    img = Image.open(image)

    # 在渲染时调用_resize_image方法，并传递scale因子
    resized_image = image_painter._resize_image(scale)

    # 计算绘制位置
    x = int(image_painter.offset_x * scale)
    y = int(image_painter.offset_y * scale)

    # 绘制图片
    img.paste(resized_image, (x, y), resized_image)

    # 保存图片
    img.save(image)
