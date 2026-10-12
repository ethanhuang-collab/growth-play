---
name: workflow-node-graph
description: >-
  Build precise workflow / DAG node graphs where topology is the content —
  swimlaned process posters and compact pipeline views. Use when the user asks
  for a workflow diagram, node graph, node-and-wire diagram, process map poster,
  process poster, pipeline diagram, DAG, system flow diagram, swimlane diagram,
  "how the whole process works on one page", a print-fidelity or plotter-size
  diagram, or a Clay-style pipeline graph; or wants ownership tracks,
  swimlanes, a dedicated shared lane, review triangles, approval diamonds, a
  shape and tag legend, and looping paths drawn legibly. Covers registry-driven
  HTML rendering, measured node heights, z-order layering, lane rules, loop
  rendering, tag/legend honesty, single-page vector PDF export, and zoomed-crop
  visual verification. This skill only draws a process that already exists — not
  for proportional volume flows (use chart-sankey), editable conceptual sketches
  (use excalidraw-concepts), or designing the orchestration itself (use
  langgraph-builder).
status: active
maturity: maturing
last_matured: 2026-08-07
---

# Workflow Node Graph

## Role

Render a real process as a node graph where **the topology is the content**:
which step follows which, who owns each stretch, where a human gates it, what
loops, and where it ends. Output is a self-contained HTML file rendered from a
data registry, exported as a single-page vector PDF plus zoomed crops.

This is a precision-drawing skill, not an idea-sketching skill. If the arrows
could be rearranged without changing the claim, you are in the wrong skill.

## Boundaries

Three skills now touch "diagrams". Pick deliberately:

| Use | When | Skill |
|---|---|---|
| Editable conceptual sketch, mental model, 5-12 boxes someone will drag around later | The idea is fuzzy and the artifact should stay editable | `$excalidraw-concepts` |
| Proportional ribbon flow where **volume** is the message (counts split and merge, band width carries value) | Quantities matter more than sequence | `$chart-sankey` |
| Precise workflow/DAG where **ordering, gates, ownership and loops** are the message and the output is a print-fidelity poster or a compact pipeline view | Topology matters, quantities do not | this skill |

Also:

- Apply `$professional-graph-making` shared rules on top of this skill: color
  economy (one accent plus neutrals), no decorative styling, quiet type,
  conclusion-first title, source/scope note. This skill wins on type-specific
  geometry; surface any genuine conflict rather than blending silently.
- Use `$frontend-visual-qa` for the rendered-proof loop; this skill names the
  specific crops and checks a node graph needs.
- Use `$slide-making` when the deliverable is a deck; this skill can produce the
  PDF that gets placed on a slide.
- Use `$langgraph-builder` when the ask is to **build** the orchestration —
  persistent state, threshold triggers, retries, approval queues. This skill
  draws the workflow; it does not run it.
- Stop and ask if the process itself is undecided. This skill draws a process
  someone can already describe; it does not invent one.

## Native Clay layout verification

For an existing Clay canvas, inspect its native rendering; a custom diagram
cannot prove native routing. The HTML/SVG/PDF machinery below applies to authored
diagrams, not to Clay's renderer.

1. Read graph identity, dependencies and saved positions through API/CLI first.
   State the specific missing native wire/port geometry before using the browser.
   Open the intended workspace/workflow draft with `?version=edit` (preserve
   other query parameters), save/reload, and verify the displayed draft/edit
   state and expected nodes. The URL parameter alone is not readback proof.
2. Inspect actual ports and trace every rendered edge at usable zoom, including
   fan-ins, fan-outs and long bypass paths past unrelated cards. Record coverage
   against the full graph's edge inventory and retain readable region crops;
   offscreen or unrendered edges remain unverified. A coordinate inventory, downward
   dependency test or distant overview cannot establish wire clearance.
3. When native geometry is exposed, check the actual rendered paths against
   nonendpoint card bounds and other paths. Do not substitute straight lines
   between node coordinates. If geometry or complete coverage is unavailable,
   report the automated check as unavailable with an unknown count; separately
   report visual inspection as pass, fail, partial or unknown with its scope.
   Claim an automated zero only from a completed check of actual geometry for
   all expected edges and cards. A visible crossing or path behind another card
   fails visual QA even if coordinate checks pass.
