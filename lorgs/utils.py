

from functools import wraps
import itertools
import datetime
import re


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def format_time(timestamp):

    t = datetime.timedelta(milliseconds=timestamp)

    t = str(t) # "0:05:12.00000"
    t = t[2:7]
    return t

    # minutes = timestamp

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


def flatten(l):
    """flattens a list of lists into a single large list.

    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
    """
    return list(itertools.chain.from_iterable(l))


def shrink_text(text):
    return re.sub(r"\s+", " ", text)


def as_list(func):
    """Wrap a Generator to return a list."""
    @wraps(func)
    def wrapped(*args, **kwargs):
        return list(func(*args, **kwargs))

    return wrapped
