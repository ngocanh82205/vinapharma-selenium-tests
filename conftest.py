import os
from datetime import datetime

import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--base-url", default="https://vinapharma.click", help="Địa chỉ website cần test")
    parser.addoption("--headless", action="store_true", help="Chạy Chrome không hiện cửa sổ")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    # Selenium 4.6+ tự tải ChromeDriver phù hợp (Selenium Manager)
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # chỉ dùng explicit wait trong Page Object
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Chụp màn hình khi test thất bại và lưu vào reports/screenshots."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs("reports/screenshots", exist_ok=True)
            name = f"{item.name}_{datetime.now():%H%M%S}.png"
            drv.save_screenshot(os.path.join("reports/screenshots", name))
