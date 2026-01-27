
class BasePage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

        # Header / always visible elements
        self.logout_button = page.get_by_role("button", name="Logout")
        self.impact_report_button = page.get_by_role("link", name="Impact report")
        self.page_title = page.get_by_role("heading", name="Container Balancer")

        # Default landing section elements
        self.container_table = page.locator("[data-testid='container-table']")
        self.refresh_button = page.locator("button:has-text('Refresh')")

    def open_base(self, url):
        """Navigate to a base page."""
        return self.page.goto(url)


