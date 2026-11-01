# Đặc tả dashboard Power BI

Semantic model `BankKPI` đã được xuất ra `BankKPI.SemanticModel\definition` trong thư mục này (định dạng TMDL). Model gồm 7 bảng (3 bảng fact, 4 bảng dim), 8 quan hệ dạng sao, và 17 measure chia theo thư mục hiển thị.

## Cách mở

Mở Power BI Desktop, chọn File > Open, rồi mở thư mục `BankKPI.SemanticModel` nếu bản Power BI của bạn hỗ trợ TMDL. Nếu không, tạo báo cáo trống, chọn Get Data > Text/CSV từng file trong `02_data/raw_simulated` và `02_data/reference`, rồi tạo quan hệ theo bảng sau. Các đường dẫn trong mã M trỏ đến `D:\03_career\Project\bank-business-performance-dashboard\02_data\...`; nếu chuyển thư mục thì cần sửa lại.

Quan hệ: `fact_performance` nối với `dim_branch`, `dim_segment`, `dim_product` và `dim_month`. `fact_policy_check` và `fact_incentive` nối với `dim_branch` và `dim_month`. Tất cả quan hệ là many-to-one, lọc một chiều từ dim sang fact.

## Measure đã có

Thư mục "1. Kế hoạch vs thực tế": Dư nợ kế hoạch, Dư nợ thực tế, Tỷ lệ HT dư nợ, Chênh lệch dư nợ, Doanh thu kế hoạch, Doanh thu thực tế, Tỷ lệ HT doanh thu, Chênh lệch doanh thu, KH mới kế hoạch, KH mới thực tế, Tỷ lệ HT khách hàng mới.

Thư mục "2. Chính sách và incentive": Số tháng vi phạm hạn mức không TSBĐ, Số tháng vi phạm trần hoa hồng, Điểm KPI trung bình, Tỷ lệ tháng đạt KPI, Quỹ incentive.

Thư mục "4. Chất lượng dữ liệu": Số dòng thiếu doanh thu (DQ01).

## Trang 1: Tổng quan

Bốn thẻ KPI đầu trang: Tỷ lệ HT dư nợ, Tỷ lệ HT doanh thu, Tỷ lệ HT khách hàng mới, Điểm KPI trung bình. Đặt cạnh mỗi thẻ là chênh lệch so với kế hoạch, tô màu theo ngưỡng 100%, 95%. Biểu đồ đường tỷ lệ HT dư nợ theo tháng, có thêm đường 100%. Bảng chi nhánh với tỷ lệ HT dư nợ, tỷ lệ HT doanh thu và điểm KPI, có thanh dữ liệu (data bar) cho chênh lệch doanh thu. Bộ lọc: năm, quý, vùng.

## Trang 2: Kế hoạch vs thực tế

Biểu đồ cột nhóm: doanh thu kế hoạch và thực tế theo chi nhánh. Ma trận chi nhánh x phân khúc, giá trị là Chênh lệch doanh thu, tô màu đỏ cho giá trị âm. Biểu đồ thác nước (waterfall) giải thích chênh lệch doanh thu toàn công ty theo chi nhánh. Đây là trang để trả lời câu hỏi nguyên nhân, nên đặt CN Huế SME làm ví dụ mặc định khi trình bày: dùng bộ lọc chi nhánh và phân khúc để drill-down. Ghi chú: tháng 2/2025 của CN Đà Nẵng (thẻ tín dụng) có tỷ lệ doanh thu bất thường do dòng thiếu dữ liệu, nên cần gắn cờ DQ01 trên trang này.

## Trang 3: Chính sách và incentive

Ma trận tháng x chi nhánh, ô là cờ vi phạm hạn mức không TSBĐ, tô đỏ khi vi phạm. Biểu đồ cột: số tháng vi phạm theo chi nhánh. Bảng KPI và quỹ incentive theo chi nhánh. Một biểu đồ phân tán (scatter) với trục x là tỷ lệ HT doanh thu, trục y là điểm KPI, mỗi chi nhánh là một điểm, để thấy nhóm đạt KPI nhưng vi phạm chính sách (CN Cần Thơ là ví dụ). Nên thêm tooltip hiển thị số tháng vi phạm.

## Trang 4: Chất lượng dữ liệu

Thẻ Số dòng thiếu doanh thu (mục tiêu 0). Bảng liệt kê dòng thiếu và dòng trùng, lấy từ `03_sql/data_quality_checks/dq_checks.sql`. Thẻ đối chiếu tỷ lệ HT dư nợ giữa fact_performance và fact_incentive (DQ03). Ghi chú cuối trang: số dòng bị loại và cách xử lý.

## Lưu ý khi trình bày

Số liệu là giả lập, nên ghi rõ trên mỗi trang. Đừng trình bày con số incentive như cơ chế thật; đó là đề xuất minh họa.
