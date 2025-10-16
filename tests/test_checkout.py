import re

from automation.pages.cart_page import CartPage
from automation.pages.home_page import HomePage
from automation.pages.modals import LoginModal
from automation.pages.product_page import ProductPage
from tests.data.orders import DEFAULT_ORDER
from tests.data.users import TEST_USER


def _extract_order_id(confirmation_text: str) -> str:
    match = re.search(r"Id:\s*(\d+)", confirmation_text)
    if not match:
        raise AssertionError(f"Order confirmation did not include an Id. Raw text:\n{confirmation_text}")
    return match.group(1)


def test_checkout_happy_path(driver, base_url):
    home_page = HomePage(driver)
    home_page.open_home(base_url)

    login_modal = home_page.open_login_modal()
    login_modal.submit_credentials(TEST_USER["username"], TEST_USER["password"])
    assert home_page.is_user_logged_in()

    product_page = ProductPage(driver)
    home_page.open_product_details("Samsung galaxy s6")
    product_page.add_product_to_cart()
    product_page.return_to_home()

    home_page.navigate_to_cart()
    cart_page = CartPage(driver)
    cart_items = cart_page.get_items()
    assert cart_items, "Cart is empty before checkout."
    expected_total = cart_page.get_total_price()

    place_order_modal = cart_page.open_place_order_modal()
    place_order_modal.fill_order_form(DEFAULT_ORDER)
    place_order_modal.submit_order()

    confirmation_text = place_order_modal.capture_confirmation()
    order_id = _extract_order_id(confirmation_text)
    assert order_id.isdigit(), "Order Id is not numeric."
    assert str(int(expected_total)) in confirmation_text, "Order amount not present in confirmation."

    place_order_modal.acknowledge_confirmation()

    cart_page.wait_until_loaded()
    assert not cart_page.get_items(), "Cart still contains items after completing order."
