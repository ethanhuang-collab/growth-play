---
name: clay-prompt-authoring
description: Author, edit, debug, and validate production Clay Use AI and Claygent prompts, including Claygent public web research prompts that search sources and verify evidence URLs, content manipulation prompts that do not browse, chip wiring, prompt input contracts, required/unrequired inputs, output fields, JSON Schema, single-value classifiers, Claygent source and stop rules, outbound copy prompts, and sample-row test/refine loops.
status: active
maturity: maturing
last_matured: 2026-08-21
---

# Clay Prompt Authoring

## Role

Use this skill when the user needs a Clay prompt written, consolidated, debugged,
or productionized for a Use AI or Claygent column.

This skill owns:

- prompt wording and structure;
- input labels and Clay chip wiring;
- required versus optional input policy;
- JSON Schema and output-field shape;
- null/default behavior;
- hard gates, exclusion rules, and deterministic decision rubrics;
- Claygent search/source/stop rules;
- sample-row tests and prompt refinement.

## Boundaries

Use `clay-platform-troubleshooting` when the main issue is provider behavior,
run state, waterfalls, credit burn, auth, plan gates, CRM sync, webhooks, or
external writes. Bring the work back here only when the specific fix is prompt
wording, chips, schema, or Claygent instructions.

Use `sheet` or Clay formula guidance when the user is building a formula column
or checkbox/data-type expression. If the user is using Clay's "Generate" button
for a formula, provide plain-English formula instructions rather than pretending
the prompt box will execute code.

Use `clay-search-query` when the task is a Clay Search advanced query for people,
companies, or jobs. Claygent web research is not Clay Search.

Use `clay-handoff-doc-generator` or `clay-quality-assessment` for handoff docs
or client-facing QA reports. This skill can improve the prompts inside those
workflows, but it does not own the full table architecture.

Do not bulk-run, sync, enrich, or write externally as part of prompt authoring.
Prompt QA should stay on a small sample unless Ethan explicitly approves more.

## Core Principle

Write prompts as reusable input contracts, not as prose glued to exact column
names.

Define the linked inputs once in an `## Inputs` section. After that, refer to
semantic labels such as `LinkedIn`, `Original company`, `Enriched org`,
`Person name`, or `Work email`, instead of repeatedly embedding exact Clay
column references throughout the rules.

Global default: put the `## Inputs` section at the bottom of the prompt, as
the last section after `## Output`. Ethan links the actual Clay chips there.
Only move Inputs elsewhere if Ethan explicitly asks.

Draft plain text first, then resolve chips. Trying to write prose and wire Clay
chips at the same time usually causes menu mistakes and brittle prompts.

## Standard Workflow

1. Classify the prompt job.
   - `single_value_classifier`: returns one enum such as `Current` or
     `Not Current`.
   - `structured_extraction`: returns JSON fields or arrays.
   - `entity_match`: compares person/company/domain/title evidence.
   - `research_agent`: uses Claygent or web research.
   - `outbound_copy`: writes subject/body or persona-specific copy.
   - `meta_prompt`: prompt for another prompt generator.

   If the prompt is a Claygent web research task, read
   `references/claygent-web-research.md` for source hierarchy, search strategy,
   conflict handling, and anti-hallucination checks. If the prompt only
   manipulates row inputs without browsing, read
   `references/claygent-content-manipulation.md` for no-internet source
   boundaries, priority-ordered classification, scoring, and synthesis patterns.

2. Define the output contract before writing the prompt.
   - Name every output field.
   - Decide enum values exactly.
   - Decide null/default behavior.
   - Decide whether the output is one value, plain text, or JSON.
   - If the column is Claygent and returns structured JSON, write the JSON
     Schema first and embed that schema object in the prompt `OUTPUT FORMAT`
     section. Do not keep the schema as a separate chat artifact.

3. Define the input contract.
   - List every linked input once.
   - Use semantic labels, not hardcoded Clay column names, unless Ethan asks for
     exact chip names.
   - Mark inputs required only when blank values should block the row.
   - For optional inputs, state how to behave when they are blank.

4. Add test cases before finalizing consequential prompts.
   - Include one happy path.
   - Include one sparse/null row.
   - Include one ambiguity or false-positive row.
   - Include one known-bad row that should be rejected.
   - For generated prompts, ask the prompt generator for validation tests before
     asking for the final prompt with JSON Schema already inside `OUTPUT FORMAT`.

5. Draft the prompt with the smallest complete structure.
   - `## Goal`
   - `## Source Boundary` or `## Research Instructions`, if relevant
   - `## Decision Rules` or `## Extraction Rules`
   - `## Hard Exclusions`, if relevant
   - `## Final Validation`
   - `## Output` (for Claygent JSON outputs, this section must contain the
     JSON Schema object, not a prose field list)
   - `## Inputs` (always last — global default)

