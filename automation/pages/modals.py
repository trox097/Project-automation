from __future__ import annotations

from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginModal(BasePage):
    """Encapsulates interactions with the Demoblaze login modal dialog."""

    MODAL = (By.ID, "logInModal")
    USERNAME = (By.ID, "loginusername")
    PASSWORD = (By.ID, "loginpassword")
    SUBMIT = (By.XPATH, "//button[@class='btn btn-primary' and normalize-space()='Log in']")

    def wait_until_visible(self) -> None:
        self.wait_for_visible(self.MODAL)

    def submit_credentials(self, username: str, password: str) -> None:
        self.wait_until_visible()
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)
        self.wait_for_invisibility(self.MODAL)


class PlaceOrderModal(BasePage):
    """Handles the place order modal that completes the checkout flow."""

    MODAL = (By.ID, "orderModal")
    NAME = (By.ID, "name")
    COUNTRY = (By.ID, "country")
    CITY = (By.ID, "city")
    CARD = (By.ID, "card")
    MONTH = (By.ID, "month")
    YEAR = (By.ID, "year")
    PURCHASE_BUTTON = (By.XPATH, "//button[@class='btn btn-primary' and normalize-space()='Purchase']")
    CONFIRMATION_MODAL = (By.CLASS_NAME, "sweet-alert")
    CONFIRMATION_TEXT = (By.CSS_SELECTOR, ".sweet-alert p")
    CONFIRMATION_OK = (By.XPATH, "//button[@class='confirm btn btn-lg btn-primary' and normalize-space()='OK']")

    def wait_until_visible(self) -> None:
        self.wait_for_visible(self.MODAL)

    def fill_order_form(self, order_data: dict) -> None:
        self.wait_until_visible()
        self.type(self.NAME, order_data["name"])
        self.type(self.COUNTRY, order_data["country"])
        self.type(self.CITY, order_data["city"])
        self.type(self.CARD, order_data["card"])
        self.type(self.MONTH, order_data["month"])
        self.type(self.YEAR, order_data["year"])

    def submit_order(self) -> None:
        self.click(self.PURCHASE_BUTTON)
        self.wait_for_visible(self.CONFIRMATION_MODAL)

    def capture_confirmation(self) -> str:
        return self.get_text(self.CONFIRMATION_TEXT)

    def acknowledge_confirmation(self) -> None:
        self.click(self.CONFIRMATION_OK)
