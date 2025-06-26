from playwright.sync_api import expect
from variables import last_name, first_name, item


class CartCreation:

    def __init__(self, page, iframe):
        self.page = page
        self.iframe = iframe


    def add_to_cart(self):
        self.iframe.locator('#category-9').click()
        filters = self.iframe.locator('#search_filters')
        filters.wait_for()
        filters.locator('a', has_text='80x120cm').click()
        self.page.wait_for_timeout(2000)
        products = self.iframe.locator('#products div.js-product')
        print(products.count())
        expect(products).to_have_count(3, timeout=2000)
        self.iframe.locator('div.js-product', has_text=item).click()
        self.iframe.get_by_role(role='button', name='Add to cart').click()
        cart_frame = self.iframe.locator('div.modal-content')
        cart_frame.get_by_role(role='link', name='Proceed to checkout').click()
        self.page.wait_for_timeout(2000)
        self.iframe.get_by_text('Proceed to checkout').click()
        expect(self.iframe.get_by_role(role='textbox', name='First Name')).to_have_value(first_name)
        expect(self.iframe.get_by_role(role='textbox', name='Last Name')).to_have_value(last_name)
        self.iframe.locator('a.js-show-details').click()
        expect(self.iframe.locator('#cart-summary-product-list')).to_contain_text(item[:19])