# Test Mode

| Field | Value |
| --- | --- |
| Id / version / status | `test-mode` · v4 · global, 2026-10-10 |
| What it does | On every non-live run, sends to Ethan instead of the real people. The play still picks and records the real person and owners |
| Inputs | The route (`dry-run`, `test-owner`, `test-channel`, `live`), the picked person, the resolved owners |
| Outcomes | The seats the send nodes read: Gong prospect, Gong owner, action queue assignee, Slack channel |
| External writes | none. This node only chooses addresses |
| Pins | none |
| Consumers | Closed Lost re-arch `6E. Ethan Test Seats` (one node). Closed-Won lookalike keeps the same swap inside three code nodes, `T5D. Resolve GTME and ClayDR` (assignee, channel), `T7B. Choose the Gong prospect` (prospect), and `T7D. Prepare delivery` (owner, channel). Verified against `clay workflows graph get --mode full` 2026-10-08 |
| Was | card 41 |

## Core

1. One node is the switch. The send nodes read their addresses from it. Copying the test addresses into the send nodes makes a second switch, which is not allowed.
2. On any route except `live`, the seats are:

| Seat | Test value |
| --- | --- |
| Gong prospect | `huangster123@gmail.com`, Salesforce Contact `003a700000u9APiAAM` |
| Second Gong prospect | `ethan80808@gmail.com`, Contact `003a700000u9zQqAAI`, when the first is already in the flow |
| Gong flow owner | `ethan.huang@clay.com` |
| Action queue assignee | Ethan's Salesforce User `005a700000E6R0fAAF` |
| Slack channel | `#__copilot_ethanh` `C0BP3JTNNCF` |
| Salesforce owner writes | dry-run. There is no sandbox |
| Campaign Member | the picked person at the account, even on a test. This is the one Salesforce write a test run makes, so the next run of that account stops |

3. `live` is never chosen by a test.
4. On live the node passes the real person and owners through unchanged.
5. A Gong enrollment is not a sent email. `gong-add-prospect-to-flow` stores the copy and creates a flow instance. It does not deliver step 1. The send is a Gmail message from `ethan.huang@clay.com` with that step's subject and HTML body, to the address the gate names.

## Steps

The rounds run in this order. The gate is `huangster123@gmail.com` except during the real batch.

1. **Huangster.** Run the play with the gate on Huangster. Send step 1 from Gmail to `huangster123@gmail.com`. Verify the actual Sent message and pass the audit/QC checkpoint before the next round starts.
2. **Real test batch.** Two cases, run separately. Manual gets its own account, person, and flow. Auto gets its own account, person, and flow. Each send is step 1 from Gmail to that person's real email.
3. **Gate back to Huangster.** `TEST_RECIPIENT` is `huangster123@gmail.com`, Contact `003a700000u9APiAAM`, before anything else runs.

## After Every Huangster Send

Immediately after each test email to `huangster123@gmail.com`, the agent audits that exact send and starts independent QC without waiting for Ethan to ask. This checkpoint comes before the real test batch and before calling the test phase done. It also applies to repeat sends.

Use the exact Gmail Sent message addressed to `huangster123@gmail.com` and review its stored copy as the selected intended person would read it. Verify the connected sender account and match the message id, timestamp and test/step before reading. Sent mail is sufficient for this checkpoint; Huangster inbox access is optional. A missing exact message or unavailable body is `unverified`. Record Sent evidence as sent-message/copy verification; claim inbox receipt only with receiving evidence.

Before an authorized test send, capture the expected selected person and account, qualifying signal and timestamp, branch/step, approved copy or generator output, sender, test recipients and link/calendar destinations, with source references. QC derives identity and signal expectations from the signed play logic and source facts before reading the message. For an existing send, reconstruct expectations from its original source evidence. The generated email is not its own source of truth.

The envelope goes to Huangster; personalization stays about the real person the play selected. A correct greeting does not have to say Ethan. Historical contacts may appear when the approved copy and source evidence support their role.

