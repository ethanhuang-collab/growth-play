# Document Generation Prompt

You are producing a client-facing quality assessment document for a Clay.com workflow. You will receive three inputs:

1. **Schema JSON** — condensed Clay table schema with column metadata, dependencies, waterfall structure, and prompts.
2. **Metrics JSON** — pre-computed per-column fill rates and value distributions derived from the CSV export.
3. **SOW** — Statement of Work text (plain, docx-extracted, or pdf-extracted).

Your job is to produce a **single JSON document spec** that a renderer script will turn into a branded Word document.

## The Five-Section Shape (Locked)

The document has exactly **five sections**, in order. Only the cover page sits on its own page; sections 2–5 flow continuously.

1. **Cover page** — Clay logo, "{Client} × Clay — {Project}", subtitle, navy rule, confidential footer. Driven by `meta`.
2. **Overview** — prose only. What is the table meant to do (per the SOW)? What is the key outcome? **No fill rates. No costs. No provider names.**
3. **Flow Logic** — high-level A → B → C → … of the pipeline. **Conceptual only — no providers, no fill rates, no costs.**
4. **Per-Stage Provider Fill Rates** — same stage list as Section 3, each expanded into a bulleted list of providers and their fill rates. **No costs.**
5. **Coverage & Quality (Aggregate Level)** — one income-statement-style table that is the **only** place credit costs appear in the document. The "Final Delivery" row is the **last row** of this table.

Think of sections 3 and 4 as the "what happens" / "with what data" pair, and section 5 as the consolidated finance-style summary that ties fill rate and Clay credit cost to every group and provider in the pipeline.

## Critical Framing Rules

This document is a **client-facing deliverable**. It paints the Clay workflow in a factual, positive light. Every number is a fact, not a judgment.

**Do:**
- State fill rates as bolded percentages
- Name providers by canonical name (Findymail, Hunter, Prospeo — not action keys)
- Keep prose in past/present tense describing what the workflow does
- Use business language, not column names

**Do not:**
- Mention Clay credit costs anywhere outside the Section 5 table
- Mention specific providers in Section 2 or Section 3
- Mention fill rates in Section 2 or Section 3
- Assign quality scores, letter grades, or recommendations
- Use words like "unfortunately", "however", "only X%", "just", "needs", "should", "could be improved"
- Compare against benchmarks ("above average", "industry standard")

If a fill rate is low, state it plainly: "Phone numbers were sourced for **34%** of contacts." The reader interprets the number.

## Document JSON Spec Format

Produce a single JSON object with this shape. The renderer expects exactly these keys.

```json
{
  "meta": {
    "clientName": "string",
    "projectName": "string",
    "documentTitle": "string (e.g., 'Client × Clay — Project Name')",
    "subtitle": "Quality Assessment — Workflow Performance Review",
    "generatedDate": "YYYY-MM-DD",
    "sowDate": "YYYY-MM-DD or null",
    "tableName": "string",
    "rowCount": number,
    "stageCount": number
  },
  "overview": {
    "prose": "3–6 sentences. What is this table meant to do, drawn from the SOW? Who is it for and what is the key business outcome? No fill rates, no providers, no costs.",
    "multiTableNote": "Optional. Include only when the workflow spans multiple tables and only one is being assessed here. Renders as an italic note under the prose."
  },
  "flowLogic": {
    "intro": "1–2 sentences framing the pipeline at the highest level (e.g. 'The pipeline runs in eight stages, each enriching the prior stage's output.'). No providers. No fill rates. No costs.",
    "steps": [
      {
        "stageNumber": 1,
        "stageName": "Source Ingestion",
        "description": "1–2 sentences describing in business terms what this stage does. No providers named. No fill rates. No credits."
      }
    ]
  },
  "stageDetails": {
    "intro": "Optional 1-sentence bridge, e.g. 'The list below expands each stage into the providers that powered it, with the fill rate observed for each.'",
    "stages": [
      {
        "stageNumber": 1,
        "stageName": "Source Ingestion",
        "providers": [
          {"name": "Spain Campaign Template (upstream Find Companies table)", "fillRate": "100%"}
        ]
      },
      {
        "stageNumber": 4,
        "stageName": "Work Email Sourcing",
        "waterfall": true,
        "providers": [
          {"name": "Findymail", "fillRate": "41%"},
          {"name": "Hunter", "fillRate": "+18%"},
          {"name": "Prospeo", "fillRate": "+9%"}
        ]
      }
    ]
  },
  "coverageTable": {
    "intro": "1 sentence framing this as the consolidated coverage and credit view, e.g. 'The table below combines per-provider fill rate with the actual per-row Clay credit cost, grouped by stage like an income statement.'",
    "groups": [
      {
        "stageNumber": 4,
        "label": "Work Email Sourcing",
        "providers": [
          {"name": "Findymail", "fillRate": "41%", "credits": "1", "effectiveCredits": "0.41"},
          {"name": "Hunter", "fillRate": "+18%", "credits": "1", "effectiveCredits": "0.59"},
          {"name": "Prospeo", "fillRate": "+9%", "credits": "0.25", "effectiveCredits": "0.21"}
        ],
        "blended": {
          "label": "Work Email Sourcing — blended",
          "fillRate": "59%",
          "credits": "—",
          "effectiveCredits": "1.21"
        }
      }
    ],
    "finalDelivery": {
      "label": "Final Delivery",
      "fillRate": "59% (1,334 of 2,271)",
      "credits": "—",
      "effectiveCredits": "≈X.X"
    },
    "footnote": "Optional 1-line italic note. E.g. 'Per-call credits are Clay\\'s published action rate. Effective credits/row reflect what each call actually costs once we account for refund-on-no-data policies and observed fill rates: providers that refund on empty result are weighted by their fill rate; providers that charge regardless of result are billed at their full per-call rate every time they fire.'"
  }
}
```

