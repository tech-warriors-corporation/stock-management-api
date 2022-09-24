import datetime

def format_to_iso(date):
    if isinstance(date, datetime.date):
        return date.isoformat()
    else:
        return None
