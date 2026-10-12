# Document Template (Annotated Example)

This file shows exactly what a finished Quality Assessment document looks like once rendered. The AI producing the JSON spec should match this shape and tone. Placeholder values are in `{braces}`; keep the prose style and replace specifics.

The deliverable has **five sections in this order**: Cover · Overview · Flow Logic · Per-Stage Provider Fill Rates · Coverage & Quality. Only the cover sits on its own page. Sections 2–5 flow continuously.

---

## COVER PAGE

*[Clay logo, top-left, ~72×54px]*

**{Client Name} × Clay**
*(36pt navy bold)*

**{Project Name}**
*(24pt blue bold, below title)*

*Quality Assessment — Workflow Performance Review*
*(italic gray subtitle)*

*[horizontal rule, navy 6pt]*

*Footer (bottom-left, italic gray): "Confidential — Clay Professional Services" — no page number on the cover.*

*[page break — only forced page break in the document]*

---

## 1. Overview

This workflow delivers a prioritized, contact-ready list of qualified mid-market healthcare technology buyers across North America and the UK. The table seeds from a saved Sales Navigator search, layers in firmographic and technographic enrichment, qualifies each company against an ICP rubric, and returns named contacts with verified work emails and direct dial numbers ready for outbound sequencing. The intended outcome is a refreshed, sales-ready contact pool delivered on a recurring cadence so the {Client} go-to-market team can spend their time selling, not sourcing.

*Note: this assessment covers a single Clay table. Engagements with multiple delivery tables receive one Quality Assessment per table; figures in this document apply only to the table named below.*

---

## 2. Flow Logic

The pipeline runs in five conceptual stages, each building on the prior stage's output.

1. **Source ingestion** — pull raw target companies from the upstream source list and resolve a clean root domain for each row.
2. **Firmographic & technographic enrichment** — layer in industry, headcount, technology stack, and headquarters detail to give every company a full firmographic profile.
3. **ICP qualification** — score each enriched company against the ICP rubric and tag rows that meet the qualifying threshold.
4. **Contact sourcing & validation** — find the relevant person at every qualifying account and produce a deliverable, validated work email.
5. **Phone enrichment & output preparation** — append direct dial numbers where available and assemble the final delivery view.

*(No providers, fill rates, or credit costs appear in this section by design — Section 3 covers the provider detail and Section 4 consolidates the coverage and credit view.)*

---

## 3. Per-Stage Provider Fill Rates

The list below expands each stage above into the providers that powered it, with the fill rate observed for each. Costs appear in Section 4.

**Stage 1 — Source ingestion**
- **Sales Navigator saved search (upstream)** — fill rate **100%**
- **Clay Native Domain Resolution** — fill rate **98%**

**Stage 2 — Firmographic & technographic enrichment**
- **HG Insights** — fill rate **94%**
- **BuiltWith** — fill rate **86%**
- **Clay HQ Address Lookup** — fill rate **91%**

**Stage 3 — ICP qualification**
- **Claygent (Argon) — six-signal qualification research** — fill rate **92%**
- **Claygent compliance research** — fill rate **89%**

**Stage 4 — Contact sourcing & validation** *(waterfall — providers listed in schema order; subsequent providers show incremental contribution)*
- **Findymail** — fill rate **41%**
- **Hunter** — fill rate **+18%**
- **Prospeo** — fill rate **+9%**
- **Kitt** — fill rate **+4%**
- **ZeroBounce verification** — fill rate **64%**

**Stage 5 — Phone enrichment & output preparation**
- **Surfe** — fill rate **28%**
- **CPJ / MixRank fallback** — fill rate **+6%**
- **Output view assembly (formula)** — fill rate **100%**

---

## 4. Coverage & Quality (Aggregate Level)

The table below combines per-provider fill rate with per-call Clay credit cost, grouped by stage like an income statement. Group blended rows weight per-call credits by each provider's incremental hit rate. The **Final Delivery** row is the last row in the table.

