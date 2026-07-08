# PROMPT TEMPLATE — Bộ prompt theo module
### Phân tích dữ liệu SCADA tua bin gió · Wind Turbine SCADA

> **Cách dùng:** mỗi module có một prompt riêng bên dưới. Copy prompt của module cần làm,
> dán cho AI Agent trong VS Code, Agent sẽ sinh file tương ứng. Làm tuần tự từ Module 1.
> Nếu dùng dữ liệu của bạn, chỉ cần thay tên file `T1.csv` bằng đường dẫn file CSV của bạn.
>
> **Dữ liệu:** T1.csv — 5 cột: Date/Time (10 phút/lần), LV ActivePower (kW),
> Wind Speed (m/s), Theoretical_Power_Curve (KWh), Wind Direction (°).
>
> **Luồng nối module:** T1.csv → (M2) du_lieu_sach.csv → các module báo cáo/UI.

---

## MODULE 0 — CÀI ĐẶT THƯ VIỆN & MÔI TRƯỜNG
**Đầu vào:** (không) · **Đầu ra:** requirements.txt + môi trường đã cài đủ thư viện
**Làm một lần** trước khi bắt đầu các module khác.

### Danh sách thư viện dùng trong cả khóa

| Thư viện | Dùng cho module | Vai trò |
|----------|-----------------|---------|
| pandas | tất cả | đọc, xử lý dữ liệu bảng |
| numpy | M2 (làm sạch) | tính toán số, xử lý NaN |
| matplotlib | M3, M5 | vẽ biểu đồ tĩnh (PNG) |
| openpyxl | M4 | ghi file Excel (.xlsx) |
| reportlab | M5 | tạo file PDF |
| plotly | M6, M7 | biểu đồ động (tương tác) |
| streamlit | M7 | dashboard web có server |
| fastapi | M8 | dựng API dữ liệu |
| uvicorn | M8 | server chạy API FastAPI |
| python-multipart | M8 | nhận file tải lên qua API (endpoint upload) |
| jupyter, ipykernel | M1–M5 | chạy notebook (.ipynb) |

Ghi chú: plotly dùng cho dashboard HTML (M6) và Streamlit (M7); fastapi/uvicorn/python-multipart cho API (M8).

### PROMPT (dán cho Agent)

```
Tôi sắp làm một loạt bài phân tích dữ liệu và xuất báo cáo bằng Python trong VS Code,
dùng các thư viện: pandas, numpy, matplotlib, openpyxl, reportlab, plotly, streamlit,
fastapi, uvicorn, python-multipart, và jupyter (để chạy notebook).

Hãy giúp tôi:
1. Tạo một file "requirements.txt" liệt kê các thư viện trên (kèm phiên bản tối thiểu hợp lý).
2. Cho tôi câu lệnh để cài tất cả bằng một dòng từ file requirements.txt.
3. Cho tôi cả câu lệnh cài trực tiếp không cần file (phòng khi không dùng requirements.txt).
4. Viết một đoạn code Python ngắn để kiểm tra tất cả thư viện đã cài thành công
   (import thử và in phiên bản từng thư viện).

Giải thích ngắn gọn mỗi thư viện dùng để làm gì. Chú thích tiếng Việt.
```

### Nội dung requirements.txt (tham khảo — nếu muốn tạo tay)

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
openpyxl>=3.1.0
reportlab>=4.0.0
plotly>=5.18.0
streamlit>=1.30.0
fastapi>=0.110.0
uvicorn>=0.27.0
python-multipart>=0.0.9
jupyter>=1.0.0
ipykernel>=6.0.0
```

### Câu lệnh cài đặt

```
# Cách 1 — cài từ file requirements.txt (khuyến nghị)
pip install -r requirements.txt

# Cách 2 — cài trực tiếp một dòng (không cần file)
pip install pandas numpy matplotlib openpyxl reportlab plotly streamlit fastapi uvicorn python-multipart jupyter ipykernel

# Nếu lệnh pip báo lỗi trên Windows, thử:
py -m pip install -r requirements.txt
```
---

## MODULE 1 — ĐỌC & KHẢO SÁT DỮ LIỆU
**Đầu vào:** Data/input/T1.csv · **Đầu ra:** Source/khao_sat.ipynb (notebook)

```
Tôi đang có file dữ liệu điện gió tua bin lưu trong Data/input/T1.csv (cùng thư mục), gồm 5 cột:
Date/Time (mốc thời gian, 10 phút/lần), LV ActivePower (kW) là công suất thực,
Wind Speed (m/s) là tốc độ gió, Theoretical_Power_Curve (KWh) là công suất lý thuyết,
Wind Direction (°) là hướng gió.

