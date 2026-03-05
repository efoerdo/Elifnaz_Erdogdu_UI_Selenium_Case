from __future__ import annotations

from pathlib import Path

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 20) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def wait_for_url_contains(self, value: str) -> None:
        self.wait.until(EC.url_contains(value))

    def wait_for_visible(self, by: By, locator: str):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def wait_for_present(self, by: By, locator: str):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click(self, by: By, locator: str) -> None:
        self.wait.until(EC.element_to_be_clickable((by, locator))).click()

    def dismiss_cookie_banner_if_present(self) -> None:
        candidates = [
            (By.XPATH, "//button[contains(., 'Accept All') or contains(., 'Accept all') or contains(., 'I Agree') or contains(., 'Allow all') ]"),
            (By.CSS_SELECTOR, "#cookie_action_close_header"),
            (By.CSS_SELECTOR, "a.cky-btn-accept"),
            (By.CSS_SELECTOR, "button.cky-btn-accept"),
        ]

        for by, locator in candidates:
            try:
                elements = self.driver.find_elements(by, locator)
                if elements:
                    elements[0].click()
                    return
            except (NoSuchElementException, TimeoutException):
                continue

    @staticmethod
    def ensure_dir(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
