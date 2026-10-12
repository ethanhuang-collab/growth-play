---
name: slide-making
description: Design, build, and materially edit professional slide decks (PowerPoint, Google Slides, Keynote, HTML). Covers layout consistency, typography hierarchy, alignment, box sizing, table formatting, visual rhythm, white space, information hierarchy, color usage, diagrams, and content density. Use when creating a deck, building slides from content, or applying layout fixes to a deck file. For critique-only review, screenshot feedback, or final polish recommendations without deck-file edits, use slide-analyst.
status: active
---

# Slide Making

General design principles for professional slide decks.

For the storytelling layer (audience/so-what discipline, narrative structure,
slideument rule, iterative-process reference), see
[references/slide-design-principles.md](references/slide-design-principles.md).
For HTML-deck entrance animations and live-demo slide patterns (top-down
population order, stagger timing ladder, animation vocabulary — studied from
the Clay slides remake at clayslides.lovable.app), see
[references/slide-animation-patterns.md](references/slide-animation-patterns.md).
Curated good example slides and decks live in
`~/Code/coding-system/gallery/slides/` and `gallery/decks/` (distinct from the
graphs store).

## Information Hierarchy

### One Idea Per Slide

- Every slide communicates a single clear point. If a slide has two ideas, split it into two slides.
- **Conclusion-first headlines** — the title states the takeaway, not the topic. "Revenue doubled in Q3" not "Q3 revenue overview."
- Body text supports the headline; it never introduces a second argument.

### The Squint Test

- From six feet away (or zoomed to 30%), a viewer should be able to tell what the slide is about from the title and visual weight alone.
- If you squint and everything blurs into an even block of gray, the slide lacks hierarchy.

### Reading Order

- Audience reads: (1) headline, (2) largest visual or number, (3) body text, (4) footer/source.
- Design to that order. The most important element should be the biggest and highest on the slide.

## Layout & Alignment

### Title Consistency

- **All content slide titles must start at the same X, Y position and use the same font size.** Extract the title position and size from the first content slide and replicate it exactly on every subsequent content slide.
- Slide-wide titles span full page width: `TITLE_WIDTH = slide_width - 2 * margin`.
- Section break slides may use a different (larger) title size, but all section breaks must match each other.
- Title slides and closing slides follow their own rules but must be internally consistent if there are multiples.

### Left and Right Block Alignment

- **Establish a single left content margin** for all slides. Eyebrows, headings, body text, labels, slabs, and tables share the same left edge. No element drifts.
- **Left blocks:** All content in the left column aligns to the same left margin.
- **Right blocks:** All content in the right column aligns to the same right edge. Right blocks do not float; they sit at a fixed distance from the slide edge.
- **Right content margin** mirrors the left. Tables and content blocks extend to this edge, not stop short.
- Snap to grid — use exact coordinates, never approximate positions.

### Box Sizing Consistency

- **Peer slides use identical dimensions** for equivalent elements. If one slide has a quote box 5" x 2.8", every peer slide uses 5" x 2.8".
- **Never shrink a box because it has less content.** Size all boxes to the maximum needed across the peer set.
- **Peer elements** — badge, icon, title, labels, body text, quote slab, goal divider, footer — same position and size on every peer slide.
- Structure content as detectable groupings; render with a shared helper for consistency.

### Vertical Rhythm

- Consistent vertical spacing between sections (eyebrow → heading → body → footer) across all slides of the same type.
- Divider lines, goal sections, and footers sit at the same Y position on every peer slide.
- If one slide puts a label at Y=1508, all peer slides put it at Y=1508.

### Layout Zones

- **Respect source layout zones.** Header bands, content areas, footer strips have boundaries. Extract them from existing slides.
- **Never place body content inside a header band.** The title belongs in the header zone; everything else starts below it.
- Extract zone boundaries from the source slide, not assumptions.
- Two-pass verification: (1) Scan shapes to find zone boundaries, (2) Set new positions using those boundaries — never hardcode arbitrary Y values.

