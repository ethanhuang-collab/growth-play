# Route & Score

| Field | Value |
| --- | --- |
| Id / version / status | `route-and-score` · v3 · global, approved 2026-10-09 (Core 2: the GTME try; Core 8: the person must be on the target account) |
| What it does | Assigns a ClayDR whether or not the account qualifies. Assigns a GTME only when the account qualifies, and only on a trigger that can reach a GTME. A play-name trigger assigns no new GTME |
| Inputs | The picked person's full name and email, the account id, the account's current `ClayDR__c`, `OwnerId`, `Owned_by_GTME__c`, and parent owner |
| Outcomes | `owners_ready` (ClayDR set, GTME set or none), `hold_no_claydr` (live run and still no ClayDR), `hold_wrong_account` (the function answered for a different account) |
| External writes | Salesforce, on the function's side: the ClayDR on the account, qualification fields, and possibly a contact or account create. Snowflake routing log. Undo: a ClayDR assignment can be changed by hand in Salesforce. A created contact or account stays |
| Pins | `[GTMOps] Route & Score Account` `t_0tia25leiuqgvCTevZZ`, built by Bruno Radice. Read-only for us, permanently |
| Consumers | Closed-Won lookalike `T5A`–`T5D`. Closed Lost re-arch `6A`–`6G`. Verified against the live graphs 2026-10-08 |
| Was | card 33 (`../functions/33-route-and-score.md`; the fullest copy is in clay-planning-system `growth-plays/building-blocks/functions/33-route-and-score.md`) |

## How The Function Works

Bruno's function is a Clay table with 268 columns, called like a function. For one person it:

1. Matches the email to a Salesforce contact and account. It checks contact email, other emails, account domain, and LinkedIn. If nothing matches, it can create the contact or the account.
2. Scores the person: qualification, sales tier, and contact tier (decision maker or influencer).
3. Assigns owners on the account, unless `Score Without Routing` is true. Bruno's note on `Force Route to ClayDR`: true means a ClayDR and no GTME. Left blank, a lead the function routes to a GTME also gets a ClayDR. A play-name trigger is not one of those leads. Score-only run `run_0tmmconpdP6CGFGx2Y6` (2026-10-08, trigger `Closed-Lost Re-Heat`, nothing written to Salesforce): Malwarebytes was Sales Led and the GTME stayed the integration user, flag blank and flag true. Allen & Company of Florida was Disqualified and the ClayDR route flag stayed on, flag blank and flag true. The function's own line: only Inbound Form, Contact Us, Linkedin Ads, Meta Ads, ClayDR Routing, and force routes reach a GTME.
4. Returns `Final Qualification`, the account and contact ids, the ClayDR's email (`RR ClayDR Email - Account`), GTME name and links, and a `Final Routing Decision`. It does not return a GTME user id.

## The Case, And Andrew's Check

Closed Lost, 2026-10-08, Allen & Company of Florida (`wfr_0tmm5dlQRneNva86XsU`). Employee count 68 is in the 50–149 band, and tech score, headcount growth, and funding all miss. Route & Score returned Final Qualification `Disqualified`, Roe Layer `Disqualified — No Action`, and the explainer "This contact will NOT be followed up with — the account is Disqualified." Both owners were blank. The call was score-only, so it wrote no owner. The later run `run_0tmmconpdP6CGFGx2Y6` kept the ClayDR route flag on for this same account. Disqualified is not a hold (D42). It is why no GTME comes back.

Andrew's paid-alumni play does not give a counterexample. From 2026-09-15 through 2026-10-05 it wrote a ClayDR on 15 accounts and changed the Salesforce owner on none of them. Those accounts were already owned by a GTM Engineer. Across every trigger in the last 45 days, no account whose explainer says Disqualified was assigned a GTME on the same day as its ClayDR route. Spendesk is the same shape as before: a subsidiary whose parent already has a GTME, not a disqualified account that received one.

## Core

