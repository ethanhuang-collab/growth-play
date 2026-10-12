#!/usr/bin/env python3
"""Render a Clay Quality Assessment document from a structured JSON spec.

Usage
-----
    python generate_docx.py --spec spec.json --out ~/Downloads/report.docx
    cat spec.json | python generate_docx.py --out ~/Downloads/report.docx

The JSON spec schema is documented in references/prompt.md. The brand tokens
applied here come from references/brand_spec.md — they are authoritative and
should not be altered without updating that reference.

The deliverable has five sections in this order, with only the cover on its
own page:

    1. Cover                     — render_cover
    2. Overview                  — render_overview
    3. Flow Logic                — render_flow_logic
    4. Per-Stage Provider Fill   — render_stage_details
       Rates
    5. Coverage & Quality        — render_coverage_table
       (Aggregate Level)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable

try:
    from docx import Document
    from docx.enum.table import WD_ALIGN_VERTICAL
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError:
    sys.stderr.write(
        "python-docx is required. Install with: pip install python-docx\n"
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Brand tokens — mirror references/brand_spec.md exactly.
# ---------------------------------------------------------------------------

NAVY = RGBColor(0x1F, 0x4E, 0x79)
BLUE = RGBColor(0x2E, 0x75, 0xB6)
MID_BLUE = RGBColor(0x2F, 0x54, 0x96)
LIGHT_BLUE_HEX = "EBF3FB"
GRAY = RGBColor(0x59, 0x59, 0x59)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BORDER_HEX = "D0DCE8"
NAVY_HEX = "1F4E79"
BLUE_HEX = "2E75B6"
HEADER_BORDER_HEX = "4472A4"
TOP_BORDER_HEX = NAVY_HEX

FONT_FAMILY = "Arial"

DEFAULT_LOGO = Path(__file__).resolve().parent.parent / "assets" / "Clay_Logo_Icon.png"

BLOCKED_WORDS = [
    r"\bunfortunately\b",
    r"\bhowever only\b",
    r"\bonly\b(?=\s+\d)",   # "only 34%" style
    r"\bneeds improvement\b",
    r"\bbelow target\b",
    r"\bopportunity for improvement\b",
    r"\bshould be improved\b",
    r"\bcould be improved\b",
]
BLOCKED_REGEX = re.compile("|".join(BLOCKED_WORDS), re.IGNORECASE)

BOLD_SPLIT_RE = re.compile(r"(\*\*[^*]+\*\*)")

# Indentation in twips (twentieths of a point) for the income-statement table.
# 260 twips ≈ 0.18 inch — matches the ~one-tab feel called for in the template.
INDENT_TWIPS = 260


@dataclass
class RenderContext:
    doc: Document
    logo_path: Path | None


# ---------------------------------------------------------------------------
# Low-level XML helpers
# ---------------------------------------------------------------------------


def _shade(element, hex_color: str) -> None:
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    element.append(shd)


def _cell_borders(tc, hex_color: str = BORDER_HEX, sz: int = 4,
                   *, top_color: str | None = None, top_sz: int | None = None) -> None:
    tcPr = tc.get_or_add_tcPr()
    existing = tcPr.find(qn("w:tcBorders"))
    if existing is not None:
        tcPr.remove(existing)
    borders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        border = OxmlElement(f"w:{side}")
        border.set(qn("w:val"), "single")
        if side == "top" and top_color is not None:
            border.set(qn("w:sz"), str(top_sz or 12))
            border.set(qn("w:color"), top_color)
        else:
            border.set(qn("w:sz"), str(sz))
            border.set(qn("w:color"), hex_color)
        border.set(qn("w:space"), "0")
        borders.append(border)
    tcPr.append(borders)


def _cell_margin(tc, top=80, bottom=80, left=140, right=140) -> None:
    tcPr = tc.get_or_add_tcPr()
    existing = tcPr.find(qn("w:tcMar"))
    if existing is not None:
        tcPr.remove(existing)
    mar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        mar.append(node)
    tcPr.append(mar)


def _cell_nowrap(tc) -> None:
    tcPr = tc.get_or_add_tcPr()
    node = OxmlElement("w:noWrap")
    tcPr.append(node)


def _cell_fixed_width(cell, dxa: int) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcW = tcPr.find(qn("w:tcW"))
    if tcW is not None:
        tcPr.remove(tcW)
    tcW = OxmlElement("w:tcW")
    tcW.set(qn("w:w"), str(dxa))
    tcW.set(qn("w:type"), "dxa")
    tcPr.append(tcW)


def _set_run_font(run, size_pt: float, *, bold=False, italic=False, color: RGBColor | None = None):
    run.font.name = FONT_FAMILY
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rFonts.set(qn(f"w:{attr}"), FONT_FAMILY)


def _paragraph_spacing(paragraph, *, before=6, after=6, line=1.15):
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE


def _paragraph_left_indent_twips(paragraph, twips: int) -> None:
    """Set the paragraph's left indentation in twips (1/20 of a point)."""
    if twips <= 0:
        return
    pPr = paragraph._p.get_or_add_pPr()
    ind = pPr.find(qn("w:ind"))
    if ind is None:
        ind = OxmlElement("w:ind")
        pPr.append(ind)
    ind.set(qn("w:left"), str(twips))


