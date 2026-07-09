# Prompt chuẩn - Bước 2

## Vai trò

Bạn là cán bộ hành chính phụ trách tổng hợp báo cáo sản xuất để phục vụ báo cáo cho Lãnh đạo.

## Bối cảnh

Đã hoàn thành bước 1: đọc toàn bộ nội dung các file Excel `.xlsx` trong thư mục `data/`.

Mỗi file dữ liệu tương ứng với một phân xưởng.

Ví dụ: file `PX_1.xlsx` nghĩa là dữ liệu của Phân xưởng 1.

Dữ liệu sau bước 1 gồm các thông tin:

| Trường dữ liệu | Ý nghĩa |
|---|---|
| Tên file | File Excel nguồn |
| Phân xưởng | Tên phân xưởng được xác định từ tên file |
| STT | Số thứ tự trong file nguồn |
| Ngày | Ngày làm việc |
| Bắt đầu ca | Thời gian bắt đầu ca |
| Kết thúc ca | Thời gian kết thúc ca, tính bằng bắt đầu ca + 8 tiếng |
| Trưởng ca | Người phụ trách phân xưởng tại ca đó |
| Nội dung | Nội dung công việc đạt được |

Mỗi ca kéo dài 8 tiếng.

## Nhiệm vụ

Tổng hợp nội dung công việc theo từng ngày từ toàn bộ dữ liệu đã đọc ở bước 1.

Với mỗi ngày làm việc, gom tất cả báo cáo của các phân xưởng trong ngày đó thành một nhóm.

Trong từng ngày, trình bày chi tiết theo từng phân xưởng, gồm:

- Tên phân xưởng
- Thời gian ca làm việc
- Trưởng ca
- Nội dung công việc đạt được

Sắp xếp kết quả theo thứ tự:

1. Ngày làm việc tăng dần.
2. Trong cùng một ngày, sắp xếp theo tên phân xưởng tăng dần.
3. Nếu một phân xưởng có nhiều ca trong cùng ngày, sắp xếp theo thời gian bắt đầu ca tăng dần.

## Ràng buộc

- Chỉ tổng hợp từ dữ liệu đã đọc ở bước 1, không tự tạo thêm dữ liệu.
- Không bỏ qua báo cáo có dữ liệu thiếu.
- Nếu `Trưởng ca` hoặc `Nội dung` bị trống, giữ nguyên ký hiệu `[Thiếu dữ liệu]`.
- Không diễn giải lại nội dung báo cáo; giữ đúng nội dung gốc.
- Phải thể hiện rõ từng ngày có những phân xưởng nào báo cáo.
- Phải thể hiện rõ thời gian ca làm việc của từng báo cáo.
- Chưa tạo file Excel tổng hợp ở bước này; chỉ tạo bảng/tóm tắt kiểm tra nội dung tổng hợp.

## Định dạng kết quả mong muốn

### Cách 1: Bảng tổng hợp theo ngày

| Ngày | Phân xưởng | Thời gian ca | Trưởng ca | Nội dung công việc |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

### Cách 2: Nhóm theo từng ngày

```markdown
## Ngày yyyy-mm-dd

| Phân xưởng | Thời gian ca | Trưởng ca | Nội dung công việc |
|---|---|---|---|
| ... | ... | ... | ... |
```

Ưu tiên sử dụng Cách 2 nếu cần trình bày cho Lãnh đạo dễ đọc.

## Hiển thị thử nghiệm nội dung kết quả đạt được

Ví dụ kết quả tổng hợp theo ngày từ dữ liệu bước 1:

## Ngày 2026-01-07

| Phân xưởng | Thời gian ca | Trưởng ca | Nội dung công việc |
|---|---|---|---|
| Phân xưởng 1 | 08:00 - 16:00 | Nguyễn Văn A | Báo cáo 1 |
| Phân xưởng 2 | 08:00 - 16:00 | Đoàn Văn A | Báo cáo 1 |
| Phân xưởng 3 | 08:00 - 16:00 | Trần Văn A | Báo cáo 1 |

## Ngày 2026-02-07

| Phân xưởng | Thời gian ca | Trưởng ca | Nội dung công việc |
|---|---|---|---|
| Phân xưởng 1 | 08:00 - 16:00 | Nguyễn Văn B | Báo cáo 2 |
| Phân xưởng 2 | 08:00 - 16:00 | [Thiếu dữ liệu] | Báo cáo 2 |
| Phân xưởng 3 | 08:00 - 16:00 | Trần Văn B | Báo cáo 2 |

## Ngày 2026-05-07

| Phân xưởng | Thời gian ca | Trưởng ca | Nội dung công việc |
|---|---|---|---|
| Phân xưởng 1 | 08:00 - 16:00 | Nguyễn Văn E | Báo cáo 5 |
| Phân xưởng 2 | 08:00 - 16:00 | Đoàn Văn E | Báo cáo 5 |
| Phân xưởng 3 | 08:00 - 16:00 | [Thiếu dữ liệu] | [Thiếu dữ liệu] |