1. **Read as the recipient.** Inspect the actual Sent message's subject, sender, greeting, body and links. Ask whether this reads correctly for the selected person: name spacing, company, signal, timing, claims and CTA. Use the stored HTML/text and render it when appearance is uncertain. Check authoritative outgoing recipient metadata for To/Cc/Bcc; inbox headers alone cannot rule out Bcc. Huangster is the only delivery recipient. A draft, Gong enrollment or successful API response is not message readback.
2. **Verify the facts and copy.** An independent QC agent applies the cases below to the actual sent copy, comparing the real person, company and signal with original source evidence even when the email reads plausibly. Tie the message to its workflow run, tested version or draft snapshot, branch/step and expected copy. Inspect actual link targets as well as visible text. QC flags defects for the copy owner; it does not invent or rewrite copy.
3. **Escalate when needed.** A content/source mismatch, duplicate send, unexplained output or recipient/write safety concern triggers inspection of the affected connected run and write readbacks. Trace the relevant eligibility, suppression, person, owner, signal, generation and delivery values at their consumers; reconcile writes with the route registry and approval scope, including off-graph Gmail sends. Existing lifecycle checks can also require this audit. Routine message QC proves the inspected copy and its checked facts; other branches and full workflow/write verification keep their separate requirements.
4. **Save the evidence and verdict.** The QC agent records the audit and its verdict in the play's `qc/<workflow id>/qc.md`, with the run id, version or snapshot, message id and timestamp, and evidence source (`Sent` or `inbox`). Keep send verification and inbox receipt separate; unavailable inbox evidence does not block Sent-based copy QC. For each case record its id, expected result, observed result, evidence reference, verdict (`pass`, `fail`, `unverified` or `not applicable`), finding and next action. `not applicable` needs a reason grounded in the play contract. Record proofs only for checks actually performed, using the existing proof ledger. Keep prospect/customer identities and message payloads outside Git; committed receipts are redacted and fixtures hash-only.
5. **Clear the checkpoint.** The next round starts only after `pass` or `pass with notes`, with no material finding open. Missing evidence, pending checks or a material failure means `blocked`, never a pass. Apply fixes through the existing build/release rules, invalidate affected proofs and rerun the affected checks. Another send or external mutation needs the existing authorization; QC does not open a write gate. This one-send verdict does not establish coverage of untested branches.

### Email QC Cases

These are checks on the actual message and its source record. The defect examples define what to catch; they do not require fabricated records, deliberately bad sends or a live run per row. Negative-case coverage that has not been exercised stays untested.

| Id | Case / defect to catch | Passing evidence |
| --- | --- | --- |
| Q01 | Bad name spacing: leading/trailing or doubled spaces, joined words, a malformed greeting | The name and greeting have the intended word boundaries in the rendered message and populated text. Preserve legitimate multiword names, accents, hyphens and apostrophes. A blank name uses only an approved fallback. |
| Q02 | Wrong person: wrong name, wrong candidate, obsolete employer or role | Personalization and qualification match the selected real person's source record and the play's current-employment checks. Compare stable identity as well as the displayed name; two people can share a name. |
| Q03 | Wrong company or mixed context: another account, sibling entity or previous run's details | Company, domain and every account-specific detail belong to the intended account under the play's entity rules. Source-to-message joins retain the correct person/account ids. |
| Q04 | Wrong signal: another person's/account's event, wrong event type or reversed outcome | The source signal belongs to the intended entity, matches the qualifying event and selected branch, and supports the email's description. |
| Q05 | Wrong timing: stale or missing signal, unsupported "recently" or incorrect elapsed time | The source event date satisfies the play's agreed timing rule at send time. Any recency or duration claim agrees with that date. No universal freshness window is invented. |
| Q06 | Unsupported personalization: invented role, tool, number, meeting history or intent | Each factual claim has source evidence and fits the approved talk track and considerations. Missing or conflicting evidence is `unverified`; QC flags the issue for the copy owner. |
| Q07 | Wrong copy: wrong play, manual/auto branch, step or stale generator/template | Subject and body match the intended step and authorized copy or generator output for this real record and route. The run identifies the configuration that produced them. |
| Q08 | Broken text or HTML: unresolved merge fields, null-like values, joined paragraphs, escaped markup or truncation | The actual message renders with readable spacing and complete content, and subject, HTML and any supplied plain-text part agree. Check both populated fields and rendered output. |
| Q09 | Wrong links or CTA: mismatched link text, broken destination or another owner's calendar | Actual `href` values and CTA match the intended destination and route's owner/calendar rules; verify the destination through safe read-only evidence. Do not activate unsubscribe or other action links to test them. An unperformed required destination check is `unverified`. |
| Q10 | Wrong delivery: wrong sender, real-person recipient or unexpected Cc/Bcc | Authoritative outgoing recipient metadata names Huangster only, and the sender matches the route. The preserved real person's name in the body is expected, not a delivery error. |
| Q11 | Run audit on escalation: mismatched facts/output, duplicate delivery or a recipient/write safety concern | Inspect the affected trace and write readbacks against the route registry and approval scope, including off-graph sends; resolve the finding and rerun affected checks. Apply this row when an escalation trigger or existing lifecycle requirement calls for it. Otherwise record `not applicable` with that scope reason, without claiming full workflow/write verification. |
| Q12 | Wrong evidence: older message, unrelated run or changed configuration | Message id/time, run, selected record, branch and tested version/snapshot agree. Required checks use that candidate's evidence; stale proofs, an enrollment alone or a success response do not pass. |

