"""Provide the ModNotes class."""
from collections.abc import Iterable
from itertools import islice
from sys import version_info
from typing import TYPE_CHECKING, Any, Generator, Iterator, Optional, Tuple, Union

from ..const import API_PATH
from ..models.base import PRAWBase
from ..models.listing.generator import ListingGenerator
from .reddit.comment import Comment
from .reddit.redditor import Redditor
from .reddit.submission import Submission

if version_info >= (3, 8):
    from functools import singledispatchmethod
else:
    from singledispatch import singledispatchmethod

if TYPE_CHECKING:  # pragma: no cover
    import praw


class ModNotes(PRAWBase):
    """Provides methods to interact with mod notes.

    For example, notes for a user can be iterated through like so:

    .. code-block:: python

        for note in reddit.subreddit("redditdev").mod.notes("spez"):
            print(f"{note.label}: {note.user_note_data['note']}")

    .. note::

        The authenticated user must be a moderator of the subreddit.

    """

    def _all_generator(
        self,
        redditor: Union[str, "praw.models.Redditor"],
        subreddit: Optional[Union[str, "praw.models.Subreddit"]] = None,
        **generator_kwargs,
    ):
        self._safely_add_arguments(
            arguments=generator_kwargs,
            key="params",
            subreddit=subreddit or self.subreddit,
            user=redditor,
        )
        return ListingGenerator(self._reddit, API_PATH["mod_notes"], **generator_kwargs)

    def _bulk_generator(self, subreddits, users):
        subs_iter = iter(subreddits)
        users_iter = iter(users)
        while True:
            subreddits_chunk = list(islice(subs_iter, 500))
            users_chunk = list(islice(users_iter, 500))
            if not any([subreddits_chunk, users_chunk]):
                break
            params = {
                "subreddits": ",".join(map(str, subreddits_chunk)),
                "users": ",".join(map(str, users_chunk)),
            }
            response = self._reddit.get(API_PATH["mod_notes_bulk"], params=params)
            for note_dict in response["mod_notes"]:
                yield self._reddit._objector.objectify(note_dict)

    @singledispatchmethod
    def __call__(
        self,
        items,
        **generator_kwargs,
    ):  # ignore noqa: D102
        raise ValueError(f"Getting notes for type {type(items)} is not supported.")

    @__call__.register(str)
    @__call__.register(Redditor)
    def _(
        self,
        redditor: Union[str, "praw.models.Redditor"],
        *,
        all_notes: bool = True,
        subreddit: Optional[Union[str, "praw.models.Subreddit"]] = None,
        **generator_kwargs: Any,
    ) -> Iterator["praw.models.ModNote"]:
        """Return notes associated with a :class:`.Redditor`.

        :param redditor: The redditor to return notes on.
        :param all_notes: Whether to return all notes, or only the latest (default:
            ``True``).
        :param subreddit: The subreddit to retrieve the notes from. If ``None``, uses
            this instance's ``subreddit`` (default: ``None``).

        """
        if not subreddit and not self.subreddit:
            raise ValueError(
                "`subreddit` must be provided if `ModNotes.subreddit` is not set."
            )
        if all_notes:
            return self._all_generator(
                redditor, subreddit or self.subreddit, **generator_kwargs
            )
        else:
            return self._bulk_generator([subreddit or self.subreddit], [redditor])

    @__call__.register(Comment)
    @__call__.register(Submission)
    def _(
        self,
        item: Union["praw.models.Comment", "praw.models.Submission"],
        *,
        all_notes: bool = True,
        **generator_kwargs: Any,
    ) -> Iterator["praw.models.ModNote"]:
        """Return notes associated with the author of a :class:`.Comment` or :class:`.Submission`.

        :param item: The thing to return notes on. Must be a :class:`.Comment` or
            :class:`.Submission`.
        :param all_notes: Whether to return all notes, or only the latest (default:
            ``True``).

        """
        if all_notes:
            return self._all_generator(item.author, item.subreddit, **generator_kwargs)
        else:
            return self._bulk_generator([item.subreddit], [item.author])

    @__call__.register(Iterable)
    def _(
        self,
        items: Iterable[
            Union[
                Tuple[
                    Union[str, "praw.models.Subreddit"],
                    Union[str, "praw.models.Redditor"],
                ],
                "praw.models.Submission",
                "praw.models.Comment",
                str,
            ]
        ],
        *,
        all_notes: bool = False,
        subreddit: Optional[Union[str, "praw.models.Subreddit"]] = None,
        **generator_kwargs: Any,
    ) -> Generator["praw.models.ModNote", None, None]:
        """Get the most recent note for each subreddit/user pair, or ``None`` if they don't have any.

        :param items: A list of subreddit/username tuples, :class:`.Comment`,
            :class:`.Redditor`, or :class:`.Submission` objects, or redditor names. Can
            contain any combination of previously mentioned items.
        :param all_notes: Whether to return all, or only the latest notes (default:
            ``False``).
        :param subreddit: The subreddit to retrieve the notes from. If ``None``, uses
            this instance's ``subreddit`` (default: ``None``). This is only applicable
            for :class:`.Redditor` usernames or objects.
        :param generator_kwargs: Additional keyword arguments passed to the generator.
            This is ignored when ``all_notes`` is ``False``.

        :returns: A generator that yields the most recent note or ``None`` if the user
            doesn't have any notes per entry in their relative order. If ``all_notes``
            is ``True``, this will yield all notes for each entry.

        .. code-block:: python

            pairs = [("redditdev", "spez"), ("announcements", "spez"), ("redditdev", "bboe")]
            for note in reddit.mod_notes(pairs):
                if note is None:
                    print("No note")
                else:
                    print(note)

        .. code-block:: python

            submissions = list(reddit.subreddit("redditdev").hot())
            notes = list(reddit.mod_notes(submissions))

        .. code-block:: python

            comments = reddit.submissions("92dd8").comments.list()
            notes = list(reddit.mod_notes(comments))

        """
        from .reddit.subreddit import Subreddit

        subreddits = []
        users = []
        for subreddit_user in items:
            if isinstance(subreddit_user, (Comment, Submission)):
                subreddits.append(subreddit_user.subreddit.display_name)
                users.append(subreddit_user.author.name)
            elif isinstance(subreddit_user, Tuple):
                if isinstance(subreddit_user[0], Subreddit):
                    subreddits.append(subreddit_user[0].display_name)
                else:
                    subreddits.append(subreddit_user[0])
                if isinstance(subreddit_user[1], Redditor):
                    users.append(subreddit_user[1].name)
                else:
                    users.append(subreddit_user[1])
            elif isinstance(subreddit_user, str):
                if (subreddit or self.subreddit) is None:
                    raise ValueError(
                        "`subreddit` must be provided if `ModNotes.subreddit` is not set."
                    )
                subreddits.append(subreddit or self.subreddit)
                users.append(subreddit_user)
            else:
                raise ValueError(
                    f"Cannot get subreddit and user fields from type {type(subreddit_user)}"
                )

        if all_notes:
            for redditor, subreddit in zip(users, subreddits):
                yield from self._all_generator(redditor, subreddit, **generator_kwargs)
        else:
            yield from self._bulk_generator(subreddits, users)

    def __init__(
        self, reddit: "praw.Reddit", subreddit: "praw.models.Subreddit" = None
    ):
        """Create a ModNotes instance.

        :param reddit: An instance of :class:`.Reddit`.
        :param subreddit: The subreddit associated with the notes.

        """
        self._reddit = reddit
        self.subreddit = subreddit

    def create(
        self,
        *,
        label: Optional[str] = None,
        note: str,
        redditor: Union[str, "praw.models.Redditor"],
        subreddit: Union[str, "praw.models.Subreddit"] = None,
        thing: Optional[
            Union[str, "praw.models.Comment", "praw.models.Submission"]
        ] = None,
        **other_settings: Any,
    ) -> "praw.models.ModNote":
        """Create a note for a redditor in this subreddit.

        :param redditor: The redditor to create the note for.
        :param note: The content of the note, limited to 250 characters.
        :param label: The label to create the note under, can be ``None`` or one of
            ``"BOT_BAN"``, ``"PERMA_BAN"``, ``"BAN"``, ``"ABUSE_WARNING"``,
            ``"SPAM_WARNING"``, ``"SPAM_WATCH"``, ``"SOLID_CONTRIBUTOR"``,
            ``"HELPFUL_USER"`` (default: ``None``).
        :param subreddit: The subreddit associated with the note. If ``None``, uses this
            instance's ``subreddit`` (default: ``None``). This is required if ``thing``
            is not provided and this instance's ``subreddit`` is ``None``.
        :param thing: Either the fullname of a comment/submission, a :class:`.Comment`,
            or a :class:`.Submission` to associate with the note.

        :returns: The newly created :class:`.ModNote`.

        """
        if not subreddit:
            if thing:
                subreddit = thing.subreddit
            elif self.subreddit:
                subreddit = self.subreddit
            else:  # this is only reachable from praw.Reddit.mod_notes
                raise ValueError("`subreddit` or `thing` must be provided.")
        if not redditor:
            if thing:
                redditor = thing.author
            else:
                raise ValueError("`redditor` or `thing` must be provided.")
        data = {
            "user": str(redditor),
            "subreddit": str(subreddit),
            "note": note,
        }
        if label:
            data["label"] = label
        if thing:
            data["thing"] = str(thing.fullname)
        data.update(other_settings)
        return self._reddit.post(API_PATH["mod_notes"], data=data)

    def delete(
        self,
        *,
        delete_all: bool = False,
        note_id: str = None,
        redditor: Union[str, "praw.models.Redditor"] = None,
    ):
        """Delete a note for a redditor.

        :param delete_all: When ``True``, delete all notes for the given
            :class:`.Redditor` (default: ``False``).
        :param note_id: The ID of the note to delete. This is ignored if ``delete_all``
            is ``True``.
        :param redditor: The :class:`.Redditor` to delete the note from.

        For example, to delete a note with the ID
        ``"ModNote_d324b280-5ecc-435d-8159-3e259e84e339"``, try:

        .. code-block:: python

            reddit.subreddit("redditdev").mod.notes.delete(
                redditor="spez", note_id="ModNote_d324b280-5ecc-435d-8159-3e259e84e339"
            )

        To delete all notes for u/spez, try:

        .. code-block:: python

            reddit.subreddit("redditdev").mod.notes.delete(redditor="spez", delete_all=True)

        .. note::

            This will make consume a request for each note.

        """
        if delete_all:
            for note in self(redditor):
                note.delete()
        elif (redditor, note_id).count(None) == 1:
            raise TypeError(
                "Either `redditor` and `note_id`, or `redditor` and `delete_all` must be provided."
            )
        params = {
            "user": str(redditor),
            "subreddit": str(self.subreddit),
            "note_id": note_id,
        }
        self._reddit.delete(API_PATH["mod_notes"], params=params)
