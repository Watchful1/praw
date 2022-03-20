"""Provide the ModNoteMixin class."""


class ModNoteMixin:
    """Interface for classes that can have a mod note set on them."""

    def add_note(self, note: str, label: str = None):
        """TODO
        """
        return self.subreddit.notes.add(self.author, note, label, self.fullname)

    def get_author_notes(self):
        """TODO
        """
        return self.subreddit.notes(self.author)
