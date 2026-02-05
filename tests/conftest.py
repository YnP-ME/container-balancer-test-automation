import os
import yaml
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect

from ui.pages.login_page import LoginPage
from ui.pages.base_page import BasePage


# ---------- ENV ----------
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


# ---------- CLI options ----------
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
def playwright_instance():
    """Start Playwright once per test session (Allure-safe)"""
    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser_page(playwright_instance, request):
    """Fresh browser per test"""

    browser_name = request.config.getoption("--browser")

    browser = getattr(playwright_instance, browser_name).launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    yield page

    context.close()
    browser.close()


@pytest.fixture
def login(browser_page, base_url):
    """Login before test"""

    base = BasePage(browser_page)
    login_page = LoginPage(browser_page, base_url)

    browser_page.goto(base_url)
    login_page.open_login()
    login_page.enter_username(USERNAME)
    login_page.enter_password(PASSWORD)
    login_page.click_login()

    expect(base.logout_button).to_be_visible(timeout=10000)

    return browser_page
