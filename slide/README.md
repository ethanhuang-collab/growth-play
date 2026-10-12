# Growth Play Slide

One 16:9 slide per play. The layout matches the edited deck in Downloads from 2026-10-10: title and go-live pill, Who We Target and Considerations on the left, Talk Track across the right, claymation icons, Clay logo. Each block is one PowerPoint bullet list, so Enter starts the next bullet.

Generate it at stage 1 or stage 2, from the `## Slide` section of the overview. Stage 1 still has the Talk Track and Considerations prompts. Stage 2 generates it again once those are filled. Go-live stays `[Date]` until someone sets it.

## Command

```bash
python3 growth-play/slide/generate.py plays/<play>/overview.md
```

The words come from `overview.md` under `## Slide`. Stage 1 derives Who We Target from the approved business logic, including the timing condition that makes outreach timely now. Ethan is not asked. Stage 2 asks for the Talk Track and for Considerations, and writes both into the same section. Generate the file at either stage. Go-live stays `[Date]` until someone sets it. A JSON file of the same fields still works. The Closed-Lost sample is in `plays/closed-lost-rearch/overview.md`.

Needs `python-pptx` and `pillow` (`requirements.txt`). The PowerPoint file and a PNG preview land in `~/Downloads`. Upload the `.pptx` to Drive and open it with Google Slides. Slides uses Poppins. The preview uses Roobert when the Terra brand zip is in Downloads.

## Slide Section

| Block | When it is asked |
| --- | --- |
| Title | Stage 1. The exact play name |
| Who We Target | Stage 1. Derived account, person, and timing. Top left. `**Label:** text` or a plain bullet |
| Talk Track | Stage 2. Asked outright. Full right side. One bullet per line |
| Considerations | Stage 2. Asked outright. Bottom left. One bullet per line |
| Go-live | Left as `[Date]` until a person sets it |

A line wrapped entirely in brackets is drawn as a prompt. Icons, colors, and the three headings stay on the template. Each block is a single text box with a real bullet on every line.
