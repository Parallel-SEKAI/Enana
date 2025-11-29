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
    """
    Draw text on an existing image with automatic line wrapping support.

    Args:
        image: Path to the image file.
        text: The text to draw.
        position: The (x, y) coordinates where the text should start.
        color: The RGBA color of the text.
        font: The font name or font object to use.
        font_size: The font size in points.
        max_width: The maximum width before wrapping occurs.
    """
    # Open the image
    img = Image.open(image)
    # Get the image size
    width, height = img.size
    # Create a font object
    from .utils import get_font

    font_obj = get_font(font, font_size)
    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # Handle automatic line wrapping
    if max_width is None:
        # If no max_width is set, draw the text directly
        draw.text(position, text, font=font_obj, fill=color)
    else:
        # Implement automatic line wrapping
        x, y = position

        # Calculate single line height
        line_height = int(
            draw.textbbox((0, 0), "A", font=font_obj)[3]
            - draw.textbbox((0, 0), "A", font=font_obj)[1]
        )
        line_height = int(line_height * 1.5)  # Line height coefficient

        # Split words
        words = text.split()
        if not words:
            return

        current_line = words[0]

        for word in words[1:]:
            # Test the width of current line plus the next word
            test_line = f"{current_line} {word}"
            test_bbox = draw.textbbox((0, 0), test_line, font=font_obj)
            test_width = int(test_bbox[2] - test_bbox[0])

            if test_width <= max_width:
                # If adding the next word still fits within max_width, continue
                current_line = test_line
            else:
                # Otherwise, draw the current line and start a new one
                draw.text((x, y), current_line, font=font_obj, fill=color)
                y += line_height
                current_line = word

        # Draw the last line
        draw.text((x, y), current_line, font=font_obj, fill=color)

    # Save the image
    img.save(image)


def draw_image(
    image: Path,
    image_painter: "ImagePainter",
    scale: float,
):
    """
    Draw one image onto another image.

    Args:
        image: Path to the target image file.
        image_painter: ImagePainter object containing the image to draw and related parameters.
        scale: Scale factor for the drawing.
    """
    # Open the target image
    img = Image.open(image)

    # Call _resize_image method during rendering with scale factor
    resized_image = image_painter._resize_image(scale)

    # Calculate drawing position
    x = int(image_painter.offset_x * scale)
    y = int(image_painter.offset_y * scale)

    # Draw the image
    img.paste(resized_image, (x, y), resized_image)

    # Save the image
    img.save(image)
