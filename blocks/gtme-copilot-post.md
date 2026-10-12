# GTME Copilot Post

| Field | Value |
| --- | --- |
| Id / version / status | `gtme-copilot-post` · v1 · global, 2026-10-08 |
| What it does | Tells the account's GTME, in their copilot Slack channel, that the play reached out |
| Inputs | The GTME's Salesforce User id (from Route & Score), the message text |
| Outcomes | `posted`, `skipped_no_gtme`, or `failed` (logged on the run, [Write Failure](write-failure-alert.md)) |
| External writes | Slack message. Undo: delete the message |
| Pins | Clay action `send-message-to-channel-botname`, package `ad402586-6ea0-418c-8f42-3eae964728e9`. Channel from `User.Copilot_Channel__c` |
| Consumers | Closed-Won lookalike `T10A`. Closed Lost re-arch `21A. GTME Co_pilot`. Verified against the live graphs 2026-10-08 |
| Was | card 38 (the field map) |

## Core

1. Read the GTME's `User.Copilot_Channel__c` with one SOQL read on `User`, together with the ClayDR's email.
2. If there is no GTME, skip the post. That is not a failure, and the run continues.
3. Post with `send-message-to-channel-botname`: channel is the copilot channel, `summary` is the message, the bot name is the play's name, the emoji is `:clay:`.
4. The post is separate from the Action Queue. Neither one feeds the other.
5. [Test Mode](test-mode.md) swaps the channel to Ethan's `#__copilot_ethanh` (`C0BP3JTNNCF`).

## Parameters

| Parameter | Meaning | Values today |
| --- | --- | --- |
| `bot_name` | Name shown on the post | Closed-won `Closed-Won Look-alike` |
| `message` | The text. Ethan owns the copy | per play |
| `required_for_count` | Whether a run counts as sent only when the post went out | Closed Lost re-arch: required when a GTME owns the account and on test runs. Closed-won: optional |

## Must Not

- Do not hold the run when there is no GTME.
- Do not use `Push HiL to Terra` or `Send Simple Insight to Terra` for this line. Those are Terra cards.

## Lessons It Prevents

- An early draft made the action queue wait for the post. A missing GTME would have removed the ClayDR's to-do.

## Decisions

Closed Lost re-arch D42 (no GTME is not a hold). Closed-won 2026-10-08 ("yes this is fine" for the no-GTME case).
