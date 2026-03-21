"""Visual validation and iterative fixing of TikZ figures using Claude Code CLI.

Compiles each tikzpicture block to PNG, pipes it to `claude --print` for
visual inspection, and if issues are found, asks Claude to rewrite the TikZ
code. The cycle repeats until the figure passes or max iterations are reached.

Requires:
  - pdflatex on PATH
  - pdftoppm on PATH (poppler-utils)
  - claude CLI on PATH (Claude Code SDK)

Usage:
    python -m tex_postprocess.tikz_visual_validator <tex_directory> [--fix] [--model sonnet]
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Tuple

from .post_process import _TIKZ_PREAMBLE, _TIKZ_POSTAMBLE

_TIKZ_BLOCK_RE = re.compile(
    r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})',
    re.DOTALL,
)

_VISION_PROMPT = """\
You are a strict visual quality inspector for TikZ diagrams in academic papers.
Examine this rendered diagram image carefully and report ANY of these issues:

1. OVERLAPPING BOXES: Any boxes, nodes, or containers whose borders or content
   overlap each other, even partially. Content should never be hidden.
2. TEXT CLIPPING: ANY text that is cut off, truncated, or extends beyond its
   containing box. Even a single clipped character counts. Look carefully at
   every box — if text touches or crosses a box border, that is clipping.
3. ARROW COLLISIONS: Arrows or lines passing through unrelated nodes/boxes.
4. OVERCROWDING: Elements so close together that labels overlap or are hard to
   distinguish from neighboring elements.
5. MISALIGNMENT: Elements that should be aligned (e.g., in a row or column)
   but are visibly offset.
6. TINY TEXT: Any text that is too small to read comfortably at normal viewing
   size. Common signs: dense paragraphs or long sentences crammed into boxes
   using \\footnotesize, \\scriptsize, or \\tiny; text that would be unreadable
   when printed. Figures should use SHORT labels and keywords (not full
   sentences). If a box contains more than ~10-15 words it is almost certainly
   too verbose. Flag it even when the text technically fits inside its box.

Be strict. If you see ANY text clipping, overlapping, or tiny/dense text, report it.
Zoom in mentally on each box and verify all text fits within its borders AND
is large enough to read easily.

Return ONLY a JSON object (no markdown fences):
{"has_issues": true/false, "issues": [{"type": "text_clipping", "description": "The Memory/Caching box has truncated text"}], "severity": "none"|"warning"|"error", "summary": "one sentence"}
"""

_FIX_PROMPT_TEMPLATE = """\
The following TikZ code produces a diagram with visual issues.
Fix the TikZ code so that all text fits inside boxes, nothing overlaps,
and the layout is clean and readable.

ISSUES FOUND:
{issues}

CURRENT TIKZ CODE:
```latex
{tikz_code}
```

Rules:
- Use `text width=` instead of `minimum width=` to prevent text clipping
- Use absolute (x,y) coordinates to prevent overlap from relative positioning
- Make boxes wide enough for their content
- For TINY TEXT issues: shorten verbose labels to concise keywords or short
  phrases (max ~10 words per box). Use \\small or \\footnotesize at most —
  NEVER \\scriptsize or \\tiny. Replace full sentences with bullet-style
  keywords. A figure should communicate structure, not reproduce paragraphs.
