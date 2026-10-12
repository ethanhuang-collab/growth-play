---
name: workflow-node-design
description: Challenge workflow node boundaries by business responsibility before planning, auditing, or restructuring an executable workflow.
status: active
---

# Workflow Node Design

## Rule

Before a detailed workflow plan or audit, map the business responsibilities to
the current or proposed nodes. Do not accept existing node boundaries merely
because the graph already runs or the user named one node to inspect.

Proactively propose a clearer split when responsibilities differ materially in
source evidence, inclusion rules, output, failure handling, or review decisions.
Make that recommendation during the audit; Ethan should not need to request the
architectural alternative after receiving only fixes inside the old structure.

## Check

1. Name the business jobs in plain language before choosing code, tool, or
   agent node types. Identify which jobs are hidden inside broad setup nodes.
2. Compare each population or decision's evidence, eligibility rules and output.
   Give materially different jobs independently inspectable node contracts.
   Distinguish these executable nodes from business stages: cohort judgments
   and their cleanup may deliver one stage's result through several nodes.
3. Keep reconciliation and cleanup explicit when multiple lists or decisions
   must become one dependable result. Define identity precedence, duplicate
   handling, missing/invalid decisions, exclusions, caps and complete accounting
   where relevant. Known hard rules belong in deterministic validation.
4. Map nodes to business stages by inspecting incoming execution dependencies
   and input bindings, not just names or predicates. Cleanup and validation
   within one stage take letters. A shared gate receiving independent business
   streams gets a new major number even if its predicate checks only one stream.
   After a split or merge, review the entire sequence and downstream names using
   [naming.md](naming.md); retain stable IDs and historical evidence.
5. For three or more sequential substeps in one stage, add the title-only
   stage header defined in [naming.md](naming.md). Keep the header out of
   executable nodes and preserve independently inspectable substeps. An existing
   numbered gate with lettered outcomes does not need a duplicate heading.
6. Show the smallest useful structure and explain the benefit, cost and binding
   changes. If existing boundaries are suitable, say briefly why.
7. Verify each node and the path through it. A visual split is not proof that
   the underlying rules, evidence or failure handling have been corrected.

## Numbered stage layout

Numbered workflow canvases and diagrams use **compact parallel lanes**. Inspect
the original layout and actual dependency edges before moving nodes. Within a
dependent path, stages and lettered sequential substeps progress top to bottom.
Independent branches from a shared stage start at the same vertical level, even
when their numbers differ; a larger number alone does not require a lower row.

For example, after stage 3, `4a → 4b → 4c` can implement one people stage in
a downward lane beside email `5a → 5b`, signals `6`, and calls
`7a → 7b`. Align starts `4a`, `5a`, `6`, and `7a`. If `5b`, `6` and `7b` join
at one gate, that shared stage is `8`, even if it checks call completeness;
place it below the three paths it waits for. Preserve actual dependencies.
These are illustrative stages, not a required template. An explicit user layout
overrides this default.

Preserve useful existing lanes and make local adjustments before considering a
wholesale reflow. When creating or inserting a node, place it in its lane and
dependency level, save the coordinates, and read them back; do not leave it at
the canvas's default bottom position. Verify saved path order, aligned branch
starts, and sibling spacing. Prefer API/CLI readback; if native wire/port geometry
is missing, name that browser gap and inspect the rendering after save/reload.
Follow the native checks in
[workflow-node-graph](graph/SKILL.md#native-clay-layout-verification).
Coordinates and downward edges do not prove uncrossed wires or card clearance.
Report unavailable checks as unknown, not zero. Immutable native ports outrank
fail-left/continue-right preferences; preserve their meanings and adjust layout.
Draft handoffs must open an explicit `?version=edit` link and verify the intended
workflow and draft state. Keep geometry, semantic identity and run QA separate.
Never add execution edges, change bindings, or rename transition targets merely
to achieve layout.
For Clay sibling placement and manual-position preservation, follow
[naming.md](naming.md).

## Boundaries

- Apply to executable workflow design, audits, reviews and restructuring. A
  factual question may be answered first; do not turn every lookup into a plan.
- An audit can recommend restructuring without authorization to modify live
  state. Existing mutation, prompt, test, publishing and external-write gates
  still govern implementation.
- Do not split mechanically by field or force a fixed number of nodes. Keep
  work together when its evidence, rules and outputs form one coherent job.
- A business-node split does not require an AI call per node. Use code for
  known rules and models only where judgment is needed; surface any cost change.
- Preserve project-specific vocabulary, cohort policies and approval rules in
  their owning repo. Do not promote one project's categories into a universal
  workflow template.
- Apply [naming.md](naming.md) after choosing responsibilities for a
  Clay graph; naming conventions do not substitute for this design check.

## Why

2026-09-14: an audit missed the useful split of people judgment and cleanup.
Later corrections distinguished business stages from executable nodes, restored
compact parallel lanes and required downstream numbering review. The shared
layout check still stopped at coordinates: it missed native port crossings and
a bypass edge behind a card despite the graph skill's renderer collision rules.
Native rendered-wire proof and draft-version handoff are separate requirements.
