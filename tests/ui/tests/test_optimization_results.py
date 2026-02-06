import csv
import allure
import pytest
from playwright.sync_api import expect
from tests.ui.pages.optimization_results_page import Optimization_Result_Page


# Test: Optimization Result page opens correctly
def test_open_opt_result_page(browser_page, base_url, login):
    # Create page object
    opt_result = Optimization_Result_Page(browser_page, base_url)

    # Navigate to Optimization Result section
    opt_result.open_opt_result()

    # Basic page load validations
    opt_result.is_page_opened()

    # Verify key UI elements are visible
    expect(opt_result.service_view_button).to_be_visible()
    expect(opt_result.port_view_button).to_be_visible()
    expect(opt_result.total_cost_section).to_be_visible()
    expect(opt_result.download_csv_button).to_be_visible()


# Test: Service / Vessel / Date dropdowns change value
def test_service_view(browser_page, base_url, login):
    opt_result = Optimization_Result_Page(browser_page, base_url)
    opt_result.open_opt_result()

    # ----- Service -----
    service_before = opt_result.get_service_name()
    opt_result.click_service_dropdown()
    service_after = opt_result.get_service_name()

    # ----- Vessel -----
    vessel_before = opt_result.get_vessel_name()
    opt_result.click_vessel_dropdown()
    vessel_after = opt_result.get_vessel_name()

    # ----- Departure date -----
    date_before = opt_result.get_departure_date()
    opt_result.click_departure_date_dropdown()
    date_after = opt_result.get_departure_date()

    # Validate values actually changed
    assert service_before != service_after, "Service should change after dropdown click"
    assert vessel_before != vessel_after, "Vessel should change after dropdown click"
    assert date_before != date_after, "Departure date should change after dropdown click"


# Test: Port View table loads and column headers exist
def test_port_view(browser_page, base_url, login):
    opt_result = Optimization_Result_Page(browser_page, base_url)

    # Open Optimization Result page
    opt_result.open_opt_result()

    # Switch to Port View tab
    opt_result.open_port_view_page()

    # Wait until Port View table is visible
    expect(opt_result.port_view_table).to_be_visible(timeout=20000)

    # Validate table column names
    assert opt_result.port_column.inner_text() == "Port"
    assert opt_result.type_column.inner_text() == "Type"
    assert opt_result.gap_before_column.inner_text() == "Gap: Before"
    assert opt_result.gap_after_column.inner_text() == "Gap: After"
    assert opt_result.reason_column.inner_text() == "Reason"


# Test: Total Cost KPI (skipped for now)
@pytest.mark.skip(reason="Not implemented yet")
def test_total_cost(browser_page, base_url, login):
    opt_result = Optimization_Result_Page(browser_page, base_url)
    opt_result.open_opt_result()

    # Capture KPI before action
    total_before = opt_result.get_kpi_value("Total Cost")

    # TODO: perform action that should change KPI

    total_after = opt_result.get_kpi_value("Total Cost")

    # Validate KPI changed
    assert total_before != total_after


# Test: Download CSV and validate file + content
def test_download_csv(browser_page, base_url, login):
    opt_result = Optimization_Result_Page(browser_page, base_url)
    opt_result.open_opt_result()

    # Trigger CSV download
    file_path = opt_result.download_csv()

    # Ensure file exists on disk
    assert file_path.exists(), f"CSV not found: {file_path}"

    # Read CSV and make sure it has data
    with open(file_path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    assert len(rows) > 0, "CSV file is empty"

    # Attach CSV to Allure report (for GitHub Actions too)
    with open(file_path, "rb") as f:
        allure.attach(
            f.read(),
            name=file_path.name,
            attachment_type=allure.attachment_type.CSV
        )