def _add_horizontal_rule(paragraph, hex_color: str = NAVY_HEX, size: int = 12):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = pPr.find(qn("w:pBdr"))
    if pBdr is None:
        pBdr = OxmlElement("w:pBdr")
        pPr.append(pBdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), hex_color)
    pBdr.append(bottom)


def _paragraph_bottom_border(paragraph, hex_color=NAVY_HEX, size=6):
    _add_horizontal_rule(paragraph, hex_color=hex_color, size=size)


def _add_page_break(doc: Document) -> None:
    p = doc.add_paragraph()
    _paragraph_spacing(p, before=0, after=0, line=1.0)
    run = p.add_run()
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    run._element.append(br)


def _add_page_number_field(paragraph) -> None:
    """Append 'Page X of Y' using Word field codes."""

    def _field_run(text=None):
        return paragraph.add_run(text if text is not None else "")

    def _add_field(code: str):
        fld_begin = OxmlElement("w:fldChar")
        fld_begin.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = code
        fld_sep = OxmlElement("w:fldChar")
        fld_sep.set(qn("w:fldCharType"), "separate")
        fld_end = OxmlElement("w:fldChar")
        fld_end.set(qn("w:fldCharType"), "end")
        run = _field_run()
        run._element.append(fld_begin)
        run._element.append(instr)
        run._element.append(fld_sep)
        run._element.append(fld_end)
        _set_run_font(run, 9, italic=True, color=GRAY)

    r = paragraph.add_run("Page ")
    _set_run_font(r, 9, italic=True, color=GRAY)
    _add_field(" PAGE ")
    r = paragraph.add_run(" of ")
    _set_run_font(r, 9, italic=True, color=GRAY)
    _add_field(" NUMPAGES ")


# ---------------------------------------------------------------------------
# Paragraph + text helpers
# ---------------------------------------------------------------------------


