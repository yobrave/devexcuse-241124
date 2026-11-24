#!/usr/bin/env python3
"""Build the entry artifact for the make.fun developer-excuse bounty.

The judge reads one line. This script takes that line from entry.txt in
the same folder, trims it to a single non-empty line, refuses anything
over 200 characters or under 1, and writes it to the output directory
the grader mounts. One JSON line on stdout says what happened.
"""
import json
import os
import pathlib
import sys

SLUG = "u-motasimfuad-make-the-ai-judge-laugh-developer-49386be3"
LIMIT = 200


def load_line():
    folder = pathlib.Path(__file__).resolve().parent
    text = (folder / "entry.txt").read_text(encoding="utf-8")
    for row in text.replace("\r\n", "\n").split("\n"):
        row = row.strip()
        if row:
            return row
    raise ValueError("entry.txt holds no non-blank line")


def emit(line):
    target = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target.mkdir(parents=True, exist_ok=True)
    (target / "entry.txt").write_text(line + "\n",
                                      encoding="utf-8", newline="\n")


def report(kind, **facts):
    payload = {"status": kind, "slug": SLUG, **facts}
    print(json.dumps(payload))
    return 0 if kind == "ok" else 2


def run():
    try:
        line = load_line()
    except FileNotFoundError:
        return report("missing", hint="entry.txt must sit beside main.py")
    except ValueError as why:
        return report("blank", hint=str(why))
    if not 1 <= len(line) <= LIMIT:
        return report("too_long", got=len(line), limit=LIMIT)
    emit(line)
    return report("ok", wrote=len(line))


if __name__ == "__main__":
    sys.exit(run())
