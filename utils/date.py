import datetime
from time import time

date_text_format = 'dd/MM/yyyy'
date_save_format = 'yyyy/MM/dd hh24:mi:ss'
date_save_format_length = 19

def format_to_save_date(date_string):
    return date_string.replace('T', ' ')[:date_save_format_length]

def format_to_iso(date):
    if isinstance(date, datetime.date):
        return date.isoformat()
    else:
        return None

def get_int_time():
    return int(time())

def get_year(date):
    position = 11
    year_length = 4

    return date[position:(position + year_length)]
