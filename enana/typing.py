class Padding:
    """
    A class representing padding with top, right, bottom, and left values.
    """

    def __init__(
        self,
        *,
        top: int | float,
        right: int | float,
        bottom: int | float,
        left: int | float,
    ):
        """
        Initialize the Padding object.

        Args:
            top: The top padding value.
            right: The right padding value.
            bottom: The bottom padding value.
            left: The left padding value.
        """
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    @classmethod
    def zero(cls) -> "Padding":
        """
        Create a Padding object with all values set to 0.

        Returns:
            A Padding object with all values 0.
        """
        return cls(top=0, right=0, bottom=0, left=0)

    @classmethod
    def all(cls, value: int | float) -> "Padding":
        """
        Create a Padding object with all values set to the same value.

        Args:
            value: The value to use for all padding sides.

        Returns:
            A Padding object with all values set to the given value.
        """
        return cls(top=value, right=value, bottom=value, left=value)

    @classmethod
    def symmetric(
        cls, vertical: int | float, horizontal: int | float
    ) -> "Padding":
        """
        Create a Padding object with symmetric values.

        Args:
            vertical: The value to use for top and bottom padding.
            horizontal: The value to use for left and right padding.

        Returns:
            A Padding object with symmetric values.
        """
        return cls(
            top=vertical, right=horizontal, bottom=vertical, left=horizontal
        )

    @property
    def vertical(self) -> int | float:
        """
        Get the total vertical padding (top + bottom).

        Returns:
            The total vertical padding.
        """
        return self.top + self.bottom

    @property
    def horizontal(self) -> int | float:
        """
        Get the total horizontal padding (left + right).

        Returns:
            The total horizontal padding.
        """
        return self.left + self.right

    def __bool__(self) -> bool:
        """
        Check if any padding value is non-zero.

        Returns:
            True if any padding value is non-zero, False otherwise.
        """
        return any([self.top, self.right, self.bottom, self.left])

    def __repr__(self) -> str:
        """
        Get a string representation of the Padding object.

        Returns:
            A string representation of the Padding object.
        """
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class Margin(Padding):
    """
    A class representing margin, inheriting from Padding.
    """

    pass


class BorderRadius:
    """
    A class representing border radius with values for all four corners.
    """

    def __init__(
        self,
        *,
        top_left: int | float,
        top_right: int | float,
        bottom_right: int | float,
        bottom_left: int | float,
    ):
        """
        Initialize the BorderRadius object.

        Args:
            top_left: The top-left border radius.
            top_right: The top-right border radius.
            bottom_right: The bottom-right border radius.
            bottom_left: The bottom-left border radius.
        """
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left

    @classmethod
    def zero(cls) -> "BorderRadius":
        """
        Create a BorderRadius object with all values set to 0.

        Returns:
            A BorderRadius object with all values 0.
        """
        return cls(top_left=0, top_right=0, bottom_right=0, bottom_left=0)

    @classmethod
    def all(cls, value: int | float) -> "BorderRadius":
        """
        Create a BorderRadius object with all values set to the same value.

        Args:
            value: The value to use for all border radii.

        Returns:
            A BorderRadius object with all values set to the given value.
        """
        return cls(
            top_left=value,
            top_right=value,
            bottom_right=value,
            bottom_left=value,
        )
