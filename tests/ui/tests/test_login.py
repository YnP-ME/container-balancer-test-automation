import time
import pytest
from playwright.sync_api import expect
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.base_page import BasePage

import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

@pytest.mark.order(1)
def test_login_page_elements_before_login(browser_page, base_url):
    """Check that all login page elements are visible before login."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    # Assertions for page elements visibility
    expect(login.login_page_title, "Login page title is not visible").to_be_visible()
    expect(login.username_input, "Username input is not visible").to_be_visible()
    expect(login.password_input, "Password input is not visible").to_be_visible()
    expect(login.login_button, "Login button is not visible").to_be_visible()

@pytest.mark.order(2)
def test_valid_login(browser_page, base_url, config):
    """User can log in successfully and see expected elements."""
    login = LoginPage(browser_page, base_url)
    login.open_login()

    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()
    base = BasePage(browser_page, base_url)
    base.open_base()

    # Assertions for admin login success
    expect(base.logout_button, "Exit button not visible after admin login").to_be_visible()
    expect(base.page_title, "Header is not visible").to_be_visible()
    expect(base.impact_report_button, "Report button is not visible").to_be_visible()


@pytest.mark.order(3)
def test_logout(browser_page, base_url):
    """Test logout functionality and returning to login page."""
    base = BasePage(browser_page, base_url)
    login = LoginPage(browser_page, base_url)

    # Click logout
    base.click_logout()
    time.sleep(1)

    # Assertions for returned login page
    expect(login.username_input, "Username input is not visible").to_be_visible()
    expect(login.password_input, "Password input is not visible").to_be_visible()
    expect(login.login_button, "Login button is not visible").to_be_visible()