Hãy tạo giúp tôi một file notebook tên "Source/module_1_khao_sat.ipynb" để đọc và khảo sát dữ liệu, gồm các bước:
1. Đọc T1.csv vào DataFrame và hiển thị 5 dòng đầu.
2. In số dòng, số cột và kiểu dữ liệu của từng cột.
3. In thống kê mô tả (describe) cho các cột số.
4. Kiểm tra chất lượng dữ liệu: đếm giá trị thiếu mỗi cột; đếm số dòng có công suất âm;
   đếm số dòng có công suất gần 0 (< 10 kW) nhưng tốc độ gió mạnh (> 5 m/s) — đây là nghi sự cố.
5. Vẽ nhanh histogram phân phối tốc độ gió và công suất để hình dung dữ liệu.

Mỗi bước để trong một ô riêng, có chú thích tiếng Việt, in kết quả rõ ràng.
Đây là bước khảo sát nên chỉ hiển thị kết quả, không xuất file dữ liệu.
```

---

## MODULE 2 — LÀM SẠCH & CHUẨN HÓA DỮ LIỆU
**Đầu vào:** T1.csv · **Đầu ra:** Source/module_2_lam_sach.ipynb (notebook) + Data/output/du_lieu_sach.csv (dữ liệu sạch)

```
Từ file T1.csv (5 cột như trên), hãy tạo một notebook tên "Source/module_2_lam_sach.ipynb" để làm sạch
và chuẩn hóa dữ liệu, rồi lưu ra file "Data/output/du_lieu_sach.csv". Các bước:

1. Đọc T1.csv, đổi tên cột sang dạng ngắn không dấu:
   thoi_gian, cong_suat_kw, toc_do_gio, cong_suat_ly_thuyet, huong_gio.
2. Chuyển cột thoi_gian sang kiểu datetime (định dạng "dd MM yyyy HH:mm"),
   các cột còn lại sang kiểu số.
3. Khử các dòng trùng thời gian, sắp xếp theo thời gian và đặt thoi_gian làm chỉ mục.
4. Loại giá trị ngoài ngưỡng vật lý: công suất 0–3600 kW, tốc độ gió 0–30 m/s,
   hướng gió 0–360 độ. Thay giá trị ngoài ngưỡng bằng NaN rồi nội suy tuyến tính
   (giới hạn 6 bước liên tiếp). Sau đó bỏ các dòng còn thiếu ở cột công suất và tốc độ gió.
5. In số dòng trước và sau khi làm sạch để so sánh.
6. Lưu kết quả ra file "du_lieu_sach.csv".

Mỗi bước một ô, chú thích tiếng Việt. Nhấn mạnh: không xóa hẳn dữ liệu lỗi mà thay bằng NaN
rồi nội suy có kiểm soát, tránh bịa số cho khoảng mất tín hiệu quá dài.
```

---

## MODULE 3 — VẼ BIỂU ĐỒ PHÂN TÍCH
**Đầu vào:** du_lieu_sach.csv · **Đầu ra:** Source/module_3_ve_bieu_do.ipynb (notebook) + 4 file PNG

```
Tôi có file Data/output/du_lieu_sach.csv (đã làm sạch) với các cột:
thoi_gian (chỉ mục thời gian), cong_suat_kw, toc_do_gio, cong_suat_ly_thuyet, huong_gio.

Hãy tạo notebook "Source/module_3_ve_bieu_do.ipynb" vẽ 4 biểu đồ (dùng matplotlib), vừa hiển thị trong notebook vừa lưu ra file PNG vào folder Report:

1. Đường cong công suất: biểu đồ phân tán tốc độ gió (trục X) và công suất thực (trục Y).
   Tô đỏ các điểm nghi sự cố (gió > 5 m/s và công suất < 50% công suất lý thuyết).
   Lưu: duong_cong_cong_suat.png
2. Sản lượng theo tháng: biểu đồ cột tổng công suất theo tháng,
   kèm đường tốc độ gió trung bình trên trục y phụ. Lưu: san_luong_thang.png
