from typing import List, Optional

from .painter import Painter


class Widget:
    _width: Optional[int | float] = None
    _height: Optional[int | float] = None

    def __init__(self):
        pass

    @classmethod
    def from_json(cls, json: dict) -> "Widget":
        """
        从JSON字典创建Widget对象

        Args:
            json: JSON字典，符合widget.schema.json

        Returns:
            Widget: 对应的Widget对象
        """
        from .utils import from_json

        return from_json(json)

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
