# Write Failure

| Field | Value |
| --- | --- |
| Id / version / status | `write-failure` · v2 · global, 2026-10-08 |
| What it does | Leaves a failed external write on the Clay run. No Slack message |
| Inputs | none. The failed node is the record |
| Outcomes | `failed`, visible on the run |
| External writes | none |
| Pins | none |
| Consumers | Every write block: [Gong Enrollment](gong-enrollment.md), [Campaign Member](campaign-member.md), [Action Queue](action-queue.md), [GTME Copilot Post](gtme-copilot-post.md). In Closed Lost re-arch those are `21B`, `24B`, `23A`, `21A`; in Closed-Won lookalike `T8A`/`T8B`, `T8D`, `T9B`, `T10A`. A failed write stops that branch and shows on the run. Verified against the live graphs 2026-10-08 |
| Was | card 20 |

## Core

1. A failed write is logged on the run. It is not posted to Slack.
2. The run is not marked sent when one of its writes failed.

## Parameters

None. Every play logs the same way.

## Must Not

- Do not add a Slack alert for a failed write.
- Do not end a run as sent when one of its writes failed.

## Lessons It Prevents

- Closed Lost v7 built a Slack alert for failed writes (card 20, D33, D34). Nobody wanted the message; Ethan withdrew it on 2026-10-08 and the run record is the alert.

## Decisions

Ethan, 2026-10-08: a failed write should just log. Kit decision D38. Earlier Slack alert: Closed Lost v7 D33, D34, withdrawn as a global block.
