# Claygent Web Research Prompts

Source imported from `/Users/ethanhuang1/Downloads/claygent-web-research.skill`
on 2026-06-10.

Use this reference when a Claygent prompt should browse the public web, run
searches, visit source pages, and return structured facts or classifications.
Do not use it for prompts that only transform existing row inputs.

## When To Use

Use a web-research Claygent prompt when the row needs new public evidence:

- company, person, job, market, funding, location, or technology facts;
- source-backed classification from public pages;
- evidence URLs for human review;
- recency-sensitive research;
- disambiguation where the row inputs are insufficient.

If the prompt only classifies titles, parses supplied text, scores an account
from existing columns, or rewrites content, use `claygent-content-manipulation.md`
instead.

## Authoring Workflow

1. Confirm inputs, desired outputs, output format, source expectations, and edge
   cases.
2. Summarize the research logic before writing the final prompt when the task is
   ambiguous or consequential.
3. Choose the search style:
   - prescriptive for specific facts such as address, revenue, domain, employee
     count, official page, or job listing;
   - open for judgment tasks such as business-model fit or signal assessment;
   - hybrid for controlled classifications that need definitive sources first
     and flexible fallbacks second.
4. Write source priority and conflict rules before examples.
5. End with a direct output instruction such as `Return ONLY the JSON object`,
   then embed the full JSON Schema object in `OUTPUT FORMAT`. Do not leave the
   schema as a separate artifact.
6. Validate output field names, null behavior, evidence URLs, and examples.

## Prompt Sections

Use these sections for production prompts:

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
RESEARCH METHODOLOGY
==========================================

==========================================
KEY DEFINITIONS
==========================================

==========================================
DECISION RULES
==========================================

==========================================
EDGE CASES
==========================================

==========================================
CONFLICTING DATA POLICY
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
      "enum": ["Current", "Not Current"]
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

Omit `KEY DEFINITIONS` or `DECISION RULES` only when the task is pure extraction
with no controlled classification.

## Research Method Pattern

For specific facts:

```text
### Phase 1: Official Sources
1. Visit the provided official URL or domain when available.
2. Check relevant pages such as About, Careers, Contact, Press, Leadership,
   Blog, Legal, Pricing, Docs, or Product.
3. Extract only facts visible on pages you visit.

### Phase 2: Authoritative Third Parties
Run simple searches such as:
- "COMPANYNAME" headquarters
- "COMPANYNAME" leadership "PERSONNAME"
- site:linkedin.com/in "PERSONNAME" "COMPANYNAME"
- site:sec.gov "COMPANYNAME" 10-K

### Phase 3: Supplementary Sources
Use reputable news, directories, job boards, databases, and cached snippets only
as fallback evidence. Do not let a weaker source override a stronger source.
```

For judgment tasks:

```text
Start with the official website to understand the entity, then cross-reference
with recent third-party evidence. Use the source hierarchy and decision rules
below. Stop when there is enough evidence to satisfy the output contract.
```

## Source And Conflict Rules

- Every factual output must come from a source visited during the run.
- Do not infer, guess, or rely on model memory.
- Copy exact identifiers, names, URLs, and numbers from sources when exactness
  matters.
- Prefer official/company sources for positioning and product facts.
- Prefer regulatory filings, official registries, or primary databases for
  legal, financial, and ownership facts.
- Prefer current person-level sources over old bios, stale event pages, or
  generic snippets for employment facts.
- When sources conflict, use the stated hierarchy and add the strongest evidence
  URL. If conflict remains material, return the fallback enum or an empty field
  rather than overclaiming.

## Null Policy

For downstream Clay fields, use:

- strings: `""`;
- booleans: `false`;
- arrays: `[]`;
- objects: `null` only when the schema intentionally permits it;
- enum classifiers: the exact fallback enum from the output contract.

Avoid `"N/A"`, `"Unknown"`, `"Not Found"`, and prose substitutes unless one is
an explicit enum value.

## Formatting Rules

- Input labels in definitions: `snake_case`.
- Clay filler variables in pasteable templates: `ALLCAPS`, no braces.
- Output JSON fields: `camelCase`.
- Examples, edge cases, and output schema must use identical field names and
  casing.
- Return JSON only when downstream columns parse the result. No markdown fences.
- Embed the full JSON Schema object in `OUTPUT FORMAT`. Examples must match it.
- Do not deliver schema as a separate chat block.

## Failure Checks

Before delivering, check for:

- passive wording that could make Claygent echo inputs;
- missing "do not output the input data" instruction;
- output examples that do not match the schema exactly;
- JSON Schema delivered outside the prompt instead of inside `OUTPUT FORMAT`;
- no evidence/source URL fields when review needs proof;
- source priority that is too vague to resolve conflicts;
- missing stop condition, causing web-research sprawl;
- null behavior that would break formulas;
- overbroad search queries for common names or ambiguous companies.
