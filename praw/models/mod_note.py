"""Provide the ModNote class."""
from .base import PRAWBase


class ModNote(PRAWBase):
    """TODO"""

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        return getattr(self, "id")
