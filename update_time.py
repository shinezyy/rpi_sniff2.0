import time

ISO_TIME_FORMAT = '%Y-%m-%d %X'

def get_current_time():
    return time.strftime(ISO_TIME_FORMAT,time.localtime())

MINUTE_TIME_FORMAT = '%X'

def get_current_minute():
    return time.time() / 3
