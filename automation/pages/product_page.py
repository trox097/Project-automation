from __future__ import annotations

import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class ProductPage(BasePage):
    """Product detail page supporting add to cart operations."""

    TITLE = (By.CLASS_NAME, "name")
    PRICE = (By.CLASS_NAME, "price-container")
    ADD_TO_CART = (By.XPATH, "//a[@class='btn btn-success btn-lg' and normalize-space()='Add to cart']")
    HOME_NAV = (By.ID, "nava")

    def get_product_name(self) -> str:
        return self.get_text(self.TITLE)

    def get_product_price(self) -> float:
        raw_price = self.get_text(self.PRICE)
        match = re.search(r"(\d+)", raw_price)
        if not match:
            raise AssertionError(f"Unable to parse price from: {raw_price}")
        return float(match.group(1))

    def add_product_to_cart(self) -> str:
        self.click(self.ADD_TO_CART)
        alert_text = self.wait_for_alert_and_accept()
        time.sleep(2)
        return alert_text

    def return_to_home(self):
        element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.HOME_NAV))
        self.driver.execute_script("arguments[0].click();", element)
        from .home_page import HomePage

        home_page = HomePage(self.driver)
        home_page.wait_for_visible(home_page.PRODUCTS_CONTAINER)
        return home_page
