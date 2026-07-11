#!/usr/bin/env python3
import pathlib
import sys

if len(sys.argv) != 6:
    raise SystemExit("Usage: replace-references.py <file> <old> <new> <old-basename> <new-basename>")

path = pathlib.Path(sys.argv[1])
old, new, old_basename, new_basename = sys.argv[2:6]
text = path.read_text(encoding="utf-8")
text = text.replace(old, new).replace(old_basename, new_basename)
path.write_text(text, encoding="utf-8")
