# Edge Cases

Every known edge case the skill must handle, the behavior it should exhibit, and where in the pipeline the handling lives (CSV processing, AI prompt, or rendering script).

## Input File Edge Cases

### 1. Missing input file

**Condition:** One of the three required inputs (CSV, schema, SOW) is not provided or the path is invalid.

**Handling (skill orchestrator):** Stop before processing. Tell the user exactly which input is missing and what format is expected. Do not attempt a partial document.

---

### 2. Empty CSV (zero data rows)

**Condition:** CSV has a header row but no data rows.

**Handling (CSV processor):** Output a Metrics JSON with `rowCount: 0` and empty `perColumn`. **Handling (AI prompt):** Produce a shortened "table not yet populated" document variant — cover page, project overview, SOW mapping table without fill rates, and a note in Output Summary: "The table has been configured but not yet run. This document describes the configured pipeline; fill rate metrics will be populated after the first run."

---

### 3. CSV header row only has one column / is malformed

**Condition:** Header parsing detects < 2 columns, or the file has zero newlines.

**Handling (CSV processor):** Raise a clear error: "CSV appears malformed — the header row did not parse into multiple columns. Verify this is a standard Clay table export." Do not proceed.

---

### 4. CSV is tab-separated instead of comma-separated

**Condition:** The first line contains more tabs than commas.

**Handling (CSV processor):** Auto-switch to tab delimiter. Log a note in the Metrics JSON: `"delimiter": "tab"`.

---

### 5. CSV has embedded newlines in cells (Claygent summaries, multi-line outputs)

**Condition:** A single "row" in the CSV spans multiple physical lines because a cell contains newlines.

**Handling (CSV processor):** Use the `csv` module's quote-aware parser. Never split on `\n`. Test coverage: any cell value containing `"\n"` should be counted as a single filled cell.

---

### 6. CSV has a BOM or is latin-1 encoded

**Condition:** File starts with `\ufeff` or cannot decode as UTF-8.

**Handling (CSV processor):** Open with `utf-8-sig` first (handles BOM transparently). On `UnicodeDecodeError`, retry with `latin-1` and log `"encoding": "latin-1"` in the Metrics JSON.

---

### 7. Schema JSON is the older v1.0 format (not condensed v2.1)

**Condition:** Schema lacks `emailWaterfallProviders`, `columnCount`, or `columns[].dependencies`.

**Handling (schema parser):** Attempt best-effort parsing. Infer waterfall order from column names and formula `waterfallEntries` if available. Log a note in the final document's metadata field that the schema was pre-v2.1. Do not fail — produce a document with whatever can be extracted.

---

### 8. SOW is a PDF

**Condition:** `sow_path` ends in `.pdf`.

**Handling (SOW parser):** Attempt `pdftotext` via subprocess. If not installed, fall back to `pypdf` or `PyPDF2` if available. If neither works, raise: "Cannot extract text from PDF. Install `poppler` (`brew install poppler`) or convert the SOW to `.docx` or `.txt` first."

---

### 9. SOW is a `.docx`

**Condition:** `sow_path` ends in `.docx`.

**Handling (SOW parser):** Use `python-docx` to extract paragraphs. Concatenate all runs including table cells (SOWs often have tables for deliverables).

---

### 10. SOW has no explicit deliverables / success metrics

**Condition:** SOW is pure descriptive prose with no enumerated deliverables.

**Handling (AI prompt):** Produce the Project Overview from the prose. Skip the SOW Scope Mapping section entirely (or replace with a brief paragraph noting "The SOW scope is described in the Project Overview above; no explicit per-deliverable mapping is provided."). Do not invent deliverables.

---

### 11. Multiple SOW versions / extra files in the drop

**Condition:** User drops multiple files ambiguously or a folder with several SOWs.

**Handling (skill orchestrator):** Ask the user to specify which SOW to use. Do not default silently. If the user supplies a folder path, list all `.txt/.docx/.pdf` files and ask.

## Schema vs. CSV Matching Edge Cases

### 12. CSV column name is truncated compared to schema

**Condition:** Clay's CSV export truncates long column names (e.g., "Claygent Compliance Research Output" → "Claygent Compliance Researc").

**Handling (CSV processor):** Fuzzy match via prefix + Levenshtein. See [csv_processing.md](csv_processing.md).

---

### 13. CSV has a column not in the schema

**Condition:** User added a manual column or an older CSV export references a now-deleted column.

**Handling:** Include in the Metrics JSON's `perColumn` with a `userAdded: true` flag. The AI prompt excludes `userAdded` columns from the pipeline narrative (they're not part of the designed pipeline) but may mention the row count. Do not surface them as gaps.

