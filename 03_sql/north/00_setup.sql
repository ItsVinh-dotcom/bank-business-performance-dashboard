-- 00_setup.sql — Tạo bảng schema north và nạp CSV miền Bắc
-- Chạy trong PSQL Tool:
--   \cd 'D:/03_career/Project/bank-business-performance-dashboard'
--   \i 03_sql/north/00_setup.sql
-- Đáp số: fact_performance 505, fact_incentive 72, fact_policy_check 72,
--         dim_branch 4, dim_month 18, dim_product 5, dim_segment 3
--
-- 4 bảng có [MẪU] là ví dụ đã viết sẵn. 3 bảng có [BẠN VIẾT] làm theo bảng mẫu tương ứng.

-- ===== 1. Xóa bảng cũ (để chạy lại nhiều lần) =====
-- Xóa bảng fact TRƯỚC, bảng dim SAU.
-- Lý do: bảng fact có khóa ngoại trỏ vào dim. Nếu xóa dim trước, Postgres báo lỗi
-- vì vẫn còn bảng fact đang tham chiếu tới nó.
-- IF EXISTS: lần chạy đầu tiên chưa có bảng thì bỏ qua, không báo lỗi.
DROP TABLE IF EXISTS north.fact_performance;
DROP TABLE IF EXISTS north.fact_incentive;
DROP TABLE IF EXISTS north.fact_policy_check;
DROP TABLE IF EXISTS north.dim_branch;
DROP TABLE IF EXISTS north.dim_month;
DROP TABLE IF EXISTS north.dim_product;
DROP TABLE IF EXISTS north.dim_segment;

