# Dàn ý trình bày (khoảng 10 phút, dùng cho phỏng vấn)

Dàn ý này viết theo thứ tự nghiệp vụ, không theo thứ tự kỹ thuật. Mục tiêu là cho người nghe thấy cách bạn nghĩ về bài toán quản trị hiệu suất, rồi mới thấy công cụ bạn dùng.

## 1. Bối cảnh và câu hỏi quản trị (1 phút)

Trình bày ba câu hỏi nghiệp vụ chính: chi nhánh nào đang lệch kế hoạch và vì sao, cơ chế KPI có khuyến khích đúng hành vi không, và báo cáo có đáng tin không. Nhấn mạnh rằng dữ liệu là giả lập để thực hành.

## 2. Cách tiếp cận (1 phút)

Giải thích luồng: định nghĩa KPI, dữ liệu kế hoạch và thực tế theo tháng-chi nhánh-phân khúc-sản phẩm, kiểm tra chất lượng dữ liệu, phân tích chênh lệch, rồi dashboard và khuyến nghị.

## 3. Phát hiện chính (4 phút)

Bắt đầu bằng tổng công ty đi đúng kế hoạch để tạo bất ngờ. Sau đó chia nhỏ ra CN Huế SME (thiếu khoảng 7,3 tỷ đồng, dư nợ đạt 84% đến 89%, nguyên nhân chủ yếu là khách hàng mới). Tiếp theo là CN Cần Thơ, đạt KPI nhưng vi phạm hạn mức trong 4 tháng. Cuối cùng là CN Đà Nẵng thẻ tín dụng Q4/2025 vượt kế hoạch, và dữ liệu thiếu làm sai tỷ lệ tháng 2/2025.

## 4. Khuyến nghị (2 phút)

Trình bày năm khuyến nghị, nhưng chỉ đi sâu vào hai: thêm điều kiện tuân thủ vào KPI, và bắt buộc kiểm tra DQ trước khi báo cáo. Nêu thứ tự triển khai 30 ngày.

## 5. Dashboard và kỹ thuật (1 phút)

Demo nhanh một trang. Nói về SQL và cách kiểm tra chéo số liệu giữa truy vấn, phân tích và dashboard. Nếu được hỏi về công cụ, nói rõ đã dùng Power BI và SQL, còn Python dùng để sinh dữ liệu giả lập.

## 6. Giới hạn và bước tiếp theo (1 phút)

Nêu rõ những gì dữ liệu không có: nợ xấu, chi phí vốn, lợi nhuận sau rủi ro, ngày. Đề xuất bước tiếp theo khi có dữ liệu nội bộ.

## Câu hỏi có thể gặp

Về KPI: "Tại sao trọng số 60/40?" Trả lời: đó là giả định để minh họa, nên điều chỉnh theo chiến lược, và mô phỏng trước khi áp dụng. Về dữ liệu: "Làm sao biết số liệu đúng?" Trả lời: có bộ kiểm tra DQ01 đến DQ04 và đối chiếu chéo giữa các bảng. Về nhân sự phỏng vấn: "Bạn đã làm việc với dữ liệu ngân hàng chưa?" Trả lời trung thực theo kinh nghiệm thực của bạn, và dùng dự án này như bằng chứng về cách tiếp cận.
