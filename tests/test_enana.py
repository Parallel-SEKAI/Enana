from pathlib import Path

from enana import (
    BorderRadius,
    Column,
    Container,
    Margin,
    Padding,
    Page,
    Row,
    Text,
    hex_to_rgba,
)


def test_enana():
    Page(
        child=Container(
            color=hex_to_rgba(0xDDAACCFF),
            padding=Padding(left=10, top=10, right=10, bottom=10),
            margin=Margin(left=10, top=10, right=10, bottom=10),
            border_radius=BorderRadius(
                top_left=10, top_right=10, bottom_left=10, bottom_right=10
            ),
            child=Row(
                children=[
                    Column(
                        children=[
                            Container(
                                width=50,
                                height=50,
                                color=hex_to_rgba(0x39C5BBFF),
                                child=Text(text="Hello"),
                            ),
                            Container(
                                width=1,
                                height=12,
                            ),
                            Container(
                                width=50,
                                height=50,
                                color=hex_to_rgba(0x39C5BBFF),
                                child=Text(text="Hello"),
                            ),
                        ]
                    ),
                    Container(
                        width=12,
                        height=1,
                    ),
                    Column(
                        children=[
                            Container(
                                width=50,
                                height=50,
                                color=hex_to_rgba(0x39C5BBFF),
                                child=Text(text="Hello"),
                            ),
                            Container(
                                width=1,
                                height=12,
                            ),
                            Container(
                                width=50,
                                height=50,
                                color=hex_to_rgba(0x39C5BBFF),
                                child=Text(text="Hello"),
                            ),
                        ]
                    ),
                ]
            ),
        )
    ).paint(filename=Path("test.png"))


if __name__ == "__main__":
    test_enana()
