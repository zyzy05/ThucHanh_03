# Giải thích mã nguồn CoAP_Lab

## Kiến trúc chung
CoAP là giao thức ứng dụng nhẹ dành cho IoT. Trong bộ bài này, `aiocoap` cung cấp CoAP Server/Client; các tài nguyên được định danh bằng URI và trao đổi payload dạng văn bản hoặc JSON. Mặc định CoAP dùng UDP cổng 5683.

## Bài 1 — GET và POST
- `coap_server_bai1.py`: tạo tài nguyên `/iot/lab/message`.
  - `render_get()`: ghi log yêu cầu và trả lời thông điệp chào mừng với mã `2.05 Content`.
  - `render_post()`: đọc payload Client gửi, in payload và thời gian nhận, sau đó trả lời `2.04 Changed`.
- `coap_client_bai1.py`: gửi GET trước, in phản hồi; tiếp theo gửi POST chứa mã sinh viên, họ tên và lời chào.
- GET dùng để đọc tài nguyên; POST gửi dữ liệu tới tài nguyên để Server xử lý.

## Bài 2 — Dữ liệu cảm biến
- `sensor_server_bai2.py`: giữ dữ liệu cảm biến hiện tại trong tài nguyên. Một tác vụ nền cập nhật nhiệt độ và độ ẩm ngẫu nhiên mỗi 3 giây. GET trả về JSON với `device_id`, `temperature`, `humidity`.
- `monitor_client_bai2.py`: gửi GET mỗi 3 giây, giải mã JSON, hiển thị thời gian nhận và kiểm tra:
  - Nhiệt độ > 35°C: `CANH BAO: Nhiet do cao`.
  - Độ ẩm < 40%: `CANH BAO: Do am thap`.
- Đây là mô hình polling theo đúng yêu cầu Bài 2. Client có xử lý lỗi giao tiếp để tiếp tục thử ở chu kỳ sau.

## Bài 3 — GET/PUT/Observe
- `light_server_bai3.py`: tài nguyên Observable có trạng thái ban đầu `OFF`.
  - GET trả JSON trạng thái.
  - PUT nhận JSON `{ "device_id": "light01", "command": "ON" }` hoặc `OFF`.
  - Khi trạng thái thực sự thay đổi, Server cập nhật tài nguyên và gọi cơ chế thông báo Observe.
- `light_controller_bai3.py`: nhận lệnh từ bàn phím. `ON`/`OFF` dùng PUT, `STATUS` dùng GET, `EXIT` thoát.
- `light_monitor_bai3.py`: đăng ký Observe và in trạng thái ban đầu cũng như các cập nhật do Server gửi. Client không dùng vòng lặp GET định kỳ.
- PUT cập nhật trạng thái tài nguyên; Observe cho phép Server gửi thông báo khi tài nguyên thay đổi.

## Thứ tự chạy
1. Khởi động Server của bài tương ứng.
2. Khởi động Monitoring Client (Bài 3 nếu có).
3. Khởi động Controller/Client.
4. Thử lệnh và đối chiếu log ở từng terminal.

## Tùy chỉnh trước khi nộp
- Bài 1: sửa `STUDENT_ID` và `STUDENT_NAME`.
- README: bổ sung thông tin sinh viên/nhóm.
- Chụp ảnh terminal hoặc lưu log chạy thực tế để làm minh chứng. Ví dụ đầu ra trong tài liệu chỉ là định dạng tham khảo, không phải log thực thi đã chụp.
