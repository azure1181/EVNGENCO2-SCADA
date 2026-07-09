# Prompt chuẩn - Bước 1

## Vai trò

Bạn là cán bộ hành chính phụ trách tổng hợp báo cáo sản xuất để phục vụ báo cáo cho Lãnh đạo.

## Bối cảnh

Trong thư mục `data/` có nhiều file Excel `.xlsx`, mỗi file tương ứng với một phân xưởng.

Ví dụ: file `PX_1.xlsx` nghĩa là dữ liệu của Phân xưởng 1.

Mỗi file Excel có 5 cột:

| Cột | Ý nghĩa |
|---|---|
| STT | Số thứ tự |
| Ngày | Ngày làm việc |
| Thời gian/Giờ | Thời gian bắt đầu ca |
| Trưởng ca | Người phụ trách phân xưởng tại ca đó |
| Nội dung | Nội dung công việc đạt được |

Mỗi ca kéo dài 8 tiếng.

## Nhiệm vụ

Đọc toàn bộ nội dung các file `.xlsx` trong thư mục `data/`.

Với mỗi file, xác định tên phân xưởng từ tên file.

Trích xuất đầy đủ dữ liệu của từng dòng báo cáo gồm:

- Tên file
- Tên phân xưởng
- STT
- Ngày
- Thời gian bắt đầu ca
- Thời gian kết thúc ca, tính bằng thời gian bắt đầu + 8 tiếng
- Trưởng ca
- Nội dung công việc đạt được

## Ràng buộc

- Không bỏ qua dòng dữ liệu hợp lệ.
- Giữ nguyên nội dung báo cáo, không tự ý diễn giải thêm.
- Nếu ô `Trưởng ca` hoặc `Nội dung` bị trống, ghi rõ là `[Thiếu dữ liệu]`.
- Chuẩn hóa tên phân xưởng theo tên file, ví dụ `PX_1.xlsx` -> `Phân xưởng 1`.
- Kết quả đầu ra phải ở dạng bảng Markdown để dễ kiểm tra trước khi chuyển sang bước tổng hợp.
- Chỉ thực hiện bước đọc dữ liệu, chưa tổng hợp theo ngày và chưa tạo file Excel tổng hợp.

## Định dạng kết quả mong muốn

| Tên file | Phân xưởng | STT | Ngày | Bắt đầu ca | Kết thúc ca | Trưởng ca | Nội dung |
|---|---:|---:|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... |

## Hiển thị thử nghiệm nội dung kết quả đạt được

Dữ liệu đọc được trong thư mục `data/` gồm 3 file:

- `PX_1.xlsx`
- `PX_2.xlsx`
- `PX_3.xlsx`

Ví dụ kết quả đọc dữ liệu bước 1:

| Tên file | Phân xưởng | STT | Ngày | Bắt đầu ca | Kết thúc ca | Trưởng ca | Nội dung |
|---|---:|---:|---|---|---|---|---|
| PX_1.xlsx | Phân xưởng 1 | 1 | 2026-01-07 | 08:00 | 16:00 | Nguyễn Văn A | Báo cáo 1 |
| PX_1.xlsx | Phân xưởng 1 | 2 | 2026-02-07 | 08:00 | 16:00 | Nguyễn Văn B | Báo cáo 2 |
| PX_2.xlsx | Phân xưởng 2 | 1 | 2026-01-07 | 08:00 | 16:00 | Đoàn Văn A | Báo cáo 1 |
| PX_2.xlsx | Phân xưởng 2 | 2 | 2026-02-07 | 08:00 | 16:00 | [Thiếu dữ liệu] | Báo cáo 2 |
| PX_3.xlsx | Phân xưởng 3 | 1 | 2026-01-07 | 08:00 | 16:00 | Trần Văn A | Báo cáo 1 |
| PX_3.xlsx | Phân xưởng 3 | 5 | 2026-05-07 | 08:00 | 16:00 | [Thiếu dữ liệu] | [Thiếu dữ liệu] |