All applicable rows are required. Q11 is an escalation check; the other rows apply to the routine sent-copy review, with contract-based reasons for intentionally absent fields. A `fail` or `unverified` row blocks this checkpoint. `pass with notes` is reserved for optional style preferences after the required checks pass; bad name spacing, identity, signal, links and routing are required checks. Passing this copy checkpoint does not clear separate lifecycle, branch or write-safety gates.

## Parameters

None. The seats are the same on every play. A play that wants a different test seat changes this card, not its own node.

## On Charts

Test Mode nodes, and any node that only exists to stop a test from reaching a real person, are green on every chart:

```
classDef testMode fill:#D6F0D8,stroke:#3C8A46,color:#123D18
class <id> testMode
```

The Clay canvas has no color field on a node or a group. The color is on the chart only.

## Must Not

- Do not use `ethan.huang@clay.com` as the Gong prospect. Gong leaves a clay.com address Pending.
- Do not run more than 2 real test records per round (Closed Lost re-arch D27).
- Do not start the real test batch or mark the test phase done while a Huangster send's audit or QC is pending or blocked.
- Do not pass the copy check using only a draft, generator output or Gong enrollment; read the actual Sent or received message.
- Do not treat a Running Gong instance as proof the email went out. Check the inbox, or Sent mail from `ethan.huang@clay.com`.

## Lessons It Prevents

- A test enrolled `ethan.huang@clay.com` as the Gong prospect and it sat Pending forever, because Gong treats a clay.com address as a team member (Closed Lost re-arch handoff 2026-10-08). The prospect seat is `huangster123@gmail.com`.
- Closed-Won copied the test addresses into three code nodes instead of one switch, so a seat change there is three edits. Core 1 asks for one node.
- The test color was amber in Closed Lost re-arch D35 and green in the kit. One color, green, on every chart (kit decision D26).

## Decisions

Ethan 2026-10-10: "Make it so that after we send a test email to huangster123 we audit and do a qc". Version 2 adds the required checkpoint after every Huangster send.

Ethan 2026-10-10: "First think about the test cases ie bad name spacing etc wrong person wrong signal etc then build". The case matrix defines the required checks before the checkpoint is used.

Ethan 2026-10-10: "Can we do it from huangster email address the check pov". Version 3 starts QC from the message received in Huangster's mailbox, read as the selected intended person; deeper run/write audit follows a finding or an existing lifecycle requirement.

Ethan 2026-10-10: "you cna jsut see the sent email to see if it worked". Version 4 accepts the exact sender Sent message for the same recipient-POV QC, superseding version 3's inbox-access requirement. Sent evidence verifies the send and stored copy; receiving evidence is needed only to claim inbox receipt.

Ethan 2026-10-08: test mode sends to `huangster123@gmail.com`, and Ethan's test blockers are green. Kit decision D26. Earlier: Closed Lost re-arch D13, D27, D35 (that decision said amber; green replaces it).
