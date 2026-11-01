# Kiểm thử tự động website VinaPharma với Selenium + Python

Bộ kiểm thử giao diện tự động cho website nhà thuốc trực tuyến https://vinapharma.click, viết bằng Python, Selenium WebDriver và pytest, theo mô hình Page Object Model (POM).

## Phạm vi kiểm thử (41 test case)

| Nhóm | File | Số case | Nội dung |
| --- | --- | --- | --- |
| Sản phẩm | `tests/test_products.py` | 24 | Mở trang chủ, lọc 12 danh mục, sắp xếp bán chạy/mới nhất, lọc thuốc kê đơn (ETC), tìm kiếm có/không có kết quả, trang chi tiết có tên và giá, sản phẩm không tồn tại |
| Giỏ hàng | `tests/test_cart.py` | 4 | Thêm vào giỏ từ trang chi tiết và trang danh sách, giỏ hàng hiển thị đúng sản phẩm, vào trang thanh toán khi chưa đăng nhập |
| Tài khoản | `tests/test_auth.py` | 13 | 6 case đăng nhập sai và 6 case đăng ký sai (đọc từ file CSV), 1 case đăng nhập đúng (cần tài khoản thật) |

## Cấu trúc thư mục

```
vinapharma-selenium-tests/
├── conftest.py          # Khởi tạo Chrome, tham số --base-url, --headless, chụp màn hình khi test lỗi
├── pytest.ini           # Cấu hình pytest, xuất báo cáo HTML
├── requirements.txt
├── pages/               # Page Object: mỗi trang web là một lớp
│   ├── locators.py      # TẤT CẢ locator ở một chỗ
│   ├── base_page.py     # Hàm dùng chung: chờ, click, nhập, đọc lỗi
│   ├── product_pages.py # Trang chủ, danh sách, chi tiết sản phẩm, giỏ hàng
│   └── auth_pages.py    # Đăng nhập, đăng ký
├── data/                # Dữ liệu test (data-driven)
│   ├── login_invalid.csv
│   └── register_invalid.csv
└── tests/               # Các kịch bản kiểm thử
```

## Cài đặt

Cần Python 3.10+ và trình duyệt Chrome.

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

Selenium 4.6 trở lên tự tải ChromeDriver, không cần cài riêng.

## Chạy test

```bash
pytest                         # chạy tất cả, mở Chrome
pytest --headless              # chạy ngầm, không hiện cửa sổ
pytest -m smoke                # chỉ chạy test nhanh
pytest -m negative             # chỉ chạy test dữ liệu sai
pytest tests/test_auth.py      # chạy một file
pytest --base-url http://localhost:8000   # test bản chạy local
```

Đăng nhập với tài khoản thật (Windows PowerShell):

```powershell
$env:VP_EMAIL="email@cua-ban.com"; $env:VP_PASSWORD="matkhau"; pytest -m auth
```

Kết quả: mở `reports/report.html`. Ảnh chụp màn hình các test lỗi nằm trong `reports/screenshots/`.

## Việc cần làm trước khi chạy lần đầu

Các locator đánh dấu `KIỂM TRA` trong `pages/locators.py` được viết theo cách đặt tên mặc định của Laravel, chưa đối chiếu với HTML thật. Kiểm tra lại như sau:

1. Mở trang bằng Chrome, nhấn F12, bấm biểu tượng mũi tên rồi click vào ô cần kiểm tra.
2. Xem thuộc tính `name`, `id` hoặc `class` của phần tử.
3. Sửa locator trong `pages/locators.py` nếu khác. Không cần sửa file test.

Các test đăng ký chỉ dùng dữ liệu sai nên không tạo tài khoản thật trên website.

## Kiến thức cần nắm để giải thích khi phỏng vấn

- **Page Object Model:** tách locator và thao tác của từng trang ra khỏi kịch bản test. Khi giao diện đổi, chỉ sửa một chỗ.
- **Explicit wait** (`WebDriverWait` + `expected_conditions`): chờ đến khi phần tử hiển thị hoặc click được, thay vì `time.sleep`. Giúp test ổn định, ít lỗi chập chờn (flaky).
- **Data-driven testing:** dữ liệu nằm trong CSV, `@pytest.mark.parametrize` sinh mỗi dòng thành một test case riêng.
- **Fixture** (`conftest.py`): mở trình duyệt trước mỗi test và đóng sau test.
- **Marker** (`smoke`, `negative`, `auth`): chọn nhóm test cần chạy.
- **Kiểm tra validate của trình duyệt:** với ô có thuộc tính `required`, thông báo lỗi do trình duyệt hiển thị chứ không nằm trong HTML, nên phải đọc `validationMessage` bằng JavaScript.
- **Kỹ thuật thiết kế test case:** phân vùng tương đương (email đúng/sai định dạng), giá trị biên (mật khẩu quá ngắn), kiểm thử bảo mật cơ bản (chuỗi SQL injection).
