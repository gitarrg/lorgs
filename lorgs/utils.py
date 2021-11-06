
from operator import attrgetter
import asyncio
import datetime
import functools
import itertools
import typing

import arrow


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    if n <= 0: # special case to allow unchucked
        yield lst
        return

    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def format_time(timestamp: int):
    """Format a time/duration.

    Args:
        timestamp: time in milliseconds

    Example:
        >>> format_time(272000)
        "4:32"

    """
    duration = datetime.timedelta(milliseconds=timestamp)

    duration_str = str(duration) # "0:05:12.00000"
    duration_str = duration_str[2:7]
    return duration_str


def format_timestamp(timestamp):
    if timestamp == 0:
        return "never"

    t = arrow.get(timestamp)
    return t.strftime("%H:%M %d.%m.%Y")


def format_big_number(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'k', 'm', 'g', 't', 'p'][magnitude])


def slug(text, space=""):
    text = text.lower()
    text = text.replace("'", "")
    text = text.replace("-", "")
    text = text.replace(" ", space)
    return text


def str_int_list(string, sep="."):
    """Converts string-list of intergers into an actual list."""
    if not string:
        return []

    return [int(v) for v in string.split(sep)]


def get_nested_value(dct: typing.Dict[str, typing.Any], *keys: str, default=None):

    data = dct
    for key in keys:
        data = data or {}
        try:
            data = data[key]
        except KeyError:
            return default

    return data


def flatten(l):
    """Flattens a list of lists into a single large list.

    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
    """
    return list(itertools.chain.from_iterable(l))


def as_list(func):
    """Wrap a Generator to return a list."""
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return list(func(*args, **kwargs))

    return wrapped

def uniqify(iterable, key):
    d = {key(item): item for item in iterable}
    return list(d.values())


def find(predicate, seq):
    """A helper to return the first element found in the sequence
    that meets the predicate. For example: ::

        member = discord.utils.find(lambda m: m.name == 'Mighty', channel.guild.members)

    would find the first :class:`~discord.Member` whose name is 'Mighty' and return it.
    If an entry is not found, then ``None`` is returned.

    This is different from :func:`py:filter` due to the fact it stops the moment it finds
    a valid entry.

    Parameters
    -----------
    predicate
        A function that returns a boolean-like result.
    seq: iterable
        The iterable to search through.
    """

    for element in seq:
        if predicate(element):
            return element
    return None


def get(iterable, **attrs):
    r"""A helper that returns the first element in the iterable that meets
    all the traits passed in ``attrs``. This is an alternative for
    :func:`~discord.utils.find`.

    When multiple attributes are specified, they are checked using
    logical AND, not logical OR. Meaning they have to meet every
    attribute passed in and not one of them.

    To have a nested attribute search (i.e. search by ``x.y``) then
    pass in ``x__y`` as the keyword argument.

    If nothing is found that matches the attributes passed, then
    ``None`` is returned.

    Examples
    ---------

    Basic usage:

    .. code-block:: python3

        member = discord.utils.get(message.guild.members, name='Foo')

    Multiple attribute matching:

    .. code-block:: python3

        channel = discord.utils.get(guild.voice_channels, name='Foo', bitrate=64000)

    Nested attribute matching:

    .. code-block:: python3

        channel = discord.utils.get(client.get_all_channels(), guild__name='Cool', name='general')

    Parameters
    -----------
    iterable
        An iterable to search through.
    \*\*attrs
        Keyword arguments that denote attributes to search with.
    """

    # global -> local
    _all = all
    attrget = attrgetter

    # Special case the single element call
    if len(attrs) == 1:
        k, v = attrs.popitem()
        pred = attrget(k.replace('__', '.'))
        for elem in iterable:
            if pred(elem) == v:
                return elem
        return None

    converted = [
        (attrget(attr.replace('__', '.')), value)
        for attr, value in attrs.items()
    ]

    for elem in iterable:
        if _all(pred(elem) == value for pred, value in converted):
            return elem
    return None


def run_in_executor(_func):
    """Wraps a function to run inside the asyncio default executor.

    We can use this to make blocking functions async (more or less)

    """
    @functools.wraps(_func)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        func = functools.partial(_func, *args, **kwargs)
        return loop.run_in_executor(executor=None, func=func)

    return wrapped

