from __future__ import annotations

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class HomePage(BasePage):
    """Landing page for catalogue exploration and authentication entry points."""

    LOGIN_BUTTON = (By.ID, "login2")
    LOGOUT_BUTTON = (By.ID, "logout2")
    USER_GREETING = (By.ID, "nameofuser")
    CART_LINK = (By.ID, "cartur")
    PRODUCTS_CONTAINER = (By.ID, "tbodyid")
    CATEGORY_LINK_TEMPLATE = "//a[contains(@class,'list-group-item') and normalize-space()='{category}']"

    def open_home(self, base_url: str) -> None:
        self.open(base_url)
        self.wait_for_visible(self.PRODUCTS_CONTAINER)

    def is_on_home_page(self, base_url: str) -> bool:
        return self.driver.current_url.rstrip("/") in (base_url.rstrip("/"), f"{base_url.rstrip('/')}/index.html")

    def open_login_modal(self):
        self.click(self.LOGIN_BUTTON)
        from .modals import LoginModal  # Local import to avoid circular dependency.

        return LoginModal(self.driver)

    def is_user_logged_in(self) -> bool:
        return self.is_visible(self.USER_GREETING)

    def is_logout_visible(self) -> bool:
        return self.is_visible(self.LOGOUT_BUTTON)

    def wait_for_authenticated_state(self, username: str | None = None) -> None:
        self.wait_for_visible(self.USER_GREETING)
        self.wait_for_visible(self.LOGOUT_BUTTON)
        if username:
            actual_username = self.get_logged_in_username()
            if username not in actual_username:
                raise AssertionError(f"Expected username '{username}' in greeting, got '{actual_username}'")

    def get_logged_in_username(self) -> str:
        return self.get_text(self.USER_GREETING)

    def select_category(self, category_name: str) -> None:
        category_locator = (By.XPATH, self.CATEGORY_LINK_TEMPLATE.format(category=category_name))
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(category_locator))
        element.click()
        self.wait_for_visible(self.PRODUCTS_CONTAINER)
        wait.until(lambda _: self.driver.find_elements(By.CSS_SELECTOR, "#tbodyid .hrefch"))

    def open_product_details(self, product_name: str) -> None:
        self.wait_for_visible(self.PRODUCTS_CONTAINER)
        product_locator = (By.XPATH, f"//a[@class='hrefch' and normalize-space()='{product_name}']")
        wait = WebDriverWait(self.driver, 15, ignored_exceptions=(StaleElementReferenceException,))
        wait.until(EC.presence_of_element_located(product_locator))

        for attempt in range(3):
            try:
                element = wait.until(EC.element_to_be_clickable(product_locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element.click()
                break
            except StaleElementReferenceException:
                if attempt == 2:
                    raise
                wait.until(EC.presence_of_element_located(product_locator))

    def navigate_to_cart(self) -> None:
        self.click(self.CART_LINK)
