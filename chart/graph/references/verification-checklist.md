# Workflow Node Graph — Verification Checklist

Run this every time, including after a "small" node addition. Adding one node
shifts every downstream column, so layout is never done until this passes.

## 1. Serve

`file://` is blocked for Playwright automation and unreliable for headless
print. Always serve.

```bash
python3 -m http.server 8731 --directory "$(dirname "$HTML")" &
curl -s -o /dev/null -w '%{http_code}\n' "http://localhost:8731/$(basename "$HTML")"   # expect 200
```

## 2. Console must be clean

Load the page and read the console. A silent JS error means the registry never
rendered and you are about to export a blank sheet. `favicon.ico` 404 is the
only acceptable entry.

The template ships both routing audits, so assert them before export:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --virtual-time-budget=4000 --dump-dom \
  "http://localhost:8731/$(basename "$HTML")" \
  | rg -o 'data-wire-[a-z-]*="[^"]*"'
```

Expect `data-wire-collisions="0"` and `data-wire-crossings="0"`. When a count
is nonzero, `data-wire-crossing-edges` and the console warnings name the
offending edge pairs and nodes. A nonzero audit is a hard failure — reflow the
layout or add registry waypoints; do not overrule it by looking at the render,
because the node layer paints over the very collisions you are looking for.

Two ways this check silently passes when it should not:

- **Untagged wires.** The audits only cover paths carrying `data-from` and
  `data-to`. Any wire drawn outside the template's `path()` helper, or drawn
  without passing its endpoints, is exempt. Confirm the audited path count
  matches the number of edges in the registry.
- **An audit that cannot fail.** If you modify the audit code, inject a
  deliberately illegal wire first and confirm the count goes nonzero. A zero
  from a broken audit looks identical to a zero from a clean graph.

## 3. Confirm the measured size

The template publishes what it measured:

```js
window.__poster   // {widthPx, heightPx, pageIn:[w,h]}
```

`pageIn` must be `px / 96` (plus a small safety margin). If `widthPx` equals
the browser viewport width, the poster is sizing to the window instead of the
content — fix that before exporting or the page size is meaningless.

## 4. Export the single-page vector PDF

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=4000 \
  --print-to-pdf=out/graph.pdf \
  "http://localhost:8731/$(basename "$HTML")"
```

## 5. Verify the PDF — do not assume

```bash
python3 - <<'PY'
import re
d = open('out/graph.pdf','rb').read()
print('pages:', len(re.findall(rb'/Type\s*/Page[^s]', d)))
print('mediabox:', set(re.findall(rb'/MediaBox\s*\[[^\]]*\]', d)))
PY
```

- `pages` must be `1`.
- MediaBox is in points: `inches * 72`. Cross-check against `window.__poster`.
- More than one page means the `@page` size is stale — it is being hard-coded
  somewhere instead of derived from the measured box.

## 6. Export zoomed crops and READ THEM BACK

A 2500px-wide poster is unreadable when shrunk into a chat message. Full-poster
screenshots prove nothing about legibility.

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --virtual-time-budget=4000 \
  --window-size=<W+60>,<H+60> --screenshot=out/full.png \
  "http://localhost:8731/$(basename "$HTML")"

python3 - <<'PY'
from PIL import Image
im = Image.open('out/full.png')
# overlapping halves at 1:1 so text stays readable
im.crop((0, 0, im.width//2 + 120, im.height)).save('out/left.png')
im.crop((im.width//2 - 120, 0, im.width, im.height)).save('out/right.png')
PY
```

Then actually open `out/left.png` and `out/right.png` with the image reader.
Looking is the check. Code review does not substitute.

## 7. What the crops must show

- [ ] Right edge not clipped; the last node and its wire are fully inside
- [ ] No node sitting behind a lane tint (z-order regression)
- [ ] No arrow ending in empty space or short of its node (height regression)
- [ ] No connector runs through or behind a nonendpoint card; rendered
      `data-wire-collisions` is `0` when the page exposes the audit
- [ ] No wires cross or overlap outside a true shared endpoint or explicit
      junction; rendered `data-wire-crossings` is `0`
- [ ] Obstructed connectors use rounded waypoint routes through open corridors,
      not diagonals hidden behind the node layer
- [ ] Merge inputs are ordered so the final approaches do not cross or double
      back; longer branches have their own corridor
- [ ] Unrelated wires do not cross; any shared trunk is an intentional branch
      from the same source
- [ ] Fan-outs with three or more branches use ordered per-branch ports or one
      trunk rendered once to an explicit junction
- [ ] Fan-out port order matches downstream approach order; no curves tangle
      immediately beside the source card
- [ ] One endpoint language is used consistently: compact visible ports with
      plain wires, or annotated-poster arrowheads without visible ports
- [ ] Every horizontal input-port center is within 2px of the left card edge
      and vertically centered on its declared target row
- [ ] Every horizontal output-port center is within 2px of the right card edge
      and anchored to an output row/body region, not the whole-card midpoint
- [ ] No arrowhead overlaps a visible port; no port overlaps body text; ports
      retain at least 8px of visual clearance from copy
- [ ] Source ports are hollow, destination ports are filled, and every visible
      port corresponds to a real edge
- [ ] Header glyphs remain inside headers and cannot be mistaken for circular
      connector ports
- [ ] No wire label sitting unmasked on top of a stroke
- [ ] No lane label touching the first node column
- [ ] Adjacent-node cycles read as a closed loop, not a long detour
- [ ] Dashed vs solid distinguishable at a glance
- [ ] Every tag in the graph appears in the legend, and vice versa
- [ ] No opaque abbreviation a fresh reader would have to ask about
- [ ] Every named branch outcome, including no / reject / disqualified /
      no-match, is a visible terminal node, not an omitted path

Also inspect a 1:1 crop of the busiest fan-in and fan-out port by port. A
full-poster screenshot is not sufficient proof of endpoint geometry.

## 8. Tear down

```bash
kill %1   # or the recorded server pid
```
