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

        # CSV Formatter
        self.formatter = CsvFormatter(self.filename)

        # Setup logger
        self.logger = logging.getLogger(self.usr)
        self.logger.setLevel(logging.DEBUG)

        # Stream handler (console)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        self.logger.addHandler(stream_handler)

        # File handler using CsvFormatter
        file_handler = logging.StreamHandler(self.formatter.output)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

        # For reference when closing
        self.DuoHandler = file_handler
