"""Provide the ModAction class."""
from typing import TYPE_CHECKING, Union

from .base import PRAWBase

if TYPE_CHECKING:  # pragma: no cover
    import praw


class ModNote(PRAWBase):
    """TODO"""

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        return getattr(self, "id")

    # @property
    # def user(self) -> "praw.models.Redditor":
    #     """Return the :class:`.Redditor` who the action was issued by."""
    #     return self._reddit.redditor(self._user)  # pylint: disable=no-member
    #
    # @user.setter
    # def user(self, value: Union[str, "praw.models.Redditor"]):
    #     self._user = value  # pylint: disable=attribute-defined-outside-init
    #
    # @property
    # def operator(self) -> "praw.models.Redditor":
    #     """Return the :class:`.Redditor` who the action was issued by."""
    #     return self._reddit.redditor(self._operator)  # pylint: disable=no-member
    #
    # @operator.setter
    # def operator(self, value: Union[str, "praw.models.Redditor"]):
    #     self._operator = value  # pylint: disable=attribute-defined-outside-init
    #
    # @property
    # def subreddit(self) -> "praw.models.Subreddit":
    #     """Return the :class:`.Redditor` who the action was issued by."""
    #     return self._reddit.subreddit(self._subreddit)  # pylint: disable=no-member
    #
    # @subreddit.setter
    # def subreddit(self, value: Union[str, "praw.models.Subreddit"]):
    #     self._subreddit = value  # pylint: disable=attribute-defined-outside-init
