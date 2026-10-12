# CSV Processing Guide

The CSV input is the source of truth for all numbers in the quality assessment document. This file defines how to process it reliably, including for very large tables (50K+ rows) that may not fit in memory or context.

## Goals

1. Count filled vs. empty cells per column — the core fill rate input
2. Match CSV columns to schema columns — so fill rates can be attached to the pipeline narrative
3. Compute waterfall contributions — per-provider incremental fill
4. Compute value distributions for categorical columns (ICP tier, qualification status, etc.)
5. Do all of this without loading the entire CSV into memory or the AI context window

## Streaming Strategy

**Always stream the CSV row-by-row using Python's `csv.DictReader` or `csv.reader`.** Never call `pandas.read_csv` on large files without chunking, and never pass the raw CSV contents into an AI prompt.

### Memory-safe row counting and per-column fill

```python
import csv

def stream_fill_rates(csv_path, max_rows=None):
    counters = None
    total = 0
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)
        counters = {h: {'filled': 0, 'empty': 0} for h in headers}
        for row in reader:
            total += 1
            if max_rows and total > max_rows:
                break
            for i, cell in enumerate(row):
                if i >= len(headers):
                    continue
                key = headers[i]
                if cell and cell.strip():
                    counters[key]['filled'] += 1
                else:
                    counters[key]['empty'] += 1
    return headers, counters, total
```

### Encoding

Use `utf-8-sig` to strip a potential BOM from Clay exports. Fall back to `latin-1` with warning if `utf-8-sig` fails (rare, but some older exports use it).

### Delimiter detection

Default is comma. If the first line contains more tabs than commas, switch to tab-delimited. Use `csv.Sniffer().sniff(sample)` only if the header row is ambiguous.

### Quote handling

Use the `csv` module's default double-quote handling. Never use naive `line.split(',')` — Clay cells contain commas in Claygent outputs, multi-line summaries, and URL parameters.

## Fuzzy Column Matching

CSV exports from Clay sometimes truncate long column names, replace special characters, or add suffixes. The schema is the source of truth for column names, but the CSV may use a slightly different form. We match fuzzily.

### Normalization Rules

Apply these transforms to both the CSV header name and each schema column name before matching:

