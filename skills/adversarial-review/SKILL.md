---
name: adversarial-review
description: Run an independent adversarial review of an artifact with isolated agents and a verifying judge. Use when Ethan says "fire adversarial agents", "adversarial review", "independent reviewers and a judge", "red-team this plan", "have two agents attack it and a third decide", "QC agent loop", "independent readers plus adjudicator", "score these outputs against my labels", or asks whether a plan, spec, prompt, workflow graph, or batch of generated outputs would survive hostile review. Three modes - design-review (planner, two adversaries, judge), output-qc (N readers, two adjudicators, agreement gate, gold labels), critic (one adversary plus author response). Not for ordinary diff review, QC bundles, or best-of-N variant generation.
status: active
maturity: trial
---

# Adversarial Review

## Role

Produce one verified, ranked set of actions on an artifact by having agents
that cannot see each other attack it, then having a judge on a different model
family check their claims against the primary source. The value is
independence plus verification. An adversary who sees the other adversary
converges; a judge who trusts the adversary's quote inherits its mistake.

The parent agent owns the brief, the lane split, the judge's sanity pass, the
review doc, and the final recommendation. Adversaries and judges are read-only.

## Boundaries

- Use `review` for an ordinary single-pass diff or PR review with no
  independence requirement.
- Use `qc` for the ship/no-ship bundle (tests, visual QA, security lanes).
  `qc` may call this skill as one lane when a plan or prompt needs attack.
- Use `subagent-orchestration` for lane mechanics, fan-out sizing, and the
  subagent return contract. Its Parallel Plan Review mode (explorers then one
  critic) is for forming a plan; this skill is for attacking an artifact that
  already exists.
- Use the `peer-review` rule (`~/.cursor/rules/peer-review.mdc`) when Ethan
  pastes another model's findings and wants them evaluated; that is the judge
  step alone, in the parent thread.
- Do not use for best-of-N variant generation; adversaries find faults, they
  do not produce competing artifacts.
- Do not run it on an artifact under 60 lines or a question with one factual
  answer. Check it yourself.
- Stop and ask when no primary source exists to verify against (no file, no
  transcript, no data). A judge cannot verify claims about a conversation.

## Mode Selection

| Artifact | Mode | Lanes |
|---|---|---|
| Plan, spec, design doc, workflow graph, architecture, build contract, SOW, prompt set | `design-review` | 2 adversaries, 1 judge |
| Batch of generated outputs that a human could label (digests, labels, extracted records, scored rows, N emails) | `output-qc` | N readers, 2 adjudicators, agreement gate |
| One prompt, one email, one node, one short doc, a single function | `design-review` by default; `critic` only when Ethan asks for a quick pass | 2 adversaries from different points of view, 1 judge |

