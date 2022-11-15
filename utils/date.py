import datetime
from time import time

date_text_format = 'dd/MM/yyyy'

def format_to_iso(date):
    if isinstance(date, datetime.date):
        return date.isoformat()
    else:
        return None

def get_int_time():
    return int(time())
