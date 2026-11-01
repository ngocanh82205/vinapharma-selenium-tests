from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages import locators as L


class BasePage:
    TIMEOUT = 10

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def open(self, path=""):
        self.driver.get(f"{self.base_url}{path}")
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @property
    def url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title

    def cart_count(self):
        """Số trên biểu tượng giỏ hàng ở header."""
        try:
            text = self.find(L.CART_COUNT).text.strip()
            return int(text) if text.isdigit() else 0
        except TimeoutException:
            return 0

    def error_messages(self):
        return [e.text.strip() for e in self.driver.find_elements(*L.ERROR_MESSAGES) if e.text.strip()]
