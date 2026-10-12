---
name: clay-platform-troubleshooting
description: Troubleshoot Clay.com workflow operations, enrichment runs, waterfalls, Claygent/web research behavior, CRM Sync, webhooks, HTTP API columns, credits, billing or plan/feature access gates, provider errors, connected-account auth, field mapping, idempotency, sample-row tests, external write approval, and platform-specific failures. Use when a Clay workflow is slow, expensive, blocked, failing across rows, or unclear at the provider/run/sync/webhook layer rather than needing only prompt wording, hand-off docs, quality assessment, SOW, or brand assets.
status: active
maturity: trial
last_matured: 2026-05-19
---

# Clay Platform Troubleshooting

## Role

Use this skill when the problem is a Clay workflow operation rather than only a
Clay prompt. Typical triggers include unexpected credit burn, waterfall/provider
behavior, Claygent runs that wander or fail, CRM Sync issues, webhook or HTTP API
columns, plan/feature access, stuck runs, row-level errors, enrichment coverage
gaps, and uncertainty about whether a fix should happen in Clay, a connected
provider, or an external automation.

The goal is to diagnose the workflow surface, contain blast radius, test a small
representative row set, and return a practical fix path with credit and side
effect risks visible.

## Boundaries

- Use `clay-prompt-authoring` when the main issue is Use AI/Claygent prompt
  wording, chip wiring, required inputs, JSON Schema output, null policy, or
  row-level prompt refinement.
- Use `clay-quality-assessment` for a client-facing post-build QA document from
  CSV/schema/SOW inputs.
- Use `clay-handoff-doc-generator` for deployment documentation and hand-off
  docs.
- Use `clay-sow-generator` for scoping, commercial assumptions, or SOW language.
- Use `clay-search-query` when the task is writing or running a Clay Search
  advanced query rather than diagnosing a workflow, enrichment, or sync failure.
- Use `operational-automation-api-builder` when the fix becomes an external
  webhook/API/cron job outside Clay.
- Use `security-review` for credential handling, connected accounts, customer
  data exposure, or write access to CRM/marketing systems.
- Do not bulk rerun, sync, enrich, export sensitive data, or trigger external
  writes without an explicit approval gate.

## Intake

Collect only the missing fields needed to act:

```text
Clay troubleshooting intake

1. Workflow goal: What should the Clay table or workbook accomplish?
2. Failure surface: Prompt, provider/waterfall, Claygent, CRM sync, webhook/API,
   credits, plan gate, row state, permissions, or unclear?
3. Evidence: Error text, screenshots, affected columns, sample row IDs, run
   history, credits used, and what changed recently.
4. Scope: How many rows are affected? Is this one table, workbook, or connected
   downstream system?
5. Side effects: Would the next action enrich, spend credits, sync records,
   call a webhook/API, or update a CRM?
6. Proof target: What proves the fix worked? Parsed field, coverage rate,
   row count, sync status, credit delta, screenshot, or export?
```

Minimum viable intake before touching a live workflow:

- affected table/workbook or enough schema context;
- intended output and observed failure;
- whether the next step spends credits or writes externally;
- a small sample row set or permission to choose one.

## Support Ticket Clay Links

When a customer support ticket includes a Clay workbook, table, or view URL,
treat that link as live evidence to inspect, not only as context for a generic
reply. Prefer the read-only Clay API observer/API key path first for schema,
row, run-health, function/subroutine, and credit evidence. Use browser/UI
inspection only when the question is UI-visible, unavailable through the API, or
ambiguous from API evidence, such as a blank drawer, setup panel, visible header
order, modal state, login/session behavior, or screenshot-only symptom.

Before drafting the customer response, summarize what the live table actually
shows: table/workbook name, row count or sample size, relevant columns/actions,
function or subroutine graph when present, observed errors/statuses, and any
limits in what was observable. Do not ask for the same pasted table link again
unless the API/browser evidence is unavailable or multiple remembered links
could govern the ticket.

## Diagnostic Workflow

1. Classify the failure surface: input data, prompt/schema, provider/waterfall,
   Claygent/web research, run state, plan/feature gate, credit/billing, CRM
   sync, webhook/HTTP API, rate limit, permissions, or downstream system.
2. Contain blast radius. Avoid full-table reruns while diagnosing. Pick a
   5-50 row sample that includes normal rows, sparse rows, failing rows, and a
   known-answer row when available.
3. Check current Clay UI/docs/account state for feature access, connected
   account ownership, billing/credit visibility, and any plan-gated feature
   before promising that a workflow can run as designed.
4. Trace one row end to end: source inputs, formulas, enrichment/provider calls,
   waterfall fallbacks, Claygent instructions, output fields, downstream sync or
   webhook trigger, and final proof field.
5. Make credit impact visible before running. Inspect provider order, fallback
   conditions, duplicate enrichment columns, Claygent web research loops, rerun
   scope, and whether blank/low-quality inputs will fan out into expensive
   attempts.
6. Apply the smallest reversible change: adjust provider order, add row gates,
   fix formulas, tighten Claygent source/stop rules, repair auth, update object
   mapping, reduce the sample, or route the issue to prompt authoring.
7. Re-test on the same sample. Compare before/after outputs, row statuses,
   errors, credit deltas, evidence URLs, sync states, and downstream side
   effects.
8. Decide the durable fix: Clay configuration, prompt/schema edit, provider
   substitution, row-gating formula, connector reauth, webhook/API hardening,
   manual runbook, or external automation.

## Platform Checks

Waterfalls:

- Confirm the lookup objective, provider order, fallback conditions, and when a
  row should stop trying providers.
- Add row gates before expensive or low-confidence fallbacks.
- Test a representative sample before running the whole table.

Claygent and web research:

- Define source priority, stop conditions, evidence fields, and null behavior.
- Separate web research from deterministic formatting or scoring when the jobs
  need different inputs or proof.
- Inspect sources and parsed fields, not only whether a cell completed.

CRM Sync and external writes:

- Confirm object type, owner/account, field mapping, dedupe key, sync direction,
  update versus create behavior, and rollback path.
- Prefer sandbox/staging or draft states for first runs when available.
- Treat every CRM/marketing write as at least a reversible external write until
  proven otherwise.

Webhooks and HTTP API columns:

- Confirm current feature access, auth method, payload shape, idempotency key,
  rate limits, retry behavior, and error capture.
- Send the smallest safe sample first and preserve request/response proof
  without logging secrets.

## Quality Gate

A troubleshooting pass is ready when:

- the failure surface is named;
- credit and side-effect risks are explicit;
- the first test uses a bounded row sample;
- the before/after proof is concrete;
- the durable fix is assigned to the right owner skill, Clay configuration,
  connected provider, or external automation;
- any remaining blocker is named precisely, such as plan access, missing
  permissions, stale auth, provider outage, rate limit, or unsupported workflow.

## Output Contract

When reporting Clay table, column, action, field, source, or subroutine findings,
use the human-readable English name first. Include raw Clay IDs only as
supporting disambiguation in parentheses or a follow-up detail, not as the
primary label. For example, write `OUT - Email` before
`f_0tghg93K37rnm2rfkzF`, and write `Sandbox LinkedIn Profile URL subroutine`
before `t_0tghhduVB7EpQhgmqPa`.

End with:

- Workflow goal and failure surface
- Safety tier: read-only, credit-spending, reversible write, or high-impact
  external write
- Sample row plan and proof target
- Credit/plan/access risks
- Diagnosis and smallest safe test
- Durable fix recommendation
- Follow-up owner: `clay-prompt-authoring`, Clay configuration, connector
  reauth, external automation, security review, or human support/escalation
