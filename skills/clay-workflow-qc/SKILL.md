---
name: clay-workflow-qc
description: Run a portable, read-only Clay workflow QC specialist review of pins, bindings, schemas, graph transitions, intake mapping, pagination, retry behavior, and side-effect gates. Use for technical Clay workflow inspection or as a single independent lane under qc. Not a table discovery router, live builder, or bulk test runner.
status: active
maturity: trial
---

# Clay Workflow QC

## Role

Provide one technical Clay workflow review lane. This distills the downloaded pressure-test plugin's Clay checklist and replaces the clay-expert router's unavailable specialist/MCP assumptions with explicit discovery of installed tools. It is not a full replacement for the original clay-expert router.

## Boundaries

- One reviewer owns this lane. Under `qc`, return findings to the parent; do not create nested agents.
- Read-only by default; local report files are allowed. Do not run nodes/workflows, spend enrichment credits, mutate bindings, enable writes, publish or fix findings.
- Load current repo instructions, scope and workflow acceptance contract. Resolve material source conflicts before a readiness conclusion.
- Before selecting test evidence, read [the global real-data and early-permission rule](../../shared/coding/qc-steering.md). Use representative real cases; label saved replay versus fresh execution. A reviewer reports any missing action-specific approval to the parent immediately; this skill remains read-only.
- Prefer configured read-only API observers and supported Clay CLI commands. Discover capabilities from installed documentation/help; do not invent endpoints, register an obsolete MCP, or assume missing tools are installed. Verify the selected workspace before CLI reads where the project requires it. Missing auth is a blocker, not permission for browser fallback.
- Keep original plugin files intact. This portable specialist uses the session's inherited model and does not claim the original vendor-specific protocol.
- Route individual run/provider failures to `clay-platform-troubleshooting`, prompt-specific review to `clay-prompt-authoring`, and credential/data boundaries to `security-review` only when relevant. Load a named installed skill before using it. Do not assume clay-atlas or inspector-360 exists.

## Workflow

1. Record the workflow/workspace IDs, intended business behavior, current holds, candidate commit/dirty-file or snapshot identity and evidence capture time. Use a parent-provided immutable bundle when running alongside another reviewer; do not silently fetch a different candidate.
2. Inspect saved node schemas, input pins/source node IDs/source paths, automapping, tool-output paths, transition names and conditions, intake fields and downstream consumers. Check optional/missing/null outputs and undeclared fields that consumers need.
3. Trace branch reachability, explicit terminal outcomes, failure handling, paginated reads, identity reconciliation, duplicate/retry behavior, concurrency and external-write guards. Distinguish preparation from verified delivery. Never treat a create response as saved-content verification.
4. Inspect relevant structural warnings, stale agent/tool versions and shared mapping dependencies. A valid graph is not runtime proof; classify warnings by demonstrated impact.
5. Reuse repository-native validators and recorded tests after inspecting what the commands do. Run only offline/read-only checks within the authorized scope. Keep semantic, naming, layout and runtime verdicts separate. Use a current positional snapshot for layout checks and rendered evidence when required; saved coordinates alone do not prove wire appearance.
6. Review representative captured runs against independent expectations. State whether evidence is static inspection, mock execution, recorded replay or live readback. Do not claim current runtime acceptance from historical reports.
7. Write the independent report before reading a sibling report. The parent deduplicates findings; fixes remain a separate authorized task.

## Checks

Tie findings to stable node IDs and source evidence. Preserve current business decisions and external-write holds. Missing evidence remains unknown. No technical review changes permission to test, send, publish or supersede data.

## Output Contract

- Candidate identity and freshness; actual model if known; tools used.
- Separate semantic, naming, geometry and runtime verdicts: pass, concerns or unknown.
- Findings by severity with node ID, file/line or snapshot path, reproducible failure path, proposed fix and smallest safe check.
- Known held dependencies versus new defects; relevant warnings; what looks correct.
- At most 10 prioritized actions, performed/skipped checks, and residual risk.

## Resources

See [provenance](references/provenance.md). Invoke `$clay-workflow-qc` explicitly or use it as an optional domain lane under `$qc`.
