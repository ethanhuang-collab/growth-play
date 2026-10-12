# Prior Art

What this skill is distilled from. Read when deciding whether a mode fits, or
when Ethan asks "is this the same as the QC agent loop I used before".

## Loss Buckets v2 Pilot (2026-09-09) - the `output-qc` mode

Source: `docs/plans/2026-09-09-loss-buckets-v2-pilot.md`; retro at
`clay-planning-system/docs/reviews/2026-09-09-closed-lost-workflow-retro.md`
(sections 3.6 and "What went right").

- 50 closed-lost deals, two-axis rubric with explicit precedence rules, 20
  gold deals hand-labeled by Ethan first.
- 10 parallel readers (one fast model), 5 deals each, full transcripts plus
  rules; all 50 labels schema-valid in under 6 minutes.
- Two adjudicators on different model families did independent full re-reads
  (9 and 27 minutes). Agreement gate: A = B is final (42/50 on all fields);
  8 disagreements went to a third read by the orchestrator.
- 86% agreement with Ethan's gold labels. Of the two misses, one was a
  mislabeled speaker in the gold set, not a model error.
- Lessons folded in: check adjudicator quotes against the source's speakers
  and dates (adjudicator B briefly cited speakers absent from the files);
  most disagreement was a rubric boundary ("stated condition is not a reason",
  "Deferred requires the later time as the reason"), fixed by rule edits, not
  by rerunning; readers are a good cheap first draft, adjudicators are the
  quality.

## aa-visual-intake Overlay Sweep (2026-08-19) - dual-read plus adjudication

Source: `projects/aa-visual-intake/QC.md` gate log, `pipeline/qc/`.

- Dual-read detection on 400 images with 10 adjudications on disagreement;
  concentric coverage expansion (10% ring first, same bar before widening).
- First 10% grade sample hit 18% disagreement, all on one rubric boundary;
  adjudicated by direct view, rubric tightened, full population re-audited.
  Same lesson as loss buckets: disagreement locates the rubric gap.

## Bain Capital Advisors Directory (2026-07) - adversarial re-verification gate

Source: `projects/bain-capital-advisors/current.md`, `overview.md`.

- Deterministic gates G1-G5 green does not mean facts verified. G2 (cited
  URLs resolve to the claimed fact) and G6 (independent 10% adversarial
  re-verification, prioritizing senior, thin, and conflicting records) were
  left explicitly open rather than claimed.
- Pattern carried into this skill: "a citation exists" and "the citation
  supports the claim" are separate checks, and the second is the judge's job.

## Palantir-type Work

Ethan recalls an earlier QC agent loop with independent agents on Palantir
interview prep. The vault's `projects/palantir-interview-prep/` notes do not
record the loop's mechanics, so nothing from it is encoded here beyond the
shape Ethan described (independent agents, then a QC pass). Add a section if
the original artifacts are found.

## Judge Mechanism Miss (2026-10-06) - why the judge re-reads the source

During an adversarial review of a Clay workflow build, a judge marked a finding
as verified: the build had "self-graded 3/8 then 8/8" on a check, implying a
grading loop that had been gamed or was circular. The judge confirmed the
numbers appeared in the cited file. The numbers were a builder's phrase-count
over prompt text (how many required phrases were present), not a graded
result at all. The finding drove a recommendation that was wrong in mechanism.

Rules that came out of it, now in SKILL.md:

- The judge verifies mechanism, not existence, for any finding it ranks.
- The parent re-opens the primary source for the top three actions.
- One parent miss downgrades the judge's other `HOLDS` labels to `PARTIAL`
  until spot-checked.
- Labels are `HOLDS / PARTIAL / FAILS / REJECTED`; "verified" alone is not a
  label.

## Neighboring Skills And Rules

- `subagent-orchestration`: lane mechanics, fan-out sizing, Parallel Plan
  Review (explorers then critic, for forming a plan rather than attacking one).
- `qc`: ship/no-ship bundle; may use this skill as one lane.
- `review`: single-pass findings standard this skill's finding format extends.
- `~/.cursor/rules/peer-review.mdc`: evaluate another model's findings in the
  parent thread; equivalent to the judge step alone.
- `~/.cursor/rules/parallel-subagents.mdc`: launch independent lanes in one
  message; model default for subagents.
