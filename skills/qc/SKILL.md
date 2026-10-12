---
name: qc
description: Bundle quality control into a cohesive consolidated pass across code review, visual QA, security/data checks, domain specialists, repo-native checks, and independent subagent lanes. Use when the user asks to QC, quality check, final check, pre-merge check, smoke test, sanity check, ready-to-ship check, ship/no-ship judgment, verify done-ness, or inspect work before shipping; automatically compose with subagent-orchestration for non-trivial QC instead of waiting for the user to ask for subagents.
status: active
maturity: trial
---

# Quality Control

## Role

Use this skill to decide whether work is actually ready to ship. QC is an
orchestrator: it maps the changed surface, selects the relevant specialist
skills, runs the verification paths, delegates independent review lanes to
subagents when useful, then synthesizes the result into a clear ship/no-ship
judgment.

QC is not "run tests and vibes." It is the cohesive final pass that makes the
right checks happen together.

## Boundaries

- Use `review` alone when Ethan asks only for code review findings.
- Use `tdd` when the request is specifically tests-first development or
  regression-test design.
- Use `root-cause-debugging` first when there is a concrete failing behavior
  and the cause is unknown.
- QC is read-only by default. Do not edit files, change app/workflow settings,
  click through destructive or write-like UI actions, rerun live workflow
  actions, sync external systems, or otherwise apply fixes during QC unless
  Ethan explicitly asks you to make the change.
- Use `build` only after Ethan explicitly asks to implement the fix or clearly
  changes the request from QC/reporting into execution.
- Keep tiny, obvious checks in the parent thread. Do not create a subagent ritual
  for a one-file typo or a single command.

## Test evidence

