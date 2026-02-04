from playwright.async_api import expect
from tests.ui.pages.base_page import BasePage

class Optimization_Result_Page(BasePage):
    """Page object model for the Optimization Result page."""
    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url

        # ---------- Optimization Result  page elements ----------
        self.optimization_result_section = page.get_by_text("Optimization Result", exact=False)
        self.optimization_result_table_container = page.locator("div.min-h-0.flex-1.overflow-y-auto")

    def is_page_opened(self):
        """Fail test if page is not loaded."""
        expect( self.optimization_result_section,"Optimization Result header is not visible").to_be_visible()
        expect(self.optimization_result_table_container,"Optimization Result table container is not visible").to_be_visible()

