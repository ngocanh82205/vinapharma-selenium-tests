import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_csv(filename):
    """Đọc file CSV trong thư mục data thành danh sách dict (dùng cho data-driven test)."""
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return list(csv.DictReader(f))
