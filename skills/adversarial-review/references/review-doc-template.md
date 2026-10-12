# Review Doc Template

Save at `reviews/<YYYY-MM-DD>-<artifact>-adversarial-review.md` in the owning
project or repo. Keep it under 150 lines. The chat summary is at most ten lines
and links here.

```md
# Adversarial Review - <artifact name>

Date: <YYYY-MM-DD>
Artifact: <path or id, version or commit>
Mode: design-review | output-qc | critic
Lanes: <A lens / B lens / judge> or <N readers / adjudicators A, B>
Models: <per lane, or "inherit; single family available">
Rounds: <1|2>  Wall clock: <min>  Agent calls: <n>

## Ranked Actions

| # | Sev | Label | Finding | Cite | Fix |
|---|---|---|---|---|---|
| 1 | blocker | HOLDS | ... | path:line | ... |

## Contradictions

- <A said / B said / judge picked / reason or "needs human">

## Both Missed

- <JUDGE-ADDED or PARENT-ADDED finding, cite, fix>

## Rejected

- <finding> - <one-line reason>

## Verification Log

- Judge opened: <citations>
- Parent sanity pass (top 3): <held / demoted #n because ...>
- Misses: <judge or parent errors found, or none>

## Next

- Owner: <who fixes>
- Second round: allowed | not allowed (<stopping-rule reason>)
- Residual risk: <one or two lines>
```

## output-qc Additions

```md
## Agreement

| Field | Readers vs final | A vs B | Final vs gold |
|---|---|---|---|

## Disagreement Rows

| Item | Reader | Adj A | Adj B | Third read | Reason |
|---|---|---|---|---|---|

## Gold Misses

- <item>: <final vs gold> - <model miss | gold-label miss> - <diagnosis>

## Rubric Edits Proposed

1. <rule text to add or change> - removes <k> of <n> disagreements
```
