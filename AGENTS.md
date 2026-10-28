# Growth Play Kit

Markdown skills, block cards, and two Python CLIs. There is no web server and no test suite.

## Cursor Cloud specific instructions

The base image does not include `ensurepip`. Install `python3.12-venv` before creating a virtualenv (`sudo apt-get update && sudo apt-get install -y python3.12-venv`).

From the repo root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r slide/requirements.txt python-docx
```

`.venv/` is local and is not committed. `python-pptx` pulls in `lxml`, which `slide/generate.py` imports directly. `python-docx` is only for `skills/clay-quality-assessment/scripts/generate_docx.py`.

Slide generator (the app to run):

```bash
.venv/bin/python slide/generate.py slide/examples/closed-lost-re-heat.json --out /tmp/slides
```

That writes a 1920×1080 `.pptx` and a `.png`. Poppins in `slide/fonts/` is the preview font when `~/Downloads/Terra — Brand Design System.zip` is absent. Do not pass `--open`; that calls macOS `open`.

A `## Slide` section in an overview markdown file is the other accepted input. JSON specs need `title`, `who`, `talk`, and `considerations`.

Schema loader smoke check:

```bash
.venv/bin/python skills/clay-quality-assessment/scripts/load_schema.py path/to/schema.json --out /tmp/schema.json
```
