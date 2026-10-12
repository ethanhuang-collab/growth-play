# Brand Specification

This skill produces documents that match the Clay Professional Services visual system shared with the `clay-handoff-doc-generator` skill. All values below are authoritative; the renderer script must apply them exactly.

## Colors (hex)

| Token | Hex | Use |
|---|---|---|
| **Navy** | `1F4E79` | H1 / cover title, part banners, table header fills, horizontal rules |
| **Blue** | `2E75B6` | H2 headings, bold label text in label cards, column headers |
| **Mid Blue** | `2F5496` | Stage subheadings in the Pipeline Walkthrough |
| **Light Blue** | `EBF3FB` | Alternating table row fill, label-table left-column fill |
| **Gray** | `595959` | Body copy (all prose) |
| **White** | `FFFFFF` | Header text on navy fills |
| **Border** | `D0DCE8` | All data table borders, 1pt single |

## Typography

- **Font family:** Arial throughout. No exceptions. No fallback stacks.
- **Never use ALL CAPS** for any heading, banner, label, or table header.
- All headings use **Title Case** ("Pipeline Walkthrough", not "PIPELINE WALKTHROUGH" or "pipeline walkthrough").

| Role | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Cover title (Client × Clay) | 36pt | Bold | Navy `1F4E79` | Centered or left-aligned |
| Project name (cover) | 24pt | Bold | Blue `2E75B6` | Below cover title |
| Subtitle (cover) | 14pt | Italic | Gray `595959` | "Quality Assessment — Workflow Performance Review" |
| H1 / Section number | 24pt | Bold | Blue `2E75B6` | Bottom border in Light Blue `EBF3FB` |
| H2 / Stage heading | 18pt | Bold | Mid Blue `2F5496` | Italic optional |
| Body | 11pt | Regular | Gray `595959` | Line spacing 1.15 |
| Inline bold percentages | 11pt | Bold | Gray `595959` | Same color as surrounding prose |
| Table header text | 11pt | Bold | White `FFFFFF` | On navy fill |
| Table body text | 11pt | Regular | Gray `595959` | |
| Label column (label cards) | 11pt | Bold | Blue `2E75B6` | On Light Blue fill |
| Footer / confidential line | 9pt | Italic | Gray `595959` | |

Note: the handoff generator uses larger point sizes (20pt body, 24pt H2, etc.). This quality assessment document uses standard business-document sizing (11pt body). If you are adapting from the handoff brand spec, scale down.

## Tables

- **Header row:** navy `1F4E79` fill, white bold text, border `4472A4` 1pt.
- **Data rows:** alternating white and Light Blue `EBF3FB`. First data row white.
- **All data borders:** `D0DCE8` 1pt single.
- **Cell padding (DXA):** top 80, bottom 80, left 140, right 140.
- **Label-style tables (cover card, scope card, output card):** left column Light Blue `EBF3FB` fill with bold blue label text; right column white fill with gray body text.
- **Width distribution:** fixed columns (like the "#" column in numbered tables) should be 600 DXA (≈ 1 inch) minimum with `noWrap: true`. Remaining width distributes evenly across other columns.

## Page Setup

- **Margins:** 1 inch top/bottom, 1 inch left/right.
- **Page size:** US Letter (8.5" × 11").
- **Line spacing:** 1.15 for body, 1.0 for table cells.
- **Paragraph spacing:** 6pt before/after body paragraphs; 12pt before an H1; 8pt before an H2.

## Logo

- **File:** `assets/Clay_Logo_Icon.png` (shipped with the skill).
- **Cover page:** left-aligned above the title, approximately 72×54 px (0.75" × 0.56" at 96 DPI).
- **Document header (every page):** left-aligned at approximately 36×27 px (0.375" × 0.28" at 96 DPI) alongside the document title text.

## Cover Page Layout (top to bottom)

1. Clay logo (left-aligned, ~72×54 px)
2. Title: "{Client} × Clay" (36pt navy bold)
3. Project name (24pt blue bold)
4. Subtitle: "Quality Assessment — Workflow Performance Review" (italic gray)
5. Horizontal rule (navy `1F4E79` 6pt thickness)
6. Metadata label table (Client · Project · Table · Row Count · Stages · Document Type)
7. Confidential footer line (italic gray 9pt): "Confidential — Clay Professional Services"

## Document Header (every page after cover)

- **Left:** Clay logo small + document title string ("{Client} × Clay — Quality Assessment")
- **Right:** nothing
- **Bottom border:** navy `1F4E79` 1pt single line separating header from content

## Document Footer (every page after cover)

- **Left:** "Confidential — Clay Professional Services"
- **Right:** "Page X of Y" using Word field codes (`PAGE` and `NUMPAGES` — not string constants)
- **Top border:** navy `1F4E79` 1pt single line separating footer from content
- **Font:** 9pt italic gray `595959`

## Section Formatting Rules

- **Project Overview:** H1 "Project Overview", body prose, then label card.
- **Pipeline Walkthrough:** H1 "Pipeline Walkthrough", intro prose (2 sentences), then one H2 per stage. Each stage: H2 "Stage N — {Name}", body prose (with bolded inline percentages), optional waterfall table.
- **SOW Scope Mapping:** H1 "SOW Scope Mapping", intro prose (1 sentence), then a data table.
- **Output Summary:** H1 "Output Summary", body prose, then label card.

## Column Header Rules — Global

Use exact headers. Do not substitute "Step", "Layer", "No.", "Item", or all-caps variants.

| Section | Headers |
|---|---|
| Cover & scope label cards | *(label / value — no headers shown)* |
| Waterfall table | `Provider · Contribution · Running Total` |
| SOW Scope Mapping | `Deliverable · Columns · Fill Rate` |
| Output metrics card | *(label / value — no headers shown)* |

## Anti-Deviation Rules

- No ALL CAPS anywhere
- No emojis in body, headers, or table cells
- No red/yellow/green coloring of data
- No charts or graphs (this document is a written walkthrough, not a dashboard)
- No color other than the defined tokens
- No font other than Arial
