"""Minimal JSONC (JSON with Comments) editing helpers.

Comments are stripped without shifting character offsets, so structural
positions found in stripped text map 1:1 onto the original text.
"""

from __future__ import annotations

import json
import re


def strip_comments(text: str) -> str:
    """Replace // and /* */ comments with spaces, preserving offsets."""
    out = list(text)
    i = 0
    n = len(text)
    in_str = False
    while i < n:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            i += 1
            continue
        if ch == "/" and i + 1 < n:
            nxt = text[i + 1]
            if nxt == "/":
                while i < n and text[i] != "\n":
                    out[i] = " "
                    i += 1
                continue
            if nxt == "*":
                out[i] = " "
                out[i + 1] = " "
                i += 2
                while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                    out[i] = " "
                    i += 1
                if i + 1 < n:
                    out[i] = " "
                    out[i + 1] = " "
                    i += 2
                continue
        i += 1
    return "".join(out)


def is_valid(text: str) -> bool:
    try:
        json.loads(strip_comments(text))
        return True
    except ValueError:
        return False


def _skip_whitespace(text: str, i: int) -> int:
    while i < len(text) and text[i] in " \t\r\n":
        i += 1
    return i


def _match_brace(text: str, i: int) -> int:
    """Index of the '}' matching the '{' at i (string-aware), or -1."""
    depth = 0
    in_str = False
    n = len(text)
    while i < n:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _key_value_at_root(text: str, key: str) -> int:
    """Index of the value for a key in the root object, or -1."""
    pattern = re.compile(r'"' + re.escape(key) + r'"\s*:')
    depth = 0
    in_str = False
    n = len(text)
    i = 0
    while i < n:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
            i += 1
            continue
        if depth == 1:
            m = pattern.match(text, i)
            if m:
                return _skip_whitespace(text, m.end())
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        i += 1
    return -1


def object_span(text: str, key: str) -> tuple[int, int] | None:
    """(open, close) brace indices of the root-level object for key."""
    clean = strip_comments(text)
    value = _key_value_at_root(clean, key)
    if value < 0 or clean[value] != "{":
        return None
    close = _match_brace(clean, value)
    if close < 0:
        return None
    return (value, close)


def top_level_close(text: str) -> int:
    """Index of the closing brace of the top-level object, or -1."""
    clean = strip_comments(text)
    i = _skip_whitespace(clean, 0)
    if i >= len(clean) or clean[i] != "{":
        return -1
    return _match_brace(clean, i)


def remove_block(text: str, start_marker: str, end_marker: str) -> str:
    """Remove the start/end marker lines and everything between them."""
    pattern = re.compile(
        r"(?m)^[ \t]*"
        + re.escape(start_marker)
        + r"[^\n]*\n(?:[^\n]*\n)*?[ \t]*"
        + re.escape(end_marker)
        + r"[^\n]*(?:\n|$)"
    )
    return pattern.sub("", text)


def remove_named_entries(text: str, span: tuple[int, int], names: list[str]) -> str:
    """Remove '"name": {...}' entries inside the object span."""
    open_i, close_i = span
    head = text[: open_i + 1]
    body = text[open_i + 1 : close_i]
    tail = text[close_i:]
    for name in names:
        body = _remove_entry(body, name)
    return head + body + tail


def _remove_entry(body: str, name: str) -> str:
    clean = strip_comments(body)
    pattern = re.compile(r'"' + re.escape(name) + r'"\s*:')
    matches = list(pattern.finditer(clean))
    for m in reversed(matches):
        value_i = _skip_whitespace(clean, m.end())
        if value_i >= len(clean) or clean[value_i] not in '{["':
            continue
        end = _scan_value(clean, value_i)
        i = end
        while i < len(clean) and clean[i] in " \t":
            i += 1
        if i < len(clean) and clean[i] == ",":
            i += 1
        i = _skip_whitespace(clean, i)
        line_start = m.start()
        while line_start > 0 and body[line_start - 1] != "\n":
            line_start -= 1
        body = body[:line_start] + body[i:]
    return body


def _scan_value(text: str, i: int) -> int:
    """End index (exclusive) of the JSON value starting at i."""
    n = len(text)
    ch = text[i]
    if ch == '"':
        i += 1
        while i < n:
            if text[i] == "\\":
                i += 2
                continue
            if text[i] == '"':
                return i + 1
            i += 1
        return i
    if ch in "[{":
        close = "]" if ch == "[" else "}"
        depth = 0
        in_str = False
        while i < n:
            c = text[i]
            if in_str:
                if c == "\\":
                    i += 2
                    continue
                if c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c in "[{":
                    depth += 1
                elif c in "]}":
                    depth -= 1
                    if depth == 0 and c == close:
                        return i + 1
            i += 1
        return i
    while i < n and text[i] not in ",}\n":
        i += 1
    return i


def fix_trailing_commas(text: str) -> str:
    """Remove commas that directly precede a closing brace (string/comment-aware)."""
    drop: list[int] = []
    in_str = False
    n = len(text)
    i = 0
    last = ("", -1)
    while i < n:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            last = (ch, i)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        if ch in " \t\r\n":
            i += 1
            continue
        if ch == ",":
            last = (",", i)
            i += 1
            continue
        if ch == "}" and last[0] == ",":
            drop.append(last[1])
        last = (ch, i)
        i += 1
    if not drop:
        return text
    out = list(text)
    for idx in reversed(drop):
        del out[idx]
    return "".join(out)


def build_block(
    start_marker: str, end_marker: str, entries: list[str], needs_comma: bool
) -> str:
    """Build a managed marker block from entry texts."""
    lines = [start_marker]
    for idx, entry in enumerate(entries):
        comma = "," if idx < len(entries) - 1 or needs_comma else ""
        lines.append(entry + comma)
    lines.append(end_marker)
    return "\n".join(lines)


def insert_after_brace(text: str, brace_idx: int, block: str) -> str:
    """Insert a block right after the '{' at brace_idx (marker on its own line)."""
    next_line = text[brace_idx + 1 : brace_idx + 2] == "\n"
    tail = "" if next_line else "\n"
    return text[: brace_idx + 1] + "\n" + block + tail + text[brace_idx + 1 :]


def insert_key_before_close(text: str, close_idx: int, key: str, block: str) -> str:
    """Insert '"key": { block }' just before the top-level closing brace."""
    prefix = text[:close_idx].rstrip(" \t\r\n")
    comma = "," if not prefix.endswith("{") else ""
    return (
        prefix
        + comma
        + "\n  \""
        + key
        + "\": {\n"
        + block
        + "\n  }\n"
        + text[close_idx:]
    )
