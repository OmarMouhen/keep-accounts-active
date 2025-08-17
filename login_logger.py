from playwright.sync_api import sync_playwright
import logging
from logging_formatter import CsvFormatter, DuoHandler

class LoginLogger:
    def __init__(self, base_url, login_url, usr_sel, usr, pwd_sel, pwd, homepage, filename):
        self.logger = logging.getLogger(usr)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = CsvFormatter(filename)
        self.DuoHandler = DuoHandler(self.formatter)
        self.logger.addHandler(self.DuoHandler)
        self.base_url = base_url
        self.login_url = login_url
        self.usr_sel = usr_sel
        self.usr = usr
        self.pwd_sel = pwd_sel
        self.pwd = pwd
        self.homepage = homepage
        self.tab = None

    def one_step_login(self, pw, btn_sel):
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        self.tab = context.new_page()
        self.tab.goto(self.login_url)
        self.tab.fill(self.usr_sel, self.usr)
        self.tab.fill(self.pwd_sel, self.pwd)
        self.tab.click(btn_sel)
        self.tab.wait_for_url(self.homepage, timeout=20000)

    def redirect(self, href_sel):
        self.tab.click(href_sel)
        self.tab.wait_for_url("**/account", timeout=15000)