3. Phân phối: hai histogram cạnh nhau cho tốc độ gió và công suất. Lưu: phan_phoi.png
4. Công suất theo hướng gió: chia hướng gió thành 8 hướng, vẽ cột công suất trung bình
   mỗi hướng. Lưu: huong_gio.png

Chú thích tiếng Việt. Sau mỗi biểu đồ, thêm một ô markdown nhận xét cách đọc biểu đồ trong file notebook.
```

---

## MODULE 4 — BÁO CÁO EXCEL
**Đầu vào:** du_lieu_sach.csv · **Đầu ra:** Source/bao_cao_excel.ipynb (notebook) + BaoCao_SCADA.xlsx

```
Từ file du_lieu_sach.csv (cột: thoi_gian là chỉ mục, cong_suat_kw, toc_do_gio,
cong_suat_ly_thuyet, huong_gio), hãy tạo notebook "Source/module_4_bao_cao_excel.ipynb" xuất một file
báo cáo Excel tên "Report/BaoCao_SCADA.xlsx" gồm 3 sheet:

1. Sheet "Chi_so_chung": bảng các chỉ số tổng quan — tổng số bản ghi, công suất trung bình,
   tốc độ gió trung bình, số điểm nghi sự cố, tổng thời gian sự cố (giờ).
   Điểm nghi sự cố = gió > 5 m/s và công suất < 50% công suất lý thuyết; mỗi điểm tương ứng 10 phút.
2. Sheet "Tong_hop_thang": tổng hợp theo tháng — tổng sản lượng, công suất trung bình,
   tốc độ gió trung bình, số điểm sự cố.
3. Sheet "Diem_su_co": danh sách các điểm nghi sự cố (thời gian, tốc độ gió, công suất thực,
   công suất lý thuyết).

Dùng pandas ExcelWriter. Chú thích tiếng Việt. In số dòng của mỗi sheet để kiểm chứng.
```

---

## MODULE 5 — BÁO CÁO PDF
**Đầu vào:** du_lieu_sach.csv · **Đầu ra:** Source/module_5_bao_cao_pdf.ipynb (notebook) + Report/BaoCao_SCADA.pdf
**Cần cài:** pip install reportlab matplotlib pandas

```
Từ file du_lieu_sach.csv (cột: thoi_gian là chỉ mục, cong_suat_kw, toc_do_gio,
cong_suat_ly_thuyet, huong_gio), hãy tạo notebook "Source/module_5_bao_cao_pdf.ipynb" tạo một báo cáo PDF
chuyên nghiệp tên "Report/BaoCao_SCADA.pdf" (dùng thư viện reportlab), có cấu trúc:

- Trang bìa: tiêu đề báo cáo, tên bộ dữ liệu, tổng số bản ghi.
- Chương 1: bảng các chỉ số chính (tổng bản ghi, công suất TB, tốc độ gió TB,
  số điểm sự cố, tổng giờ sự cố). Bảng có màu nền tiêu đề và viền.
- Chương 2: đường cong công suất — vẽ biểu đồ scatter gió vs công suất, tô đỏ điểm sự cố,
  lưu PNG tạm rồi chèn vào PDF, kèm đoạn giải thích.
- Chương 3: biểu đồ sản lượng theo tháng (chèn ảnh).
- Chương 4: kết luận và kiến nghị (nêu số điểm sự cố và đề xuất kiểm tra).

Dùng matplotlib.use("Agg"). Sau khi chèn ảnh vào PDF thì xóa file PNG tạm.
Lưu ý: để tránh lỗi font tiếng Việt trong PDF, dùng chữ không dấu cho nội dung PDF.
Chú thích tiếng Việt trong code.
```

---

## MODULE 6 — DASHBOARD HTML TĨNH (Plotly + Bootstrap)
**Đầu vào:** du_lieu_sach.csv · **Đầu ra:** Source/module_6_dashboard.py (file Python) + dashboard.html
**Cần cài:** pip install plotly pandas · **Chạy:** python dashboard.py

```
Từ file du_lieu_sach.csv (cột: thoi_gian là chỉ mục, cong_suat_kw, toc_do_gio,
cong_suat_ly_thuyet, huong_gio), hãy tạo một file Python tên "Source/module_6_dashboard.py" sinh ra
một trang dashboard HTML tĩnh tên "Report/dashboard.html". Trang này dùng Plotly cho biểu đồ động
(zoom, di chuột xem giá trị) và Bootstrap cho giao diện, mở được bằng trình duyệt mà
KHÔNG cần server.

