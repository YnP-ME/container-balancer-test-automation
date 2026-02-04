import time
from tests.ui.pages.base_page import BasePage

class LoginPage(BasePage):
    """Page object model for the login page."""
    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url
        self.url = f"{base_url}login"

        # ---------- Login page elements ----------
        self.login_page_title = page.get_by_alt_text("Logo ADP")
        self.login_form = page.locator("form")
        self.username_input = page.locator('input[placeholder="Enter your login"]')
        self.password_input = page.locator('input[placeholder="Enter your password"]')
        self.login_button = page.locator('button[type="submit"].bg-brand-500')
        self.invalid_login_error = page.get_by_text("Incorrect login or password", exact=True)


    # ---------- Page actions ----------
    def open_login(self):
        """Navigate to the login page."""
        return self.goto(self.url)

    def enter_username(self, username):
        """Fill in the username field."""
        time.sleep(3)
        self.username_input.fill(username)

    def enter_password(self, password):
        """Fill in the password field."""
        time.sleep(3)
        self.password_input.fill(password)

    def click_login(self):
        # Wait until button is enabled AND visible
        loader = self.page.locator('[role="status"][aria-busy="true"]')
        # Wait for overlay to disappear
        try:
            loader.wait_for(state="hidden", timeout=30000)
        except:
            pass
        # Click when fully ready
        self.login_button.click()








