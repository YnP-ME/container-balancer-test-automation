import shutil
from pathlib import Path
from playwright.sync_api import expect


class Optimization_Result_Page:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

        # -------- Main page --------
        self.opt_result_header = page.get_by_text("Optimization Result", exact=False)
        self.opt_result_table = page.locator("div.min-h-0.flex-1.overflow-y-auto")
        self.opt_result_section = page.get_by_text("Optimization Result")

        self.service_view_button = page.get_by_role("button", name="Service View")
        self.port_view_button = page.get_by_role("button", name="Port View")

        self.total_cost_section = page.locator("section:has-text('Total Cost')")
        self.download_csv_button = page.get_by_role("link", name="Download CSV")

        # -------- Dropdowns --------
        self.service_dropdown = page.locator("div.py-2.pr-4.align-top >> svg")
        self.vessel_dropdown = page.locator("div.py-2.text-sm.text-gray-900").nth(0).locator("xpath=preceding-sibling::svg | following-sibling::svg")
        self.departure_date_dropdown = page.locator("div.py-2.text-sm.text-gray-900").nth(1).locator("xpath=preceding-sibling::svg | following-sibling::svg")

        # -------- Port view --------
        self.port_view_table = page.locator("div.table-scrollbar table")

        self.port_column = page.get_by_text("Port")
        self.type_column = page.get_by_text("Type")
        self.gap_before_column = page.get_by_text("Gap: Before")
        self.gap_after_column = page.get_by_text("Gap: After")
        self.reason_column = page.get_by_text("Reason")

    # ---------- Page actions ----------

    def is_page_opened(self):
        expect(self.opt_result_header).to_be_visible()
        expect(self.opt_result_table).to_be_visible()

    def open_opt_result(self):
        self.opt_result_section.click()
        self.opt_result_table.wait_for(state="visible", timeout=15000)

    def open_port_view_page(self):
        self.port_view_button.click()

    # ---------- KPI ----------

    def get_kpi_value(self, label: str) -> str:
        return self.page.locator(
            f"section:has-text('{label}') div.text-brand-600"
        ).first.inner_text()

    # ---------- Service / Vessel / Date ----------

    def get_service_name(self) -> str:
        return self.page.locator("div.py-2.pr-4.align-top").inner_text()

    def click_service_dropdown(self):
        self.service_dropdown.click()

    def get_vessel_name(self) -> str:
        return self.page.locator("div.py-2.text-sm.text-gray-900").nth(0).inner_text()

    def click_vessel_dropdown(self):
        self.page.locator("svg.transition-colors.fill-black").first.click()

    def get_departure_date(self) -> str:
        return self.page.locator("div.py-2.text-sm.text-gray-900").nth(1).inner_text()

    def click_departure_date_dropdown(self):
        self.page.locator("svg.rotate-180.transition-colors").click()

    # ---------- CSV ----------

    def download_csv(self, download_dir="downloads"):
        Path(download_dir).mkdir(exist_ok=True)

        with self.page.expect_download(timeout=10000) as download_info:
            self.download_csv_button.click()

        download = download_info.value
        final_path = Path(download_dir) / download.suggested_filename

        shutil.move(download.path(), final_path)

        return final_path
