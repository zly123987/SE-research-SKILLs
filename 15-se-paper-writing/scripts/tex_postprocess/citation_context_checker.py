"""Citation context consistency checker.

Verifies that the way citations are used in prose matches the actual BibTeX
entries. Catches common errors:

1. Author name mismatch: "Wang et al.~\\cite{key}" but bib entry has no Wang
2. Year mismatch: "In 2023, X showed...~\\cite{key}" but bib year is 2021
3. Extracts citation contexts for optional LLM-based semantic checking

This module is stdlib-only (no external dependencies) and integrates into
the tex_postprocess pipeline as a report-only step (no auto-fix).
"""

import os
import re
from typing import Dict, Any, List, Optional, Tuple


# ── Data structures ──────────────────────────────────────────────────────────

class CitationContext:
    """A single citation usage in a .tex file."""

    __slots__ = ("key", "tex_file", "line_num", "sentence", "preceding_text")

    def __init__(
        self,
        key: str,
        tex_file: str,
        line_num: int,
        sentence: str,
        preceding_text: str,
    ):
        self.key = key
        self.tex_file = tex_file
        self.line_num = line_num
        self.sentence = sentence
        self.preceding_text = preceding_text

    def __repr__(self) -> str:
        return (
            f"CitationContext(key={self.key!r}, "
            f"file={os.path.basename(self.tex_file)}:{self.line_num})"
        )


class BibEntry:
    """Parsed metadata from a BibTeX entry."""

    __slots__ = ("key", "authors", "year", "title")

    def __init__(
        self,
        key: str,
        authors: List[str],
        year: str,
        title: str,
    ):
        self.key = key
        self.authors = authors  # list of last names (lowercase)
        self.year = year
        self.title = title


class Mismatch:
    """A detected inconsistency between citation usage and BibTeX entry."""

    __slots__ = (
        "key", "tex_file", "line_num", "mismatch_type",
        "text_value", "bib_value", "sentence",
    )

    def __init__(
        self,
        key: str,
        tex_file: str,
        line_num: int,
        mismatch_type: str,
        text_value: str,
        bib_value: str,
        sentence: str,
    ):
        self.key = key
        self.tex_file = tex_file
        self.line_num = line_num
        self.mismatch_type = mismatch_type  # "author" | "year"
        self.text_value = text_value
        self.bib_value = bib_value
        self.sentence = sentence

    def __repr__(self) -> str:
        return (
            f"Mismatch({self.mismatch_type}: "
            f"text={self.text_value!r} vs bib={self.bib_value!r}, "
            f"{os.path.basename(self.tex_file)}:{self.line_num})"
        )


# ── BibTeX parsing ───────────────────────────────────────────────────────────

_BIB_ENTRY_RE = re.compile(r"@\w+\{([^,]+),", re.MULTILINE)
_FIELD_RE = re.compile(
    r"^\s*(\w+)\s*=\s*[\{\"](.*?)[\}\"]",
    re.MULTILINE | re.DOTALL,
)


