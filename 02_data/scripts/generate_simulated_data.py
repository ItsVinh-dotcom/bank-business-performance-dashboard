"""
Sinh dữ liệu GIẢ LẬP cho project Bank Business Performance & KPI Dashboard.

Toàn bộ số liệu là giả lập để phục vụ thực hành; không phản ánh dữ liệu thật
của bất kỳ ngân hàng nào. Có seed cố định để tái lập kết quả.

Chạy:
    python 02_data/scripts/generate_simulated_data.py

Đầu ra (02_data/raw_simulated/):
    fact_performance.csv   : tháng x chi nhánh x phân khúc x sản phẩm (kế hoạch & thực tế)
    fact_policy_check.csv  : tháng x chi nhánh (chỉ số chính sách và hạn mức)
    fact_incentive.csv     : tháng x chi nhánh (điểm KPI và quỹ incentive)
Đầu ra (02_data/reference/):
    dim_branch.csv, dim_segment.csv, dim_product.csv, dim_month.csv

Các "điểm bất thường có chủ đích" được cài sẵn để phục vụ phân tích:
    - CN Huế: thực hiện thấp hơn kế hoạch liên tục từ tháng 7/2025 ở phân khúc SME.
    - CN Cần Thơ: vi phạm hạn mức cho vay không có tài sản bảo đảm trong 4 tháng cuối 2025.
    - CN Đà Nẵng: tăng trưởng thẻ tín dụng mạnh vào Q4/2025 (mix sản phẩm lệch).
    - Lỗi dữ liệu nhỏ có chủ đích (để kiểm tra chất lượng): 3 dòng thiếu giá trị thực tế
      và 2 dòng trùng khóa; ghi rõ trong 08_documentation/assumptions.md.
"""

from __future__ import annotations

import csv
import random
from datetime import date
from pathlib import Path

SEED = 20260601
random.seed(SEED)

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "02_data" / "raw_simulated"
REF_DIR = ROOT / "02_data" / "reference"

BRANCHES = [
    # branch_id, branch_name, region, size_factor
    ("BR01", "CN Hà Nội", "Miền Bắc", 1.40),
    ("BR02", "CN Hải Phòng", "Miền Bắc", 0.90),
    ("BR03", "CN Huế", "Miền Trung", 0.70),
    ("BR04", "CN Đà Nẵng", "Miền Trung", 1.10),
    ("BR05", "CN TP.HCM", "Miền Nam", 1.70),
    ("BR06", "CN Cần Thơ", "Miền Nam", 0.80),
]

SEGMENTS = [
    # segment_id, segment_name, base_balance_bn (quy mô tháng trung bình, tỷ VND)
    ("SEG01", "Cá nhân", 1200.0),
    ("SEG02", "SME", 800.0),
    ("SEG03", "Doanh nghiệp", 1000.0),
]

PRODUCTS = [
    # product_id, product_name, product_group, yield_rate (lãi/phí ước tính năm)
    ("PRD01", "Tiền gửi có kỳ hạn", "Huy động", 0.045),
    ("PRD02", "Vay tiêu dùng", "Tín dụng", 0.110),
    ("PRD03", "Vay SME", "Tín dụng", 0.095),
    ("PRD04", "Thẻ tín dụng", "Thẻ & thanh toán", 0.160),
    ("PRD05", "Thanh toán không dùng tiền mặt", "Thẻ & thanh toán", 0.020),
]

# Tỷ trọng sản phẩm theo phân khúc (tổng = 1 cho mỗi phân khúc)
PRODUCT_MIX = {
    "SEG01": {"PRD01": 0.30, "PRD02": 0.30, "PRD03": 0.00, "PRD04": 0.25, "PRD05": 0.15},
    "SEG02": {"PRD01": 0.25, "PRD02": 0.00, "PRD03": 0.45, "PRD04": 0.10, "PRD05": 0.20},
    "SEG03": {"PRD01": 0.45, "PRD02": 0.00, "PRD03": 0.35, "PRD04": 0.00, "PRD05": 0.20},
}

