"""Provide the ModNoteMixin class."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import praw


class ModNoteMixin:
    """Interface for classes that can have a mod note set on them."""

    author: "praw.models.Redditor"
    fullname: str
    thing: "praw.models.Subreddit"

    def add_note(self, note: str, *, label: str = None):
        """Create a mod note on the author of this object in the subreddit it's posted in.

        :param note: The content of the note, limited to 250 characters
        :param label: The label to create the note under, can be ``None`` or one of
            ``"BOT_BAN"``, ``"PERMA_BAN"``, ``"BAN"``, ``"ABUSE_WARNING"``,
            ``"SPAM_WARNING"``, ``"SPAM_WATCH"``, ``"SOLID_CONTRIBUTOR"``,
            ``"HELPFUL_USER"``.

        :returns: The :class:`.ModNote` that was created.

        .. note::

            The authenticated user must be a moderator of the subreddit.

        For example, to create a note with the label ``"HELPFUL_USER"`` on a submission,
        try:

        .. code-block:: python

            reddit.submission("92dd8").mod.add_note("Test note", "HELPFUL_USER")

        """
        return self.thing.subreddit.mod.notes.create(
            redditor=self.thing.author,
            note=note,
            label=label,
            fullname=self.thing.fullname,
        )

    def notes(self):
        """Get the mod notes for the author of this object in the subreddit it's posted in.

        :returns: A generator of :class:`.ModNote` instances.

        .. code-block:: python

            for note in reddit.submission("92dd8").mod.notes():
                print(f"{note.label}: {note.user_note_data['note']}")

        """
        return self.thing.subreddit.mod.notes(self.thing.author)
