# Suppression

| Field | Value |
| --- | --- |
| Id / version / status | `suppression` · v3 · global, 2026-10-10 |
| What it does | Decides whether the account stops, and whether one person is skipped. These are two separate checks. |
| Inputs | Account id, the people the play is choosing between, and the play's campaign ids |
| Outcomes | Account: `continue`, `stop`, or `hold` (lookup failed), each with a reason. Per person: `keep` or `skip`, each with a reason |
| External writes | none |
| Pins | Salesforce reads run as `SFDC Integration User (GTM Ops)` |
| Consumers | Closed-Won lookalike `T1A`–`T2A` (account stop; `T1B. Read this play's campaign members` is account stop 3). Closed Lost re-arch `4A`–`4F` (account stop; `4C. This Play's Campaigns` is account stop 3) and `5C. Pick Person` (contact skip). Existing graphs keep their own nodes until someone rebuilds that part. Verified against `clay workflows graph get --mode summary` 2026-10-08 |
| Was | card 40 (`../graph/40-account-contact-suppression.md`) |

## Core

The core is the same in every play. A play does not edit it. A change to the core is a new version of this card.

### Account Stop

Stop the account when any of these is true:

1. A GTME, GS, or FDE sent a message or made a call to anyone at the account in the past 30 days.
2. The account has an open opportunity.
3. The account is already in this play. A Campaign Member on one of the play's campaign ids, for anyone at the account, inside the window, and the run does not fire. No enrollment and no send. The ids are in Parameters. This uses Andrew's first query below.
4. `Account.Suppressed__c` is true. The flag alone is the stop. `Suppression_Reasons__c` is shown when it is filled, and the stop does not need it.

A Salesforce lookup that fails is a `hold`, not a `continue`.

### Contact Skip

Skip that one person, and keep the account, when any of these is true:

1. A ClayDR or an SDR sent that person a message or called them in the past 30 days. An SDR counts as a ClayDR here, and a call has the same outcome as a message. Both skip the person. Neither stops the account. A message counts even when it came from a different campaign.
2. The person is in a Gong flow right now. This uses Andrew's second query below.
3. The person opted out of email, or the Contact is suppressed in Salesforce.
4. The person has a `clay.com` email on a workspace-user row. That is Clay staff inside the customer's workspace.

### Andrew's Two Queries

These are the shapes from paid-alumni `wf_0tjvpv4jjx4oJEcyubY`, read with `clay workflows graph get` on 2026-10-08. A play copies the shape and fills in its own parameters.

Already in this play (account stop 3):

```sql
SELECT Id, CampaignId, ContactId, CreatedDate FROM CampaignMember
WHERE CampaignId IN ({{play_campaign_ids}})
  AND Contact.AccountId = '{{account_id}}'
  AND CreatedDate = LAST_N_DAYS:{{already_in_play_days}}
LIMIT 1
```

In a Gong flow now (contact skip 2):

```sql
SELECT Id, Name, Gong__Actively_Being_in_a_Flow__c FROM Contact
WHERE Id = '{{contact_id}}' AND Gong__Actively_Being_in_a_Flow__c = true
LIMIT 1
```

A play that checks several people at once can use the same filter with `WHERE Id IN (...)`, or read `Contact__r.Gong__Actively_Being_in_a_Flow__c` on the workspace-user rows it already fetched.

### One Touch Read

One Task read on the account feeds both account stop 1 and contact skip 1. The contact skip matches the person on `WhoId` in the rows that read already returned. Closed Lost re-arch's read is the reference:

```sql
SELECT Id, Subject, ActivityDate, CreatedDate, WhoId, Who.Name, TaskSubtype, Type, Status,
  TYPEOF Owner WHEN User THEN Id, Name, Email, Title, Department, UserRole.Name END
FROM Task
WHERE (AccountId = '{{account_id}}' OR Account.ParentId = '{{account_id}}')
  AND ActivityDate = LAST_N_DAYS:30
  AND (Subject LIKE '[Gong Out]%' OR TaskSubtype = 'Call' OR Type = 'Call' OR Type = 'Meeting')
ORDER BY ActivityDate DESC LIMIT 500
```

The sender's role comes from the owner's title, department, or role name.

## Parameters

Each play fills these in. Two plays can reasonably disagree on them.

| Parameter | Meaning | Values today |
| --- | --- | --- |
| `play_campaign_ids` | This play's current Salesforce campaigns. A Campaign Member on one of these, for anyone at the account, means do not fire: no Gong enrollment and no send. Old campaign versions are not the check | Closed Lost re-arch manual `701a700001Ji6srAAB`, auto `701a700001JnAatAAF`. Closed-Won manual `701a700001JcipOAAR`, auto `701a700001JcBleAAF` |
| `already_in_play_days` | How far back a Campaign Member counts as already in this play | Paid-alumni 30. Closed Lost re-arch 30. Closed-won lookalike 90 (its D09) |
| `extra_contact_skips` | Skips a play adds on top of the core list. Optional | none |

## Must Not

- Do not use `Gong__Engage_Flow__c` for "already in this play". Salesforce gets that row only when the flow instance finishes, so a running instance does not show there.
- Do not run a second Task query for the contact skip. The one touch read already has the rows.
- Do not let an SDR or ClayDR touch stop the account.
- Do not read old campaign ids. A campaign that was remade means the old id leaves `play_campaign_ids`.
- Do not widen account stop 3 to other plays' campaigns. Another play touching the account does not stop this one (Ethan, 2026-10-09: "we don't care about other plays on the account level"). The person-level Gong check still catches someone already in any flow.
- Do not assume Gong creates the member. The write is [`campaign-member.md`](campaign-member.md), and it records the picked person. A member for the test seat is on Ethan's account, so the next run of the customer still fires.
- Do not leave a new Salesforce node on `sydneybox1-sandbox`. Switch it to `SFDC Integration User (GTM Ops)` in the node drawer, since the CLI cannot set that account.

## Lessons It Prevents

- Electric Era (`001a700000E7xqdAAB`, reason `Customer;`) ran to the end because the node did not read `Suppressed__c`. Run `wfr_0tmlvl8MuiXnmseyJ8y`, fixed in `wfr_0tmm2f2SigtDhBSCE4J` (Closed Lost re-arch D39).
- "Already enrolled" had three definitions across the two plays. This card has one (Closed Lost re-arch D41, superseding D33's `Gong__Engage_Flow__c`).
- The contact skip was once a second query chain. Ethan cut it on 2026-10-08.

## Decisions

Ethan 2026-10-08: already in this play means enrolled in this existing play, using Andrew's queries as the shape. No suppression reason is needed. An SDR is the same as a ClayDR, so the call has the same outcome. Account suppression is global. Kit decision D24. Earlier: Closed Lost re-arch D14, D20, D24, D33, D39, D41. Closed-won D08, D09.