6. Wire chips after drafting.
   - Replace placeholders one by one from Clay's slash menu.
   - Keep readable labels outside chips.
   - Confirm each inserted reference is a real chip, not copied text.
   - Scan for leftover `{placeholder}` or `{{typed_reference}}` text.

7. Test the same sample rows after every prompt/schema edit.
   - Inspect parsed output fields, not just whether the cell ran.
   - Confirm enums, nulls, arrays, evidence URLs, and confidence fields.
   - Make the smallest change that fixes the observed failure.

## Prompt Shapes

### Single-Value Classifier

Use when downstream formulas need one clean value.

```text
## Goal
Decide [specific decision].

Use only the linked inputs provided. Do not browse.

## Decision Rules
Return `Allowed Value A` only if [strict condition].

Return `Allowed Value B` if:
- [condition]
- [condition]

If evidence is missing, conflicting, or ambiguous, return `Allowed Value B`.

## Output
Return exactly one value:

Allowed Value A

or

Allowed Value B

## Inputs
Use the provided inputs for:
- [semantic input]
- [semantic input]
```

Use this for current-employment checks, title eligibility, suppression gates,
persona classifiers, and "same company?" checks. Avoid explanations unless a
separate reason field is explicitly needed.

### Structured JSON Extraction

Use when downstream columns need multiple fields.

Prompt rules:

- Return JSON only.
- No markdown, commentary, prefaces, or code fences.
- Field names must match the output schema exactly.
- Use exact enums.
- Use `null`, `false`, `[]`, or `""` consistently based on downstream needs.

Minimal schema pattern:

```json
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
```

When a Use AI cell returns one flat blob instead of nested fields, fix the
configured output fields or JSON Schema. Do not try to solve a schema-shape
failure only with prose.

### Embedded JSON Schema (Claygent)

For every Claygent prompt that returns structured JSON, embed the JSON Schema
inside the prompt `OUTPUT FORMAT` section. That object is the single source of
truth for the model, the pasteable prompt, and Clay's column JSON schema field.

Required contents of `OUTPUT FORMAT`:

- `Return JSON only. No markdown, no code fences, no commentary.`
- The full JSON Schema object (`type`, `properties`, `required`,
  `additionalProperties`, enums).
- Null/default notes that match the schema.

Then put one or more filled instances in `EXAMPLES` using the same keys, types,
and enums. An annotated example object may follow the schema to show allowed
enum strings, but it does not replace the schema.

Do not:

- deliver JSON Schema as a separate chat block outside the prompt;
- describe output fields only in prose when the column returns JSON;
- invent a second schema in wiring notes; tell Ethan to paste the schema
  already inside `OUTPUT FORMAT` into the Clay column JSON schema field.

Skip embedding only when the Claygent output is a single enum, boolean, or
plain-text string with no parsed fields.

### Claygent / Web Research

Use Claygent prompts when the row needs public research, not just source-bounded
analysis.

For production Claygent web research prompts, load
`references/claygent-web-research.md` before drafting the final prompt. Keep the
main answer compact unless the user asks for a full prompt template.

Add:

- source priority;
- search queries or search strategy;
- allowed and disallowed sources;
- recency/freshness standard when relevant;
- stop conditions;
- evidence requirements when downstream review needs proof;
- failure behavior when evidence is missing.

Template:

```text
## Goal
Use public web research to [specific task].

## Research Instructions
1. Check person-level LinkedIn or official/company sources first.
2. If the known URL is blank, broken, or not person-level, search the web using
   the person name plus the original company and role.
3. Prefer the most recent person-level source.
4. Do not use company pages, old bios, stale speaker pages, or generic search
   snippets as stronger evidence than a newer person profile.
5. Stop once enough evidence exists to make the requested output decision.

## Output
Return JSON only. No markdown, no code fences, no commentary.

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

## Inputs
Use the provided inputs for:
- Person name
- Original company
- LinkedIn
- Work email
```

For Claygent, do not let research sprawl. The prompt should say what to search,
what counts as proof, when to stop, and what to do when proof is unavailable.

### Content Manipulation / Reasoning

Use content manipulation prompts when the model should only classify, parse,
score, synthesize, or transform linked row inputs. Load
`references/claygent-content-manipulation.md` when the prompt needs detailed
taxonomy, scoring, synthesis, edge-case, or no-internet guardrails.

These prompts should explicitly state that they have no internet access and must
use only the supplied inputs. Use priority-ordered rules for classifications and
explicit component weights for scoring.

### Entity Match / Current Employment

For employment validation, compare current company evidence to the original
target company. Past experience does not count as current employment.

