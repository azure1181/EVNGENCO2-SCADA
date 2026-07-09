# Prompt bước 2 - Tổng hợp dữ liệu theo ngày

Vai trò:
Bạn là cán bộ hành chính phụ trách tổng hợp nhật ký công việc hằng ngày từ các phân xưởng để chuẩn bị báo cáo cho Lãnh đạo.

Bối cảnh:
Tôi đã có bảng dữ liệu trung gian từ bước 1, được đọc từ toàn bộ các file Excel trong thư mục `data/`. Mỗi dòng dữ liệu thể hiện một nội dung báo cáo của một phân xưởng trong một ngày làm việc.

Bảng dữ liệu trung gian gồm các cột:
- `Tên phân xưởng`
- `STT nguồn`
- `Ngày`
- `Giờ`
- `Trưởng ca`
- `Nội dung`
- `File nguồn`

Nhiệm vụ:
Hãy tổng hợp nội dung công việc theo từng ngày làm việc từ tất cả các phân xưởng. Với mỗi ngày, liệt kê chi tiết từng phân xưởng, thời gian bắt đầu ca, trưởng ca và nội dung công việc/báo cáo đạt được.

Ràng buộc:
- Nhóm dữ liệu theo cột `Ngày`.
- Trong mỗi ngày, sắp xếp theo `Tên phân xưởng`, sau đó theo `Giờ`.
- Giữ đầy đủ thông tin của từng phân xưởng, không gộp mất nội dung chi tiết.
- Nếu cùng một phân xưởng có nhiều dòng trong cùng một ngày, giữ từng dòng riêng hoặc ghép theo thứ tự thời gian, nhưng không làm mất thông tin.
- Nếu thiếu `Trưởng ca`, hiển thị là `Chưa cập nhật`.
- Nếu thiếu `Nội dung`, hiển thị là `Chưa cập nhật`.
- Không thêm nhận xét chủ quan ngoài dữ liệu nguồn.

Kết quả mong muốn:
Tạo được bảng tổng hợp theo ngày với cấu trúc dễ kiểm tra, gồm các thông tin:
- `Ngày`
- `Tên phân xưởng`
- `Giờ`
- `Trưởng ca`
- `Nội dung`

Ví dụ tổng hợp thử cho ngày `2026-01-07`:

| Ngày | Tên phân xưởng | Giờ | Trưởng ca | Nội dung |
| --- | --- | --- | --- | --- |
| 2026-01-07 | PX_1 | 08:00 | Nguyễn Văn A | Báo cáo 1 |
| 2026-01-07 | PX_2 | 08:00 | Đoàn Văn A | Báo cáo 1 |
| 2026-01-07 | PX_3 | 08:00 | Trần Văn A | Báo cáo 1 |

Bảng tổng hợp này sẽ được dùng cho bước 3 để tạo file Excel báo cáo cuối cùng.
