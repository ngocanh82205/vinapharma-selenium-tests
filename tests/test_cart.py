import pytest

from pages.product_pages import CartPage, ProductDetailPage, ProductListPage


@pytest.mark.smoke
def test_them_vao_gio_tang_so_luong(driver, base_url):
    page = ProductDetailPage(driver, base_url).load("ibuprofen-400mg")
    before = page.cart_count()
    page.add_to_cart()
    page.wait.until(lambda d: page.cart_count() > before)
    assert page.cart_count() == before + 1


def test_them_tu_danh_sach_san_pham(driver, base_url):
    page = ProductListPage(driver, base_url).load()
    before = page.cart_count()
    page.add_first_to_cart()
    page.wait.until(lambda d: page.cart_count() > before)


def test_gio_hang_hien_san_pham_da_them(driver, base_url):
    detail = ProductDetailPage(driver, base_url).load("vien-sui-vitamin-c-1000mg")
    name = detail.name()
    detail.add_to_cart()
    detail.wait.until(lambda d: detail.cart_count() > 0)
    CartPage(driver, base_url).load()
    assert name.lower() in driver.page_source.lower()


@pytest.mark.negative
def test_thanh_toan_khi_chua_dang_nhap_chuyen_ve_login(driver, base_url):
    CartPage(driver, base_url).open("/checkout")
    assert "/login" in driver.current_url or "đăng nhập" in driver.page_source.lower()