1. **The ClayDR comes first.** Every run needs a ClayDR. The GTME is optional.
2. **Call it when the ClayDR is blank, or when the GTME is blank.** A blank ClayDR must be filled. A blank GTME is a try: the call may not assign one on a play-name trigger, and a disqualified account never gets one, but the play asks. If both owners are set, skip the call and read the GTME from the account. (Ethan, 2026-10-09: force a ClayDR always; try for a GTME; a GTME cannot be forced when the account is not qualified.)
3. **When the ClayDR is blank, pass `Force Route to ClayDR` true.** Do this on every play, even when the account is disqualified. When a ClayDR is already set and only the GTME is blank, leave the flag blank, because true would block the GTME. This is what Closed Lost re-arch `6B` and Closed-Won `5A` do today.
4. **`Score Without Routing` = true on every test run.** [Test Mode](test-mode.md) decides what a test run is. It is false only on live, after the scope contract records the go-ahead. It skips the route writes. It does not skip every write inside the function (contact or account create can still happen).
5. **Re-read the account after the call.** Read `ClayDR__c`, `OwnerId`, `Owned_by_GTME__c`, and the parent's owner. Downstream nodes use the re-read, not the values the run started with.
6. **Read the GTME after the call.** It is the owner the function just wrote, or `Account.OwnerId` when `Owned_by_GTME__c` is already true, or the parent's owner when the parent is GTME-owned. Otherwise there is no GTME. `Account.GTME__c` is not the owner field. A disqualified account can still get a ClayDR. It does not get a GTME. Skip the run when `Final Qualification` is `Disqualified` only if the play's chart says so. Paid-alumni does. Closed Lost re-arch enrolled Allen & Company after a Disqualified score.
7. **No GTME is not a stop.** The run continues. The GTME Copilot Post is skipped. The ClayDR still gets the Gong enrollment and the action queue item.
8. **Hand it a person who is on the target account.** The function matches by the person's email, not by our account id. The pick step skips any ranked person whose Salesforce `Contact.AccountId` is not the target before the call (Closed-Won `T3F`, version 12, 2026-10-09). GridGain: the first pick, `will.bland@mariadb.com`, routed MariaDB; the next pick, `janey.lee@gridgain.com`, routed GridGain and it got a ClayDR.
9. **Stops.** On live, no ClayDR after the call holds the run (`hold_no_claydr`). If `Final Account Id` is still not the target account after rule 8, hold the run (`hold_wrong_account`); that is a data problem on the contact, not a retry.

## What The Live Plays Do Today

| Play | `Force Route to ClayDR` | What that means |
| --- | --- | --- |
| Paid-alumni `wf_0tjvpv4jjx4oJEcyubY`, the reference Andrew runs | Not passed, so blank. Trigger `Paid Alumni Job Changer`. A later node skips `Disqualified` | Andrew's own skip. Not this block |
| Closed-won lookalike, `T5A` | True when the ClayDR is blank. Blank when a ClayDR is already set | A missing ClayDR is forced, even if the account is disqualified |
| Closed Lost re-arch, `6B` | True when the ClayDR is blank. Blank when a ClayDR is already set | Same |

## Parameters

| Parameter | Meaning | Values today |
| --- | --- | --- |
| `qualification_trigger` | The Gong title, the words inside `[Outbound] {title} [GTM Play]`. Not the repo folder name, and not the full flow name with `[Auto]` or `[Manual]`. Ask Ethan once, with the campaign setup title. Do not ask Bruno to add it | Closed-won: `Closed-Won Look-Alikes`. Closed Lost re-arch: `Closed-Lost Re-Heat`. Trial-extension: `Trial-extension Follow-up` |
| `live_routing` | Whether `Score Without Routing` is false on live | Both plays: false until approval |

## Must Not

- Never create, update, delete, or reconfigure anything on `t_0tia25leiuqgvCTevZZ`. A needed change is a written request to Bruno.
- Do not treat Disqualified as "no ClayDR." Allen kept the ClayDR route flag.
- Do not expect a play-name trigger to assign a GTME. Only a qualified account gets a GTME, and only on Inbound Form, Contact Us, Linkedin Ads, Meta Ads, or ClayDR Routing. `Force Route to ClayDR` is not one of those.
- Do not read `GTME__c` as the GTME. It was filled on 5 of 136,855 Tier 1–3 accounts on 2026-10-07.
- Do not use the owners the run started with after the call. Use the re-read.

## Lessons It Prevents

- Route & Score was re-explained mid-build in two chats before this was written down once (chat `e7a52139`).
- A routing check wrote a real ClayDR onto Spendesk. Test runs pass `Score Without Routing` = true.

## Decisions

Ethan 2026-10-08: a disqualified account can still get a ClayDR, and only a qualified account gets a GTME. Kit decision D35. The run is `run_0tmmconpdP6CGFGx2Y6`. Earlier: D33, Closed Lost re-arch D42.
