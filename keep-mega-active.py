import logging
from logging import StreamHandler
from logging import Logger
from logging import FileHandler
from logging import Formatter
import os
import io
import csv
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright


def get_datetime():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S:%f")


def get_datestamp():
    return get_datetime().split()[0]


def get_timestamp():
    return get_datetime().split()[1]


def get_year():
    return get_datestamp().split("-")[0]


Year = get_year()


class CsvFormatter:
    def __init__(self, filename):
        self.filename = filename
        self.fieldnames = ["Date", "Time", "Level", "Message"]
        self.csvfile = open(self.filename, "a+", newline="", encoding="utf-8")
        self.file_writer = csv.DictWriter(
            self.csvfile,
            quoting=csv.QUOTE_ALL,
            fieldnames=self.fieldnames,
            extrasaction="ignore",
        )
        if os.path.getsize(self.filename) == 0:
            self.file_writer.writeheader()

        self.console = io.StringIO()
        self.console_writer = csv.writer(
            self.console, quoting=csv.QUOTE_MINIMAL, delimiter="\t"
        )

    def format(self, level, msg):
        Date = get_datestamp()
        Time = get_timestamp()
        self.file_writer.writerow({
            "Date": Date,
            "Time": Time,
            "Level": level,
            "Message": msg
        })
        self.console_writer.writerow([Date, Time, level, msg])
        data = self.console.getvalue()
        self.console.truncate(0)
        self.console.seek(0)
        return data.strip()

    def close(self):
        self.csvfile.close()


class LoginLogger:
    def __init__(self, base_url, login_url, usr_sel, usr, pwd_sel, pwd, homepage, filename):
        self.logger = logging.getLogger(usr)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = CsvFormatter(filename)

        # Custom handler writing both to file and console
        self.DuoHandler = logging.Handler()
        self.DuoHandler.emit = self._emit
        self.logger.addHandler(self.DuoHandler)

        # Required for browser session
        self.base_url = base_url
        self.login_url = login_url
        self.usr_sel = usr_sel
        self.usr = usr
        self.pwd_sel = pwd_sel
        self.pwd = pwd
        self.homepage = homepage
        self.tab = None

    def _emit(self, record):
        msg = self.formatter.format(record.levelname, record.getMessage())
        print(msg)

    def one_step_login(self, pw: sync_playwright, login_btn_sel: str):
        browser = pw.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        self.tab = page
        page.goto(self.login_url)
        page.fill(self.usr_sel, self.usr)
        page.fill(self.pwd_sel, self.pwd)
        page.click(login_btn_sel)
        page.wait_for_url(self.homepage, timeout=15000)

    def redirect(self, href_sel):
        self.tab.click(href_sel)
        self.tab.wait_for_url("**/account", timeout=15000)
