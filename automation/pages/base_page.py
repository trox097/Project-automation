from __future__ import annotations

from typing import Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Common web driver helpers shared across all page objects."""

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self._wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def wait_for_visible(self, locator: Tuple[str, str]):
        return self._wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: Tuple[str, str]):
        return self._wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Tuple[str, str]) -> None:
        element = self.wait_for_clickable(locator)
        element.click()

    def type(self, locator: Tuple[str, str], value: str, clear: bool = True) -> None:
        element = self.wait_for_visible(locator)
        if clear:
            element.clear()
        element.send_keys(value)

    def get_text(self, locator: Tuple[str, str]) -> str:
        element = self.wait_for_visible(locator)
        return element.text

    def wait_for_invisibility(self, locator: Tuple[str, str]) -> None:
        self._wait.until(EC.invisibility_of_element_located(locator))

    def is_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_alert_and_accept(self) -> str:
        alert = self._wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text
