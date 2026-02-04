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


def test_login_page_elements_before_login(browser_page, base_url):
    """Check that all login page elements are visible before login."""
    browser_page.goto(base_url)  # <<< ensure browser is on the URL

    login = LoginPage(browser_page, base_url)
    login.open_login()

    # Assertions for page elements visibility
    expect(login.login_page_title, "Login page title is not visible").to_be_visible(timeout=20000)
    expect(login.username_input, "Username input is not visible").to_be_visible(timeout=20000)
    expect(login.password_input, "Password input is not visible").to_be_visible()
    expect(login.login_button, "Login button is not visible").to_be_visible()


def test_login(browser_page, base_url):
    """User can log in successfully and see expected elements."""
    browser_page.goto(base_url)

    login = LoginPage(browser_page, base_url)
    login.open_login()
    login.enter_username(USERNAME)
    login.enter_password(PASSWORD)
    login.click_login()

    base = BasePage(browser_page)

    # Assertions for admin login success
    expect(base.logout_button, "Exit button not visible after login").to_be_visible(timeout=20000)
    expect(base.page_title, "Header is not visible").to_be_visible(timeout=20000)
    expect(base.impact_report_button, "Report button is not visible").to_be_visible(timeout=20000)


def test_logout(browser_page, base_url,login):
    """Test logout functionality and returning to login page."""
    browser_page.goto(base_url)

    base = BasePage(browser_page)
    login = LoginPage(browser_page, base_url)

    # Click logout
    base.click_logout()

    # Assertions for returned login page
    expect(login.username_input, "Username input is not visible").to_be_visible(timeout=20000)
    expect(login.password_input, "Password input is not visible").to_be_visible(timeout=20000)
    expect(login.login_button, "Login button is not visible").to_be_visible(timeout=20000)