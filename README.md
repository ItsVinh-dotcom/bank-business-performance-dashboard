# Bank Business Performance & KPI Dashboard

Project portfolio mô phỏng quy trình theo dõi KPI và hiệu quả kinh doanh theo
thời gian, vùng, chi nhánh và sản phẩm. Trọng tâm là định nghĩa chỉ tiêu,
so sánh kế hoạch với thực tế, phân tích chênh lệch và hỗ trợ đề xuất hành động
quản trị.

## Cấu trúc

- `01_project_scope`: câu hỏi nghiệp vụ và từ điển KPI.
- `02_data`: dữ liệu giả lập, dữ liệu đã xử lý và dữ liệu tham chiếu.
- `03_sql`: truy vấn và kiểm tra chất lượng dữ liệu.
- `04_analysis`: phân tích kế hoạch - thực tế, nguyên nhân chênh lệch và dự báo.
- `05_dashboard`: dashboard Power BI và file xuất.
- `06_recommendations`: nhận định và khuyến nghị.
- `07_presentation`: tài liệu trình bày project.
- `08_documentation`: tài liệu kỹ thuật và giả định.

## Dữ liệu và quyền riêng tư

Đây là project thực hành độc lập. Chỉ sử dụng dữ liệu giả lập hoặc dữ liệu công
khai phù hợp; không đưa dữ liệu khách hàng, dữ liệu nội bộ ngân hàng, thông tin
đăng nhập hoặc bí mật lên repository.

## Tự động push sau mỗi commit

Repository này dùng Git hook tại `.githooks/post-commit` để push commit hiện
tại lên `origin` sau khi commit hoàn tất. Hook chỉ được kích hoạt trong bản
clone đã cấu hình `core.hooksPath`; xem README của repository để biết cách bật
trên máy khác.
