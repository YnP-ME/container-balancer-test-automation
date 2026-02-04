import pytest
from playwright.sync_api import expect
from tests.ui.pages.port_setup_page import PortSetupPage
from tests.ui.pages.optimization_results_page import Optimization_Result_Page


def test_open_port_setup_page(browser_page, base_url, login):
    port_setup = PortSetupPage(browser_page, base_url)
    port_setup.open_port_setup()

    expect(port_setup.port_setup_content).to_be_visible()
    expect(port_setup.save_changes_btn).to_have_count(1)
    expect(port_setup.cost_storage_input).to_be_visible()
    expect(port_setup.cost_handling_input).to_be_visible()
    expect(port_setup.empty_available_input).to_be_visible()


def test_update_numeric_fields(browser_page, base_url, login):
    port_page = PortSetupPage(browser_page, base_url)
    opt_result = Optimization_Result_Page(browser_page, base_url)

    port_page.open_port_setup()

    before_storage = port_page.get_storage_value()
    before_handling = port_page.get_handling_value()
    before_empty = port_page.get_empty_available_value()

    port_page.change_storage_value(before_storage + 1)
    port_page.change_handling_value(before_handling + 1)
    port_page.change_empty_available_value(before_empty + 1)

    port_page.click_save_changes()

    expect(opt_result.optimization_result_section).to_be_visible(timeout=20000)

    port_page.open_port_setup()

    assert port_page.get_storage_value() == before_storage + 1
    assert port_page.get_handling_value() == before_handling + 1
    assert port_page.get_empty_available_value() == before_empty + 1


def test_cancel_button(browser_page, base_url, login):
    port_page = PortSetupPage(browser_page, base_url)
    port_page.open_port_setup()

    original_storage = port_page.get_storage_value()
    original_handling = port_page.get_handling_value()
    original_empty = port_page.get_empty_available_value()

    port_page.change_storage_value(original_storage + 5)
    port_page.change_handling_value(original_handling + 5)
    port_page.change_empty_available_value(original_empty + 5)

    port_page.click_cancel()

    port_page.open_port_setup()

    assert port_page.get_storage_value() == original_storage
    assert port_page.get_handling_value() == original_handling
    assert port_page.get_empty_available_value() == original_empty


def test_change_all_roles_and_toggle(browser_page, base_url, login):
    all_roles = [
        "inbound only",
        "full access",
        "repositioning disabled",
        "outbound only",
    ]

    port_page = PortSetupPage(browser_page, base_url)
    port_page.open_port_setup()

    for role in all_roles:
        port_page.select_role(role)

        current_toggle = port_page.get_trans_shipment_state()
        port_page.toggle_trans_shipment()

        port_page.click_save_changes()
        port_page.open_port_setup()

        assert port_page.get_selected_role() == role
        assert port_page.get_trans_shipment_state() != current_toggle
