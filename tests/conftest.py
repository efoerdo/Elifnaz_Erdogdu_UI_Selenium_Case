from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Browser to run tests with: chrome or firefox",
    )


@pytest.fixture
def browser_name(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--browser")


@pytest.fixture
def driver(browser_name: str):
    if browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("-width=1920")
        options.add_argument("-height=1080")
        firefox_binary = os.getenv("FIREFOX_BINARY")
        if firefox_binary:
            options.binary_location = firefox_binary

        geckodriver_path = os.getenv("GECKODRIVER_PATH")
        try:
            if geckodriver_path:
                service = FirefoxService(executable_path=geckodriver_path)
                driver_instance = webdriver.Firefox(service=service, options=options)
            else:
                driver_instance = webdriver.Firefox(options=options)
        except Exception as exc:
            raise RuntimeError(
                "Firefox setup failed. If Selenium Manager cannot download geckodriver, "
                "set GECKODRIVER_PATH and optionally FIREFOX_BINARY environment variables. "
                f"Original error: {exc}"
            )
    else:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver_instance = webdriver.Chrome(options=options)

    driver_instance.set_page_load_timeout(60)
    driver_instance.implicitly_wait(0)

    yield driver_instance

    driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call):
    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)

    if report.when in ("setup", "call") and report.failed:
        driver_instance = item.funcargs.get("driver")
        browser = item.funcargs.get("browser_name", "unknown")

        if driver_instance:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshots_dir = Path("screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            screenshot_file = screenshots_dir / f"{item.name}_{browser}_{timestamp}.png"
            driver_instance.save_screenshot(str(screenshot_file))
