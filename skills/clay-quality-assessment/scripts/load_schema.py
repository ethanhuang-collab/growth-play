#!/usr/bin/env python3
"""Unified Clay schema loader.

Both the `clay-handoff-doc-generator` and `clay-quality-assessment` skills
accept a Clay condensed schema as input. The Chrome extension can export that
schema in two shapes:

1. **Single-file** — one JSON file containing `columns[]`, `tableName`,
   `emailWaterfallProviders`, etc. Produced by "Extract Condensed".
2. **Chunked folder** — a directory (e.g. `Q/`) containing a manifest, a
   summary, prompts, and `columns-N` chunk files. Produced by "Extract Chunked"
   when a table is too large for a single file.

This loader takes either shape and returns a single merged dict that matches
the single-file format. Both skills should call this at the start of their
pipeline so downstream prompts/renderers only have to handle one shape.

Usage (CLI)
-----------
    python load_schema.py <path-to-file-or-folder> [--out merged.json]

Usage (Python)
--------------
    from load_schema import load_schema
    schema = load_schema("path/to/Q")
    schema = load_schema("path/to/single.json")
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path
from typing import Any


def _is_single_file_schema(data: dict) -> bool:
    """Heuristic: single-file condensed schemas carry `columns` at the root."""
    return isinstance(data.get("columns"), list) and "chunkIndex" not in data


def _load_chunked_folder(folder: Path) -> dict[str, Any]:
    """Merge a chunked export folder into a single schema dict."""
    json_files = sorted(glob.glob(str(folder / "*.json")))
    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {folder}")

    manifest: dict[str, Any] | None = None
    summary: dict[str, Any] | None = None
    prompts_obj: dict[str, Any] | None = None
    pricing_obj: dict[str, Any] | None = None
    chunks: dict[int, list] = {}
    # Some future exports may include orphan single-file schemas in the same
    # folder. If we find a single-file one and nothing else, return that.
    single_file_candidates: list[dict[str, Any]] = []

    for path in json_files:
        with open(path, encoding="utf-8") as f:
            try:
                doc = json.load(f)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

        if not isinstance(doc, dict):
            continue

        # Classify.
        if "chunkIndex" in doc and isinstance(doc.get("columns"), list):
            chunks[int(doc["chunkIndex"])] = doc["columns"]
        elif "perColumn" in doc and ("totals" in doc or "fetchedAt" in doc):
            # Pricing block: per-column credit cost from live Clay pricing.
            pricing_obj = doc
        elif "totalChunks" in doc or (
            "tableId" in doc and "columns" not in doc
        ):
            # Manifest: has table meta but no columns.
            manifest = doc
        elif "columnBreakdown" in doc or "enrichmentProviders" in doc:
            summary = doc
        elif "prompts" in doc or set(doc.keys()) == {"prompts"}:
            prompts_obj = doc
        elif _is_single_file_schema(doc):
            single_file_candidates.append(doc)

    # If the folder actually contained a single-file schema, prefer it.
    if single_file_candidates and not chunks:
        return single_file_candidates[0]

    if not chunks:
        raise ValueError(
            f"Could not identify chunked schema in {folder}. "
            "No column chunks (files with `chunkIndex`) were found."
        )

    # Merge chunks in order.
    merged_columns: list = []
    for idx in sorted(chunks):
        merged_columns.extend(chunks[idx])

    merged: dict[str, Any] = {"columns": merged_columns}

    # Copy useful top-level fields from manifest + summary (manifest wins).
    for src in (summary or {}, manifest or {}):
        for key in (
            "tableId",
            "tableName",
            "totalRows",
            "totalColumns",
            "columnCount",
            "extractedAt",
            "sourceUrl",
            "workspace",
            "viewFilters",
            "fillRates",
            "emailWaterfallProviders",
            "enrichmentProviders",
            "columnBreakdown",
            "workspaceCredits",
            "version",
            "exportedAt",
            "pricing",
        ):
            if key in src and key not in merged:
                merged[key] = src[key]

    # Prompts can arrive as `{prompts: [...]}` or as the list itself.
    if prompts_obj is not None:
        merged["prompts"] = prompts_obj.get("prompts", prompts_obj)

    # Pricing block lands in its own file (`pricing.json`); attach it so the
    # QA skill can render "Credits per Row" without re-fetching from Clay.
    if pricing_obj is not None and "pricing" not in merged:
        merged["pricing"] = pricing_obj

    # Fallback columnCount if missing.
    merged.setdefault("columnCount", len(merged_columns))

    return merged


def load_schema(path: str | os.PathLike) -> dict[str, Any]:
    """Load a Clay condensed schema from a single JSON file or chunked folder.

    Returns a dict matching the single-file condensed format.
    """
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(p)

    if p.is_dir():
        return _load_chunked_folder(p)

    with open(p, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"{p} is not a JSON object")

    # If somebody passed a single chunk file, try to load its parent folder.
    if "chunkIndex" in data and "columns" in data:
        return _load_chunked_folder(p.parent)

    if _is_single_file_schema(data):
        return data

    # Unknown shape — return as-is and let the caller decide.
    return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge a Clay schema (single file or chunked folder) into one JSON object."
    )
    parser.add_argument("path", help="Path to a JSON file or a folder of chunks.")
    parser.add_argument(
        "--out",
        help="Where to write the merged schema. Default: stdout.",
    )
    args = parser.parse_args()

    try:
        schema = load_schema(args.path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps(schema, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).expanduser().write_text(payload, encoding="utf-8")
        cols = len(schema.get("columns", []))
        print(
            f"Merged schema written to {args.out} "
            f"({cols} columns, table={schema.get('tableName', '?')})",
            file=sys.stderr,
        )
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
