


import datetime


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