def _add_prose(paragraph, text: str, *, size=11, color=GRAY, base_bold=False):
    """Render prose with **inline bold** segments parsed into separate runs."""
    if not text:
        return
    parts = BOLD_SPLIT_RE.split(text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            _set_run_font(run, size, bold=True, color=color)
        else:
            run = paragraph.add_run(part)
            _set_run_font(run, size, bold=base_bold, color=color)


def _sanitize_prose(text: str) -> str:
    """Apply light automatic cleanup for blocked phrasing."""
    if not text:
        return text
    cleaned = re.sub(r"\bonly\s+(?=\d)", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bjust\s+(?=\d)", "", cleaned, flags=re.IGNORECASE)
    return cleaned


def _warn_if_blocked_words(text: str, location: str) -> None:
    if not text:
        return
    for match in BLOCKED_REGEX.finditer(text):
        sys.stderr.write(
            f"[warn] blocked phrasing in {location}: '{match.group(0)}'\n"
        )


# ---------------------------------------------------------------------------
# Heading + paragraph constructors
# ---------------------------------------------------------------------------


def add_h1(doc: Document, text: str):
    p = doc.add_paragraph()
    _paragraph_spacing(p, before=14, after=8, line=1.15)
    run = p.add_run(text)
    _set_run_font(run, 24, bold=True, color=BLUE)
    _paragraph_bottom_border(p, hex_color=LIGHT_BLUE_HEX, size=8)
    return p


def add_h2(doc: Document, text: str):
    p = doc.add_paragraph()
    _paragraph_spacing(p, before=8, after=4, line=1.15)
    run = p.add_run(text)
    _set_run_font(run, 14, bold=True, color=MID_BLUE)
    return p


def add_body(doc: Document, text: str):
    p = doc.add_paragraph()
    _paragraph_spacing(p, before=6, after=6, line=1.15)
    _add_prose(p, text)
    return p


def add_bullet(doc: Document, text: str, *, level: int = 0):
    """Render a bulleted body line. `level` controls indent (0 or 1)."""
    p = doc.add_paragraph(style="List Bullet")
    _paragraph_spacing(p, before=2, after=2, line=1.15)
    if level > 0:
        _paragraph_left_indent_twips(p, 360 + level * INDENT_TWIPS)
    _add_prose(p, text or "", size=11, color=GRAY)
    return p


# ---------------------------------------------------------------------------
# Generic data table helpers (kept for cover-card / metadata uses if needed)
# ---------------------------------------------------------------------------


def _configure_header_cell(cell, text: str):
    cell.text = ""
    tc = cell._tc
    _shade(tc.get_or_add_tcPr(), NAVY_HEX)
    _cell_borders(tc, hex_color=HEADER_BORDER_HEX, sz=4)
    _cell_margin(tc)
    p = cell.paragraphs[0]
    _paragraph_spacing(p, before=0, after=0, line=1.0)
    run = p.add_run(text)
    _set_run_font(run, 11, bold=True, color=WHITE)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def _add_paragraph_after_table(doc: Document):
    p = doc.add_paragraph()
    _paragraph_spacing(p, before=4, after=4, line=1.0)


# ---------------------------------------------------------------------------
# Page setup, header, footer
# ---------------------------------------------------------------------------


def configure_page(doc: Document):
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        section.different_first_page_header_footer = True


def configure_header_footer(doc: Document, meta: dict[str, Any], logo_path: Path | None):
    section = doc.sections[0]
    header = section.header
    header.is_linked_to_previous = False
    header_p = header.paragraphs[0]
    header_p.clear()
    _paragraph_spacing(header_p, before=0, after=0, line=1.0)
    if logo_path and logo_path.exists():
        run = header_p.add_run()
        try:
            run.add_picture(str(logo_path), width=Inches(0.4))
        except Exception as exc:
            sys.stderr.write(f"[warn] could not embed header logo: {exc}\n")
    header_p.add_run("   ")
    title_run = header_p.add_run(meta.get("documentTitle", ""))
    _set_run_font(title_run, 10, bold=True, color=NAVY)
    _paragraph_bottom_border(header_p, hex_color=NAVY_HEX, size=4)

    footer = section.footer
    footer.is_linked_to_previous = False
    footer_p = footer.paragraphs[0]
    footer_p.clear()
    _paragraph_spacing(footer_p, before=0, after=0, line=1.0)
    from docx.shared import Inches as _Inches
    pf = footer_p.paragraph_format
    tab_stops = pf.tab_stops
    tab_stops.add_tab_stop(_Inches(6.5), alignment=2)  # right-aligned tab
    left_run = footer_p.add_run("Confidential — Clay Professional Services")
    _set_run_font(left_run, 9, italic=True, color=GRAY)
    footer_p.add_run("\t")
    _add_page_number_field(footer_p)

    fp_header = section.first_page_header
    fp_header.is_linked_to_previous = False
    for p in list(fp_header.paragraphs):
        p.clear()
    fp_footer = section.first_page_footer
    fp_footer.is_linked_to_previous = False
    for p in list(fp_footer.paragraphs):
        p.clear()
    fp_footer_p = fp_footer.paragraphs[0]
    _paragraph_spacing(fp_footer_p, before=0, after=0, line=1.0)
    fp_footer_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    fp_left = fp_footer_p.add_run("Confidential — Clay Professional Services")
    _set_run_font(fp_left, 9, italic=True, color=GRAY)


# ---------------------------------------------------------------------------
# Section 1 — Cover
# ---------------------------------------------------------------------------


def render_cover(ctx: RenderContext, spec: dict[str, Any]) -> None:
    doc = ctx.doc
    meta = spec.get("meta", {})

    if ctx.logo_path and ctx.logo_path.exists():
        p = doc.add_paragraph()
        _paragraph_spacing(p, before=0, after=12)
        run = p.add_run()
        try:
            run.add_picture(str(ctx.logo_path), width=Inches(0.75))
        except Exception as exc:
            sys.stderr.write(f"[warn] could not embed cover logo: {exc}\n")

    title = meta.get("documentTitle") or f"{meta.get('clientName', 'Client')} × Clay"
    p = doc.add_paragraph()
    _paragraph_spacing(p, before=48, after=6)
    run = p.add_run(title)
    _set_run_font(run, 36, bold=True, color=NAVY)

    project = meta.get("projectName") or ""
    if project:
        p = doc.add_paragraph()
        _paragraph_spacing(p, before=0, after=6)
        run = p.add_run(project)
        _set_run_font(run, 24, bold=True, color=BLUE)

    subtitle = meta.get("subtitle") or "Quality Assessment — Workflow Performance Review"
    p = doc.add_paragraph()
    _paragraph_spacing(p, before=0, after=12)
    run = p.add_run(subtitle)
    _set_run_font(run, 14, italic=True, color=GRAY)

    rule = doc.add_paragraph()
    _paragraph_spacing(rule, before=0, after=16)
    _paragraph_bottom_border(rule, hex_color=NAVY_HEX, size=12)

    _add_page_break(doc)


# ---------------------------------------------------------------------------
# Section 2 — Overview (prose only)
# ---------------------------------------------------------------------------


def render_overview(ctx: RenderContext, spec: dict[str, Any]) -> None:
    doc = ctx.doc
    overview = spec.get("overview") or {}
    if not overview:
        return
    add_h1(doc, "1. Overview")
    prose = overview.get("prose") or ""
    prose = _sanitize_prose(prose)
    _warn_if_blocked_words(prose, "overview.prose")
    if prose:
        add_body(doc, prose)
    multi_note = overview.get("multiTableNote") or ""
    if multi_note:
        p = doc.add_paragraph()
        _paragraph_spacing(p, before=2, after=8, line=1.15)
        run = p.add_run(multi_note)
        _set_run_font(run, 10, italic=True, color=GRAY)


# ---------------------------------------------------------------------------
# Section 3 — Flow Logic (no providers, no fill rates, no costs)
# ---------------------------------------------------------------------------


def render_flow_logic(ctx: RenderContext, spec: dict[str, Any]) -> None:
    doc = ctx.doc
    fl = spec.get("flowLogic") or {}
    steps = fl.get("steps") or []
    if not steps:
        return
    add_h1(doc, "2. Flow Logic")
    intro = fl.get("intro") or ""
    intro = _sanitize_prose(intro)
    _warn_if_blocked_words(intro, "flowLogic.intro")
    if intro:
        add_body(doc, intro)
    for i, step in enumerate(steps):
        number = step.get("stageNumber", i + 1)
        name = step.get("stageName") or f"Stage {number}"
        description = step.get("description") or ""
        description = _sanitize_prose(description)
        _warn_if_blocked_words(description, f"flowLogic.steps[{i}].description")
        # "Stage N — Stage Name" bold lead-in followed by description
        p = doc.add_paragraph(style="List Number")
        _paragraph_spacing(p, before=4, after=4, line=1.15)
        lead = p.add_run(f"{name}")
        _set_run_font(lead, 11, bold=True, color=NAVY)
        if description:
            tail = p.add_run(f" — {description}")
            _set_run_font(tail, 11, color=GRAY)


# ---------------------------------------------------------------------------
# Section 4 — Per-Stage Provider Fill Rates (no costs)
# ---------------------------------------------------------------------------


def render_stage_details(ctx: RenderContext, spec: dict[str, Any]) -> None:
    doc = ctx.doc
    sd = spec.get("stageDetails") or {}
    stages = sd.get("stages") or []
    if not stages:
        return
    add_h1(doc, "3. Per-Stage Provider Fill Rates")
    intro = sd.get("intro") or (
        "The list below expands each stage above into the providers that powered it, "
        "with the fill rate observed for each. Costs appear in Section 4."
    )
    intro = _sanitize_prose(intro)
    _warn_if_blocked_words(intro, "stageDetails.intro")
    add_body(doc, intro)

    for i, stage in enumerate(stages):
        number = stage.get("stageNumber", i + 1)
        name = stage.get("stageName") or f"Stage {number}"
        is_waterfall = bool(stage.get("waterfall"))
        heading = f"Stage {number} — {name}"
        if is_waterfall:
            heading += "  (waterfall — first provider absolute, subsequent are incremental)"
        # Use a smaller H2 for stage labels here so they read like sub-headers
        p = doc.add_paragraph()
        _paragraph_spacing(p, before=10, after=2, line=1.15)
        run = p.add_run(heading)
        _set_run_font(run, 12, bold=True, color=MID_BLUE)

        providers = stage.get("providers") or []
        for j, prov in enumerate(providers):
            pname = prov.get("name") or ""
            fill = prov.get("fillRate") or ""
            line = f"**{pname}** — fill rate **{fill}**" if fill else f"**{pname}**"
            add_bullet(doc, line)


# ---------------------------------------------------------------------------
# Section 5 — Coverage & Quality (the income-statement table)
# ---------------------------------------------------------------------------


def _add_indented_label_run(cell, text: str, *, indent_level: int, bold: bool, color: RGBColor):
    """Render a left-column label paragraph with accounting-style indent."""
    p = cell.paragraphs[0] if not cell.paragraphs[0].text else cell.add_paragraph()
    # Use the existing paragraph if it's still empty.
    p = cell.paragraphs[0]
    p.text = ""
    _paragraph_spacing(p, before=0, after=0, line=1.0)
    _paragraph_left_indent_twips(p, indent_level * INDENT_TWIPS)
    run = p.add_run(text or "")
    _set_run_font(run, 11, bold=bold, color=color)


def _configure_coverage_cell(cell, text: str, *,
                              row_kind: str,
                              indent_level: int = 0,
                              align_right: bool = False,
                              top_border: bool = False) -> None:
    """Configure a single cell in the Section 5 coverage table.

    `row_kind` controls weight, color, and shading:
      - "group_header": bold navy on light-blue band
      - "provider":     regular gray on white
      - "blended":      regular gray on white, italic-tinted via mid-blue,
                         indented one extra level (indent_level passed in)
      - "final":        same visual rules as `blended`, but with a top border
    """
    cell.text = ""
    tc = cell._tc
    if row_kind == "group_header":
        fill = LIGHT_BLUE_HEX
        text_color = NAVY
        bold = True
    elif row_kind == "provider":
        fill = "FFFFFF"
        text_color = GRAY
        bold = False
    elif row_kind == "blended":
        fill = "FFFFFF"
        text_color = MID_BLUE
        bold = False
    elif row_kind == "final":
        fill = "FFFFFF"
        text_color = NAVY
        bold = False
    else:
        fill = "FFFFFF"
        text_color = GRAY
        bold = False
    _shade(tc.get_or_add_tcPr(), fill)
    if top_border:
        _cell_borders(tc, hex_color=BORDER_HEX, sz=4, top_color=TOP_BORDER_HEX, top_sz=12)
    else:
        _cell_borders(tc, hex_color=BORDER_HEX, sz=4)
    _cell_margin(tc, top=60, bottom=60, left=120, right=120)

    p = cell.paragraphs[0]
    p.text = ""
    _paragraph_spacing(p, before=0, after=0, line=1.0)
    if indent_level > 0:
        _paragraph_left_indent_twips(p, indent_level * INDENT_TWIPS)
    if align_right:
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(text or "")
    _set_run_font(run, 11, bold=bold, color=text_color)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def render_coverage_table(ctx: RenderContext, spec: dict[str, Any]) -> None:
    doc = ctx.doc
    ct = spec.get("coverageTable") or {}
    groups = ct.get("groups") or []
    final = ct.get("finalDelivery") or {}
    if not groups and not final:
        return
    add_h1(doc, "4. Coverage & Quality (Aggregate Level)")
    # Build row plan first so we know total row count and whether any row carries
    # effectiveCredits (per-row cost). When effectiveCredits is present we render
    # a 4-column table that splits "per call" from "per row" — the per-row number
    # is what actually shows up on the bill once refund-on-no-data policies and
    # observed fill rates are factored in.
    row_plan: list[dict[str, Any]] = []
    has_effective = False
    for g in groups:
        label = g.get("label") or g.get("stageName") or "Stage"
        row_plan.append({"kind": "group_header", "label": label})
        for prov in (g.get("providers") or []):
            eff = prov.get("effectiveCredits")
            if eff not in (None, ""):
                has_effective = True
            row_plan.append({
                "kind": "provider",
                "label": prov.get("name") or "",
                "fillRate": prov.get("fillRate") or "",
                "credits": prov.get("credits") or "",
                "effectiveCredits": eff if eff not in (None, "") else "",
            })
        blended = g.get("blended") or {}
        if blended:
            eff = blended.get("effectiveCredits")
            if eff not in (None, ""):
                has_effective = True
            row_plan.append({
                "kind": "blended",
                "label": blended.get("label") or f"{label} — blended",
                "fillRate": blended.get("fillRate") or "",
                "credits": blended.get("credits") or "",
                "effectiveCredits": eff if eff not in (None, "") else "",
            })

    if final:
        eff = final.get("effectiveCredits")
        if eff not in (None, ""):
            has_effective = True
        row_plan.append({
            "kind": "final",
            "label": final.get("label") or "Final Delivery",
            "fillRate": final.get("fillRate") or "",
            "credits": final.get("credits") or "",
            "effectiveCredits": eff if eff not in (None, "") else "",
            "topBorder": True,
        })

    if has_effective:
        intro = ct.get("intro") or (
            "The table below combines per-provider fill rate with the actual per-row "
            "Clay credit cost, grouped by stage like an income statement. Per-call "
            "credits show Clay's published rate; per-row credits reflect what each "
            "call actually costs once refund-on-no-data policies and observed fill "
            "rates are factored in. The Final Delivery row is the last row in the table."
        )
    else:
        intro = ct.get("intro") or (
            "The table below combines per-provider fill rate with per-call Clay credit cost, "
            "grouped by stage like an income statement. Group blended rows weight per-call "
            "credits by each provider's incremental hit rate. The Final Delivery row is the "
            "last row in the table."
        )
    intro = _sanitize_prose(intro)
    _warn_if_blocked_words(intro, "coverageTable.intro")
    add_body(doc, intro)

    # Header row + body rows. 4 columns when effectiveCredits is present, else 3
    # (back-compat with older spec output).
    if has_effective:
        n_cols = 4
        headers = ["Section / Provider", "Fill Rate", "Per Call (credits)", "Per Row (credits)"]
    else:
        n_cols = 3
        headers = ["Section / Provider", "Fill Rate", "Cost (Clay credits)"]

    table = doc.add_table(rows=1 + len(row_plan), cols=n_cols)
    # Force fixed table layout so the table fills the full content width
    # (8.5" page - 2 x 1" margins = 6.5" = 9360 dxa) instead of shrinking to
    # the autofit-preferred width of its content.
    table.autofit = False
    table.allow_autofit = False
    tbl = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    # Remove any existing width / layout nodes so we own them.
    for tag in ("w:tblW", "w:tblLayout"):
        existing = tblPr.find(qn(tag))
        if existing is not None:
            tblPr.remove(existing)
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), "9360")
    tblW.set(qn("w:type"), "dxa")
    tblPr.append(tblW)
    tblLayout = OxmlElement("w:tblLayout")
    tblLayout.set(qn("w:type"), "fixed")
    tblPr.append(tblLayout)

    for c, header in enumerate(headers):
        _configure_header_cell(table.rows[0].cells[c], header)
    # Right-hand numeric columns stay tight; the label column takes the
    # remaining width so the table spans the full margin-to-margin run.
    if n_cols == 4:
        right_widths = [1300, 1700, 1700]
    else:
        right_widths = [1300, 1700]
    label_width = 9360 - sum(right_widths)
    for row in table.rows:
        _cell_fixed_width(row.cells[0], label_width)
        for offset, w in enumerate(right_widths, start=1):
            _cell_fixed_width(row.cells[offset], w)

    for r_idx, plan in enumerate(row_plan, start=1):
        kind = plan["kind"]
        label = plan["label"]
        fill = plan.get("fillRate", "")
        credits = plan.get("credits", "")
        eff_credits = plan.get("effectiveCredits", "")
        top_border = plan.get("topBorder", False)
        if kind == "group_header":
            _configure_coverage_cell(table.rows[r_idx].cells[0], label,
                                      row_kind="group_header", indent_level=0)
            _configure_coverage_cell(table.rows[r_idx].cells[1], "",
                                      row_kind="group_header", align_right=True)
            _configure_coverage_cell(table.rows[r_idx].cells[2], "",
                                      row_kind="group_header", align_right=True)
            if n_cols == 4:
                _configure_coverage_cell(table.rows[r_idx].cells[3], "",
                                          row_kind="group_header", align_right=True)
        elif kind == "provider":
            _configure_coverage_cell(table.rows[r_idx].cells[0], label,
                                      row_kind="provider", indent_level=1)
            _configure_coverage_cell(table.rows[r_idx].cells[1], fill,
                                      row_kind="provider", align_right=True)
            _configure_coverage_cell(table.rows[r_idx].cells[2], credits,
                                      row_kind="provider", align_right=True)
            if n_cols == 4:
                _configure_coverage_cell(table.rows[r_idx].cells[3], eff_credits,
                                          row_kind="provider", align_right=True)
        elif kind == "blended":
            _configure_coverage_cell(table.rows[r_idx].cells[0], label,
                                      row_kind="blended", indent_level=2)
            _configure_coverage_cell(table.rows[r_idx].cells[1], fill,
                                      row_kind="blended", align_right=True)
            _configure_coverage_cell(table.rows[r_idx].cells[2], credits,
                                      row_kind="blended", align_right=True)
            if n_cols == 4:
                _configure_coverage_cell(table.rows[r_idx].cells[3], eff_credits,
                                          row_kind="blended", align_right=True)
        elif kind == "final":
            _configure_coverage_cell(table.rows[r_idx].cells[0], label,
                                      row_kind="final", indent_level=2,
                                      top_border=top_border)
            _configure_coverage_cell(table.rows[r_idx].cells[1], fill,
                                      row_kind="final", align_right=True,
                                      top_border=top_border)
            _configure_coverage_cell(table.rows[r_idx].cells[2], credits,
                                      row_kind="final", align_right=True,
                                      top_border=top_border)
            if n_cols == 4:
                _configure_coverage_cell(table.rows[r_idx].cells[3], eff_credits,
                                          row_kind="final", align_right=True,
                                          top_border=top_border)

    _add_paragraph_after_table(doc)

    footnote = ct.get("footnote") or ""
    if footnote:
        p = doc.add_paragraph()
        _paragraph_spacing(p, before=2, after=8, line=1.15)
        run = p.add_run(footnote)
        _set_run_font(run, 9, italic=True, color=GRAY)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def render_document(spec: dict[str, Any], out_path: Path, logo_path: Path | None) -> Path:
    doc = Document()
    configure_page(doc)

    style = doc.styles["Normal"]
    style.font.name = FONT_FAMILY
    style.font.size = Pt(11)
    style.font.color.rgb = GRAY
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rFonts.set(qn(f"w:{attr}"), FONT_FAMILY)

    configure_header_footer(doc, spec.get("meta", {}), logo_path)

    ctx = RenderContext(doc=doc, logo_path=logo_path)

    render_cover(ctx, spec)            # Section 1 — own page
    render_overview(ctx, spec)         # Section 2
    render_flow_logic(ctx, spec)       # Section 3
    render_stage_details(ctx, spec)    # Section 4
    render_coverage_table(ctx, spec)   # Section 5

    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(out_path)
        return out_path
    except (PermissionError, OSError) as primary_exc:
        fallback = Path.home() / out_path.name
        sys.stderr.write(
            f"[warn] cannot write {out_path} ({primary_exc}); falling back to {fallback}\n"
        )
        try:
            doc.save(fallback)
            return fallback
        except (PermissionError, OSError) as fallback_exc:
            tmp_fallback = Path("/tmp") / out_path.name
            sys.stderr.write(
                f"[warn] cannot write {fallback} ({fallback_exc}); falling back to {tmp_fallback}\n"
            )
            doc.save(tmp_fallback)
            return tmp_fallback


