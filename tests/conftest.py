import os
import yaml
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect
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


@pytest.fixture
def browser_page():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    yield page   # test runs here

    context.close()
    browser.close()
    playwright.stop()


@pytest.fixture
def login(browser_page, base_url):
    base = BasePage(browser_page)
    login_page = LoginPage(browser_page, base_url)

    # Always start from clean URL
    browser_page.goto(base_url)

    login_page.open_login()
    login_page.enter_username(USERNAME)
    login_page.enter_password(PASSWORD)
    login_page.click_login()

    # Strong sync point (important)
    expect(base.logout_button).to_be_visible()