## White Space & Content Density

- **White space is intentional, not leftover.** It directs the eye and separates ideas. Do not fill every inch.
- **But don't waste it either.** A slide with 40% empty space and 12pt text should jump to 18pt or 24pt instead.
- **3-second rule:** A viewer should grasp the main point within 3 seconds of seeing the slide.
- **Max 2-4 lines** of body copy per text block. If content doesn't fit at readable sizes, split across two slides rather than shrinking fonts.
- Avoid bullet walls (6+ bullets). If you have more than 5 bullets, restructure: group into categories, use a table, or split slides.

## Typography

### Size Tiers

Use these four tiers for all text. Pick the largest tier that fits the available space.

| Tier | Size (pt) | Use for |
|------|-----------|---------|
| 24 | 24 | Headings, stat numbers, pull-quotes — as large as possible |
| 18 | 18 | Body text, bullet content, descriptions |
| 14 | 14 | Secondary body, table content, captions |
| 12 | 12 | Labels, eyebrows, badges |
| 10 | 10 | Footnotes, sources, footer text, small metadata |

### Title Word Length

- **Target ~20 words or fewer** for slide titles. Peer slide titles should be roughly the same word count so they occupy a similar visual footprint.
- If one title is 8 words and another is 25, rewrite for parity. Consistent title length creates rhythm across the deck.

### Rules

- **Font preservation:** When editing an existing deck, preserve the font already in use. Never substitute fonts arbitrarily.
- **Single font family** for titles, labels, and body. Bold and size create hierarchy; avoid mixing families unless design explicitly requires it.
- **As large as possible:** Always use the largest size tier that fits. A slide with empty space and 12pt text should be 18pt or 24pt instead.
- **Peer slides, identical font sizes** — never shrink one slide to fit more text while siblings stay large.
- **Sentence case** for all text. No periods in headings or titles.
- **All-caps is banned** (ruled 2026-07-23) — no uppercase labels, headers,
  eyebrows, or axis text anywhere. Caps-lock text reads as jarring.
- Avoid widows and orphans in headlines.
- **Emphasis calibration (ruled 2026-07-23):** let hierarchy do the work; bold
  is the MAIN form of emphasis, deployed only when needed — not frequently.
  Color-bold is the escalation above bold. Italics are a different register
  (quote attribution, asides, de-emphasis), used less than bold and never as a
  parallel emphasis tool. Underlines, outlines, and mid-block size changes are
  rare. When the brand accent lacks pop against the background, the strong
  emphasis color is the highest-contrast neutral (generally black on white) —
  reserved for special slides and strong emphasis.

### Text Containment

- Text must never bleed, overflow, or spill past container edges. Increase container height/width or reduce line density until text fits.
- Footer, summary, and bottom content must sit above the slide bottom within assigned zones.
- When placing bullets in slabs, ensure text box height accounts for all lines with adequate padding.

### Slide Boundary Enforcement

- **Every shape must fit within the slide canvas.** No shape's bottom edge (`top + height`) may exceed `slide_height`, and no shape's right edge (`left + width`) may exceed `slide_width`.
- After placing all shapes on a slide, run a boundary sweep: iterate every shape and assert `top + height <= slide_height` and `left + width <= slide_width`. Flag any violation before saving.
- When stacking N content boxes vertically, compute the available vertical space first (`content_bottom - content_top`), divide by N plus gaps, and size each box to fit — never place boxes at hardcoded Y values without checking they land inside the slide.
- If a box would bleed past the bottom, compress box heights, reduce internal padding, or split content across two slides — never allow silent overflow.

## Color Usage

- **White (or off-white) background is the default** for slides and charts
  (ruled 2026-07-23). Dark, full-bleed, or heavy on-brand backgrounds are a
  deliberate exception reserved for **killer/showcase slides** — rare
  moments of maximum emphasis (see `gallery/slides/swd-9.3-*` and the 5.7
  showstopper graph). Ask before going dark; never make it the deck default.
