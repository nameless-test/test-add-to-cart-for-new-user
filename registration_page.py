from playwright.sync_api import expect
from variables import first_name, last_name, e_mail, password, birthdate

fields = {'First Name': first_name,
          'Last Name': last_name,
          'Email': e_mail,
          'Password': password,
          'Birthdate': birthdate}

class LoginPage:

    def __init__(self, page):
        self.page = page
        self.iframe = None


    def go_to_registration_page(self):
        self.page.goto('https://demo.prestashop.com/#/en/front')
        self.iframe = self.page.frame_locator("iframe").first
        self.iframe.locator('div.user-info a').click()
        self.iframe.locator('div.no-account a').click()


    def fill_registration_form(self):
        expect(self.iframe.locator('#field-id_gender-1')).not_to_be_checked()
        expect(self.iframe.locator('#field-id_gender-2')).not_to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Receive offers from our partners')).not_to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='I agree to the terms and conditions and the privacy policy')).not_to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Sign up for our newsletter')).not_to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Customer data privacy')).not_to_be_checked()
        for name, value in fields.items():
            self.iframe.get_by_role(role='textbox', name=name).fill(value)
        self.iframe.locator('#field-id_gender-1').check()
        self.iframe.get_by_role(role='checkbox', name='Receive offers from our partners').check()
        self.iframe.get_by_role(role='checkbox', name='I agree to the terms and conditions and the privacy policy').check()
        self.iframe.get_by_role(role='checkbox', name='Sign up for our newsletter').check()
        self.iframe.get_by_role(role='checkbox', name='Customer data privacy').check()
        expect(self.iframe.locator('#field-id_gender-1')).to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Receive offers from our partners')).to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='I agree to the terms and conditions and the privacy policy')).to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Sign up for our newsletter')).to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Customer data privacy')).to_be_checked()
        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.page.wait_for_timeout(3000)
        expect(self.iframe.locator('div.user-info a.account')).to_contain_text(f'{first_name} {last_name}')