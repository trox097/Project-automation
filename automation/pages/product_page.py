from __future__ import annotations

import re

from selenium.webdriver.common.by import By

from .base_page import BasePage


class ProductPage(BasePage):
    """Product detail page supporting add to cart operations."""

    TITLE = (By.CLASS_NAME, "name")
    PRICE = (By.CLASS_NAME, "price-container")
    ADD_TO_CART = (By.XPATH, "//a[@class='btn btn-success btn-lg' and normalize-space()='Add to cart']")
    HOME_NAV = (By.XPATH, "//a[@class='nav-link' and normalize-space()='Home']")

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
        return self.wait_for_alert_and_accept()

    def return_to_home(self) -> None:
        self.click(self.HOME_NAV)
