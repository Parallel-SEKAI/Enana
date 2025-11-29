<!-- Enana documentation master file, created by
sphinx-quickstart on Sat Nov 29 15:46:23 2025.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->

# Enana documentation

Add your content using `reStructuredText` syntax. See the
[reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html)
documentation for details.

# API Reference

Enana - A lightweight Python UI library for generating high-quality image-based UI interfaces.

This module provides the main components and utilities for creating UI interfaces that can be rendered as images.

### *class* enana.BorderRadius(, top_left: int | float, top_right: int | float, bottom_right: int | float, bottom_left: int | float)

Bases: `object`

A class representing border radius with values for all four corners.

#### *classmethod* all(value: int | float) → [BorderRadius](#enana.typing.BorderRadius)

Create a BorderRadius object with all values set to the same value.

* **Parameters:**
  **value** – The value to use for all border radii.
* **Returns:**
  A BorderRadius object with all values set to the given value.

#### *classmethod* zero() → [BorderRadius](#enana.typing.BorderRadius)

Create a BorderRadius object with all values set to 0.

* **Returns:**
  A BorderRadius object with all values 0.

### *class* enana.Column(, width: int | float | None = None, height: int | float | None = None, color: Tuple[int, int, int, int] = (0, 0, 0, 0), padding: [Padding](#enana.typing.Padding) | None = None, margin: [Margin](#enana.typing.Margin) | None = None, border_radius: [BorderRadius](#enana.typing.BorderRadius) | None = None, children: List[[Widget](#enana.widget.Widget)] | None = None)

