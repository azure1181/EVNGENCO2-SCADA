# PROMPT NÂNG CAO — Advanced Prompt Engineering (Ngày 2)
### Khóa Ứng dụng AI · Wind Turbine SCADA · EVNGENCO2

> Prompt "rỗng" (chỉ nêu yêu cầu) thường cho code sai đơn vị, thiếu kiểm chứng, hoặc vô tình
> đưa dữ liệu nhạy cảm lên công cụ AI. Prompt **nâng cao** đóng khung đủ **6 thành phần** để
> AI hiểu đúng bối cảnh, tôn trọng ràng buộc bảo mật, và tạo ra sản phẩm **kiểm chứng được**.

---

## 1. Sáu thành phần của một prompt nâng cao

| # | Thành phần | Trả lời câu hỏi | Vì sao cần |
|---|-----------|-----------------|-----------|
| 1 | **Vai trò** (role) | AI đóng vai ai? | Định hình văn phong, mức độ chuyên môn, thư viện ưu tiên |
| 2 | **Bối cảnh & dữ liệu** (context) | Dữ liệu gì, cột nào, đơn vị, tần suất? | Tránh AI đoán sai cấu trúc/đơn vị dữ liệu |
| 3 | **Dữ liệu mẫu** (sample) | Vài dòng minh họa thật (đã ẩn danh) | AI khớp đúng định dạng, tên cột, kiểu giá trị |
| 4 | **Tiêu chí đầu ra** (output) | Sản phẩm gồm gì, chạy thế nào, định dạng nào? | Nhận đúng thứ cần, không thừa/thiếu |
| 5 | **Ràng buộc bảo mật** (security) | Được/không được đưa gì lên AI? | Không lộ dữ liệu vận hành/cá nhân/nội bộ |
| 6 | **Tiêu chí kiểm chứng** (verification) | Làm sao biết kết quả đúng? | Buộc AI kèm cách tự kiểm tra, test case |

---

## 2. Template rỗng (sao chép & điền)

```text
[VAI TRÒ]
Bạn là <ví dụ: kỹ sư dữ liệu Python, cẩn thận, ưu tiên code rõ ràng, có chú thích tiếng Việt>.

[BỐI CẢNH & DỮ LIỆU]
Tôi đang xử lý <mô tả bài toán>.
Dữ liệu ở <đường dẫn>, gồm các cột:
- <ten_cot> (<ý nghĩa>, <đơn vị>, <tần suất/kiểu>)
- ...
Lưu ý nghiệp vụ: <quy tắc tính, ngưỡng, định nghĩa đặc thù — ví dụ "điểm sự cố = ...">.

[DỮ LIỆU MẪU]  (đã ẩn danh)
<dán 3–5 dòng đầu thật hoặc mô phỏng>

[TIÊU CHÍ ĐẦU RA]
- Sản phẩm: <notebook / file .py / API / báo cáo ...>
- Cách chạy: <lệnh cụ thể>
- Định dạng/đặt tên: <ví dụ path, tên hàm, tên file output>
- Ràng buộc kỹ thuật: <thư viện, phiên bản, tách hàm dùng chung, ...>

[RÀNG BUỘC BẢO MẬT]
- Chỉ dùng dữ liệu mẫu/mô phỏng/ẩn danh. KHÔNG đưa dữ liệu vận hành thật, dữ liệu cá nhân,
  mã thiết bị/hệ thống, thông tin tài chính/nội bộ chưa được phê duyệt.
- Không nhúng đường dẫn nội bộ, khóa API, mật khẩu, tên máy chủ thật vào code hay ví dụ.
- Nếu cần minh họa, hãy tạo dữ liệu giả.

[TIÊU CHÍ KIỂM CHỨNG]
- Nêu cách tự kiểm tra kết quả (giá trị kỳ vọng, khoảng hợp lệ).
- Kèm ít nhất <N> test case (gồm ca biên và ca lỗi).
- Giải thích ngắn gọn phương án TRƯỚC khi viết code.
```

---

## 3. Ví dụ điền sẵn — prompt đã tạo ra chính module dự báo trong folder này

> Đây là prompt thật đã dùng để sinh `mo_hinh_du_bao.py`, `module_9_huan_luyen_mo_hinh.ipynb`
> và `app_du_bao.py`. Chú ý cách 6 thành phần lồng vào nhau.

