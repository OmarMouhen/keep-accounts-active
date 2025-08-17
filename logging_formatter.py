import logging
import datetime
import csv
import os

Year = datetime.datetime.now().year

class CsvFormatter(logging.Formatter):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.csvfile = open(filename, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csvfile)
        self.writer.writerow(["Level", "Message"])

    def format(self, record):
        self.writer.writerow([record.levelname, record.getMessage()])
        self.csvfile.flush()
        return super().format(record)

class DuoHandler(logging.Handler):
    def __init__(self, formatter):
        super().__init__()
        self.setFormatter(formatter)

    def emit(self, record):
        print(self.format(record))
