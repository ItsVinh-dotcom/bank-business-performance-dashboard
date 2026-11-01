# Từ điển KPI - Bank Business Performance & KPI Dashboard

Tài liệu này định nghĩa các chỉ tiêu dùng chung trong dự án. Mọi số liệu trong dự án là giả lập (xem `02_data/scripts/generate_simulated_data.py`).

Quy ước chung: tiền tính theo tỷ VND (bn) cho dư nợ/huy động và triệu VND (mn) cho doanh thu và incentive. Kỳ báo cáo là tháng. Chiều phân tích gồm thời gian, vùng/miền, chi nhánh, phân khúc khách hàng và nhóm sản phẩm.

## 1. Nhóm chỉ tiêu kế hoạch và thực hiện

| Mã | Tên chỉ tiêu | Công thức | Nguồn | Ghi chú |
|---|---|---|---|---|
| K01 | Dư nợ/huy động kế hoạch | `plan_balance_bn` | fact_performance | Kế hoạch năm chia theo tháng |
| K02 | Dư nợ/huy động thực tế | `actual_balance_bn` | fact_performance | Số dư cuối tháng |
| K03 | Tỷ lệ hoàn thành dư nợ (BAL_ACH) | `SUM(actual_balance_bn) / SUM(plan_balance_bn)` | fact_performance | Ngưỡng: ≥ 100% đạt, 95% đến dưới 100% cảnh báo, dưới 95% đỏ |
| K04 | Doanh thu kế hoạch | `plan_revenue_mn` | fact_performance | Thu nhập lãi thuần và phí ước tính |
| K05 | Doanh thu thực tế | `actual_revenue_mn` | fact_performance | Có thể thiếu giá trị, xem kiểm tra DQ |
| K06 | Tỷ lệ hoàn thành doanh thu (REV_ACH) | `SUM(actual_revenue_mn) / SUM(plan_revenue_mn)` | fact_performance | Cùng ngưỡng với K03 |
| K07 | Khách hàng mới kế hoạch/thực tế | `plan_new_customers`, `actual_new_customers` | fact_performance | Đơn vị: khách hàng |
| K08 | Tỷ lệ hoàn thành khách hàng mới (NEW_ACH) | `SUM(actual_new_customers) / SUM(plan_new_customers)` | fact_performance | Dùng để giải thích driver |
| K09 | Chênh lệch dư nợ (VAR_BAL) | `actual_balance_bn - plan_balance_bn` | tính toán | Dương là vượt, âm là thiếu |
| K10 | Chênh lệch doanh thu (VAR_REV) | `actual_revenue_mn - plan_revenue_mn` | tính toán | Dùng để xếp hạng nguyên nhân |

## 2. Nhóm chỉ tiêu KPI và incentive

| Mã | Tên chỉ tiêu | Công thức | Nguồn | Ghi chú |
|---|---|---|---|---|
| K11 | Điểm KPI chi nhánh | `100 × (0,6 × BAL_ACH + 0,4 × REV_ACH)` | fact_incentive | Trọng số là giả định, có thể điều chỉnh |
| K12 | Quỹ incentive chi nhánh | `MAX(KPI - 90, 0) × 1,5` (triệu VND) | fact_incentive | Công thức giả định để minh họa cơ chế |
| K13 | Tỷ lệ đạt KPI | Số tháng có KPI ≥ 100 / tổng số tháng | tính toán | Dùng cho xếp hạng quý |

Lưu ý khi trình bày: K11 và K12 là cơ chế minh họa, không phải cơ chế của bất kỳ tổ chức nào. Khi phỏng vấn, nên nói rõ đây là đề xuất thiết kế và có thể điều chỉnh theo khẩu vị rủi ro và chiến lược kinh doanh.

## 3. Nhóm chỉ tiêu tuân thủ chính sách tài chính kinh doanh

| Mã | Tên chỉ tiêu | Công thức | Nguồn | Ghi chú |
|---|---|---|---|---|
| K14 | Tỷ lệ cho vay không TSBĐ | `unsecured_loan_ratio` | fact_policy_check | Giả định hạn mức tối đa 30% |
| K15 | Vi phạm hạn mức không TSBĐ | `unsecured_loan_ratio > unsecured_loan_limit` | tính toán | Cờ 1/0 theo tháng và chi nhánh |
| K16 | Tỷ lệ hoa hồng trên doanh thu mới | `commission_ratio` | fact_policy_check | Giả định trần 3,5% |
| K17 | Vi phạm trần hoa hồng | `commission_ratio > commission_cap` | tính toán | Cờ 1/0 theo tháng và chi nhánh |

## 4. Nhóm chỉ tiêu chất lượng dữ liệu

| Mã | Kiểm tra | Điều kiện lỗi |
|---|---|---|
| DQ01 | Thiếu giá trị thực tế | `actual_revenue_mn` rỗng |
| DQ02 | Trùng khóa | Trùng `(month, branch_id, segment_id, product_id)` |
| DQ03 | Đối chiếu tổng hợp | Tổng dư nợ thực tế theo chi nhánh-tháng trong fact_incentive không khớp với fact_performance |
| DQ04 | Khóa tham chiếu | `branch_id`, `segment_id`, `product_id` không có trong bảng dim |

Chi tiết truy vấn nằm ở `03_sql/data_quality_checks/`.

## 5. Chiều phân tích

Thời gian: tháng, quý, năm. Địa lý: vùng/miền, chi nhánh. Khách hàng: cá nhân, SME, doanh nghiệp. Sản phẩm: theo `product_group` (Huy động, Tín dụng, Thẻ và thanh toán).