4. Match branch placement to immutable native port order. Uncrossed routing
   takes priority over fail-left/continue-right and alphabetical sibling defaults.
   Move nodes or use supported routing controls; never swap branch semantics,
   reconnect edges, rename targets or change bindings just to improve geometry.
   Recheck affected paths after saving and reloading, and document the exception.
5. Hand off the inspected draft link explicitly with `version=edit`; verify it
   opens that draft, not the default/published view. Report saved coordinates,
   rendered-wire coverage, semantic identity and run evidence separately. Do not
   describe unavailable wire checks as passed or a draft as published.

## View Modes

Choose the mode **before** laying anything out, and say which one you chose.

Numbered workflows use **compact parallel lanes** in either mode, following
[workflow-node-design.md](../../shared/coding/workflow-node-design.md). Inspect
the original layout and dependency edges before reflowing it. Dependent paths
progress top to bottom; independent numbered branches start at a shared vertical
level. A higher number alone does not require a lower row. This takes precedence
over the horizontal column/lane examples below; adapt ports and corridors while
preserving real topology. Prefer local placement fixes; never add edges to make
numbering sequential. An explicit user layout overrides this default. Verify
new nodes' saved lane positions, path order, and aligned branch starts.

Numbers identify business stages; executable substeps within one stage use
letters. For example, `4a → 4b → 4c` can run beside `5a → 5b`, `6`, and
`7a → 7b`. Inspect incoming edges and input bindings before grouping a gate:
if it joins `5b`, `6` and `7b`, it starts stage `8`, even when its predicate
checks only calls. Only validation internal to one stage stays lettered.
After a split or merge, recheck the whole stage sequence and downstream labels
against the current approved map, following
[clay-workflow-node-naming.md](../../shared/coding/clay-workflow-node-naming.md).
Keep stable registry IDs and historical artifacts; update current labels through
an explicit old/new mapping. Drawing a rename does not update a live workflow
or its name-dependent consumers.

### Stage title headers

