-- Bài 1 — DQ02: trùng khóa trong fact_performance
-- Câu hỏi: Có dòng nào trùng khóa (month, branch_id, segment_id, product_id) không?
-- Đáp số kỳ vọng: 1 khóa (2025-07, HP, DN, TGKH) xuất hiện 2 lần
SELECT
	month,
	branch_id,
	segment_id,
	product_id,
	COUNT(*) AS solan
FROM north.fact_performance
GROUP BY
	month,
	branch_id,
	segment_id,
	product_id
HAVING COUNT(*) > 1
ORDER BY solan DESC
-- Câu 2: Dữ liệu có thực sự trùng nhau ở toàn bộ các giá trị, hay là chỉ trùng ở các dữ liệu khóa?
SELECT
	month, branch_id, segment_id, product_id, plan_balance_bn, actual_balance_bn, plan_revenue_mn, actual_revenue_mn, plan_new_customers, actual_new_customers,
	COUNT(*) AS solan
FROM north.fact_performance
GROUP BY
	month, branch_id, segment_id, product_id, plan_balance_bn, actual_balance_bn, plan_revenue_mn, actual_revenue_mn, plan_new_customers, actual_new_customers
HAVING COUNT(*) > 1
ORDER BY solan DESC
-- Câu 2: đúng, 232,95 tỷ. Tôi vừa chạy thêm để bạn thấy mức ảnh hưởng:
-- Số dư thực tế bị thổi lên khoảng 12%, nhưng tỷ lệ hoàn thành chỉ lệch 0,08 điểm %. Lý do: dòng trùng bị cộng hai lần ở cả kế hoạch lẫn thực tế, nên khi chia thì gần như triệt tiêu nhau. Đây là điểm đáng nói khi phỏng vấn: nhìn tỷ lệ thấy ổn, không ai nghi ngờ, nhưng con số tuyệt đối gửi lên lãnh đạo bị sai hơn 230 tỷ. Câu nên dùng: "Dòng trùng không làm sai tỷ lệ nhiều, nhưng làm sai số tuyệt đối 12%. Vì vậy em kiểm tra trùng khóa trước khi phát hành báo cáo, không chỉ nhìn tỷ lệ."