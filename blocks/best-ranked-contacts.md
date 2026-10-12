# Best Ranked Contacts

| Field | Value |
| --- | --- |
| Id / version / status | `best-ranked-contacts` · v3 · global, 2026-10-09 (Core 5: null answers are nobody; Core 6: the person is on the target account) |
| What it does | Ranks the workspace users at the account and picks the best person to contact |
| Inputs | `Workspace_User_Relationship__c` rows for `Account.Primary_Workspace__c`, the touch rows from [Suppression](suppression.md) |
| Outcomes | `picked` with one Contact id, or `nobody` (no rows, or everyone skipped) |
| External writes | none |
| Pins | Claygent `[GROWTH] Best Ranked Contacts` `c_0tfqa7vy2yKPStkvBhc`, model `claude-opus-4-6`, internet search off. Version: the most recent (Ethan, 2026-10-08). On 2026-10-08 that was `cv_0tmlhawjWsi67W8eBUt`; closed-won was built on `cv_0tmkqf7pGkTqbjyADHs` |
| Consumers | Closed-Won lookalike `T3A`–`T3F`. Closed Lost re-arch `5A`–`5C`. Verified against the live graphs 2026-10-08 |
| Was | card 39 |

## Core

Read, shape, check for empty, call, pick.

1. Read the workspace-user rows. Each carries `Id`, `Contact__c`, and the Contact's name, title, `Persona__c`, `MailingCountry`, `Suppression_Reasons__c`, `HasOptedOutOfEmail`, `Gong__Actively_Being_in_a_Flow__c`, and `Last_Workspace_Login_Detected__c`.
2. Shape: copy the Account's `Main_Workspace_Contributor__c` onto each row. The Claygent expects it there.
3. Zero rows goes to `nobody` before the Claygent. An empty list must not call it.
4. Call the Claygent by id. Do not send or re-author a prompt. It is shared and is not ours to edit.
5. Check the answer before parsing it. The Claygent may return a bare `null`, the string `null`, an empty string, or an object with no `rankedContacts`. Every one of those is `nobody`, and the run goes to the play's fallback. The node reads the answer as text first and parses JSON only when it starts with `{`. (Ethan, 2026-10-09: the null return is fine; check for it.)
6. Pick: start at `bestContact`, then walk `rankedContacts`, skipping anyone the [Suppression](suppression.md) contact skip names, and anyone whose Salesforce `Contact.AccountId` is not the target account (a workspace user from another company, or a contact filed under another account; GridGain 2026-10-09, Closed-Won `T3F` version 12). An empty touch read does not fail the pick.
7. Record the Claygent version the run used.

## Parameters

| Parameter | Meaning | Values today |
| --- | --- | --- |
| `fallback` | Who to use when nobody is left | Closed Lost re-arch: the primary workspace creator (D37). Closed-won: none after the list; when the workspace has no rows, `Account.Main_Workspace_Contributor__c` is handed to the Claygent as the only row (`T3B`, `T3C`) |

## Must Not

- Do not edit the Claygent.
- Do not parse the answer as JSON before checking it. A bare `null` broke the output parser on GAIA (`wfr_0tmlieouF6V8j55B5jY`); a plain string failed Damco twice (`wfr_62c9078ba40b3baef1501a535fd20657`, `wfr_7d5b3389d258ae71a09bd245fca069c9`). Step 3 stops the empty call; step 5 catches the empty answer. Do not ask the Claygent's owner to change its prompt for this.
- Do not move to a new Claygent version without re-running the test packet.

## Lessons It Prevents

- A bare `null` from the Claygent broke the output parser on GAIA (`wfr_0tmlieouF6V8j55B5jY`). Step 3 checks for zero rows before the call.
- Closed-won was built on `cv_0tmkqf7pGkTqbjyADHs` while the Claygent had moved to `cv_0tmlhawjWsi67W8eBUt`. Step 6 records the version each run used (closed-won erratum 2026-10-07 22:00).

## Decisions

Closed Lost re-arch D17, D19, D32, D37. Closed-won erratum 2026-10-07 22:00; Ethan 2026-10-08 "use the most recent version".
