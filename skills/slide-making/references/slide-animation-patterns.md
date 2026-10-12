# Slide animation patterns (HTML decks)

Source study: the Clay slides remake at [https://clayslides.lovable.app/](https://clayslides.lovable.app/)
(inspected 2026-07-31, live CSS extracted via browser). Captured for
customer-demo deck sets where slight animations are appropriate. The
animations there are small, they work, and each one demos something.

For the judgment layer — why these animations work and how to critique
motion on any surface — use the `animation-coach` skill; its worked example
on this same deck lives at
`skills/animation-coach/references/case-clayslides.md`.

## Core principles

1. **Animations demo, they don't decorate.** The best slide in the reference
   deck (Waterfall Enrichment) is a simulated product run: the animation IS
   the argument. If an animation doesn't act out the concept or guide reading
   order, cut it.
2. **Top-down population in reading order.** Elements enter in the order the
   audience should read them: headline first, then section labels, then
   content groups left-to-right, punchline last. Never animate footer/chrome.
3. **Animate entrance, then stop.** One-shot animations with
   `animation-fill-mode: forwards`. Elements start at `opacity: 0` and hold
   their final state. No looping content animations.
4. **The final frame is the slide.** After all animations settle, the slide
   must pass every static rule in SKILL.md (hierarchy, alignment, squint
   test). Exports to PPTX/PDF drop animation, so the settled state is
   canonical.

## Timing ladder (measured from the reference)

Slide 1 ("Most teams start here...") measured delays, all `fade-in-up`:

| Element                    | Delay        |
| -------------------------- | ------------ |
| Headline (h2)              | 0ms          |
| Group label 1 ("Data")     | 200ms        |
| Group label 2 ("CRM")      | 350ms        |
| Logos in group 1           | 400ms, 500ms |
| Logos in group 2           | 550ms, 650ms |
| Punchline ("That worked.") | 900ms        |

Rules derived:

- **Within a group:** 100–150ms steps between sibling items.
- **Between groups:** 150–200ms offset; left group populates before right.
- **Before the punchline/takeaway:** a longer beat (~250ms of dead air) so
  the payoff lands separately.
- **Total population:** everything on screen within ~1.2s. Don't make the
  presenter wait.

## Animation vocabulary (exact specs from reference CSS)

One entrance verb dominates; everything else is a special-purpose accent.

### Default entrance

- `fade-in-up` — 0.6s ease-out; opacity 0→1, translateY(30px)→0. Use for
  ~90% of entrances.
- `stagger-in` — 0.5s ease-out; translateY(20px)→0. Lighter variant for
  list items.
- `fade-in-scale` — 0.5s ease-out; scale(0.9)→1. For cards/panels.
- `slide-in-left` / `slide-in-right` — 0.6s ease-out; translateX(∓40px)→0.
  Reserved for comparison columns (before/after entering from opposite
  sides).

### Demo-state accents (simulated product runs)

- `success-pop` — 0.4s; scale 0→1.2→1. Checkmarks landing.
- `waterfall-fill` — 0.4s; opacity 0 + scale 0.8→1.05→1. Cells filling in.
- `step-activate` — 0.5s spring; opacity 0.4→1, scale 0.95→1.03→1 with a
  brief glow. A pipeline step becoming active.
- `badge-pop` — 0.4s spring; translateY(8px) + scale 0.5→1.15→1. Small
  badges/pills appearing.
- `counter-reveal` — 0.6s spring; scale 0.8→1.1→1. Stat numbers landing.
- `card-expand` — 0.4s ease-out; scale 0.95→1.
- `credit-popup` — 0.667s; rise-and-fade tooltip (like "-1 credit" floating
  off a cell).
- `waterfall-flow` / `tier-grow` — 0.6–0.8s; width 0→100% (or to a CSS var)
  for progress bars and tier columns.
- `draw-line` — 1.5s ease-out; SVG stroke-dashoffset 1000→0 for connectors.
- `connector-draw` — 1s; `clip-path: inset(0 100% 0 0)`→`inset(0)` to draw
  non-SVG connector lines left-to-right.

### Easing

- Default: `ease-out`.
- Spring overshoot `cubic-bezier(0.34, 1.56, 0.64, 1)` is reserved for
  success/activation moments (pops, badges, counters) — at most one spring
  moment per slide.

### Ambient (use very sparingly)

- `float` — 6s loop, ±10px drift. Decorative background shapes only.
- `pulse-subtle` — 2s loop, opacity 1→0.9. "This thing is alive" hint.
- `pulse-glow` — 2s loop, expanding shadow ring. Live/active indicator.

Never apply ambient loops to text or content the audience must read.

## The live-demo slide pattern

The Waterfall Enrichment slide is the template for demoing a sequential
process inside a slide:

1. A product-like table renders instantly (header + rows, empty cells).
2. Rows process **one at a time, top-down**. Only one row is "active".
3. Within the active row, cells advance **left-to-right**: a miss renders
   a dim "—", the active cell shows a spinner, a hit gets a green check
   (`success-pop`), then the result column fills with the found value and
   the row tints green.
4. Below the demo, static explainer cards name the concept the animation
   just acted out ("Sequential search", "Pay for results").

This works because the motion encodes the mechanism (sequence, fallback,
stop-on-success) — a static table could not show that.

## Implementation notes

- Tailwind-style utility classes: named keyframes + `.animate-*` classes,
  fixed `.delay-100` … `.delay-2000` utilities, inline `animation-delay`
  for computed staggers.
- Always pair delayed entrances with `animation-fill-mode: forwards` (or
  Tailwind `fill-mode-forwards`) and initial `opacity: 0`, otherwise
  elements flash before their turn.
- Stateful demos (spinner → check → fill) are driven by a JS timer stepping
  React state, not CSS alone; CSS handles each state's entrance.
- Movement distances stay small: 20–40px translates, 0.8–0.95 scales.
  Nothing flies across the slide.
- Durations 0.4–0.6s for entrances; only line-draws go up to 1.5s.

## QA additions for animated decks

- [ ] Population order matches reading order (title → labels → groups
      left-to-right → punchline)
- [ ] Punchline enters last, after a distinct pause
- [ ] All entrances one-shot with `forwards`; no looping content animation
- [ ] At most one spring/overshoot moment per slide
- [ ] Full population within ~1.2s (excluding intentional live-demo runs)
- [ ] Settled final frame passes the static QA checklist in SKILL.md
- [ ] Demo animations encode a real mechanism, not decoration
