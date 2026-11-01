from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages import locators as L
from pages.base_page import BasePage


class HomePage(BasePage):
    def load(self):
        return self.open("/")

    def search(self, keyword):
        self.type(L.SEARCH_INPUT, keyword)
        self.find(L.SEARCH_INPUT).send_keys(Keys.ENTER)
        return ProductListPage(self.driver, self.base_url)


class ProductListPage(BasePage):
    def load(self, category=None, sort=None, product_type=None):
        params = []
        if category:
            params.append(f"category={category}")
        if sort:
            params.append(f"sort={sort}")
        if product_type:
            params.append(f"type={product_type}")
        query = ("?" + "&".join(params)) if params else ""
        return self.open(f"/products{query}")

    def product_links(self):
        links = self.find_all(L.PRODUCT_CARD_LINKS)
        return list(dict.fromkeys(a.get_attribute("href") for a in links if a.get_attribute("href")))

    def add_first_to_cart(self):
        self.click(L.ADD_TO_CART_BUTTONS)


class ProductDetailPage(BasePage):
    def load(self, slug):
        return self.open(f"/products/{slug}")

    def name(self):
        return self.find(L.PRODUCT_TITLE).text.strip()

    def has_price(self):
        return self.is_visible(L.PRICE_TEXT)

    def add_to_cart(self):
        self.click(L.ADD_TO_CART_BUTTONS)


class CartPage(BasePage):
    def load(self):
        return self.open("/cart")

    def wait_url_contains(self, part):
        return self.wait.until(EC.url_contains(part))
