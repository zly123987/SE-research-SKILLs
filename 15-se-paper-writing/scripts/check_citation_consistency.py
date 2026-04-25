#!/usr/bin/env python3
"""Comprehensive citation checker: consistency, missing citations, and semantic verification.

Three checks:
  1. Context consistency (deterministic): Author name and year match between prose and BibTeX
  2. Missing citations (deterministic): Entities in prose that should have \\cite{} or \\url{}
  3. Semantic consistency (LLM-based): Does the prose claim match the cited paper's title?

Usage:
    # All deterministic checks (no API calls)
    python check_citation_consistency.py /path/to/paper/dir --level deterministic

    # Full check including LLM semantic verification
    python check_citation_consistency.py /path/to/paper/dir

    # LLM semantic check only
    python check_citation_consistency.py /path/to/paper/dir --level semantic

Requires for LLM checks: claude-agent-sdk (pip install claude-agent-sdk)
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Allow running standalone from the scripts/ directory
_script_dir = Path(__file__).resolve().parent
_postprocess_dir = _script_dir / "tex_postprocess"
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

from tex_postprocess.citation_context_checker import (
    check_citation_context_consistency,
    format_contexts_for_llm,
)
from tex_postprocess.missing_citation_checker import (
    check_missing_citations,
)


def _find_paper_files(paper_dir: Path) -> tuple:
    """Locate bib, tex dir, and main.tex in a paper directory."""
    bib_files = list(paper_dir.glob("*.bib"))
    bib_path = str(bib_files[0]) if bib_files else None

    # Look for sections/ subdirectory
    sections_dir = paper_dir / "sections"
    tex_dir = str(sections_dir) if sections_dir.is_dir() else str(paper_dir)

    # Look for main.tex
    main_tex = paper_dir / "main.tex"
    main_tex_path = str(main_tex) if main_tex.is_file() else None

    return bib_path, tex_dir, main_tex_path


async def _semantic_check(
    contexts: list,
    batch_size: int = 12,
) -> list:
    """Run LLM-based semantic consistency check on citation contexts.

    Sends batches of citation contexts to Claude and asks it to verify
    that the prose description is consistent with the cited paper's title
    and metadata.

    Returns:
        List of flagged inconsistencies.
    """
    try:
        from claude_agent_sdk import Agent
    except ImportError:
        try:
            from anthropic import Anthropic
        except ImportError:
            print(
                "ERROR: Neither claude-agent-sdk nor anthropic SDK found.\n"
                "Install with: pip install claude-agent-sdk\n"
                "Or run with --level deterministic to skip LLM checks."
            )
            return []

    if not contexts:
        return []

    flagged = []

    # Process in batches
    for i in range(0, len(contexts), batch_size):
        batch = contexts[i : i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(contexts) + batch_size - 1) // batch_size
        print(f"  Checking batch {batch_num}/{total_batches} "
              f"({len(batch)} citations)...")

        prompt = _build_semantic_prompt(batch)

        try:
            # Try claude-agent-sdk first
            try:
                from claude_agent_sdk import Agent

                agent = Agent(
                    model="claude-sonnet-4-20250514",
                    system="You are a citation consistency checker for academic papers. "
                           "Respond ONLY with valid JSON, no other text.",
                )
                response = await agent.run(prompt)
                response_text = response.text if hasattr(response, "text") else str(response)
            except (ImportError, Exception):
                # Fall back to anthropic SDK
                from anthropic import Anthropic

                client = Anthropic()
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2048,
                    system="You are a citation consistency checker for academic papers. "
                           "Respond ONLY with valid JSON, no other text.",
                    messages=[{"role": "user", "content": prompt}],
                )
                response_text = message.content[0].text

            # Parse JSON response
            results = _parse_llm_response(response_text)
            for result in results:
                if not result.get("consistent", True):
                    result["batch"] = batch_num
                    flagged.append(result)

        except Exception as e:
            print(f"  WARNING: Batch {batch_num} failed: {e}")
            continue

    return flagged


def _build_semantic_prompt(batch: list) -> str:
    """Build the prompt for semantic citation checking."""
    lines = [
        "For each citation below, check if the prose description is semantically "
        "consistent with the cited paper's title and author metadata.\n",
        "Flag ONLY clear mismatches — cases where the prose makes a specific claim "
        "about the cited work that contradicts the paper's title or attributes it "
        "to wrong authors. Do NOT flag generic citations like "
        "\"prior work~\\cite{key}\" where no specific claim is made.\n",
        "Respond with a JSON array. For each citation:\n"
        '  {"key": "...", "consistent": true/false, "issue": "explanation if false"}\n',
    ]

    for idx, ctx in enumerate(batch, 1):
        lines.append(f"--- Citation {idx} ---")
        lines.append(f"Key: {ctx['key']}")
        lines.append(f"Authors (last names): {ctx['authors']}")
        lines.append(f"Year: {ctx['year']}")
        lines.append(f"Title: {ctx['title']}")
        lines.append(f"Prose context: {ctx['prose']}")
        lines.append(f"File: {ctx['file']}:{ctx['line']}")
        lines.append("")

    return "\n".join(lines)


def _parse_llm_response(text: str) -> list:
    """Parse JSON array from LLM response, handling markdown fences."""
    text = text.strip()
    # Strip markdown code fences
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
    if text.endswith("```"):
        text = text[: text.rfind("```")]
    text = text.strip()

    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
        return [result]
    except json.JSONDecodeError:
        # Try to find JSON array in the text
        match = __import__("re").search(r"\[.*\]", text, __import__("re").DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return []


def _print_report(
    deterministic_result: dict,
    missing_result: dict,
    semantic_flags: list,
    level: str,
):
    """Print a combined report."""
    print(f"\n{'=' * 60}")
    print("Citation Consistency Report")
    print(f"{'=' * 60}")

    total_issues = 0

    if level in ("deterministic", "all"):
        author_n = deterministic_result.get("author_mismatches", 0)
        year_n = deterministic_result.get("year_mismatches", 0)
        checked = deterministic_result.get("citations_checked", 0)
        total_issues += author_n + year_n

        print(f"\n[Check 1] Context Consistency ({checked} citations)")
        print(f"  Author mismatches: {author_n}")
        print(f"  Year mismatches:   {year_n}")

    if level in ("deterministic", "all") and missing_result:
        missing_n = missing_result.get("total", 0)
        total_issues += missing_n

        print(f"\n[Check 2] Missing Citations")
        print(f"  Uncited entities: {missing_n}")
        by_cat = missing_result.get("by_category", {})
        if by_cat:
            for cat, count in sorted(by_cat.items()):
                print(f"    {cat}: {count}")

    if level in ("semantic", "all") and semantic_flags is not None:
        total_issues += len(semantic_flags)
        print(f"\n[Check 3] Semantic Consistency (LLM-based)")
        print(f"  Inconsistencies found: {len(semantic_flags)}")

        for flag in semantic_flags:
            print(f"\n  Key: {flag.get('key', '?')}")
            print(f"  Issue: {flag.get('issue', 'unknown')}")

    print(f"\n{'─' * 60}")
    if total_issues == 0:
        print("  All citation checks passed.")
    else:
        print(f"  Total issues: {total_issues}")
    print(f"{'=' * 60}")

    return total_issues


async def async_main(paper_dir: str, level: str = "all"):
    """Main async entry point."""
    paper_path = Path(paper_dir)
    if not paper_path.is_dir():
        print(f"ERROR: Not a directory: {paper_dir}")
        return 1

    bib_path, tex_dir, main_tex_path = _find_paper_files(paper_path)

    if not bib_path:
        print(f"ERROR: No .bib file found in {paper_dir}")
        return 1

    print(f"Paper directory: {paper_dir}")
    print(f"BibTeX file:     {bib_path}")
    print(f"TeX directory:   {tex_dir}")
    if main_tex_path:
        print(f"Main TeX:        {main_tex_path}")
    print()

    # Check 1: Context consistency (deterministic)
    deterministic_result = {}
    if level in ("deterministic", "all"):
        print("[Check 1] Running context consistency checks...")
        deterministic_result = check_citation_context_consistency(
            tex_dir, bib_path, main_tex_path=main_tex_path, verbose=True
        )

    # Check 2: Missing citations (deterministic)
    missing_result = {}
    if level in ("deterministic", "all"):
        print("\n[Check 2] Scanning for missing citations...")
        missing_result = check_missing_citations(
            tex_dir, main_tex_path=main_tex_path, verbose=True
        )

    # Check 3: Semantic consistency (LLM-based)
    semantic_flags = None
    if level in ("semantic", "all"):
        print("\n[Check 3] Running semantic checks (LLM-based)...")
        contexts = format_contexts_for_llm(
            tex_dir, bib_path, main_tex_path=main_tex_path
        )
        if contexts:
            semantic_flags = await _semantic_check(contexts)
        else:
            print("  No citation contexts to check.")
            semantic_flags = []

    total_issues = _print_report(
        deterministic_result, missing_result, semantic_flags, level
    )
    return 1 if total_issues > 0 else 0


def main():
    parser = argparse.ArgumentParser(
        description="Check citation usage consistency in LaTeX papers."
    )
    parser.add_argument(
        "paper_dir",
        help="Directory containing .bib and .tex files",
    )
    parser.add_argument(
        "--level",
        choices=["deterministic", "semantic", "all"],
        default="all",
        help="Check level: deterministic (no API), semantic (LLM only), all (default)",
    )

    args = parser.parse_args()
    exit_code = asyncio.run(async_main(args.paper_dir, level=args.level))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
