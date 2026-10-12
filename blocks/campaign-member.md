# Campaign Member

| Field | Value |
| --- | --- |
| Id / version / status | `campaign-member` · v1 · global, approved 2026-10-08 |
| What it does | Writes the picked person onto this play's Salesforce campaign, right after Gong enrollment. That member is what stops the next run of the account |
| Inputs | The Gong flow id just used, and the picked person's Contact id |
| Outcomes | `member` written, or `failed` (logged on the run, [Write Failure](write-failure-alert.md)) |
| External writes | Salesforce `CampaignMember`, status `Sent`. Undo: delete the member |
| Pins | `[GTM Ops] Campaign Member LCU` `t_0t9kx1eahrfCiyDwwAX`. About 20 copies exist in the workspace; use this id |
| Consumers | Paid-alumni (reference). First real member: Janey Lee on `701a700001JcipOAAR`, Closed-Won run `wfr_b8b4d25d8217ee56eaf372fd58d4a7f6`, 2026-10-09. Closed Lost v7 (held). Closed Lost re-arch `24A` `wfn_0tmmc6josaJUtEAGAD9`, `24B` `wfn_0tmmc6qSMWXXcmWDSPj`. Closed-Won lookalike `T8C` `wfn_0tmmcq5JGYFY9kk8RSQ`, `T8D` `wfn_0tmmcq6hGJapmAEfRpi`, added 2026-10-08 |
| Was | cards 17 and 36 |

## Core

1. Run immediately after Gong enrollment, once per enrolled person. The path is Gong, then this block, then the action queue.
2. The member is the person the play picked, at that account. It is not the test seat. Ethan's contact is not on the customer account, so a member written for him would not stop the next run.
3. The campaign is the one for the flow just used. Manual and auto each have their own id.
4. Look up, then create or update. Status `Sent`. Final Status `Sent`. Notes and Qualification Status are the play's casual name.
5. A member on that campaign, for anyone at the account, inside the window, means the next run does not fire. That check is [Suppression](suppression.md).
6. A failed write stays on the run and does not un-count it. The run counts on the Gong enrollment, because the person is being emailed either way, and the ClayDR's to-do still follows. The failure is logged on the run, not posted to Slack (Closed Lost D38; Closed-Won version 9, 2026-10-09). The gap it leaves is in the dedupe: a daily read of Gong flow instances on the play's flows in the last 30 days with no member at that account is the repair list. That read is an operations check, not a node.

## Parameters

| Parameter | Meaning | Values today |
| --- | --- | --- |
| `campaign_by_flow` | Flow id (`flow=`) to campaign id. Never key this map on `flow-step-id=` | Closed Lost re-arch manual flow `7822886536753112041` → `701a700001Ji6srAAB`. Auto flow `7315015979702319623` → `701a700001JnAatAAF`. Closed-Won manual flow `2751667605583158577` → `701a700001JcipOAAR`. Auto flow `6248627259904112412` → `701a700001JcBleAAF`. Trial-extension manual flow `3893909031139751666` → `701a700001K2DBqAAN`. Auto flow `4519910719264475895` → `701a700001K2Lr7AAF`. Not `701a700001K2Ah0AAF`: that one holds the step id and a name ending in `:` |

The campaign ids this block maps come from [Campaign Setup](campaign-setup.md), which runs after the overview. The Gong ID on that form is the same `flow=` value this block keys on.

## Must Not

- Do not key `campaign_by_flow` on `flow-step-id=`. The Typeform rule is on [Campaign Setup](campaign-setup.md).
- Do not write the test seat as the member.
- Do not use an old campaign id. Closed Lost `701a700001GiKB2AAN` and `701a700001IDEwxAAH` are old versions.
- Do not read or set the campaign's `IsActive` checkbox. It is a lookup-menu setting and does not block a member write: 37 unchecked GTM Play campaigns took 4,425 members in the 90 days to 2026-10-09, and paid-alumni's campaign has 52 with the box unchecked. The 30-day window in Suppression is what "active" means (Ethan, 2026-10-09).
- Do not expect Gong to create the member. On 2026-10-08 all four campaigns had 0 members and a blank `Engage_Flow_Id__c`, after the Arcoro and Allen enrollments.

## Lessons It Prevents

- Arcoro and Allen & Company were enrolled in Gong on 2026-10-08 and no Campaign Member appeared on any of the four campaigns. Suppression's "already in this play" check had nothing to read, so this write became a block (kit decision D34).
- A member written for the test seat sits on Ethan's account, not the customer's, so it does not stop the customer's next run. Core 2 names the picked person.
- Closed Lost carried two old campaign ids (`701a700001GiKB2AAN`, `701a700001IDEwxAAH`) that a remade campaign left behind.

## Decisions

Ethan 2026-10-08: yes to the campaign member write. The write is kit decision D34. Closed Lost re-arch D41 is the read side (node `4C`, the already-in-play check), not the write approval.
