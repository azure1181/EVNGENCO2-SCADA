# Prompt bước 3 - Tạo file Excel tổng hợp

## Dữ liệu tổng hợp thử cho 1 ngày

Ngày làm việc: 2026-01-07

| STT | Ngày | Tên phân xưởng | Nội dung |
| --- | --- | --- | --- |
| 1 | 2026-01-07 | PX_1 | Trưởng ca: Nguyễn Văn A. Nội dung báo cáo: Báo cáo 1 |
| 2 | 2026-01-07 | PX_2 | Trưởng ca: Đoàn Văn A. Nội dung báo cáo: Báo cáo 1 |
| 3 | 2026-01-07 | PX_3 | Trưởng ca: Trần Văn A. Nội dung báo cáo: Báo cáo 1 |

## Prompt chuẩn

Vai trò:
Bạn là cán bộ hành chính phụ trách tổng hợp báo cáo sản xuất, chuẩn bị file Excel báo cáo cho Lãnh đạo.

Bối cảnh:
Tôi đã có bảng tổng hợp theo ngày từ bước 2. Bảng này chứa dữ liệu công việc của từng phân xưởng theo từng ngày làm việc, bao gồm ngày, tên phân xưởng, giờ bắt đầu ca, trưởng ca và nội dung báo cáo.

Mục tiêu của bước 3 là tạo file Excel tổng hợp cuối cùng để gửi Lãnh đạo.

Nhiệm vụ:
Hãy tạo file Excel tổng hợp từ dữ liệu đã được xử lý ở bước 2.

File Excel đầu ra gồm 4 cột:
- `STT`: số thứ tự trong bảng tổng hợp
- `Ngày`: ngày làm việc
- `Tên phân xưởng`: tên phân xưởng lấy từ tên file nguồn hoặc dữ liệu trung gian
- `Nội dung`: ghép tên trưởng ca và nội dung báo cáo theo định dạng: `Trưởng ca: [Tên trưởng ca]. Nội dung báo cáo: [Nội dung]`

Ràng buộc:
- Mỗi dòng trong file đầu ra tương ứng với một phân xưởng trong một ngày làm việc.
- Nếu cùng một phân xưởng có nhiều nội dung trong cùng một ngày, ghép các nội dung theo thứ tự thời gian và xuống dòng trong cùng ô `Nội dung`.
- Nếu thiếu `Trưởng ca`, ghi `Trưởng ca: Chưa cập nhật`.
- Nếu thiếu `Nội dung`, ghi `Nội dung báo cáo: Chưa cập nhật`.
- Sắp xếp dữ liệu theo `Ngày`, sau đó theo `Tên phân xưởng`.
- Định dạng cột `Ngày` theo kiểu `yyyy-mm-dd`.
- Tên sheet đầu ra là `Tong hop`.
- Tên file đầu ra là `tong_hop_bao_cao.xlsx`.
- Bảng cần có hàng tiêu đề rõ ràng.
- Tự động điều chỉnh độ rộng cột.
- Bật wrap text cho cột `Nội dung`.
- Giữ nội dung ngắn gọn, rõ ràng, phù hợp làm báo cáo cho Lãnh đạo.

Kết quả mong muốn:
Tạo file Excel `tong_hop_bao_cao.xlsx` có cấu trúc đúng 4 cột nêu trên, dữ liệu sạch, dễ đọc và sẵn sàng gửi Lãnh đạo.