```text
[VAI TRÒ]
Bạn là kỹ sư ML Python thực dụng. Ưu tiên code rõ ràng, tách "hàm dùng chung" để
notebook, API và unit test cùng gọi. Chú thích bằng tiếng Việt.

[BỐI CẢNH & DỮ LIỆU]
Tôi có dữ liệu SCADA tua bin gió đã làm sạch tại Data/output/du_lieu_sach.csv.
Cột (chỉ mục là thoi_gian, tần suất 10 phút/lần):
- cong_suat_kw          (công suất thực, kW)
- toc_do_gio            (tốc độ gió, m/s)
- cong_suat_ly_thuyet   (công suất lý thuyết, kWh)
- huong_gio             (hướng gió, độ 0–360)
Bài toán: hồi quy power-curve — dự đoán cong_suat_kw từ (toc_do_gio, huong_gio).
Mục đích: biết dự báo gió → ước lượng công suất; so sánh thực tế vs dự đoán để
phát hiện tua bin chạy dưới mức.

[DỮ LIỆU MẪU]
thoi_gian,cong_suat_kw,toc_do_gio,cong_suat_ly_thuyet,huong_gio
2018-01-01 00:00:00,380.05,5.31,416.33,259.99
2018-01-01 00:10:00,453.77,5.67,519.92,268.64

[TIÊU CHÍ ĐẦU RA]
- Một file core (hàm dùng chung): đọc dữ liệu, tách X/y, huấn luyện, đánh giá,
  lưu/nạp model (.joblib), dự báo. Công suất dự đoán phải được chặn >= 0.
- Một notebook: huấn luyện + đánh giá (R², MAE, RMSE trên tập held-out) + vẽ đường
  cong công suất thực tế vs dự đoán + lưu model.
- Một API FastAPI: POST /api/du-bao nhận file CSV (cột toc_do_gio, huong_gio) → trả
  công suất dự đoán từng dòng; có /docs đẹp; chạy được cho máy khác trong LAN.
- Dùng scikit-learn; giữ file model nhỏ (~vài MB).

[RÀNG BUỘC BẢO MẬT]
- Chỉ dùng dữ liệu mẫu đã ẩn danh này. Không thêm dữ liệu vận hành thật khác.
- Không nhúng IP thật, khóa API, đường dẫn nội bộ vào code; đường dẫn để tương đối.
- Endpoint upload phải kiểm tra đuôi .csv và từ chối file lạ.

[TIÊU CHÍ KIỂM CHỨNG]
- R² trên tập kiểm tra phải > 0.8; dự đoán tăng theo tốc độ gió rồi bão hòa.
- Kèm unit test: logic tách X/y, ca thiếu cột (báo lỗi), dự đoán không âm,
  và test API cho ca hợp lệ / sai đuôi / thiếu cột.
- Giải thích phương án trước khi viết code.
```

---

## 4. Đối chiếu prompt "rỗng" vs "nâng cao"

| Prompt rỗng | Hệ quả thường gặp | Prompt nâng cao khắc phục bằng |
|---|---|---|
| "Viết code dự đoán công suất gió" | Sai tên cột, sai đơn vị, không lưu model | Thành phần 2 + 3 (context + mẫu) |
| Không nói định dạng đầu ra | Trả 1 script lộn xộn, khó ghép | Thành phần 4 (tiêu chí đầu ra) |
| Dán cả file dữ liệu thật lên AI | Rò rỉ dữ liệu vận hành | Thành phần 5 (bảo mật) |
| Không yêu cầu kiểm chứng | Code chạy nhưng kết quả sai âm thầm | Thành phần 6 (kiểm chứng + test) |

---

## 5. Checklist rút gọn trước khi bấm gửi prompt

- [ ] Đã nêu **vai trò** cho AI?
- [ ] Đã mô tả **cột + đơn vị + tần suất** dữ liệu?
- [ ] Đã dán **vài dòng mẫu đã ẩn danh** (không phải dữ liệu thật nhạy cảm)?
- [ ] Đã ghi rõ **sản phẩm + cách chạy + đặt tên/đường dẫn**?
- [ ] Đã nêu **ràng buộc bảo mật** (không dữ liệu thật/khóa/IP nội bộ)?
- [ ] Đã yêu cầu **cách kiểm chứng + test case**?
- [ ] Đã yêu cầu AI **giải thích phương án trước khi viết code**?

> Nguyên tắc an toàn dữ liệu chi tiết: xem mục 10 của *Kế hoạch khóa học*. Quy tắc vàng —
> **chỉ dùng dữ liệu mẫu/mô phỏng/ẩn danh trên công cụ AI công cộng.**
