import pytest
from playwright.sync_api import expect
from tests.ui.pages.port_setup_page import PortSetupPage
from tests.ui.pages.optimization_results_page import Optimization_Result_Page


@pytest.mark.order(1)
def test_open_port_setup_page(browser_page, base_url, login):
    """Check that Port Setup page elements are visible after login."""
    port_setup = PortSetupPage(browser_page, base_url)
    port_setup.open_port_setup()

    # Assertions for key elements visibility
    expect(port_setup.port_setup_section, "Port Setup header is not visible").to_be_visible()
    expect(port_setup.save_changes_btn, "Save Changes button is not visible").to_be_visible()
    expect(port_setup.cost_storage_input, "Cost: Storage input is not visible").to_be_visible()
    expect(port_setup.cost_handling_input, "Cost: Handling input is not visible").to_be_visible()
    expect(port_setup.empty_available_input, "Empty Available input is not visible").to_be_visible()


@pytest.mark.order(2)
def test_update_numeric_fields(browser_page, base_url):
    """Test updating Cost: Storage, Cost: Handling, Empty Available fields."""
    port_page = PortSetupPage(browser_page, base_url)

    # Read current values
    before_storage = port_page.get_storage_value()
    before_handling = port_page.get_handling_value()
    before_empty = port_page.get_empty_available_value()

    # Update values
    port_page.change_storage_value(before_storage + 1)
    port_page.change_handling_value(before_handling + 1)
    port_page.change_empty_available_value(before_empty + 1)

    # Save changes
    port_page.click_save_changes()

    # Re-open page to read updated values
    port_page.open_port_setup()
    after_storage = port_page.get_storage_value()
    after_handling = port_page.get_handling_value()
    after_empty = port_page.get_empty_available_value()

    # Assertions with descriptive failure messages
    assert after_storage == before_storage + 1, f"Cost: Storage did not update correctly (before: {before_storage}, after: {after_storage})"
    assert after_handling == before_handling + 1, f"Cost: Handling did not update correctly (before: {before_handling}, after: {after_handling})"
    assert after_empty == before_empty + 1, f"Empty Available did not update correctly (before: {before_empty}, after: {after_empty})"


@pytest.mark.parametrize("role, trans_shipment", [
    ("full access", True),
    ("repositioning disabled", False),
    ("outbound only", True),
    ("inbound only", False)
])
def test_change_role_and_transshipment(browser_page, base_url, role, trans_shipment):
    """Test all Role dropdown options and Trans-shipment toggle state."""
    port_page = PortSetupPage(browser_page, base_url)

    # Change role
    port_page.select_role(role)

    # Ensure toggle is in expected state
    current_toggle = port_page.get_trans_shipment_state()
    if current_toggle != trans_shipment:
        port_page.toggle_trans_shipment()

    # Save changes
    port_page.click_save_changes()

    # Re-open page
    port_page.open_port_setup()

    # Assertions with clear messages
    selected_role = port_page.get_selected_role()
    toggle_state = port_page.get_trans_shipment_state()
    assert selected_role == role, f"Role selection failed: expected '{role}', got '{selected_role}'"
    assert toggle_state == trans_shipment, f"Trans-shipment toggle state failed for role '{role}': expected {trans_shipment}, got {toggle_state}"


@pytest.mark.order(3)
def test_optimization_result_page(browser_page, base_url):
    """Verify Optimization Result page is loaded after Port Setup changes."""
    opt_result = Optimization_Result_Page(browser_page, base_url)
    # Use expect for visibility with descriptive message
    expect(opt_result.optimization_result_section, "Optimization Result section is not visible").to_be_visible()
@pytest.mark.order(4)
def test_cancel_button(browser_page, base_url):
    """Check that Cancel button discards changes and original values remain."""
    port_page = PortSetupPage(browser_page, base_url)

    # Open Port Setup page
    port_page.open_port_setup()

    # Read current values
    original_storage = port_page.get_storage_value()
    original_handling = port_page.get_handling_value()
    original_empty = port_page.get_empty_available_value()

    # Make changes
    port_page.change_storage_value(original_storage + 5)
    port_page.change_handling_value(original_handling + 5)
    port_page.change_empty_available_value(original_empty + 5)

    # Click Cancel
    port_page.click_cancel()

    # Re-open Port Setup page to verify values
    port_page.open_port_setup()

    # Assertions: values should remain unchanged
    assert port_page.get_storage_value() == original_storage, (
        f"Cost: Storage changed after clicking Cancel (expected {original_storage})"
    )
    assert port_page.get_handling_value() == original_handling, (
        f"Cost: Handling changed after clicking Cancel (expected {original_handling})"
    )
    assert port_page.get_empty_available_value() == original_empty, (
        f"Empty Available changed after clicking Cancel (expected {original_empty})"
    )
