from automation.pages.home_page import HomePage
from automation.pages.modals import LoginModal
from tests.data.users import TEST_USER


def test_successful_login(driver, base_url):
    home_page = HomePage(driver)
    home_page.open_home(base_url)

    login_modal = home_page.open_login_modal()
    assert isinstance(login_modal, LoginModal)

    login_modal.submit_credentials(TEST_USER["username"], TEST_USER["password"])

    assert home_page.is_user_logged_in(), "User greeting not visible after login."
    greeting = home_page.get_logged_in_username()
    assert TEST_USER["username"] in greeting, f"Expected username in greeting, got {greeting!r}"
