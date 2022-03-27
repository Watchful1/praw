"""Provide the ModNote class."""
from .base import PRAWBase


class ModNote(PRAWBase):
    """Represent a mod note.

    .. include:: ../../typical_attributes.rst

    ================= =================================================================
    Attribute         Description
    ================= =================================================================
    ``action``        If this note represents a moderator action, this field
                      indicates the type of action. For example `banuser` if
                      the action was banning.
    ``created_at``    Time the comment was created, represented in `Unix Time`_.
    ``description``   If this note represents a moderator action, this field
                      indicates the description of the action. For example, if
                      the action was banning the user, this is the ban reason.
    ``details``       If this note represents a moderator action, this field
                      indicates the details of the action. For example, if the
                      action was banning the user, this is the duration of the
                      ban.
    ``id``            The ID of the mod note.
    ``label``         The label applied to the note, currently one of BOT_BAN,
                      PERMA_BAN, BAN, ABUSE_WARNING, SPAM_WARNING, SPAM_WATCH,
                      SOLID_CONTRIBUTOR, HELPFUL_USER. Can be None.
    ``moderator``     The moderator who created the note.
    ``note``          The text of the note.
    ``reddit_id``     The fullname of the object this note is attached to, or
                      None if not set. If this note represents a moderators
                      action, the fullname here is the object the action was
                      performed on.
    ``subreddit``     The subreddit the note is in.
    ``type``          The type of note. NOTE for regular notes, or one of
                      APPROVAL, REMOVAL, BAN, MUTE, INVITE, SPAM,
                      CONTENT_CHANGE, MOD_ACTION.
    ``user``          The user the note is on.
    ================= =================================================================

    .. _unix time: https://en.wikipedia.org/wiki/Unix_time

    """

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        return getattr(self, "id")
