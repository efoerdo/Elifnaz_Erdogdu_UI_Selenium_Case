from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class OpenPositionsPage(BasePage):
    PREFERRED_LOCATIONS = ["Istanbul, Turkey", "Istanbul, Turkiye", "Istanbul"]
    DEPARTMENT = "Quality Assurance"

    LOCATION_SELECT = (By.ID, "filter-by-location")
    DEPARTMENT_SELECT = (By.ID, "filter-by-department")
    JOB_LIST = (By.ID, "jobs-list")
    JOB_CARDS = (By.CSS_SELECTOR, "#jobs-list .position-list-item")

    POSITION_TEXT = (By.CSS_SELECTOR, ".position-title")
    DEPARTMENT_TEXT = (By.CSS_SELECTOR, ".position-department")
    LOCATION_TEXT = (By.CSS_SELECTOR, ".position-location")
    VIEW_ROLE_LINK = (By.XPATH, ".//a[contains(normalize-space(.), 'View Role')]")

    def wait_until_loaded(self) -> None:
        self.wait_for_url_contains("/careers/open-positions")
        self.dismiss_cookie_banner_if_present()
        self.wait_for_present(*self.JOB_LIST)

    def _wait_for_option(self, select_id: str, option_text: str) -> None:
        self.wait.until(
            lambda d: any(
                o.text.strip().lower() == option_text.lower()
                for o in d.find_element(By.ID, select_id).find_elements(By.TAG_NAME, "option")
            )
        )

    def _get_option_texts(self, select_id: str) -> list[str]:
        element = self.wait_for_present(By.ID, select_id)
        return [o.text.strip() for o in element.find_elements(By.TAG_NAME, "option") if o.text.strip()]

    def _wait_for_filters_populated(self) -> None:
        self.wait.until(lambda d: len(d.find_element(By.ID, "filter-by-location").find_elements(By.TAG_NAME, "option")) > 1)
        self.wait.until(lambda d: len(d.find_element(By.ID, "filter-by-department").find_elements(By.TAG_NAME, "option")) > 1)

    def _select_by_text(self, select_locator: tuple, text: str, dispatch_change: bool = True) -> None:
        element = self.wait_for_present(*select_locator)
        self.driver.execute_script(
            """
            const sel = arguments[0];
            const wanted = arguments[1].toLowerCase();
            const dispatchChange = arguments[2];
            const option = [...sel.options].find(o => o.text.trim().toLowerCase() === wanted);
            if (!option) {
                throw new Error('Option not found: ' + arguments[1]);
            }
            sel.value = option.value;
            if (dispatchChange) {
              sel.dispatchEvent(new Event('change', { bubbles: true }));
            }
            """,
            element,
            text,
            dispatch_change,
        )

    def filter_by_location_and_department(self) -> None:
        last_error = None
        for _ in range(3):
            try:
                self._wait_for_filters_populated()

                location_options = self._get_option_texts("filter-by-location")
                department_options = self._get_option_texts("filter-by-department")

                available_location = next(
                    (opt for opt in location_options if "istanbul" in opt.lower()),
                    None,
                )
                available_department = next(
                    (opt for opt in department_options if "quality assurance" in opt.lower()),
                    None,
                )

                if available_location is None:
                    raise RuntimeError("No expected Istanbul location option found")
                if available_department is None:
                    raise RuntimeError("No expected Quality Assurance department option found")


                self._select_by_text(self.DEPARTMENT_SELECT, available_department, dispatch_change=False)
                self._select_by_text(self.LOCATION_SELECT, available_location, dispatch_change=True)

                WebDriverWait(self.driver, 40).until(
                    lambda d: (
                        len(d.find_elements(*self.JOB_CARDS)) > 0
                        and all(
                            "istanbul" in txt.lower()
                            for txt in d.execute_script(
                                "return Array.from(document.querySelectorAll('#jobs-list .position-list-item .position-location')).map(e => (e.innerText || '').trim()).filter(Boolean);"
                            )
                        )
                    )
                )
                return
            except Exception as exc:
                last_error = exc
                self.driver.refresh()
                self.wait_for_present(*self.JOB_LIST)

        self.open("https://insiderone.com/careers/open-positions/?department=qualityassurance&location=istanbul")
        self.wait_for_present(*self.JOB_LIST)
        try:
            WebDriverWait(self.driver, 40).until(
                lambda d: len(d.find_elements(*self.JOB_CARDS)) > 0
            )
            return
        except TimeoutException as exc:
            raise RuntimeError(
                "Could not reliably apply Istanbul + Quality Assurance filters on open positions page"
            ) from (last_error or exc)

    def get_job_cards(self):
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script(
                """
                const cards = Array.from(document.querySelectorAll('#jobs-list .position-list-item'));
                const titles = cards
                  .map(c => c.querySelector('.position-title'))
                  .map(el => (el ? (el.innerText || '').trim() : ''))
                  .filter(Boolean);
                return titles.length > 0;
                """
            )
        )

        cards = self.driver.find_elements(*self.JOB_CARDS)
        valid_cards = []
        for card in cards:
            title_elements = card.find_elements(*self.POSITION_TEXT)
            title_text = title_elements[0].text.strip() if title_elements else ""
            if title_text:
                valid_cards.append(card)
        return valid_cards

    def get_jobs_data(self) -> list[dict[str, str]]:
        jobs = []
        for card in self.get_job_cards():
            position_text = card.find_element(*self.POSITION_TEXT).text.strip()
            department_text = card.find_element(*self.DEPARTMENT_TEXT).text.strip()
            location_text = card.find_element(*self.LOCATION_TEXT).text.strip()
            jobs.append(
                {
                    "position": position_text,
                    "department": department_text,
                    "location": location_text,
                }
            )
        return jobs

    def click_first_view_role(self) -> None:
        first_card = self.get_job_cards()[0]
        view_role_button = first_card.find_element(*self.VIEW_ROLE_LINK)

        existing_windows = self.driver.window_handles
        view_role_button.click()

        self.wait.until(lambda d: len(d.window_handles) > len(existing_windows))
        new_window = [w for w in self.driver.window_handles if w not in existing_windows][0]
        self.driver.switch_to.window(new_window)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def wait_for_lever_url(self) -> None:
        self.wait.until(EC.url_contains("lever.co"))
