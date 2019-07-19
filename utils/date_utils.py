from datetime import datetime, timedelta


def strip_time(dt):
    return datetime(dt.year, dt.month, dt.day, 0, 0, 0, 0)


def last_week_pair():
    today = strip_time(datetime.now())
    return today - timedelta(days=6), today - timedelta(days=1)
