---
name: workflow-change-review
description: Review workflow or DAG changes for downstream impact, renumbering, stage grouping, stale references, crossed paths, and layout regressions. Use before adding, removing, moving, merging, or renaming workflow nodes, or for a retrospective on repeated workflow formatting failures. Produces an impact map and repair plan; not a live builder or workflow runner.
status: active
maturity: trial
metadata:
  version: "0.1.0"
  maturity: "trial"
---

# Workflow Change Review

## Role

Turn a node-level request into a complete, reviewable workflow change. Separate
required dependency repair from optional renumbering. Explain repeated failures
from evidence rather than blaming concurrency without a reproduction.

This is a portable review process. It has no required connector, repository,
model vendor, sibling skill, or automatic graph-rewrite engine.

## Boundaries

- Review is read-only by default; local review artifacts are allowed. Invocation
  does not authorize workflow edits, tests that spend credits, external writes,
  or publication. A separately authorized implementation uses the reviewed plan.
- Start from the latest confirmed user decisions and target project contract;
  they override this skill's naming/layout defaults. Historical receipts are
  evidence, not automatically current instructions.
- Inspect available API/CLI or saved exports first. Use a browser only for a
  named gap such as rendered wire paths, within the environment's permissions.
  Missing tools or auth are unknowns, not permission to invent results.
- Reuse existing validation, material hashes and test harnesses after checking
  their coverage. Do not claim this skill installs a lock or enforces every
  direct UI/CLI edit. Do not add another framework for a one-off review.

## Workflow

1. **Pin the scope.** Record requested changes, current decisions, source
   commit plus dirty-file identity, workflow/workspace, draft or published
   snapshot, and capture time as available. State absent evidence. If reviewers
   work in parallel, give them the same captured candidate.
2. **Map responsibilities and identity.** Distinguish business stages,
   executable nodes, repeated executions, retired cards, and presentation-only
   headings. Record stable logical/platform IDs separately from mutable display
   addresses and names. A name used by routing code is an executable dependency.
3. **Trace the complete impact.** Read
   [change-impact.md](references/change-impact.md) for structural changes or
   recurring failures. Inspect consumers, bindings, schemas, edges, transitions,
   stage membership, headings, current docs and tests. Include references
   outside the visually downstream lane and shared dependencies.
4. **Prepare the naming/layout decision.** Read
   [naming-and-layout.md](references/naming-and-layout.md). Removing a node does
   not necessarily remove a stage. Preserve valid existing addresses unless
   renumbering is explicitly approved. Before changing other existing addresses,
   present the exact old-to-new map and ask once whether to compact or retain
   gaps. An already approved map needs no second confirmation.
5. **Specify one coherent repair.** Include unambiguous reference and membership
   repairs in the authorized change scope. Do not invent replacement data or
   bypass a deleted gate. Name unresolved semantic decisions. A candidate with
   dangling references, duplicate addresses or unintended backward ordering
   remains unapplied until resolved; these are not cosmetic gaps.
6. **Define verification for this version.** Separate semantics, references,
   naming, native geometry, runtime and synchronization. Inspect full visible
   inventory for layout and the affected dependency paths for runtime. Reuse
   captured real cases first; use labeled synthetic cases for missing edge
   conditions. Historical tests or simulated geometry cannot certify a current
   native workflow. Leave absent evidence unknown.
7. **For an authorized application, verify the handoff.** Recommend one writer,
   a fresh base comparison, stable-ID matching, scoped mutations and full
   readback. Detect conflicting writes before and after application; a
   cooperative lease alone does not prevent UI races. Recheck changed evidence
   and deliver a link to the exact draft/published state actually verified.

For a retrospective, stop at findings and the proposed repair plan unless fixes
are separately requested. Reconstruct a short timeline; distinguish proved
causes, code-path risks and hypotheses; list what is already fixed versus open.
Use bounded offline reproductions where useful. Do not estimate saved time or
attribute a live failure solely from a hypothetical test.

## Checks

- Every impacted active node has one intended stage membership and a unique
  address under the selected naming policy; approved exceptions are explicit.
- Deletion does not leave stale bindings, routes, expected paths or outcome
  references. Name changes update exact operational consumers together.
- Source labels, visible names, current maps and group titles agree. Preserve
  historical receipts and their original names with an alias/lineage map.
- Headers remain non-executable. Layout preserves actual dependencies, native
  port meanings and approved section/bridge exceptions; actual wire/card
  geometry is inspected when making a visual acceptance claim.
- Proof matches the inspected material version. Display-only edits refresh
  presentation proof; behavior/contract/operational-name edits refresh affected
  node and path proof. Unchanged evidence is reused only with matching identity.
- Review success never substitutes for implementation, runtime proof or
  authorization. Report source, draft and publication separately.

## Output Contract

Use [the review template](assets/change-review-template.md), scaling detail to
the change. Return: scope and candidate identity; findings with evidence and
severity; impact map; required repairs versus optional naming changes; the one
concrete confirmation needed, if any; checks performed/skipped; separate
verdicts and the next safe action. No broad renaming question without the map.

The skill starts at **trial** maturity. Validation and example reviews test its
instructions, not platform-wide enforcement or native runtime correctness.
