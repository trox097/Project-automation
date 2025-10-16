from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

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


@pytest.fixture(scope="session")
def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


@pytest.fixture(scope="session")
def _load_json_data(data_dir: Path):
    def loader(file_name: str) -> Dict:
        with data_dir.joinpath(file_name).open(encoding="utf-8") as handle:
            return json.load(handle)

    return loader


@pytest.fixture(scope="session")
def users_data(_load_json_data) -> Dict[str, Dict[str, str]]:
    return _load_json_data("users.json")


@pytest.fixture(scope="session")
def orders_data(_load_json_data) -> Dict[str, Dict[str, str]]:
    return _load_json_data("orders.json")


@pytest.fixture
def valid_user(users_data: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    return users_data["valid_user"]


@pytest.fixture
def default_order(orders_data: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    return orders_data["default_order"]


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
