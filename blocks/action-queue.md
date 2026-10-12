# Action Queue

| Field | Value |
| --- | --- |
| Id / version / status | `action-queue` · v1 · global, 2026-10-08 |
| What it does | Gives one person, normally the ClayDR, a Terra to-do for the contact the play just enrolled |
| Inputs | Assignee Salesforce User id, Contact id, Engage Flow ID, Engage Flow Instance ID, External ID. Optional: Campaign ID, Campaign Member ID, Touchpoint ID, E&S ID |
| Outcomes | `queued` with `SA Record ID`, or `failed` (logged on the run, [Write Failure](write-failure-alert.md)) |
| External writes | Salesforce `Signal_Action__c`. Terra reads it onto the assignee's to-do list. Undo: delete the Signal Action |
| Pins | Function `Add to Action Queue` `t_0tftcorryGVAimjzpWF`, view `gv_0tfb5brsfsY3JnNQ8FS` |
| Consumers | Closed-Won lookalike `T9A`/`T9B`. Closed Lost re-arch `23A. ClayDR Action Queue`. Verified against the live graphs 2026-10-08 |
| Was | cards 18 and 36 |

## How The Function Works

`Add to Action Queue` creates one Salesforce `Signal_Action__c` record and returns its id, `SA Record ID`. That is all it does. It sends no Slack message, email, or alert.

Terra shows each Signal Action on the assignee's personal to-do list. A row shows the person, title, location, company, and tier, then the play name. The group label above the rows is the Gong flow step, for example `Step 2 · Manual email`. Terra fills the step and the play name from the Engage Flow ID and Engage Flow Instance ID. Opening the row goes to that contact's Action View. The to-do has no body or message text. Nothing on it is sent.

One record has one assignee. A second person sees an item only when a second record is created with their user id.

Without a flow id and instance id, the row shows `No Step Data`. The blue `No Type` group above it is a Terra-side mapping per play. There is no function input for it. Closed Lost is mapped to `GTM Play [Closed Lost Reheat]`. A new play asks for its mapping before the chart is signed. Seen on Ethan's two test calls on 2026-10-07 (`SA-32369` `a42a7000000KjaTAAS`, and `a42a7000000Kjc5AAC`).

## Core

1. Run after Gong enrollment, and pass that enrollment's flow id and instance id.
2. The assignee is the ClayDR's Salesforce User id from the Route & Score re-read.
3. External ID is the Gong flow instance id. When there was no enrollment, use `<opportunity id>-<account id>`.
4. The item does not depend on the GTME Copilot Post. A missing GTME does not remove the ClayDR's item.
5. [Test Mode](test-mode.md) swaps the assignee to Ethan's Salesforce User `005a700000E6R0fAAF`.

## Parameters

| Parameter | Meaning | Values today |
| --- | --- | --- |
| `terra_type_label` | The Terra-side group name for one play. Not part of this block. Closed-Won's unmapped label is that play's item | Closed Lost: `GTM Play [Closed Lost Reheat]` |
| `campaign_id` | Optional. Passed when the play has a campaign | per play |

## Must Not

- Do not expect the to-do to carry a message. There is no body input.
- Do not use `Push HiL to Terra` or `Send Simple Insight to Terra` for this. Those post cards to a person's copilot Slack channel and are separate entry points.
- Do not require a Campaign Member id. Card 18 did. Both current plays queue without one.

## Lessons It Prevents

- Card 18 tied the queue to Campaign Member attribution, which neither new play writes.
- The `No Type` group label was mistaken for something the function sets.

## Decisions

Closed Lost re-arch D12 (the queue item goes to the ClayDR), D18, D19, D42 (assignee from the re-read). Closed-won D13.
