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

        # 📝 Création du formatter CSV personnalisé
        self.formatter = CsvFormatter(filename)

        # 🧱 Création du handler de log (utilisé à la fois en fichier et console)
        self.DuoHandler = logging.StreamHandler(self.formatter.csvfile)
        self.DuoHandler.setFormatter(self.formatter)

        # 📒 Création du logger principal
        self.logger = logging.getLogger(f"logger_{usr}")
        self.logger.setLevel(logging.DEBUG)

        # Supprime les anciens handlers (évite duplication)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 🔗 Attache le handler personnalisé
        self.logger.addHandler(self.DuoHandler)

    def one_step_login(self, playwright, login_btn_selector):
        browser = playwright.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(self.login_url)

        page.fill(self.usr_sel, self.usr)
        page.fill(self.pwd_sel, self.pwd)
        self.logger.info("Submitting login form")
        page.click(login_btn_selector)
        page.wait_for_url(self.dashboard_url)

        self.logger.info("✅ Login successful")
        self.tab = page
        self.browser = browser
        self.context = context

    def redirect(self, href_sel):
        self.tab.wait_for_selector(href_sel)
        self.tab.click(href_sel)
        self.tab.wait_for_load_state("networkidle")
        self.logger.info(f"➡️ Redirected to: {self.tab.url}")
