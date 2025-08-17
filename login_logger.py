import sys
sys.dont_write_bytecode = True

from datetime import datetime, timezone
import logging
import csv
import io
import os

def get_datetime():
    datetimestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S:%f")
    return datetimestamp

def get_datestamp():
    datestamp = get_datetime().split()[0]
    return datestamp

def get_timestamp():
    timestamp = get_datetime().split()[1]
    return timestamp

def get_year():
    year = get_datestamp().split("-")[0]
    return year

Year = get_year()

class CsvFormatter:
    def __init__(self, filename):
        self.output = io.StringIO()
        self.filename = filename
        self.fieldnames = ["Date", "Time", "Level", "Message"]
        self.csvfile = None

        # File writer setup
        if os.path.isfile(self.filename):
            self.csvfile = open(self.filename, "a+", newline="", encoding="utf-8")
        else:
            self.csvfile = open(self.filename, "w+", newline="", encoding="utf-8")
        
        self.file_writer = csv.DictWriter(
            self.csvfile,
            quoting=csv.QUOTE_ALL,
            fieldnames=self.fieldnames,
            extrasaction="ignore"
        )

        if os.path.getsize(self.filename) == 0:
            self.file_writer.writeheader()

        # Stream handler (console) writer
        self.console_writer = csv.writer(
            self.output, quoting=csv.QUOTE_MINIMAL, delimiter="\t"
        )

    def format(self, record):
        Date = get_datestamp()
        Time = get_timestamp()
        self.file_writer.writerow(
            {
                "Date": Date,
                "Time": Time,
                "Level": record.levelname,
                "Message": record.msg,
            }
        )
        self.console_writer.writerow([Date, Time, record.levelname, record.msg])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()

    def close(self):
        if self.csvfile:
            self.csvfile.close()
