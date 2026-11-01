import os

import pytest

from pages.auth_pages import LoginPage, RegisterPage
from tests.helpers import load_csv

LOGIN_CASES = load_csv("login_invalid.csv")
REGISTER_CASES = load_csv("register_invalid.csv")


@pytest.mark.negative
@pytest.mark.parametrize("row", LOGIN_CASES, ids=[r["case_id"] for r in LOGIN_CASES])
def test_dang_nhap_khong_hop_le(driver, base_url, row):
    """Dữ liệu sai thì phải ở lại trang đăng nhập và có thông báo lỗi."""
    page = LoginPage(driver, base_url).load()
    page.login(row["email"], row["password"])
    assert "/login" in page.url, f"{row['case_id']}: đăng nhập được với dữ liệu sai"
    has_error = page.error_messages() or page.driver.execute_script(
        "const el=document.querySelector('form :invalid'); return el ? el.validationMessage : '';"
    )
    assert has_error, f"{row['case_id']}: không có thông báo lỗi ({row['description']})"


@pytest.mark.auth
def test_dang_nhap_hop_le(driver, base_url):
    email, password = os.getenv("VP_EMAIL"), os.getenv("VP_PASSWORD")
    if not email or not password:
        pytest.skip("Chưa đặt biến môi trường VP_EMAIL / VP_PASSWORD")
    page = LoginPage(driver, base_url).load()
    page.login(email, password)
    page.wait.until(lambda d: "/login" not in d.current_url)


@pytest.mark.negative
@pytest.mark.parametrize("row", REGISTER_CASES, ids=[r["case_id"] for r in REGISTER_CASES])
def test_dang_ky_khong_hop_le(driver, base_url, row):
    """Đăng ký với dữ liệu sai không được tạo tài khoản."""
    page = RegisterPage(driver, base_url).load()
    page.fill(row["name"], row["email"], row["phone"], row["password"], row["confirm"],
              agree=row["agree"].lower() == "true")
    page.submit()
    assert "/register" in page.url, f"{row['case_id']}: đăng ký thành công với dữ liệu sai"
    assert page.error_messages() or page.browser_validation_message(), \
        f"{row['case_id']}: không có thông báo lỗi ({row['description']})"
