---
name: hand-off-qc
description: Independent second pass on a post-call hand-off packet (Slack hand-off + Salesforce notes) before it is returned to Ethan. Cuts redundant facts stated twice, checks every claim against the Gong transcript, and enforces the hand-off shape. Use after `hand-off` drafts a packet, or when Ethan asks for a QC / de-dupe pass on hand-off notes. Runs in a fresh context that did not write the draft.
status: active
maturity: trial
last_matured: 2026-09-08
---

# Hand-off QC

## Role

Audit a hand-off packet another context just wrote. You did not write it; that
is the point. Read the draft cold, read the transcript cold, and fix what is
redundant, unsupported, or out of shape. Then report what you cut.

This is the hand-off equivalent of `brief-qc-redundancy` in Brief_Builder. The
failure it exists to catch, from the Highbeam packet on 2026-09-08: the header
said "Cameron Kalis, Head of Business Development," and a business paragraph
three lines later said "outbound runs through a BDR team led by Head of
Business Development Cameron Kalis." Same fact, two homes. The writer could not
see it because the writer had just added both.

## Boundaries

- Use `hand-off` to draft the packet. This skill never drafts from scratch.
- Use `brief-qc-redundancy` for pre-meeting briefs; the shape is different.
- Inputs are the draft and the transcript (Gong call id or cached transcript
  file). Do not read the writer's reasoning, chat history, or notes about why a
  line was written. If the launcher passed any, ignore it.
- No external writes. Do not send Slack, do not touch Salesforce, do not commit.

## Workflow

1. **Read the transcript first**, then the draft. Not the other way round; a
   reviewer who reads the draft first goes looking for confirmation.
2. **Redundancy pass.** List every fact in the Slack block: a person's role, a
   company fact, a tool, a number, a quote, a next step. If a fact appears twice
   in different clothes, delete the later copy and keep the first home. Common
   collisions:
   - Header line vs Context (role, company, customer status, call length)
   - Context vs Identified use case (the workflow he described)
   - Pain point vs Blockers (the incumbent's advantage stated twice)
   - Desired outcome vs Next steps (what the demo should show)
   Salesforce notes are exempt from cross-block comparison with Slack: they are
   a separate paste and are meant to restate tech stack, use case, and pain.
   Within Salesforce notes, the three fields must not restate each other.
3. **Support pass.** Every claim must trace to a transcript line or the named
   email thread. Tech stack, use case, pain point, owner, next step: if the
   source is silent, the field says unknown or is cut. Quotes must be verbatim.
   Roles and company facts pulled from LinkedIn or Terra must be labelled with
   their source in the packet.
4. **Pain-point rule.** Pain is their GTM status quo. If Clay did not exist the
   sentence must still hold. Cut Clay plan, price, credits, product gaps, and
   Clay-vs-incumbent bake-off language from the pain field. A bake-off result
   belongs in Desired outcome or Context, not Pain.
5. **Shape pass.** The Slack block has these sections and no others, in order:
   header line, Context, Current tech stack, Identified use case, Pain point,
   Desired outcome, Blockers / risks, Next steps. There is no separate
   Business section; the business model lives at the top of Context. The
   contact's role is in the header line only. Business model is at most three
   sentences of under 25 words each.
6. **Delivery format.** The Slack block ships as a Slack message into
   `#ethan-dr` via `slack_send_message` (a draft only when Ethan asked for
   one), so section labels are `**Label:**` in standard Markdown and nothing
   else is emphasized. No markdown headers, no code fences. If the block is
   being handed back as chat text instead, that is a finding: the packet must
   not be pasted from chat into Slack.
7. Edit the draft in place. Do not restyle sentences you are not cutting.

## Checks

- Zero facts appear twice within the Slack block.
- Zero facts appear twice within the Salesforce notes.
- Every claim traces to the transcript, the named email thread, or a labelled
  outside source.
- Pain point holds with Clay removed from the sentence.
- Section order matches the shape above; no Business section; role only in the
  header.
- Slack block delivered into `#ethan-dr` with `**Label:**` markers only; Salesforce notes carry no markdown emphasis.

## Output Contract

Return the repaired packet (both blocks, still visibly separate), then one
report line per cut or fix:

`cut: <fact> — lived in <section A> and <section B>, kept <A>`
`fix: <what changed> — <why, with transcript timestamp or source>`

If nothing needed changing, say `clean` and list the checks that passed. A
false `clean` is the only outcome here that does real damage.

## Launching

`hand-off` launches this as a subagent with a fresh context: pass only the
draft text, the Gong call id (or transcript path), and the email thread if one
was read. Nothing else.
