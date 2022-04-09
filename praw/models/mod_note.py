"""Provide the ModNote class."""
from praw.endpoints import API_PATH

from .base import PRAWBase


class ModNote(PRAWBase):
    """Represent a mod note.

    .. include:: ../../typical_attributes.rst

    =============== ====================================================================
    Attribute       Description
    =============== ====================================================================
    ``action``      If this note represents a moderator action, this field indicates the
                    type of action. For example ``"banuser"`` if the action was banning.
    ``created_at``  Time the comment was created, represented in `Unix Time`_.
    ``description`` If this note represents a moderator action, this field indicates the
                    description of the action. For example, if the action was banning
                    the user, this is the ban reason.
    ``details``     If this note represents a moderator action, this field indicates the
                    details of the action. For example, if the action was banning the
                    user, this is the duration of the ban.
    ``id``          The ID of the mod note.
    ``label``       The label applied to the note, currently one of ``"BOT_BAN"``,
                    ``"PERMA_BAN"``, ``"BAN"``, ``"ABUSE_WARNING"``, ``"SPAM_WARNING"``,
                    ``"SPAM_WATCH"``, ``"SOLID_CONTRIBUTOR"``, ``"HELPFUL_USER"``. Can
                    be ``None``.
    ``moderator``   The moderator who created the note.
    ``note``        The text of the note.
    ``reddit_id``   The fullname of the object this note is attached to, or ``None`` if
                    not set. If this note represents a moderators action, the fullname
                    here is the object the action was performed on.
    ``subreddit``   The subreddit the note is in.
    ``type``        The type of note. ``"NOTE"`` for regular notes, or one of
                    ``"APPROVAL"``, ``"REMOVAL"``, ``"BAN"``, ``"MUTE"``, ``"INVITE"``,
                    ``"SPAM"``, ``"CONTENT_CHANGE"``, ``"MOD_ACTION"``.
    ``user``        The user the note is on.
    =============== ====================================================================

    .. _unix time: https://en.wikipedia.org/wiki/Unix_time

    """

    def delete(self):
        """Delete this note.

        For example, to delete a note with ID
        ``"ModNote_d324b280-5ecc-435d-8159-3e259e84e339"`` for redditor ``"spez"``:

        .. code-block:: python

            reddit.subreddit("redditdev").mod.notes().delete(
                redditor="spez", note_id="ModNote_d324b280-5ecc-435d-8159-3e259e84e339"
            )

        For example, to delete the last note for redditor ``"spez"``:

        .. code-block:: python

            for note in reddit.subreddit("redditdev").mod.notes("spez"):
                note.delete()

        For example, to delete all notes for a user:

        .. code-block:: python

            reddit.subreddit("redditdev").mod.notes.delete(redditor="spez")

        """
        params = {
            "user": str(self.user),
            "subreddit": str(self.subreddit),
            "note_id": self.id,
        }
        self._reddit.delete(API_PATH["mod_notes"], params=params)