Follow [Test data preference](../../shared/coding/qc-steering.md#test-data-preference):
start with representative real records or captured runs, check expected outcomes
independently, and add synthetic cases only for named coverage gaps. Report data
origin and distinguish replay evidence from connected or live execution proof.
This selects evidence; it does not itself trigger concentric sample expansion.

## QC Bundle

Start every QC pass with a target map, then invoke the relevant parts of the
bundle.

Target map:

- Changed surface: files, routes, PR, artifact, data flow, deployment, or plan.
- User-facing risk: UI, copy, workflow, dashboard, document, email, Slack, or
  API behavior a recipient will experience.
- Correctness risk: business logic, state, async flow, parsing, data contracts,
  tests, migrations, or generated artifacts.
- Trust boundary: auth, secrets, permissions, PII, external APIs, webhooks,
  scheduled jobs, LLM tools, or customer data.
- Verification path: nearest native commands, browser proof, screenshots,
  fixture/repro, snapshot/export render, or manual smoke path.
- Repo hygiene and lineage: dirty files, generated noise, branch/PR state,
  scope drift, merge/rebase/split decision, and smallest next PR boundary.

Core bundle:

| Surface | Skill or path | Use when |
|---|---|---|
| Correctness review | `review` | Diffs, PRs, implementation plans, edge cases, regressions, maintainability. |
| Test quality | `tdd` | Behavior changes need tests, regression tests, or coverage-gap analysis. |
| Bug diagnosis | `root-cause-debugging` | QC finds or starts from a reproducible failure. |
| Visual behavior | `frontend-visual-qa` | Frontend, dashboard, chart, screenshot, export, responsive layout, clipping, or browser interaction. |
| Security | `security-review` | Auth, permissions, secrets, webhooks, cron/API routes, data exposure, dependencies, or LLM/tool paths. |
| Repo pulse | Native commands | Lint, typecheck, tests, build, smoke checks, or project-specific verification. |
| Fixes | `build` | A scoped fix should be made after the issue is understood. |

Shared gates:

| Gate | Use when |
|---|---|
| `definition-of-done` | The ship target or acceptance criteria are fuzzy. |
| `agent-task-scope` | The QC target needs a scope card or has drift risk. |
| `verification-todo-gates` | Verification must be named before edits continue. |
| `post-agent-closeout` | Agent-written work, broad diffs, risky surfaces, or skipped checks need closeout fields. |
| `context-hygiene` | Search, logs, docs, or review evidence could flood the parent thread. |
| `subagent-delegation` | Independent lanes should be delegated with clear contracts. |
| `loop-breaker-protocol` | Repeated failures or stuck checks need a smaller diagnostic loop. |
| `narrow-adapters` | QC reveals a repeated manual/browser/API ritual that should become a small adapter. |

Domain specialists:

| Surface | Add these skills when relevant |
|---|---|
| Website or product UI | `frontend-visual-qa`, `ux-quality-assessment`, `website-making`, `visual-design-and-brand` |
| Dashboard or chart | `dashboard`, `professional-graph-making`, `metric`, `data-semantics` |
| SQL, sheets, or data contracts | `sql`, `sheet`, `spreadsheets`, `data-semantics`, `metric` |
| Operational API, cron, webhook, queue, or automation | `operational-automation-api-builder`, `security-review`, `llm-shadow-mode-safety` when AI is involved |
| Slack bot or integration | `slack-bot-builder`, `security-review`, native Slack/plugin checks when available |
| Clay workflow artifact | Relevant `clay-*` skill plus schema/data checks, canvas/graph topology, and `visible-terminal-branches` |
| Slide, document, or spreadsheet deliverable | `slide-making`, `documents`, `spreadsheets`, brand/domain skill, and rendered/export QA |

Only invoke domain specialists that match the target map. Do not turn QC into a
grab bag of unrelated skill names.

## Optional GTM and Clay review lanes

For a GTM play implemented as a Clay workflow, add `gtm-play-qc` for targeting,
timing, messaging and operational outcomes, and `clay-workflow-qc` for graph,
bindings, schemas and side-effect gates when those risks apply. These are
portable, separately named adaptations of installed Cursor plugins. They do not
require a particular model vendor or missing sibling skills.

Use one independent reviewer per selected lane, both on the same identified
candidate/evidence bundle. No nested agent teams. Keep native tests, node-level
acceptance, visual evidence and final readiness judgment in this QC process.
A specialist opinion never substitutes for execution proof, a required human
acceptance ledger, or authorization for live actions. Record unavailable evidence
as unknown. If the user explicitly asks for the original dual-vendor Cursor
pressure test, verify its requested models instead of silently substituting these
portable lanes.

## Numbered workflow acceptance

For numbered workflows, load the canonical
[node naming](../../shared/coding/clay-workflow-node-naming.md) and
[node design](../../shared/coding/workflow-node-design.md) rules. Review the
complete current candidate: normalized unique addresses, independent operation
boundaries, title-only headers for long sequential stages, dependency/lane order,
fixed-port meanings, and native wire coverage. Headers are presentation objects;
do not count or test them as executable nodes. Existing numbered gates do not
need duplicate stage titles. Keep semantic, naming, geometry and runtime
verdicts separate and report missing evidence as unknown. A saved historical
graph or successful coordinate readback cannot establish current acceptance.

## Planner Harness Opportunity

For broad diffs or recurring release checks, use a QC planner harness to inspect
the target surface and propose lanes: code review, native verification,
frontend/browser proof, security/data boundary review, repo hygiene, and domain
specialists. The harness should emit a compact JSON/Markdown plan with skipped
lanes and reasons.

Keep the ship/no-ship judgment in this skill. A planner harness can prevent
missed lanes, but it cannot decide whether evidence is good enough to ship.

## Concentric Coverage Expansion

Ethan ruling 2026-08-19 (origin: aa-visual-intake overlay QC). When QC
verifies a population by sampling — images, lesson records, generated
artifacts, data rows — expand coverage in concentric rings instead of
trusting one sample:

1. Start with a small ring (5-10%) to validate the check itself before
   scaling it.
2. Each ring must pass the same bar before expanding (e.g. 10% -> 30% ->
   100% for corpora, 5% -> 15% -> 40% for expensive verification).
3. A failed ring stops expansion: remediate, re-run that ring with a fresh
   seed, and only then widen.
4. Disclosed or flagged defects still count as fails — the bar measures
   genuine quality, not documentation coverage.
5. Zero-miss populations (evidence stores, gallery promotions) expand to
   100%; capping coverage lower is an Ethan decision, not a default.

## Steering

When a user asks for QC, final check, smoke test, or ready-to-ship confidence:

1. Treat it as a consolidated QC effort, not a single review mode.
2. Announce the QC bundle in one sentence: review, tests, visual/browser,
   security/data, domain specialists, and native verification as applicable.
3. Use subagents automatically for non-trivial QC lanes. Ethan should not need
   to say "use subagents."
4. Keep the parent thread responsible for target mapping, lane selection,
   subagent prompts, synthesis, recommended fixes, and the final ship/no-ship
   call.
5. If the target map shows a lane is irrelevant, skip it explicitly and briefly.
6. For live tools and customer/workflow surfaces such as Clay tables, CRMs,
   sequencers, automations, webhooks, or production dashboards, inspect and
   diagnose only. Report the issue, cause, recommended fix, and safest test
   plan; wait for an explicit execution request before making the change.
7. When the selected QC bundle includes browser proof and the default local
   browser path is blocked, immediately offer to open Chrome and retry there.
   Treat "prompt to open the real browser" as the default recovery path for
   browser-dependent QC instead of quietly falling back to code-only evidence.

## Automatic Subagents

For non-trivial QC, compose with `subagent-orchestration` automatically. A
request routed to `qc` is a request for this bundle, including read-only
subagent passes when the gate below is met. The parent agent owns target
selection, integration, final judgment, and any edits.

Use read-only subagents by default when at least one is true:

- the diff spans multiple files, modules, or behavior surfaces
- test output, logs, or build output would be noisy
- frontend/browser QA and code review can run independently
- security, data, or auth boundaries deserve a fresh pass
- the user asks for final confidence before merge, ship, handoff, or deploy

Suggested split:

- Diff reviewer: inspect the changed behavior for correctness, edge cases,
  maintainability, regressions, and missing tests. Use `review`.
- Verification runner: discover and run the nearest useful lint, typecheck,
  tests, build, or smoke commands; summarize failures with the smallest likely
  cause. Use `tdd` for test-gap judgment and `root-cause-debugging` for failures.
- Visual/product QA: render desktop/mobile or fixed-format proof for UI,
  dashboard, chart, website, slide, document, or export surfaces. Use
  `frontend-visual-qa` and relevant domain design skills.
- Security/data boundary reviewer: inspect only sensitive boundaries involving
  auth, secrets, permissions, PII, webhooks, APIs, cron jobs, LLM tools, or data
  contracts. Use `security-review` plus domain data/automation skills.
- Repo hygiene reviewer: for broad diffs or PR prep, inspect status, generated
  noise, scope drift, branch/merge state, and smallest next PR boundary. Use
  `post-agent-closeout` as the checklist.
- Domain specialist: only when the target map calls for it, run a focused pass
  for dashboards, charts, SQL, spreadsheets, Slack bots, Clay workflows, docs,
  slides, or operational automations.

Start write-capable subagents only when fixes can be split into disjoint file
ownership. Tell every worker not to revert user changes or other agents' work.

Use `templates/qc-subagent-scope.md` for the scope card when multiple lanes are
needed.

## Workflow

1. Identify the QC target: diff, branch, PR, files, route, artifact, plan, or
   pasted code.
2. Build the target map: changed surface, user-facing risk, correctness risk,
   trust boundary, verification path, and repo hygiene/lineage state.
3. State the bundle you will run: core skills, domain specialists, native
   checks, and skipped lanes.
4. Decide whether automatic subagents pass the gate. If yes, create a compact
   scope card using `templates/qc-subagent-scope.md`.
5. Run parent-thread checks that block lane selection, then delegate independent
   lanes in parallel where helpful.
6. Inspect the target and run the nearest useful commands or browser checks.
   If browser verification is required and the in-app/local path fails, ask to
   open Chrome before concluding that live proof could not be gathered.
7. If failures appear, diagnose enough to distinguish product bugs, test/setup
   problems, and unrelated pre-existing failures.
8. Report findings and recommended fixes. Do not apply fixes as part of QC
   unless Ethan explicitly asks for execution after seeing the issue/solution.
9. If Ethan asks for fixes, switch to `build`, apply the scoped change, and
   re-run the failed or changed verification path.
10. Synthesize a ship/no-ship judgment with evidence and residual risk.

## Stacked visual feedback (chart/layout)

When the user gives **layout + metric + color** requirements across multiple
turns, or rejects with a screenshot ("this is not what I want"):

1. **Re-read the full constraint set** — do not treat the latest message as a
   patch on the previous wrong interpretation. List every requirement explicitly
   before editing again.
2. **Disambiguate overloaded words** — "legend on the right" may mean band
   identity rail per chart, category legend column, or swatch-left inside legend
   rows. Confirm which before ship (`donut-chart-convention` multi-band pattern).
3. **Verify metric grain** — caption text, slice labels, center overlay, and
   footer totals must use the same entity (project vs use case vs dollar). Run
   `data-semantics` grain check when any number is user-facing.
4. **Do not ship on code review alone** — run `frontend-visual-qa` or capture
   proof that shows: slice labels, center hole, legend/rail placement, and colors.
5. **Screenshot rejection = do not ship** until a new proof matches every listed
   constraint. A passing typecheck is not sufficient.

**Incident pattern (Services Impact ARR-band donuts, 2026-06):** first pass
passed lint but failed user intent on four independent axes (wrong slice metric,
totals below chart, far-right category legend instead of per-chart band rail,
distinct hues instead of blue ramp). QC should have caught any one of these with
a constraint checklist + render proof.

## Workflow graph topology (Clay, DAGs, posters)

Do not QC a node graph against the plan text alone. Open the canvas or graph
summary and count named branch labels (Enterprise, SMB, Disqualified, default,
no-match). Each label must have a visible downstream node.

"No action needed" / no write-back is still a node: a labeled skip or noop,
not a silent `endRunOnNoMatch` drop. A CLI run that ends cleanly without that
node is not a pass. Follow `shared/shipping/visible-terminal-branches.md`.

**Incident pattern (Booking.com inbound Clay workflow, 2026-08-25):** QC passed
the plan's "no Disqualified node" reading. The canvas only showed Enterprise
and SMB. The miss was visual topology, not enrich/qualify mappings.

## Output Contract

Lead with:

- Ship status: `ship`, `ship with caveats`, or `do not ship`
- Findings by severity, with file/line evidence when available
- Recommended solution for each actionable finding, including the safest
  smallest test when the fix touches live systems or external writes
- Target map and selected QC bundle
- Skills/paths invoked
- Subagents used, or why the parent stayed local
- Verification run
- Repo hygiene, scope drift, and branch/PR decision when relevant
- Residual risk
