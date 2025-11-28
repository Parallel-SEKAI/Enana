class Padding:
    def __init__(
        self,
        *,
        top: int | float,
        right: int | float,
        bottom: int | float,
        left: int | float,
    ):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    @classmethod
    def zero(cls) -> "Padding":
        return cls(top=0, right=0, bottom=0, left=0)

    @classmethod
    def all(cls, value: int | float) -> "Padding":
        return cls(top=value, right=value, bottom=value, left=value)

    @classmethod
    def symmetric(
        cls, vertical: int | float, horizontal: int | float
    ) -> "Padding":
        return cls(
            top=vertical, right=horizontal, bottom=vertical, left=horizontal
        )

    @property
    def vertical(self) -> int | float:
        return self.top + self.bottom

    @property
    def horizontal(self) -> int | float:
        return self.left + self.right

    def __bool__(self) -> bool:
        return any([self.top, self.right, self.bottom, self.left])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class Margin(Padding):
    pass


class BorderRadius:
    def __init__(
        self,
        *,
        top_left: int | float,
        top_right: int | float,
        bottom_right: int | float,
        bottom_left: int | float,
    ):
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left

    @classmethod
    def zero(cls) -> "BorderRadius":
        return cls(top_left=0, top_right=0, bottom_right=0, bottom_left=0)

    @classmethod
    def all(cls, value: int | float) -> "BorderRadius":
        return cls(
            top_left=value,
            top_right=value,
            bottom_right=value,
            bottom_left=value,
        )
