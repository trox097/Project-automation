from __future__ import annotations

from typing import List, Dict

from selenium.webdriver.common.by import By

from .base_page import BasePage


class CartPage(BasePage):
    """Shopping cart page interactions and assertions."""

    CART_TABLE = (By.ID, "tbodyid")
    CART_ROWS = (By.CSS_SELECTOR, "#tbodyid > tr")
    TOTAL_PRICE = (By.ID, "totalp")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[@class='btn btn-success' and normalize-space()='Place Order']")

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
