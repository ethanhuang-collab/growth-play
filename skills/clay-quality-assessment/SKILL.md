---
name: clay-quality-assessment
description: >-
  Generate a branded, client-facing quality assessment document for a Clay.com
  workflow by combining three inputs (CSV export, condensed schema JSON, and
  Statement of Work). Produces a five-section Word document — Cover, Overview,
  Flow Logic, Per-Stage Provider Fill Rates, and a single income-statement-style
  Coverage & Quality table — where Clay credit costs only appear in the final
  table. Use when the user asks to assess Clay workflow quality, check fill
  rates, create a Clay QA document, or deliver a client-facing report on
  enrichment performance.
status: active
---

# Clay Quality Assessment

A self-contained skill that turns three files into a polished, client-facing quality assessment document. The user drops files in; a branded Word document comes out. The document walks through the enrichment pipeline in execution order, reporting raw fill rates inline as facts — no scores, no recommendations, no benchmark comparisons.

The deliverable has **five sections**, with only the cover sitting on its own page. Sections 2–5 flow continuously. Clay credit costs appear in **only one place**: the consolidated coverage table in Section 5.

## Inputs (all three required)

Resolve all bundled paths from this skill directory, regardless of whether the
skill was loaded through Foundations, Claude, Cursor, or Codex. Do not assume a
tool-native install location.

1. **CSV** — Clay table export. Source of truth for numbers (fill rates, value distributions, waterfall contributions). Format: standard CSV with headers in row 1. Can be large (50K+ rows); the skill processes it column-by-column.

