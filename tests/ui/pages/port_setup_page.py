from playwright.sync_api import expect
from tests.ui.pages.base_page import BasePage

class PortSetupPage(BasePage):
    """Page object model for the PortSetup page."""
    def __init__(self, page, base_url):
        super().__init__(page)
        self.base_url = base_url

        # ---------- Port Setup page elements ----------
        self.port_setup_section = page.get_by_text("Ports Setup", exact=True)
        self.port_setup_content = page.locator("div", has_text="Ports Setup")
        self.save_changes_btn = page.get_by_role("button", name="Save Changes")
        self.cancel_btn = page.get_by_role("button", name="Cancel")

        # Dropdown / Role button
        self.role_btn = page.get_by_role("button", name="outbound only")

        # Toggle
        self.trans_shipment_toggle = page.locator("button[aria-pressed]")

        # Numeric inputs
        self.cost_storage_input = page.locator("input[type='number'][inputmode='decimal']").nth(0)
        self.cost_handling_input = page.locator("input[type='number'][inputmode='decimal']").nth(1)
        self.empty_available_input = page.locator("input[type='number'][inputmode='decimal']").nth(2)

        # Dropdown options
        self.full_access_option = page.get_by_role("option", name="full access")
        self.repositioning_disabled_option = page.get_by_role("option", name="repositioning disabled")
        self.outbound_only_option = page.get_by_role("option", name="outbound only")
        self.inbound_only_option = page.get_by_role("option", name="inbound only")

    # ---------- Page actions ----------

    def open_port_setup(self):
        """Navigate to the Port Setup page."""
        self.port_setup_section.click()

    def click_save_changes(self):
        expect(self.save_changes_btn).to_be_enabled()
        self.save_changes_btn.click()

    def click_cancel(self):
        expect(self.cancel_btn).to_be_enabled()
        self.cancel_btn.click()

    # ---------- Dropdown / Role ----------

    def select_role(self, role_name: str):
        """Select a role from the dropdown."""
        self.role_btn.click()  # open dropdown
        option = self.page.get_by_role("option", name=role_name)
        option.click()

    def get_selected_role(self) -> str:
        """Return the currently selected role."""
        return self.role_btn.inner_text()

    # ---------- Toggle ----------

    def toggle_trans_shipment(self):
        """Toggle the Trans-shipment button."""
        self.trans_shipment_toggle.click()

    def get_trans_shipment_state(self) -> bool:
        """Return True if toggle is ON, False if OFF."""
        state = self.trans_shipment_toggle.get_attribute("aria-pressed")
        return state == "true"

    # ---------- Numeric fields ----------

    def get_storage_value(self) -> int:
        expect(self.cost_storage_input).to_be_visible()
        return int(self.cost_storage_input.input_value())

    def change_storage_value(self, value: int):
        expect(self.cost_storage_input).to_be_enabled()
        self.cost_storage_input.fill(str(value))

    def get_handling_value(self) -> int:
        expect(self.cost_handling_input).to_be_visible()
        return int(self.cost_handling_input.input_value())

    def change_handling_value(self, value: int):
        expect(self.cost_handling_input).to_be_enabled()
        self.cost_handling_input.fill(str(value))

    def get_empty_available_value(self) -> int:
        expect(self.empty_available_input).to_be_visible()
        return int(self.empty_available_input.input_value())

    def change_empty_available_value(self, value: int):
        expect(self.empty_available_input).to_be_enabled()
        self.empty_available_input.fill(str(value))
