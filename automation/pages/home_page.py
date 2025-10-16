from __future__ import annotations

from selenium.webdriver.common.by import By

from .base_page import BasePage


class HomePage(BasePage):
    """Landing page for catalogue exploration and authentication entry points."""

    LOGIN_BUTTON = (By.ID, "login2")
    LOGOUT_BUTTON = (By.ID, "logout2")
    USER_GREETING = (By.ID, "nameofuser")
    CART_LINK = (By.ID, "cartur")
    PRODUCTS_CONTAINER = (By.ID, "tbodyid")

    def open_home(self, base_url: str) -> None:
        self.open(base_url)
        self.wait_for_visible(self.PRODUCTS_CONTAINER)

    def open_login_modal(self):
        self.click(self.LOGIN_BUTTON)
        from .modals import LoginModal  # Local import to avoid circular dependency.

        return LoginModal(self.driver)

    def is_user_logged_in(self) -> bool:
        return self.is_visible(self.USER_GREETING)

    def get_logged_in_username(self) -> str:
        return self.get_text(self.USER_GREETING)

    def open_product_details(self, product_name: str) -> None:
        product_locator = (By.XPATH, f"//a[@class='hrefch' and normalize-space()='{product_name}']")
        self.click(product_locator)

    def navigate_to_cart(self) -> None:
        self.click(self.CART_LINK)
