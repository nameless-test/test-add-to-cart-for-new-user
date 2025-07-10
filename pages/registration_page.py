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

    # перехід на сторінку реєстрації
    def go_to_registration_page(self):
        self.page.goto('https://demo.prestashop.com/#/en/front')
        self.iframe = self.page.frame_locator("iframe").first
        self.iframe.locator('div.user-info a').click()
        self.iframe.locator('div.no-account a').click()

    def get_validation_message(self, field):
        field.evaluate("el => el.reportValidity()")
        return field.evaluate("el => el.validationMessage")

    # перевірка повідомлень-помилок від браузера
    def check_required_fields_validation(self, message='Жодне поле не показало повідомлення валідації'):
        required_fields = self.iframe.locator('input[required]')
        count = required_fields.count()
        found_error = False

        for i in range(count):
            field = required_fields.nth(i)
            msg = self.get_validation_message(field)
            print(f"Поле {i}: {msg}")
            if msg.strip():
                found_error = True
                break
        assert found_error, message

    def negative_checks(self):
        # Незаповнена форма
        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.check_required_fields_validation('Валідація не спрацювала при порожній формі')

        # Незаповнені чекбокси
        for name, value in fields.items():
            self.iframe.get_by_role(role='textbox', name=name).fill(value)

        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.check_required_fields_validation('Валідація не спрацювала при незаповнених чекбоксах')

        # Заповнено лише чекбокс про умови користування
        self.iframe.get_by_role(role='checkbox', name='I agree to the terms and conditions and the privacy policy').check()
        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.check_required_fields_validation('Не виявлено помилку при незаповненому полі Customer data privacy')

        # Заповнено чекбокс про особисті дані
        self.iframe.get_by_role(role='checkbox', name='I agree to the terms and conditions and the privacy policy').uncheck()
        self.iframe.get_by_role(role='checkbox', name='Customer data privacy').check()
        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.check_required_fields_validation('Не виявлено помилку при незаповненому полі I agree to the terms and conditions and the privacy policy')

        # Некоректне ім'я
        self.iframe.get_by_role(role='checkbox', name='I agree to the terms and conditions and the privacy policy').check()
        self.iframe.get_by_role(role='textbox', name='First Name').fill(f'{first_name}1234')
        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.page.wait_for_timeout(2000)
        expect(self.iframe.locator('li.alert.alert-danger')).to_contain_text('Invalid format.')

        # Некоректне прізвище
        self.iframe.get_by_role(role='textbox', name='First Name').fill(first_name)
        self.iframe.get_by_role(role='textbox', name='Last Name').fill(f'{last_name}1234')
        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.page.wait_for_timeout(2000)
        expect(self.iframe.locator('li.alert.alert-danger')).to_contain_text('Invalid format.')

        # Некоректна пошта
        self.iframe.get_by_role(role='textbox', name='Last Name').fill(last_name)
        self.iframe.get_by_role(role='textbox', name='Email').fill('test')
        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.check_required_fields_validation('Пошта без @+gmail.com дозволена')

        # Некоректна пошта
        self.iframe.get_by_role(role='textbox', name='Email').fill('test@')
        self.iframe.get_by_role(role='button', name='SAVE').click()
        self.check_required_fields_validation('Пошта без gmail.com дозволена')

    def check_registration_form(self):
        expect(self.iframe.locator('#field-id_gender-1')).not_to_be_checked()
        expect(self.iframe.locator('#field-id_gender-2')).not_to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Receive offers from our partners')).not_to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='I agree to the terms and conditions and the privacy policy')).not_to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Sign up for our newsletter')).not_to_be_checked()
        expect(self.iframe.get_by_role(role='checkbox', name='Customer data privacy')).not_to_be_checked()

    def fill_registration_form(self):
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
        self.page.wait_for_timeout(2000)
        expect(self.iframe.locator('div.user-info a.account')).to_contain_text(f'{first_name} {last_name}')
