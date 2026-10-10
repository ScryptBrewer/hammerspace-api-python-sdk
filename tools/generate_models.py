"""Regenerate hammerspace/models/generated.py from the vendored swagger spec.

Pipeline:
1. datamodel-codegen (dev tool, not a project dependency) emits Pydantic v2
   models with ``--target-python-version 3.10`` (0.83 dropped the 3.9 target).
2. This script then rewrites every top-level ``X | None`` union to
   ``Optional[X]`` so the module imports on Python 3.9, which pyproject
   declares as the minimum supported version (PEP 604 annotations fail
   pydantic's eager evaluation on 3.9).

Usage:
    python tools/generate_models.py --spec Hammerspace_5_3_swagger.json
"""
import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

HEADER_TYPING_LINE = "from typing import Any"


def split_top_level(typ: str) -> List[str]:
    """Split ``A | B | C`` on top-level `` | `` separators (bracket-aware)."""
    alts: List[str] = []
    depth = 0
    cur_start = 0
    i = 0
    while i < len(typ):
        ch = typ[i]
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif depth == 0 and typ.startswith(" | ", i):
            alts.append(typ[cur_start:i])
            i += 3
            cur_start = i
            continue
        i += 1
    alts.append(typ[cur_start:])
    return [a.strip() for a in alts]


def convert_union(typ: str) -> str:
    """Rewrite a single annotation: top-level ``X | None`` -> ``Optional[X]``."""
    alts = split_top_level(typ)
    if len(alts) <= 1:
        return typ
    non_none = [a for a in alts if a != "None"]
    if len(non_none) == len(alts):
        return typ
    if len(non_none) == 1:
        return f"Optional[{non_none[0]}]"
    return f"Union[{', '.join(non_none)}, None]"


def convert_line(line: str) -> Tuple[str, bool]:
    """Convert the annotation on one generated model-field line."""
    stripped = line.lstrip()
    if ":" not in stripped or " | None" not in stripped:
        return line, False
    indent = line[: len(line) - len(stripped)]
    name, rest = stripped.split(":", 1)
    if " = " in rest:
        typ, default = rest.split(" = ", 1)
        converted = convert_union(typ.strip())
        return f"{indent}{name}: {converted} = {default}", converted != typ.strip()
    converted = convert_union(rest.strip())
    return f"{indent}{name}: {converted}", converted != rest.strip()


def make_py39_compatible(source: str) -> Tuple[str, int]:
    lines_out = []
    changed = 0
    for line in source.splitlines():
        new_line, was_changed = convert_line(line)
        if was_changed:
            changed += 1
        lines_out.append(new_line)
    text = "\n".join(lines_out)
    if HEADER_TYPING_LINE in text and "Optional" not in text.split("\n\n")[0]:
        text = text.replace(
            HEADER_TYPING_LINE, "from typing import Any, Optional", 1
        )
    return text, changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", default="Hammerspace_5_3_swagger.json")
    parser.add_argument("--output", default="hammerspace/models/generated.py")
    args = parser.parse_args()

    cmd = [
        sys.executable, "-m", "datamodel_code_generator",
        "--input", args.spec,
        "--input-file-type", "jsonschema",
        "--target-pydantic-version", "2",
        "--target-python-version", "3.10",
        "--snake-case-field",
        "--base-class", "hammerspace.models.base.HammerspaceBaseModel",
        "--use-schema-description",
        "--use-field-description",
        "--output", args.output,
    ]
    subprocess.run(cmd, check=True)

    out_path = Path(args.output)
    text, changed = make_py39_compatible(out_path.read_text())
    out_path.write_text(text)
    print(f"rewrote {changed} annotations to Optional[...] for Python 3.9 -> {args.output}")


if __name__ == "__main__":
    main()
