from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class QACareersPage(BasePage):
    URL = "https://insiderone.com/careers/quality-assurance/"

    PAGE_TITLE = (By.XPATH, "//h1[contains(., 'Quality Assurance')]")
    SEE_ALL_QA_JOBS_BUTTON = (By.XPATH, "//a[contains(normalize-space(.), 'See all QA jobs')]")

    def open_and_go_to_qa_jobs(self) -> None:
        self.open(self.URL)
        self.wait_for_url_contains("/careers/quality-assurance")
        self.dismiss_cookie_banner_if_present()
        self.wait_for_present(*self.PAGE_TITLE)
        self.click(*self.SEE_ALL_QA_JOBS_BUTTON)
