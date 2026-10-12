---
name: gtm-play-qc
description: Run a portable, read-only GTM play pressure test. Use for GTM play QC, targeting and selection risks, lifecycle routing, suppression, cooldown, messaging honesty, or activation readiness. A focused business reviewer that can run as one independent lane under qc; not a replacement for test execution or technical workflow QC.
status: active
maturity: trial
---

# GTM Play QC

## Role

Review whether a GTM play's selection, timing, messaging and handoff deliver its stated business promise. This is a portable adaptation of the Cursor gtm-play-pressure-test plugin's GTM lens, not its original dual-vendor execution protocol.

## Boundaries

- One reviewer performs this lane. Under `qc`, return findings to the parent; do not spawn a nested review team.
- Use the session's inherited model. State the actual model when known, otherwise mark it unavailable. Never claim Claude/Grok or vendor diversity without those actual executions. If the user explicitly requests the original cross-vendor review, load that installed plugin and verify model availability instead of silently adapting it.
- Read-only: no workflow runs, enrichment, enrollment, activation, provider calls that spend credits, external writes or fixes. Local report files are allowed. Running this skill is not permission to run the target workflow.
- Follow the target project's confirmed scope, evidence standards and acceptance rules. Do not promote one project's stage labels, exceptions or approvals into this skill.
- Use `qc` for overall readiness and `clay-workflow-qc` for Clay wiring. Use existing troubleshooting skills for a concrete failed run.

## Workflow

1. Identify target, audience, business promise, source universe, record grain, intended outcomes, suppression rules, ownership and send/write policy from current project evidence. Ask only for material missing decisions; do not invent them.
2. Record candidate identity: commit plus dirty-file hashes or captured candidate hash, workflow/snapshot/version and capture time when available. Missing fresh state limits the verdict to the inspected artifact.
3. Review entry criteria against the promise; persona/title fit; identity and deduplication; uncertainty; in-flight records; cooldown/race risks; fallbacks; evidence recency; messaging honesty; attribution; handoff ownership; volume and backfill behavior.
4. Separate business Wait/no-action outcomes from errors and missing ownership. Check that review notes do not accidentally authorize outreach or make a usable artifact unusable contrary to the project contract.
5. Trace concrete counterexamples through the candidate. Prefer captured real cases and independently specified expected outcomes. Label hypothetical cases and uncovered behavior; do not manufacture execution proof.
6. Return an independent report before reading sibling findings. The parent reconciles disagreements using the same candidate and confirmed decisions.

## Checks

Every material claim has node/field/file evidence or is marked a hypothesis. Separate known holds from regressions. A passing business review is not runtime proof or external-write approval.

## Output Contract

- Scope and candidate identity; evidence freshness; actual model if known.
- Verdict for inspected scope: pass, concerns, or unknown.
- Targeting/selection; operations/enrollment; messaging/outcome findings.
- Each finding: severity, evidence, concrete failure scenario, business consequence, smallest proposed fix and safest verification.
- What looks sound; at most 10 prioritized actions; distinguish before-test from before-volume actions without granting permission to execute either.
- Checks performed, skipped checks, unknowns and residual risks.

## Resources

See [provenance](references/provenance.md). Invoke `$gtm-play-qc` explicitly or use it as an optional domain lane under `$qc`.