-- ===== dim_segment [MẪU 1: bảng dim đơn giản nhất] =====
-- Cột trong CSV: segment_id,segment_name
CREATE TABLE north.dim_segment (
    segment_id   VARCHAR(10) PRIMARY KEY,   -- mã ngắn (CN, SME, DN). PRIMARY KEY = không trùng, không rỗng
    segment_name TEXT NOT NULL              -- tên hiển thị, độ dài tùy ý. NOT NULL = bắt buộc có
);
-- \copy: đọc file CSV trên máy bạn và đưa vào bảng.
-- HEADER true = bỏ qua dòng đầu (tiêu đề cột). Thứ tự cột trong bảng phải giống thứ tự trong CSV.
-- Lệnh \copy viết trên MỘT dòng, không có dấu ; ở cuối.
\copy north.dim_segment FROM '02_data/north_provinces/dim_segment.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- ===== dim_branch [MẪU 2: bảng dim có nhiều cột chữ] =====
-- Cột trong CSV: branch_id,branch_name,province,economic_profile
CREATE TABLE north.dim_branch (
    branch_id        VARCHAR(10) PRIMARY KEY,
    branch_name      TEXT NOT NULL,
    province         TEXT,
    economic_profile TEXT                   -- trong CSV có dấu phẩy trong ngoặc kép, FORMAT csv tự xử lý
);
\copy north.dim_branch FROM '02_data/north_provinces/dim_branch.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- ===== dim_month [MẪU 3: bảng dim có cột số nguyên] =====
-- Cột trong CSV: month,year,month_num,quarter
CREATE TABLE north.dim_month (
    month     CHAR(7) PRIMARY KEY,          -- luôn đúng 7 ký tự: '2025-01'
    year      INTEGER NOT NULL,             -- số nguyên: 2025
    month_num INTEGER NOT NULL,             -- 1..12
    quarter   TEXT NOT NULL                 -- 'Q1-2025'
);
\copy north.dim_month FROM '02_data/north_provinces/dim_month.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- ===== dim_product [BẠN VIẾT — giống MẪU 2] =====
-- Cột trong CSV: product_id,product_name,product_group,net_yield_annual
-- Điểm mới: net_yield_annual là tỷ lệ (0.09) → kiểu NUMERIC(8,4)
--   NUMERIC(8,4) = tổng 8 chữ số, trong đó 4 chữ số sau dấu phẩy. Số tiền và tỷ lệ dùng NUMERIC cho chính xác.
CREATE TABLE north.dim_product (
    product_id       VARCHAR(10) PRIMARY KEY,
    product_name     TEXT NOT NULL,
    product_group    TEXT NOT NULL,         -- Huy động / Tín dụng / Thẻ & thanh toán
    net_yield_annual NUMERIC(8,4)           -- lợi suất ròng năm, 0.09 = 9%
);
\copy north.dim_product FROM '02_data/north_provinces/dim_product.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- ===== fact_incentive [MẪU 4: bảng fact có khóa ngoại] =====
-- Cột trong CSV: month,branch_id,balance_achievement,revenue_achievement,kpi_score,incentive_pool_mn
CREATE TABLE north.fact_incentive (
    month               CHAR(7)     NOT NULL REFERENCES north.dim_month (month),
    branch_id           VARCHAR(10) NOT NULL REFERENCES north.dim_branch (branch_id),
    -- REFERENCES = khóa ngoại: giá trị ở đây BẮT BUỘC phải có trong bảng dim.
    -- Kiểu dữ liệu phải giống cột bên dim (CHAR(7) ↔ CHAR(7)).
    balance_achievement NUMERIC(8,4),       -- tỷ lệ 1.0044
    revenue_achievement NUMERIC(8,4),
    kpi_score           NUMERIC(12,2),      -- điểm 100.45
    incentive_pool_mn   NUMERIC(12,2),      -- tiền, triệu VND
    PRIMARY KEY (month, branch_id)          -- khóa ghép: mỗi chi nhánh chỉ có 1 dòng mỗi tháng
);
\copy north.fact_incentive FROM '02_data/north_provinces/fact_incentive.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- ===== fact_policy_check [BẠN VIẾT — gần như giống hệt MẪU 4] =====
-- Cột trong CSV: month,branch_id,unsecured_loan_ratio,unsecured_loan_limit,commission_ratio,commission_cap
-- Cùng grain với fact_incentive (tháng × chi nhánh). 4 cột còn lại đều là tỷ lệ.
CREATE TABLE north.fact_policy_check (
    month                CHAR(7)     NOT NULL REFERENCES north.dim_month (month),
    branch_id            VARCHAR(10) NOT NULL REFERENCES north.dim_branch (branch_id),
    unsecured_loan_ratio NUMERIC(8,4),      -- tỷ lệ cho vay không TSBĐ thực tế
    unsecured_loan_limit NUMERIC(8,4),      -- hạn mức 0.30
    commission_ratio     NUMERIC(8,4),      -- tỷ lệ hoa hồng thực tế
    commission_cap       NUMERIC(8,4),      -- trần 0.035
    PRIMARY KEY (month, branch_id)
);
\copy north.fact_policy_check FROM '02_data/north_provinces/fact_policy_check.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- ===== fact_performance [BẠN VIẾT — mở rộng từ MẪU 4] =====
-- Cột trong CSV: month,branch_id,segment_id,product_id,plan_balance_bn,actual_balance_bn,plan_revenue_mn,actual_revenue_mn,plan_new_customers,actual_new_customers
-- Khác MẪU 4:
--   - 4 cột khóa, mỗi cột REFERENCES một bảng dim khác nhau
--   - cột tiền NUMERIC(12,2), cột khách hàng INTEGER
--   - actual_revenue_mn KHÔNG đặt NOT NULL (vì dữ liệu có dòng thiếu)
--   - KHÔNG đặt PRIMARY KEY (vì dữ liệu có dòng trùng — xem Bài 1)
CREATE TABLE north.fact_performance (
    month                CHAR(7)     NOT NULL REFERENCES north.dim_month (month),
    branch_id            VARCHAR(10) NOT NULL REFERENCES north.dim_branch (branch_id),
    segment_id           VARCHAR(10) NOT NULL REFERENCES north.dim_segment (segment_id),
    product_id           VARCHAR(10) NOT NULL REFERENCES north.dim_product (product_id),
    plan_balance_bn      NUMERIC(12,2),     -- tỷ VND, số dư cuối tháng (chỉ tiêu THỜI ĐIỂM)
    actual_balance_bn    NUMERIC(12,2),
    plan_revenue_mn      NUMERIC(12,2),     -- triệu VND, phát sinh trong tháng (chỉ tiêu THỜI KỲ)
    actual_revenue_mn    NUMERIC(12,2),     -- cho phép NULL: dữ liệu có dòng thiếu (Bài 2)
    plan_new_customers   INTEGER,
    actual_new_customers INTEGER            -- INTEGER / INTEGER = số nguyên → nhớ ép kiểu khi chia (Bài 9)
    -- Không có PRIMARY KEY: dữ liệu có 1 dòng trùng khóa (Bài 1).
);
\copy north.fact_performance FROM '02_data/north_provinces/fact_performance.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')

-- ===== Kiểm tra số dòng =====
-- TODO: một câu SELECT trả về 7 dòng: ten_bang, so_dong
--       Gợi ý: SELECT 'dim_segment' AS ten_bang, COUNT(*) AS so_dong FROM north.dim_segment
--              UNION ALL ... (6 bảng còn lại)