- Do NOT change the semantic content (labels, structure, meaning)
- Keep the same color scheme and style names
- Return ONLY the fixed tikzpicture block (from \\begin{{tikzpicture}} to \\end{{tikzpicture}}), no explanation
"""


def _static_check_tiny_text(block: str) -> List[Dict[str, str]]:
    """Static analysis: detect nodes with too many words or tiny font commands.

    Returns a list of issue dicts (same format as vision issues).
    """
    issues: List[Dict[str, str]] = []

    # Check for tiny font commands
    tiny_fonts = re.findall(r'\\(tiny|scriptsize)\b', block)
    if tiny_fonts:
        issues.append({
            "type": "tiny_text",
            "description": (
                f"Figure uses very small font command(s): "
                f"{', '.join(set(tiny_fonts))}. "
                "Use \\small or \\footnotesize at most."
            ),
        })

    # Check for verbose node text (extract text from node definitions)
    # Match node content: node[...]{TEXT} or node{TEXT}
    # Also match standalone {TEXT} blocks after node declarations
    node_texts = re.findall(
        r'(?:node\s*(?:\[[^\]]*\])?\s*(?:\([^)]*\))?\s*)\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',
        block,
    )

    for text in node_texts:
        # Strip LaTeX commands to get approximate word count
        clean = re.sub(r'\\[a-zA-Z]+\s*(?:\{[^}]*\}|\[[^\]]*\])?', ' ', text)
        clean = re.sub(r'[{}\\$]', ' ', clean)
        clean = re.sub(r'\\\\', ' ', clean)   # line breaks
        words = [w for w in clean.split() if len(w) >= 2]

        if len(words) > 25:
            snippet = ' '.join(words[:8]) + '...'
            issues.append({
                "type": "tiny_text",
                "description": (
                    f"Node has {len(words)} words (max ~25 recommended): "
                    f"\"{snippet}\". Shorten to concise keywords."
                ),
            })

    return issues


def _extract_tikz_blocks(content: str) -> List[Tuple[int, int, str]]:
    """Extract all tikzpicture blocks from a string."""
    return [(m.start(), m.end(), m.group(1)) for m in _TIKZ_BLOCK_RE.finditer(content)]


def _compile_tikz_to_png(
    block: str, tmpdir: str, dpi: int = 300
) -> Optional[str]:
    """Compile a TikZ block to PDF then convert to PNG.

    Returns path to the PNG file, or None on failure.
    """
    tex_content = _TIKZ_PREAMBLE + block + _TIKZ_POSTAMBLE
    tex_path = os.path.join(tmpdir, "figure.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
        cwd=tmpdir,
        capture_output=True,
        timeout=30,
    )
    pdf_path = os.path.join(tmpdir, "figure.pdf")
    if result.returncode != 0 or not os.path.isfile(pdf_path):
        return None

    png_prefix = os.path.join(tmpdir, "figure")
    subprocess.run(
        ["pdftoppm", "-png", "-singlefile", "-r", str(dpi), pdf_path, png_prefix],
        capture_output=True,
        timeout=30,
    )
    png_path = f"{png_prefix}.png"
    if os.path.isfile(png_path):
        return png_path
    return None


def _check_image_with_claude_cli(
    png_path: str, model: str = "sonnet"
) -> Dict[str, Any]:
    """Pipe a PNG image to `claude --print` and parse the JSON response."""
    with open(png_path, "rb") as f:
        image_bytes = f.read()

    result = subprocess.run(
        [
            "claude",
            "--print",
            "--model", model,
            "--allowedTools", "",
            _VISION_PROMPT,
        ],
        input=image_bytes,
        capture_output=True,
        timeout=120,
    )

    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace")[:200]
        return {
            "has_issues": False,
            "issues": [],
            "severity": "unknown",
            "summary": f"claude CLI error: {stderr}",
        }

    raw = result.stdout.decode("utf-8", errors="replace").strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    # Try to extract JSON from the response
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    return {
        "has_issues": False,
        "issues": [],
        "severity": "unknown",
        "summary": f"Could not parse response: {raw[:200]}",
    }


def _fix_tikz_with_claude_cli(
    tikz_code: str, issues: List[Dict[str, str]], model: str = "sonnet"
) -> Optional[str]:
    """Ask Claude to fix a TikZ block given the visual issues found.

    Returns the fixed tikzpicture block, or None on failure.
    """
    issues_text = "\n".join(
        f"- {iss.get('type', '?')}: {iss.get('description', '')}"
        for iss in issues
    )
    prompt = _FIX_PROMPT_TEMPLATE.format(issues=issues_text, tikz_code=tikz_code)

    result = subprocess.run(
        [
            "claude",
            "--print",
            "--model", model,
            "--allowedTools", "",
            prompt,
        ],
        capture_output=True,
        timeout=180,
    )

    if result.returncode != 0:
        return None

    raw = result.stdout.decode("utf-8", errors="replace").strip()

    # Extract tikzpicture block from response
    m = re.search(
        r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})',
        raw,
        re.DOTALL,
    )
    if m:
        return m.group(1)
    return None


def _validate_and_fix_block(
    block: str,
    label: str,
    model: str = "sonnet",
    max_iterations: int = 3,
    dpi: int = 300,
    verbose: bool = True,
) -> Tuple[str, Dict[str, Any], bool]:
    """Validate a TikZ block and iteratively fix it until it passes.

    Returns:
        (final_block, check_result, was_fixed)
    """
    current_block = block

    for iteration in range(max_iterations):
        with tempfile.TemporaryDirectory() as tmpdir:
            png_path = _compile_tikz_to_png(current_block, tmpdir, dpi=dpi)
            if png_path is None:
                if verbose:
                    print(f"SKIP (compile failed at iteration {iteration})")
                return current_block, {"has_issues": False, "summary": "compile failed"}, False

            check = _check_image_with_claude_cli(png_path, model=model)

        # Merge static tiny-text analysis into the vision check
        static_issues = _static_check_tiny_text(current_block)
        if static_issues:
            check.setdefault("issues", []).extend(static_issues)
            check["has_issues"] = True
            if check.get("severity") == "none":
                check["severity"] = "warning"

        if not check.get("has_issues", False):
            if iteration == 0:
                if verbose:
                    print("OK")
            else:
                if verbose:
                    print(f"FIXED (after {iteration} iteration(s))")
            return current_block, check, iteration > 0

        # Issues found — attempt fix
        issues = check.get("issues", [])
        if verbose:
            suffix = f" (iteration {iteration + 1}/{max_iterations})"
            if iteration == 0:
                print(f"ISSUES FOUND{suffix}")
            else:
                print(f"    Still has issues{suffix}")
            for iss in issues:
                print(f"    - {iss.get('type', '?')}: {iss.get('description', '')}")

        if iteration < max_iterations - 1:
            if verbose:
                print(f"    Asking Claude to fix...", end=" ", flush=True)
            fixed = _fix_tikz_with_claude_cli(current_block, issues, model=model)
            if fixed is None:
                if verbose:
                    print("fix failed, keeping original")
                return current_block, check, False
            # Verify the fix compiles before accepting it
            with tempfile.TemporaryDirectory() as tmpdir2:
                if _compile_tikz_to_png(fixed, tmpdir2, dpi=dpi) is not None:
                    current_block = fixed
                    if verbose:
                        print("got fix, re-checking...")
                else:
                    if verbose:
                        print("fix doesn't compile, keeping previous version")
                    return current_block, check, False

    # Exhausted iterations
    if verbose:
        print(f"    Max iterations reached, issues remain")
    return current_block, check, current_block != block


def check_tikz_figures_in_directory(
    tex_dir: str,
    verbose: bool = True,
    model: str = "sonnet",
    max_figures: int = 50,
    dpi: int = 300,
    auto_fix: bool = False,
    max_fix_iterations: int = 3,
) -> Dict[str, Any]:
    """Visually validate all TikZ figures in a directory using Claude Vision.

    Args:
        tex_dir: Directory containing .tex files
        verbose: Print progress
        model: Claude model name (sonnet, opus, haiku)
        max_figures: Safety cap on number of figures to check
        dpi: Render resolution
        auto_fix: If True, attempt to fix figures that fail validation
        max_fix_iterations: Max fix-check cycles per figure

    Returns:
        Report dict with total_figures_checked, figures_with_issues, details.
    """
    # -- prerequisite checks --
    if not shutil.which("pdflatex"):
        if verbose:
            print("  Skipping visual check: pdflatex not found on PATH")
        return {"skipped_reason": "pdflatex not available"}

    if not shutil.which("pdftoppm"):
        if verbose:
            print("  Skipping visual check: pdftoppm not found on PATH")
        return {"skipped_reason": "pdftoppm not available"}

    if not shutil.which("claude"):
        if verbose:
            print("  Skipping visual check: claude CLI not found on PATH")
        return {"skipped_reason": "claude CLI not available"}

    # -- collect all tikz blocks across files --
    figures: List[Tuple[str, int, str]] = []
    tex_files = sorted(f for f in os.listdir(tex_dir) if f.endswith(".tex"))

    for tex_file in tex_files:
        file_path = os.path.join(tex_dir, tex_file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue
        blocks = _extract_tikz_blocks(content)
        for idx, (_, _, block_text) in enumerate(blocks):
            figures.append((tex_file, idx, block_text))

    if not figures:
        if verbose:
            print("  No TikZ figures found")
        return {"total_figures_checked": 0, "figures_with_issues": 0, "details": {}}

    if verbose:
        print(f"  Found {len(figures)} TikZ figure(s) across {len(tex_files)} file(s)")
        if auto_fix:
            print(f"  Auto-fix enabled (max {max_fix_iterations} iterations per figure)")

    if len(figures) > max_figures:
        if verbose:
            print(f"  Capping at {max_figures} figures (safety limit)")
        figures = figures[:max_figures]

    # -- compile, render, check (and optionally fix) each figure --
    report: Dict[str, Any] = {
        "total_figures_checked": 0,
        "figures_with_issues": 0,
        "figures_ok": 0,
        "figures_fixed": 0,
        "skipped_compile_fail": 0,
        "details": {},
    }

    for i, (tex_file, block_idx, block_text) in enumerate(figures, 1):
        label = f"{tex_file} (figure {block_idx + 1})"
        if verbose:
            print(f"  [{i}/{len(figures)}] Checking {label}...", end=" ", flush=True)

        if auto_fix:
            final_block, result, was_fixed = _validate_and_fix_block(
                block_text, label, model=model,
                max_iterations=max_fix_iterations, dpi=dpi, verbose=verbose,
            )

            if was_fixed:
                # Write the fix back to the file
                file_path = os.path.join(tex_dir, tex_file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    # Replace the original block with the fixed one
                    file_content = file_content.replace(block_text, final_block)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(file_content)
                    report["figures_fixed"] += 1
                    if verbose:
                        print(f"    Written fix to {tex_file}")
                except Exception as e:
                    if verbose:
                        print(f"    Failed to write fix: {e}")
        else:
            # Check-only mode
            with tempfile.TemporaryDirectory() as tmpdir:
                png_path = _compile_tikz_to_png(block_text, tmpdir, dpi=dpi)
                if png_path is None:
                    report["skipped_compile_fail"] += 1
                    if verbose:
                        print("SKIP (compile failed)")
                    continue
                try:
                    result = _check_image_with_claude_cli(png_path, model=model)
                except Exception as e:
                    if verbose:
                        print(f"ERROR ({e})")
                    continue

            # Merge static tiny-text analysis
            static_issues = _static_check_tiny_text(block_text)
            if static_issues:
                result.setdefault("issues", []).extend(static_issues)
                result["has_issues"] = True
                if result.get("severity") == "none":
                    result["severity"] = "warning"

            has_issues = result.get("has_issues", False)
            if has_issues:
                if verbose:
                    print("ISSUES FOUND")
                    for iss in result.get("issues", []):
                        print(f"    - {iss.get('type', '?')}: {iss.get('description', '')}")
            else:
                if verbose:
                    print("OK")

        report["total_figures_checked"] += 1
        has_issues = result.get("has_issues", False)
        if has_issues:
            report["figures_with_issues"] += 1
        else:
            report["figures_ok"] += 1

        report["details"].setdefault(tex_file, []).append(
            {"block_index": block_idx, **result}
        )

    if verbose:
        print(
            f"\n  Visual check summary: {report['figures_with_issues']} issue(s) "
            f"in {report['total_figures_checked']} figure(s) checked"
        )
        if auto_fix and report["figures_fixed"] > 0:
            print(f"  Auto-fixed {report['figures_fixed']} figure(s)")

    return report


if __name__ == "__main__":
    import sys

    usage = (
        "Usage: python -m utils.tikz_visual_validator <tex_directory> [--fix] [--model MODEL]\n"
        "  --fix    Attempt to auto-fix figures with issues (iterative loop)\n"
        "  --model  Claude model to use (default: sonnet)"
    )

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(usage)
        sys.exit(0 if sys.argv[1:] == ["--help"] else 1)

    target = sys.argv[1]
    auto_fix = "--fix" in sys.argv
    cli_model = "sonnet"
    for j, arg in enumerate(sys.argv):
        if arg == "--model" and j + 1 < len(sys.argv):
            cli_model = sys.argv[j + 1]

    if os.path.isdir(target):
        check_tikz_figures_in_directory(
            target, verbose=True, model=cli_model, auto_fix=auto_fix,
        )
    else:
        print(f"Error: {target} is not a directory")
        sys.exit(1)