- **Limit to 3-4 colors** per deck (one primary, one accent, one or two neutrals). More than that creates visual noise.
- **Consistent meaning:** If blue means "primary action" on slide 2, it means that on slide 10 too. Never reuse a color for a different semantic purpose.
- **Sufficient contrast:** Text must have a contrast ratio of at least 4.5:1 against its background. Light text on light backgrounds is unreadable from any distance.
- **Avoid pure black on pure white** for long text — dark gray (#1B1A18 or similar) on off-white is easier on the eyes.
- Use color to differentiate, not decorate. Every colored element should serve a purpose (grouping, emphasis, status).

## Tables

### Border & Style Consistency

- **Pick one border style and apply it to every table.** If the first table uses colored header-row borders with no internal vertical lines, every table follows that pattern.
- Headers must match their column's body alignment.

### Column Alignment

| Column | Alignment |
|--------|-----------|
| Leftmost (labels/names) | Left-align |
| Middle (short values, statuses) | Center-align |
| Rightmost (numbers, dates, notes) | Right-align |

If rightmost column has long descriptive text (not numbers), left-align it instead.

### Sizing

- Tables span full content width between margins. A narrow table centered on a wide slide wastes space.
- Font size as large as content allows — fill vertical space rather than leaving empty rows below.
- Column widths reflect content importance — primary label columns get more width, short value columns get less.

## Diagrams & Flowcharts

- **Keep boxes compact** — enough padding for readability but not so large they crowd out the connecting lines.
- **Visible connectors:** Lines between boxes should be clearly visible (min 12px length). If boxes are so large the lines disappear, shrink the boxes.
- **Even spacing:** Equal vertical and horizontal gaps between all nodes at the same level.
- **Consistent node sizes** within a tier — all child nodes the same width and height.
- **Direction:** Flow top-to-bottom or left-to-right. Never mix directions in a single diagram.
- **Labels on lines** only when the relationship isn't obvious from context.
- **Max 7±2 nodes** visible at once. If a diagram has more than 9 nodes, break it across slides or use progressive reveal.

## Groupings & Bullets

- Bullet when there are logical groupings. Section labels are not bulleted; only list items get bullets.
- Each bullet on its own line — separate paragraphs, no comma-separated lines.
- In peer groups (e.g., all section breaks, all feature cards), use the same capitalization and punctuation pattern.
- Bullet items should be parallel in structure — all start with a verb, or all are noun phrases. Don't mix.

## Slide Types (General)

### Title Slide
- Large heading + optional subtitle. Logo if applicable.
- Minimal content — this sets the tone, not the argument.

### Section Break
- Bold heading on a contrasting background. No body copy — this is a visual pause.
- All section breaks match each other in style.

### Content Slide
- Eyebrow/label above the heading.
- Heading + body on one side; visual on the other (or full-width content below).
- Use containers (cards, slabs, panels) to group related content.

### Stats / Metric Slide
- 1-3 large stat callouts. The number is the visual hero.
- Minimal surrounding copy. Let the stat speak.

### Quote / Testimonial
- One quote per slide. Large pull-quote in italic or medium weight.
- Attribution below in smaller text.

### Comparison / Table
- Use containers or columns. Keep rows scannable.
- Color-code categories, not individual values.

### Closing / CTA
- One clear action per closing slide. Logo + call-to-action.
- Contact info or next-step URL.

## Animation (HTML Decks Only)

For customer-demo deck sets, slight entrance animations are allowed. Full
specs, timing ladder, and the live-demo slide pattern live in
[references/slide-animation-patterns.md](references/slide-animation-patterns.md).
The non-negotiables:

- **Animations demo, they don't decorate.** The best animation acts out the
  mechanism (e.g. a waterfall table processing rows top-down, cells
  left-to-right, checks popping on success). If it doesn't demo or guide
  reading order, cut it.
- **Top-down population in reading order:** headline (0ms) → group labels
  (~200ms) → content items (100–150ms steps, left group first) → punchline
  last (~900ms, after a distinct pause).
- **One-shot entrances** with `animation-fill-mode: forwards`; default verb
  is fade-in-up (0.6s ease-out, 30px rise). No looping content animation.
- **At most one spring/overshoot pop per slide**, reserved for the success
  or payoff moment.
- **The settled final frame is the slide** — it must pass every static rule
  in this skill, since PPTX/PDF exports drop animation.

## Slide Count & Pacing

- **1 slide per minute** as a rough guide for a live talk. A 10-minute presentation = ~10 slides.
- **Vary slide density:** Alternate between dense content slides and visual pauses (section breaks, stat callouts, images).
- **Front-load the argument.** The core message should be clear by slide 3-4, not held as a reveal for the end.

## File-Format Boundary

Use document/presentation plugins or library-specific helpers for low-level
PPTX mechanics such as reading, writing, XML repair, or export. This skill owns
the presentation judgment: story, hierarchy, layout rhythm, brand consistency,
and rendered slide proof. When a deck is generated or repaired, inspect rendered
slides or screenshots before judging it complete.

## Final Polish Pass

When an existing deck is mostly built and Ethan asks you to polish, clean up, or
edit the actual deck file page by page, preserve the original and work from
rendered slides or screenshots. For critique-only polish requests, use
`slide-analyst` first. The polish pass should not rewrite claims, numbers,
citations, slide order, author names, or figures unless Ethan explicitly asks.

Check each slide for:

- projector-readable type and consistent title/body size tiers;
- text-frame overflow, clipped text, footer collisions, and page-number overlap;
- peer-slide drift in title position, box sizes, spacing, and visual weight;
- unintended italic/bold/style leaks;
- contrast, color meaning, source/footnote readability, and chart legibility;
- whether the slide still passes the squint test after fixes.

Apply the smallest targeted fix and keep a short change log when editing a
deck file. If the requested change would alter content rather than layout,
pause and call that out.

## Dimensions & Defaults

- **Standard dimensions:** 13.33 x 7.5 in (16:9). For older projectors: 10 x 7.5 in (4:3).
- **Margins:** 0.36-0.48 in for body; 0.9 in for decks with more whitespace.
- **Content start Y:** 0.3-0.7 in from top.
- **Footer:** Right-aligned, small (10-11 pt), consistent position across all slides.
- **Save outputs to `~/Downloads`** unless a specific path is requested.

## QA Checklist

- [ ] All content slide titles share the same position and font size
- [ ] All left blocks share the same left margin; all right blocks share the same right edge
- [ ] Peer slides use identical positions and dimensions for equivalent elements
- [ ] Box sizes consistent across peer slides — no shrinking to fit less content
- [ ] No text bleeds or overflows containers
- [ ] No shape exceeds slide boundaries (bottom edge ≤ slide height, right edge ≤ slide width)
- [ ] Stacked content boxes computed to fit available vertical space — no silent overflow past slide bottom
- [ ] Vertical spacing between sections is consistent across peer slides
- [ ] Tables span full content width; border style consistent across all tables
- [ ] Table column alignment follows left / center / right
- [ ] Text uses size tiers (24 / 18 / 14 / 12 / 10) — as large as space allows
- [ ] Peer slides use identical font sizes
- [ ] Color usage consistent — same color = same meaning throughout
- [ ] Sufficient text-to-background contrast
- [ ] Diagrams have visible connectors, even spacing, consistent node sizes
- [ ] Each slide passes the squint test — hierarchy is clear at a glance
- [ ] No bullet walls (6+ bullets on one slide)
- [ ] One clear idea per slide; conclusion-first headlines
- [ ] Final polish pass preserved the original and checked rendered slides when
      an existing deck was edited
