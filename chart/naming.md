---
name: clay-workflow-node-naming
description: Clay workflow canvas node names — one number per business stage, letters for its executable substeps. Use when creating, renaming, restructuring, or documenting Clay workflow nodes.
status: active
---

# Clay Workflow Node Naming

## When the graph is written

Apply this rule while writing `workflow-plan.md`, before that page is shown and before any node is created in Clay. A decision buried as a letter of the previous stage is not ready for review. The lookalike graph failed this on 2026-10-08: `1F Any targets?` and `1G Log: no lookalikes` should have been stage `2`, outcome `2A`, outcome `2B`, and the next work at `3`. The naming file had not been opened until after the nodes existed.

## Rule

Each **number identifies one business stage**, not one model call. A shared
topic is insufficient: preparation producing evidence and a decision consuming
it can be separate jobs. Cohort judgments and cleanup can be distinct nodes
within one coherent stage. Inspect responsibilities, incoming execution edges,
and input bindings before assigning numbers; titles alone cannot define stages.

A singleton is `N. Name`. Two or more substeps use `Na`, `Nb`, …, whether
sequential operations or exclusive outcomes. No lone `Na`, `Na2`, or `N.1`.
Every distinct executable node needs a unique address independent of its title:
`5a. Count emails` and `5A. Prepare pages` collide. Compare case-insensitively;
internal labels may normalize uppercase. Accept bare stage numbers; reject
zero, leading-zero stages and malformed suffixes. Repeated executions retain
one address; physically separate retry nodes need separate addresses.

A business admission gate owns a numbered stage and lettered outcomes, including
three or more: `18. Assignment decision` → `18a. Assigned` / `18b. Unassigned` /
`18c. Needs review`. Preparing its context is a separate preceding operation.
Internal validation may remain lettered within its stage. A shared gate joining
independent streams starts a new number even if its predicate checks one stream:
email `5b`, signals `6`, calls `7b` → gate `8`, not `7c`.

## Same task across parallel scenarios

Global preference confirmed by Ethan on 2026-09-15: when the same task is
applied to different scenarios at the same branch/dependency level, keep one
stage number and assign sibling letters: `15a`, `15b`, `15c`. Place these
scenario variants horizontally, left to right, at the same vertical level;
include the scenario in each title, such as `15a. Create Notion page — renewal`
and `15b. Create Notion page — reactivation`. Do not assign separate major
numbers solely because the scenario differs.

This applies across workflow plans, diagrams, and node labels, not only to
Closed Lost or Notion. Distinct business jobs still get distinct stage numbers.
Existing same-stage sequential substeps may still use letters vertically;
letters alone do not imply parallel execution. Determine horizontal siblings
versus vertical progression from actual dependencies. Never turn dependent
steps into siblings or add dependencies just to satisfy visual alignment.

## Patterns

| Shape | Names |
| --- | --- |
| Singleton | `6. Signals + renewal window` |
| Cohort judgments and cleanup | `4a. Judge A` → `4b. Judge B` → `4c. Reconcile people` |
| Fetch and cleanup | `5a. Fetch emails` → `5b. Clean emails` |
| Gate outcomes | `2. Gong present?` → `2a. Skip` / `2b. Continue` |
| Simple router outcomes | `12. Play router` → `12a. Renewal` … `12d. Wait` |

A branch performing a new business job gets its own stage; branching alone does
not establish that. `1. Unpack` followed by `1a. Gong present?` wrongly hides a
new gate. A people/email/signals/calls consolidator cannot be `4b` of one stream.

## Title headers for long stages

For **three or more sequential executable substeps**, put a **title-only header
above the chain**: `5. Email gatherer`, then `5a`, `5b`, `5c`, and so on. Count
an actual same-stage directed chain, not array order, descendants, disconnected
nodes, or alternatives. One/two substeps need no extra title. A bare numbered
gate already supplies its heading; `18 → 18a / 18b / 18c` gets no competing `18`.