2. **Schema** — condensed Clay schema. Source of truth for the narrative (pipeline order, provider names, waterfall structure, formula logic, conditional gates). Accepts **either** shape:
   - A single condensed JSON file (from the extension's **Extract Condensed** button), **or**
   - A folder of chunked JSON files (from **Extract Chunked** — e.g. `Q/`) containing a manifest, summary, prompts, and `chunkIndex`-tagged column chunks.

   Both shapes are normalized by the bundled loader at `scripts/load_schema.py`. The hand-off doc skill consumes the exact same shape — you can use the same input for both skills without any pre-processing:

   ```bash
   cd /path/to/clay-quality-assessment
   python3 scripts/load_schema.py path/to/folder-or-file --out /tmp/schema.json
   ```

3. **Statement of Work** — plain text, `.docx`, or `.pdf`. Defines project scope, success criteria, and deliverables. Use as the anchor for the document's framing.

Optional overrides:
- **Client name** — default is inferred from the SOW. Override if needed.
- **Output path** — default is `~/Downloads/clay-qa-{client}-{YYYY-MM-DD}.docx`.

## Output

A branded `.docx` saved to `~/Downloads/`. Uses the same visual system as the companion `clay-handoff-doc-generator` skill: navy `1F4E79` and blue `2E75B6` headers, Arial throughout, Clay logo on cover and every page header.

## Workflow

### Step 1 — Validate and locate inputs

Confirm all three files exist and are readable. If any is missing, ask the user to provide it. Do not attempt to generate a document with fewer than three inputs.

If the user points at a folder or drops multiple files matching the same input type (e.g. two SOWs), list the candidates and ask which to use. Never pick silently.

### Step 2 — Parse the schema

Read the schema JSON. Build a map of columns by name → metadata. Extract:

- `columns[]` with index, name, type (text/formula/action/source/number)
- Per-column: `dependencies`, `dependents`, `conditionalRun`, `inputParams`, `outputFields`, `promptPurpose`, `formulaText`, `formulaType`, `waterfallEntries`
- `emailWaterfallProviders` (if present) — the canonical cascade order
- `tableName`, `columnCount`, `viewFilters`
- `pricing` (optional) — when present, contains `perColumn[]` (deterministic credit cost per column from Clay's live `/v3/actions` and `/v3/model-pricing` APIs, fetched at extraction time) and `totals` (`creditsPerRow`, `columnsPriced`, `columnsUnpriced`). Each `perColumn` entry also carries `refundOnNoData` (true when the action's `refundRules.SUCCESS_NO_DATA` is set, i.e. Clay refunds the credit when the call returns no data) and — when fill rates are available at extract time — `fillRate` (0–1) and `effectiveCredits` (= `credits` if `refundOnNoData` is false, else `credits × fillRate`). `totals` then also includes `effectiveCreditsPerRow`, `columnsWithFillRate`, and `effectiveColumnsCounted`, representing the realistic per-row credit spend after refund-on-no-data policies and observed fill rates are factored in. This is the source of truth for the credit-cost summary section. If absent, fall back to published rates (see prompt). Surfaced into the chunked export as a separate `pricing.json` file with totals also echoed in the chunk manifest.

Build the pipeline execution order by topological sort of `dependencies`. This is the stage sequence the document will walk through.

### Step 3 — Process the CSV

Follow [references/csv_processing.md](references/csv_processing.md) for the streaming + matching algorithm. The essentials:

1. Read the CSV header row to enumerate columns.
2. Stream each row, counting filled vs. empty cells per column. Do not load all rows into memory.
3. Fuzzy-match CSV column names to schema column names (normalize whitespace, strip Clay-added suffixes like ` (2)`, use Levenshtein similarity ≥ 0.85).
4. For waterfall columns identified in the schema, compute per-provider incremental contribution by walking the provider columns in schema-defined order and tallying "first provider that filled" for each row.
5. For score/categorical columns, tally the value distribution.
6. For columns gated by `conditionalRun`, compute fill rate over *eligible rows* (rows where the gate passes), not total rows. Note both numbers.

Output of this step: a structured JSON object (`metrics.json`) holding `perColumn` fill rates, `waterfallContributions`, `valueDistributions`, and `rowCount` — saved to a temp location for the next step.

### Step 4 — Parse the SOW

Extract:
- Client name, project name
- Objective (verbatim)
- Phase descriptions and deliverables
- Countries / segments / verticals in scope (if any)
- Success metrics if stated (may be absent)

For `.docx`, read via `python-docx`. For `.pdf`, use `pdftotext` (macOS: `pdftotext file.pdf -`). For `.txt`, read directly.

### Step 5 — Generate the document spec

Using the prompt in [references/prompt.md](references/prompt.md), the AI produces a structured JSON document spec with sections, prose, and tables. Input context: the schema, the computed metrics, the parsed SOW, and the brand spec.

The document format is locked to the pipeline walkthrough structure described in [references/document_template.md](references/document_template.md). Do not deviate.

### Step 6 — Render the Word document

Before rendering, validate the AI output:

- **Invalid JSON** — strip any leading/trailing prose or markdown code fences and retry `json.loads()` once. If it still fails, show the raw output and ask the user to retry; do not render.
- **Conflicts object** — if the AI returns `{"conflicts": [...]}` instead of a document spec (see [references/prompt.md](references/prompt.md)), surface the conflicts to the user in plain language and ask them to resolve before re-invoking. The renderer script also short-circuits on this shape with exit code 3.
- **Stage count sanity** — if `flowLogic.steps` (or equivalently `stageDetails.stages`) has fewer than 2 or more than 12 entries, render anyway but log a warning. Don't retry automatically.
- **Stage name parity** — `flowLogic.steps[].stageName`, `stageDetails.stages[].stageName`, and `coverageTable.groups[].label` must match across sections.
- **Cost segregation** — confirm no fill rates or credits appear in `overview.prose` or `flowLogic.*`, and no credits appear in `stageDetails.*`. The renderer doesn't enforce this; the prompt does.

Then run [scripts/generate_docx.py](scripts/generate_docx.py) with the document spec. The script applies the brand (colors, fonts, logo, spacing) described in [references/brand_spec.md](references/brand_spec.md) and writes the `.docx` to the output path.

### Step 7 — Report

Tell the user where the document was saved. Include a one-line summary of table size, stage count, and completion.

## Document Structure

A flowing, client-facing narrative. **Five sections** in order — only the cover is on its own page; sections 2–5 flow continuously.

1. **Cover Page** — Clay logo, "{Client} × Clay — {Project}", subtitle, navy rule, confidential footer. No metadata table.
2. **Overview** — 3–6 sentences describing what the table is meant to do (per the SOW) and the key business outcome. **No fill rates. No providers. No costs.**
3. **Flow Logic** — high-level A → B → C → … of the pipeline as a numbered list of stage names with a one-sentence description each. **Conceptual only — no providers, no fill rates, no costs.**
4. **Per-Stage Provider Fill Rates** — same stage list as Section 3, each expanded into a bulleted list of providers with the fill rate observed for each. For waterfall stages, providers are listed in schema-defined order with the first showing absolute fill rate (`41%`) and subsequent providers showing incremental contribution (`+18%`). **No costs in this section.**
5. **Coverage & Quality (Aggregate Level)** — one income-statement-style table that is the **only** place Clay credit costs appear. Columns: `Section / Provider`, `Fill Rate`, `Per Call (credits)`, `Per Row (credits)` when `pricing` carries `effectiveCredits`; otherwise the legacy 3-column `Section / Provider`, `Fill Rate`, `Cost (Clay credits)` layout. The `Per Row` column is the realistic per-row spend — for refund-on-no-data providers it collapses to `credits × fillRate`; for charge-on-no-result providers it equals the per-call rate. Rows follow accounting indentation:
   - **Group headers** (e.g. "Source ingestion") — bold, no fill / cost values
   - **Provider rows** — indented one level under their group, regular weight
   - **Group blended rows** ("X — blended") — indented two levels, **not bolded**, with credits weighted by each provider's incremental hit rate
   - **Final Delivery** — the last row in the table, indented to the blended-row level, separated by a top border, **not bolded**

Explicitly excluded from the document:
- Numerical quality scores
- Recommendations or "next steps"
- Risk callouts or "gaps"
- Benchmark comparisons ("above industry average", etc.)
- Traffic-light / red-yellow-green coding
- Any language that implies the workflow is incomplete or underperforming
- Clay credit costs anywhere outside the Section 5 coverage table
- Provider names or fill rates anywhere in Sections 2 or 3

Every percentage is a raw fact. The reader draws their own conclusions.

### Cost Calculation (Section 5 only)

- **Per-call credits** for each provider come from the schema's `pricing.perColumn[].credits` when present (live values from Clay's `/v3/actions` and `/v3/model-pricing`). Fall back to the companion hand-off skill's `references/enrichment_credits.json` keyed by `actionKey` only when the schema has no pricing block. When both skills are installed from Foundations, that file is available at `../clay-handoff-doc-generator/references/enrichment_credits.json` relative to this skill directory; otherwise locate the companion skill first and resolve the file from that folder. For free formula / source-table steps, use `0`.
- **Effective per-row credits** for a single provider come from `pricing.perColumn[].effectiveCredits` when present. The extension computes this as `credits × fillRate` when `refundOnNoData` is true (Clay refunds the call on no-data, so you only pay for hits) and as `credits` when `refundOnNoData` is false (provider bills on every attempt, including misses). When the extension didn't have a fill rate at extract time, the prompt computes `effectiveCredits` the same way using the CSV-derived per-column fill rate.
- **Blended group cost** (the "X — blended" row) is computed as `Σ over providers of (incremental hit rate × per-call credits)` for the legacy per-call view, **and** as `Σ over providers of effectiveCredits` for the per-row view. For a waterfall where Findymail (refundOnNoData=true) contributes 41% at 1 credit, Hunter (refundOnNoData=true) +18% at 1 credit, and Prospeo (refundOnNoData=false) +9% at 0.25 credits, the blended per-row row is `0.41×1 + 0.18×1 + 0.25 = 0.84 credits/row` (Prospeo charges every attempt, so its full 0.25 lands regardless of fill rate).
- **Final Delivery cost** is the sum of the per-stage blended values for whichever column is being rendered (`credits` or `effectiveCredits`). When `pricing.totals.effectiveCreditsPerRow` is present, use it directly for the Final Delivery `effectiveCredits` cell.