def _default_output_path(spec: dict[str, Any]) -> Path:
    meta = spec.get("meta", {})
    client = (meta.get("clientName") or "client").lower()
    client = re.sub(r"[^a-z0-9]+", "-", client).strip("-") or "client"
    today = meta.get("generatedDate") or date.today().isoformat()
    return Path.home() / "Downloads" / f"clay-qa-{client}-{today}.docx"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", type=Path, default=None,
                        help="Path to JSON spec. If omitted, reads from stdin.")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output .docx path. Defaults to ~/Downloads/clay-qa-{client}-{date}.docx")
    parser.add_argument("--logo", type=Path, default=DEFAULT_LOGO,
                        help="Path to the Clay logo PNG. Defaults to the skill's bundled logo.")
    args = parser.parse_args(argv)

    if args.spec is not None:
        spec_text = args.spec.read_text(encoding="utf-8")
    else:
        spec_text = sys.stdin.read()

    if not spec_text.strip():
        sys.stderr.write("No JSON spec provided via --spec or stdin.\n")
        return 2

    try:
        spec = json.loads(spec_text)
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"Invalid JSON spec: {exc}\n")
        return 2

    if "conflicts" in spec and "meta" not in spec:
        sys.stderr.write(
            "Received a conflicts object instead of a document spec. Surface the "
            "conflicts to the user and re-invoke generation after they are resolved.\n"
        )
        sys.stdout.write(json.dumps(spec, indent=2))
        return 3

    logo = args.logo if args.logo and args.logo.exists() else None
    if args.logo and not args.logo.exists():
        sys.stderr.write(f"[warn] logo not found at {args.logo}; continuing without it.\n")

    out_path = args.out or _default_output_path(spec)
    final_path = render_document(spec, out_path, logo)

    print(str(final_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
