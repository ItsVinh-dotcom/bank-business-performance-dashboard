"""
Dữ liệu MÔ PHỎNG cho dự án Bank Business Performance - nhánh miền Bắc.

Không phải dữ liệu thật của bất kỳ ngân hàng hay địa phương nào. Quy mô và
đặc điểm kinh tế từng chi nhánh được hiệu chỉnh theo nhận định định tính
(Hà Nội là trung tâm tài chính lớn nhất; Hải Phòng là cảng và công nghiệp;
Quảng Ninh là than và du lịch; Bắc Ninh là khu công nghiệp FDI). Các con số
tổng quy mô chỉ là giả định để tạo dữ liệu có độ lớn hợp lý.

Chạy:  python generate_north_sim.py <thư_mục_đích>
Seed cố định để tái lập.
"""

from __future__ import annotations

import csv
import random
import sys
from datetime import date
from pathlib import Path

SEED = 20260601
random.seed(SEED)

# branch_id, tên chi nhánh, tỉnh/thành, đặc điểm kinh tế, quy mô dư nợ tháng 1/2025 (tỷ VND)
BRANCHES = [
    ("HN", "CN Hà Nội", "Hà Nội", "Trung tâm tài chính, doanh nghiệp dịch vụ", 4000.0),
    ("HP", "CN Hải Phòng", "Hải Phòng", "Cảng biển và công nghiệp chế biến", 1800.0),
    ("QN", "CN Quảng Ninh", "Quảng Ninh", "Than, du lịch và dịch vụ lưu trú", 1000.0),
    ("BN", "CN Bắc Ninh", "Bắc Ninh", "Khu công nghiệp FDI, lao động làm công ăn lương", 1300.0),
]

# segment_id, tên phân khúc
SEGMENTS = {"CN": "Cá nhân", "SME": "SME", "DN": "Doanh nghiệp"}

# product_id, tên sản phẩm, nhóm, lợi suất ròng năm (ước tính), khách hàng mới / tỷ dư nợ
PRODUCTS = {
    "TGKH": ("Tiền gửi có kỳ hạn", "Huy động", 0.020, 0.9),
    "VTD": ("Vay tiêu dùng", "Tín dụng", 0.090, 2.2),
    "THE": ("Thẻ tín dụng", "Thẻ & thanh toán", 0.140, 3.5),
    "VSME": ("Vay SME", "Tín dụng", 0.070, 0.12),
    "VDN": ("Vay doanh nghiệp", "Tín dụng", 0.065, 0.02),
}

# Tổ hợp hợp lệ (phân khúc, sản phẩm) và tỷ trọng trong tổng dư nợ chi nhánh.
# Tổng tỷ trọng mỗi chi nhánh = 1.
MIX = {
    "HN": {("CN", "TGKH"): .12, ("CN", "VTD"): .10, ("CN", "THE"): .04,
           ("SME", "TGKH"): .05, ("SME", "VSME"): .12,
           ("DN", "TGKH"): .20, ("DN", "VDN"): .37},
    "HP": {("CN", "TGKH"): .10, ("CN", "VTD"): .08, ("CN", "THE"): .03,
           ("SME", "TGKH"): .08, ("SME", "VSME"): .20,
           ("DN", "TGKH"): .12, ("DN", "VDN"): .39},
    "QN": {("CN", "TGKH"): .14, ("CN", "VTD"): .07, ("CN", "THE"): .09,
           ("SME", "TGKH"): .05, ("SME", "VSME"): .14,
           ("DN", "TGKH"): .12, ("DN", "VDN"): .39},
    "BN": {("CN", "TGKH"): .09, ("CN", "VTD"): .18, ("CN", "THE"): .03,
           ("SME", "TGKH"): .05, ("SME", "VSME"): .10,
           ("DN", "TGKH"): .10, ("DN", "VDN"): .45},
}

MONTHS = []
for y in (2025, 2026):
    for m in range(1, 13):
        if y == 2026 and m > 6:
            break
        MONTHS.append(date(y, m, 1))

