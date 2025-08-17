import logging
from logging_formatter import CsvFormatter

class LoginLogger:
    def __init__(self, base_url, login_url, usr_sel, usr, pwd_sel, pwd, homepage, filename):
        self.base_url = base_url
        self.login_url = login_url
        self.usr_sel = usr_sel
        self.usr = usr
        self.pwd_sel = pwd_sel
        self.pwd = pwd
        self.dashboard_url = homepage
        self.filename = filename

        # CSV Formatter + FileHandler
        self.logger = logging.getLogger(f"mega_logger_{usr}")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        self.DuoHandler = logging.FileHandler(self.filename, encoding="utf-8")
        self.DuoHandler.setFormatter(CsvFormatter())
        self.logger.addHandler(self.DuoHandler)
