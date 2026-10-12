# Campaign Setup

| Field | Value |
| --- | --- |
| Id / version / status | `campaign-setup` · v1 · global, 2026-10-10 |
| What it does | Makes this play's Gong folder, its manual and auto flows, and the Salesforce campaigns those flows enroll into |
| Inputs | From phase 1, the overview: the play title Ethan confirmed, and one sentence of what the play does |
| Outcomes | Two Gong flow ids (`flow=`), two filled Typeforms, two Salesforce campaign ids once the form replies |
| External writes | Gong Engage (duplicate two flows). Salesforce, through the Typeform, which creates a Campaign. Undo: do not enroll anyone to undo a folder; a campaign member is a later block |
| Pins | Typeform https://clayhq.typeform.com/to/UPvikaV0. Source flows to duplicate: Closed-Lost Re-heat manual `7822886536753112041`, auto `7315015979702319623`. Parent folder `[LIVE] GTM Plays` |
| Consumers | Trial-extension, flows already made, Typeform not submitted. Next play reads this card |
| Was | none. The Typeform field list used to sit on [Campaign Member](campaign-member.md) |

## When

This runs once phase 1 is signed: the question rounds are closed and the overview is signed. It uses the title and the one sentence from that page. It starts in the background with the other steps named for that moment, the cohort counts and the test-record search. The node chart does not wait on the Salesforce campaign ids. The build does: [Gong Enrollment](gong-enrollment.md) and [Campaign Member](campaign-member.md) need the flow ids and the campaign ids this step writes down.

The only question for Ethan is the title. Confirm it, then do the rest. Do not ask field by field.

## Before

Check before creating anything. Ethan makes these by hand sometimes.

1. Gong: the folder `[Outbound] {title} [GTM Play] [v0]` and both child flows, Auto and Manual. If a flow is already there, keep its `flow=` id and do not duplicate it.
2. Salesforce: a campaign whose name is that flow's title, or whose external id is that flow id. If it is there, do not submit the Typeform for it.

Create only the piece that is missing.

## After

Watch `#__copilot_marketing` (`C08P5NZ4J1Z`). A finished Typeform posts from Clay Bot: it tags Ethan, says the campaign was submitted, and links the Salesforce campaign. `Already Exists? false` means the campaign is new. `Already Exists? true` means the before-check should have caught it.

The order is: submit the form, Salesforce creates the campaign (Created By shows Spencer Chemtob), then Clay Bot posts it. The post came about two minutes after the submit on 2026-10-10.

The campaign id in that post is only the pointer. Read the record: name is the flow title, External ID is the `flow=` id. Snowflake (`FIVETRAN.SALESFORCE.CAMPAIGN`) is enough once it has synced, but that sync can be many hours behind. Until then, read the campaign page in the signed-in work Chrome profile.

Write that pair onto [Gong Enrollment](gong-enrollment.md) and [Campaign Member](campaign-member.md) only after Snowflake shows it. Both flows have to pass before the step is done.

## Core

1. **Title.** A play has three names, and they are not the same string. The folder name (`plays/trial-extension-non-converters`, lifecycle name `Trial Extension Non-Converters`) stays in the repo. The Gong title is the words Ethan confirms, and only those words go in `[Outbound] {title} [GTM Play] [v0]`. The Qualification Trigger on [Route & Score](route-and-score.md) is those same words, not the folder name and not the full bracketed flow name. Ask him to confirm the Gong title. Recommend the name already on the flows when they exist. His answer is verbatim.
2. **Folder.** Inside `[LIVE] GTM Plays`, one folder: `[Outbound] {title} [GTM Play] [v0]`. Drop a trailing `(2)` if Gong adds one on duplicate.
3. **Two flows.** Duplicate the Closed-Lost Re-heat manual flow and the Closed-Lost Re-heat auto flow. Rename only the title part.
   - `[Outbound] {title} [GTM Play] [Auto] [v0]` is Tier 3.
   - `[Outbound] {title} [GTM Play] [Manual] [v0]` is Tier 1 and Tier 2.
4. **The id is `flow=`.** Open each flow. The Gong URL has `folder=`, `flow=`, and `flow-step-id=`. The Typeform and every later enroll use `flow=`. `flow-step-id=` is the step on screen. It can sit in a comment. It is not enrolled and it is not written on the campaign.
5. **Typeform, twice.** https://clayhq.typeform.com/to/UPvikaV0. Auto first, then manual. The date is three boxes, month, day, and year, set to the day the form is filled.