Bases: [`Container`](#enana.container.Container)

A vertical layout widget that arranges its children in a column.

* **Parameters:**
  * **width** – The width of the column.
  * **height** – The height of the column.
  * **color** – The background color of the column in RGBA format.
  * **padding** – The padding inside the column.
  * **margin** – The margin outside the column.
  * **border_radius** – The border radius of the column.
  * **children** – The list of child widgets to be arranged vertically.

#### *property* height *: int | float*

Get the height of the column.

If the height is not explicitly set, it will be calculated based on the sum of heights of its children.

* **Returns:**
  The height of the column.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this column.

* **Returns:**
  A list of Painter objects that will be used to render this column.

#### *property* width *: int | float*

Get the width of the column.

If the width is not explicitly set, it will be calculated based on the maximum width of its children.

* **Returns:**
  The width of the column.

### *class* enana.Container(, width: int | float | None = None, height: int | float | None = None, color: Tuple[int, int, int, int] = (0, 0, 0, 0), padding: [Padding](#enana.typing.Padding) | None = None, margin: [Margin](#enana.typing.Margin) | None = None, border_radius: [BorderRadius](#enana.typing.BorderRadius) | None = None, child: [Widget](#enana.widget.Widget) | None = None)

Bases: [`Widget`](#enana.widget.Widget)

A container widget that wraps other widgets and provides styling properties.

* **Parameters:**
  * **width** – The width of the container.
  * **height** – The height of the container.
  * **color** – The background color of the container in RGBA format.
  * **padding** – The padding inside the container.
  * **margin** – The margin outside the container.
  * **border_radius** – The border radius of the container.
  * **child** – The child widget to be wrapped by this container.

#### *property* height *: int | float*

Get the height of the container.

If the height is not explicitly set, it will be calculated based on the child widget’s height.

* **Returns:**
  The height of the container.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this container.

* **Returns:**
  A list of Painter objects that will be used to render this container.

#### *property* width *: int | float*

Get the width of the container.

If the width is not explicitly set, it will be calculated based on the child widget’s width.

* **Returns:**
  The width of the container.

### *class* enana.Image(, url: str, width: int | float, height: int | float, size: [ImageSize](#enana.image.ImageSize) = ImageSize.DEFAULT)

Bases: [`Widget`](#enana.widget.Widget)

An image widget for displaying images.

* **Parameters:**
  * **url** – The URL of the image, supports http(s), file, and base64 formats.
  * **width** – The width of the image container.
  * **height** – The height of the image container.
  * **size** – The image sizing mode, defaults to DEFAULT.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this image widget.

* **Returns:**
  A list of Painter objects that will be used to render this image.

### *class* enana.ImageSize(\*values)

Bases: `Enum`

Enum for image sizing modes.

- COVER: Resize the image to cover the entire container, cropping if necessary.
- CONTAIN: Resize the image to fit within the container, maintaining aspect ratio.
- DEFAULT: Use the original image size without resizing.

#### CONTAIN *= 'contain'*

#### COVER *= 'cover'*

#### DEFAULT *= 'default'*

### *class* enana.Margin(, top: int | float, right: int | float, bottom: int | float, left: int | float)

Bases: [`Padding`](#enana.typing.Padding)

A class representing margin, inheriting from Padding.

### *class* enana.Padding(, top: int | float, right: int | float, bottom: int | float, left: int | float)

Bases: `object`

A class representing padding with top, right, bottom, and left values.

#### *classmethod* all(value: int | float) → [Padding](#enana.typing.Padding)

Create a Padding object with all values set to the same value.

* **Parameters:**
  **value** – The value to use for all padding sides.
* **Returns:**
  A Padding object with all values set to the given value.

#### *property* horizontal *: int | float*

Get the total horizontal padding (left + right).

* **Returns:**
  The total horizontal padding.

#### *classmethod* symmetric(vertical: int | float, horizontal: int | float) → [Padding](#enana.typing.Padding)

Create a Padding object with symmetric values.

* **Parameters:**
  * **vertical** – The value to use for top and bottom padding.
  * **horizontal** – The value to use for left and right padding.
* **Returns:**
  A Padding object with symmetric values.

#### *property* vertical *: int | float*

Get the total vertical padding (top + bottom).

* **Returns:**
  The total vertical padding.

#### *classmethod* zero() → [Padding](#enana.typing.Padding)

Create a Padding object with all values set to 0.

* **Returns:**
  A Padding object with all values 0.

### *class* enana.Page(, child: [Widget](#enana.widget.Widget))

Bases: [`Widget`](#enana.widget.Widget)

A page widget that serves as the root container for UI elements.

#### *classmethod* from_json(json: dict) → [Page](#enana.page.Page)

Create a Page object from a JSON dictionary.

* **Parameters:**
  **json** – JSON dictionary, conforming to page.schema.json
* **Returns:**
  The corresponding Page object
* **Return type:**
  [Page](#enana.Page)

#### paint(, scale: float = 1.0, filename: Path) → None

Paint the page to an image file.

* **Parameters:**
  * **scale** – Scale factor for the image, defaults to 1.0.
  * **filename** – Path to save the generated image.

### *class* enana.Painter(, width: int | float, height: int | float, func: Callable[[int | float, int | float], bool], color: Tuple[int, int, int, int])

Bases: `object`

Base class for all painters, responsible for rendering pixels.

#### paint(x: int | float, y: int | float) → bool

Determine if a pixel at the given coordinates should be painted.

* **Parameters:**
  * **x** – The x-coordinate.
  * **y** – The y-coordinate.
* **Returns:**
  True if the pixel should be painted, False otherwise.

### *class* enana.Row(, width: int | float | None = None, height: int | float | None = None, color: Tuple[int, int, int, int] = (0, 0, 0, 0), padding: [Padding](#enana.typing.Padding) | None = None, margin: [Margin](#enana.typing.Margin) | None = None, border_radius: [BorderRadius](#enana.typing.BorderRadius) | None = None, children: List[[Widget](#enana.widget.Widget)] | None = None)

Bases: [`Container`](#enana.container.Container)

A horizontal layout widget that arranges its children in a row.

* **Parameters:**
  * **width** – The width of the row.
  * **height** – The height of the row.
  * **color** – The background color of the row in RGBA format.
  * **padding** – The padding inside the row.
  * **margin** – The margin outside the row.
  * **border_radius** – The border radius of the row.
  * **children** – The list of child widgets to be arranged horizontally.

#### *property* height *: int | float*

Get the height of the row.

If the height is not explicitly set, it will be calculated based on the maximum height of its children.

* **Returns:**
  The height of the row.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this row.

* **Returns:**
  A list of Painter objects that will be used to render this row.

#### *property* width *: int | float*

Get the width of the row.

If the width is not explicitly set, it will be calculated based on the sum of widths of its children.

* **Returns:**
  The width of the row.

### *class* enana.Text(, text: str, font: str = 'Arial', font_size: int = 12, max_width: int | None = None, color: Tuple[int, int, int, int] = (0, 0, 0, 255))

Bases: [`Widget`](#enana.widget.Widget)

A text widget for displaying text content.

* **Parameters:**
  * **text** – The text content to display.
  * **font** – The font name to use.
  * **font_size** – The font size in points.
  * **max_width** – The maximum width of the text before wrapping.
  * **color** – The text color in RGBA format.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this text widget.

* **Returns:**
  A list of Painter objects that will be used to render this text.

### *class* enana.Widget

Bases: `object`

#### *classmethod* from_json(json: dict) → [Widget](#enana.widget.Widget)

从JSON字典创建Widget对象

* **Parameters:**
  **json** – JSON字典，符合widget.schema.json
* **Returns:**
  对应的Widget对象
* **Return type:**
  [Widget](#enana.Widget)

#### *property* height *: int | float*

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

#### *property* width *: int | float*

### enana.hex_to_rgba(hex_color: int) → Tuple[int, int, int, int]

Convert a hexadecimal color integer to an RGBA tuple

* **Parameters:**
  **hex_color** – Hexadecimal color in 0xRRGGBBAA format
* **Returns:**
  RGBA tuple with values ranging from 0-255
* **Return type:**
  Tuple[int, int, int, int]

<a id="module-enana.container"></a>

### *class* enana.container.Container(, width: int | float | None = None, height: int | float | None = None, color: Tuple[int, int, int, int] = (0, 0, 0, 0), padding: [Padding](#enana.typing.Padding) | None = None, margin: [Margin](#enana.typing.Margin) | None = None, border_radius: [BorderRadius](#enana.typing.BorderRadius) | None = None, child: [Widget](#enana.widget.Widget) | None = None)

Bases: [`Widget`](#enana.widget.Widget)

A container widget that wraps other widgets and provides styling properties.

* **Parameters:**
  * **width** – The width of the container.
  * **height** – The height of the container.
  * **color** – The background color of the container in RGBA format.
  * **padding** – The padding inside the container.
  * **margin** – The margin outside the container.
  * **border_radius** – The border radius of the container.
  * **child** – The child widget to be wrapped by this container.

#### *property* height *: int | float*

Get the height of the container.

If the height is not explicitly set, it will be calculated based on the child widget’s height.

* **Returns:**
  The height of the container.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this container.

* **Returns:**
  A list of Painter objects that will be used to render this container.

#### *property* width *: int | float*

Get the width of the container.

If the width is not explicitly set, it will be calculated based on the child widget’s width.

* **Returns:**
  The width of the container.

<a id="module-enana.column"></a>

### *class* enana.column.Column(, width: int | float | None = None, height: int | float | None = None, color: Tuple[int, int, int, int] = (0, 0, 0, 0), padding: [Padding](#enana.typing.Padding) | None = None, margin: [Margin](#enana.typing.Margin) | None = None, border_radius: [BorderRadius](#enana.typing.BorderRadius) | None = None, children: List[[Widget](#enana.widget.Widget)] | None = None)

Bases: [`Container`](#enana.container.Container)

A vertical layout widget that arranges its children in a column.

* **Parameters:**
  * **width** – The width of the column.
  * **height** – The height of the column.
  * **color** – The background color of the column in RGBA format.
  * **padding** – The padding inside the column.
  * **margin** – The margin outside the column.
  * **border_radius** – The border radius of the column.
  * **children** – The list of child widgets to be arranged vertically.

#### *property* height *: int | float*

Get the height of the column.

If the height is not explicitly set, it will be calculated based on the sum of heights of its children.

* **Returns:**
  The height of the column.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this column.

* **Returns:**
  A list of Painter objects that will be used to render this column.

#### *property* width *: int | float*

Get the width of the column.

If the width is not explicitly set, it will be calculated based on the maximum width of its children.

* **Returns:**
  The width of the column.

<a id="module-enana.row"></a>

### *class* enana.row.Row(, width: int | float | None = None, height: int | float | None = None, color: Tuple[int, int, int, int] = (0, 0, 0, 0), padding: [Padding](#enana.typing.Padding) | None = None, margin: [Margin](#enana.typing.Margin) | None = None, border_radius: [BorderRadius](#enana.typing.BorderRadius) | None = None, children: List[[Widget](#enana.widget.Widget)] | None = None)

Bases: [`Container`](#enana.container.Container)

A horizontal layout widget that arranges its children in a row.

* **Parameters:**
  * **width** – The width of the row.
  * **height** – The height of the row.
  * **color** – The background color of the row in RGBA format.
  * **padding** – The padding inside the row.
  * **margin** – The margin outside the row.
  * **border_radius** – The border radius of the row.
  * **children** – The list of child widgets to be arranged horizontally.

#### *property* height *: int | float*

Get the height of the row.

If the height is not explicitly set, it will be calculated based on the maximum height of its children.

* **Returns:**
  The height of the row.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this row.

* **Returns:**
  A list of Painter objects that will be used to render this row.

#### *property* width *: int | float*

Get the width of the row.

If the width is not explicitly set, it will be calculated based on the sum of widths of its children.

* **Returns:**
  The width of the row.

<a id="module-enana.text"></a>

### *class* enana.text.Text(, text: str, font: str = 'Arial', font_size: int = 12, max_width: int | None = None, color: Tuple[int, int, int, int] = (0, 0, 0, 255))

Bases: [`Widget`](#enana.widget.Widget)

A text widget for displaying text content.

* **Parameters:**
  * **text** – The text content to display.
  * **font** – The font name to use.
  * **font_size** – The font size in points.
  * **max_width** – The maximum width of the text before wrapping.
  * **color** – The text color in RGBA format.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this text widget.

* **Returns:**
  A list of Painter objects that will be used to render this text.

<a id="module-enana.image"></a>

### *class* enana.image.Image(, url: str, width: int | float, height: int | float, size: [ImageSize](#enana.image.ImageSize) = ImageSize.DEFAULT)

Bases: [`Widget`](#enana.widget.Widget)

An image widget for displaying images.

* **Parameters:**
  * **url** – The URL of the image, supports http(s), file, and base64 formats.
  * **width** – The width of the image container.
  * **height** – The height of the image container.
  * **size** – The image sizing mode, defaults to DEFAULT.

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

Get the list of painters for this image widget.

* **Returns:**
  A list of Painter objects that will be used to render this image.

### *class* enana.image.ImageSize(\*values)

Bases: `Enum`

Enum for image sizing modes.

- COVER: Resize the image to cover the entire container, cropping if necessary.
- CONTAIN: Resize the image to fit within the container, maintaining aspect ratio.
- DEFAULT: Use the original image size without resizing.

#### CONTAIN *= 'contain'*

#### COVER *= 'cover'*

#### DEFAULT *= 'default'*

<a id="module-enana.page"></a>

### *class* enana.page.DrawFunction(painters: List, scale: float)

Bases: `object`

A serializable drawing function class for executing drawing operations in a multiprocessing environment.

### *class* enana.page.Page(, child: [Widget](#enana.widget.Widget))

Bases: [`Widget`](#enana.widget.Widget)

A page widget that serves as the root container for UI elements.

#### *classmethod* from_json(json: dict) → [Page](#enana.page.Page)

Create a Page object from a JSON dictionary.

* **Parameters:**
  **json** – JSON dictionary, conforming to page.schema.json
* **Returns:**
  The corresponding Page object
* **Return type:**
  [Page](#enana.page.Page)

#### paint(, scale: float = 1.0, filename: Path) → None

Paint the page to an image file.

* **Parameters:**
  * **scale** – Scale factor for the image, defaults to 1.0.
  * **filename** – Path to save the generated image.

<a id="module-enana.painter"></a>

### *class* enana.painter.ImagePainter(, image: Image, width: int | float, height: int | float, size: object | None = None)

Bases: [`Painter`](#enana.painter.Painter)

Painter for rendering images.

### *class* enana.painter.Painter(, width: int | float, height: int | float, func: Callable[[int | float, int | float], bool], color: Tuple[int, int, int, int])

Bases: `object`

Base class for all painters, responsible for rendering pixels.

#### paint(x: int | float, y: int | float) → bool

Determine if a pixel at the given coordinates should be painted.

* **Parameters:**
  * **x** – The x-coordinate.
  * **y** – The y-coordinate.
* **Returns:**
  True if the pixel should be painted, False otherwise.

### *class* enana.painter.TextPainter(, text: str, font: str = 'Arial', font_size: int = 12, max_width: int | None = None, color: Tuple[int, int, int, int])

Bases: [`Painter`](#enana.painter.Painter)

Painter for rendering text.

<a id="module-enana.generator"></a>

### enana.generator.draw_image(image: Path, image_painter: [ImagePainter](#enana.painter.ImagePainter), scale: float)

Draw one image onto another image.

* **Parameters:**
  * **image** – Path to the target image file.
  * **image_painter** – ImagePainter object containing the image to draw and related parameters.
  * **scale** – Scale factor for the drawing.

### enana.generator.draw_text(image: Path, text: str, position: Tuple[int, int], color: Tuple[int, int, int, int], font: str | Any = 'Arial', font_size: int = 12, max_width: int | None = None)

Draw text on an existing image with automatic line wrapping support.

* **Parameters:**
  * **image** – Path to the image file.
  * **text** – The text to draw.
  * **position** – The (x, y) coordinates where the text should start.
  * **color** – The RGBA color of the text.
  * **font** – The font name or font object to use.
  * **font_size** – The font size in points.
  * **max_width** – The maximum width before wrapping occurs.

### enana.generator.generate_image(func: Callable[[int, int], Tuple[int, int, int, int]], width: int, height: int, filename: Path) → None

Creates and saves an image in parallel using multiprocessing.

* **Parameters:**
  * **func** – A function that takes x and y coordinates and returns an RGBA tuple.
  * **width** – The width of the image.
  * **height** – The height of the image.
  * **filename** – The file path to save the image to.

<a id="module-enana.typing"></a>

### *class* enana.typing.BorderRadius(, top_left: int | float, top_right: int | float, bottom_right: int | float, bottom_left: int | float)

Bases: `object`

A class representing border radius with values for all four corners.

#### *classmethod* all(value: int | float) → [BorderRadius](#enana.typing.BorderRadius)

Create a BorderRadius object with all values set to the same value.

* **Parameters:**
  **value** – The value to use for all border radii.
* **Returns:**
  A BorderRadius object with all values set to the given value.

#### *classmethod* zero() → [BorderRadius](#enana.typing.BorderRadius)

Create a BorderRadius object with all values set to 0.

* **Returns:**
  A BorderRadius object with all values 0.

### *class* enana.typing.Margin(, top: int | float, right: int | float, bottom: int | float, left: int | float)

Bases: [`Padding`](#enana.typing.Padding)

A class representing margin, inheriting from Padding.

### *class* enana.typing.Padding(, top: int | float, right: int | float, bottom: int | float, left: int | float)

Bases: `object`

A class representing padding with top, right, bottom, and left values.

#### *classmethod* all(value: int | float) → [Padding](#enana.typing.Padding)

Create a Padding object with all values set to the same value.

* **Parameters:**
  **value** – The value to use for all padding sides.
* **Returns:**
  A Padding object with all values set to the given value.

#### *property* horizontal *: int | float*

Get the total horizontal padding (left + right).

* **Returns:**
  The total horizontal padding.

#### *classmethod* symmetric(vertical: int | float, horizontal: int | float) → [Padding](#enana.typing.Padding)

Create a Padding object with symmetric values.

* **Parameters:**
  * **vertical** – The value to use for top and bottom padding.
  * **horizontal** – The value to use for left and right padding.
* **Returns:**
  A Padding object with symmetric values.

#### *property* vertical *: int | float*

Get the total vertical padding (top + bottom).

* **Returns:**
  The total vertical padding.

#### *classmethod* zero() → [Padding](#enana.typing.Padding)

Create a Padding object with all values set to 0.

* **Returns:**
  A Padding object with all values 0.

<a id="module-enana.utils"></a>

### enana.utils.always_false(x: int | float, y: int | float) → bool

A function that always returns False, used for Painter’s func parameter

* **Parameters:**
  * **x** – x-coordinate
  * **y** – y-coordinate
* **Returns:**
  Always returns False
* **Return type:**
  bool

### enana.utils.always_true(x: int | float, y: int | float) → bool

A function that always returns True, used for Painter’s func parameter

* **Parameters:**
  * **x** – x-coordinate
  * **y** – y-coordinate
* **Returns:**
  Always returns True
* **Return type:**
  bool

### enana.utils.from_json(json: dict) → [Widget](#enana.Widget)

Create a Widget object from a JSON dictionary.

* **Parameters:**
  **json** – JSON dictionary, conforming to widget.schema.json
* **Returns:**
  The corresponding Widget object
* **Return type:**
  [Widget](#enana.Widget)

### enana.utils.get_font(font: Any, font_size: int) → FreeTypeFont

Get a font object, supporting both direct font objects and font names

* **Parameters:**
  * **font** – Font object or font name
  * **font_size** – Font size in points
* **Returns:**
  Font object
* **Return type:**
  ImageFont.FreeTypeFont

### enana.utils.hex_to_rgba(hex_color: int) → Tuple[int, int, int, int]

Convert a hexadecimal color integer to an RGBA tuple

* **Parameters:**
  **hex_color** – Hexadecimal color in 0xRRGGBBAA format
* **Returns:**
  RGBA tuple with values ranging from 0-255
* **Return type:**
  Tuple[int, int, int, int]

<a id="module-enana.widget"></a>

### *class* enana.widget.Widget

Bases: `object`

#### *classmethod* from_json(json: dict) → [Widget](#enana.widget.Widget)

从JSON字典创建Widget对象

* **Parameters:**
  **json** – JSON字典，符合widget.schema.json
* **Returns:**
  对应的Widget对象
* **Return type:**
  [Widget](#enana.widget.Widget)

#### *property* height *: int | float*

#### *property* painters *: List[[Painter](#enana.painter.Painter)]*

#### *property* width *: int | float*
