"""Provide the ModNoteMixin class."""


class ModNoteMixin:
    """Interface for classes that can have a mod note set on them."""

    def add_note(self, note: str, label: str = None):
        """Create a mod note on the author of this object in the subreddit it's
        posted in.

        :param note: The content of the note, limited to 250 characters
        :param label: The label to create the note under, can be None or one of
            ``"BOT_BAN"``, ``"PERMA_BAN"``, ``"BAN"``, ``"ABUSE_WARNING"``,
            ``"SPAM_WARNING"``, ``"SPAM_WATCH"``, ``"SOLID_CONTRIBUTOR"``,
            ``"HELPFUL_USER"``.
        :returns: The :class:`.ModNote` that was created.

            .. note::

                The authenticated user must be a moderator of the subreddit.

        """
        return self.subreddit.notes.add(self.author, note, label, self.fullname)

    def get_author_notes(self):
        """Get the mod notes for the author of this object in the subreddit it's
        posted in.

        :returns: A generator of :class:`.ModNote`.

        """
        return self.subreddit.notes(self.author)