Rules to include:

- Compare company identity, not title relevance.
- Minor punctuation, legal suffix, abbreviation, casing, brand, and parent
  company differences are okay.
- If the original company appears only in past experience, return not current.
- If the current org is blank, conflicting, or too vague, return not current.
- If the enriched profile appears to be the wrong person, return not current.
- Email domain may support a decision, but it cannot override newer profile
  evidence showing a different current employer.

### Outbound Copy Prompts

For outbound copy, prefer deterministic formulas when persona branches are
known. If an AI prompt is needed:

- separate subject line and body into separate outputs or columns;
- define persona, offer, proof, CTA, and banned phrasing;
- do not overfit weak personalization;
- do not invent company-specific facts;
- avoid limp openers such as "thought this might be relevant";
- output send-ready copy only, with no commentary;
- keep first-step emails short unless Ethan explicitly asks for a longer asset.

## Required Inputs

Mark an input required only when the prompt cannot produce a useful result
without it. Required blank inputs block the row from running.

Use required for primary identifiers:

- company name/domain when company identity is the task;
- person name or LinkedIn when person identity is the task;
- candidate list when ranking candidates;
- source text when extracting from source text.

Use optional for helpful context:

- description, notes, industry, geography, employee count;
- prior enrichment result;
- secondary URLs;
- fallback evidence.

For optional inputs, include missing-input behavior:

```text
If Additional context is blank, ignore it and rely on the primary identifiers.
Do not mention that the field was missing.
```

## Null And Default Policy

Define null/default behavior explicitly in production prompts.

For downstream-consumed Clay fields:

- strings: `""` unless schema intentionally permits `null`;
- booleans: `false`;
- arrays: `[]`;
- objects: `null` when no selected record exists;
- enum classifiers: use the exact fallback enum, such as `Not Current` or
  `Unclear`.

Avoid `"N/A"`, `"Unknown"`, `"Not found"`, or prose substitutes in fields used
by downstream formulas.

## Hard Gates

Use hard gates before positive matching when the task can false-positive on
keyword overlap.

Examples:

- `Executive Assistant to CMO` should not match `CMO`.
- `Total Rewards` should not match customer loyalty/rewards.
- `company LinkedIn page` should not count as a person LinkedIn profile.
- A company mentioned in past experience should not count as current employer.

Put hard exclusions before title waterfalls, persona assignment, candidate
ranking, and outreach eligibility.

## Troubleshooting

Flat blob output:

- Add or fix the JSON Schema / output fields.
- Confirm the schema object is inside the Claygent prompt, not only in chat.
- Ensure the prompt says JSON only.
- Remove markdown fences, prose wrappers, and extra commentary.
- Model arrays and nested objects explicitly.

Wrong chip or missing input:

- Check that chips are real Clay references, not typed `{{...}}` text.
- Check for blank required inputs.
- Reinsert wrong chips one by one from the slash menu.
- Keep labels outside chips.

Prompt returns too much:

- Make the output contract smaller.
- Use single-value classifiers where possible.
- Move evidence/reason into separate optional fields only when needed.

Prompt is noisy or inconsistent:

- Add a hard gate.
- Add deterministic tie-breaks.
- Add null behavior.
- Split unrelated jobs into separate columns.
- Tighten source priority and stop conditions.

Formula/checkbox column is showing prompt text:

- This is not a prompt-quality issue. The Clay column is likely in text/static
  mode or the data type cannot coerce the output.
- If using Clay's Generate box, give plain-English formula instructions.
- If using a formula editor, ensure the output type is a real boolean, number,
  or text value matching the column data type.

## Quality Gate

A Clay prompt is ready when:

- the job type and output contract are explicit;
- input labels are chip-agnostic and linked once;
- the `## Inputs` section is the last section of the prompt (global default);
- required/optional inputs are intentional;
- hard gates run before positive matches;
- JSON/schema fields match prompt field names exactly;
- Claygent JSON prompts embed the JSON Schema object in `OUTPUT FORMAT`;
- the chat reply does not attach a second schema block for Ethan to copy;
- null/default behavior is stable for downstream formulas;
- Claygent prompts include source priority and stop rules;
- sample rows include normal, sparse, ambiguous, and known-bad cases;
- the same sample rows pass after the final edit.

## Output Contract

When using this skill, return:

- the prompt or prompt section to paste, with JSON Schema already inside
  `OUTPUT FORMAT` when the Claygent column returns structured JSON;
- chip-wiring notes that point at that embedded schema rather than repeating it;
- the required/optional input guidance when relevant;
- sample test cases or QA notes for production prompts;
- any unresolved Clay setup risk, such as chip wiring or formula data-type mode.
