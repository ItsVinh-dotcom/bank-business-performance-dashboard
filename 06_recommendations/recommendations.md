# Khuyến nghị quản trị

Các khuyến nghị dưới đây dựa trên dữ liệu giả lập trong dự án, nên mang tính minh họa phương pháp. Khi áp dụng thực tế cần kiểm chứng lại với dữ liệu nội bộ.

## 1. Tái cấu trúc hoạt động bán SME tại CN Huế (ưu tiên cao)

Dư nợ SME tại CN Huế đạt khoảng 84% đến 89% kế hoạch liên tục từ tháng 7/2025, tương ứng thiếu khoảng 7,3 tỷ đồng doanh thu trong kỳ. Chênh lệch chủ yếu do số khách hàng mới thấp, không phải do giá hay mix. Đề xuất: đánh giá lại kênh tiếp cận SME của chi nhánh (đội ngũ, địa bàn, nguồn khách), đặt mục tiêu khách hàng mới theo tuần thay vì theo tháng để phát hiện sớm, và xem xét kế hoạch đã đặt có quá cao so với năng lực địa bàn hay không. Chỉ số theo dõi: tỷ lệ hoàn thành khách hàng mới SME hàng tuần, và dư nợ bình quân trên mỗi khách hàng.

## 2. Thêm điều kiện tuân thủ chính sách vào cơ chế KPI (ưu tiên cao)

CN Cần Thơ vi phạm hạn mức cho vay không tài sản bảo đảm trong 4 tháng cuối 2025 nhưng vẫn đạt KPI trong 9 tháng và nhận đủ quỹ incentive. Đề xuất: đưa tuân thủ thành điều kiện gate. Chi nhánh vi phạm hạn mức trong tháng sẽ không đủ điều kiện nhận incentive tháng đó, hoặc bị trừ một phần quỹ. Cách này không làm giảm động lực bán hàng nhưng buộc chi nhánh đặt tăng trưởng trong giới hạn rủi ro. Cần thống nhất với bộ phận quản trị rủi ro về ngưỡng và cách xử lý trường hợp vi phạm có lý do chính đáng.

## 3. Đánh giá lại cơ chế incentive theo ngưỡng tuyến tính (ưu tiên trung bình)

Công thức hiện tại (quỹ = (KPI - 90) × 1,5) khiến CN Huế, với KPI trung bình 98,3, chỉ nhận khoảng 224 triệu VND trong kỳ, trong khi CN Đà Nẵng nhận khoảng 292 triệu VND. Mức chênh này lớn so với mức chênh KPI thực tế. Đề xuất: cân nhắc quỹ theo bậc thang (ví dụ dưới 95% không có quỹ, 95% đến 100% có quỹ một phần, trên 100% tăng dần có trần). Cần mô phỏng ít nhất hai phương án trước khi đề xuất để so sánh chi phí và tác động đến hành vi.

## 4. Tách rõ kết quả nội tại và kết quả do chiến dịch (ưu tiên trung bình)

CN Đà Nẵng vượt kế hoạch 20% đến 31% đối với thẻ tín dụng trong Q4/2025. Nếu đây là chiến dịch, kế hoạch năm sau cần tính đến để tránh đặt mức nền quá cao, hoặc ngược lại đặt mức nền quá thấp và khiến chi nhánh nhận incentive trùng lặp. Đề xuất: ghi nhận cờ chiến dịch trong dữ liệu kế hoạch và thực tế, để báo cáo có thể tách đóng góp của chiến dịch khỏi tăng trưởng nền.

## 5. Đưa kiểm tra chất lượng dữ liệu thành bước bắt buộc trước khi báo cáo (ưu tiên cao)

Trong dữ liệu có ba dòng thiếu doanh thu và hai dòng trùng khóa. Dòng thiếu làm sai tỷ lệ hoàn thành doanh thu của cả một tháng-sản phẩm, và dòng trùng làm lệch dư nợ đã cộng. Đề xuất: chạy bộ kiểm tra `03_sql/data_quality_checks/dq_checks.sql` trước mỗi kỳ báo cáo, và chỉ phát hành báo cáo khi các kiểm tra DQ01, DQ02 và DQ04 bằng 0, hoặc có ghi chú về các dòng bị loại. Chi phí thực hiện thấp và tránh được việc phải đính chính số liệu với lãnh đạo.

## Thứ tự triển khai đề xuất

Trong 30 ngày tới nên làm khuyến nghị 5 (nền tảng dữ liệu) và khuyến nghị 1 (xử lý điểm nóng). Trong quý tiếp theo, mô phỏng khuyến nghị 2 và 3 với dữ liệu nội bộ, rồi trình duyệt cùng bộ phận rủi ro và nhân sự. Khuyến nghị 4 có thể làm song song khi lập kế hoạch năm sau.
