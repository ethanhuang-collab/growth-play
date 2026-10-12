# Page Shape

The five headings are verbatim. Title Case on the page.

## Link Callout

Above Overview. The Clay workflow link, then each live campaign or send destination. No ids in the label. The link itself may contain the id.

## Overview

- One sentence: what starts a run, and what a finished run does.
- **Status** and **DRI** on one line. The status names the play's phase, in these words: "Chart signed, not built" (the pages are signed and no node exists), "Built, not published" (the workflow exists and is unpublished; say where the test sends go), or "Live" with the publish date. One more sentence of context is allowed.
- **Last Updated:** on its own line. The date only. It is today on every create or update.
- Volume on one line. Eligible today, new entrants per week, or both. Quick stats. Not a table. Not a bar chart.
- No Why Now section. No Who Gets What.

## How It Works

One sentence under the stage chart: the run starts from one record, and cheap checks run before anything is sent.

### Stage chart and table

The chart a reader sees first uses the stage names from the table. Each stop leaves the path. The table is:

| Stage | What Happens | Stops If |
| --- | --- | --- |
| 1. Name | What this stage decides, in one or two sentences. | The stop, in the play's words. |

Who Gets What is not a column. Who receives a send belongs in the send step's row, or in Sample Outputs.

### Chart toggles

Sibling toggles. Same heading level within a level. Never nest a chart toggle inside another chart toggle.

**Level 1. Full Node Graph.** One node per step. Title form is `1A. Full Title`, taken from the live node name when that name already has the number. Use the plan's name field when the live name is a platform default such as Webhook. A chain that is its own subgraph is one box. Test-mode nodes are green and nothing else is colored. The live canvas has no color field; the green is diagram-only.

**Level 2.** One toggle per box that level 1 collapsed. Name the toggle after that chain. The chart shows the interior and still collapses any stretch of more than one node into a box. It starts at the level-1 node that enters the box and returns to the level-1 node the box continues into. Same titles on both charts.

**Level 3.** One toggle per remaining multi-node box. These toggles are siblings of each other, not children of the level-2 toggle. Each chart includes the node it starts from and the node it returns to. A cross edge into another level-3 chart shows that other chart's node by its full title.

Stop when every remaining box is one node. Two graphs at the same grain, such as a parent run and a child run, are two level-1 toggles, not a parent with the child nested inside it.

Render mermaid to an image, upload with the Notion file upload, and embed the image. Search-and-replace cannot match an image already on the page. To change a chart, upload a new file and replace the page content.

When there is no live graph yet (status "Chart signed, not built"), the node titles come from the plan's node name fields. When there is one, the live titles win, and the Reference And Considerations toggle names any title that differs from the plan.

## Sample Outputs

Name every artifact a counted run leaves. One toggle per variant, with the verbatim string inside. Label copy that is not final as a placeholder and name who owns it. Link one real example when a test run produced one, and say what that example is missing.

## Success Criteria

The play's own measures, including the launch check. Say "Not yet measured" when that is true. Do not invent a target.

## Reference And Considerations

One toggle. Everything under it is hidden until opened. Put here, and only here:

- Open items
- How the volume number was counted, including what the count skipped
- What changed from the prior version of the play
- A cohort or funnel, collapsed again if it is a table
- Sources, as backticked paths
- Contributors, and who owns a shared function the play must not edit

Do not put a second toggle around the whole section. Nested detail inside it is fine.