Follow the canonical [long-stage header rule](../../shared/coding/clay-workflow-node-naming.md#title-headers-for-long-stages).
For three or more sequential substeps in one stage, draw a title-only header
such as `5. Email gatherer` above `5a → 5b → 5c`. Keep the individual substeps
visible. Derive the chain from actual dependencies; three sibling outcomes do
not count as a chain. A numbered gate already supplies its stage heading.

Represent the title as a group/frame heading or annotation, never as a fake
executable node or a new edge. Keep presentation inventory separate from the
execution graph and node/run QC counts. For native Clay, verify supported named
groups and their membership restrictions first; if unavailable, show the header
in the authored review diagram and report native status as unsupported/unknown.
Do not change behavior to make grouping work. Verify the header is above its
members, uniquely identifies the stage, and leaves all substeps readable.

### `annotated-poster`

Dense, explanatory, one big sheet. Every node carries a step label, a title, an
optional subtitle and a list of tagged system calls. Swimlanes, gates, loops
and a footer legend. Nodes are ~214px wide and heights vary with content.

Choose it to explain **process logic to a decision-maker**: who owns what,
where the approvals are, what happens on a no, what repeats. A no / reject /
disqualified / no-match outcome is still a node on the sheet. Do not leave
that path as an unlabeled dead end. Follow
`shared/shipping/visible-terminal-branches.md`.

Reference implementation: [assets/workflow-poster-template.html](assets/workflow-poster-template.html).

### `compact-dag`

Many small uniform cards on a regular pitch, thin light curved connectors,
generous whitespace, small type, no edge labels, no legend. Unnumbered graphs
default to left-to-right flow; numbered paths run downward in parallel lanes.
Per-step detail is deliberately absent.

Choose it to show **a many-step pipeline's shape and scale** — how long the
chain is, where it forks and rejoins, how much machinery there is — when the
content of each step does not matter.

Style reference: [references/compact-dag-reference.png](references/compact-dag-reference.png).

Grammar to match:

- Canvas: flat light cool grey (`#eef0f3`), no frame, large empty margins.
- Card: white fill, 1px `#dfe3e8` border, `rx 3`, **uniform width** (~150-190px)
  across the whole graph; height varies only with row count.
- Header row: small colored glyph (~11px) at the left, then the step name at
  ~11px semibold near-black. A hairline divider under the header.
- Body rows: ~10px muted grey (`#8a929c`) — a scale line such as
  `24 columns`, then one row per named input (`Left dataset`, `Right dataset`).
- Ports: a filled grey dot on the **left edge of the specific row** it feeds;
  a hollow white dot with a grey ring on the right edge at the output row.
- Connectors: 1px `#c7ccd3` bezier with horizontal tangents at both ends when
  the direct corridor is empty; otherwise use registry-declared waypoints and
  wide rounded elbows that clear every nonendpoint card. Never labeled.
- Grouped steps may stack two title rows inside one card; a status row (green
  tint) may sit below the card body.
- Rows do not have to align across columns; columns do sit on a regular pitch.

Do not mix modes in one artifact. If the user wants both, produce two files.

## Workflow

1. Confirm the mode from the section above and state it back in one line.
2. Write the registry before any markup. Nodes, forward flow, branch drops and
   loops are **data arrays**; a small script renders them. Never hand-draw
   diagram markup — hand-drawn markup cannot survive a node insertion.
3. Copy [assets/workflow-poster-template.html](assets/workflow-poster-template.html)
   for `annotated-poster` and edit only the registry block at the bottom.
4. Apply the locked rules below.
5. Serve the file over a local HTTP server and export the PDF plus crops.
6. Read the crops back and fix what you see. Repeat until clean.
7. Report the mode, file paths, page size, and any open naming choices.

## Locked Rules

### Registry-driven rendering with measured heights

Declare `NODES`, `LANES`, `FLOW`, `VFLOW`, `LOOPS`; render with a loop. After
inserting each node element, read `el.offsetHeight` and store it in the box
map **before computing any wire**. Wire endpoints are derived from real
rendered height; a guessed height detaches every arrow attached to that node.
Polygon shapes (review/approval) are the one exception — they carry explicit
`w`/`h` because they are SVG, not flowed content.

### Z-order is not optional

`background zones/lanes: 0` → `SVG wires: 1` → `nodes: 2` → `floating labels: 3`.

Get this wrong and nodes disappear behind lane tints. This has already cost one
debugging cycle; set the four z-indexes explicitly, do not rely on DOM order.

### Port geometry and endpoint language

Choose one endpoint language per view mode and keep it mechanically consistent:

- `compact-dag`: visible edge ports, no connector arrowheads. A hollow port is
  the source; a filled port is the destination.
- `annotated-poster`: arrowheaded wires are allowed when the nodes do not also
  render visible endpoint ports.
- Never place an arrowhead and a visible port at the same coordinate. They
  overlap after export and create an irregular dark blob.

For visible ports:

- A horizontal input-port center must sit within 2px of the node's left border
  and be vertically centered on the declared target row.
- A horizontal output-port center must sit within 2px of the right border and
  be anchored to an explicit output row or the body region, not `top: 50%` of
  the entire card.
- If a port is positioned inside a padded body or row, its offset must account
  for that padding. A raw edge offset such as `left: -5px` is wrong when the
  containing row begins 15px inside the card.
- Keep at least 8px of visible clearance between a port and body copy. A port
  that reads like a bullet inside the text has failed, even if the wire reaches
  it mathematically.
- Header glyphs stay inside headers and use a non-circular shape; connector
  ports stay circular and live only on card edges.
- Render ports only for real edges. No decorative or orphan ports.

Observed failure (OpsMill workflow, 2026-08-07): single-input ports were
positioned relative to a padded body row but used an offset intended for a
node-level anchor, moving them roughly 14px inside the card. Output ports were
centered on the whole card, and SVG arrowheads terminated on top of the visible
ports. The full-poster view looked acceptable, but a 1:1 crop exposed stray
body bullets, seam-level output rings, and endpoint blobs. The fix was to use
padding-aware left-edge inputs, body-anchored outputs, and port-only connectors.

### Obstacle-free routing and merge-port order

A connector may touch only its source and destination nodes. It must never run
through, behind, or visually scrape another card—even when the node layer hides
the offending segment in the final render.

- Use a direct Bézier only after confirming the full curve lies in an empty
  corridor. When a direct curve would enter another node's box, add explicit
  `via` points to the edge registry and render a rounded orthogonal route.
- Keep routing data in the edge registry. Do not hand-draw one-off SVG paths in
  markup; node moves must be fixable by changing coordinates or waypoints.
- Reserve at least 8px of clearance around every nonendpoint node, measured
  from the card border, not from its text or fill. Increase the margin when
  shadows or thick borders make an 8px gap read as contact.
- Route long lower branches through a dedicated corridor below the relevant
  row of cards, then approach the destination port horizontally. Do not send a
  diagonal through the middle of a neighboring workflow.
- Treat merge-port order as part of layout, not as a fixed semantic list. Map
  the closest/direct branch to the nearest clean input row, place longer routed
  branches on separate rows, and order the final approaches so they are
  monotone and do not cross. If business priority requires another order,
  reflow or widen the layout instead of accepting crossings.
- Avoid wire-to-wire crossings as well as wire-to-node crossings. Shared trunks
  from one source may branch deliberately; unrelated edges should receive
  separate horizontal or vertical corridors.
- A node with three or more outgoing branches must use one explicit fan-out
  grammar:
  - ordered output ports: one port per branch, vertically ordered to match the
    downstream nodes or their final routing corridors; or
  - one trunk rendered once to an explicit junction, followed by separate
    branches.
- Never draw several independent paths from one undifferentiated port when
  they overlap, cross, or peel away at slightly different angles. Coincident
  strokes are not a shared trunk; they produce uneven weight and an ambiguous
  knot after export.
- Treat fan-out port order like merge-port order. Source ports and destination
  approaches should be monotone whenever possible. If the source and
  destination orders are inverted, reorder the rows or reflow the nodes before
  adding detours.
- Reflow nodes before adding increasingly elaborate detours. A wider canvas is
  preferable to a clever route that a fresh reader cannot trace.

For authored diagrams, run a rendered collision audit after drawing wires:
sample every SVG path with `getPointAtLength()` and compare the samples against
every nonendpoint node's bounding box expanded by the clearance margin. Publish the result on the page
(for example `data-wire-collisions="0"`) so headless QA can assert it. The
required result is zero; visual inspection does not override a nonzero audit.

Also run a rendered wire-crossing audit. Sample each path into short segments,
test every path pair for segment intersections, and ignore only a small radius
around a genuinely shared endpoint or explicit junction. Publish the count on
the page (for example `data-wire-crossings="0"`). This check includes edges
that share a source node: a common source is not permission to tangle after the
port.

Both audits ship implemented in
[assets/workflow-poster-template.html](assets/workflow-poster-template.html);
do not rewrite them per project. They audit only paths carrying `data-from`
and `data-to`, so every wire must be drawn through the template's `path()`
helper with its endpoints passed in — an untagged path is silently exempt from
both checks. Assert the published counts headlessly rather than eyeballing the
render:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --virtual-time-budget=4000 \
  --dump-dom http://localhost:8731/graph.html \
  | rg -o 'data-wire-[a-z-]*="[^"]*"'
```

A zero on a graph whose wires were never tagged is a false pass. When changing
the audit itself, inject a deliberately illegal wire and confirm the count goes
nonzero before trusting a zero.

Observed failure (OpsMill workflow, 2026-08-07): a direct company-to-new-hire
curve passed behind the repository card, so the node layer concealed the
collision. Separately, four signals approached one merge in an order that made
GitHub activity and top-contributor lines cross or double back. The fix widened
the discovery lane, moved the merge right, ordered its inputs by clean final
approach, routed the bottom signal through a lower corridor, and added a
rendered collision audit.

Observed failure (OpsMill workflow, 2026-08-07): four branches left one company
output port as separate curves. They crossed and overlapped immediately beside
the card even though none intersected a node. The fix replaced the single port
with four ordered output ports, reordered the upper discovery rows so source
and destination order matched, and added a pairwise rendered wire-crossing
audit.

### Swimlanes, and the shared-lane rule

Use dotted horizontal lanes when the flow has genuinely parallel origination
paths or ownership tracks — not as decoration.

- **Work common to every lane gets its own dedicated shared lane.** Parking
  shared work inside one of the real lanes makes it read as belonging to that
  lane, which is a factual misstatement of the process.
- Lanes make fork-and-rejoin legible as **vertical movement**: a path leaving
  the shared lane, doing something, and coming back is the visual proof of what
  is unique to that lane.
- Reserve a left gutter (~160px) for lane labels so they never collide with the
  first node column. Shift every node x by the gutter in code, not by hand.
- Size lane bands from the measured extents of their members, plus padding.

### Loop rendering

- Forward flow: solid, darker, `stroke-width 1.5`. Anything that loops back:
  dashed (`5 4`), lighter, `stroke-width 1`. A reader must be able to tell
  repetition from progression at a glance without reading a label.
- **Cycle between two adjacent nodes → tight two-arrow cycle**: the solid
  forward wire plus a dashed return arc tucked immediately beneath both nodes,
  so the pair reads as one closed loop. A long dashed detour to the bottom of
  the sheet does not read as a cycle at all.
- Genuinely long returns route along the bottom edge of a lane, not through it.
- **Every wire label gets a white background rect sized from its own
  `getBBox()`** so it masks the stroke it sits on. Insert the rect before the
  text node, then size it from the measured text box.

### Shape and border semantics

Use consistently, and declare each one in the footer legend:

| Encoding | Meaning |
|---|---|
| Triangle | human review |
| Diamond | approval gate |
| Dark filled node | terminal state |
| Dashed border | shared service |
| Left accent stripe | self-firing trigger |
| 2px border | convergence / merge point |
| Dotted border, tinted | off-path branch |

### Tag honesty

Every node tag must name something a reader can decode without asking.

- **Opaque abbreviations are banned.** A real reviewer asked "idk what svc
  means" — that is the failure mode this rule exists to prevent.
- Distinguish the kinds of call: a **named vendor system** we call (`api`,
  with the specific system and object: `crm — stage`), something **we build
  and own** (`ours`), a **model or skill** invocation (`llm`), and a
  **clock-driven** trigger (`cron`).
- Where the vendor genuinely is not decided, tag the **capability/port**
  (`port`, e.g. `market data — screen`) rather than silently picking a product,
  and surface the open choice to the user in your report.
- The footer legend must match the tag vocabulary actually present. A legend
  entry for a tag you removed is a defect; a tag with no legend entry is a
  defect.

## Export and Verification

```bash
# 1. Preview server — Playwright and headless Chrome block file:// for this,
#    so a server is mandatory, not a convenience.
python3 -m http.server 8731 --directory <dir>

# 2. Single-page vector PDF. The template injects @page from the measured
#    poster box (poster_px / 96 inches), so the whole graph lands on ONE page
#    with selectable vector text and infinite zoom.
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=4000 \
  --print-to-pdf=out/graph.pdf \
  http://localhost:8731/graph.html

# 3. Verify the PDF rather than assuming it worked.
python3 - <<'PY'
import re; d=open('out/graph.pdf','rb').read()
print('pages:', len(re.findall(rb'/Type\s*/Page[^s]', d)))
print('mediabox:', set(re.findall(rb'/MediaBox\s*\[[^\]]*\]', d)))
PY
```

**The legibility rule — the one people skip.** Any poster wider than roughly
2000px is illegible once it is shrunk into a chat message. Always also export
zoomed region crops (a Playwright `clip`, or a headless screenshot sliced into
overlapping halves) and **read the images back** before declaring the work
done. Visual verification means actually looking. It catches right-edge
clipping and node/wire/label collisions that no amount of code review does.

**Iteration reality.** Poster width and page size get recomputed every time a
node is added, because adding one node shifts every downstream column. Derive
the poster width from the measured content extents and inject `@page` from it —
never hard-code inches. Expect to widen and re-verify rather than treating
layout as done.

## Checks

For native Clay, complete the native verification section above and report its
coverage and unavailable checks. For authored diagrams, run
[references/verification-checklist.md](references/verification-checklist.md)
before reporting. Minimum bar for authored diagrams:

- [ ] Mode named, and only one mode used in the file
- [ ] Numbered dependent paths run downward, independent branch starts share a
      level, and new nodes fit their lane; explicit user layout takes precedence
- [ ] Stage boundaries follow inspected incoming dependencies, not titles alone;
      substeps and downstream labels match the current map, with IDs/history preserved
- [ ] Diagram rendered from registry arrays, no hand-drawn nodes or wires
- [ ] Every node height read from `offsetHeight` before wires computed
- [ ] Z-order set explicitly: lanes 0, wires 1, nodes 2, labels 3
- [ ] Endpoint language is mode-consistent: compact ports without arrowheads,
      or annotated-poster arrowheads without visible endpoint ports
- [ ] Input and output port centers sit within 2px of the correct card edge and
      align to their declared row/body anchor
- [ ] No port overlaps body text or reads as a bullet; no orphan port is shown
- [ ] Every wire is drawn through `path()` with its endpoints passed, so it
      carries `data-from`/`data-to` and is actually covered by the audits
- [ ] No connector enters the expanded bounding box of a nonendpoint node;
      the rendered collision audit reports zero
- [ ] The rendered wire-crossing audit reports zero outside true shared
      endpoints or explicit junctions
- [ ] Direct Béziers are used only in empty corridors; obstructed paths use
      registry-declared rounded orthogonal waypoints
- [ ] Fan-outs with three or more branches use ordered per-branch ports or one
      trunk rendered once to an explicit junction
- [ ] Fan-out source order and downstream approach order are monotone; no knot
      forms immediately beside a source card
- [ ] Merge input rows are ordered with the final approach geometry so lines do
      not cross or double back
- [ ] Unrelated wires do not cross; long branches use dedicated corridors
- [ ] Shared work sits in its own shared lane, not inside an origination lane
- [ ] Left gutter reserved; no lane label touches the first node column
- [ ] Loops dashed and lighter; adjacent cycles drawn as a tight return arc
- [ ] Every wire label has a `getBBox`-sized white mask rect
- [ ] Legend matches the shapes, borders and tags actually present — both ways
- [ ] No opaque tag abbreviations; vendor vs ours vs model vs clock distinguished
- [ ] Undecided vendors tagged as capability/port and surfaced to the user
- [ ] PDF verified as **1 page** with the expected MediaBox
- [ ] Zoomed crops exported **and read back**; right edge not clipped
- [ ] A 1:1 crop of the busiest fan-in and fan-out was inspected port by port
- [ ] Every named branch outcome, including no / reject / disqualified /
      no-match, is a visible terminal node, not an omitted path

## Output Contract

For native Clay, report the verified draft link, saved identity, inspected edge
coverage, per-check status and evidence paths. For authored diagrams, report:

- view mode and why that mode over the other;
- the HTML path, the PDF path, and the crop paths;
- poster pixel size and the resulting page size in inches;
- PDF page count and MediaBox as verified, not assumed;
- what the zoomed crops showed and what was fixed;
- any node whose vendor is tagged as an undecided capability/port, stated as an
  open choice for the user.

## Resources

- [assets/workflow-poster-template.html](assets/workflow-poster-template.html) —
  runnable `annotated-poster` template: registry, measured heights, z-order,
  lanes, shapes, loops, masked labels, auto page sizing, and the rendered
  wire/node collision and wire/wire crossing audits.
- [references/compact-dag-reference.png](references/compact-dag-reference.png) —
  style reference for `compact-dag` mode.
- [references/verification-checklist.md](references/verification-checklist.md) —
  the export and read-back loop as runnable steps.