## Rules for Filling Each Section

### meta
- `clientName` and `projectName` come from the SOW. Strip "× Clay" from project name if the SOW uses that framing.
- `generatedDate` = today's date.
- `sowDate` = the SOW's issue date if stated, else null.
- `rowCount` and `tableName` come from the schema or metrics.
- `stageCount` = the number of entries in `flowLogic.steps` (and `stageDetails.stages`).

### overview.prose
- Lead with what the table accomplishes for the client, paraphrased from the SOW objective.
- Follow with 2–4 sentences on the business outcome (segment served, downstream use case, why this matters).
- Do **not** mention column names, provider names, fill rates, or credit costs.
- If the workflow has multiple tables and only one is being assessed, say so explicitly in one sentence and/or use `multiTableNote`.

### flowLogic.steps
- 4–8 steps in execution order, mirroring the topological order of the schema's dependency graph.
- Each step: `stageNumber` (1-indexed), `stageName` (business-clear, no column names), `description` (1–2 sentences in business terms).
- Do **not** name providers, fill rates, or credit costs in this section.
- Stage names should match exactly between `flowLogic.steps[].stageName` and `stageDetails.stages[].stageName`.

### stageDetails.stages
- One entry per stage, same `stageNumber` and `stageName` as `flowLogic.steps`.
- `providers[]` is an ordered list of every provider/data source involved in that stage with a per-provider fill rate.
- For waterfall stages, set `waterfall: true` and list providers in schema-defined order. The first provider's `fillRate` is its absolute hit rate (e.g. `"41%"`); each subsequent provider is its **incremental** contribution prefixed with `+` (e.g. `"+18%"`).
- For non-waterfall stages, each provider's `fillRate` is the column's standalone fill rate (e.g. `"100%"`, `"93%"`).
- Use canonical provider names (Findymail, Hunter, Prospeo). Do not use action keys.
- **No credit costs in this section.**

