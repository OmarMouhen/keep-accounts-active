from playwright.sync_api import sync_playwright, TimeoutError

class LoginLogger:
    def __init__(self, base_url, login_url, usr_sel, usr, pwd_sel, pwd, homepage, filename):
        self.base_url = base_url
        self.login_url = login_url
        self.usr_sel = usr_sel
        self.usr = usr
        self.pwd_sel = pwd_sel
        self.pwd = pwd
        self.homepage = homepage
        self.filename = filename

        from logging_formatter import CsvFormatter
        self.formatter = CsvFormatter(self.filename)
        self.logger = self.formatter.logger
        self.DuoHandler = self.formatter.handler

    def one_step_login(self, pw, submit_btn_sel):
        browser = pw.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        self.logger.info(f"Opening login page {self.login_url}")
        page.goto(self.login_url)

        self.logger.info(f"Typing email: {self.usr}")
        page.fill(self.usr_sel, self.usr)

        self.logger.info("Clicking Next/Login")
        page.click("button.login-button")

        # Wait for password field
        page.wait_for_selector(self.pwd_sel)
        self.logger.info("Typing password")
        page.fill(self.pwd_sel, self.pwd)

        self.logger.info("Clicking final login button")
        page.click(submit_btn_sel)

        try:
            self.logger.info("Waiting for MEGA UI to appear...")
            page.wait_for_selector("#fmholder", timeout=120000)
            self.logger.info(f"✅ Login successful. Landed on: {page.url}")
        except TimeoutError:
            self.logger.error("❌ TimeoutError: MEGA interface did not load in time.")
            page.screenshot(path="mega_login_failed.png")
            raise

        self.browser = browser
        self.context = context
        self.tab = page
        self.dashboard_url = page.url

    def redirect(self, href_sel):
        self.logger.info(f"Redirecting to profile using selector: {href_sel}")
        self.tab.click(href_sel)
        self.tab.wait_for_load_state("domcontentloaded")