LIMIT_UNSECURED = 0.30   # hạn mức giả định: (vay tiêu dùng + thẻ) / tổng dư nợ tín dụng
COMMISSION_CAP = 0.035   # trần giả định tỷ lệ hoa hồng / doanh thu mới


def idx(d: date) -> int:
    return (d.year - 2025) * 12 + d.month - 1


def trend(d: date) -> float:
    """Tăng trưởng dư nợ kế hoạch khoảng 1,2% mỗi tháng."""
    return 1.012 ** idx(d)


def seasonal(d: date, product: str, branch: str) -> float:
    """Mùa vụ theo sản phẩm và địa phương."""
    f = 1.0
    m = d.month
    # Tết (tháng 1-2): tiền gửi cá nhân tăng trước Tết; chi tiêu thẻ tăng.
    if m in (1,) and product == "TGKH":
        f *= 1.06
    if m in (1, 2) and product == "THE":
        f *= 1.10
    if m == 2 and product == "VTD":
        f *= 0.95
    # Cuối năm: đẩy tín dụng tiêu dùng và doanh nghiệp.
    if m in (11, 12) and product in ("VTD", "VDN"):
        f *= 1.03
    # Quảng Ninh: mùa du lịch hè, thẻ và SME lưu trú tăng.
    if branch == "QN" and m in (6, 7, 8) and product in ("THE", "VSME"):
        f *= 1.12
    return f


def plan_balance(branch: str, seg: str, prod: str, share: float, base: float, d: date) -> float:
    return base * share * trend(d) * seasonal(d, prod, branch)


def actual_factor(branch: str, seg: str, prod: str, d: date) -> float:
    """Hệ số thực hiện so với kế hoạch, kèm nhiễu và các điểm bất thường có chủ đích."""
    f = random.gauss(1.0, 0.012)  # nhiễu nhỏ, số thực thường bám kế hoạch
    # Hà Nội: thực hiện tốt, nhất là doanh nghiệp.
    if branch == "HN" and seg == "DN":
        f *= 1.01
    # Hải Phòng: SME lệch kế hoạch từ tháng 1/2026 (áp lực sản xuất, giả định).
    if branch == "HP" and seg == "SME" and d >= date(2026, 1, 1):
        f *= 0.91
    # Quảng Ninh: thẻ tăng mạnh hơn kế hoạch vào mùa hè 2025.
    if branch == "QN" and prod == "THE" and date(2025, 6, 1) <= d <= date(2025, 8, 1):
        f *= 1.18
    # Quảng Ninh: SME tiền gửi hụt kế hoạch đầu 2025 (giả định).
    if branch == "QN" and prod == "TGKH" and seg == "SME" and d < date(2025, 4, 1):
        f *= 0.90
    # Bắc Ninh: vay tiêu dùng đẩy mạnh cuối 2025 (xem phần chính sách).
    if branch == "BN" and prod == "VTD" and date(2025, 11, 1) <= d <= date(2025, 12, 1):
        f *= 1.25
    return f


def build_performance():
    rows = []
    base_by_branch = {b[0]: b[4] for b in BRANCHES}
    for d in MONTHS:
        for bid, _, _, _, _ in BRANCHES:
            for (seg, prod), share in MIX[bid].items():
                pb = plan_balance(bid, seg, prod, share, base_by_branch[bid], d)
                ab = pb * actual_factor(bid, seg, prod, d)
                yld = PRODUCTS[prod][2]
                pr = pb * yld / 12 * 1000            # triệu VND / tháng
                ar = ab * yld / 12 * 1000 * random.gauss(1.0, 0.01)
                k = PRODUCTS[prod][3]
                pn = round(pb * k * 10 + random.uniform(-2, 2))
                an = round(pn * (ab / pb) * random.gauss(1.0, 0.04))
                rows.append({
                    "month": d.strftime("%Y-%m"),
                    "branch_id": bid,
                    "segment_id": seg,
                    "product_id": prod,
                    "plan_balance_bn": round(pb, 2),
                    "actual_balance_bn": round(ab, 2),
                    "plan_revenue_mn": round(pr, 1),
                    "actual_revenue_mn": round(ar, 1),
                    "plan_new_customers": max(pn, 0),
                    "actual_new_customers": max(an, 0),
                })
    return rows


