# Giả định, hạn chế và ghi chú kỹ thuật

## 1. Tính chất dữ liệu

Toàn bộ dữ liệu trong dự án là giả lập, được sinh bằng `02_data/scripts/generate_simulated_data.py` với seed cố định (20260601), nên có thể tái lập đúng từng số. Không có dữ liệu khách hàng, dữ liệu nội bộ hoặc thông tin của bất kỳ tổ chức nào.

Các tên chi nhánh, vùng và sản phẩm là tên mô phỏng và không đại diện cho cơ cấu thực của bất kỳ ngân hàng nào. Phạm vi thời gian là tháng 1/2025 đến tháng 6/2026, 6 chi nhánh, 3 phân khúc, 5 nhóm sản phẩm.

## 2. Giả định nghiệp vụ

Hạn mức cho vay không tài sản bảo đảm được giả định ở mức 30% dư nợ tín dụng của chi nhánh. Trần tỷ lệ hoa hồng trên doanh thu mới được giả định ở mức 3,5%. Cả hai con số này đều là giả định minh họa, không phải số liệu chính sách thật.

Trọng số KPI (60% dư nợ, 40% doanh thu) và công thức quỹ incentive (KPI trên 90, nhân 1,5) là đề xuất thiết kế để minh họa cơ chế, không phải cơ chế đang áp dụng ở đâu.

Kế hoạch được đặt theo xu hướng tăng trưởng khoảng 1,2% mỗi tháng và mùa vụ (Tết và cuối năm). Thực tế được sinh từ kế hoạch với nhiễu ngẫu nhiên khoảng 3% đến 5%, cộng các điểm bất thường có chủ đích (CN Huế SME từ tháng 7/2025, CN Đà Nẵng thẻ tín dụng Q4/2025, CN Cần Thơ vi phạm hạn mức tháng 9 đến tháng 12/2025).

Dữ liệu không có kế hoạch cho nửa cuối 2026, nên dự báo trong `04_analysis/forecast/` chỉ là ngoại suy xu hướng từ 6 tháng gần nhất.

## 3. Lỗi dữ liệu có chủ đích

Có ba dòng thiếu `actual_revenue_mn` (tại các vị trí dòng 101, 487 và 1100 trong bảng sinh ra) và hai dòng trùng khóa `(month, branch_id, segment_id, product_id)`. Các lỗi này được cài để kiểm tra quy trình DQ, không phải lỗi của quá trình sinh dữ liệu. Khi tái lập, số dòng của `fact_performance.csv` là 1.190 (1.188 dòng gốc cộng 2 dòng trùng).

Bảng `fact_incentive` được tính trên dữ liệu sạch trước khi cài lỗi, nên đối chiếu DQ03 có thể phát hiện chênh lệch do dòng trùng.

## 4. Quy ước kỹ thuật

Số tiền dư nợ và huy động tính bằng tỷ VND (bn), doanh thu và incentive tính bằng triệu VND (mn). Tỷ lệ hoàn thành tổng hợp luôn tính bằng tổng tử số chia tổng mẫu số, không lấy trung bình của các tỷ lệ.

Các truy vấn SQL viết theo ANSI SQL. Đã kiểm tra chạy được trên SQLite với dữ liệu CSV. Khi chuyển sang PostgreSQL hoặc SQL Server cần kiểm tra lại cú pháp hàm `NULLIF` và `RANK() OVER`.

Mã phân khúc, chi nhánh và sản phẩm nằm trong thư mục `02_data/reference`. Mọi bảng fact đều khóa theo tháng dạng `YYYY-MM`.

## 5. Hạn chế đã biết

Dữ liệu không có chiều thời gian theo ngày, nên không phân tích được xu hướng trong tháng. Không có dữ liệu chi phí vốn, rủi ro tín dụng (nợ xấu) hay lợi nhuận sau rủi ro, nên các chỉ tiêu tài chính chỉ dừng ở dư nợ và doanh thu. Phân khúc SME chỉ có một sản phẩm vay, nên không thể tách sâu theo sản phẩm trong phân khúc đó.

Các kết luận trong `04_analysis` và `06_recommendations` đúng với dữ liệu này, nhưng không nên được hiểu là kết luận về bất kỳ ngân hàng cụ thể nào.
