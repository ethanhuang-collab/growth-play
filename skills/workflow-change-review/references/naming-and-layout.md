# Naming, stages and layout

Use these defaults only when the user/project has not specified a different
scheme. Preserve approved exceptions and record their scope. Do not copy one
project's step numbers, coordinates, gap list or permissions into another.

## Meaning before numbering

- A major number identifies a business stage. Nodes are independently
  inspectable operations with inputs, outputs and failure behavior.
- A singleton can be `5. Gather evidence`. Coherent substeps can be
  `5a`, `5b`, `5c`; a bare gate can own `8a`, `8b`, `8c` outcomes under `8`.
  Letters are not limited to two branches and do not themselves imply parallelism.
- The same operation across independent scenarios can share a stage number
  with sibling letters. Distinct business jobs need distinct stages; shared
  subject matter alone does not justify grouping them.
- A join accepting independent evidence streams is reviewed as its own stage,
  rather than automatically inheriting one incoming branch's number.
- Compare addresses case-insensitively. Different titles do not make duplicate
  `5a` addresses unique. Preserve stable IDs through every rename.
- Follow the configured title grammar, including approved wrappers such as
  brackets. Unknown parsing is an evidence gap, not permission to drop a card
  or silently overwrite its title.

## Title-only headers

For three or more sequential executable substeps within one stage, provide a
title-only heading such as `5. Email gatherer` above `5a → 5b → 5c`.
Determine chain length from real dependencies, not array order or node count.
Three exclusive branches are not a three-step chain. An existing bare gate
already supplies its stage heading; do not add a competing duplicate.

The heading is a frame, annotation or group title, not a runnable no-op node.
It has no input bindings, transitions, per-node test or execution count. Keep
the substeps visible. Recompute header eligibility when nodes are removed;
when a chain shrinks below three, a title is no longer required, not forbidden.

Verify native group support and boundary restrictions before proposing a
native group. If grouping would require rewiring, preserve the graph and report
the native gap; show the heading in the review diagram instead. A partial
native group must say which nodes it includes and must not imply full coverage.

## Renumbering decision

Always inspect the whole stage map after a structural edit. Inspection does
not authorize changing all of it. Existing approved gaps remain valid.

| Change | Required analysis | Confirmation boundary |
| --- | --- | --- |
| Remove 5b from 5a→5b→5c | Repair its consumers; stage 5 still exists. | Show the local 5c→5b option before compaction. |
| Remove stage 5 entirely | Identify affected edges, consumed data and current references. | Show 6→5, 7→6… and ask once before shifting. |
| Reduce a stage to one node | Check the selected singleton convention. | Surface the local 5a→5 rename in the same decision. |
| Insert before stage 1 | Prepare valid ordering and contracts. | Do not invent 0 or silently shift the workflow; preview the required map. |
| Rename an operational target | Find exact name-based code and lookup consumers. | Explicitly approved renaming includes required consumer repair; do not ask twice. |
| Explicitly retire a card | Confirm it is outside the active execution graph. | Follow the retirement naming rule; keep its bounds in visual QC. |

Confirmation example, populated with actual values: “This removes one business
stage. Keep the remaining numbers, or renumber the 12 nodes in this map to close
the gap?” Count changed nodes, stages and headings separately. Avoid asking
whether to rename “everything” when only one lane is affected.

While a choice is pending, retain valid existing addresses and record gaps. If
the proposed edit necessarily makes naming or executable references invalid,
keep the candidate unapplied; do not describe it as complete. Unknown rewiring
semantics require a separate concrete decision, not a generic naming approval.

## Geometry and precedence

- Dependent paths normally progress downward. Independent branch starts share
  a level and use compact numerical left-to-right lanes. This is not a global
  rule that every node numbered 9 must sit below every node numbered 8.
- Sequential letters progress downward; independent sibling letters progress
  horizontally where native port order permits. Never add edges for appearance.
- Immutable native output ports outrank a preferred failure-left/success-right
  convention. Preserve branch meanings and endpoints; route wires and place
  destinations to fit. A port exception does not waive crossing checks.
- Explicit section boundaries or sideways bridges override the default only
  for their named scope. Preserve them using stable identities, not brittle
  assumptions that a particular number always occupies that section.
- Preserve manual placement. Do not invoke an autoformatter unless included in
  the requested change, followed by verification against the project contract.
- Check all visible cards, including disabled/disconnected/retired cards, for
  overlap and wire clearance. Only explicitly retired cards get retirement
  label exceptions; an accidentally disconnected active node is still a defect.
- Saved coordinates prove persistence, not wire readability. Inspect rendered
  paths, port origins, crossings, labels, long bypasses and card bounds. Report
  unavailable native geometry as unknown even if authored diagrams look clean.
