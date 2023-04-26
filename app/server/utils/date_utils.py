import datetime
import time


def has_expired(expiry: int):
    return expiry <= int(round(time.time() * 1000))


def get_current_timestamp():
    return int(round(time.time() * 1000))


def get_current_date_time():
    return datetime.datetime.now()
