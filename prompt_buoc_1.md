# Prompt bước 1 - Đọc dữ liệu Excel nguồn

Vai trò:
Bạn là cán bộ hành chính phụ trách kiểm tra và chuẩn hóa dữ liệu báo cáo sản xuất trước khi tổng hợp gửi Lãnh đạo.

Bối cảnh:
Tôi có nhiều file Excel trong thư mục `data/`. Mỗi file Excel đại diện cho một phân xưởng. Tên phân xưởng được lấy từ tên file, ví dụ `PX_1.xlsx` tương ứng với phân xưởng `PX_1`.

Mỗi file Excel có 5 cột dữ liệu:
- `STT`: số thứ tự
- `Ngày`: ngày làm việc
- `Giờ` hoặc `Thời gian`: thời gian bắt đầu ca
- `Trưởng ca`: tên người phụ trách ca
- `Nội dung`: nội dung công việc/báo cáo đạt được

Nhiệm vụ:
Hãy đọc toàn bộ các file `.xlsx` trong thư mục `data/`, trích xuất dữ liệu ở 5 cột trên và bổ sung thêm thông tin `Tên phân xưởng` từ tên file nguồn.

Ràng buộc:
- Chỉ đọc các file có phần mở rộng `.xlsx`.
- Bỏ qua hàng tiêu đề trong từng file nguồn.
- Chỉ lấy các dòng có dữ liệu hợp lệ ở cột `Ngày`.
- Giữ ngày ở dạng dữ liệu ngày, không chuyển thành chuỗi nếu đang xử lý trong Excel.
- Nếu tên cột thời gian là `Giờ` hoặc `Thời gian` thì đều hiểu là thời gian bắt đầu ca.
- Nếu thiếu `Trưởng ca`, ghi nhận là `Chưa cập nhật`.
- Nếu thiếu `Nội dung`, ghi nhận là `Chưa cập nhật`.
- Không tự ý sửa nội dung báo cáo, chỉ chuẩn hóa phần trống và tên phân xưởng.

Kết quả mong muốn:
Tạo được một bảng dữ liệu trung gian gồm các cột:
- `Tên phân xưởng`
- `STT nguồn`
- `Ngày`
- `Giờ`
- `Trưởng ca`
- `Nội dung`
- `File nguồn`

Bảng dữ liệu trung gian này sẽ được dùng cho bước 2 để tổng hợp theo ngày.