MONTHS = []
for y in (2025, 2026):
    for m in range(1, 13):
        if y == 2026 and m > 6:
            break
        MONTHS.append(date(y, m, 1))


def month_index(d: date) -> int:
    return (d.year - 2025) * 12 + d.month - 1


def seasonal(d: date) -> float:
    """Hệ số mùa vụ: Tết (tháng 1-2) và cuối năm (tháng 11-12) tăng nhẹ."""
    return {1: 1.08, 2: 0.95, 11: 1.05, 12: 1.10}.get(d.month, 1.0)


def trend(d: date) -> float:
    """Tăng trưởng đều khoảng 1.2% mỗi tháng."""
    return 1.012 ** month_index(d)


def noise(scale: float = 0.03) -> float:
    return random.gauss(1.0, scale)


def plan_factor(d: date, branch_id: str, segment_id: str) -> float:
    """Kế hoạch đặt theo xu hướng và mùa vụ, hơi cao so với quy mô nền."""
    return 1.02 * trend(d) * seasonal(d)


def actual_factor(d: date, branch_id: str, segment_id: str) -> float:
    """Thực tế = kế hoạch x hệ số thực hiện (có nhiễu) + các điểm bất thường có chủ đích."""
    f = plan_factor(d, branch_id, segment_id) * noise(0.04)
    # CN Huế, phân khúc SME: thấp hơn kế hoạch từ tháng 7/2025
    if branch_id == "BR03" and segment_id == "SEG02" and d >= date(2025, 7, 1):
        f *= 0.86
    # CN Đà Nẵng: vượt kế hoạch mạnh ở thẻ trong Q4/2025 (xử lý ở tầng sản phẩm)
    return f


def build_performance() -> list[dict]:
    rows: list[dict] = []
    for d in MONTHS:
        for b_id, b_name, region, b_size in BRANCHES:
            for s_id, s_name, s_base in SEGMENTS:
                for p_id, p_name, p_group, p_yield in PRODUCTS:
                    mix = PRODUCT_MIX[s_id][p_id]
                    if mix == 0:
                        continue
                    base_balance = s_base * b_size * mix * 1.0  # tỷ VND
                    plan_balance = base_balance * plan_factor(d, b_id, s_id)
                    actual_bal = base_balance * actual_factor(d, b_id, s_id)

                    # CN Đà Nẵng: thẻ tín dụng vượt kế hoạch Q4/2025
                    if b_id == "BR04" and p_id == "PRD04" and date(2025, 10, 1) <= d <= date(2025, 12, 1):
                        actual_bal *= 1.25

                    plan_rev = plan_balance * p_yield / 12 * 1000  # triệu VND/tháng
                    actual_rev = actual_bal * p_yield / 12 * 1000 * noise(0.03)

                    plan_new = round(plan_balance * 8.5 * b_size / 10 + random.uniform(-3, 3))
                    actual_new = round(plan_new * (actual_bal / plan_balance) * noise(0.05))

                    rows.append(
                        {
                            "month": d.strftime("%Y-%m"),
                            "branch_id": b_id,
                            "segment_id": s_id,
                            "product_id": p_id,
                            "plan_balance_bn": round(plan_balance, 2),
                            "actual_balance_bn": round(actual_bal, 2),
                            "plan_revenue_mn": round(plan_rev, 1),
                            "actual_revenue_mn": round(actual_rev, 1),
                            "plan_new_customers": max(plan_new, 0),
                            "actual_new_customers": max(actual_new, 0),
                        }
                    )
    return rows


def build_policy_check() -> list[dict]:
    rows: list[dict] = []
    for d in MONTHS:
        for b_id, b_name, region, b_size in BRANCHES:
            # Hạn mức chính sách (giả định): tỷ lệ cho vay không có TSBĐ tối đa 30% dư nợ tín dụng
            limit_unsecured = 0.30
            unsecured = random.gauss(0.22, 0.02)
            if b_id == "BR06" and date(2025, 9, 1) <= d <= date(2025, 12, 1):
                unsecured = random.gauss(0.335, 0.01)  # vi phạm hạn mức
            # Tỷ lệ chi phí hoa hồng trên doanh thu mới (giả định trần 3.5%)
            commission_cap = 0.035
            commission = random.gauss(0.028, 0.003)
            rows.append(
                {
                    "month": d.strftime("%Y-%m"),
                    "branch_id": b_id,
                    "unsecured_loan_ratio": round(unsecured, 4),
                    "unsecured_loan_limit": limit_unsecured,
                    "commission_ratio": round(commission, 4),
                    "commission_cap": commission_cap,
                }
            )
    return rows