### coverageTable.groups
- One group per stage in execution order. `stageNumber` and `label` should match `flowLogic.steps[].stageName`.
- `providers[]`: ordered list of providers within that stage. Each carries `name`, `fillRate`, `credits` (per-call Clay rate), and `effectiveCredits` (per-row expected cost).
  - For non-waterfall providers, `fillRate` is the standalone fill rate.
  - For waterfall providers, `fillRate` follows the same `"41%"` / `"+18%"` convention as Section 4.
  - `credits` is the Clay credit cost **per call** for that provider, drawn from the schema's `pricing.perColumn[].credits` (keyed by column name). Fall back to the companion hand-off skill's `references/enrichment_credits.json` (keyed by `actionKey`) only when the schema has no live pricing. When both skills are installed from Foundations, that file is available at `../clay-handoff-doc-generator/references/enrichment_credits.json` relative to this skill directory. Use the numeric value as a string (e.g. `"1"`, `"0.25"`). For free formula/platform steps, use `"0"`.
  - `effectiveCredits` is the **per-row expected cost** for that provider — the number that actually shows up on the bill per source row. Compute from the schema's `pricing.perColumn[].effectiveCredits` when present (it already accounts for `refundOnNoData`). When the schema does not pre-compute it, derive it as follows:
    - If `pricing.perColumn[].refundOnNoData === true`: `effectiveCredits = credits × fillRate` (you only pay when the provider returns data).
    - If `pricing.perColumn[].refundOnNoData === false`: `effectiveCredits = credits × attemptRate`, where `attemptRate` is the fraction of source rows on which this provider fired. For a non-waterfall provider that fires on every row, `attemptRate = 1`. For a waterfall provider, `attemptRate = 1 − (cumulative fill rate of all preceding providers)` (the share of rows still uncovered when this provider's turn came up).
    - For free formulas / platform steps: `effectiveCredits = "0"`.
  - Round `effectiveCredits` to two decimals as a string (e.g. `"0.21"`, `"1.00"`).
- `blended`: a single row representing the group total.
  - `fillRate`: the consolidated end-of-stage fill rate (e.g. waterfall final coverage, or fill rate of the stage's primary output column).
  - `credits`: render as `"—"` for blended rows — per-call rate is meaningless once we sum across providers.
  - `effectiveCredits`: **sum of `effectiveCredits` across the group's providers**. This is what the stage actually costs per source row.

### coverageTable.finalDelivery
- Always present. Renders as the **last row** of the table, indented to the same level as a blended-group row, separated visually by a top border, **not bolded**.
- `fillRate`: overall delivery fill rate of the final output (e.g. `"59% (1,334 of 2,271)"` for the merged email column).
- `credits`: render as `"—"`.
- `effectiveCredits`: total per-row Clay credit cost, summed across all stage blendeds. Prefer the schema's `pricing.totals.effectiveCreditsPerRow` when present; otherwise sum the group blendeds. Round to a sensible value (e.g. `"≈12.4"`).

### coverageTable rendering rules (handled by the renderer; do not replicate in prose)
- Group header rows show only `label` in the left column (no fill rate / credits).
- Provider rows are indented one level beneath their group header.
- Blended group rows are indented two levels beneath the group header (same level as `finalDelivery`), and are **not bolded**.
- The `finalDelivery` row sits below the last group, separated by a top border.
- Costs appear only in this table; never in earlier sections.

## Cost Source

**Primary source** — the schema's `pricing` block, which the Chrome extension populates from Clay's live `/v3/actions`, `/v3/model-pricing`, and `/v3/attributes` endpoints at extraction time:
- `pricing.perColumn[]` — one entry per column with `name`, `credits` (per-call), `refundOnNoData` (boolean), `fillRate` (0–1, when available), and `effectiveCredits` (per-row expected cost). Match by column name.
- `pricing.totals.creditsPerRow` — nominal sum (worst case, ignores fill rate).
- `pricing.totals.effectiveCreditsPerRow` — the realistic per-row spend (use this for `finalDelivery.effectiveCredits`).

**Fallback** — only when `pricing` is absent or a column is missing from `pricing.perColumn[]`:
- Pull per-call credits from the companion hand-off skill's `references/enrichment_credits.json`, keyed by `actionKey`.
- Assume `refundOnNoData = true` (most providers refund on no data) unless the action key is in the known charge-on-no-result list (waterfall execution, some validators).
- Compute `effectiveCredits` using the formulas in the `coverageTable.groups` section above.

For formula columns, source-table imports, and other no-action steps: `credits = "0"` and `effectiveCredits = "0"`.
For AI / Claygent calls without static fallback pricing: use `"0"` for both fields and add a footnote noting AI cost is excluded from the row total.

## Data Hygiene Rules

1. **Never invent a percentage.** If the metrics don't have a value for a column, omit that provider rather than estimate.
2. **Never invent a provider.** Only name providers found in the schema's `emailWaterfallProviders`, `waterfallEntries`, action columns, or formula references.
3. **Never restate a number in a way that implies judgment.** "Only 34%" is a judgment. "34%" is a fact.
4. **No costs outside Section 5.** Sections 2–4 must not contain any reference to Clay credits, dollar costs, or pricing.
5. **Stage names must match across sections 3, 4, and 5.**
6. **Date / system columns** — exclude from fill rate computation: any column whose name contains `date`, `timestamp`, `created`, `updated`, `modified`, or starts with `_internal_` / equals `id`.

## Conflict Surfacing

Before producing the final JSON, scan for material conflicts. If any exist, return a structured pre-generation response instead of the document spec:

```json
{
  "conflicts": [
    {
      "category": "string",
      "description": "string",
      "sources": [{"label": "SOW", "value": "quoted text"}, {"label": "Schema", "value": "quoted text"}]
    }
  ]
}
```

Surface only:
- SOW deliverables with no schema column implementing them (>25% of deliverables unimplemented)
- SOW-stated country/segment lists that don't match schema `inputParams`
- Provider ordering in the SOW that differs from `emailWaterfallProviders`
- CSV row count wildly different from SOW-stated target

If no material conflicts, proceed directly to the document JSON.

## Output

Your response must be a single valid JSON object. No markdown fences, no surrounding prose. Either the document spec or the conflicts object.

## Quality Checklist (Self-Check Before Returning)

- [ ] Exactly five top-level content keys: `meta`, `overview`, `flowLogic`, `stageDetails`, `coverageTable`
- [ ] No costs anywhere except in `coverageTable`
- [ ] No provider names in `overview` or `flowLogic`
- [ ] No fill rates in `overview` or `flowLogic`
- [ ] `flowLogic.steps[].stageName` matches `stageDetails.stages[].stageName` matches `coverageTable.groups[].label`
- [ ] Stage count is 4–8
- [ ] Waterfall providers are listed in schema-defined order, first absolute %, rest with `+` prefix
- [ ] Every provider in `coverageTable` has both `credits` (per-call) and `effectiveCredits` (per-row) values (use `"0"` for free)
- [ ] Every blended row and `finalDelivery` row uses `"—"` for `credits` and a real number for `effectiveCredits`
- [ ] `coverageTable.finalDelivery.effectiveCredits` matches `pricing.totals.effectiveCreditsPerRow` when present (within rounding)
- [ ] `coverageTable.finalDelivery` is present
- [ ] No blocked words: `unfortunately`, `however only`, `just N%`, `needs`, `should`, `could be improved`, `below target`, `opportunity for`
- [ ] JSON validates (balanced braces, quoted strings, proper commas)
