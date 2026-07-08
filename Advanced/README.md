# Advanced — Gói nâng cao Ngày 2
### Prompt nâng cao · Mô hình dự báo (power curve) · Unit test

Gói này bổ sung cho phần cơ bản trong `Source/`, tập trung vào nội dung **Ngày 2** của khóa học:
prompt có context/bảo mật, một **mô hình AI đơn giản chạy được**, và **unit test** kiểm soát chất lượng.
Toàn bộ tự chứa, không sửa code đã kiểm chứng trong `Source/`.

## Cấu trúc

```
Advanced/
├── Prompt_nang_cao.md              # Phần 1: template prompt 6 thành phần + ví dụ điền sẵn
├── mo_hinh_du_bao.py               # Core logic (hàm dùng chung: đọc, train, dự báo, lưu/nạp)
├── module_9_huan_luyen_mo_hinh.ipynb  # Notebook: huấn luyện + đánh giá + vẽ + lưu model
├── app_du_bao.py                   # Phần 3: API FastAPI /api/du-bao (upload CSV → dự đoán)
├── model/power_curve_model.joblib  # Model đã huấn luyện (do notebook tạo, ~7 MB)
├── tests/                          # Phần 2: unit test (pytest)
│   ├── conftest.py                 #   dữ liệu giả lập + fixture
│   ├── test_xu_ly_du_lieu.py       #   nhánh 1: xử lý dữ liệu
│   ├── test_mo_hinh.py             #   nhánh 2: mô hình
│   └── test_api_du_bao.py          #   API dự báo (TestClient)
└── README.md
```

## Mô hình

- **Bài toán:** hồi quy power-curve — dự đoán `cong_suat_kw` từ `toc_do_gio`, `huong_gio`.
- **Thuật toán:** `RandomForestRegressor` (giới hạn độ sâu để nhỏ gọn ~7 MB, chống overfit).
- **Chất lượng:** R² ≈ **0.91** trên tập kiểm tra (held-out), MAE ≈ **164 kW**.
- **Công dụng:** biết dự báo gió → ước lượng công suất/sản lượng; hoặc so sánh
  thực tế vs dự đoán để phát hiện tua bin chạy dưới mức.

## Cách chạy

**Bước 0 — cài thư viện** (nếu chưa): `pip install -r ../requirements.txt`

**Bước 1 — huấn luyện & lưu model** (chạy một lần): mở và chạy hết
`module_9_huan_luyen_mo_hinh.ipynb` → tạo `model/power_curve_model.joblib`.

**Bước 2 — chạy API dự báo:** chọn **một** trong hai cách (cả hai đều chạy được vì file
tự thêm thư mục của nó vào `sys.path`). Dùng cổng **8001** để không đè lên
`Source/module_8_app_api.py` (đang dùng 8000):
```bash
# Cách 1 — từ trong Advanced/ (app KHÔNG có tiền tố):
cd Advanced
uvicorn app_du_bao:app --reload --port 8001

# Cách 2 — từ thư mục gốc dự án (app CÓ tiền tố "Advanced." — dấu chấm, không phải /):
uvicorn Advanced.app_du_bao:app --reload --port 8001
```
Mở http://127.0.0.1:8001/docs → tại `POST /api/du-bao` bấm **Try it out** → tải lên một
file CSV có cột `toc_do_gio, huong_gio` → nhận công suất dự đoán từng dòng.

Cho máy khác trong LAN (thêm `--host 0.0.0.0`):
```bash
uvicorn Advanced.app_du_bao:app --host 0.0.0.0 --port 8001   # chạy từ gốc dự án
```
(lấy IP máy chủ: Windows `ipconfig`, Linux/macOS `hostname -I`).

**Bước 3 — chạy unit test:**
```bash
cd Advanced
python -m pytest tests/ -v
```
(Nhóm test API sẽ tự **skip** nếu chưa có file model — hãy chạy Bước 1 trước.)

## Ví dụ file CSV để thử `/api/du-bao`

```csv
toc_do_gio,huong_gio
3,180
8,180
12,180
25,180
```
