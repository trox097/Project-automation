from automation.pages.home_page import HomePage
from automation.pages.modals import LoginModal


def test_successful_login(driver, base_url, valid_user):
    home_page = HomePage(driver)
    home_page.open_home(base_url)

    login_modal = home_page.open_login_modal()
    assert isinstance(login_modal, LoginModal)

    login_modal.submit_credentials(valid_user["username"], valid_user["password"])

    home_page.wait_for_authenticated_state(valid_user["username"])

    assert home_page.is_on_home_page(base_url), "User was not redirected to the home page after login."
    assert home_page.is_logout_visible(), "Logout option is not visible after login."
