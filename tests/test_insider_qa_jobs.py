from pages.home_page import HomePage
from pages.open_positions_page import OpenPositionsPage
from pages.qa_careers_page import QACareersPage


def test_insider_qa_jobs_flow(driver):
    home_page = HomePage(driver)
    qa_careers_page = QACareersPage(driver)
    open_positions_page = OpenPositionsPage(driver)

    # 1) Home page should open and main blocks should be loaded
    home_page.open_and_validate()
    assert "Insider" in home_page.get_title(), "Insider home page title is not loaded"
    assert home_page.are_main_blocks_visible(), "One or more home page main blocks are not visible"

    # 2) Navigate to QA careers, click "See all QA jobs", and filter jobs
    qa_careers_page.open_and_go_to_qa_jobs()
    open_positions_page.wait_until_loaded()
    assert "/careers/open-positions" in driver.current_url, "Open positions page is not loaded"

    open_positions_page.filter_by_location_and_department()

    # 3) Validate all listed jobs
    jobs = open_positions_page.get_jobs_data()
    assert jobs, "No jobs found for selected filters"

    for job in jobs:
        position_text = job["position"]
        department_text = job["department"]
        location_text = job["location"]

        assert (
            "quality assurance" in position_text.lower()
            or "quality" in position_text.lower()
            or " qa " in f" {position_text.lower()} "
        ), f"Position does not contain expected QA wording: {position_text}"
        assert "quality assurance" in department_text.lower(), (
            f"Department does not contain 'Quality Assurance': {department_text}"
        )
        assert "istanbul" in location_text.lower(), (
            f"Location does not contain expected Istanbul wording: {location_text}"
        )

    # 4) Click "View Role" and verify redirect to Lever
    open_positions_page.click_first_view_role()
    open_positions_page.wait_for_lever_url()
    assert "lever.co" in open_positions_page.get_current_url().lower(), (
        f"Expected redirect to Lever page, but got: {open_positions_page.get_current_url()}"
    )
