---
name: clay-formulas
description: Write, debug, and validate Clay table formula columns using Clay's JavaScript-expression sandbox, including mustache column references, optional chaining, lodash and moment helpers, lookup `.records`, Clay.getCellStatus, array/object transforms, scoring logic, row gates, and formula error triage. Use for Clay formulas, not Google Sheets or Excel formulas and not Use AI/Claygent prompt wording.
status: active
maturity: trial
last_matured: 2026-06-10
---

# Clay Formulas

## Role

Use this skill when the user needs a Clay formula column written or debugged.
Clay formulas are JavaScript-like expressions in Clay's sandbox, not standard
JavaScript scripts and not spreadsheet formulas.

This skill was distilled from
`/Users/ethanhuang1/Downloads/clay-formulas.skill` on 2026-06-10.

## Boundaries

- Use `clay-prompt-authoring` for Use AI or Claygent prompt wording, chip
  contracts, output schema, and sample-row prompt QA.
- Use `sheet` for Google Sheets or Excel formulas.
- Use `clay-platform-troubleshooting` when the issue is provider behavior,
  credits, waterfalls, auth, runs, CRM sync, or live workflow state.
- Use `clay-search-query` to author or run a Clay Search advanced query for
  people, companies, or jobs.
- Do not bulk-run or mutate a live Clay table as part of formula authoring.

## Core Rules

- Clay formulas are a single expression. Do not use `return`, top-level
  `let`/`const`/`var`, function wrappers, or IIFEs.
- Reference columns with Clay mustache syntax such as `{{Column Name}}`.
- Use optional chaining on every nested access: `{{Enrich Person}}?.experience`.
- Template literals do not work reliably; use string concatenation with `+`.
- Convert numeric inputs with `Number()` before scoring to avoid string
  concatenation.
- Default nullish values explicitly: `({{Text}} || "")`, `({{List}} || [])`,
  `Number({{Score}} || 0)`.
- Avoid object spread, `Object.assign`, `_.assign`, and `_.merge` on complex
  enrichment objects. Wrap complex objects under a named property instead.
- Lookup columns usually return `{ records: [...] }`; process
  `{{Lookup}}?.records || []`.
- Filter List of Objects columns usually expose `.filteredArray`.
- Use `Clay.getCellStatus()` with capital `C`.

## Useful Sandbox APIs

Generally available:

- Lodash as `_`, including common array, object, string, grouping, sorting, and
  aggregation helpers.
- Moment as `moment`, including formatting, comparison, `diff`, `startOf`,
  `endOf`, `isBefore`, `isAfter`, `isBetween`, and durations.
- `JSON.parse()` and `JSON.stringify()`.
- `Math`, `Number`, `String`, `Boolean`, `Date`, `encodeURIComponent`,
  `decodeURIComponent`, `btoa`, `new URL()`, `Array.isArray`, `Object.keys`,
  `Object.values`, and `Object.entries`.

Known traps:

- `atob()` is not available.
- Backtick template literals are unreliable.
- Regex `.replace()` is unreliable; prefer `.split("x").join("y")`.
- `.replaceAll()` is unavailable; use split/join.
- `_.template()` is unavailable.
- FormulaJS and Moment plugins are unavailable in formula columns.
- `matchAll()` returns an iterator and is usually not useful.

## Formula Workflow

1. Identify desired output type: boolean, number, string, object, or array.
2. List each input column and whether it may be blank, string-stored JSON, an
   enrichment object, a lookup result, or an array.
3. Check for known traps before writing.
4. Write the smallest expression that produces the output.
5. Add defensive defaults and optional chaining.
6. For complex logic, split into helper Clay columns rather than forcing a huge
   expression.
7. Provide one or two sample-row expectations for validation.

## Patterns

Simple conditional:

```javascript
{{Employee Count}} >= 500 ? "Enterprise" : "SMB"
```

Numeric scoring:

```javascript
Number({{Score A}} || 0) + Number({{Score B}} || 0) + Number({{Score C}} || 0)
```

Safe nested access:

```javascript
{{Enrich Person}}?.experience?.[0]?.company || ""
```

Lookup processing:

```javascript
({{Lookup Multiple Rows}}?.records || []).map(r => r?.name).filter(Boolean)
```

Array to comma-separated text:

```javascript
({{People}} || []).map(p => p?.name).filter(Boolean).join(", ")
```

Global string replacement:

```javascript
({{Company Name}} || "").split(", Inc.").join("").trim()
```

Status gate:

```javascript
Clay.getCellStatus({{Find Work Email}})?.toLowerCase() === "success"
```

Safe JSON parse for string-stored JSON:

```javascript
{{Payload}} ? JSON.parse({{Payload}})?.field || "" : ""
```

Wrap complex enrichment data:

```javascript
[{ enrichPersonData: {{Enrich Person}}, selected: true }]
```

## Debugging

Yellow triangle or cannot evaluate:

- Remove `return`, declarations, function wrappers, and template literals.
- Add optional chaining to every object/property access.
- Replace regex `.replace()` with split/join.
- Check whether lookup data lives under `.records`.
- Split the logic into helper columns if it is too dense.

Blank or undefined output:

- Confirm the referenced column has a value on the sample row.
- Default null values with `||`.
- Check casing and exact column names inside `{{...}}`.
- For lookup and filter columns, inspect `.records` or `.filteredArray`.

`[object Object]` output:

- Use `JSON.stringify()` when the target should be text.
- Explicitly select subfields when the target should be a scalar.

Concatenated numbers such as `315502`:

- Wrap every scoring input in `Number()`.

## Quality Gate

A Clay formula answer is ready when:

- it is a single Clay-compatible expression;
- all column references use `{{Column Name}}`;
- blank and null inputs are handled;
- nested data uses optional chaining;
- lookup/filter result wrappers are handled when relevant;
- numeric math uses `Number()` where inputs may be strings;
- the expected output type is stated;
- sample validation rows or edge cases are named.

## Output Contract

When using this skill, return:

- the final Clay formula expression;
- the expected output type;
- any assumptions about input columns or data shape;
- sample-row validation notes;
- any reason to split the logic into helper columns.
