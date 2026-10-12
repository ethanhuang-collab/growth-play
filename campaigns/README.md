# Campaign Setup

Campaign setup runs once the overview is signed. It makes the play's Gong folder, the manual flow for Tier 1 and Tier 2, the auto flow for Tier 3, and the Salesforce campaigns those flows enroll into.

The rules are the [Campaign Setup](../blocks/campaign-setup.md) card. This page is the order to run them in. The only question for Ethan is the Gong title. Confirm that title, then do the rest.

## Order

1. Read the signed overview for the title he confirmed and the one sentence that describes the play.
2. Look before creating anything. If the Gong folder and both flows are already there, keep their `flow=` ids. If a Salesforce campaign already matches a flow, leave that Typeform unsubmitted.
3. Inside `[LIVE] GTM Plays`, make `[Outbound] {title} [GTM Play] [v0]` when it is missing. Duplicate the Closed-Lost Re-heat manual flow and the Closed-Lost Re-heat auto flow, and rename only the title part.
4. Submit https://clayhq.typeform.com/to/UPvikaV0 twice, auto first, then manual. The field list is on the card. The Gong ID is the number after `flow=` in the flow URL.
5. Watch `#__copilot_marketing`. Clay Bot posts the Salesforce campaign a couple of minutes after the form. Read the campaign record: the name is the flow title, and the external id is the `flow=` id.
6. Write `manual_flow_id` and `auto_flow_id` onto [Gong Enrollment](../blocks/gong-enrollment.md). When both campaigns exist, write `campaign_by_flow` onto [Campaign Member](../blocks/campaign-member.md).

The node chart does not wait on the campaign ids. The build does.

Gong Engage and the Typeform are external writes. They start after the overview is signed and the title is confirmed.
