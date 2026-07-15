#!/usr/bin/env python3
"""Validate the Markdown manuscript and its SVG illustrations.

The checker deliberately uses only Python's standard library so contributors and
CI can run the same quality gate without installing a documentation toolchain.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
ASSETS = CHAPTERS / "assets"
README = ROOT / "README.md"

LINK_RE = re.compile(
    r"(?P<image>!)?\[[^]\n]*]\(\s*(?:<(?P<angle>[^>]+)>|(?P<plain>[^)\s]+))"
)
FENCE_RE = re.compile(r"^\s*(?P<marker>`{3,}|~{3,})(?P<info>.*)$")
HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
REMOTE_SCHEMES = {"http", "https", "mailto", "data"}


def relative(path: Path) -> str:
    """Return a stable repository-relative path for diagnostics."""

    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def mask_fenced_code(text: str) -> str:
    """Hide fenced code while preserving offsets used in diagnostics."""

    masked: list[str] = []
    fence_marker: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        ending = line[len(content) :]
        fence = FENCE_RE.match(content)
        if fence_marker is None:
            if fence:
                marker = fence.group("marker")
                fence_marker = marker[0]
                fence_length = len(marker)
                masked.append(" " * len(content) + ending)
            else:
                masked.append(line)
            continue

        masked.append(" " * len(content) + ending)
        if fence:
            marker = fence.group("marker")
            info = fence.group("info").strip()
            if marker[0] == fence_marker and len(marker) >= fence_length and not info:
                fence_marker = None
                fence_length = 0
    return "".join(masked)


def local_target(source: Path, raw_target: str) -> Path | None:
    """Resolve a Markdown target, or return None for remote/anchor links."""

    target = raw_target.strip()
    parsed = urlsplit(target)
    if parsed.scheme.lower() in REMOTE_SCHEMES or target.startswith("#"):
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate.resolve()
    return (source.parent / candidate).resolve()


def validate_markdown(path: Path, errors: list[str], image_refs: Counter[Path]) -> None:
    text = path.read_text(encoding="utf-8")

    for match in LINK_RE.finditer(mask_fenced_code(text)):
        raw_target = match.group("angle") or match.group("plain")
        target = local_target(path, raw_target)
        if target is not None and not target.exists():
            errors.append(
                f"{relative(path)}:{line_number(text, match.start())}: "
                f"local link does not exist: {raw_target}"
            )
        if match.group("image") and target is not None:
            image_refs[target] += 1
            alt = match.group(0).split("]", 1)[0][2:].strip()
            if not alt:
                errors.append(
                    f"{relative(path)}:{line_number(text, match.start())}: image alt text is empty"
                )

    fence_marker: str | None = None
    fence_length = 0
    headings: list[tuple[int, int]] = []

    for number, line in enumerate(text.splitlines(), start=1):
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group("marker")
            info = fence.group("info").strip()
            if fence_marker is None:
                fence_marker = marker[0]
                fence_length = len(marker)
                if not info:
                    errors.append(
                        f"{relative(path)}:{number}: fenced code block has no language"
                    )
            elif marker[0] == fence_marker and len(marker) >= fence_length and not info:
                fence_marker = None
                fence_length = 0
            continue

        if fence_marker is None:
            heading = HEADING_RE.match(line)
            if heading:
                headings.append((len(heading.group("marks")), number))

    if fence_marker is not None:
        errors.append(f"{relative(path)}: fenced code block is not closed")

    h1_count = sum(level == 1 for level, _ in headings)
    if h1_count != 1:
        errors.append(f"{relative(path)}: expected exactly one H1, found {h1_count}")
    for previous, current in zip(headings, headings[1:]):
        if current[0] > previous[0] + 1:
            errors.append(
                f"{relative(path)}:{current[1]}: heading level jumps "
                f"from H{previous[0]} to H{current[0]}"
            )


def validate_svg(path: Path, errors: list[str]) -> None:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        errors.append(f"{relative(path)}: invalid XML: {exc}")
        return

    if root.tag.rsplit("}", 1)[-1] != "svg":
        errors.append(f"{relative(path)}: root element is not <svg>")
    view_box = root.attrib.get("viewBox", "").split()
    if len(view_box) != 4:
        errors.append(f"{relative(path)}: expected a four-value viewBox")
        return
    try:
        width, height = float(view_box[2]), float(view_box[3])
    except ValueError:
        errors.append(f"{relative(path)}: viewBox contains non-numeric values")
        return
    if width <= 0 or height <= 0:
        errors.append(f"{relative(path)}: viewBox width and height must be positive")


def validate_readme(chapter_files: list[Path], errors: list[str]) -> None:
    text = README.read_text(encoding="utf-8")
    listed = Counter(
        match.group(1)
        for match in re.finditer(r"\((chapters/[^)#]+\.md)(?:#[^)]*)?\)", text)
    )
    expected = {relative(path) for path in chapter_files}

    for missing in sorted(expected - listed.keys()):
        errors.append(f"README.md: chapter is missing from the table of contents: {missing}")
    for unknown in sorted(listed.keys() - expected):
        errors.append(f"README.md: table of contents points to an unknown chapter: {unknown}")
    for duplicate, count in sorted(listed.items()):
        if duplicate in expected and count != 1:
            errors.append(
                f"README.md: chapter appears {count} times in the table of contents: {duplicate}"
            )

    stated_count = re.search(
        r"现有\s*\*\*(?:\d+\s*个部分、)?(\d+)\s*篇文章\*\*", text
    )
    if not stated_count:
        errors.append("README.md: cannot find the stated article count")
    elif int(stated_count.group(1)) != len(chapter_files):
        errors.append(
            "README.md: stated article count is "
            f"{stated_count.group(1)}, but found {len(chapter_files)} chapter files"
        )


def main() -> int:
    errors: list[str] = []
    chapter_files = sorted(CHAPTERS.rglob("*.md"))
    svg_files = sorted(ASSETS.glob("*.svg"))
    image_refs: Counter[Path] = Counter()

    if not chapter_files:
        errors.append("chapters: no Markdown files found")
    if not svg_files:
        errors.append("chapters/assets: no SVG files found")

    for path in chapter_files:
        validate_markdown(path, errors, image_refs)
    for path in svg_files:
        validate_svg(path, errors)

    validate_readme(chapter_files, errors)

    svg_set = {path.resolve() for path in svg_files}
    for unreferenced in sorted(svg_set - image_refs.keys()):
        errors.append(f"{relative(unreferenced)}: SVG is not referenced by any chapter")
    for referenced in sorted(image_refs.keys() - svg_set):
        if referenced.suffix.lower() == ".svg":
            errors.append(f"{relative(referenced)}: referenced SVG is outside chapters/assets")

    if errors:
        print(f"Book validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in sorted(errors):
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(
        f"Book validation passed: {len(chapter_files)} chapters, "
        f"{len(svg_files)} SVGs, {sum(image_refs.values())} image references."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
