


import datetime

def format_time(timestamp):

    t = datetime.timedelta(milliseconds=timestamp)

    t = str(t) # "0:05:12.00000"
    t = t[2:7]
    return t

    # minutes = timestamp
