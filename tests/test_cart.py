import pytest

from automation.pages.cart_page import CartPage
from automation.pages.home_page import HomePage
from automation.pages.modals import LoginModal
from automation.pages.product_page import ProductPage


@pytest.mark.smoke
def test_add_products_updates_cart(driver, base_url, valid_user):
    products_to_add = ["Samsung galaxy s6", "Nokia lumia 1520"]

    home_page = HomePage(driver)
    home_page.open_home(base_url)
    home_page.select_category("Phones")

    login_modal = home_page.open_login_modal()
    login_modal.submit_credentials(valid_user["username"], valid_user["password"])
    assert home_page.is_user_logged_in()

    home_page.navigate_to_cart()
    cart_page = CartPage(driver)
    cart_page.clear_cart()
    home_page = cart_page.return_to_home()
    home_page.select_category("Phones")

    product_page = ProductPage(driver)
    for product in products_to_add:
        home_page.open_product_details(product)
        assert product_page.get_product_name() == product
        alert_text = product_page.add_product_to_cart()
        assert "Product added" in alert_text
        home_page = product_page.return_to_home()
        home_page.select_category("Phones")

    home_page.navigate_to_cart()
    cart_page = CartPage(driver)
    cart_page.wait_for_item_count(len(products_to_add))
    items = cart_page.get_items()

    cart_titles = [item["title"] for item in items]
    assert sorted(cart_titles) == sorted(products_to_add), (
        f"Cart contents mismatch. Expected {products_to_add}, got {cart_titles}"
    )


@pytest.mark.regression
def test_cart_displays_correct_details(driver, base_url, valid_user):
    products_to_add = ["Samsung galaxy s6", "Nokia lumia 1520"]

    home_page = HomePage(driver)
    home_page.open_home(base_url)
    home_page.select_category("Phones")

    login_modal = home_page.open_login_modal()
    login_modal.submit_credentials(valid_user["username"], valid_user["password"])
    assert home_page.is_user_logged_in()

    home_page.navigate_to_cart()
    cart_page = CartPage(driver)
    cart_page.clear_cart()
    home_page = cart_page.return_to_home()
    home_page.select_category("Phones")

    product_page = ProductPage(driver)
    expected_prices = {}
    for product in products_to_add:
        home_page.open_product_details(product)
        product_name = product_page.get_product_name()
        assert product_name == product
        expected_prices[product_name] = product_page.get_product_price()
        product_page.add_product_to_cart()
        home_page = product_page.return_to_home()
        home_page.select_category("Phones")

    home_page.navigate_to_cart()
    cart_page = CartPage(driver)
    cart_page.wait_for_item_count(len(products_to_add))
    cart_items = cart_page.get_items()

    assert len(cart_items) == len(products_to_add), (
        f"Expected {len(products_to_add)} items in cart, found {len(cart_items)}"
    )

    calculated_total = 0
    for item in cart_items:
        title = item["title"]
        price = float(item["price"])
        calculated_total += price
        expected_price = expected_prices.get(title)
        assert expected_price is not None, f"Unexpected product {title} present in cart"
        assert price == expected_price, f"Price mismatch for {title}: {price} vs {expected_price}"

    total_in_cart = cart_page.get_total_price()
    assert total_in_cart == calculated_total, (
        f"Displayed total {total_in_cart} does not match calculated {calculated_total}"
    )
