# Đặc tả dashboard Power BI - miền Bắc

Semantic model: `BankKPINorth` (thư mục `05_dashboard\powerbi\BankKPINorth.SemanticModel`). Dữ liệu: `02_data\north_provinces`, 4 chi nhánh, tháng 1/2025 đến tháng 6/2026. Toàn bộ là dữ liệu mô phỏng.

## Cách bắt đầu

1. Mở Power BI Desktop, tạo báo cáo trống, lưu thành `dashboard_mien_bac.pbix` trong `05_dashboard\powerbi`.
2. Get Data > Text/CSV, nạp lần lượt 7 file: fact_performance, fact_policy_check, fact_incentive (từ `02_data\north_provinces`), và dim_branch, dim_segment, dim_product, dim_month (cùng thư mục). Hoặc, nếu Power BI Desktop của bạn mở được thư mục TMDL, mở `BankKPINorth.SemanticModel` trực tiếp.
3. Kiểm tra Model view: có 8 quan hệ, tất cả là many-to-one, lọc một chiều từ dim sang fact.
4. Nạp measure từ thư mục hiển thị "1. Kế hoạch vs thực tế", "2. Chính sách và incentive", "4. Chất lượng dữ liệu".

## Measure có sẵn

Kế hoạch vs thực tế: Dư nợ kế hoạch, Dư nợ thực tế, Tỷ lệ HT dư nợ, Chênh lệch dư nợ, Doanh thu kế hoạch, Doanh thu thực tế, Tỷ lệ HT doanh thu, Chênh lệch doanh thu, KH mới kế hoạch, KH mới thực tế, Tỷ lệ HT khách hàng mới.

Chính sách và incentive: Số tháng vi phạm hạn mức không TSBĐ, Điểm KPI trung bình, Tỷ lệ tháng đạt KPI, Quỹ incentive, Quỹ có điều kiện tuân thủ.

Chất lượng dữ liệu: Số dòng thiếu doanh thu (mục tiêu 0), Số dòng trùng khóa (mục tiêu 0).

## Trang 1: Tổng quan

Hàng thẻ (Card) đầu trang: Tỷ lệ HT dư nợ, Tỷ lệ HT doanh thu, Điểm KPI trung bình, Quỹ incentive, Số tháng vi phạm hạn mức không TSBĐ.

Slicer: dim_month[quarter] (dạng danh sách), dim_branch[province].

Bảng (Table): dim_branch[branch_name], dim_branch[province], dim_branch[economic_profile], Tỷ lệ HT dư nợ, Tỷ lệ HT doanh thu, Chênh lệch doanh thu, Điểm KPI trung bình. Định dạng có điều kiện: tỷ lệ HT dưới 95% tô đỏ, từ 95% đến dưới 100% tô vàng, từ 100% trở lên tô xanh.

Biểu đồ đường (Line chart): trục x là dim_month[month], giá trị là Tỷ lệ HT dư nợ, legend là dim_branch[branch_name]. Kỳ vọng: CN Hải Phòng thấp hơn các chi nhánh khác từ đầu 2026 do SME.

## Trang 2: Kế hoạch vs thực tế

Biểu đồ cột nhóm (Clustered column): trục x là dim_branch[branch_name], giá trị là Doanh thu kế hoạch và Doanh thu thực tế.

Ma trận (Matrix): hàng là dim_branch[branch_name], cột là dim_segment[segment_name], giá trị là Chênh lệch doanh thu. Đặt định dạng có điều kiện đỏ cho giá trị âm. Kỳ vọng: ô Hải Phòng x SME là âm rõ rệt.

Bảng (Table): dim_segment[segment_name], dim_product[product_name], Tỷ lệ HT dư nợ, Tỷ lệ HT doanh thu, Chênh lệch doanh thu. Dùng để drill xuống sản phẩm.

Ghi chú: Tỷ lệ HT doanh thu tháng 2/2025 của CN Quảng Ninh có thể lệch do dòng thiếu doanh thu. Trang 4 giúp xác định dòng đó.

## Trang 3: Chính sách và incentive

Biểu đồ đường: trục x là dim_month[month], giá trị là trung bình fact_policy_check[unsecured_loan_ratio], legend là dim_branch[branch_name]. Thêm một đường tham chiếu cho hạn mức 30% (dùng fact_policy_check[unsecured_loan_limit]). Kỳ vọng: CN Bắc Ninh vượt hạn mức tháng 11 và 12/2025.

Ma trận (Matrix): hàng là dim_branch[branch_name], cột là dim_month[quarter], giá trị là Số tháng vi phạm hạn mức không TSBĐ. Định dạng đỏ khi lớn hơn 0.

Biểu đồ cột nhóm: trục x là dim_branch[branch_name], giá trị là Quỹ incentive và Quỹ có điều kiện tuân thủ. Khoảng chênh lệch giữa hai cột là phần tiền thưởng bị ảnh hưởng bởi vi phạm, dùng cho lập luận đề xuất.

Biểu đồ phân tán (Scatter): mỗi chi nhánh là một điểm. Trục x là Tỷ lệ HT doanh thu, trục y là Điểm KPI trung bình, chi tiết là dim_branch[branch_name]. Dùng để thảo luận nhóm đạt KPI nhưng vi phạm chính sách.

## Trang 4: Chất lượng dữ liệu

Hàng thẻ: Số dòng thiếu doanh thu, Số dòng trùng khóa. Kỳ vọng: 2 và 1.

Bảng chi tiết (Table): lấy từ fact_performance, bộ lọc `actual_revenue_mn` là trống (blank) để liệt kê dòng thiếu. Thêm month, branch_id, segment_id, product_id.

Ghi chú cuối trang: số dòng bị loại khỏi các tỷ lệ (dòng thiếu doanh thu) và số dòng trùng vẫn được tính (dòng trùng). Đây là quy tắc đã ghi trong `08_documentation`.

## Kiểm tra trước khi trình bày

Tỷ lệ HT dư nợ toàn công ty xấp xỉ 100,6%. Điểm KPI trung bình xấp xỉ 100. Số tháng vi phạm không TSBĐ bằng 2 (CN Bắc Ninh tháng 11 và 12/2025). Số dòng thiếu doanh thu bằng 2. Số dòng trùng khóa bằng 1. Nếu con số lệch, kiểm tra lại bộ lọc và quan hệ trước khi tin số.