def parse_bib_entries(bib_path: str) -> Dict[str, BibEntry]:
    """Parse a .bib file and extract metadata for each entry.

    Returns:
        Dictionary mapping citation key -> BibEntry.
    """
    if not os.path.isfile(bib_path):
        return {}

    with open(bib_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    entries: Dict[str, BibEntry] = {}

    # Split into individual entries by finding @type{key, blocks
    entry_starts = list(_BIB_ENTRY_RE.finditer(content))

    for idx, match in enumerate(entry_starts):
        key = match.group(1).strip()
        start = match.start()
        end = entry_starts[idx + 1].start() if idx + 1 < len(entry_starts) else len(content)
        entry_text = content[start:end]

        # Extract fields
        fields: Dict[str, str] = {}
        for field_match in _FIELD_RE.finditer(entry_text):
            field_name = field_match.group(1).lower()
            field_value = field_match.group(2).strip()
            fields[field_name] = field_value

        authors = _extract_all_author_lastnames(fields.get("author", ""))
        year = fields.get("year", "").strip()
        title = fields.get("title", "").strip()
        # Clean LaTeX braces from title
        title = title.replace("{", "").replace("}", "")

        entries[key] = BibEntry(key=key, authors=authors, year=year, title=title)

    return entries


def _extract_all_author_lastnames(author_str: str) -> List[str]:
    """Extract all author last names from a BibTeX author field.

    Handles:
    - "Last, First and Last2, First2"
    - "First Last and First2 Last2"
    - Braced names: "{van der Berg}, Jan"
    - LaTeX accents: "\\'e" etc.

    Returns:
        List of lowercase last names.
    """
    if not author_str:
        return []

    # Remove LaTeX commands and braces for name extraction
    cleaned = re.sub(r"\\[a-zA-Z]+\{[^}]*\}", "", author_str)
    cleaned = re.sub(r"\\.", "", cleaned)
    cleaned = cleaned.replace("{", "").replace("}", "")

    # Split on " and " to get individual authors
    authors = re.split(r"\s+and\s+", cleaned)

    lastnames: List[str] = []
    for author in authors:
        author = author.strip()
        if not author:
            continue

        if "," in author:
            # Format: "Last, First"
            lastname = author.split(",")[0].strip()
        else:
            # Format: "First Last" or "First Middle Last"
            parts = author.split()
            if parts:
                lastname = parts[-1].strip()
            else:
                continue

        # Clean and lowercase
        lastname = re.sub(r"[^a-zA-Z]", "", lastname).lower()
        if lastname:
            lastnames.append(lastname)

    return lastnames


# ── Citation context extraction ──────────────────────────────────────────────

# Match \cite{...}, \citep{...}, \citet{...}, etc.
# Exclude \citet since it auto-generates author names (always correct)
_CITE_CMD_RE = re.compile(
    r"\\(cite[ps]?|citealp|citeauthor)\{([^}]+)\}"
)

# Commands where author names are auto-rendered (don't check these for author
# consistency since the style file generates the name from the bib entry)
_AUTO_AUTHOR_CMDS = {"citet", "citeauthor"}


def extract_citation_contexts(
    tex_dir: str,
    main_tex_path: Optional[str] = None,
) -> List[CitationContext]:
    """Extract all citation usages with surrounding context from .tex files.

    Returns:
        List of CitationContext objects.
    """
    contexts: List[CitationContext] = []
    tex_files: List[str] = []

    if os.path.isdir(tex_dir):
        for fname in os.listdir(tex_dir):
            if fname.endswith(".tex"):
                tex_files.append(os.path.join(tex_dir, fname))

    if main_tex_path and os.path.isfile(main_tex_path):
        if main_tex_path not in tex_files:
            tex_files.append(main_tex_path)

    for tex_path in sorted(tex_files):
        try:
            with open(tex_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except Exception:
            continue

        full_text = "".join(lines)

        for match in _CITE_CMD_RE.finditer(full_text):
            cmd = match.group(1)
            keys_str = match.group(2)
            cite_start = match.start()

            # Find line number
            line_num = full_text[:cite_start].count("\n") + 1

            # Extract surrounding sentence (~200 chars before and after)
            preceding_start = max(0, cite_start - 200)
            following_end = min(len(full_text), match.end() + 200)

            preceding_text = full_text[preceding_start:cite_start]
            sentence = full_text[preceding_start:following_end]

            # Clean LaTeX noise for readability
            sentence = _clean_latex_for_display(sentence)
            preceding_text = _clean_latex_for_display(preceding_text)

            # Split multi-key citations into individual contexts
            keys = [k.strip() for k in keys_str.split(",") if k.strip()]

            for key in keys:
                ctx = CitationContext(
                    key=key,
                    tex_file=tex_path,
                    line_num=line_num,
                    sentence=sentence,
                    preceding_text=preceding_text,
                )
                # Tag with the cite command for later filtering
                ctx._cmd = cmd  # type: ignore[attr-defined]
                contexts.append(ctx)

    return contexts


def _clean_latex_for_display(text: str) -> str:
    """Strip common LaTeX noise for readable display."""
    # Remove comments
    text = re.sub(r"%.*$", "", text, flags=re.MULTILINE)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ── Consistency checks ───────────────────────────────────────────────────────

# "Wang et al." or "Wang and Li" before a cite command
_AUTHOR_ET_AL_RE = re.compile(
    r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+et\s+al\.?",
)
_AUTHOR_AND_RE = re.compile(
    r"([A-Z][a-z]+)\s+and\s+([A-Z][a-z]+)",
)
# Year patterns near citations
_YEAR_IN_TEXT_RE = re.compile(
    r"(?:[Ii]n|[Ss]ince|[Ff]rom|[Aa]fter|[Bb]efore)\s+(\d{4})"
)
_YEAR_PAREN_RE = re.compile(r"\((\d{4})\)")


def check_author_consistency(
    context: CitationContext,
    bib_entry: BibEntry,
) -> Optional[Mismatch]:
    """Check if author names in prose match the BibTeX entry.

    Only checks when prose explicitly names an author near the citation.
    Skips \\citet and \\citeauthor (auto-generated names).
    """
    cmd = getattr(context, "_cmd", "cite")
    if cmd in _AUTO_AUTHOR_CMDS:
        return None

    # Only check the ~100 chars immediately before the \cite
    preceding = context.preceding_text[-100:] if len(context.preceding_text) > 100 else context.preceding_text

    # Look for "Author et al." pattern
    et_al_match = _AUTHOR_ET_AL_RE.search(preceding)
    if et_al_match:
        text_author = et_al_match.group(1).split()[-1].lower()  # last word
        if not _author_matches(text_author, bib_entry.authors):
            return Mismatch(
                key=context.key,
                tex_file=context.tex_file,
                line_num=context.line_num,
                mismatch_type="author",
                text_value=et_al_match.group(0),
                bib_value=", ".join(bib_entry.authors),
                sentence=context.sentence[:150],
            )

    # Look for "Author and Author" pattern
    and_match = _AUTHOR_AND_RE.search(preceding)
    if and_match:
        name1 = and_match.group(1).lower()
        name2 = and_match.group(2).lower()
        if (not _author_matches(name1, bib_entry.authors)
                and not _author_matches(name2, bib_entry.authors)):
            return Mismatch(
                key=context.key,
                tex_file=context.tex_file,
                line_num=context.line_num,
                mismatch_type="author",
                text_value=and_match.group(0),
                bib_value=", ".join(bib_entry.authors),
                sentence=context.sentence[:150],
            )

    return None


def _author_matches(text_name: str, bib_authors: List[str]) -> bool:
    """Check if a name from prose matches any author in the bib entry."""
    text_name = re.sub(r"[^a-z]", "", text_name.lower())
    if not text_name:
        return True  # can't check empty names

    for bib_author in bib_authors:
        bib_clean = re.sub(r"[^a-z]", "", bib_author.lower())
        # Exact match or prefix match (for abbreviated names)
        if text_name == bib_clean or bib_clean.startswith(text_name) or text_name.startswith(bib_clean):
            return True
    return False


def check_year_consistency(
    context: CitationContext,
    bib_entry: BibEntry,
) -> Optional[Mismatch]:
    """Check if a year mentioned near the citation matches the BibTeX year."""
    if not bib_entry.year:
        return None

    # Only check ~80 chars before the \cite
    preceding = context.preceding_text[-80:] if len(context.preceding_text) > 80 else context.preceding_text

    # Look for "In YYYY" style
    year_match = _YEAR_IN_TEXT_RE.search(preceding)
    if year_match:
        text_year = year_match.group(1)
        if text_year != bib_entry.year:
            return Mismatch(
                key=context.key,
                tex_file=context.tex_file,
                line_num=context.line_num,
                mismatch_type="year",
                text_value=text_year,
                bib_value=bib_entry.year,
                sentence=context.sentence[:150],
            )

    # Look for "(YYYY)" near the cite
    paren_match = _YEAR_PAREN_RE.search(preceding)
    if paren_match:
        text_year = paren_match.group(1)
        if text_year != bib_entry.year:
            return Mismatch(
                key=context.key,
                tex_file=context.tex_file,
                line_num=context.line_num,
                mismatch_type="year",
                text_value=text_year,
                bib_value=bib_entry.year,
                sentence=context.sentence[:150],
            )

    return None


# ── Main entry point ─────────────────────────────────────────────────────────

def check_citation_context_consistency(
    tex_dir: str,
    bib_path: str,
    main_tex_path: Optional[str] = None,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Check all citation usages for consistency with BibTeX entries.

    This is a report-only check — no files are modified.

    Args:
        tex_dir: Directory containing .tex files.
        bib_path: Path to .bib file.
        main_tex_path: Optional path to main.tex.
        verbose: Print progress and results.

    Returns:
        Dictionary with mismatches and statistics.
    """
    if verbose:
        print("Parsing BibTeX entries...")

    bib_entries = parse_bib_entries(bib_path)
    if not bib_entries:
        if verbose:
            print("  No BibTeX entries found. Skipping.")
        return {
            "citations_checked": 0,
            "author_mismatches": 0,
            "year_mismatches": 0,
            "mismatches": [],
        }

    if verbose:
        print(f"  Found {len(bib_entries)} BibTeX entries")
        print("Extracting citation contexts from .tex files...")

    contexts = extract_citation_contexts(tex_dir, main_tex_path)
    if verbose:
        print(f"  Found {len(contexts)} citation usages")

    mismatches: List[Dict[str, Any]] = []
    author_count = 0
    year_count = 0
    checked = 0

    for ctx in contexts:
        bib_entry = bib_entries.get(ctx.key)
        if bib_entry is None:
            continue  # dangling citation — handled by step 8

        checked += 1

        # Check author consistency
        author_mismatch = check_author_consistency(ctx, bib_entry)
        if author_mismatch:
            author_count += 1
            mismatches.append({
                "type": "author",
                "key": author_mismatch.key,
                "file": os.path.basename(author_mismatch.tex_file),
                "line": author_mismatch.line_num,
                "text_says": author_mismatch.text_value,
                "bib_says": author_mismatch.bib_value,
                "context": author_mismatch.sentence,
            })

        # Check year consistency
        year_mismatch = check_year_consistency(ctx, bib_entry)
        if year_mismatch:
            year_count += 1
            mismatches.append({
                "type": "year",
                "key": year_mismatch.key,
                "file": os.path.basename(year_mismatch.tex_file),
                "line": year_mismatch.line_num,
                "text_says": year_mismatch.text_value,
                "bib_says": year_mismatch.bib_value,
                "context": year_mismatch.sentence,
            })

    if verbose:
        print(f"\n  Citations checked: {checked}")
        print(f"  Author mismatches: {author_count}")
        print(f"  Year mismatches:   {year_count}")

        if mismatches:
            print(f"\n  {'─' * 50}")
            for m in mismatches:
                print(f"  [{m['type'].upper()}] {m['file']}:{m['line']}")
                print(f"    Key:      {m['key']}")
                print(f"    Text says: {m['text_says']}")
                print(f"    Bib says:  {m['bib_says']}")
                print(f"    Context:   {m['context'][:120]}...")
                print()
        else:
            print("  No mismatches found.")

    return {
        "citations_checked": checked,
        "author_mismatches": author_count,
        "year_mismatches": year_count,
        "mismatches": mismatches,
    }


def format_contexts_for_llm(
    tex_dir: str,
    bib_path: str,
    main_tex_path: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Export citation contexts with bib metadata for LLM-based semantic check.

    Returns a list of dicts suitable for batching into an LLM prompt:
        [{"key": ..., "prose": ..., "title": ..., "authors": ..., "year": ...,
          "file": ..., "line": ...}, ...]
    """
    bib_entries = parse_bib_entries(bib_path)
    contexts = extract_citation_contexts(tex_dir, main_tex_path)

    items: List[Dict[str, str]] = []
    for ctx in contexts:
        bib_entry = bib_entries.get(ctx.key)
        if bib_entry is None:
            continue

        items.append({
            "key": ctx.key,
            "prose": ctx.sentence[:250],
            "title": bib_entry.title,
            "authors": ", ".join(bib_entry.authors),
            "year": bib_entry.year,
            "file": os.path.basename(ctx.tex_file),
            "line": str(ctx.line_num),
        })

    return items


# ── CLI entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: python citation_context_checker.py <bib_file> <tex_directory> [main.tex]"
        )
        print("  Checks citation usage consistency against BibTeX entries")
        print("  Optional third arg: path to main.tex")
        sys.exit(1)

    bib_file = sys.argv[1]
    tex_directory = sys.argv[2]
    main_tex = sys.argv[3] if len(sys.argv) > 3 else None

    result = check_citation_context_consistency(
        tex_directory, bib_file, main_tex_path=main_tex, verbose=True
    )

    total = result["author_mismatches"] + result["year_mismatches"]
    sys.exit(1 if total > 0 else 0)
