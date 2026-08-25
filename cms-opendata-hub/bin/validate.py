#!/usr/bin/env python3
"""Validate resource records against the schema and the controlled vocabularies.

Run locally with `python bin/validate.py`; CI runs it on every pull request.
The point is that a contributor gets told exactly what is wrong without a
maintainer having to read the diff.
"""

import sys
import pathlib
import datetime
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "_resources"
VOCAB = yaml.safe_load((ROOT / "_data" / "vocab.yml").read_text())
DATASETS = yaml.safe_load((ROOT / "_data" / "datasets.yml").read_text()) or {}

REQUIRED = [
    "title", "status", "last_verified", "summary", "audience",
    "languages", "duration", "setup_burden", "links", "license",
]

# field name -> vocabulary key, and whether the field is a list
CONTROLLED = {
    "status": ("status", False),
    "setup_burden": ("setup_burden", False),
    "audience": ("audience", True),
    "physics_topics": ("physics_topic", True),
    "computing_topics": ("computing_topic", True),
    "tags": ("tag", True),
}

NESTED_CONTROLLED = {
    ("prerequisites", "physics"): "physics_topic",
    ("prerequisites", "computing"): "computing_topic",
    ("data", "formats"): "data_format",
}


def allowed(key):
    return {entry["id"] for entry in VOCAB[key]}


def split_front_matter(text, path, errors):
    if not text.startswith("---"):
        errors.append(f"{path.name}: no YAML front matter")
        return None, ""
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{path.name}: front matter is not closed with ---")
        return None, ""
    try:
        return yaml.safe_load(parts[1]), parts[2]
    except yaml.YAMLError as exc:
        errors.append(f"{path.name}: front matter is not valid YAML: {exc}")
        return None, ""


def check(path, errors, warnings):
    meta, body = split_front_matter(path.read_text(), path, errors)
    if meta is None:
        return

    name = path.name

    for field in REQUIRED:
        if not meta.get(field):
            errors.append(f"{name}: missing required field '{field}'")

    for field, (vocab_key, is_list) in CONTROLLED.items():
        value = meta.get(field)
        if value is None:
            continue
        values = value if is_list else [value]
        for v in values:
            if v not in allowed(vocab_key):
                errors.append(
                    f"{name}: '{v}' in {field} is not in the {vocab_key} vocabulary. "
                    f"Add it to _data/vocab.yml in this PR if it belongs there."
                )

    for (outer, inner), vocab_key in NESTED_CONTROLLED.items():
        for v in (meta.get(outer) or {}).get(inner) or []:
            if v not in allowed(vocab_key):
                errors.append(
                    f"{name}: '{v}' in {outer}.{inner} is not in the {vocab_key} vocabulary"
                )

    for ds in (meta.get("data") or {}).get("datasets") or []:
        if ds not in DATASETS:
            errors.append(f"{name}: dataset '{ds}' is not defined in _data/datasets.yml")

    link_types = allowed("link_type")
    for link in meta.get("links") or []:
        if link.get("type") not in link_types:
            errors.append(f"{name}: link type '{link.get('type')}' is not in the vocabulary")
        url = link.get("url", "")
        if not url.startswith("http"):
            errors.append(f"{name}: link '{url}' is not an absolute URL")

    duration = meta.get("duration") or {}
    lo, hi = duration.get("min_minutes"), duration.get("max_minutes")
    if lo is None:
        errors.append(f"{name}: duration.min_minutes is required")
    elif hi is not None and hi < lo:
        errors.append(f"{name}: duration.max_minutes is less than min_minutes")

    verified = meta.get("last_verified")
    if isinstance(verified, datetime.date):
        age = (datetime.date.today() - verified).days
        if age > 550:
            warnings.append(
                f"{name}: last verified {age} days ago. Check the links and bump the date."
            )
    elif verified is not None:
        errors.append(f"{name}: last_verified must be a date, e.g. 2026-08-20")

    if len(body.strip()) < 120:
        warnings.append(f"{name}: description is very short. A paragraph or two helps a lot.")


def main():
    errors, warnings = [], []
    files = sorted(RESOURCES.glob("*.md"))

    if not files:
        print("No resource records found in _resources/")
        return 1

    for path in files:
        check(path, errors, warnings)

    for w in warnings:
        print(f"warning  {w}")
    for e in errors:
        print(f"ERROR    {e}")

    print(f"\n{len(files)} records checked, {len(errors)} errors, {len(warnings)} warnings.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
