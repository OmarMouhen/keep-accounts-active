from datetime import datetime, timezone
import logging

def get_datetime():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S:%f")

def get_datestamp():
    return get_datetime().split()[0]

def get_timestamp():
    return get_datetime().split()[1]

def get_year():
    return get_datestamp().split("-")[0]

Year = get_year()

class CsvFormatter(logging.Formatter):
    def format(self, record):
        date = get_datestamp()
        time = get_timestamp()
        level = record.levelname
        msg = record.getMessage()
        return f'"{date}","{time}","{level}","{msg}"'
