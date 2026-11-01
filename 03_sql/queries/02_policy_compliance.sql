-- =====================================================================
-- 02_policy_compliance.sql
-- Kiểm soát tuân thủ chính sách tài chính kinh doanh theo chi nhánh-tháng.
-- Bảng nguồn: fact_policy_check, dim_branch, dim_month.
-- =====================================================================

-- 2A. Cờ vi phạm theo từng chi nhánh-tháng
SELECT
    pc.month,
    b.region,
    b.branch_name,
    pc.unsecured_loan_ratio,
    pc.unsecured_loan_limit,
    CASE WHEN pc.unsecured_loan_ratio > pc.unsecured_loan_limit THEN 1 ELSE 0 END AS flag_unsecured_breach,
    pc.commission_ratio,
    pc.commission_cap,
    CASE WHEN pc.commission_ratio > pc.commission_cap THEN 1 ELSE 0 END           AS flag_commission_breach,
    CASE WHEN pc.unsecured_loan_ratio > pc.unsecured_loan_limit
           OR pc.commission_ratio > pc.commission_cap THEN 1 ELSE 0 END          AS flag_any_breach
FROM fact_policy_check pc
JOIN dim_branch b ON b.branch_id = pc.branch_id
ORDER BY pc.month, b.branch_name;


-- 2B. Số tháng vi phạm theo chi nhánh trong kỳ (cho bảng tóm tắt và cảnh báo)
SELECT
    b.branch_name,
    SUM(CASE WHEN pc.unsecured_loan_ratio > pc.unsecured_loan_limit THEN 1 ELSE 0 END) AS months_unsecured_breach,
    SUM(CASE WHEN pc.commission_ratio > pc.commission_cap THEN 1 ELSE 0 END)           AS months_commission_breach,
    MAX(pc.unsecured_loan_ratio)                                                       AS max_unsecured_ratio,
    MAX(pc.commission_ratio)                                                           AS max_commission_ratio
FROM fact_policy_check pc
JOIN dim_branch b ON b.branch_id = pc.branch_id
GROUP BY b.branch_name
ORDER BY months_unsecured_breach DESC, months_commission_breach DESC;


-- 2C. Liên kết vi phạm với kết quả kinh doanh cùng tháng
--     Trả lời câu hỏi: chi nhánh vi phạm chính sách có đạt kế hoạch không?
SELECT
    pc.month,
    b.branch_name,
    CASE WHEN pc.unsecured_loan_ratio > pc.unsecured_loan_limit THEN 1 ELSE 0 END AS flag_unsecured_breach,
    SUM(p.actual_balance_bn) / NULLIF(SUM(p.plan_balance_bn), 0)                  AS bal_ach,
    SUM(p.actual_revenue_mn) / NULLIF(SUM(p.plan_revenue_mn), 0)                  AS rev_ach
FROM fact_policy_check pc
JOIN dim_branch b ON b.branch_id = pc.branch_id
JOIN fact_performance p ON p.month = pc.month AND p.branch_id = pc.branch_id
GROUP BY pc.month, b.branch_name,
         CASE WHEN pc.unsecured_loan_ratio > pc.unsecured_loan_limit THEN 1 ELSE 0 END
ORDER BY pc.month, b.branch_name;