---

### 14. Schema has a column not in the CSV

**Condition:** A recently added schema column hasn't been included in the CSV export.

**Handling:** Exclude from fill rate metrics. In the pipeline narrative, the AI should either mention the stage without a fill rate ("Claygent performs compliance research") or omit that stage from the walkthrough if no CSV data exists. Do not invent a fill rate.

---

### 15. Ambiguous fuzzy match (two CSV columns normalize to the same name)

**Condition:** Both "Email" and "Email (2)" normalize to "email" after stripping the `(2)` suffix.

**Handling (CSV processor):** Keep both as distinct columns. Match the first one (by index) to the schema column. Log the second in `matchReport.ambiguous` with a note. Do not bind both to the same schema column.

## Column-Type Edge Cases

### 16. Date / timestamp columns

**Condition:** Column name contains "date", "timestamp", "created", "updated", "modified".

**Handling (CSV processor):** Count fills but exclude from pipeline narrative. The Metrics JSON marks them with `isTemporal: true`. The AI prompt explicitly skips these in the pipeline walkthrough.

---

### 17. System / internal columns

**Condition:** Column name matches `id`, `_.*`, `run_button_.*`, or is the primary key.

**Handling:** Exclude entirely from metrics. Never mentioned in the document.

---

### 18. Score / categorical column (has value distribution, not fill rate)

**Condition:** Column type is `formula` with non-waterfall formulaType, or `number`, or mentioned in promptPurpose as a "tier", "score", "category".

**Handling (CSV processor):** Compute value distribution via [csv_processing.md § Value Distribution](csv_processing.md). **Handling (AI prompt):** Report the dominant value's percentage in the pipeline narrative rather than a "fill rate". Example: "Scored **Tier 1** on 18% of rows and **Tier 2** on 35%."

---

### 19. Multi-value (array) columns

**Condition:** Column value is a JSON array or comma-separated list (e.g., "tech1, tech2, tech3").

**Handling (CSV processor):** Treat as "filled" if non-empty. Do not attempt per-element distribution (too noisy for this document).

---

### 20. Extremely long cell values

**Condition:** Cell contains more than 10,000 characters (common for raw Claygent research outputs).

**Handling:** Still count as filled. Do not include the actual value anywhere in the Metrics JSON or AI prompt.

## Waterfall Edge Cases

### 21. Waterfall providers in CSV don't match schema's declared order

**Condition:** Schema declares `[Findymail, Hunter, Prospeo]` but CSV has only `[Hunter, Prospeo]` (Findymail column is missing).

**Handling (CSV processor):** Compute contributions for the providers that exist in both. Log missing providers in `matchReport`. **Handling (AI prompt):** Report only the providers with data in the waterfall table. Do not leave blank rows.

---

### 22. Only one provider in the waterfall has non-zero fill

**Condition:** Subsequent providers contributed 0% because the first provider filled everything.

**Handling:** Still include all providers in the waterfall table with `+0%` contributions. The table shows the actual cascade depth of the pipeline design. Running total stays constant.

---

### 23. No waterfall exists in the schema

**Condition:** Schema has no `emailWaterfallProviders` and no `formulaType: "waterfall"`.

**Handling:** Skip the waterfall table format entirely. Treat email/phone columns as simple single-provider stages.

## Conditional-Run Edge Cases

### 24. Gate column referenced in `conditionalRun` is not in the CSV

**Condition:** The schema says `conditionalRun: "{{ICP Qualification}} == 'pass'"` but ICP Qualification column isn't in the CSV (schema/CSV mismatch).

**Handling (CSV processor):** Fall back to total-row fill rate. Note `gateColumnMissing: true` in the eligibleFillRates entry. **Handling (AI prompt):** Report only the total-row rate without the "of eligible rows" qualification.

---

### 25. Complex conditional gate (AND/OR logic, nested formulas)

**Condition:** `conditionalRun` uses multiple gate columns with logic.

**Handling (CSV processor):** Try to parse. If parsing fails, default to "any non-empty value in the referenced columns counts as eligible". Note `gateSimplified: true`.

## Volume Edge Cases

### 26. Very small CSV (< 50 rows)

**Condition:** `rowCount < 50`.

**Handling (AI prompt):** Still produce the document. In Project Overview, mention the sample size matter-of-factly: "The table currently holds 24 rows."

---

### 27. Very large CSV (> 100K rows)

**Condition:** `rowCount > 100000`.

**Handling (CSV processor):** Stream normally — no chunking needed for this size. **Handling (AI prompt):** No special treatment beyond reporting the row count.

---

