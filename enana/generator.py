import multiprocessing
from pathlib import Path
from typing import Callable, List, Tuple

from PIL import Image

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