Dashboard gồm:
1. Thanh tiêu đề (navbar) tên "Dashboard Phân tích SCADA - Tua bin gió".
2. Hàng KPI cards: tổng bản ghi, công suất TB, tốc độ gió TB, số điểm sự cố, tổng giờ sự cố.
   (Sự cố = gió > 5 m/s và công suất < 50% lý thuyết; mỗi điểm 10 phút.)
3. Ba biểu đồ Plotly tương tác:
   - Đường cong công suất (scatter gió vs công suất, tô màu theo nghi sự cố, lấy mẫu ~8000 điểm).
   - Sản lượng theo tháng (biểu đồ cột).
   - Công suất trung bình theo ngày (biểu đồ đường).

Kỹ thuật: dùng plotly.io.to_html(fig, include_plotlyjs=..., full_html=False) để lấy div mỗi
biểu đồ; chỉ biểu đồ đầu nhúng plotly.js (include_plotlyjs=True), các biểu đồ sau dùng chung.
Nhúng Bootstrap qua CDN. Ghép tất cả thành một chuỗi HTML và ghi ra file dashboard.html.
Chú thích tiếng Việt. In thông báo sau khi tạo xong file.
```

---

## MODULE 7 — DASHBOARD ĐỘNG STREAMLIT (server local, trỏ IP)
**Đầu vào:** du_lieu_sach.csv · **Đầu ra:** Source/module_7_app.py (file Python)
**Cần cài:** pip install streamlit plotly pandas · **Chạy:** streamlit run app.py

```
Từ file du_lieu_sach.csv (cột: thoi_gian là chỉ mục, cong_suat_kw, toc_do_gio,
cong_suat_ly_thuyet, huong_gio), hãy tạo một ứng dụng Streamlit tên "Source/module_7_app.py" làm dashboard
động chạy trên server local:

1. Thanh bên (sidebar) có bộ lọc tương tác:
   - Chọn tháng (hoặc "Tất cả").
   - Thanh trượt ngưỡng tốc độ gió xét sự cố (3–10 m/s).
   - Thanh trượt ngưỡng hiệu suất xét sự cố (30–80%).
   Sự cố = tốc độ gió > ngưỡng gió VÀ công suất < ngưỡng hiệu suất × công suất lý thuyết.
2. Hàng KPI dùng st.metric: số bản ghi, công suất TB, tốc độ gió TB, số điểm sự cố —
   tất cả cập nhật theo bộ lọc.
3. Biểu đồ Plotly (st.plotly_chart, use_container_width=True):
   - Đường cong công suất (scatter tô màu theo sự cố, lấy mẫu ~8000 điểm).
   - Sản lượng theo tháng (cột) và công suất theo ngày (đường) đặt cạnh nhau.
4. Bảng danh sách điểm sự cố (st.dataframe).

Dùng @st.cache_data cho hàm đọc dữ liệu. Chú thích tiếng Việt.
Ở đầu file, ghi chú cách chạy: "streamlit run Source/module_7_app.py" để chạy local; thêm
"--server.address 0.0.0.0" để máy khác trong mạng LAN truy cập qua http://<IP-máy-chủ>:8501; ghi chú cách lấy địa chỉ ip bằng ipconfig qua terminal
```
Cách chạy: streamlit run Source/module_7_app.py --server.address 0.0.0.0 //Thay server.adress
---

## MODULE 8 — API DỮ LIỆU (FastAPI)
**Đầu vào:** du_lieu_sach.csv + file CSV tải lên · **Đầu ra:** Source/module_8_app_api.py (file Python)
**Cần cài:** pip install fastapi uvicorn pandas python-multipart · **Chạy:** uvicorn app_api:app --reload

> Mục tiêu: hiểu cơ chế API — client gửi request (input) → server trả response (JSON).
> Khác dashboard: API chỉ trả DỮ LIỆU, không kèm giao diện, nên nhiều hệ thống có thể cùng gọi.

```
Tôi muốn xây một API để hiểu cơ chế input/output. Tôi có file du_lieu_sach.csv
(SCADA tua bin gió đã làm sạch) với cột: thoi_gian (chỉ mục), cong_suat_kw, toc_do_gio,
cong_suat_ly_thuyet, huong_gio.