## Fill Rate Conventions

- **Fill rate** = `filled / total`, where "filled" means the cell has non-empty text (not `null`, not `""`, not whitespace-only).
- **Eligible fill rate** — for columns with `conditionalRun`, report `filled / eligible` where eligible is the count of rows where the gate passes. State both denominators in the document: "verified on **72%** of the 1,840 eligible rows (40% of total)."
- **Waterfall contribution** — for each provider in a waterfall, the share of *previously-empty* rows that this provider filled. Running total across the waterfall = final waterfall fill rate.
- **Value distribution** — for score/category columns, report as `{value: count, percentage}`. Do not compute a "fill rate" for a score column since every row has a value.
- **Excluded columns** — system fields (`created_at`, `updated_at`, `id`, `_internal_*`), the primary key column, and date/timestamp columns are excluded from fill rate metrics but may appear in the pipeline narrative.

See [references/edge_cases.md](references/edge_cases.md) for the full list of edge cases and how each is handled.

## Brand & Tone

The document goes to clients. It should read as a confident, factual walkthrough of what the Clay workflow accomplishes. Every section should:

- Use business language, not column names (column names appear only in the SOW mapping table)
- Report numbers as facts, not judgments
- Name providers by their canonical names (Findymail, Hunter, Prospeo — not "find-email-v2")
- Stay in the past / present tense: "the table sourced 2,400 companies" — not "will source" or "should source"

Full brand tokens live in [references/brand_spec.md](references/brand_spec.md).

## Key References

- [references/prompt.md](references/prompt.md) — the AI prompt for document spec generation
- [references/document_template.md](references/document_template.md) — annotated example of the target document
- [references/brand_spec.md](references/brand_spec.md) — colors, typography, logo placement
- [references/csv_processing.md](references/csv_processing.md) — CSV streaming + fuzzy column matching
- [references/edge_cases.md](references/edge_cases.md) — every edge case, how the skill handles it
- [scripts/generate_docx.py](scripts/generate_docx.py) — the Word document renderer

## Sharing This Skill

```bash
cd path/to/skills-parent && zip -r ~/Downloads/clay-quality-assessment.zip clay-quality-assessment/
```

The recipient unzips into their own skill directory for Claude, Cursor, Codex, or Foundations.

## Dependencies

- Python 3.9+
- `python-docx` (install with `pip install python-docx`)
- `pdftotext` CLI (optional — only if SOW is a PDF; ships with `poppler` on macOS via `brew install poppler`)
