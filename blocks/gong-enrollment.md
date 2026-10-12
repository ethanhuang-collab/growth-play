# Gong Enrollment

| Field | Value |
| --- | --- |
| Id / version / status | `gong-enrollment` · v1 · global, 2026-10-08 |
| What it does | Puts the picked person into this play's Gong Engage flow, owned by the ClayDR |
| Inputs | Prospect Salesforce Contact id, owner email (the ClayDR's), the flow id for the chosen sequence, and step 1 subject and body overrides |
| Outcomes | `enrolled` with `flowInstanceId`, `already_in_flow` (skip), or `failed` (logged on the run, [Write Failure](write-failure-alert.md)) |
| External writes | Gong Engage. Once the first to-do is created it cannot be undone. Unassigning the flow instance stops future steps only |
| Pins | Clay actions `gong-get-assigned-flows-for-prospect` and `gong-add-prospect-to-flow`, package `48aa0220-fa5b-43d8-a1a3-ffcbebfb713a`, Gong account `aa_0t8nu3gQ3wnm2TDHvip` |
| Consumers | Closed-Won lookalike `T7B`–`T8B`. Closed Lost re-arch `21B. Gong Campaign`. Verified against the live graphs 2026-10-08 |
| Was | card 16 |

## Core

1. **Read the prospect's Gong flows first** with `gong-get-assigned-flows-for-prospect`. Gong takes a contact once per flow. If the person is already in the target flow, skip them.
2. **Enroll** with `gong-add-prospect-to-flow`: `flowId` is the flow, `crmProspectId` is the Contact id, `flowInstanceOwnerEmail` is the ClayDR's email (Gong needs the email, not the user id).
3. **Manual and automatic flows are siblings.** The play picks one per run, and the chart draws them side by side.
4. **Record `flowInstanceId`.** It is the proof of enrollment and feeds the Action Queue.
5. **[Test Mode](test-mode.md)** swaps the prospect to Ethan's `huangster123@gmail.com` Contact and the owner to `ethan.huang@clay.com`.
6. **Enrollment is not delivery.** A Running instance means the prospect is on the flow. Step 1 reaches the inbox only when it is sent from `ethan.huang@clay.com` through Gmail. The rounds are Huangster, then a real batch with one manual case and one auto case, then the gate back to `huangster123@gmail.com`. See [Test Mode](test-mode.md) Steps.

## Parameters

| Parameter | Meaning | Values today |
| --- | --- | --- |
| `manual_flow_id` | The manual sequence. The `flow=` value in the Gong URL | Closed-won `2751667605583158577`. Closed Lost re-arch `7822886536753112041`. Trial-extension `3893909031139751666` |
| `auto_flow_id` | The automatic sequence. The `flow=` value in the Gong URL | Closed-won `6248627259904112412`. Closed Lost re-arch `7315015979702319623`. Trial-extension `4519910719264475895` |
| `sequence_rule` | Which records take which flow | Closed Lost: Tier 3 automatic, Tier 1 and 2 manual. Closed-won: Tier 1 and 2 manual, every Tier 3 auto (churned included), Tier 4 no Gong step |
| `step_overrides` | Step 1 subject and body | per play |

## Must Not

- Do not paste a step id as the flow id. In a Gong URL, `flow=` is the flow and `flow-step-id=` is one step. A workflow constant, a Gong enroll call, and the channel-campaign Typeform all use `flow=`. The step id may sit in a comment so the step can be reopened. It is not enrolled and it is not written on the campaign.
- Do not enroll `ethan.huang@clay.com` as the prospect. Gong treats a clay.com address as a team member and leaves it Pending forever.
- Do not run two test sends of the same flow to the same test contact. Remove the prior instance, or use the second test seat.
- Do not rely on Salesforce `Gong__Engage_Flow__c` to see a running enrollment. It shows only finished instances.
- Do not leave a test instance on a flow whose id was withdrawn. When a flow id changes, unassign the old instances and run one enrollment on the new id before release.
- Do not count `gong-add-prospect-to-flow` success as a sent email.

## Lessons It Prevents

- Flow id versus step id confusion (Closed Lost re-arch D34). On 2026-10-10 Gong returned `Flow not found: 564113302196897991` because that number is the step on auto flow `7315015979702319623`. The 2026-10-08 erratum that pinned the step id is reversed. Andrew Morris, 18 Sep 2026: the Typeform stores the number after `flow=` in the URL.
- clay.com test prospect stuck Pending (Closed Lost re-arch handoff 2026-10-08).
- A second test send failed because the test contact was already in the flow.
- Allen & Company (`wfr_0tmm5dlQRneNva86XsU`) enrolled on auto flow `7315015979702319623`. A later note called that flow withdrawn and pinned step id `564113302196897991`. The 2026-10-10 enroll failure showed the step id is not a flow.

## Decisions

Closed Lost v7 D47 (enrollment approved), Closed Lost re-arch D26, D34, erratum 2026-10-08 (auto flow). Closed-won D29 and errata 2026-10-07.