Hãy tạo file Python tên "Source/module_8_app_api.py" dùng FastAPI, gồm các endpoint:

1. GET /api/kpi — trả JSON chỉ số tổng quan: tổng bản ghi, công suất TB, tốc độ gió TB,
   số điểm nghi sự cố, tổng giờ sự cố.
   (Sự cố = gió > 5 m/s và công suất < 50% công suất lý thuyết; mỗi điểm 10 phút.)

2. GET /api/su-co — có tham số tùy chọn "thang" (dạng YYYY-MM); trả danh sách điểm nghi
   sự cố, lọc theo tháng nếu có tham số. Trả về số điểm và danh sách bản ghi JSON.

3. GET /api/bieu-do/san-luong — trả JSON dữ liệu sản lượng theo tháng (tổng công suất,
   tốc độ gió TB mỗi tháng) để client vẽ biểu đồ.

4. POST /api/upload — nhận một file CSV người dùng tải lên (cùng cấu trúc), xử lý và trả
   về KPI của chính file đó. Kiểm tra đuôi .csv, lỗi thì trả thông báo rõ ràng.

Yêu cầu:
- Một hàm dùng chung để đọc dữ liệu và tính cột nghi sự cố.
- Đặt title và description cho API để trang /docs hiển thị đẹp.
- Chú thích tiếng Việt, ghi rõ mỗi endpoint nhận input gì trả output gì.
- Đầu file ghi chú cách chạy "uvicorn app_api:app --reload" và mở /docs để thử.
```

Sau khi chạy: mở **http://127.0.0.1:8000/docs** để thử từng endpoint (bấm "Try it out").
Cho máy khác gọi qua IP: `uvicorn Source.module_8_app_api:app --host 0.0.0.0 --port 8000` → http://<IP>:8000/docs

---

## PROMPT TỔNG HỢP (tùy chọn) — chạy toàn bộ chuỗi
> Dùng khi muốn Agent thực hiện cả quy trình một lần. Nên đã quen từng module trước khi dùng.

```
Tôi có file dữ liệu SCADA tua bin gió tên T1.csv (5 cột: Date/Time 10 phút/lần,
LV ActivePower (kW), Wind Speed (m/s), Theoretical_Power_Curve (KWh), Wind Direction (°)).

Hãy thực hiện tuần tự cả quy trình sau, làm từng bước một, chạy và kiểm tra xong bước trước mới sang bước sau:
1. Làm sạch dữ liệu, lưu ra du_lieu_sach.csv (đổi tên cột không dấu,chuẩn hóa thời gian,
   loại giá trị ngoài ngưỡng, nội suy có kiểm soát).
2. Từ du_lieu_sach.csv, vẽ 4 biểu đồ và lưu PNG.
3. Xuất báo cáo Excel 3 sheet (chỉ số chung, tổng hợp tháng, điểm sự cố).
4. Xuất báo cáo PDF có chương mục và biểu đồ.
5. Tạo file dashboard.py sinh dashboard.html (Plotly + Bootstrap).
6. Tạo file app.py chạy Streamlit làm dashboard động.
7. Tạo file app_api.py dùng FastAPI cung cấp API dữ liệu (endpoint KPI, sự cố, sản lượng, upload CSV).

Điểm sự cố định nghĩa: gió > 5 m/s và công suất < 50% công suất lý thuyết.
Sau mỗi bước, in rõ file đã tạo. Chú thích tiếng Việt. Nếu gặp lỗi, dừng lại báo tôi trước khi tiếp tục.
Các file được sắp xếp như sau: các file .py và .ipynb được xếp vào folder Source; .pdf,. docx, .html, ... được xếp vào folder Report, file .csv, .xlxs, ... được xếp vào folder Data/output
```

---

## Ghi chú khi thực hành

- **Thay dữ liệu của bạn:** đổi `T1.csv` thành đường dẫn file CSV của bạn ở Module 1–2.
  Nếu cột khác tên, sửa phần đổi tên cột trong Module 2.
- **Thứ tự bắt buộc:** Module 2 phải chạy trước (tạo du_lieu_sach.csv) thì các module
  báo cáo/UI mới có đầu vào.
- **Khi lỗi:** copy nguyên văn dòng báo lỗi, dán lại cho Agent kèm câu "sửa giúp tôi lỗi này".
```