| Field | Value |
| --- | --- |
| Work email | ethan.huang@clay.com |
| Highest-level parent SFDC Campaign ID | blank |
| Platform External ID | blank |
| When do you expect to start receiving leads | Month, Day, Year of the day the form is filled |
| Description | `{flow title}:` then the one sentence from the overview |
| Partner SFDC Account ID | blank |
| Campaign Type | `L` Hybrid Outbound (GTM Play) |
| Campaign Name | the flow title, `[Auto]` or `[Manual]` included |
| Type | Hybrid Outbound |
| Subtype | GTM Play |
| Gong ID | that flow's `flow=` id |
| External ID Source | gong |

6. **Write the ids back.** `manual_flow_id` and `auto_flow_id` go on [Gong Enrollment](gong-enrollment.md). When the form's campaign exists, `campaign_by_flow` on [Campaign Member](campaign-member.md) maps each flow id to its campaign id. Same number in both places.

## Parameters

| Parameter | Meaning | Values today |
| --- | --- | --- |
| `title` | The words inside the Gong name. Ethan confirms this once | Trial-extension: `Trial-extension Follow-up`, confirmed 2026-10-10. Gong folder and both flows already exist, so they are not duplicated |
| `one_sentence` | The line after the flow title in the Typeform description. Comes from the overview | Trial-extension: `Follows-up on people who requested a trial extension but are not paying customers.` |
| `auto_flow_id` / `manual_flow_id` | `flow=` after the duplicates exist | Trial-extension auto `4519910719264475895`, manual `3893909031139751666` (10 steps) |
| Campaigns | From the Typeform | Trial-extension auto `701a700001K2Lr7AAF`, manual `701a700001K2DBqAAN` |

## Must Not

- Do not put `flow-step-id=` in the Gong ID field. Andrew Morris, 18 Sep 2026, while filling this form with Ethan: the number after `flow=` in the URL is the id that attaches to the Salesforce campaign. [Andrew / Ethan](https://notes.granola.ai/d/aa2debc0-dd57-4d33-ac63-9b8eae61c7c2). The [Channel Campaigns](https://app.notion.com/p/3187e66eb01480848beefce618701f53) doc calls it the Gong Flow Id.
- Do not type the date as one string. The form is three boxes. An empty month, day, or year is not read.
- Do not leave the Hybrid Outbound page blank. Campaign name, Type, Subtype, Gong ID, and External ID Source are filled on the form, not only in a note.
- Do not keep `(2)` on the folder name.
- Do not enroll a person while setting the campaign up. Enrollment is [Gong Enrollment](gong-enrollment.md). A flow that sends step 1 on enroll sends it the day of the enroll, including Saturday.

## Lessons It Prevents

- Closed-Lost auto enroll returned `Flow not found: 564113302196897991` on 2026-10-10. That number is the step on flow `7315015979702319623`.
- Paid-Alumni campaigns that already have members store the flow id the workflow enrolls: manual `8276418546612004892` (30 members), auto `8002859604966279933` (14 members). The campaigns that store a step id are the ones this card is correcting: Closed-Won Look-alike manual `5579282086908866124`, auto `3306309572467454148`, Closed-Lost auto `564113302196897991`.
- Trial-extension, 2026-10-10: the date boxes and the Hybrid Outbound page stayed empty because the values were written in a note and not into the form.
- Trial-extension, 2026-10-10: an earlier Auto submit made `701a700001K2Ah0AAF`. Its name ends in `[v0]:`, because the description line was pasted into Campaign Name, and its External ID is step `7404360591528569649`. The good Auto is `701a700001K2Lr7AAF`.

## Decisions

Ethan 2026-10-10: store the Gong and Typeform steps on this card. Run them once the overview is signed, in the background, with the cohort counts and the test-record search, from the title and the one sentence on that page. Ask him to confirm the title, then do the rest. He confirmed `Trial-extension Follow-up` and said that folder already exists because he made it. Check Gong and Salesforce before creating, then confirm the Clay Bot post in `#__copilot_marketing` (`C08P5NZ4J1Z`). Same day: the slide may be generated at phase 1 or phase 2, and the Notion one-pager is made when the node chart is signed.
