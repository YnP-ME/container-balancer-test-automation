import os
import yaml
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from ui.pages.login_page import LoginPage
from ui.pages.base_page import BasePage

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


# ---------- Load config ----------
def load_config():
    config_path = os.path.join(
        os.path.dirname(__file__),
        "config",
        "config.yaml"
    )
    with open(config_path) as f:
        return yaml.safe_load(f)


# ---------- CLI options (HOOK) ----------
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser: chromium, firefox, webkit"
    )
    parser.addoption(
        "--env",
        action="store",
        default="staging",
        help="Environment name"
    )


# ---------- Fixtures ----------
@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(scope="session")
def base_url(request, config):
    active_env = (
        request.config.getoption("--env")
        or os.getenv("TEST_ENV")
        or config.get("default_env", "staging")
    )

    url = config["environments"][active_env]
    print(f"\nRunning tests against: {active_env} → {url}")
    return url


@pytest.fixture(scope="session")
def browser_page(request, config):
    browser_name = (
        request.config.getoption("--browser")
        or os.getenv("BROWSER")
        or config["browser"]["default"]
    )

    headless_mode = os.getenv("CI") == False

    playwright = sync_playwright().start()

    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=headless_mode)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless_mode)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=headless_mode)
    else:
        raise ValueError(f"Unknown browser: {browser_name}")

    context = browser.new_context()
    page = context.new_page()
    def teardown():
        page.close()
        context.close()
        browser.close()
        playwright.stop()


    request.addfinalizer(teardown)
    return page

@pytest.fixture
def login(browser_page, base_url):
    base = BasePage(browser_page)
    login = LoginPage(browser_page, base_url)
    login.open_login()
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()
    expect(base.logout_button, "Exit button not visible after admin login").to_be_visible()
