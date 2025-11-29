from pathlib import Path

from enana import (
    BorderRadius,
    Container,
    Margin,
    Padding,
    Page,
    Text,
    hex_to_rgba,
)


def test_enana():
    Page(
        child=Container(
            color=hex_to_rgba(0xDDAACCFF),
            padding=Padding(left=10, top=10, right=10, bottom=10),
            margin=Margin(left=10, top=10, right=10, bottom=10),
            border_radius=BorderRadius(top_left=10, top_right=10, bottom_left=10, bottom_right=10),
            child=Container(
                color=hex_to_rgba(0x39C5BBFF),
                child=Text(
                    text="Hello Hello Hello Hello Hello Hello Hello Hello",
                    max_width=50,
                ),
            ),
        )
    ).paint(scale=2, filename=Path("test.png"))


if __name__ == "__main__":
    test_enana()
