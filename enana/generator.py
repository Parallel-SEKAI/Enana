import multiprocessing
import os
import sys
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont

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
    font_obj: Any
    try:
        # Check if font is already a font object
        if hasattr(font, "getbbox"):
            # Already a font object, use it directly
            font_obj = font
        else:
            # Try to load the specified font
            font_obj = ImageFont.truetype(font, font_size)
    except OSError:
        # If the specified font fails, try to find a fallback font
        try:
            # Try common Windows fonts
            if sys.platform == "win32":
                # Try to find Arial or a similar font
                font_files = [
                    "arial.ttf",
                    "calibri.ttf",
                    "times.ttf",
                    "verdana.ttf",
                ]
                font_obj = None
                for font_file in font_files:
                    try:
                        font_path = os.path.join(
                            r"C:\Windows\Fonts", font_file
                        )
                        font_obj = ImageFont.truetype(font_path, font_size)
                        break
                    except OSError:
                        continue
                # If no Windows font found, use default font
                if font_obj is None:
                    font_obj = ImageFont.load_default()
            else:
                # On non-Windows platforms, use default font
                font_obj = ImageFont.load_default()
        except Exception:
            # Fallback to default font if all else fails
            font_obj = ImageFont.load_default()
    # Create a drawing context
    draw = ImageDraw.Draw(img)
    # Draw the text on the image
    draw.text(position, text, font=font_obj, fill=color)
    # Save the image
    img.save(image)
