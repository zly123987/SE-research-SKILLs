#!/usr/bin/env python3
"""Standalone visual overflow checker for LaTeX papers.

Uses Claude's vision via the SDK to inspect each page of a compiled PDF
for text/table/figure overflow, then optionally applies fixes and recompiles.

Usage:
    python check_visual_overflow.py /path/to/paper/dir
    python check_visual_overflow.py /path/to/paper/dir --check-only
    python check_visual_overflow.py /path/to/paper/dir --max-iterations 5
    python check_visual_overflow.py /path/to/paper/dir --pages 1,3,7-10

Requires: PyMuPDF (pip install PyMuPDF), claude-agent-sdk
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Allow running standalone from the scripts/ directory
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from research_agency.paper_utils.visual_checker import (
    check_all_pages,
    pdf_to_images,
    visual_check_loop,
)


def _parse_pages(pages_str: str) -> list[int]:
    """Parse page spec like '1,3,5-7' into [1,3,5,6,7]."""
    pages: list[int] = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


async def _check_only(paper_dir: Path, main_tex: str, pages: list[int] | None):
    """Check and report issues without applying fixes."""
    import tempfile

    pdf_path = paper_dir / main_tex.replace(".tex", ".pdf")
    if not pdf_path.exists():
        print(f"ERROR: PDF not found: {pdf_path}")
        return 1

    with tempfile.TemporaryDirectory(prefix="visual_check_") as tmpdir:
        result = await check_all_pages(pdf_path, Path(tmpdir), pages=pages)

    if not result.issues:
        print("No visual issues found.")
        return 0

    print(f"\nFound {len(result.issues)} visual issues:\n")
    for iss in result.issues:
        sev_icon = {"critical": "!!!", "major": "!!", "minor": "!"}
        icon = sev_icon.get(iss.severity, "?")
        print(f"  [{icon}] Page {iss.page} — {iss.issue_type} ({iss.severity})")
        print(f"      {iss.description}")
        print(f"      Fix: {iss.suggested_fix}")
        print(f"      Hint: {iss.source_hint}")
        print()

    return len(result.issues)


def main():
    parser = argparse.ArgumentParser(
        description="Visual overflow checker for LaTeX papers (uses Claude vision)",
    )
    parser.add_argument("paper_dir", type=Path, help="Paper directory containing main.tex and compiled PDF")
    parser.add_argument("--main-tex", default="main.tex", help="Main .tex file name (default: main.tex)")
    parser.add_argument("--max-iterations", type=int, default=3, help="Max fix-recompile iterations (default: 3)")
    parser.add_argument("--check-only", action="store_true", help="Report issues without fixing")
    parser.add_argument("--pages", type=str, default=None, help="Specific pages to check (e.g., '1,3,5-7')")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")
    args = parser.parse_args()

    if not args.paper_dir.is_dir():
        print(f"ERROR: Not a directory: {args.paper_dir}")
        sys.exit(1)

    pages = _parse_pages(args.pages) if args.pages else None

    if args.check_only:
        n_issues = asyncio.run(_check_only(args.paper_dir, args.main_tex, pages))
        sys.exit(0 if n_issues == 0 else 1)

    result = asyncio.run(visual_check_loop(
        paper_dir=args.paper_dir,
        main_tex=args.main_tex,
        max_iterations=args.max_iterations,
        verbose=not args.quiet,
    ))

    # Summary
    print("\n" + "=" * 60)
    if result.get("success"):
        print(f"CLEAN: All pages pass visual check after {result['iterations']} iteration(s).")
    elif result.get("error"):
        print(f"ERROR: {result['error']}")
    else:
        remaining = result.get("remaining_issues", 0)
        print(f"REMAINING: {remaining} visual issues after {result['iterations']} iteration(s).")
        for detail in result.get("remaining_issues_detail", []):
            print(f"  Page {detail['page']}: {detail['type']} — {detail['description']}")
            print(f"    Suggested: {detail['suggested_fix']}")
    print("=" * 60)

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
