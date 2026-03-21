#!/usr/bin/env python3
"""Standalone LaTeX post-processing pipeline for SE papers.

Runs a 13-step automated cleanup pipeline on a compiled paper directory,
followed by an optional visual overflow check using Claude's vision via
the Claude Agent SDK (inherits credentials from the calling process).

Pipeline steps:
  1.  Renumber Finding entries in \\mybox{} blocks
  2.  Normalize SubRQ subsection titles
  2b. Strip \\paragraph{} commands
  3.  Add RQ labels to section/subsection headers
  4.  Sanitize BibTeX (fix syntax, deduplicate, replace non-ASCII)
  5.  Normalize citation keys to alphabetical-only format
  6.  Fix nested citation commands
  7.  Sanitize stray characters in \\cite{} keys
  8.  Remove dangling citation keys (no matching .bib entry)
  9.  Validate and strip broken TikZ figures
  10. Visual validation of TikZ via Claude Vision (opt-in)
  11. Wrap TikZ in \\resizebox to prevent overflow
  12. Final citation cross-check (cited keys vs .bib entries)
  13. Check and auto-fix LaTeX syntax errors

Then optionally:
  14. Visual overflow check of compiled PDF pages via Claude Vision

Usage:
    python postprocess_paper.py /path/to/paper/dir
    python postprocess_paper.py /path/to/paper/dir --visual
    python postprocess_paper.py /path/to/paper/dir --visual --recompile
    python postprocess_paper.py /path/to/paper/dir --bib references.bib
    python postprocess_paper.py /path/to/paper/dir --main main.tex

Requires:
    - research_agency.tex_postprocess (for steps 1-13)
    - claude_agent_sdk (for visual checks, opt-in)
    - PyMuPDF (pip install PyMuPDF, for visual checks)
    - pdflatex (for TikZ validation and recompilation)
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Allow running standalone from the scripts/ directory.
# First try the local bundled copy (tex_postprocess/ next to this script),
# then fall back to the repo-level research_agency package.
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

try:
    from tex_postprocess.post_process import post_process_tex_files
except ImportError:
    _repo_root = Path(__file__).resolve().parents[3]
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))
    from research_agency.tex_postprocess.post_process import post_process_tex_files


def _find_bib(paper_dir: Path) -> str | None:
    """Auto-discover the .bib file in a paper directory."""
    bib_files = list(paper_dir.glob("*.bib"))
    if len(bib_files) == 1:
        return str(bib_files[0])
    for b in bib_files:
        if b.name in ("references.bib", "refs.bib", "bibliography.bib"):
            return str(b)
    return str(bib_files[0]) if bib_files else None


def _find_sections_dir(paper_dir: Path) -> str:
    """Find the sections/ directory containing .tex files."""
    sections = paper_dir / "sections"
    if sections.is_dir():
        return str(sections)
    return str(paper_dir)


def _find_main_tex(paper_dir: Path) -> str | None:
    """Find the main .tex file."""
    main = paper_dir / "main.tex"
    if main.is_file():
        return str(main)
    for f in paper_dir.glob("*.tex"):
        content = f.read_text(errors="ignore")[:500]
        if "\\documentclass" in content:
            return str(f)
    return None


def _recompile_latex(paper_dir: Path, main_tex: str) -> bool:
    """Recompile LaTeX (pdflatex + bibtex + 2x pdflatex)."""
    tex_name = Path(main_tex).stem
    cmds = [
        ["pdflatex", "-interaction=nonstopmode", main_tex],
        ["bibtex", tex_name],
        ["pdflatex", "-interaction=nonstopmode", main_tex],
        ["pdflatex", "-interaction=nonstopmode", main_tex],
    ]
    for cmd in cmds:
        result = subprocess.run(
            cmd, cwd=str(paper_dir), capture_output=True, timeout=120
        )
        # bibtex may warn; only fail on pdflatex errors
        if cmd[0] == "pdflatex" and result.returncode != 0:
            print(f"  Compilation failed: {' '.join(cmd)}")
            return False
    return True


def _run_visual_check(paper_dir: Path, main_tex: str, max_iterations: int = 3) -> dict:
    """Run the visual overflow check using check_visual_overflow.py as subprocess.

    Uses the Claude Agent SDK with credentials inherited from the calling process.
    """
    check_script = Path(__file__).parent / "check_visual_overflow.py"
    if not check_script.exists():
        print(f"  ⚠️  Visual checker not found: {check_script}")
        return {"skipped": True, "reason": "script not found"}

    cmd = [
        sys.executable,
        str(check_script),
        str(paper_dir),
        "--main-tex", main_tex,
        "--max-iterations", str(max_iterations),
    ]

    print(f"\n{'='*60}")
    print("Step 14: Visual overflow check (Claude Vision via Agent SDK)")
    print("-" * 60)
    print(f"  Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(paper_dir),
            timeout=600,  # 10 min max for visual checks
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        print("  ⚠️  Visual check timed out (10 min)")
        return {"success": False, "reason": "timeout"}
    except Exception as e:
        print(f"  ⚠️  Visual check failed: {e}")
        return {"success": False, "reason": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Post-process LaTeX paper: BibTeX sanitization, citation normalization, "
        "TikZ validation, syntax checking, and optional visual overflow check."
    )
    parser.add_argument("paper_dir", help="Path to the paper directory")
    parser.add_argument(
        "--bib", default=None, help="Path to .bib file (auto-detected if omitted)"
    )
    parser.add_argument(
        "--main", default=None, help="Path to main .tex file (auto-detected if omitted)"
    )
    parser.add_argument(
        "--visual",
        action="store_true",
        help="Enable visual overflow check via Claude Vision (uses Agent SDK credentials)",
    )
    parser.add_argument(
        "--visual-tikz",
        action="store_true",
        help="Enable TikZ visual validation via Claude Vision (step 10)",
    )
    parser.add_argument(
        "--recompile",
        action="store_true",
        help="Recompile LaTeX after postprocessing (before visual check)",
    )
    parser.add_argument(
        "--max-visual-iterations",
        type=int,
        default=3,
        help="Max fix-recompile iterations for visual check (default: 3)",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress verbose output"
    )
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    if not paper_dir.is_dir():
        print(f"Error: {paper_dir} is not a directory")
        sys.exit(1)

    # Auto-discover paths
    bib_path = args.bib or _find_bib(paper_dir)
    main_tex_path = args.main or _find_main_tex(paper_dir)
    sections_dir = _find_sections_dir(paper_dir)
    main_tex_name = Path(main_tex_path).name if main_tex_path else "main.tex"

    if not args.quiet:
        print(f"Paper directory: {paper_dir}")
        print(f"Sections dir:    {sections_dir}")
        print(f"BibTeX file:     {bib_path or '(none found)'}")
        print(f"Main .tex:       {main_tex_path or '(none found)'}")
        print(f"Visual check:    {'enabled' if args.visual else 'disabled'}")
        print(f"TikZ visual:     {'enabled' if args.visual_tikz else 'disabled'}")
        print(f"Recompile:       {'yes' if args.recompile else 'no'}")
        print()

    # ── Steps 1-13: Deterministic postprocessing ──────────────────────
    results = post_process_tex_files(
        tex_dir=sections_dir,
        bib_path=bib_path,
        main_tex_path=main_tex_path,
        verbose=not args.quiet,
        visual_check_tikz=args.visual_tikz,
    )

    print("\n[POST-PROCESS] Steps 1-13 complete")

    # Count remaining errors
    tex_errors = sum(
        len(errors)
        for errors in results.get("tex_checks", {}).get("directory", {}).values()
    )

    # ── Recompile if requested ────────────────────────────────────────
    if args.recompile and main_tex_path:
        print(f"\n{'='*60}")
        print("Recompiling LaTeX after postprocessing...")
        print("-" * 60)
        if _recompile_latex(paper_dir, main_tex_name):
            print("  ✅ Recompilation successful")
        else:
            print("  ⚠️  Recompilation had errors (check log)")

    # ── Step 14: Visual overflow check (optional, uses Claude SDK) ────
    visual_result = {}
    if args.visual and main_tex_path:
        visual_result = _run_visual_check(
            paper_dir, main_tex_name, args.max_visual_iterations
        )

    # ── Final summary ─────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("POSTPROCESS SUMMARY")
    print(f"{'='*60}")

    if tex_errors > 0:
        print(f"  LaTeX syntax: ⚠️  {tex_errors} error(s) remaining")
    else:
        print("  LaTeX syntax: ✅ clean")

    bib_san = results.get("bib_sanitized", {})
    if bib_san and "error" not in bib_san:
        fixes = (
            bib_san.get("duplicates_removed", 0)
            + bib_san.get("extra_ids_removed", 0)
            + bib_san.get("non_ascii_replaced", 0)
        )
        print(f"  BibTeX: {fixes} fix(es) applied")

    cit = results.get("citations_normalized", {})
    if cit.get("bib_updates", 0) > 0:
        print(f"  Citations: {cit['bib_updates']} key(s) normalized")

    crosscheck = results.get("citation_crosscheck", {})
    missing = crosscheck.get("missing_keys", set())
    if missing:
        print(f"  Cross-check: ⚠️  {len(missing)} dangling key(s) removed")
    else:
        print("  Cross-check: ✅ all cited keys in .bib")

    if visual_result:
        if visual_result.get("success"):
            print("  Visual check: ✅ clean")
        elif visual_result.get("skipped"):
            print(f"  Visual check: skipped ({visual_result.get('reason', '?')})")
        else:
            print(f"  Visual check: ⚠️  issues remain")

    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
