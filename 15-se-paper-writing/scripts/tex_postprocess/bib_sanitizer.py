"""BibTeX sanitization module.

Fixes common BibTeX issues before LaTeX compilation:
1. Extra identifiers after entry keys  (@misc{key, ExtraID, field=...})
2. Double/trailing commas              (@misc{key,,  or  field={val},,)
3. Duplicate entries                   (keeps first occurrence of each key)
4. Non-ASCII characters                (replaces with LaTeX equivalents)
5. Expecting '=' errors                (@misc{key, Word (text), field=...})
6. Malformed field values              (e.g., x""x artifacts)
7. Empty/incomplete entries            (entries missing required closing brace)
"""

import os
import re
from typing import Dict, Any, List, Tuple, Optional


# ── Unicode → LaTeX replacement map ──────────────────────────────────────────

_CHAR_MAP = {
    # Accented vowels
    '\u00e9': "\\'{e}",    '\u00e8': "\\`{e}",    '\u00ea': "\\^{e}",
    '\u00eb': '\\"{{e}}',  '\u00c9': "\\'{E}",
    '\u00e1': "\\'{a}",    '\u00e0': "\\`{a}",    '\u00e2': "\\^{a}",
    '\u00e4': '\\"{{a}}',  '\u00e3': "\\~{a}",    '\u00e5': "\\aa{}",
    '\u00f3': "\\'{o}",    '\u00f2': "\\`{o}",    '\u00f4': "\\^{o}",
    '\u00f6': '\\"{{o}}',  '\u00f5': "\\~{o}",
    '\u00fa': "\\'{u}",    '\u00f9': "\\`{u}",    '\u00fb': "\\^{u}",
    '\u00fc': '\\"{{u}}',
    '\u00ed': "\\'{i}",    '\u00ec': "\\`{i}",    '\u00ee': "\\^{i}",
    '\u00ef': '\\"{{i}}',
    # Accented consonants / special
    '\u00f1': "\\~{n}",    '\u00e7': "\\c{c}",    '\u00c7': "\\c{C}",
    '\u00f8': "\\o{}",     '\u00d8': "\\O{}",     '\u00df': "\\ss{}",
    '\u00dc': '\\"{{U}}',  '\u00d6': '\\"{{O}}',  '\u00c4': '\\"{{A}}',
    '\u0142': "\\l{}",     '\u0141': "\\L{}",     '\u011e': "\\u{G}",
    '\u015e': "\\c{S}",    '\u0131': "{\\i}",
    # Punctuation / typography
    '\u2013': '--',         '\u2014': '---',       '\u2010': '-',
    '\u201c': '``',         '\u201d': "''",
    '\u2018': '`',          '\u2019': "'",
    '\u2022': '\\textbullet{}',
    '\u2026': '\\ldots{}',
    '\u00a0': '~',          '\u200b': '',
    # Common mojibake sequences (UTF-8 bytes misread as latin-1)
    '\u00c3\u00a9': "\\'{e}",
    '\u00c3\u00b6': '\\"{{o}}',
    '\u00c3\u00a3': '\\~{a}',
    '\u00c3\u00a2': '\\^{a}',
    '\u00c3\u00bc': '\\"{{u}}',
}