Length is not the selector. A short artifact still has independent angles
(correctness, failure modes, the reader's experience, cost, the operator who
has to live with it), and one critic covers one of them. Default to two
adversaries with explicitly different points of view and, when the harness
offers more than one model family, put them on different families and the
judge on a third; record which lane ran on which family in the review doc.
Use `critic` only when Ethan explicitly asks for a quick or single-critic pass,
or when the artifact will be discarded within the day and nothing downstream
depends on it. (Ethan, 2026-10-06: "length doesn't mean there isn't stuff to
review; we want different points of view, ideally different models, for full
coverage.")

Use `output-qc` only when a rubric exists or Ethan will hand-label a gold set
(10-20 items) first. Without gold labels, readers and adjudicators can agree
and still be wrong; agreement is not accuracy.

## Shared Rules

**Independence.** Adversaries and readers receive the artifact, the brief, and
the primary sources. They never receive each other's output. The judge receives
the artifact, the brief, and all adversary output. Launch adversaries in one
message so neither can be influenced by a result.

**Model diversity.** Adversaries run on different model families from each
other when the harness offers them; the judge and adjudicators run on a family
different from the artifact's author and from the adversaries. Ethan's standing
preference (2026-10-06) is diversity for coverage, so when the harness lists
multiple families and he has not named models, choose distinct families per
lane from the harness's available list and name them in the review doc; fall
back to `inherit` only when the harness restricts model choice to the user's
explicit request, and say so. When only one family is available, still separate
the judge into its own context window. Adjudicator A and B in `output-qc` must
differ from each other.

**Finding format.** Every finding, from every lane:

```
[blocker|major|minor] <claim in one sentence>
  cite: <path:line | node id | section heading | item id>
  breaks: <what fails or regresses, and the mechanism>
  fix: <smallest change that removes it>
```

No praise. No restating the artifact. No findings without a citation. Default
cap 600 words and 12 findings per adversary; the brief may tighten it.

**Judge verification.** The judge labels each finding `HOLDS`, `PARTIAL`,
`FAILS`, or `REJECTED` and may throw findings out. For any finding that will
appear in the ranked actions, the judge must open the cited primary source
and confirm the mechanism, not just the quote. Known failure (2026-10-06): a
judge-verified finding claimed "3/8 to 8/8 self-grading" in a build; the judge
confirmed the numbers existed but not what produced them. The numbers were a
builder's phrase-count of prompt text, not a graded result. The finding
survived into the recommendation because the judge verified existence, not
mechanism. A citation that exists is not a claim that holds.

**Parent sanity pass.** After the judge returns, the parent re-opens the primary
source for the top three ranked actions. If one fails, demote it, note the miss
in the review doc, and treat the judge's other `HOLDS` labels as `PARTIAL`
until spot-checked.

**Budget and stopping.** Medium effort, built for speed (Ethan, 2026-10-06:
"a medium-effort good adversarial, but I want to keep moving"). One round by
default: both adversaries launched in one message so they run in parallel,
each capped at about 600 words and told to return within one pass; the judge
runs once. Model diversity must not add wall clock: pick the fastest capable
model per family, never chain lanes sequentially to get diversity, and fall
back to one family rather than wait. Target under 15 minutes per round.
Rounds continue while the last round produced at least one new material
finding (something the author would change); stop on the first round that
adds nothing new, or when the judge confirms zero blockers. Each round is
individually bounded so the loop stays fast even when it runs several times;
the cost that matters is wall clock per round, not round count. (Ethan,
2026-10-06: "keep going until we have exhausted; if you keep finding good
stuff, keep pushing back.") Record the round count in the review header.

**Surfacing.** Write one review doc; post a chat summary of at most ten lines
that links to it. Ethan reads the ranked list, the contradictions, and the
"both missed" section, not the raw lane output. In `output-qc` he sees only
the disagreement rows and the gold-score table.

**Read-only.** No lane edits the artifact, runs live actions, or writes to
external systems. The author (or parent, once Ethan agrees) applies fixes after
the review doc exists.

## Mode: design-review

When: a plan or spec Ethan will build from, before implementation starts or
before publish. Cost: 3 agent calls (4 if the planner is also a lane), two
sequential waves (adversaries in parallel, then judge), roughly 10-25 minutes
wall clock on a 300-800 line artifact.

1. Brief: artifact path(s), primary sources it cites, what counts as a
   `blocker` for this artifact, out-of-scope concerns, word cap, model plan.
2. Adversary A lens: feasibility and assumptions. Will this build and run as
   written; which inputs, APIs, limits, permissions, data shapes, or sequencing
   claims are unproven; where does the plan assume evidence it does not cite.
3. Adversary B lens: failure modes and blast radius. What happens on empty,
   duplicate, late, malformed, or hostile input; which step can silently pass;
   which external write, cost, or human handoff goes wrong; what is missing.
   Swap lenses when the artifact's risk is elsewhere (for a prompt: instruction
   conflicts vs. output-contract violations; for a SOW: scope ambiguity vs.
   delivery risk). Lenses must differ.
4. Judge (different family): dedupe, verify at least six citations by opening
   the source (all of them if fewer than six), label each finding, resolve
   contradictions with a one-line reason, list what both adversaries missed,
   return at most twelve ranked actions. The judge may REJECT findings and may
   add at most three of its own, clearly marked.
5. Parent sanity pass on the top three, then write the review doc.

Prompt skeletons: `references/prompt-skeletons.md` sections A, B, J.

## Mode: output-qc

When: N generated outputs that should match human judgment, such as loss
reason labels, call digests, extracted records, scored emails, or graded
images. This is the loss-buckets v2 method (`references/prior-art.md`).
Cost: N/batch reader calls plus 2 adjudicators plus one third-read per
disagreement; the 50-deal pilot ran about 6 minutes of 10 readers and 27
minutes of 2 adjudicators.

1. Rubric and gold: a written rubric with precedence rules for the hard
   boundaries, and 10-20 items Ethan has labeled. If either is missing, build
   it first; do not substitute agent consensus.
2. Readers: size by `subagent-orchestration` fan-out rules (3-7 items per
   reader for transcript-length items, more for short rows). Each reader gets
   its items, the rubric, and the primary sources, and returns one schema-valid
   label per item with a verbatim quote, speaker or locator, and confidence.
3. Adjudicators A and B: two independent full re-reads of all N items on
   different model families. They see the reader labels as a draft and may
   overturn them. Check adjudicator output against the primary source's
   speakers, dates, and ids before trusting it; the pilot's adjudicator B
   briefly produced entries citing speakers absent from the files.
4. Agreement gate: A = B is the answer. Disagreements go to a third read by the
   parent from the quotes and the primary source, with a one-line reason.
5. Score against gold. Report agreement per field, list each gold miss with
   a diagnosis, and say whether the miss is the model's or the gold label's.
6. Fold rule gaps back into the rubric. Most adjudicator disagreement is a
   rubric boundary, not a model failure; record the rule edit, not a retry.

Prompt skeletons: `references/prompt-skeletons.md` sections R, ADJ.

## Mode: critic

When: one small artifact. Cost: 1-2 agent calls, under 10 minutes.

1. One adversary with the finding format and a 300-word cap, lens chosen by
   the parent from the artifact's largest risk.
2. Author response in the parent thread: accept, reject with reason, or defer
   each finding. The parent verifies any accepted `blocker` against the source.
3. No judge. Escalate to `design-review` if the critic finds a blocker the
   author rejects, or if the artifact meets an escalation trigger above.

Prompt skeleton: `references/prompt-skeletons.md` section C.

## Workflow

1. Classify the artifact and pick the mode from the table. State the mode,
   lane count, model plan, and expected cost in one sentence before spawning.
2. Write the brief. Name the primary sources the judge will verify against. If
   none exist, stop and ask.
3. Spawn the independent lanes in a single message, read-only, with distinct
   lenses and the finding format. Do not paste one lane's output into another.
4. Run the judge or adjudicators on a different model family where possible.
   Require the verification labels and the primary-source re-read.
5. Parent sanity pass on the top three actions (or the disagreement rows).
6. Write the review doc from `references/review-doc-template.md` at
   `reviews/<YYYY-MM-DD>-<artifact>-adversarial-review.md` in the owning
   project or repo. Post a chat summary of at most ten lines linking to it.
7. Hand the ranked list to the author. Second round only if the stopping rule
   allows it.
8. Log the run:
   `~/Code/coding-system/scripts/skill-maturation.py adversarial-review --log-run --trigger "<phrase>" --outcome <ok|mixed|miss>`.

## Checks

- Every lane output uses the finding format with a citation; findings without
  one are dropped before the judge sees them.
- Adversaries received no other lane's output (check the prompts you sent).
- Judge or adjudicator model family differs from the authors, or the doc says
  why not.
- Judge verified at least six citations by opening the source and labeled all
  findings; at least one `REJECTED` or an explicit "nothing to reject".
- Parent re-opened the primary source for the top three actions.
- Review doc exists, is under 150 lines, has the contradictions and
  "both missed" sections, and the chat summary is at most ten lines.
- `output-qc` only: gold set exists before readers run, agreement reported per
  field, every gold miss diagnosed.
- No lane edited the artifact or touched a live system.

## Output Contract

Chat (at most ten lines): mode, lanes and models used, blockers confirmed,
top three actions, link to the review doc, residual risk.

Review doc:

- Header: artifact, mode, lanes, models, rounds, wall clock, cost note.
- Ranked actions (at most twelve), each with severity, verification label,
  citation, and fix.
- Contradictions: where adversaries disagreed and how the judge resolved each.
- Both missed: what the judge or parent found that no adversary raised.
- Rejected findings: what was thrown out and why, one line each.
- Verification log: which citations were opened, and any judge or parent miss.
- `output-qc` adds: agreement table per field, gold-score table, disagreement
  rows with the third-read reason, rubric edits proposed.
- Next: who fixes what, and whether a second round is allowed.

## Resources

- `references/prompt-skeletons.md`: adversary, judge, reader, adjudicator, and
  critic prompt blocks with the finding format and verification labels.
- `references/review-doc-template.md`: the review doc skeleton.
- `references/prior-art.md`: the loss-buckets v2 pilot, aa-visual-intake
  dual-read adjudication, Bain advisors G6 adversarial re-verification, and the
  2026-10-06 judge mechanism miss this skill is built from.
- `~/Code/coding-system/templates/subagent-task-prompt.md` and
  `templates/parallel-plan-review.md` for lane mechanics.
