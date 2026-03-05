from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://insiderone.com/"

    MAIN_BLOCKS = [
        "h1",
        "a[href*='/customer-data-management/']",
        "a[href*='/ai-overview/']",
        "a[href*='/channels/sms/']",
        "a[href*='/case-studies']",
        "a[href*='/integrations/']",
    ]

    def open_and_validate(self) -> None:
        self.open(self.URL)
        self.wait_for_url_contains("insiderone.com")
        self.dismiss_cookie_banner_if_present()

        for block_css in self.MAIN_BLOCKS:
            self.wait_for_present(By.CSS_SELECTOR, block_css)

    def get_title(self) -> str:
        return self.driver.title

    def are_main_blocks_visible(self) -> bool:
        for block_css in self.MAIN_BLOCKS:
            if not self.driver.find_elements(By.CSS_SELECTOR, block_css):
                return False
        return True