def sanitize_bib_file(
    bib_path: str,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Sanitize a .bib file, fixing all common issues in-place.

    Args:
        bib_path: Path to the .bib file.
        verbose: Print progress and statistics.

    Returns:
        Dictionary with counts of each fix type applied.
    """
    if not os.path.isfile(bib_path):
        if verbose:
            print(f"  BibTeX file not found: {bib_path}")
        return {'error': 'file_not_found'}

    with open(bib_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    stats: Dict[str, int] = {
        'extra_ids_removed': 0,
        'double_commas_fixed': 0,
        'duplicates_removed': 0,
        'non_ascii_replaced': 0,
        'malformed_values_fixed': 0,
        'total_entries_before': 0,
        'total_entries_after': 0,
    }

    original = content

    # ── Pass 1: Fix malformed field values ────────────────────────────────
    # e.g., x""x artifacts
    if 'x""x' in content:
        content = content.replace('x""x', '')
        stats['malformed_values_fixed'] += 1

    # ── Pass 2: Fix non-ASCII characters ──────────────────────────────────
    # Apply mojibake (multi-char) replacements first, then single-char
    for old, new in sorted(_CHAR_MAP.items(), key=lambda x: -len(x[0])):
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            stats['non_ascii_replaced'] += count

    # Remove any remaining non-ASCII
    remaining = set(re.findall(r'[^\x00-\x7F]', content))
    if remaining:
        for c in remaining:
            stats['non_ascii_replaced'] += content.count(c)
        content = re.sub(r'[^\x00-\x7F]', '', content)

    # ── Pass 3: Fix entry-level syntax errors ─────────────────────────────
    # Parse entries and fix each one
    lines = content.split('\n')
    fixed_lines: List[str] = []
    seen_keys: Dict[str, int] = {}
    i = 0

    while i < len(lines):
        line = lines[i]

        # Match entry start: @type{key, ...
        entry_match = re.match(r'^(@\w+)\{(.*)$', line)
        if entry_match:
            entry_type = entry_match.group(1)
            rest = entry_match.group(2)

            # Find the end of this entry (brace matching)
            entry_lines = [line]
            brace_count = line.count('{') - line.count('}')
            j = i
            while brace_count > 0 and j + 1 < len(lines):
                j += 1
                entry_lines.append(lines[j])
                brace_count += lines[j].count('{') - lines[j].count('}')
            entry_end = j

            stats['total_entries_before'] += 1

            # Reconstruct the entry text
            entry_text = '\n'.join(entry_lines)

            # --- Fix 3a: Extract key and clean extra identifiers ---
            key, cleaned_entry = _fix_entry_key(entry_type, rest, entry_text)

            if key is None:
                # Could not parse key — keep entry as-is
                fixed_lines.extend(entry_lines)
                i = entry_end + 1
                continue

            # --- Fix 3b: Check for duplicate key ---
            if key in seen_keys:
                stats['duplicates_removed'] += 1
                if verbose:
                    print(f"  Removed duplicate: {key} "
                          f"(line {i+1}, first at line {seen_keys[key]+1})")
                # Skip this entry (and blank line after if present)
                i = entry_end + 1
                if i < len(lines) and lines[i].strip() == '':
                    i += 1
                continue

            seen_keys[key] = i

            if cleaned_entry != entry_text:
                stats['extra_ids_removed'] += 1
                if verbose:
                    print(f"  Fixed key syntax: {key} (line {i+1})")

            # --- Fix 3c: Double commas anywhere in entry ---
            while ',,' in cleaned_entry:
                cleaned_entry = cleaned_entry.replace(',,', ',')
                stats['double_commas_fixed'] += 1

            fixed_lines.extend(cleaned_entry.split('\n'))
            stats['total_entries_after'] += 1
            i = entry_end + 1
        else:
            fixed_lines.append(line)
            i += 1

    content = '\n'.join(fixed_lines)

    # ── Write back if changed ─────────────────────────────────────────────
    if content != original:
        with open(bib_path, 'w', encoding='utf-8') as f:
            f.write(content)

    if verbose:
        print(f"\n  Sanitization summary for {os.path.basename(bib_path)}:")
        print(f"    Entries: {stats['total_entries_before']} -> "
              f"{stats['total_entries_after']}")
        print(f"    Extra IDs removed:    {stats['extra_ids_removed']}")
        print(f"    Double commas fixed:  {stats['double_commas_fixed']}")
        print(f"    Duplicates removed:   {stats['duplicates_removed']}")
        print(f"    Non-ASCII replaced:   {stats['non_ascii_replaced']}")
        print(f"    Malformed values:     {stats['malformed_values_fixed']}")

    return stats


def _fix_entry_key(
    entry_type: str,
    rest_of_first_line: str,
    full_entry: str,
) -> Tuple[Optional[str], str]:
    """Fix the entry key line, removing extra identifiers.

    Handles patterns like:
        @misc{key, ExtraID, field=...}        -> @misc{key, field=...}
        @misc{key, Word (text), field=...}    -> @misc{key, field=...}
        @misc{key,, field=...}                -> @misc{key, field=...}

    Returns:
        (key, fixed_entry_text) or (None, original) if unparseable.
    """
    # Split rest_of_first_line to get the key and remaining tokens
    # The key is everything up to the first comma
    comma_pos = rest_of_first_line.find(',')
    if comma_pos == -1:
        # No comma — probably a malformed entry, return as-is
        return (rest_of_first_line.strip().rstrip('}'), full_entry)

    key = rest_of_first_line[:comma_pos].strip()
    after_key = rest_of_first_line[comma_pos + 1:].strip()

    # Check if what follows the key is a valid BibTeX field (name = value)
    # or junk identifiers that need to be removed
    # A valid field starts with: fieldname = or fieldname={
    # Junk looks like: ExtraID, or Word (text),

    cleaned_after = _strip_junk_before_fields(after_key)

    if cleaned_after != after_key:
        # Reconstruct the first line
        new_first_line = f"{entry_type}{{{key}, {cleaned_after}"
        # Replace only the first line in the full entry
        first_newline = full_entry.find('\n')
        if first_newline == -1:
            fixed_entry = new_first_line
        else:
            fixed_entry = new_first_line + full_entry[first_newline:]
        return (key, fixed_entry)

    return (key, full_entry)


def _strip_junk_before_fields(text: str) -> str:
    """Remove non-field tokens between the key and the first real field.

    Iteratively strips tokens that don't match `fieldname =` or `fieldname={`.
    """
    original = text
    max_iterations = 10  # safety limit

    for _ in range(max_iterations):
        stripped = text.lstrip(', \t')

        if not stripped:
            return stripped

        # Check if it starts with a valid BibTeX field: word = or word={
        field_match = re.match(
            r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=', stripped
        )
        if field_match:
            return stripped

        # Check if it starts with common BibTeX field names specifically
        # (handles edge cases where field name is followed by { directly)
        field_match2 = re.match(
            r'^(title|author|year|month|url|doi|DOI|ISBN|ISSN|journal|'
            r'booktitle|publisher|volume|number|pages|series|edition|'
            r'note|eprint|archivePrefix|primaryClass|collection|address|'
            r'howpublished|school|institution|type|chapter|editor|'
            r'organization|numpages|keywords|abstract|annote)\s*[={]',
            stripped, re.IGNORECASE
        )
        if field_match2:
            return stripped

        # Not a valid field — this is junk. Remove up to next comma.
        # Handle parenthetical expressions: Word (text),
        junk_match = re.match(
            r'^[^,={}]+(?:\([^)]*\))?\s*,?\s*', stripped
        )
        if junk_match:
            text = stripped[junk_match.end():]
        else:
            # Can't parse further — return what we have
            break

    return text


def sanitize_all_bib_files(
    project_dir: str,
    verbose: bool = True,
) -> Dict[str, Dict[str, Any]]:
    """Find and sanitize all .bib files in a project directory.

    Args:
        project_dir: Root directory to search for .bib files.
        verbose: Print progress.

    Returns:
        Dictionary mapping bib file paths to their sanitization stats.
    """
    results = {}
    for root, _dirs, files in os.walk(project_dir):
        for fname in files:
            if fname.endswith('.bib'):
                bib_path = os.path.join(root, fname)
                if verbose:
                    print(f"\nSanitizing: {bib_path}")
                results[bib_path] = sanitize_bib_file(bib_path, verbose=verbose)
    return results


# ── CLI entry point ──────────────────────────────────────────────────────────

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m utils.bib_sanitizer <path-to-.bib-file-or-directory>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isfile(target) and target.endswith('.bib'):
        sanitize_bib_file(target, verbose=True)
    elif os.path.isdir(target):
        sanitize_all_bib_files(target, verbose=True)
    else:
        print(f"Error: {target} is not a .bib file or directory")
        sys.exit(1)
