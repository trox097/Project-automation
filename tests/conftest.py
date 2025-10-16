from __future__ import annotations

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Browser to run tests against.",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.demoblaze.com",
        help="Target application base URL.",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browsers in headless mode.",
    )


@pytest.fixture
def base_url(pytestconfig: pytest.Config) -> str:
    return pytestconfig.getoption("--base-url")


@pytest.fixture
def driver(pytestconfig: pytest.Config):
    browser = pytestconfig.getoption("--browser")
    headless = pytestconfig.getoption("--headless")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=options)
    else:
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        driver_instance = webdriver.Firefox(service=service, options=options)
        driver_instance.maximize_window()

    driver_instance.implicitly_wait(5)
    yield driver_instance
    driver_instance.quit()
