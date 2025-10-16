from __future__ import annotations

from typing import List, Dict

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class CartPage(BasePage):
    """Shopping cart page interactions and assertions."""

    CART_TABLE = (By.ID, "tbodyid")
    CART_ROWS = (By.CSS_SELECTOR, "#tbodyid > tr")
    TOTAL_PRICE = (By.ID, "totalp")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[@class='btn btn-success' and normalize-space()='Place Order']")
    DELETE_LINK = (By.LINK_TEXT, "Delete")
    HOME_NAV = (By.ID, "nava")

    def wait_until_loaded(self) -> None:
        self.wait_for_visible(self.CART_TABLE)

    def get_items(self) -> List[Dict[str, str]]:
        self.wait_until_loaded()
        rows = self.driver.find_elements(*self.CART_ROWS)
        items: List[Dict[str, str]] = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 3:
                continue
            items.append(
                {
                    "title": cells[1].text.strip(),
                    "price": cells[2].text.strip(),
                }
            )
        return items

    def get_total_price(self) -> float:
        total_text = self.get_text(self.TOTAL_PRICE)
        return float(total_text) if total_text else 0.0

    def open_place_order_modal(self):
        self.click(self.PLACE_ORDER_BUTTON)
        from .modals import PlaceOrderModal

        return PlaceOrderModal(self.driver)

    def clear_cart(self) -> None:
        wait = WebDriverWait(self.driver, 10)
        attempts = 0

        while True:
            rows = self.driver.find_elements(*self.CART_ROWS)
            if not rows:
                return

            initial_count = len(rows)
            delete_link = rows[0].find_element(*self.DELETE_LINK)
            delete_link.click()
            try:
                wait.until(lambda _: len(self.driver.find_elements(*self.CART_ROWS)) < initial_count)
            except TimeoutException:
                attempts += 1
                if attempts >= 3:
                    raise AssertionError("Unable to clear cart after multiple attempts.")
                self.driver.refresh()
                self.wait_until_loaded()

    def wait_for_empty(self, timeout: int = 10) -> None:
        wait = WebDriverWait(self.driver, timeout)

        def _is_empty(_):
            return not self.driver.find_elements(*self.CART_ROWS)

        wait.until(_is_empty, "Cart did not empty after waiting.")

    def wait_for_item_count(self, expected_count: int, timeout: int = 10) -> None:
        wait = WebDriverWait(self.driver, timeout)

        def _count_matches(_):
            return len(self.driver.find_elements(*self.CART_ROWS)) >= expected_count

        wait.until(_count_matches, f"Cart did not reach {expected_count} items.")

    def return_to_home(self):
        element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.HOME_NAV))
        self.driver.execute_script("arguments[0].click();", element)
        from .home_page import HomePage

        home_page = HomePage(self.driver)
        home_page.wait_for_visible(home_page.PRODUCTS_CONTAINER)
        return home_page
