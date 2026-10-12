---
name: growth-play-notion
description: >-
  Write or refresh an internal growth-play Notion one-pager in the locked
  five-section shape: Overview, How It Works, Sample Outputs, Success
  Criteria, and Reference And Considerations. Make it when the node chart is
  signed. Do not wait to be asked. Update that same page after a build, a
  test, or a publish. Not for a Clay workflow build, a customer SOW, a
  customer handoff, or the Q3 tracker.
status: active
maturity: trial
last_matured: 2026-10-08
---

# Growth Play Notion

## Role

Turn a growth play into one internal Notion page, and keep that page current. Make the page when the chart is signed (the signed `overview.md` and the signed `workflow-plan.md` exist). Do not wait to be asked. Rewrite it after each later phase: built, tested, published. This skill only chooses what a reader sees, and in what order.

The locked example is [WIP] Growth Play: Closed-Lost Re-engage [template](https://app.notion.com/p/3f47e66eb0148101ae57ed0cbd10cc8d). It is read-only. Match its shape. Do not copy its numbers onto another play.

## Inputs

- The signed `overview.md` (prose sections, stage map, outcomes, cohort numbers).
- The signed `workflow-plan.md` (node names and the mermaid charts).
- When the play has a workflow id, `clay workflows graph get <wf> --mode summary` for the live node titles and edges. Live titles win over the plan's names.
- `<play>/notion-page.md` when it exists: the page this play already has.
- The play's release record, `<play>/qc/*/releases.jsonl`, to know whether a version is published. `status.md` can lag a publish by minutes; the receipt file does not.

## Boundaries

- Stop if the chart is not signed yet: no `overview.md`, no `workflow-plan.md`, or the stage list is still a guess. Name what is missing. Do not draft the page.
- `clay-sow-generator` owns a customer statement of work. `clay-handoff-doc-generator` owns a build handoff for someone who will implement the table. `clay-workflow-qc` owns node-by-node workflow review. This skill owns the internal one-pager.
- The recorded-URL rule. The only page this skill may edit is the one whose URL is in `<play>/notion-page.md`. A play with no `notion-page.md` always gets a new private page, and its URL is written there. Never edit the Q3 tracker, the locked example, or any page whose URL is not in the play folder.
- The page stays business-level. No ids, SQL, prompts, schemas, or constants. Those stay in the source files, named in backticks inside Reference And Considerations.
- Later decisions beat earlier docs. A live graph beats a mermaid picture at the top of the plan when the two disagree. Say so in one sentence.
- Before publish, the status line says where the play is: "Chart signed, not built" or "Built, not published". After publish it says "Live since" the date and the version, plus one sentence on where sends go when the test seats are still on. Read `releases.jsonl` before writing it.

## Workflow

Two modes. Decide by whether `<play>/notion-page.md` exists.

**Create mode** (no `notion-page.md`):

1. Read the inputs above. If a workflow id exists, read the live graph; otherwise the plan's node names are the titles.
2. Create a new private Notion page. Title Case every heading. The five sections, in this order, are the whole page. Fold anything else into one of them.
3. Put a link callout above Overview: the Clay workflow, then each live campaign or other send destination.
4. Fill the five sections from [references/page-shape.md](references/page-shape.md). Overview is prose. How It Works is the stage chart, then the stage table, then the chart toggles. Sample Outputs lists every artifact. Success Criteria states the measures. Reference And Considerations is one toggle.
5. Draw charts from the live node titles when a live graph exists, otherwise from the plan's node names. Render each chart to an image so the test-mode color shows, upload it, and embed the image. Do not leave the chart as a code block, and do not invent a simplified sketch with shortened labels.
6. Write `<play>/notion-page.md`: the page URL, the date, the source commit of the play folder, and the phase the page describes. That file is the only play-folder write this skill makes.
7. Fetch the page and run the Checks list before calling it done.

**Update mode** (`notion-page.md` exists):

1. Read `notion-page.md`, fetch that page, and confirm the fetched URL matches the recorded one. Stop if it does not.
2. Read the inputs again, including the live graph when there is one.
3. Replace the five sections (and the link callout) with the new content. Keep the page title. Upload new chart images; an image already on the page cannot be matched by search-and-replace, so the content is replaced whole.
4. Bump **Last Updated** to today and the status line to the play's current phase.
5. Append a dated line to `notion-page.md` with the source commit and the phase. Do not make a second page.
6. Fetch the page and run the Checks list.

## Checks

- The five section headings are present, in order, and nothing else is a top-level section.
- Overview has one governing sentence, status and DRI, **Last Updated** on its own line, and volume as one prose line. No Why Now. No volume table and no volume chart.
- **Last Updated** is today.
- The status line matches the play's phase: "Chart signed, not built", "Built, not published", or "Live" with the date.
- The page URL in `<play>/notion-page.md` is the URL of the page that was fetched. No second page exists for the play.
- The visible chart uses the same stage names as the table. The table columns are Stage, What Happens, and Stops If.
- Chart toggles are siblings. A chart toggle is never inside another chart toggle.
- Full Node Graph uses full titles (`1A. Name`). Only test-mode nodes are green: `classDef testMode fill:#D6F0D8,stroke:#3C8A46,color:#123D18`.
- Every zoomed chart repeats the node it starts from and the node it returns to, with the same title as the chart above it.
- Sample Outputs includes every artifact a counted run leaves. Variant copy sits in toggles, verbatim.
- Reference And Considerations is one toggle. Filenames are in backticks. A staff-email rule says "Clay staff email", not a bare domain.
- The page fetch shows each image inside its own toggle, and the stage chart above the table.

## Output Contract

Return the mode (create or update), the Notion URL, the five section headings, the chart toggles by level, and the status line. If a live title differed from the plan, name that one difference. Do not paste ids, SQL, or prompts into the reply.