def build_incentive(perf_rows: list[dict]) -> list[dict]:
    """Điểm KPI tổng hợp theo chi nhánh-tháng: tỷ lệ hoàn thành dư nợ và doanh thu."""
    agg: dict[tuple[str, str], dict[str, float]] = {}
    for r in perf_rows:
        key = (r["month"], r["branch_id"])
        a = agg.setdefault(key, {"pb": 0.0, "ab": 0.0, "pr": 0.0, "ar": 0.0})
        a["pb"] += r["plan_balance_bn"]
        a["ab"] += r["actual_balance_bn"]
        a["pr"] += r["plan_revenue_mn"]
        a["ar"] += r["actual_revenue_mn"]

    rows: list[dict] = []
    for (month, b_id), a in sorted(agg.items()):
        bal_ach = a["ab"] / a["pb"] if a["pb"] else 0
        rev_ach = a["ar"] / a["pr"] if a["pr"] else 0
        kpi_score = round(100 * (0.6 * bal_ach + 0.4 * rev_ach), 2)
        incentive_pool_mn = round(max(kpi_score - 90, 0) * 1.5, 1)  # triệu VND (giả định)
        rows.append(
            {
                "month": month,
                "branch_id": b_id,
                "balance_achievement": round(bal_ach, 4),
                "revenue_achievement": round(rev_ach, 4),
                "kpi_score": kpi_score,
                "incentive_pool_mn": incentive_pool_mn,
            }
        )
    return rows


def inject_data_quality_issues(perf_rows: list[dict]) -> list[dict]:
    """Cài 3 dòng thiếu giá trị và 2 dòng trùng khóa có chủ đích để kiểm tra chất lượng dữ liệu."""
    rows = list(perf_rows)
    for idx in (101, 487, 1100):
        rows[idx] = {**rows[idx], "actual_revenue_mn": ""}
    dup_src = rows[250]
    rows.insert(251, dict(dup_src))
    dup_src2 = rows[900]
    rows.insert(901, dict(dup_src2))
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_reference() -> None:
    write_csv(
        REF_DIR / "dim_branch.csv",
        [{"branch_id": b[0], "branch_name": b[1], "region": b[2]} for b in BRANCHES],
    )
    write_csv(
        REF_DIR / "dim_segment.csv",
        [{"segment_id": s[0], "segment_name": s[1]} for s in SEGMENTS],
    )
    write_csv(
        REF_DIR / "dim_product.csv",
        [{"product_id": p[0], "product_name": p[1], "product_group": p[2]} for p in PRODUCTS],
    )
    write_csv(
        REF_DIR / "dim_month.csv",
        [
            {
                "month": d.strftime("%Y-%m"),
                "year": d.year,
                "month_num": d.month,
                "quarter": f"Q{(d.month - 1) // 3 + 1}-{d.year}",
            }
            for d in MONTHS
        ],
    )


def main() -> None:
    perf = build_performance()
    perf_dirty = inject_data_quality_issues(perf)
    write_csv(RAW_DIR / "fact_performance.csv", perf_dirty)
    write_csv(RAW_DIR / "fact_policy_check.csv", build_policy_check())
    write_csv(RAW_DIR / "fact_incentive.csv", build_incentive(perf))  # tính từ dữ liệu sạch
    write_reference()
    print(f"fact_performance: {len(perf_dirty)} dòng (kể cả dòng lỗi có chủ đích)")
    print(f"fact_policy_check: {len(MONTHS) * len(BRANCHES)} dòng")
    print(f"fact_incentive: {len(build_incentive(perf))} dòng")


if __name__ == "__main__":
    main()
