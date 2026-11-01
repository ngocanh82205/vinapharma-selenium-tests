"""Tất cả locator nằm ở một chỗ.

Mở website bằng Chrome -> F12 (DevTools) -> chọn phần tử để kiểm tra lại
các locator đánh dấu "KIỂM TRA". Nếu sai, chỉ cần sửa ở file này.
"""
from selenium.webdriver.common.by import By

# Header / chung
CART_LINK = (By.CSS_SELECTOR, "a[href$='/cart']")
CART_COUNT = (By.CSS_SELECTOR, "a[href$='/cart'] span, a[title='Giỏ hàng'] span")  # KIỂM TRA
SEARCH_INPUT = (By.CSS_SELECTOR, "form input[type='search'], form input[name='q'], form input[name='search'], form input[name='keyword']")  # KIỂM TRA

# Danh sách sản phẩm
PRODUCT_CARD_LINKS = (By.CSS_SELECTOR, "a[href*='/products/']")
ADD_TO_CART_BUTTONS = (By.XPATH, "//button[contains(normalize-space(.), 'Thêm vào giỏ')]")

# Chi tiết sản phẩm
PRODUCT_TITLE = (By.CSS_SELECTOR, "h1")
PRICE_TEXT = (By.XPATH, "//*[contains(text(), '₫')]")

# Đăng nhập
LOGIN_EMAIL = (By.CSS_SELECTOR, "input[name='email'], input[name='login'], input[name='username']")  # KIỂM TRA
LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[name='password']")
LOGIN_SUBMIT = (By.XPATH, "//form//button[contains(normalize-space(.), 'Đăng nhập')]")

# Đăng ký
REG_NAME = (By.CSS_SELECTOR, "input[name='name'], input[name='full_name'], input[name='fullname']")  # KIỂM TRA
REG_EMAIL = (By.CSS_SELECTOR, "input[name='email']")
REG_PHONE = (By.CSS_SELECTOR, "input[name='phone']")  # KIỂM TRA
REG_PASSWORD = (By.CSS_SELECTOR, "input[name='password']")
REG_CONFIRM = (By.CSS_SELECTOR, "input[name='password_confirmation']")  # tên mặc định của Laravel
REG_TERMS = (By.CSS_SELECTOR, "input[type='checkbox']")
REG_SUBMIT = (By.XPATH, "//form//button[contains(normalize-space(.), 'Đăng ký')]")

# Thông báo lỗi (Laravel thường dùng .invalid-feedback / .text-danger / .alert-danger)
ERROR_MESSAGES = (By.CSS_SELECTOR, ".invalid-feedback, .text-danger, .alert-danger, .error, [role='alert']")
