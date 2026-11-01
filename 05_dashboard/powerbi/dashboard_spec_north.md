# Đặc tả dashboard Power BI - miền Bắc

Semantic model: `BankKPINorth` (thư mục `05_dashboard\powerbi\BankKPINorth.SemanticModel`). Dữ liệu: `02_data\north_provinces`, 4 chi nhánh, tháng 1/2025 đến tháng 6/2026. Toàn bộ là dữ liệu mô phỏng.

## Cách mở và phạm vi dữ liệu

Mở `DashboardMienBac.pbip` trong Power BI Desktop. Báo cáo dùng model TMDL `BankKPINorth` và 7 CSV trong `02_data/north_provinces`. Mô hình có 8 quan hệ dạng sao, lọc một chiều từ dimension sang fact.

Dữ liệu mô phỏng theo tháng, từ 01/2025 đến 06/2026, gồm 4 chi nhánh, phân khúc và sản phẩm. Vì chưa có dữ liệu ngày, đường xu hướng biểu diễn theo tháng; không diễn giải thành biến động ngày/ngày.

Các truy vấn Power Query hiện trỏ tới thư mục dữ liệu trong workspace này. Khi chuyển project sang máy hoặc thư mục khác, cập nhật đường dẫn `File.Contents` trong các partition trước khi refresh.

## Measure có sẵn

Kế hoạch vs thực tế: Dư nợ kế hoạch, Dư nợ thực tế, Tỷ lệ HT dư nợ, Chênh lệch dư nợ, Doanh thu kế hoạch, Doanh thu thực tế, Tỷ lệ HT doanh thu, Chênh lệch doanh thu, KH mới kế hoạch, KH mới thực tế, Tỷ lệ HT khách hàng mới.

Chính sách và incentive: Số tháng vi phạm hạn mức không TSBĐ, Điểm KPI trung bình, Tỷ lệ tháng đạt KPI, Quỹ incentive, Quỹ có điều kiện tuân thủ.

Chất lượng dữ liệu: Số dòng thiếu doanh thu (mục tiêu 0), Số dòng trùng khóa (mục tiêu 0).

## Trang 1: Điều hành miền Bắc

Trang tóm tắt dành cho giám đốc vùng/chi nhánh. Bộ lọc năm và tỉnh hỗ trợ đọc nhanh theo phạm vi; chọn chi nhánh trong bảng để đi sâu. Năm mới nhất có dữ liệu là mặc định khi không lọc.

Năm thẻ đầu trang: dư nợ cuối kỳ, tăng trưởng dư nợ YTD, tăng trưởng dư nợ YoY, doanh thu YTD và tăng trưởng doanh thu YTD YoY. Hai biểu đồ đường tách riêng dư nợ kế hoạch/thực tế và doanh thu kế hoạch/thực tế theo tháng. Bảng chi nhánh tập trung vào tỷ lệ hoàn thành dư nợ cuối kỳ, tăng trưởng dư nợ từ đầu quý, tỷ lệ hoàn thành doanh thu YTD, tăng trưởng doanh thu YTD YoY, điểm KPI và số tháng vi phạm hạn mức.

Quy ước: dư nợ là số dư tại tháng báo cáo, so sánh với tháng 1, tháng đầu quý và cùng tháng năm trước; doanh thu là dòng phát sinh, so sánh lũy kế YTD với kế hoạch và cùng kỳ năm trước. Nếu chọn năm 2025, YoY sẽ trống do không có dữ liệu 2024.

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

## Giới hạn và hướng mở rộng

Dashboard hiện bao quát kế hoạch/thực tế theo chi nhánh, phân khúc, sản phẩm, KPI, incentive, tuân thủ và chất lượng dữ liệu. Dữ liệu hiện chưa có ngân sách chi tiết, số dư theo ngày, lợi nhuận theo khách hàng hay forecast ở cấp chi nhánh; không nên tự suy diễn các chỉ tiêu này. Nếu cần xu hướng ngày/ngày, cần bổ sung fact theo ngày có nhãn rõ là mô phỏng hoặc dùng dữ liệu công khai phù hợp.
