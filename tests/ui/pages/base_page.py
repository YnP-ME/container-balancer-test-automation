
class BasePage:
    def __init__(self, page):
        self.page = page

        # Header / always visible elements
        self.logout_button = page.get_by_role("button", name="Logout")
        self.impact_report_button = page.get_by_role("link", name="Impact report")
        self.page_title = page.get_by_role("heading", name="Container Balancer")

        # Default landing section elements
        self.container_table = page.locator("[data-testid='container-table']")
        self.refresh_button = page.locator("button:has-text('Refresh')")

    def goto(self, url):
        """Navigate to a given URL and return the response."""
        return self.page.goto(url)

    def click_logout(self):
       return self.logout_button.click()