### 28. Very large CSV (> 1M rows)

**Condition:** `rowCount > 1000000`.

**Handling (CSV processor):** Stream normally. Confirm the OS can handle the file size. If processing takes > 2 minutes, offer sample-mode via `--sample-rows 50000`.

## Document-Generation Edge Cases

### 29. AI returns a conflicts object instead of a document spec

**Condition:** Material conflicts were surfaced (see prompt.md).

**Handling (orchestrator):** Render the conflicts as a markdown-formatted message to the user. Ask them to resolve, then re-invoke generation. Do not render a document.

---

### 30. AI returns invalid JSON

**Condition:** `json.loads()` fails on the AI output.

**Handling (orchestrator):** Attempt a single repair pass: strip leading/trailing prose, strip markdown code fences. If still invalid, show the raw output and ask the user to retry.

---

### 31. AI returns too few or too many stages

**Condition:** `len(stages) < 2` or `len(stages) > 12`.

**Handling (orchestrator):** Render the document as-is (we trust the AI), but log a warning in the skill output. Do not retry automatically.

---

### 32. Logo file missing

**Condition:** `assets/Clay_Logo_Icon.png` not found at runtime.

**Handling (renderer script):** Render the document without the logo. Log a warning. The brand-spec'd cover and header still use the other tokens.

---

### 33. Output path is not writable

**Condition:** `~/Downloads/` doesn't exist or is read-only.

**Handling (renderer script):** Fall back to `~/clay-qa-{client}-{date}.docx`. If still unwritable, write to `/tmp/` and tell the user.

## Branding / Content Safety Edge Cases

### 34. AI prose contains blocked words

**Condition:** The document spec's prose includes words from the blocked list ("unfortunately," "only," "just," "below target," etc.).

**Handling (renderer script):** Perform a post-generation word scan on all prose fields. If blocked words are found, either auto-rewrite (remove "just", "only" where they modify percentages) or log a warning and still render — do not block the document.

---

### 35. AI prose includes a column name

**Condition:** The pipeline walkthrough prose mentions a raw column name like `Findymail Email` directly.

**Handling:** Acceptable if the column name *is* the provider name (which is our convention). The check is: if the string appears in the schema's `columns[].name` and is also a provider name, allow it. Otherwise, log a warning but render.

---

### 36. SOW mapping table has zero rows

**Condition:** No SOW deliverables map to any schema columns.

**Handling (AI prompt):** Omit the SOW Scope Mapping section entirely. Do not produce an empty table with placeholder "N/A" rows.

## Summary Table

| # | Edge Case | Handled By |
|---|---|---|
| 1 | Missing input file | Orchestrator |
| 2 | Empty CSV | CSV processor + AI prompt |
| 3 | Malformed CSV | CSV processor |
| 4 | Tab-delimited CSV | CSV processor |
| 5 | Embedded newlines | CSV processor |
| 6 | BOM / latin-1 | CSV processor |
| 7 | Old schema format | Schema parser |
| 8 | PDF SOW | SOW parser |
| 9 | DOCX SOW | SOW parser |
| 10 | No deliverables in SOW | AI prompt |
| 11 | Multiple SOWs | Orchestrator |
| 12 | Truncated CSV column names | CSV processor (fuzzy match) |
| 13 | User-added CSV columns | CSV processor + AI prompt |
| 14 | Schema columns missing from CSV | CSV processor + AI prompt |
| 15 | Ambiguous fuzzy match | CSV processor |
| 16 | Date/timestamp columns | CSV processor + AI prompt |
| 17 | System / internal columns | CSV processor |
| 18 | Score / categorical columns | CSV processor + AI prompt |
| 19 | Multi-value cells | CSV processor |
| 20 | Extremely long cell values | CSV processor |
| 21 | Waterfall provider mismatch | CSV processor + AI prompt |
| 22 | Single-provider waterfall | AI prompt |
| 23 | No waterfall | AI prompt |
| 24 | Missing gate column | CSV processor + AI prompt |
| 25 | Complex gate logic | CSV processor |
| 26 | Very small CSV | AI prompt |
| 27 | > 100K rows | CSV processor |
| 28 | > 1M rows | CSV processor |
| 29 | AI returns conflicts | Orchestrator |
| 30 | Invalid JSON from AI | Orchestrator |
| 31 | Too few/many stages | Orchestrator (warning only) |
| 32 | Logo missing | Renderer |
| 33 | Output path unwritable | Renderer |
| 34 | Blocked words in prose | Renderer |
| 35 | Column names in prose | Renderer (warning only) |
| 36 | Zero SOW mapping rows | AI prompt |
