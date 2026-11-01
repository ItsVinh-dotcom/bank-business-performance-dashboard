-- =====================================================================
-- 03_incentive_kpi.sql
-- Điểm KPI và quỹ incentive theo chi nhánh-tháng.
-- Bảng nguồn: fact_incentive, dim_branch, dim_month.
-- Công thức KPI và quỹ là giả định minh họa (xem 01_project_scope/kpi_dictionary).
-- =====================================================================

-- 3A. Bảng KPI theo chi nhánh-tháng kèm xếp hạng trong tháng
SELECT
    i.month,
    b.region,
    b.branch_name,
    i.balance_achievement,
    i.revenue_achievement,
    i.kpi_score,
    i.incentive_pool_mn,
    RANK() OVER (PARTITION BY i.month ORDER BY i.kpi_score DESC)  AS kpi_rank_in_month,
    CASE WHEN i.kpi_score >= 100 THEN 1 ELSE 0 END                AS flag_kpi_met
FROM fact_incentive i
JOIN dim_branch b ON b.branch_id = i.branch_id
ORDER BY i.month, kpi_rank_in_month;


-- 3B. Tỷ lệ tháng đạt KPI và tổng quỹ theo chi nhánh trong kỳ
SELECT
    b.branch_name,
    COUNT(*)                                                      AS months_in_period,
    SUM(CASE WHEN i.kpi_score >= 100 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS pct_months_kpi_met,
    AVG(i.kpi_score)                                              AS avg_kpi_score,
    SUM(i.incentive_pool_mn)                                      AS total_incentive_pool_mn
FROM fact_incentive i
JOIN dim_branch b ON b.branch_id = i.branch_id
GROUP BY b.branch_name
ORDER BY avg_kpi_score DESC;


-- 3C. Kiểm tra khớp giữa KPI và doanh thu: chi nhánh đạt KPI nhưng doanh thu thấp
--     Đây là câu hỏi B2 trong business_questions.md.
SELECT
    i.month,
    b.branch_name,
    i.kpi_score,
    i.revenue_achievement,
    CASE
        WHEN i.kpi_score >= 100 AND i.revenue_achievement < 1 THEN 'Đạt KPI nhưng doanh thu dưới kế hoạch'
        WHEN i.kpi_score < 100  AND i.revenue_achievement >= 1 THEN 'Doanh thu đạt nhưng KPI dưới ngưỡng'
        ELSE 'Nhất quán'
    END AS consistency_flag
FROM fact_incentive i
JOIN dim_branch b ON b.branch_id = i.branch_id
ORDER BY i.month, b.branch_name;
