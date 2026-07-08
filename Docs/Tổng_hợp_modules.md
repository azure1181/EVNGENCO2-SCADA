# TỔNG HỢP CÁC MODULE — Phân loại theo định dạng
### Khóa Ứng dụng AI · Wind Turbine SCADA

Mô hình: **notebook để HIỂU luồng · file .py để CHẠY & đóng gói**.
Sơ đồ tổng quan luồng cả khóa được vẽ riêng (Figma).

---

## Nhóm 1 — MODULE PHÂN TÍCH DỮ LIỆU (định dạng chính: NOTEBOOK)
> Chạy từng ô để thấy dữ liệu biến đổi qua từng bước. Có kèm .py để chạy nhanh/tự động.

| Mã | Tên | Đầu vào | Đầu ra | File |
|----|-----|---------|--------|------|
| M0 | Cài đặt thư viện | (không) | requirements.txt | prompt (trong Prompt_template) |
| D1 | Đọc & khảo sát | T1.csv | (in ra màn hình) | .ipynb + .py + prompt |
| D2 | Làm sạch & chuẩn hóa | T1.csv | du_lieu_sach.csv | .ipynb + .py + prompt |
| O1 | Vẽ biểu đồ | du_lieu_sach.csv | 4 file PNG | .ipynb + .py + prompt |
| O2 | Báo cáo Excel | du_lieu_sach.csv | BaoCao_SCADA.xlsx | .ipynb + .py + prompt |
| O3 | Báo cáo PDF | du_lieu_sach.csv | BaoCao_SCADA.pdf | .ipynb + .py + prompt |

**Cách dạy nhóm này:** học viên vibecode trong notebook → agent điền code vào ô →
chạy Shift+Enter thấy kết quả từng bước → hiểu luồng dữ liệu.

---

## Nhóm 2 — MODULE ỨNG DỤNG / UI (định dạng chính: FILE .PY)
> Bản chất là ứng dụng chạy độc lập, không hợp notebook. Chạy bằng terminal.

| Mã | Tên | Đầu vào | Cách chạy | File |
|----|-----|---------|-----------|------|
| O5 | Dashboard HTML tĩnh | du_lieu_sach.csv | python O5...py → mở dashboard.html | .py + prompt |
| O6 | Dashboard Streamlit | du_lieu_sach.csv | streamlit run O6...py → trỏ IP | .py + prompt + README |
| O7 | API dữ liệu (FastAPI) | du_lieu_sach.csv + file upload | uvicorn O7...:app → /docs, trỏ IP | .py + prompt + README |

**Cách dạy nhóm này:** giải thích cấu trúc file .py (hoặc để agent vibecode ra file),
rồi chạy bằng terminal. Phần "hiểu luồng" đã có sơ đồ Figma tổng quan.

---

## Luồng nối các module (đầu ra module này = đầu vào module sau)

```
T1.csv
  │
  ├─ D1 (khảo sát, chỉ xem)
  │
  └─ D2 ──► du_lieu_sach.csv
              │
              ├─ O1 ──► 4 PNG
              ├─ O2 ──► Excel
              ├─ O3 ──► PDF
              ├─ O5 ──► dashboard.html (mở trình duyệt)
              ├─ O6 ──► web app (streamlit, trỏ IP)
              └─ O7 ──► API (fastapi, /docs, trỏ IP)
```

**Điểm mấu chốt để dạy:** mọi module đều bắt đầu từ `du_lieu_sach.csv` (trừ D1, D2).
Đây là "điểm nối" — làm sạch một lần, dùng cho mọi báo cáo. Đúng tinh thần chia module.

---

## Quy ước 3 file mỗi module

- **PROMPT_xx.md** — prompt để học viên dán cho Agent (vibecode).
- **xx.ipynb** — notebook để hiểu luồng (chỉ nhóm phân tích).
- **xx.py** — code chạy được / đóng gói.

Bước cuối khóa: PROMPT TỔNG HỢP — thay path CSV, agent tự sinh toàn bộ chuỗi module.
