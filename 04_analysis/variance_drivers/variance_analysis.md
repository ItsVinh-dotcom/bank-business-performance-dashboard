# Phân tích chênh lệch kế hoạch - thực tế (Q1/2025 đến Q2/2026)

Toàn bộ số liệu là giả lập. Nguồn tính: `03_sql/queries/01_plan_vs_actual.sql`. Bảng chi tiết: `variance_by_branch_segment.csv` trong cùng thư mục. Đơn vị doanh thu là triệu VND, dư nợ là tỷ VND.

## Tóm tắt

Ở cấp toàn công ty, dư nợ và doanh thu bám sát kế hoạch, mỗi quý chỉ lệch khoảng ±1%. Nếu chỉ nhìn tổng, dự án sẽ không thấy vấn đề gì. Vấn đề nằm ở cấp chi nhánh và phân khúc, và đây là chỗ cần phân tích sâu.

Điểm đáng chú ý nhất là CN Huế, phân khúc SME. Từ tháng 7/2025, dư nợ thực hiện chỉ đạt khoảng 84% đến 89% kế hoạch mỗi tháng và chưa phục hồi trong nửa đầu 2026. Tổng chênh lệch doanh thu của cặp này là khoảng -7.328 triệu VND (khoảng 7,3 tỷ đồng), đây là khoản thiếu hụt lớn nhất trong mọi cặp chi nhánh-phân khúc.

## Nguyên nhân chính của CN Huế SME

Tỷ lệ hoàn thành dư nợ (89,9%) và tỷ lệ hoàn thành doanh thu (89,7%) gần như bằng nhau, và tỷ lệ hoàn thành khách hàng mới cũng chỉ 90,0%. Điều này cho thấy chênh lệch chủ yếu đến từ khối lượng (ít khách hàng mới hơn, dẫn đến dư nợ thấp hơn), không phải từ giá hay mix sản phẩm. Hướng xử lý nên bắt đầu từ kênh tiếp cận khách hàng SME tại Huế, chứ không phải từ lãi suất hay danh mục sản phẩm.

Lưu ý: dữ liệu giả lập chỉ có một sản phẩm vay SME cho phân khúc này, nên không thể tách sâu hơn theo sản phẩm. Khi trình bày phỏng vấn, nên nói rõ giới hạn này.

## Các điểm khác cần lưu ý

CN Cần Thơ đạt KPI trong 9 trên 18 tháng, trong đó có 4 tháng vi phạm hạn mức cho vay không có tài sản bảo đảm (tháng 9 đến tháng 12/2025, tỷ lệ khoảng 33% so với hạn mức 30%). Hiệu suất kinh doanh của chi nhánh trong các tháng vi phạm không khác biệt so với các tháng còn lại (tỷ lệ hoàn thành doanh thu trung bình khoảng 100,2% so với 100,3%). Đây là một khoảng trống thiết kế: cơ chế KPI hiện tại không có điều kiện tuân thủ chính sách, nên chi nhánh vi phạm vẫn nhận đủ incentive.

CN Đà Nẵng, sản phẩm thẻ tín dụng, vượt kế hoạch mạnh trong Q4/2025: dư nợ đạt 120% đến 131% kế hoạch mỗi tháng từ tháng 10 đến tháng 12. Đây là một cơ hội cần kiểm chứng: nên xem đó là hiệu quả của chiến dịch hay là sự kiện một lần, và việc đặt kế hoạch năm sau có tính đến hay không.

CN Huế có điểm KPI trung bình 98,3 và chỉ đạt ngưỡng 100 trong 4 tháng, quỹ incentive thấp nhất (khoảng 224 triệu VND trong kỳ). Điều này phản ánh đúng tình trạng thiếu hụt, nhưng cũng cho thấy công thức KPI tuyến tính sẽ giảm mạnh thu nhập của chi nhánh khi chỉ thiếu vài điểm phần trăm.

## Lưu ý về chất lượng dữ liệu

Ba dòng thiếu doanh thu thực tế ảnh hưởng trực tiếp đến kết quả. Ví dụ, tỷ lệ hoàn thành doanh thu của CN Đà Nẵng, thẻ tín dụng, tháng 2/2025 chỉ còn 21% nếu không xử lý dòng thiếu, trong khi thực tế là khoảng 100%. Dòng trùng khóa làm tỷ lệ hoàn thành dư nợ của CN TP.HCM, Tiền gửi có kỳ hạn, tháng 4/2025 lệch so với bảng tổng hợp. Dashboard cần đưa kiểm tra chất lượng dữ liệu vào trang riêng, và báo cáo cần ghi rõ số dòng bị loại hoặc nội suy.

## Dự báo xu hướng

Thư mục `04_analysis/forecast/` có dự báo dư nợ từng chi nhánh-phân khúc cho tháng 7 đến tháng 12/2026, dùng hồi quy tuyến tính trên 6 tháng gần nhất. Đây chỉ là dự báo xu hướng, không phải dự báo theo kế hoạch, vì dữ liệu không có kế hoạch cho nửa cuối 2026. Không nên trình bày con số này như một cam kết và không nên so sánh với kế hoạch chưa tồn tại.

## Điểm có thể nói khi phỏng vấn

Ở cấp tổng công ty, số liệu có vẻ ổn. Khi chia nhỏ theo chi nhánh và phân khúc, có một cặp cần can thiệp rõ ràng (Huế SME). Có một chi nhánh đạt KPI nhưng vi phạm chính sách (Cần Thơ), cho thấy thiết kế KPI cần thêm điều kiện tuân thủ. Và có dữ liệu thiếu hoặc trùng có thể làm sai lệch báo cáo nếu không được kiểm tra trước.
