-- =====================================================================
-- dq_checks.sql
-- Kiểm tra chất lượng dữ liệu. Mỗi khối trả về số dòng lỗi; 0 là đạt.
-- Mã kiểm tra khớp với 01_project_scope/kpi_dictionary (mục 4).
-- =====================================================================

-- DQ01: Thiếu giá trị thực tế doanh thu
SELECT 'DQ01_missing_actual_revenue' AS check_name, COUNT(*) AS error_rows
FROM fact_performance
WHERE actual_revenue_mn IS NULL OR actual_revenue_mn = '';

-- DQ01 chi tiết: liệt kê các dòng lỗi để xử lý
SELECT month, branch_id, segment_id, product_id, actual_revenue_mn
FROM fact_performance
WHERE actual_revenue_mn IS NULL OR actual_revenue_mn = '';


-- DQ02: Trùng khóa (month, branch_id, segment_id, product_id)
SELECT 'DQ02_duplicate_key' AS check_name, COUNT(*) AS error_rows
FROM (
    SELECT month, branch_id, segment_id, product_id
    FROM fact_performance
    GROUP BY month, branch_id, segment_id, product_id
    HAVING COUNT(*) > 1
) d;

-- DQ02 chi tiết
SELECT month, branch_id, segment_id, product_id, COUNT(*) AS n_rows
FROM fact_performance
GROUP BY month, branch_id, segment_id, product_id
HAVING COUNT(*) > 1;


-- DQ03: Đối chiếu tổng hợp. Tỷ lệ hoàn thành dư nợ tính lại từ fact_performance
--       phải khớp với balance_achievement trong fact_incentive (tính trên dữ liệu sạch).
--       Ngưỡng lệch: 0,5 điểm phần trăm. Lệch vượt ngưỡng cho thấy dòng trùng hoặc thiếu
--       đã làm sai số liệu tổng hợp.
WITH perf AS (
    SELECT month, branch_id,
           SUM(actual_balance_bn) / NULLIF(SUM(plan_balance_bn), 0) AS bal_ach_recalc
    FROM fact_performance
    GROUP BY month, branch_id
)
SELECT
    'DQ03_reconcile_balance_ach' AS check_name,
    COUNT(*)                     AS error_rows
FROM perf p
JOIN fact_incentive i ON i.month = p.month AND i.branch_id = p.branch_id
WHERE ABS(p.bal_ach_recalc - i.balance_achievement) > 0.005;


-- DQ04: Khóa tham chiếu không tồn tại trong bảng dim
SELECT 'DQ04_orphan_branch'  AS check_name, COUNT(*) AS error_rows
FROM fact_performance p LEFT JOIN dim_branch b ON b.branch_id = p.branch_id
WHERE b.branch_id IS NULL
UNION ALL
SELECT 'DQ04_orphan_segment', COUNT(*)
FROM fact_performance p LEFT JOIN dim_segment s ON s.segment_id = p.segment_id
WHERE s.segment_id IS NULL
UNION ALL
SELECT 'DQ04_orphan_product', COUNT(*)
FROM fact_performance p LEFT JOIN dim_product pr ON pr.product_id = p.product_id
WHERE pr.product_id IS NULL;
