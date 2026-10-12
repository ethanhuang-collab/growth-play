# Global Blocks Check

Final pass, 2026-10-08. Plan: `clay-planning-system/docs/plans/2026-10-08-global-blocks-notion-page-retro.md` part A. Live graphs read with `clay workflows graph get <wf> --mode summary` (and `--mode full` for Test Mode) on 2026-10-08: Closed Lost re-arch `wf_0tmkil3sfFqBBisk58p`, Closed-Won lookalike `wf_0tmkl1aqG4iDXsUpgxN` (one workflow, `T`-prefixed target labels). Nothing on a live play was changed.

## Cards

| Card | Header | Core | Parameters | Must Not | Lessons | Decisions | Consumers verified | Fixed in this pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Suppression](suppression.md) | yes | yes | yes | yes | yes | yes | 2026-10-08 | Consumers named `T1A`–`T2A`, `4A`–`4F`, `5C` |
| [Best Ranked Contacts](best-ranked-contacts.md) | yes | yes | yes | yes | yes | yes | 2026-10-08 | Lessons added. Consumers `T3A`–`T3F` |
| [Route & Score](route-and-score.md) | yes | yes | yes | yes | yes | yes | 2026-10-08 | Consumers `T5A`–`T5D`. Core 4 links Test Mode |
| [Gong Enrollment](gong-enrollment.md) | yes | yes | yes | yes | yes | yes | 2026-10-08 | Consumers `T7B`–`T8B`. Links to Write Failure and Test Mode |
| [Action Queue](action-queue.md) | yes | yes | yes | yes | yes | yes | 2026-10-08 | Consumers `T9A`/`T9B`. Links to Write Failure and Test Mode |
| [GTME Copilot Post](gtme-copilot-post.md) | yes | yes | yes | yes | yes | yes | 2026-10-08 | Consumers `T10A`. Links to Write Failure and Test Mode |
| [Campaign Member](campaign-member.md) | yes | yes | yes | yes | yes | yes | 2026-10-08 | Lessons added. Link to Write Failure |
| [Write Failure](write-failure-alert.md) | yes | yes | yes (none) | yes | yes | yes | 2026-10-08 | Parameters and Lessons added. Consumers list the four write blocks and their nodes |
| [Test Mode](test-mode.md) | yes | yes | yes (none) | yes | yes | yes | 2026-10-08 | Parameters and Lessons added. Consumers name the three Closed-Won code nodes `T5D`, `T7B`, `T7D` |

Route & Score and Action Queue carry extra sections before Core (how the function works, the case). The six parts are present and in order on every card.

## Index And Cross-References

- `README.md`: nine rows, one file each, the "Not global" sentence present, no row without a file.
- Every `](...md)` link in this folder resolves.
- Suppression points to Campaign Member; Route & Score points to Test Mode; the four write blocks point to Write Failure; Gong Enrollment, Action Queue, and GTME Copilot Post point to Test Mode.

## Pointers On Older Cards

| Older card | Points to | State |
| --- | --- | --- |
| `graph/16-gong-enrollment.md` | gong-enrollment | present |
| `graph/17-attribution.md` | campaign-member | present |
| `graph/20-write-failure-alert.md` | write-failure-alert | present |
| `graph/39-best-ranked-contacts.md` | best-ranked-contacts | present |
| `graph/40-account-contact-suppression.md` | suppression | present |
| `graph/41-test-module.md` | test-mode | present |
| `functions/38-copilot-channel.md` | gtme-copilot-post | present |
| `functions/36-attribution-terra-functions.md` | campaign-member, action-queue | added 2026-10-08 |
| `graph/13-notion-page.md` | pointed to a `global/notion-recap.md` that does not exist | replaced 2026-10-08 with the "not global" line |

## Proposals, Not Done Here

These files were dirty from another thread on 2026-10-08, so the pointer is written here for whoever owns that edit.

| File | Pointer it needs |
| --- | --- |
| `functions/33-route-and-score.md` | `> For new plays, use the global block [../global/route-and-score.md](../global/route-and-score.md). This card is the earlier function note.` |
| `graph/18-terra-action-queue.md` | `> For new plays, use the global block [../global/action-queue.md](../global/action-queue.md). This card tied the queue to a Campaign Member id; the global card does not.` |
| `graph/09-contact-pick.md` | Optional. `> For new plays, the pick is [../global/best-ranked-contacts.md](../global/best-ranked-contacts.md). This card is Closed Lost v7's deal-people pick.` |
| `../README.md` (building-blocks) | The first paragraph lists "Notion Recap" among the global blocks. It is not one (kit decision D38). Remove the word. |

## Retro Card Diffs After The Pass

Applied the same night from `clay-planning-system/docs/reviews/2026-10-08-*-retro/verdict.md`. None touches a Core section.

| Commit | Card | Change | Finding |
| --- | --- | --- | --- |
| `6dcded4` | Gong Enrollment | Closed-won `sequence_rule`; Must Not and Lesson on test instances left on a withdrawn flow | Closed Lost re-arch F10, Closed-Won F9 |
| `e52a88e` | Campaign Member | Decisions: the write is kit D34; play D41 is the read side | Closed Lost re-arch critic B4 |
| `54e18b1` | Best Ranked Contacts | Parameters `fallback`: closed-won hands the main workspace contributor to the Claygent when the workspace has no rows | Closed-Won F8 |

## Core Left For Ethan

No card's Core was changed. Two Core questions came out of the retros and wait for Ethan (`clay-planning-system/docs/reviews/2026-10-08-*-retro/parked.md`):

- Route & Score Core 2 says a blank GTME alone is not a reason to call, but live Closed Lost `6A` calls `6B` when either owner is blank, and D42 says Force Route is always true on that call while live `6B` passes it only when the ClayDR is blank. Either `6A` narrows or Core 2 widens.
- Best Ranked Contacts steps 3 and 5: on Closed-Won, a non-empty list where everyone is ineligible made the Claygent answer with a plain string and the node fail twice (Damco). Whether that failure is the accepted exit on live, or the shared Claygent's prompt changes, is Ethan's and the block owner's call.

No Core conflict was found between the cards and the live graphs read today beyond those two.
