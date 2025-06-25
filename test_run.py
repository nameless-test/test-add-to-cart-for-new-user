from registration_page import LoginPage
from add_item_to_cart import CartCreation
from variables import registration_data


def test_run(browser_launch):
    page = browser_launch
    login = LoginPage(page)
    login.go_to_registration_page()
    login.fill_registration_form()
    print (registration_data)
    cart = CartCreation(page, login.iframe)
    cart.add_to_cart()