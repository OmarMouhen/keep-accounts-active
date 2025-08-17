import sys
import os
import json
import subprocess
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError
from login_logger import LoginLogger
from log_concat import update_logs
from logging_formatter import Year

sys.dont_write_bytecode = True
load_dotenv()

try:
    cred_dict = json.loads(os.getenv("MEGA"))
except json.JSONDecodeError:
    print("❌ Invalid MEGA credentials JSON format.")
    sys.exit(1)

mega = "https://mega.nz/"
mega_signin = mega + "login"
mega_usr_sel = "input#login-name2"
mega_pwd_sel = "input#login-password2"
mega_homepage = "https://mega.nz/fm/recents"

def mkfilename(a):
    return f"logs/mega/[{Year}] {a} log.csv"

def query_mega_storage(instance):
    page = instance.tab
    logger = instance.logger

    try:
        page.wait_for_selector("div.account.left-pane.info-block.backup-button", timeout=15000)
        name = page.query_selector("div.membership-big-txt.name").inner_text()
        email = page.query_selector("div.membership-big-txt.email").inner_text()
        plan = page.query_selector("div.account.membership-plan").inner_text()

        logger.info("✔️ Logged in successfully")
        logger.debug(f"Name: {name}, Email: {email}, Plan: {plan}")

        for category in page.query_selector_all("div.account.item-wrapper"):
            cname = category.query_selector("div.account.progress-title > span").inner_text()
            csize = category.query_selector("div.account.progress-size.small").inner_text()
            logger.debug(f"{cname}: {csize}")
    except Exception as e:
        logger.error(f"⚠️ Could not extract profile info: {e}")

def mega_login(instance):
    try:
        with sync_playwright() as pw:
            instance.one_step_login(pw, "#login_form button.login-button")
            instance.redirect(href_sel="a.mega-component.to-my-profile.nav-elem.text-only.link")
            query_mega_storage(instance)
            instance.logger.info("✅ Tasks complete, closing browser")
    except TimeoutError as e:
        instance.logger.error(f"❌ Timeout occurred: {e}")
        instance.tab.screenshot(path="mega_timeout.png")
        sys.exit(1)
    except Exception as e:
        instance.logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        instance.logger.removeHandler(instance.DuoHandler)
        instance.formatter.csvfile.close()

def push_logs_to_private_repo():
    token = os.getenv("LOGS_PUSH_TOKEN")
    if not token:
        print("❌ LOGS_PUSH_TOKEN not set.")
        return

    repo_url = f"https://x-access-token:{token}@github.com/OmarMouhen/mega-login-logs.git"

    try:
        os.chdir("logs")
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.email", "bot@github.com"], check=True)
        subprocess.run(["git", "config", "user.name", "GitHub Actions Bot"], check=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "📝 Update logs"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
        print("✅ Logs pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")

if __name__ == "__main__":
    for i, user in enumerate(cred_dict, start=1):
        instance = LoginLogger(
            base_url=mega,
            login_url=mega_signin,
            usr_sel=mega_usr_sel,
            usr=user,
            pwd_sel=mega_pwd_sel,
            pwd=cred_dict[user],
            homepage=mega_homepage,
            filename=mkfilename(f"mega_{i}")
        )
        mega_login(instance)
        update_logs(instance)

    push_logs_to_private_repo()