| Section / Provider | Fill Rate | Cost (Clay credits) |
|---|---|---|
| **Source ingestion** | | |
| &nbsp;&nbsp;Sales Navigator saved search (upstream) | 100% | 0 |
| &nbsp;&nbsp;Clay Native Domain Resolution | 98% | 0 |
| &nbsp;&nbsp;&nbsp;&nbsp;Source ingestion — blended | 98% | 0 |
| **Firmographic & technographic enrichment** | | |
| &nbsp;&nbsp;HG Insights | 94% | 2 |
| &nbsp;&nbsp;BuiltWith | 86% | 1.5 |
| &nbsp;&nbsp;Clay HQ Address Lookup | 91% | 0.7 |
| &nbsp;&nbsp;&nbsp;&nbsp;Firmographic enrichment — blended | 96% | 4.2 |
| **ICP qualification** | | |
| &nbsp;&nbsp;Claygent (Argon) — six-signal research | 92% | 2.5 |
| &nbsp;&nbsp;Claygent compliance research | 89% | 0.5 |
| &nbsp;&nbsp;&nbsp;&nbsp;ICP qualification — blended | 92% | 3.0 |
| **Contact sourcing & validation** | | |
| &nbsp;&nbsp;Findymail | 41% | 1 |
| &nbsp;&nbsp;Hunter | +18% | 1 |
| &nbsp;&nbsp;Prospeo | +9% | 0.25 |
| &nbsp;&nbsp;Kitt | +4% | 0.4 |
| &nbsp;&nbsp;ZeroBounce verification | 64% | 0.5 |
| &nbsp;&nbsp;&nbsp;&nbsp;Contact sourcing — blended | 64% | 1.04 |
| **Phone enrichment & output prep** | | |
| &nbsp;&nbsp;Surfe | 28% | 1.5 |
| &nbsp;&nbsp;CPJ / MixRank fallback | +6% | 1.3 |
| &nbsp;&nbsp;Output view assembly (formula) | 100% | 0 |
| &nbsp;&nbsp;&nbsp;&nbsp;Phone enrichment — blended | 34% | 0.50 |
| &nbsp;&nbsp;&nbsp;&nbsp;**Final Delivery** | 64% (1,536 of 2,400) | ≈8.74 |

*Credits are per-call estimates from Clay's published action pricing. Group blended credits weight each provider's per-call cost by its incremental hit rate within the waterfall (e.g. Findymail 0.41 × 1 + Hunter 0.18 × 1 + Prospeo 0.09 × 0.25 + Kitt 0.04 × 0.4 + ZeroBounce 0.64 × 0.5 = 1.04 credits/row). The Final Delivery row is the sum of stage blendeds.*

---

*Body-page footer (every page after the cover): "Confidential — Clay Professional Services" (left), "Page X of Y" (right), 9pt gray.*

---

## Indentation Levels (For the Renderer)

The "Section / Provider" column in Section 4 follows accounting-style indentation. The renderer uses paragraph indentation in the cell, not text characters or markdown nbsp.

| Indent level | Used for | Style |
|---|---|---|
| 0 (no indent) | **Group header rows** (e.g. "Source ingestion") | Bold, navy, no fill rate / credit values populated |
| 1 (one tab worth) | **Provider rows** under a group | Regular weight |
| 2 (two tabs worth) | **Group blended rows** ("X — blended") and the **Final Delivery** row | Regular weight (NOT bold), italic optional, top-border above Final Delivery only |

A "tab worth" in the renderer is approximately 0.18 inch (`260` twips) of left indent.

---

## Notes for the Prompt

**Tone observations:**
- Every percentage is stated as a fact — no qualifiers like "only," "just," "unfortunately"
- Providers are named in bold on first mention in Sections 3 and 4
- Provider/column names never appear in Sections 1 or 2
- Fill rates never appear in Sections 1 or 2
- Credit costs never appear in Sections 1, 2, or 3 — only Section 4
- Past/present tense throughout
- Business language ("qualifying contacts," "target accounts," "outbound sequencing")

**Structural observations:**
- Cover page is the only section on its own page
- Sections 2–5 flow continuously, separated only by the section heading
- Section 3 mirrors Section 2's stage list one-for-one (same `stageName` per stage)
- Section 4's group order mirrors Sections 2 and 3
- Waterfall providers always show first provider as absolute % (e.g. "41%") and subsequent providers as incremental "+%" (e.g. "+18%")
- Group blended row label format: `{Stage Name} — blended`
- Final Delivery row sits at the bottom of the table with a top border separating it from the prior group
- Group blended rows are NOT bolded — they are only indented further than provider rows
- Group header rows are bolded; provider rows and blended rows are regular weight
