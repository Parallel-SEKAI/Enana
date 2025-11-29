# from pathlib import Path

# from enana import Page


def test_json():
    # Page(
    #     child=Container(
    #         color=hex_to_rgba(0xDDAACCFF),
    #         padding=Padding(left=10, top=10, right=10, bottom=10),
    #         margin=Margin(left=10, top=10, right=10, bottom=10),
    #         border_radius=BorderRadius(
    #             top_left=10, top_right=10, bottom_left=10, bottom_right=10
    #         ),
    #         child=Column(
    #             children=[
    #                 Container(
    #                     color=hex_to_rgba(0x39C5BBFF),
    #                     child=Text(
    #                         text="Hello Hello Hello Hello Hello Hello Hello Hello",
    #                         max_width=50,
    #                     ),
    #                 ),
    #                 Image(
    #                     url="https://www.gstatic.com/images/branding/searchlogo/ico/favicon.ico",
    #                     width=50,
    #                     height=50,
    #                     size=ImageSize.COVER,
    #                 ),
    #             ]
    #         ),
    #     )
    # ).paint(scale=10, filename=Path("test.png"))
    # Page.from_json(
    #     {
    #         "$schema": "https://raw.githubusercontent.com/Parallel-SEKAI/Enana/refs/heads/main/widget.schema.json",
    #         "type": "Page",
    #         "child": {
    #             "type": "Container",
    #             "color": [221, 170, 204, 255],
    #             "padding": [10, 10, 10, 10],
    #             "margin": [10, 10, 10, 10],
    #             "border_radius": [10, 10, 10, 10],
    #             "child": {
    #                 "type": "Column",
    #                 "children": [
    #                     {
    #                         "type": "Container",
    #                         "color": [57, 197, 187, 255],
    #                         "child": {
    #                             "type": "Text",
    #                             "text": "Hello Hello Hello Hello Hello Hello Hello Hello",
    #                             "max_width": 50,
    #                         },
    #                     },
    #                     {
    #                         "type": "Image",
    #                         "url": "https://www.gstatic.com/images/branding/searchlogo/ico/favicon.ico",
    #                         "width": 50,
    #                         "height": 50,
    #                         "size": "COVER",
    #                     },
    #                 ],
    #             },
    #         },
    #     }
    # ).paint(scale=10, filename=Path("test_json.png"))
    pass


if __name__ == "__main__":
    test_json()
