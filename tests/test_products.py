import pytest

from pages.product_pages import HomePage, ProductDetailPage, ProductListPage

CATEGORIES = [
    "thuoc", "giam-dau-ha-sot", "khang-sinh-khang-khuan", "tim-mach-huyet-ap", "thuoc-huyet-ap",
    "tieu-hoa", "ho-hap-cam-cum", "than-kinh", "vitamin-khoang-chat",
    "thuc-pham-chuc-nang", "dung-cu-y-te", "cham-soc-da",
]


@pytest.mark.smoke
def test_trang_chu_mo_duoc(driver, base_url):
    page = HomePage(driver, base_url).load()
    assert "VinaPharma" in page.title


@pytest.mark.smoke
@pytest.mark.parametrize("category", CATEGORIES)
def test_loc_theo_danh_muc(driver, base_url, category):
    page = ProductListPage(driver, base_url).load(category=category)
    assert f"category={category}" in page.url
    assert len(page.product_links()) > 0, f"Danh mục {category} không hiển thị sản phẩm nào"


@pytest.mark.parametrize("sort", ["bestseller", "newest"])
def test_sap_xep_san_pham(driver, base_url, sort):
    page = ProductListPage(driver, base_url).load(sort=sort)
    assert len(page.product_links()) > 0


def test_loc_thuoc_ke_don(driver, base_url):
    page = ProductListPage(driver, base_url).load(product_type="ETC")
    assert "type=ETC" in page.url


@pytest.mark.parametrize("keyword", ["Ibuprofen", "Vitamin", "Khẩu trang"])
def test_tim_kiem_co_ket_qua(driver, base_url, keyword):
    results = HomePage(driver, base_url).load().search(keyword)
    assert len(results.product_links()) > 0, f"Không có kết quả cho từ khóa '{keyword}'"


@pytest.mark.negative
def test_tim_kiem_khong_co_ket_qua(driver, base_url):
    results = HomePage(driver, base_url).load().search("xyzkhongtontai123")
    assert "xyzkhongtontai123" in driver.page_source or results.product_links() == []


@pytest.mark.parametrize("slug", ["ibuprofen-400mg", "vien-sui-vitamin-c-1000mg", "khau-trang-y-te-4-lop"])
def test_chi_tiet_san_pham_co_ten_va_gia(driver, base_url, slug):
    page = ProductDetailPage(driver, base_url).load(slug)
    assert page.name() != ""
    assert page.has_price()


@pytest.mark.negative
def test_san_pham_khong_ton_tai(driver, base_url):
    ProductDetailPage(driver, base_url).load("san-pham-khong-ton-tai-xyz")
    assert "404" in driver.title or "không tìm thấy" in driver.page_source.lower()
