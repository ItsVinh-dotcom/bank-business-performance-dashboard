"""Apply the shared executive layout to the existing PBIR report.

Run without arguments for a dry run. Use --apply only with Power BI Desktop
closed; the script updates layout metadata and adds sidebar visuals without
deleting existing pages or changing fact/measure visual queries.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPORT_ROOT = Path(__file__).resolve().parent / "DashboardMienBac.Report"
DEFINITION_ROOT = REPORT_ROOT / "definition"
PAGES_ROOT = DEFINITION_ROOT / "pages"
VISUAL_SCHEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
    "visualContainer/2.14.0/schema.json"
)

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
SIDEBAR_WIDTH = 190
CONTENT_X = 216
CONTENT_WIDTH = 1048
RED = "#A30E33"
NAVY = "#173F5F"
GREY = "#59636D"
LIGHT_BORDER = "#D9DEE5"


def literal(value: Any) -> dict[str, Any]:
    if isinstance(value, bool):
        text = "true" if value else "false"
    elif isinstance(value, int):
        text = f"{value}L"
    elif isinstance(value, float):
        text = f"{value}D"
    else:
        text = "'" + str(value).replace("'", "''") + "'"
    return {"expr": {"Literal": {"Value": text}}}


def color(hex_value: str) -> dict[str, Any]:
    return {"solid": {"color": literal(hex_value)}}


def properties(**values: Any) -> list[dict[str, Any]]:
    return [
        {
            "properties": {
                key: value if isinstance(value, dict) else literal(value)
                for key, value in values.items()
            }
        }
    ]


def paragraph(text: str, size: float, text_color: str, bold: bool = False) -> dict[str, Any]:
    style: dict[str, str] = {"fontSize": f"{size}pt", "color": text_color}
    if bold:
        style["fontWeight"] = "bold"
    return {"textRuns": [{"value": text, "textStyle": style}]}


def container_frame(title: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "background": properties(
            show=True,
            color=color("#FFFFFF"),
            transparency=0.0,
        ),
        "border": properties(
            show=True,
            color=color(LIGHT_BORDER),
            radius=8.0,
            width=1.0,
        ),
        "dropShadow": properties(show=False),
    }
    if title:
        result["title"] = properties(
            show=True,
            text=title,
            fontColor=color(RED),
            fontSize=11.0,
            bold=True,
            fontFamily="Segoe UI Semibold",
        )
    return result


def textbox_visual(
    name: str,
    x: int,
    y: int,
    width: int,
    height: int,
    paragraphs: list[dict[str, Any]],
    *,
    background: str | None = None,
    z: int = 20,
) -> dict[str, Any]:
    container_objects: dict[str, Any] = {
        "background": properties(show=background is not None),
        "border": properties(show=False),
        "dropShadow": properties(show=False),
        "title": properties(show=False),
        "subTitle": properties(show=False),
        "padding": properties(top=0.0, bottom=0.0, left=0.0, right=0.0),
    }
    if background:
        container_objects["background"] = properties(
            show=True,
            color=color(background),
            transparency=0.0,
        )
    return {
        "$schema": VISUAL_SCHEMA,
        "name": name,
        "position": {
            "x": x,
            "y": y,
            "z": z,
            "height": height,
            "width": width,
            "tabOrder": z,
        },
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [{"properties": {"paragraphs": paragraphs}}]
            },
        },
        "visualContainerObjects": container_objects,
    }


def write_json(path: Path, value: dict[str, Any], apply: bool) -> None:
    if not apply:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_visual(page_key: str, visual_key: str, visual: dict[str, Any], apply: bool) -> None:
    path = PAGES_ROOT / page_key / "visuals" / visual_key / "visual.json"
    write_json(path, visual, apply)


def update_existing_visual(
    page_key: str,
    visual_key: str,
    *,
    position: tuple[int, int, int, int] | None = None,
    title: str | None = None,
    display_names: dict[str, str] | None = None,
    card: bool = False,
    apply: bool,
) -> None:
    path = PAGES_ROOT / page_key / "visuals" / visual_key / "visual.json"
    visual = load_json(path)
    if position:
        x, y, width, height = position
        visual["position"].update(
            {"x": x, "y": y, "width": width, "height": height}
        )

    if display_names:
        query_state = visual.get("visual", {}).get("query", {}).get("queryState", {})
        for projection_state in query_state.values():
            for projection in projection_state.get("projections", []):
                query_ref = projection.get("queryRef")
                if query_ref in display_names:
                    projection["displayName"] = display_names[query_ref]

    container_objects = visual.setdefault("visualContainerObjects", {})
    if card:
        container_objects.update(container_frame())
        visual_objects = visual.setdefault("visual", {}).setdefault("objects", {})
        visual_objects["labels"] = properties(
            color=color(NAVY),
            fontSize=24.0,
            fontFace="Segoe UI Semibold",
            labelDisplayUnits=1.0,
        )
        visual_objects["categoryLabels"] = properties(
            show=True,
            color=color(GREY),
            fontSize=9.5,
            fontFace="Segoe UI",
        )
    elif title:
        container_objects.update(container_frame())
        container_objects.pop("title", None)
        visual_objects = visual.setdefault("visual", {}).setdefault("objects", {})
        visual_objects["title"] = properties(show=False)

    save_visual(page_key, visual_key, visual, apply)


def slicer_visual(
    name: str,
    field_table: str,
    field_name: str,
    display_name: str,
    group_name: str,
    y: int,
) -> dict[str, Any]:
    projection = {
        "field": {
            "Column": {
                "Expression": {"SourceRef": {"Entity": field_table}},
                "Property": field_name,
            }
        },
        "queryRef": f"{field_table}.{field_name}",
        "nativeQueryRef": field_name,
        "displayName": display_name,
        "active": True,
    }
    return {
        "$schema": VISUAL_SCHEMA,
        "name": name,
        "position": {
            "x": 12,
            "y": y,
            "z": 30,
            "height": 52,
            "width": 166,
            "tabOrder": 30,
        },
        "visual": {
            "visualType": "slicer",
            "query": {"queryState": {"Values": {"projections": [projection]}}},
            "objects": {
                "data": properties(mode="Dropdown"),
                "header": properties(
                    show=True,
                    fontColor=color(NAVY),
                    textSize=9.0,
                ),
                "items": properties(textSize=9.0),
            },
            "syncGroup": {
                "groupName": group_name,
                "fieldChanges": False,
                "filterChanges": True,
            },
            "drillFilterOtherVisuals": True,
        },
        "visualContainerObjects": container_frame(),
    }


def add_shared_chrome(
    page_key: str,
    title: str,
    subtitle: str,
    apply: bool,
) -> None:
    visuals_root = PAGES_ROOT / page_key / "visuals"
    visual_specs = {
        "sidebar_bg": textbox_visual(
            "sidebar_bg",
            0,
            0,
            SIDEBAR_WIDTH,
            CANVAS_HEIGHT,
            [paragraph(" ", 8.0, GREY)],
            background="#FFFFFF",
            z=-20,
        ),
        "brand": textbox_visual(
            "brand",
            0,
            0,
            SIDEBAR_WIDTH,
            82,
            [
                paragraph("BANK KPI", 14.0, "#FFFFFF", bold=True),
                paragraph("Mô phỏng hiệu quả kinh doanh", 8.5, "#FCE8EC"),
            ],
            background=RED,
        ),
        "filter_heading": textbox_visual(
            "filter_heading",
            12,
            94,
            166,
            18,
            [paragraph("BỘ LỌC", 8.5, GREY, bold=True)],
        ),
        "footer": textbox_visual(
            "footer",
            12,
            622,
            166,
            76,
            [
                paragraph("Dữ liệu mô phỏng", 8.5, GREY, bold=True),
                paragraph("Đơn vị: tỷ đồng, triệu đồng", 8.0, GREY),
                paragraph("Không phải số liệu MSB", 8.0, GREY),
            ],
        ),
        "page_header": textbox_visual(
            "page_header",
            CONTENT_X,
            2,
            CONTENT_WIDTH,
            64,
            [
                paragraph(title, 16.0, RED, bold=True),
                paragraph(subtitle, 8.5, GREY),
            ],
        ),
    }
    for visual_key, visual in visual_specs.items():
        write_json(visuals_root / visual_key / "visual.json", visual, apply)


def update_slicers(page_key: str, apply: bool) -> None:
    specifications = [
        ("s1", "dim_month", "year", "Năm", "shared_year", 120),
        ("s2", "dim_branch", "province", "Tỉnh/thành", "shared_province", 180),
        ("s3", "dim_branch", "branch_name", "Chi nhánh", "shared_branch", 240),
    ]
    for spec in specifications:
        name, table, field, label, group, y = spec
        path = PAGES_ROOT / page_key / "visuals" / name / "visual.json"
        write_json(path, slicer_visual(name, table, field, label, group, y), apply)


def update_page_name(page_key: str, display_name: str, apply: bool) -> None:
    path = PAGES_ROOT / page_key / "page.json"
    page = load_json(path)
    page["displayName"] = display_name
    write_json(path, page, apply)


def layout_pages(apply: bool) -> None:
    page_titles = {
        "p1": ("Tình hình kinh doanh | Miền Bắc", "Dư nợ cuối kỳ · Doanh thu lũy kế · Kế hoạch và tuân thủ"),
        "p2": ("Kế hoạch và chênh lệch", "Phân rã khoảng cách theo chi nhánh, phân khúc và sản phẩm"),
        "p3": ("Tuân thủ và tiền thưởng", "Theo dõi hạn mức chính sách và quỹ thưởng đủ điều kiện"),
        "p4": ("Chất lượng dữ liệu", "Theo dõi dữ liệu thiếu và trùng trước khi phân tích"),
    }
    page_names = {
        "p1": "Tổng quan",
        "p2": "Kế hoạch và chênh lệch",
        "p3": "Tuân thủ và tiền thưởng",
        "p4": "Chất lượng dữ liệu",
    }

    for page_key, (title, subtitle) in page_titles.items():
        add_shared_chrome(page_key, title, subtitle, apply)
        update_slicers(page_key, apply)
        update_page_name(page_key, page_names[page_key], apply)

    positions = {
        "p1": {
            "c1": (216, 72, 200, 84),
            "c2": (428, 72, 200, 84),
            "c3": (640, 72, 200, 84),
            "c4": (852, 72, 200, 84),
            "c5": (1064, 72, 200, 84),
            "l1": (216, 188, 510, 216),
            "l3": (736, 188, 528, 216),
            "t1": (216, 444, 1048, 256),
        },
        "p2": {
            "b1": (216, 96, 510, 248),
            "m1": (736, 96, 528, 248),
            "t2": (216, 380, 640, 320),
            "b3": (868, 380, 396, 320),
        },
        "p3": {
            "l2": (216, 96, 450, 248),
            "m2": (676, 96, 588, 248),
            "b2": (216, 380, 510, 320),
            "sc1": (736, 380, 528, 320),
        },
        "p4": {
            "q1": (216, 76, 220, 84),
            "q2": (450, 76, 220, 84),
            "t4": (216, 198, 1048, 502),
        },
    }
    titles = {
        "p1": {
            "l1": "Dư nợ theo tháng",
            "l3": "Doanh thu theo tháng",
            "t1": "Hiệu quả theo chi nhánh",
        },
        "p2": {
            "b1": "Doanh thu theo chi nhánh",
            "m1": "Chênh lệch doanh thu theo phân khúc",
            "t2": "Chi tiết theo phân khúc và sản phẩm",
            "b3": "Khoảng cách doanh thu theo phân khúc",
        },
        "p3": {
            "l2": "Tỷ lệ dư nợ không tài sản bảo đảm",
            "m2": "Số tháng vượt hạn mức theo quý",
            "b2": "Quỹ thưởng và điều kiện tuân thủ",
            "sc1": "Hoàn thành doanh thu theo chi nhánh",
        },
        "p4": {"t4": "Chi tiết kiểm tra dữ liệu"},
    }
    card_labels = {
        "c1": "Dư nợ cuối kỳ",
        "c2": "Tăng dư nợ từ đầu năm",
        "c3": "Dư nợ so cùng kỳ",
        "c4": "Doanh thu lũy kế",
        "c5": "Doanh thu so cùng kỳ",
    }

    for page_key, visual_positions in positions.items():
        for visual_key, position in visual_positions.items():
            update_existing_visual(
                page_key,
                visual_key,
                position=position,
                title=titles.get(page_key, {}).get(visual_key),
                card=visual_key.startswith("c") or visual_key.startswith("q"),
                apply=apply,
            )

    section_headers = {
        "p1": [
            ("l1", 216, 164, 510, "Dư nợ kế hoạch và thực tế"),
            ("l3", 736, 164, 528, "Doanh thu kế hoạch và thực tế"),
            ("t1", 216, 420, 1048, "Kết quả theo chi nhánh"),
        ],
        "p2": [
            ("b1", 216, 70, 510, "Doanh thu theo chi nhánh"),
            ("m1", 736, 70, 528, "Chênh lệch theo phân khúc"),
            ("t2", 216, 354, 640, "Chi tiết theo sản phẩm"),
            ("b3", 868, 354, 396, "Khoảng cách theo phân khúc"),
        ],
        "p3": [
            ("l2", 216, 70, 450, "Dư nợ không tài sản bảo đảm"),
            ("m2", 676, 70, 588, "Tháng vượt hạn mức theo quý"),
            ("b2", 216, 354, 510, "Quỹ thưởng đủ điều kiện"),
            ("sc1", 736, 354, 528, "Hoàn thành doanh thu theo chi nhánh"),
        ],
        "p4": [("t4", 216, 172, 1048, "Chi tiết kiểm tra dữ liệu")],
    }
    for page_key, headings in section_headers.items():
        for visual_key, x, y, width, heading in headings:
            name = f"heading_{visual_key}"
            heading_visual = textbox_visual(
                name,
                x,
                y,
                width,
                22,
                [paragraph(heading, 10.0, RED, bold=True)],
                z=10,
            )
            write_json(
                PAGES_ROOT / page_key / "visuals" / name / "visual.json",
                heading_visual,
                apply,
            )

    scatter_path = PAGES_ROOT / "p3" / "visuals" / "sc1" / "visual.json"
    scatter = load_json(scatter_path)
    branch_projection = {
        "field": {
            "Column": {
                "Expression": {"SourceRef": {"Entity": "dim_branch"}},
                "Property": "branch_name",
            }
        },
        "queryRef": "dim_branch.branch_name",
        "nativeQueryRef": "branch_name",
        "displayName": "Chi nhánh",
        "active": True,
    }
    revenue_attainment = {
        "field": {
            "Measure": {
                "Expression": {"SourceRef": {"Entity": "fact_performance"}},
                "Property": "Tỷ lệ HT doanh thu YTD",
            }
        },
        "queryRef": "fact_performance.Tỷ lệ HT doanh thu YTD",
        "nativeQueryRef": "Tỷ lệ HT doanh thu YTD",
        "displayName": "Hoàn thành doanh thu",
    }
    scatter["visual"]["visualType"] = "clusteredBarChart"
    scatter["visual"]["query"]["queryState"] = {
        "Category": {"projections": [branch_projection]},
        "Y": {"projections": [revenue_attainment]},
    }
    scatter["visual"]["objects"] = {"title": properties(show=False)}
    save_visual("p3", "sc1", scatter, apply)

    update_existing_visual(
        "p1",
        "c1",
        display_names={"fact_performance.Dư nợ cuối kỳ": card_labels["c1"]},
        card=True,
        apply=apply,
    )
    update_existing_visual(
        "p1",
        "c2",
        display_names={"fact_performance.Dư nợ tăng YTD": card_labels["c2"]},
        card=True,
        apply=apply,
    )
    update_existing_visual(
        "p1",
        "c3",
        display_names={"fact_performance.Dư nợ tăng YoY": card_labels["c3"]},
        card=True,
        apply=apply,
    )
    update_existing_visual(
        "p1",
        "c4",
        display_names={"fact_performance.Doanh thu YTD": card_labels["c4"]},
        card=True,
        apply=apply,
    )
    update_existing_visual(
        "p1",
        "c5",
        display_names={"fact_performance.Doanh thu tăng YTD YoY": card_labels["c5"]},
        card=True,
        apply=apply,
    )
    update_existing_visual(
        "p1",
        "t1",
        display_names={
            "fact_performance.Tỷ lệ HT dư nợ cuối kỳ": "Hoàn thành dư nợ",
            "fact_performance.Dư nợ tăng QoQ": "Tăng dư nợ quý",
            "fact_performance.Tỷ lệ HT doanh thu YTD": "Hoàn thành doanh thu",
            "fact_performance.Doanh thu tăng YTD YoY": "Tăng doanh thu cùng kỳ",
            "fact_incentive.Điểm KPI trung bình": "Điểm KPI",
            "fact_policy_check.Số tháng vi phạm hạn mức không TSBĐ": "Tháng vi phạm",
        },
        apply=apply,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the layout changes (close Power BI Desktop first)",
    )
    args = parser.parse_args()
    layout_pages(apply=args.apply)
    action = "Applied" if args.apply else "Dry run complete"
    print(f"{action}. Power BI Desktop must be closed before using --apply.")
    print("No existing pages or query definitions are deleted.")


if __name__ == "__main__":
    main()