def build_policy(perf_rows):
    """Tỷ lệ tín chấp (vay tiêu dùng + thẻ) / tổng dư nợ tín dụng, theo chi nhánh-tháng."""
    agg = {}
    for r in perf_rows:
        key = (r["month"], r["branch_id"])
        a = agg.setdefault(key, {"credit": 0.0, "unsec": 0.0})
        if r["product_id"] in ("VTD", "THE", "VSME", "VDN"):
            a["credit"] += r["actual_balance_bn"]
        if r["product_id"] in ("VTD", "THE"):
            a["unsec"] += r["actual_balance_bn"]
    rows = []
    for (month, bid), a in sorted(agg.items()):
        ratio = a["unsec"] / a["credit"] if a["credit"] else 0
        commission = random.gauss(0.028, 0.002)
        rows.append({
            "month": month,
            "branch_id": bid,
            "unsecured_loan_ratio": round(ratio, 4),
            "unsecured_loan_limit": LIMIT_UNSECURED,
            "commission_ratio": round(commission, 4),
            "commission_cap": COMMISSION_CAP,
        })
    return rows


def build_incentive(perf_rows):
    agg = {}
    for r in perf_rows:
        key = (r["month"], r["branch_id"])
        a = agg.setdefault(key, {"pb": 0.0, "ab": 0.0, "pr": 0.0, "ar": 0.0})
        a["pb"] += r["plan_balance_bn"]
        a["ab"] += r["actual_balance_bn"]
        a["pr"] += r["plan_revenue_mn"]
        a["ar"] += r["actual_revenue_mn"]
    rows = []
    for (month, bid), a in sorted(agg.items()):
        bal = a["ab"] / a["pb"]
        rev = a["ar"] / a["pr"]
        kpi = round(100 * (0.6 * bal + 0.4 * rev), 2)
        rows.append({
            "month": month,
            "branch_id": bid,
            "balance_achievement": round(bal, 4),
            "revenue_achievement": round(rev, 4),
            "kpi_score": kpi,
            "incentive_pool_mn": round(max(kpi - 90, 0) * 1.5, 1),
        })
    return rows


def inject_dq(rows):
    """Lỗi có chủ đích để kiểm tra chất lượng: 2 dòng thiếu doanh thu, 1 dòng trùng."""
    out = list(rows)
    for i in (57, 311):
        out[i] = {**out[i], "actual_revenue_mn": ""}
    out.insert(180, dict(out[180]))
    return out


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main(out_dir: Path):
    perf = build_performance()
    write_csv(out_dir / "fact_performance.csv", inject_dq(perf))
    write_csv(out_dir / "fact_policy_check.csv", build_policy(perf))
    write_csv(out_dir / "fact_incentive.csv", build_incentive(perf))
    write_csv(out_dir / "dim_branch.csv", [
        {"branch_id": b[0], "branch_name": b[1], "province": b[2], "economic_profile": b[3]} for b in BRANCHES])
    write_csv(out_dir / "dim_segment.csv", [{"segment_id": k, "segment_name": v} for k, v in SEGMENTS.items()])
    write_csv(out_dir / "dim_product.csv", [
        {"product_id": k, "product_name": v[0], "product_group": v[1], "net_yield_annual": v[2]}
        for k, v in PRODUCTS.items()])
    write_csv(out_dir / "dim_month.csv", [
        {"month": d.strftime("%Y-%m"), "year": d.year, "month_num": d.month,
         "quarter": f"Q{(d.month - 1) // 3 + 1}-{d.year}"} for d in MONTHS])
    print("OK")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
