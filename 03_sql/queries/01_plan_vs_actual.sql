-- =====================================================================
-- 01_plan_vs_actual.sql
-- Kế hoạch vs thực tế theo tháng, chi nhánh, phân khúc, sản phẩm.
-- Bảng nguồn: fact_performance (đã đổi tên/import vào DB dự án).
-- Ghi chú: viết theo ANSI SQL, đã kiểm tra logic trên SQLite và PostgreSQL.
-- Lưu ý: dữ liệu có 2 dòng trùng khóa và 3 dòng thiếu actual_revenue_mn.
--        Xem 03_sql/data_quality_checks/dq_checks.sql trước khi dùng số liệu.
-- =====================================================================

-- 1A. Chi tiết dòng: tỷ lệ hoàn thành theo từng dòng (dùng để drill-down)
SELECT
    p.month,
    b.region,
    b.branch_name,
    s.segment_name,
    pr.product_group,
    pr.product_name,
    p.plan_balance_bn,
    p.actual_balance_bn,
    p.actual_balance_bn - p.plan_balance_bn                       AS var_balance_bn,
    CASE WHEN p.plan_balance_bn = 0 THEN NULL
         ELSE p.actual_balance_bn / p.plan_balance_bn END          AS bal_ach,
    p.plan_revenue_mn,
    p.actual_revenue_mn,
    p.actual_revenue_mn - p.plan_revenue_mn                       AS var_revenue_mn,
    CASE WHEN p.plan_revenue_mn = 0 THEN NULL
         ELSE p.actual_revenue_mn / p.plan_revenue_mn END          AS rev_ach
FROM fact_performance p
JOIN dim_branch  b  ON b.branch_id  = p.branch_id
JOIN dim_segment s  ON s.segment_id = p.segment_id
JOIN dim_product pr ON pr.product_id = p.product_id;


-- 1B. Tổng hợp theo chi nhánh và tháng (cho trang plan vs actual)
--     Dùng SUM trên cả hai vế để tỷ lệ hoàn thành là tỷ lệ có trọng số, không phải trung bình tỷ lệ.
SELECT
    p.month,
    b.region,
    b.branch_name,
    SUM(p.plan_balance_bn)                                        AS plan_balance_bn,
    SUM(p.actual_balance_bn)                                      AS actual_balance_bn,
    SUM(p.actual_balance_bn) / NULLIF(SUM(p.plan_balance_bn), 0)  AS bal_ach,
    SUM(p.plan_revenue_mn)                                        AS plan_revenue_mn,
    SUM(p.actual_revenue_mn)                                      AS actual_revenue_mn,
    SUM(p.actual_revenue_mn) / NULLIF(SUM(p.plan_revenue_mn), 0)  AS rev_ach,
    CASE
        WHEN SUM(p.actual_balance_bn) / NULLIF(SUM(p.plan_balance_bn), 0) >= 1    THEN 'Đạt'
        WHEN SUM(p.actual_balance_bn) / NULLIF(SUM(p.plan_balance_bn), 0) >= 0.95 THEN 'Cảnh báo'
        ELSE 'Đỏ'
    END                                                           AS bal_status
FROM fact_performance p
JOIN dim_branch b ON b.branch_id = p.branch_id
GROUP BY p.month, b.region, b.branch_name
ORDER BY p.month, b.region, b.branch_name;


-- 1C. Tổng hợp theo phân khúc và quý (cho báo cáo quý)
SELECT
    m.quarter,
    s.segment_name,
    SUM(p.plan_balance_bn)                                        AS plan_balance_bn,
    SUM(p.actual_balance_bn)                                      AS actual_balance_bn,
    SUM(p.actual_balance_bn) / NULLIF(SUM(p.plan_balance_bn), 0)  AS bal_ach,
    SUM(p.actual_revenue_mn) / NULLIF(SUM(p.plan_revenue_mn), 0)  AS rev_ach
FROM fact_performance p
JOIN dim_segment s ON s.segment_id = p.segment_id
JOIN dim_month   m ON m.month      = p.month
GROUP BY m.quarter, s.segment_name
ORDER BY m.quarter, s.segment_name;


-- 1D. Chênh lệch doanh thu được giải thích theo khách hàng mới và dư nợ (dùng cho phân tích driver)
--     Tỷ lệ hoàn thành khách hàng mới và dư nợ theo chi nhánh-sản phẩm-tháng.
SELECT
    p.month,
    b.branch_name,
    pr.product_name,
    SUM(p.plan_new_customers)                                     AS plan_new_customers,
    SUM(p.actual_new_customers)                                   AS actual_new_customers,
    SUM(p.actual_new_customers) / NULLIF(SUM(p.plan_new_customers), 0) AS new_ach,
    SUM(p.actual_balance_bn) / NULLIF(SUM(p.plan_balance_bn), 0)  AS bal_ach,
    SUM(p.actual_revenue_mn) - SUM(p.plan_revenue_mn)             AS var_revenue_mn
FROM fact_performance p
JOIN dim_branch  b  ON b.branch_id  = p.branch_id
JOIN dim_product pr ON pr.product_id = p.product_id
GROUP BY p.month, b.branch_name, pr.product_name;
