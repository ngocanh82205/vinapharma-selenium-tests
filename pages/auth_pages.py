from pages import locators as L
from pages.base_page import BasePage


class LoginPage(BasePage):
    def load(self):
        return self.open("/login")

    def login(self, email, password):
        self.type(L.LOGIN_EMAIL, email)
        self.type(L.LOGIN_PASSWORD, password)
        self.click(L.LOGIN_SUBMIT)


class RegisterPage(BasePage):
    def load(self):
        return self.open("/register")

    def fill(self, name="", email="", phone="", password="", confirm="", agree=True):
        self.type(L.REG_NAME, name)
        self.type(L.REG_EMAIL, email)
        if self.is_visible(L.REG_PHONE, timeout=1):
            self.type(L.REG_PHONE, phone)
        self.type(L.REG_PASSWORD, password)
        if self.is_visible(L.REG_CONFIRM, timeout=1):
            self.type(L.REG_CONFIRM, confirm)
        if self.is_visible(L.REG_TERMS, timeout=1):
            box = self.find(L.REG_TERMS)
            if box.is_selected() != agree:
                box.click()

    def submit(self):
        self.click(L.REG_SUBMIT)

    def browser_validation_message(self):
        """Lấy thông báo kiểm tra của trình duyệt (thuộc tính required) nếu có."""
        return self.driver.execute_script(
            "const el = document.querySelector('form :invalid');"
            "return el ? el.validationMessage : '';"
        )
