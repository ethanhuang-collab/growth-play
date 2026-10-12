# Global Blocks

A global block is a piece of a growth play that every new play reuses the same way. Each one has its own file, named for what it does. This folder is the copy that ships with the lifecycle kit. The numbered cards in the growth-plays repo, under `building-blocks/graph/`, `building-blocks/kit/`, and `building-blocks/functions/`, are older pattern notes from Closed Lost v7. They are referenced where useful, but a new play is built from the files in this folder.

Existing workflows keep running as they are. A play adopts a global block when someone rebuilds that part of it.

## Core And Parameters

Every global block has two kinds of content.

- **Core** is logic that is the same in every play. A play does not edit it. Changing it means a new version of the block. Example: an open opportunity stops the account.
- **Parameters** are the values each play fills in, like blanks on a form. Example: this play's Gong flow id, its Salesforce campaign ids, the cooldown window in days.

The test: if two plays could reasonably disagree on it, it is a parameter. If disagreeing would be a bug, it is core.

## The Blocks

Names are the ids. The "was" column is only for finding older notes.

| Block | What it does | External write | Was |
| --- | --- | --- | --- |
| [Suppression](suppression.md) | Stops the account or skips one person | none | card 40 |
| [Best Ranked Contacts](best-ranked-contacts.md) | Picks the best workspace user to contact | none | card 39 |
| [Route & Score](route-and-score.md) | Makes sure a ClayDR owns the account, then finds the GTME if there is one | Salesforce (function side) | card 33 |
| [Gong Enrollment](gong-enrollment.md) | Puts the picked person in this play's Gong flow | Gong | card 16 |
| [Action Queue](action-queue.md) | Gives the ClayDR a Terra to-do for that person | Salesforce `Signal_Action__c`, shown in Terra | cards 18, 36 |
| [GTME Copilot Post](gtme-copilot-post.md) | Tells the account's GTME in their copilot Slack channel | Slack | card 38 |
| [Campaign Setup](campaign-setup.md) | Makes the Gong folder, the two flows, and the Salesforce campaigns. Runs in the background once the overview is signed | Gong, then Salesforce through the Typeform | none |
| [Campaign Member](campaign-member.md) | Records the person on this play's Salesforce campaign | Salesforce | cards 17, 36 |
| [Write Failure](write-failure-alert.md) | A failed write stays on the run record | none | card 20 |
| [Test Mode](test-mode.md) | Sends every test to Ethan's seats instead of the real people | none | card 41 |

Not global: message generators (card 32), Find People at Company (card 34), email and phone waterfalls (card 35), and the Notion recap. Closed Lost keeps its own recap chain. A play that needs one of these draws it out in full.

## Card Shape

Every global card has these parts, in this order:

1. A header table: id, version, status, what it does, inputs, outcomes, external writes and how to undo them, pins (function id, Claygent id and version, Salesforce account), consumers, and the old card number.
2. **Core.** The rules every play follows.
3. **Parameters.** A table of the blanks, what each means, and the value each play uses today.
4. **Must Not.** Mistakes that have already happened once.
5. **Lessons It Prevents.** The run or chat where each rule was learned.
6. **Decisions.** Where Ethan agreed to it.

A card is complete before a play uses it. A new fact goes into the card once, and the next play reads the card. It does not rediscover the block.

## How A Global Block Shows On A Chart

On the node chart a play may draw a global block as one box, named for the block. The box lists the node labels it contains. Only blocks in this folder may be collapsed this way. Anything else is drawn node by node.

- A box with an external write is orange: `classDef write fill:#FDE2C8,stroke:#D9822B,color:#4A2A0A`.
- Test Mode nodes are green: `classDef testMode fill:#D6F0D8,stroke:#3C8A46,color:#123D18`.
- Nothing else is colored.
