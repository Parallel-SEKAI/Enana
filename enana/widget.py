from typing import List, Optional

from .painter import Painter


class Widget:
    _width: Optional[int | float] = None
    _height: Optional[int | float] = None

    def __init__(self):
        pass

    @property
    def painters(self) -> List[Painter]:
        raise NotImplementedError(
            "painters property must be implemented in subclass"
        )

    @property
    def width(self) -> int | float:
        if self._width is None:
            raise NotImplementedError("width property must be set in subclass")
        return self._width

    @property
    def height(self) -> int | float:
        if self._height is None:
            raise NotImplementedError(
                "height property must be set in subclass"
            )
        return self._height

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"