1. Lowercase the string
2. Strip leading/trailing whitespace
3. Collapse internal whitespace to single spaces
4. Remove trailing ` (2)`, ` (3)`, etc. (Clay's duplicate-column suffixes)
5. Remove non-ASCII characters (emojis, special symbols) — replace with empty string
6. Remove punctuation characters: `.`, `,`, `:`, `;`, `-`, `_`, `(`, `)`, `[`, `]`, `{`, `}`, `/`, `\`
7. Remove multiple consecutive spaces

```python
import re
import unicodedata

def normalize_name(name):
    n = unicodedata.normalize('NFKD', name)
    n = n.encode('ascii', 'ignore').decode('ascii')
    n = n.lower().strip()
    n = re.sub(r'\s*\(\d+\)\s*$', '', n)
    n = re.sub(r'[.,:;\-_()\[\]{}/\\]', ' ', n)
    n = re.sub(r'\s+', ' ', n)
    return n.strip()
```

### Matching Algorithm

1. **Exact match (post-normalization):** if a CSV normalized name equals a schema normalized name, bind them. 1:1 only — if two CSV columns normalize to the same string, do not bind; flag as ambiguous.
2. **Prefix match:** if a CSV name starts with a schema name (or vice versa) and the length ratio is ≥ 0.75, bind. Common case: CSV truncates long names.
3. **Levenshtein similarity ≥ 0.85:** for any unbound CSV columns, compute similarity against all unbound schema columns. Bind the highest-similarity pair per CSV column if ≥ 0.85.
4. **Unmatched CSV columns** → mark as `user-added`. Include in fill rate summary but note they have no schema metadata.
5. **Unmatched schema columns** → mark as `not-in-csv`. Exclude from fill rate metrics; mention in the pipeline narrative only if needed.

### Similarity Calculation

Use Python's `difflib.SequenceMatcher` for a fast, dependency-free similarity:

```python
from difflib import SequenceMatcher
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()
```

## Waterfall Contribution

For waterfall columns identified in the schema (via `emailWaterfallProviders` or `formulaType: "waterfall"` entries), compute per-provider incremental contribution.

### Algorithm

Given a schema-defined provider order `[P1, P2, P3, P4]` and the corresponding CSV columns for each provider's output:

```python
def waterfall_contributions(csv_path, provider_columns):
    contributions = {p: 0 for p in provider_columns}
    total = 0
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            filled_by = None
            for p in provider_columns:
                val = row.get(p, '').strip()
                if val:
                    filled_by = p
                    break
            if filled_by:
                contributions[filled_by] += 1
    return contributions, total
```

Then:

- `contribution[P1] / total` = P1's absolute contribution (as a fraction)
- Running total after each provider = sum of contributions up to and including that provider

Format for the document:

```python
running = 0
rows = []
for i, p in enumerate(provider_columns):
    contrib_pct = contributions[p] / total * 100
    running += contrib_pct
    if i == 0:
        contrib_str = f"{contrib_pct:.0f}%"
    else:
        contrib_str = f"+{contrib_pct:.0f}%"
    rows.append({
        'provider': provider_display_name(p),
        'contribution': contrib_str,
        'runningTotal': f"{running:.0f}%",
    })
```

## Value Distribution (Score / Category Columns)

For columns the schema flags as formulas producing discrete values (ICP tiers, qualification statuses, etc.), compute a value distribution rather than a fill rate.

### Identification

A column is a score/category column if:
- `type == "formula"` and `formulaType` is not `"waterfall"`, or
- `type == "number"`, or
- the column's `promptPurpose` explicitly mentions tiers, scores, or discrete categories

### Calculation

```python
from collections import Counter

def value_distribution(csv_path, column, limit=10):
    counts = Counter()
    total = 0
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = (row.get(column, '') or '').strip()
            if val:
                counts[val] += 1
                total += 1
    top = counts.most_common(limit)
    return [
        {'value': v, 'count': c, 'percentage': f"{c/total*100:.0f}%"}
        for v, c in top
    ], total
```

If the column has more than 10 distinct values, take the top 10 and note "other" as the remainder. Never include the column in a fill rate table.

## Conditional-Run (Eligible-Row) Fill Rate

When the schema says a column has `conditionalRun` with a gate condition, compute fill rate over *eligible* rows only, in addition to total rows.

### Algorithm

```python
def eligible_fill_rate(csv_path, column, gate_column, gate_predicate):
    eligible = 0
    filled = 0
    total = 0
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            gate_val = (row.get(gate_column, '') or '').strip()
            if gate_predicate(gate_val):
                eligible += 1
                col_val = (row.get(column, '') or '').strip()
                if col_val:
                    filled += 1
    return {
        'eligible': eligible,
        'total': total,
        'filled': filled,
        'eligibleRate': filled / eligible if eligible else 0,
        'totalRate': filled / total if total else 0,
    }
```

### Gate Predicate

Clay's `conditionalRun` field typically holds a formula string like `{{some_column}} == "valid"` or `!!{{some_column}}`. Parse it into a predicate:

- `{{col}} == "valid"` → `lambda v: v == "valid"`
- `{{col}} != ""` or `!!{{col}}` → `lambda v: bool(v)`
- Compound gates (AND/OR) → parse into a lambda combining multiple checks
- If the gate expression is too complex to parse reliably, default to `lambda v: bool(v)` and note the simplification in the metrics JSON

## Excluded Columns (Never Report Fill Rates For)

Skip these from fill rate calculations regardless of content:

- Column names matching regex `/^(id|_.*|.*_id|created_at|updated_at|modified_at|.*date.*|.*timestamp.*)$/i`
- The schema's primary key column (first column with `type: "source"` and unique values)
- Clay system columns: `run_button_*`, `_internal_*`, `_table_*`

## Large-File Handling

### Row count ceiling for AI context

The AI only needs summary statistics, not raw rows. The Metrics JSON passed to the AI contains:

- `perColumn`: `{column_name: {filled, empty, rate}}`
- `waterfallContributions`: per-provider percentages
- `valueDistributions`: top 10 values per score column
- `rowCount`: total row count

A typical Metrics JSON is **< 50KB regardless of CSV size** — one object per column, not one object per row. This fits in any AI context window.

### Streaming without loading

For CSVs up to ~500MB, the streaming approach above uses constant memory (one row at a time). No chunking needed.

For CSVs larger than 500MB (rare for Clay exports), consider:
- Multi-process column sharding (read CSV once, dispatch column counts to workers)
- Reading only columns referenced by the schema (skip truly untracked CSV columns)

### Sample-mode fallback

For extremely large CSVs or when the user wants a fast preview, support `max_rows=N` to sample the first N rows. Report the sample size prominently in the metrics JSON (`"sampled": true, "sampleRows": N`) so the AI can disclose it in the document's overview.

## Output: Metrics JSON Shape

The CSV processing step writes this structure to a temp file that feeds the AI prompt:

```json
{
  "rowCount": 2400,
  "sampled": false,
  "perColumn": {
    "Findymail Email": {"filled": 984, "empty": 1416, "rate": 0.41},
    "Hunter Email": {"filled": 432, "empty": 1968, "rate": 0.18, "isWaterfallStep": true},
    "ICP Tier": {"valueDistribution": [
      {"value": "Tier 1", "count": 420, "percentage": "18%"},
      {"value": "Tier 2", "count": 840, "percentage": "35%"}
    ]}
  },
  "waterfallContributions": {
    "Email Waterfall": [
      {"provider": "Findymail", "contribution": "41%", "runningTotal": "41%"},
      {"provider": "Hunter", "contribution": "+18%", "runningTotal": "59%"}
    ]
  },
  "eligibleFillRates": {
    "Claygent Compliance": {
      "filled": 1638, "eligible": 1840, "total": 2400,
      "eligibleRate": 0.89, "totalRate": 0.68,
      "gateColumn": "ICP Qualification Pass"
    }
  },
  "matchReport": {
    "matched": 42,
    "userAddedInCsv": 1,
    "notInCsv": 3,
    "ambiguous": []
  }
}
```

The AI reads this object and weaves the numbers into the document prose.
