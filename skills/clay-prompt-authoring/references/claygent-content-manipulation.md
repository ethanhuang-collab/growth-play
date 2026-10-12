# Claygent Content Manipulation Prompts

Source imported from
`/Users/ethanhuang1/Downloads/claygent-content-manipulation.skill` on
2026-06-10.

Use this reference when a Claygent or Use AI prompt should process only the data
already supplied in row inputs. These prompts should not browse, search, or
claim facts beyond the linked inputs.

## When To Use

Use content-manipulation prompts for:

- title, persona, seniority, segment, ICP, or eligibility classification;
- parsing supplied article text, job descriptions, emails, notes, JSON, or CSV
  excerpts;
- scoring or tiering accounts from existing enrichment outputs;
- merging several upstream payloads into a review summary;
- validating input quality or consistency;
- transforming content into a different structured format.

Use `claygent-web-research.md` instead when the prompt must find new public
evidence.

## Authoring Workflow

1. Confirm inputs, output fields, output format, domain rules, edge cases, and
   whether a reference file or spreadsheet defines the taxonomy.
2. Declare that the task has no internet access and must use only provided
   inputs.
3. Put the reasoning contract before examples: categories, priority order,
   thresholds, tie-breaks, inclusions, and exclusions.
4. Add null and conflicting-signal behavior.
5. Use examples that include input, compact reasoning, and exact output.
6. Validate field names, enums, casing, and downstream parse shape.
7. Embed the JSON Schema object in `OUTPUT FORMAT`. Do not return schema as a
   separate chat artifact.

## Prompt Sections

```text
==========================================
OBJECTIVE
==========================================

==========================================
INPUT DEFINITION
==========================================

==========================================
INPUT DATA
==========================================

==========================================
CLASSIFICATION OR REASONING RULES
==========================================

==========================================
EDGE CASES
==========================================

==========================================
CONFLICTING SIGNALS POLICY
==========================================

==========================================
NULL RESULT POLICY
==========================================

==========================================
OUTPUT FORMAT
==========================================

Return ONLY a valid JSON object matching this schema. No markdown, no code
fences, no commentary. Do not echo the input data.

JSON Schema:
{
  "type": "object",
  "additionalProperties": false,
  "required": ["status", "reason"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["Allowed Value A", "Allowed Value B"]
    },
    "reason": {
      "type": "string"
    }
  }
}

This schema object is also the Clay column JSON schema. Do not invent a second
schema.

==========================================
EXAMPLES
==========================================

==========================================
FINAL VALIDATION
==========================================
```

For narrative outputs, replace `CLASSIFICATION OR REASONING RULES` with
`SYNTHESIS INSTRUCTIONS` and specify the markdown or text shape.

## Required Objective Language

Include a direct source-boundary sentence:

```text
This is a content manipulation and reasoning task. You do NOT have access to
the internet. Base your answer only on the input data and rules below.
```

Use similar wording even when the user calls the column Claygent. It prevents
the prompt from wasting time on web search or inventing facts.

## Classification Pattern

Use priority order when categories can overlap:

```text
Evaluate in this order. Once a confident match is found, stop and return that
category.

### Priority 1: [Category]
Include when:
- ...
Exclude when:
- ...

### Priority 2: [Category]
Include when:
- ...
Exclude when:
- ...

Fallback:
Return `[Fallback Enum]` when the evidence is missing, contradictory, or does
not satisfy any category.
```

Put hard exclusions before positive matches. Examples:

- `Executive Assistant to CMO` should not match `CMO`.
- `Product Manager` should not match generic people management just because it
  contains `Manager`.
- A company appearing only in past experience should not count as current.

## Scoring Pattern

For scoring prompts, define components and thresholds explicitly:

```text
### Score Components
Component A: 0-3 points
- 3 if ...
- 2 if ...
- 0 if ...

Component B: 0-2 points
- 2 if ...
- 0 if ...

### Tier Thresholds
- Tier 1: total score >= 5
- Tier 2: total score >= 3
- Tier 3: total score < 3
```

Never ask the model to "score based on fit" without weights, thresholds, and
tie-breaks.

## Synthesis Pattern

For multi-payload summaries:

```text
1. Read each input payload.
2. Extract only evidence present in the payloads.
3. For each signal, record presence, severity, source field, and confidence.
4. Resolve conflicts using the policy below.
5. Produce the exact JSON or markdown shape requested.
```

## Null Policy

- Use `""` for missing strings.
- Use `false` for missing booleans.
- Use `[]` for missing arrays.
- Use the fallback enum only when that enum is part of the taxonomy.
- Do not emit `"N/A"` or `"Not Found"` for downstream-consumed fields.

## Formatting Rules

- Input labels: `snake_case`.
- Clay filler variables in templates: `ALLCAPS`, no braces.
- Output JSON fields: `camelCase`.
- Examples must match the output contract exactly.
- JSON outputs should be JSON only, with no markdown fences or commentary.
- Embed the full JSON Schema object in `OUTPUT FORMAT`. Examples must match it.
- Do not deliver schema as a separate chat block.

## Failure Checks

Before delivering, check for:

- missing no-internet/source-boundary instruction;
- classification rules without priority order;
- inclusion lists without exclusions;
- edge cases that do not name exact output;
- examples that show reasoning but mismatched JSON;
- vague fallback behavior for sparse or contradictory inputs;
- output fields that do not match the configured Clay output fields or schema;
- JSON Schema delivered outside the prompt instead of inside `OUTPUT FORMAT`.