A header is presentation metadata: no executable node, bindings, transitions,
run status, per-node tests, or new dependencies. Keep every substep visible.
Never create an empty code/tool node or hide distinct jobs behind the title.
Use a frame/group or annotation. Clay documents named canvas groups; verify
workspace availability and membership restrictions before using them. If native
grouping cannot safely represent the title, preserve the graph, show the header
in the review diagram, and report the native gap. Never rewire to force a group.

## Renumbering after changes

After any split, merge, insertion or removal, review the whole stage map and keep
numbers consecutive. `4 → 5 → 6` becoming `4a → 4b → 4c` requires downstream
renumbering too. Build a stable-ID → old-name → new-name map for current canvas
names, plans, diagrams, references and tests.

Audit exact consumers: `context.transition_to("…")`, name-keyed outputs/lookups,
and generated bindings. Update destinations and transition strings together;
check duplicate addresses/names and stale references, read back and rerun affected
checks. Never blanket-replace: preserve unrelated CRM values, prompt instruction
numbers, versions, thresholds and business data. Preserve IDs, edges/bindings,
historical snapshots, hashes and dated reports; record lineage instead of
rewriting history. Old passing evidence cannot prove a renamed version.

## Layout and acceptance

Follow `workflow-node-design.md` and the graph skill. Dependent paths run down;
independent branches start together in compact parallel lanes, numerically left
to right. Sequential letters progress downward; equal siblings run a/b/c left
to right. Higher numbers do not impose a universal row. Preserve useful lanes;
an explicit user layout wins.

Prefer fail/skip left and continue right, but **immutable native ports outrank
position defaults**. Preserve meanings, bindings and targets; document the
exception. Never invent execution edges for visual order. After manual placement,
do not run `graph format`; update node `position` and verify saved readback.

API/CLI comes first. Missing native wire/port geometry is a named browser gap.
Inspect actual wires, ports, bypass paths and card clearance after reload;
coordinates alone cannot pass visual QA. Draft links use verified `?version=edit`,
not an uninspected default/published view.

After changes, review the complete current candidate, including visible disabled
and disconnected cards. Bind its responsibility map, headers, addresses,
dependencies, port meanings and native coverage to the same workflow/version.
Report naming, geometry, semantic and runtime verdicts separately; missing
proof is unknown. Historical regressions are not current acceptance. Use
repo-owned checks; a fingerprint identifies supplied evidence, not its truth.
The local presentation reviewer is not a platform lock or automatic coverage of
raw CLI/UI edits. Existing mutation, run and publish permissions still apply.

**Mermaid diagrams in plans and overviews:** label a node (`id["7A. Name"]`)
where it first appears; every later mention, including a join target, is the
bare id. A bare mention before the label renders as the id in some viewers
(closed-won lookalike, 2026-10-08: a join showed `c5D`). `lifecycle/overview.py
--check` flags this in `overview.md` and `workflow-plan.md`. A collapsed range
(`7 to 18`) is not a node name.

**Test-mode color.** A test-mode node swaps owner, prospect, assignee, and
channel for a non-live route, or otherwise only exists to keep a test away from
a real person. Paint only those nodes green on every house diagram (Ethan,
2026-10-08; amber before that). Orange is reserved for external writes:

```
classDef testMode fill:#D6F0D8,stroke:#3C8A46,color:#123D18
class <id> testMode
```

The live Clay canvas has no color field on a node or a group (confirmed
2026-10-08). A diagram color is not a canvas color.

## Why

Repeated stage/label confusion and coordinate-only QC missed native crossings.
The correction combines explicit responsibilities, unique addresses, readable
stage titles, and evidence for the current complete graph.

## Maintenance

Canonical for all tools; compressed plugin guidance must not override it.
Cursor pointer: `~/.cursor/rules/clay-workflow-node-naming.mdc`. This copy ships with the lifecycle kit.
Native verification: `graph/SKILL.md`.
