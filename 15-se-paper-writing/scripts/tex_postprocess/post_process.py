"""Post-processing utilities for LaTeX files.

Groups all post-processing steps:
- Renumbering findings in \mybox{} blocks
- Normalizing SubRQ titles
- Ensuring \label{} tags exist for RQ sections/subsections
- Normalizing citation keys
- Fixing nested citation commands (e.g., \cite{\cite{key},other} -> \cite{key,other})
- AI wording detection and rewriting (em-dashes, leverage, utilize, etc.)
- Number consistency check (abstract/intro claims vs evaluation data)
- LaTeX grammar checking and auto-fixing (ALWAYS LAST)
"""

import os
from typing import Dict, Any, Optional
import re

from .tex_checker import check_tex_directory, fix_tex_file
from .fix_findings import renumber_findings_in_directory
from .normalize_citations import normalize_citations_in_project
from .bib_sanitizer import sanitize_bib_file
from .citation_context_checker import check_citation_context_consistency
from .missing_citation_checker import check_missing_citations
from .ai_wording_checker import check_ai_wording_directory, check_ai_wording
from .number_consistency_checker import check_number_consistency


def post_process_tex_files(
    tex_dir: str,
    bib_path: Optional[str] = None,
    main_tex_path: Optional[str] = None,
    verbose: bool = True,
    visual_check_tikz: bool = False,
) -> Dict[str, Any]:
    """Run all post-processing steps on LaTeX files.

    Steps:
    1. Renumber findings in \mybox{} blocks globally (1, 2, 3, ...)
    2. Normalize SubRQ subsection titles
    3. Add RQ labels
    4. Sanitize BibTeX file (fix syntax errors, duplicates, non-ASCII)
    5. Normalize citation keys to alphabetical-only format (if bib_path provided)
    6. Fix nested citation commands across all .tex files
    7. Sanitize citation keys inside \cite{...}
    8. Remove dangling citation keys
    9. Validate and strip broken TikZ figures
    10. Visual validation of TikZ figures via Claude Vision (opt-in)
    11. Wrap TikZ in resizebox
    12. Final citation cross-check (cited keys vs .bib entries)
    12d. AI wording detection and rewriting (em-dashes, leverage, utilize, etc.)
    12e. Number consistency check (abstract/intro claims vs evaluation data)
    13. Check and auto-fix LaTeX syntax errors — ALWAYS LAST
    
    Args:
        tex_dir: Directory containing .tex files
        bib_path: Optional path to .bib file for citation normalization
        main_tex_path: Optional path to main.tex file (will also be checked)
        verbose: If True, print progress
        
    Returns:
        Dictionary with statistics from each step
    """
    results = {
        'tex_checks': {},
        'findings_renumbered': {},
        'citations_normalized': {}
    }
    
    if verbose:
        print(f"\n{'='*60}")
        print("Post-processing LaTeX files")
        print(f"{'='*60}\n")
    
    # Step 1: Renumber findings in \mybox{} blocks
    if verbose:
        print(f"\n{'='*60}")
        print("Step 1: Renumbering Finding entries in \\mybox{} blocks...")
        print("-" * 60)
    
    if os.path.isdir(tex_dir):
        findings_results = renumber_findings_in_directory(tex_dir, verbose=verbose)
        results['findings_renumbered'] = findings_results
    else:
        if verbose:
            print(f"⚠️  Tex directory not found: {tex_dir}")
        results['findings_renumbered'] = {}
    
    # Step 2: Normalize SubRQ subsection titles
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 2: Normalizing SubRQ subsection titles...")
            print("-" * 60)
        title_results = normalize_subrq_subsection_titles(tex_dir, verbose=verbose)
        results['subrq_titles_normalized'] = title_results
    else:
        results['subrq_titles_normalized'] = {}
    
    # Step 2b: Strip \paragraph{} commands (replace with blank line)
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 2b: Stripping \\paragraph{} commands...")
            print("-" * 60)
        para_results = _strip_paragraph_commands(tex_dir, verbose=verbose)
        results['paragraph_commands_stripped'] = para_results
    else:
        results['paragraph_commands_stripped'] = {}

    # Step 3: Ensure RQ labels exist
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 3: Adding RQ labels...")
            print("-" * 60)
        label_results = add_labels_to_rq_sections(tex_dir, verbose=verbose)
        results['rq_labels_added'] = label_results
    else:
        results['rq_labels_added'] = {}

    # Step 4: Sanitize BibTeX file (fix syntax errors before any citation processing)
    if bib_path and os.path.isfile(bib_path):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 4: Sanitizing BibTeX file...")
            print("-" * 60)
        bib_stats = sanitize_bib_file(bib_path, verbose=verbose)
        results['bib_sanitized'] = bib_stats
    else:
        results['bib_sanitized'] = {}

    # Step 5: Normalize citation keys
    if bib_path:
        if verbose:
            print(f"\n{'='*60}")
            print("Step 5: Normalizing citation keys...")
            print("-" * 60)
        
        if os.path.isfile(bib_path):
            citation_results = normalize_citations_in_project(
                bib_path, 
                tex_dir, 
                verbose=verbose
            )
            results['citations_normalized'] = citation_results
        else:
            if verbose:
                print(f"⚠️  BibTeX file not found: {bib_path}")
            results['citations_normalized'] = {
                'bib_updates': 0,
                'tex_updates': 0,
                'files_updated': 0
            }
    else:
        if verbose:
            print(f"\n{'='*60}")
            print("Step 5: Skipping citation normalization (no bib_path provided)")
            print("-" * 60)

    # Step 6: Fix nested citation commands
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 6: Fixing nested citation commands...")
            print("-" * 60)
        nested_cite_fixes = _fix_nested_citations_in_directory(tex_dir, verbose=verbose)
        results['nested_citations_fixed'] = nested_cite_fixes
    else:
        results['nested_citations_fixed'] = {}

    # Step 7: Sanitize citation keys with stray characters
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 7: Sanitizing citation keys (strip non-letters inside \\cite{})...")
            print("-" * 60)
        sanitize_fixes = _sanitize_citation_keys_in_directory(tex_dir, verbose=verbose)
        results['citation_keys_sanitized'] = sanitize_fixes
    else:
        results['citation_keys_sanitized'] = {}

    # Step 8: Remove dangling citation keys (keys with no .bib entry)
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 8: Removing dangling citation keys (no matching .bib entry)...")
            print("-" * 60)
        placeholder_fixes = _remove_placeholder_citations_in_directory(
            tex_dir, bib_path=bib_path, verbose=verbose
        )
        results['placeholder_citations_removed'] = placeholder_fixes
    else:
        results['placeholder_citations_removed'] = {}

    # Step 9: Validate and strip broken TikZ figures
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 9: Validating TikZ figures (stripping broken ones)...")
            print("-" * 60)
        tikz_fixes = _validate_and_strip_broken_tikz_in_directory(tex_dir, verbose=verbose)
        results['broken_tikz_stripped'] = tikz_fixes
    else:
        results['broken_tikz_stripped'] = {}

    # Step 10 (opt-in): Visual validation of TikZ figures via Claude Vision
    if visual_check_tikz and os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 10: Visual validation of TikZ figures (Claude Vision)...")
            print("-" * 60)
        from .tikz_visual_validator import check_tikz_figures_in_directory
        visual_results = check_tikz_figures_in_directory(tex_dir, verbose=verbose)
        results['tikz_visual_check'] = visual_results
    else:
        results['tikz_visual_check'] = {}

    # Step 11: Wrap tikzpicture blocks in \resizebox to prevent overflow
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 11: Wrapping TikZ figures in \\resizebox{\\linewidth} to prevent overflow...")
            print("-" * 60)
        resize_fixes = _wrap_tikz_in_resizebox(tex_dir, verbose=verbose)
        results['tikz_resized'] = resize_fixes
    else:
        results['tikz_resized'] = {}

    # Step 12: Final citation cross-check — verify every \cite key has a .bib entry
    if bib_path and os.path.isfile(bib_path):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 12: Final citation cross-check (cited keys vs .bib entries)...")
            print("-" * 60)
        crosscheck = _crosscheck_citations(
            tex_dir, bib_path,
            main_tex_path=main_tex_path,
            verbose=verbose,
        )
        results['citation_crosscheck'] = crosscheck
    else:
        results['citation_crosscheck'] = {}

    # Step 12b: Citation context consistency (author/year vs bib entries)
    if bib_path and os.path.isfile(bib_path) and os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 12b: Checking citation context consistency (author/year)...")
            print("-" * 60)
        context_result = check_citation_context_consistency(
            tex_dir, bib_path,
            main_tex_path=main_tex_path,
            verbose=verbose,
        )
        results['citation_context_mismatches'] = context_result
    else:
        results['citation_context_mismatches'] = {}

    # Step 12c: Missing citation detection (uncited entities)
    if os.path.isdir(tex_dir):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 12c: Detecting entities missing citations...")
            print("-" * 60)
        missing_result = check_missing_citations(
            tex_dir,
            main_tex_path=main_tex_path,
            verbose=verbose,
        )
        results['missing_citations'] = missing_result
    else:
        results['missing_citations'] = {}

    # Step 12d: AI wording detection and rewriting
    if verbose:
        print(f"\n{'='*60}")
        print("Step 12d: Checking for AI-flavored wording and rewriting...")
        print("-" * 60)

    results['ai_wording_fixed'] = {}
    if os.path.isdir(tex_dir):
        ai_results = check_ai_wording_directory(tex_dir, auto_fix=True, verbose=verbose)
        results['ai_wording_fixed'] = ai_results

    # Also check main.tex if provided and not in tex_dir
    if main_tex_path and os.path.isfile(main_tex_path):
        main_dir = os.path.dirname(main_tex_path)
        main_name = os.path.basename(main_tex_path)
        if main_dir != tex_dir or main_name not in results['ai_wording_fixed']:
            if verbose:
                print(f"\n  Checking {main_name}...")
            main_ai = check_ai_wording(main_tex_path, auto_fix=True, verbose=verbose)
            results['ai_wording_fixed'][main_name] = main_ai

    # Step 12e: Number consistency check (abstract/intro vs evaluation)
    _main_tex = main_tex_path
    if not _main_tex and os.path.isdir(tex_dir):
        candidate = os.path.join(tex_dir, 'main.tex')
        if os.path.isfile(candidate):
            _main_tex = candidate
        else:
            candidate = os.path.join(tex_dir, 'paper.tex')
            if os.path.isfile(candidate):
                _main_tex = candidate

    if _main_tex and os.path.isfile(_main_tex):
        if verbose:
            print(f"\n{'='*60}")
            print("Step 12e: Checking number consistency (abstract/intro vs evaluation)...")
            print("-" * 60)
        consistency_result = check_number_consistency(_main_tex, verbose=verbose)
        results['number_consistency'] = consistency_result
    else:
        results['number_consistency'] = {}

    # Step 13: Check and auto-fix LaTeX syntax errors (ALWAYS LAST)
    if verbose:
        print(f"\n{'='*60}")
        print("Step 13: Checking LaTeX syntax and auto-fixing errors...")
        print("-" * 60)

    if os.path.isdir(tex_dir):
        tex_check_results = check_tex_directory(tex_dir, verbose=verbose, auto_fix=True)
        results['tex_checks']['directory'] = tex_check_results
    else:
        if verbose:
            print(f"⚠️  Tex directory not found: {tex_dir}")
        results['tex_checks']['directory'] = {}

    # Also check main.tex if provided
    if main_tex_path and os.path.isfile(main_tex_path):
        if verbose:
            print(f"\nChecking main.tex:")
        remaining_errors, fixes = fix_tex_file(main_tex_path, auto_fix=True, verbose=verbose)
        results['tex_checks']['main_tex'] = {
            'remaining_errors': len(remaining_errors),
            'fixes_applied': len(fixes)
        }

    # Summary
    if verbose:
        print(f"\n{'='*60}")
        print("Post-processing Summary")
        print(f"{'='*60}")
        
        # Tex checks summary
        total_tex_errors = sum(
            len(errors) for errors in results['tex_checks'].get('directory', {}).values()
        )
        total_tex_files = len(results['tex_checks'].get('directory', {}))
        main_tex_errors = results['tex_checks'].get('main_tex', {}).get('remaining_errors', 0)
        print(f"LaTeX Syntax: {total_tex_errors} error(s) remaining in {total_tex_files} file(s)")
        if main_tex_path:
            print(f"  Main.tex: {main_tex_errors} error(s) remaining")
        
        # Findings summary
        total_findings = sum(
            count for count, _ in results['findings_renumbered'].values()
        )
        findings_files = len([r for r in results['findings_renumbered'].values() if r[0] > 0])
        print(f"Findings: {total_findings} finding(s) renumbered in {findings_files} file(s)")
        
        # Bib sanitization summary
        bib_san = results.get('bib_sanitized', {})
        if bib_san and 'error' not in bib_san:
            print(f"BibTeX sanitized: {bib_san.get('duplicates_removed', 0)} duplicates removed, "
                  f"{bib_san.get('extra_ids_removed', 0)} extra IDs fixed, "
                  f"{bib_san.get('non_ascii_replaced', 0)} non-ASCII replaced")

        # Citations summary
        if bib_path:
            bib_updates = results['citations_normalized'].get('bib_updates', 0)
            tex_updates = results['citations_normalized'].get('tex_updates', 0)
            citation_files = results['citations_normalized'].get('files_updated', 0)
            print(f"Citations: {bib_updates} BibTeX key(s) updated, {tex_updates} citation(s) updated in {citation_files} file(s)")

        # Nested \cite summary
        nested_total = sum(results['nested_citations_fixed'].get(f, 0) for f in results['nested_citations_fixed'])
        print(f"Nested citations fixed: {nested_total}")

        sanitized_total = sum(results['citation_keys_sanitized'].get(f, 0) for f in results['citation_keys_sanitized'])
        print(f"Sanitized citation keys: {sanitized_total}")
        labels_total = sum(results['rq_labels_added'].get(path, 0) for path in results.get('rq_labels_added', {}))
        print(f"RQ labels added: {labels_total}")

        normalized_titles_total = sum(results['subrq_titles_normalized'].get(f, 0) for f in results['subrq_titles_normalized'])
        print(f"Normalized SubRQ titles: {normalized_titles_total}")

        para_total = sum(results.get('paragraph_commands_stripped', {}).get(f, 0) for f in results.get('paragraph_commands_stripped', {}))
        print(f"Paragraph commands stripped: {para_total}")

        placeholder_total = sum(results.get('placeholder_citations_removed', {}).get(f, 0) for f in results.get('placeholder_citations_removed', {}))
        print(f"Placeholder citations removed: {placeholder_total}")

        tikz_total = sum(results.get('broken_tikz_stripped', {}).get(f, 0) for f in results.get('broken_tikz_stripped', {}))
        print(f"Broken TikZ figures stripped: {tikz_total}")

        resized_total = sum(results.get('tikz_resized', {}).get(f, 0) for f in results.get('tikz_resized', {}))
        print(f"TikZ figures wrapped in resizebox: {resized_total}")

        visual = results.get('tikz_visual_check', {})
        if visual.get('total_figures_checked', 0) > 0:
            print(f"TikZ visual check: {visual.get('figures_with_issues', 0)} issue(s) "
                  f"in {visual['total_figures_checked']} figure(s) checked")

        print(f"{'='*60}\n")
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python post_process.py <tex_directory> [bib_file] [main_tex]")
        print("  Post-processes all LaTeX files:")
        print("  - Checks and fixes LaTeX syntax")
        print("  - Renumbers findings globally")
        print("  - Normalizes citation keys (if bib_file provided)")
        sys.exit(1)
    
    tex_dir = sys.argv[1]
    bib_file = sys.argv[2] if len(sys.argv) > 2 else None
    main_tex = sys.argv[3] if len(sys.argv) > 3 else None
    
    post_process_tex_files(tex_dir, bib_file, main_tex, verbose=True)


def _fix_nested_citations_in_directory(tex_dir: str, verbose: bool = True) -> Dict[str, int]:
    """Fix nested citation commands in all .tex files in a directory.

    Example: \cite{\cite{enablingautomatic},vulnerability} -> \cite{enablingautomatic,vulnerability}

    Returns a mapping of file_path -> number_of_replacements.
    """
    results: Dict[str, int] = {}
    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    
    # Pattern to find nested \cite{...} inside arguments (on extracted args)
    nested_pattern = re.compile(r'\\cite[a-z]*(?:p|t|s)?\{([^}]*)\}')
    
    for tex_file in sorted(tex_files):
        file_path = os.path.join(tex_dir, tex_file)
        if 'RQ1.2_subsection.tex' in file_path:
            print(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            results[file_path] = 0
            continue
        
        original_content = content
        total_replacements = 0
        
        # Manually scan for balanced \cite{...} blocks so nested braces don't break matching
        i = 0
        pieces = []
        last_pos = 0
        while i < len(content):
            start = content.find('\\cite{', i)
            if start == -1:
                break
            pieces.append(content[last_pos:start])
            brace_start = start + len('\\cite{')
            brace_count = 1
            j = brace_start
            while j < len(content) and brace_count > 0:
                if content[j] == '\\' and j + 1 < len(content):
                    j += 2
                    continue
                if content[j] == '{':
                    brace_count += 1
                elif content[j] == '}':
                    brace_count -= 1
                j += 1
            if brace_count != 0:
                # Unbalanced; append rest and stop
                pieces.append(content[start:])
                i = len(content)
                last_pos = i
                break
            # Extract args and flatten nested cites within args
            args = content[brace_start:j-1]
            new_args, n1 = nested_pattern.subn(lambda m: m.group(1), args)
            total_replacements += n1
            parts = [p.strip().strip('{}') for p in new_args.split(',') if p.strip()]
            fixed_args = ','.join(parts)
            pieces.append('\\cite{' + fixed_args + '}')
            i = j
            last_pos = j
        pieces.append(content[last_pos:])
        new_content = ''.join(pieces)
        
        if new_content != original_content:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                results[file_path] = total_replacements
                if verbose and total_replacements:
                    print(f"✅ Fixed {total_replacements} nested citation(s) in {file_path}")
            except Exception:
                results[file_path] = 0
        else:
            results[file_path] = 0
    
    return results


def _sanitize_citation_keys_in_directory(tex_dir: str, verbose: bool = True) -> Dict[str, int]:
    """Sanitize citation keys inside \cite{...} by stripping non-alphabetic chars.

    Example: \cite{ztdjava}$> -> \cite{ztdjava}
    Example: \cite{Ztd${java}$} -> \cite{ztdjava}

    Returns mapping of file_path -> replacements_count.
    """
    results: Dict[str, int] = {}
    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    for tex_file in sorted(tex_files):
        file_path = os.path.join(tex_dir, tex_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            results[file_path] = 0
            continue

        original = content
        replacements = 0

        # Walk through balanced \cite{...} blocks
        i = 0
        out = []
        last = 0
        while i < len(content):
            start = content.find('\\cite{', i)
            if start == -1:
                break
            out.append(content[last:start])
            bstart = start + len('\\cite{')
            depth = 1
            j = bstart
            while j < len(content) and depth > 0:
                if content[j] == '\\' and j + 1 < len(content):
                    j += 2
                    continue
                if content[j] == '{':
                    depth += 1
                elif content[j] == '}':
                    depth -= 1
                j += 1
            if depth != 0:
                # unbalanced; append rest and stop
                out.append(content[start:])
                i = len(content)
                last = i
                break

            args = content[bstart:j-1]
            # Split by comma, sanitize each key
            raw_parts = [p for p in args.split(',')]
            clean_parts = []
            changed = False
            for p in raw_parts:
                token = p.strip()
                # Remove LaTeX math and braces
                token = re.sub(r'\$\{[^}]*\}\$', '', token)
                token = re.sub(r'\$[^$]*\$', '', token)
                token = token.strip('{}')
                # Keep only letters; lower-case to align with normalized bib keys
                sanitized = re.sub(r'[^A-Za-z]', '', token).lower()
                if sanitized != token:
                    changed = True
                if sanitized:
                    clean_parts.append(sanitized)
            fixed_args = ','.join(clean_parts) if clean_parts else args
            if changed:
                replacements += 1
            out.append('\\cite{' + fixed_args + '}')
            i = j
            last = j
        out.append(content[last:])

        new_content = ''.join(out)
        if new_content != original:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                results[file_path] = replacements
                if verbose and replacements:
                    print(f"✅ Sanitized {replacements} citation occurrence(s) in {file_path}")
            except Exception:
                results[file_path] = 0
        else:
            results[file_path] = 0

    return results


def add_labels_to_rq_sections(tex_dir: str, verbose: bool = True) -> Dict[str, int]:
    """Ensure \label commands exist for RQ headers and subsections."""
    updates: Dict[str, int] = {}

    header_pattern = re.compile(r'_RQ(\d+)_header\.tex$', re.IGNORECASE)
    subsection_pattern = re.compile(r'_RQ(\d+)\.(\d+)_subsection\.tex$', re.IGNORECASE)
    section_cmd = re.compile(r'\\section\{[^}]+\}')
    # Match both \subsection and \subsubsection
    subsection_cmd = re.compile(r'\\(?:sub){1,2}section\{[^}]+\}')

    for filename in sorted(os.listdir(tex_dir)):
        path = os.path.join(tex_dir, filename)
        if not filename.endswith('.tex') or not os.path.isfile(path):
            continue

        header_match = header_pattern.search(filename)
        subsection_match = subsection_pattern.search(filename)
        if not header_match and not subsection_match:
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            updates[path] = 0
            continue

        if header_match:
            (major,) = header_match.groups()
            label = f"sec:rq{major}"
            cmd_regex = section_cmd
        else:
            major, minor = subsection_match.groups()
            label = f"sec:rq{major}.{minor}"
            cmd_regex = subsection_cmd

        if f"\\label{{{label}}}" in content:
            updates[path] = 0
            continue

        cmd_match = cmd_regex.search(content)
        if not cmd_match:
            updates[path] = 0
            continue

        insertion_point = cmd_match.end()
        new_content = content[:insertion_point] + f"\n\\label{{{label}}}" + content[insertion_point:]

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updates[path] = 1
            if verbose:
                print(f"  ✅ Added label {label} to {path}")
        except Exception:
            updates[path] = 0

    return updates


def normalize_subrq_subsection_titles(tex_dir: str, verbose: bool = True) -> Dict[str, int]:
    """Convert \\subsection* titles like 'SubRQ RQ1.2: Title' to numbered \\subsection."""
    results: Dict[str, int] = {}
    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    pattern = re.compile(
        r'(\\subsection)\*\{\s*subrq\s+rq[\d\.]+\s*[:\-–—]?\s*([^}]*)\}',
        re.IGNORECASE
    )

    for tex_file in sorted(tex_files):
        file_path = os.path.join(tex_dir, tex_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            results[file_path] = 0
            continue

        def _replace(match: re.Match) -> str:
            command = match.group(1)
            title = match.group(2).strip()
            return f"{command}{{{title}}}"

        new_content, count = pattern.subn(_replace, content)
        if count > 0 and new_content != content:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                results[file_path] = count
                if verbose:
                    print(f"✅ Normalized {count} SubRQ title(s) in {file_path}")
            except Exception:
                results[file_path] = 0
        else:
            results[file_path] = 0

    return results


def _strip_paragraph_commands(tex_dir: str, verbose: bool = True) -> Dict[str, int]:
    r"""Strip \paragraph{...} commands from subsection .tex files.

    Replaces ``\paragraph{Some Title.}`` (and any trailing text on the same
    line) with a blank line so LaTeX renders a normal paragraph break instead
    of a bold run-in heading.  Only operates on *_subsection.tex and
    *_discussion_*.tex files to avoid touching section headers or other
    structural files.

    Returns mapping of file_path -> number of \paragraph commands removed.
    """
    results: Dict[str, int] = {}
    para_re = re.compile(r'^\s*\\paragraph\{[^}]*\}\s*', re.MULTILINE)

    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    for tex_file in sorted(tex_files):
        # Only touch subsection and discussion files
        lower = tex_file.lower()
        if not ('subsection' in lower or 'discussion' in lower):
            results[os.path.join(tex_dir, tex_file)] = 0
            continue

        file_path = os.path.join(tex_dir, tex_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            results[file_path] = 0
            continue

        new_content, count = para_re.subn('\n', content)
        if count > 0 and new_content != content:
            # Collapse runs of 3+ blank lines into 2
            new_content = re.sub(r'\n{3,}', '\n\n', new_content)
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                results[file_path] = count
                if verbose:
                    print(f"  ✅ Stripped {count} \\paragraph{{}} command(s) from {tex_file}")
            except Exception:
                results[file_path] = 0
        else:
            results[file_path] = 0

    return results


def _load_bib_keys(bib_path: str) -> set:
    """Load all citation keys defined in a .bib file."""
    keys = set()
    if not bib_path or not os.path.isfile(bib_path):
        return keys
    try:
        with open(bib_path, 'r', encoding='utf-8') as f:
            content = f.read()
        for m in re.finditer(r'@\w+\{([^,}\s]+)', content):
            keys.add(m.group(1).strip())
    except Exception:
        pass
    return keys


def _remove_placeholder_citations_in_directory(
    tex_dir: str,
    bib_path: str = None,
    verbose: bool = True,
) -> Dict[str, int]:
    """Remove citation keys that have no matching BibTeX entry from \\cite{} commands.

    Strategy:
      1. If a .bib file is provided, load its keys and remove any \\cite key
         that does NOT appear in the .bib file (dangling reference).
      2. As a fallback (no .bib), remove keys matching the legacy 'unknown*'
         pattern — but ONLY if they are purely placeholder-shaped (i.e.
         'Unknown' followed by a single author-like token with no year/keyword,
         such as 'UnknownGoldblum').  Keys that happen to start with 'unknown'
         but include year and keyword parts (e.g., 'unknown_2020_calibration')
         are kept because they were generated by bib_key_generator and likely
         have a valid .bib entry.

    If all keys in a \\cite{} are removed the entire \\cite{} command is deleted.
    If only some keys are removed, those keys are stripped and the rest remain.

    Returns mapping of file_path -> number of placeholder keys removed.
    """
    results: Dict[str, int] = {}
    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]

    # Try to auto-discover .bib file if not provided
    if bib_path is None:
        parent = os.path.dirname(tex_dir.rstrip('/'))
        for f in os.listdir(parent) if os.path.isdir(parent) else []:
            if f.endswith('_references.bib'):
                bib_path = os.path.join(parent, f)
                break

    bib_keys = _load_bib_keys(bib_path)

    if bib_keys:
        # Case-insensitive lookup set
        bib_keys_lower = {k.lower() for k in bib_keys}

        def _is_removable(key: str) -> bool:
            return key.lower() not in bib_keys_lower

        if verbose:
            print(f"  Loaded {len(bib_keys)} keys from .bib; will remove dangling citations")
    else:
        # Fallback: only remove bare 'Unknown<Author>' placeholders (no underscores)
        _bare_placeholder_re = re.compile(r'^Unknown[A-Z][a-z]+$')

        def _is_removable(key: str) -> bool:
            return bool(_bare_placeholder_re.match(key))

        if verbose:
            print("  No .bib file found; falling back to conservative placeholder removal")

    for tex_file in sorted(tex_files):
        file_path = os.path.join(tex_dir, tex_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            results[file_path] = 0
            continue

        original = content
        removed = 0

        def _replace_cite(m: re.Match) -> str:
            nonlocal removed
            keys_str = m.group(1)
            keys = [k.strip() for k in keys_str.split(',') if k.strip()]
            kept = []
            for k in keys:
                if _is_removable(k):
                    removed += 1
                else:
                    kept.append(k)
            if not kept:
                return ''
            return '\\cite{' + ','.join(kept) + '}'

        new_content = re.sub(r'\\cite\{([^}]*)\}', _replace_cite, content)

        # Clean up double spaces / space-before-punctuation left by removal
        new_content = re.sub(r'  +', ' ', new_content)
        new_content = re.sub(r' ([.,;:])', r'\1', new_content)

        if new_content != original:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                results[file_path] = removed
                if verbose and removed:
                    print(f"  ✅ Removed {removed} dangling citation(s) in {tex_file}")
            except Exception:
                results[file_path] = 0
        else:
            results[file_path] = 0

    return results


def _validate_and_strip_broken_tikz_in_directory(tex_dir: str, verbose: bool = True) -> Dict[str, int]:
    """Validate each tikzpicture block by attempting to compile it.

    Broken blocks (compilation failure) are replaced with an empty string.
    Requires ``pdflatex`` on PATH; silently skipped if unavailable.

    Returns mapping of file_path -> number of tikzpicture blocks removed.
    """
    import shutil
    import subprocess
    import tempfile

    results: Dict[str, int] = {}

    if not shutil.which('pdflatex'):
        if verbose:
            print("  ⚠️  pdflatex not found on PATH — skipping TikZ validation")
        return results

    tikz_block_re = re.compile(
        r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})',
        re.DOTALL,
    )

    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    for tex_file in sorted(tex_files):
        file_path = os.path.join(tex_dir, tex_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            results[file_path] = 0
            continue

        blocks = list(tikz_block_re.finditer(content))
        if not blocks:
            results[file_path] = 0
            continue

        stripped = 0
        # Process blocks in reverse so indices stay valid after replacement
        for m in reversed(blocks):
            block_text = m.group(1)
            if _tikz_block_compiles(block_text):
                continue
            # Try common mechanical fixes before stripping
            fixed = _attempt_tikz_fix(block_text)
            if fixed is not None and _tikz_block_compiles(fixed):
                content = content[:m.start()] + fixed + content[m.end():]
                if verbose:
                    print(f"  🔧 Auto-fixed a TikZ block in {tex_file}")
            else:
                content = content[:m.start()] + content[m.end():]
                stripped += 1

        if stripped > 0:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                results[file_path] = stripped
                if verbose:
                    print(f"  ✅ Stripped {stripped} broken TikZ block(s) from {tex_file}")
            except Exception:
                results[file_path] = 0
        else:
            results[file_path] = 0

    return results


# ── TikZ compilation helpers ──────────────────────────────────────────

_TIKZ_PREAMBLE = r"""\documentclass{article}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usetikzlibrary{shapes,arrows,arrows.meta,positioning,calc,fit,backgrounds,shadows,decorations.pathmorphing}
\definecolor{accentblue}{HTML}{4A90D9}
\definecolor{accentteal}{HTML}{50B8B4}
\definecolor{accentorange}{HTML}{F5A623}
\definecolor{accentgreen}{HTML}{7BC67E}
\definecolor{accentpurple}{HTML}{9B72CF}
\definecolor{accentpink}{HTML}{E87BA1}
\definecolor{lightblue}{HTML}{DCEEFB}
\definecolor{lightteal}{HTML}{D6F0EE}
\definecolor{lightorange}{HTML}{FDE8C8}
\definecolor{lightgreen}{HTML}{DFF0D8}
\definecolor{lightpurple}{HTML}{E8DDEF}
\definecolor{lightpink}{HTML}{FADADD}
\definecolor{lightgray}{HTML}{F5F5F5}
\definecolor{darkgray}{HTML}{616161}
\begin{document}
"""

_TIKZ_POSTAMBLE = r"""
\end{document}
"""


def _tikz_block_compiles(block: str) -> bool:
    """Return True if a tikzpicture block compiles without error."""
    import subprocess
    import tempfile

    # Auto-stub any custom commands used inside the block so the
    # standalone compilation test does not fail on undefined macros
    # like \tool, \bench, \RQ, etc.
    stubs = _generate_command_stubs(block)
    test_doc = _TIKZ_PREAMBLE + stubs + block + _TIKZ_POSTAMBLE
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, 'test.tex')
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(test_doc)
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'test.tex'],
                cwd=tmpdir,
                capture_output=True,
                timeout=30,
            )
            return result.returncode == 0
    except Exception:
        return False


def _generate_command_stubs(block: str) -> str:
    """Generate \\newcommand stubs for custom commands found in a TikZ block.

    Scans for \\commandname usage and generates no-op definitions for any
    command not in the standard LaTeX/TikZ built-in set.  This prevents
    standalone compilation tests from failing due to undefined macros that
    are defined in the project's main.tex.
    """
    # Extract all command names used in the block
    used = set(re.findall(r'\\([a-zA-Z]+)', block))

    # Known built-in commands that should NOT be stubbed
    builtins = {
        # LaTeX fundamentals
        'begin', 'end', 'textbf', 'textit', 'texttt', 'textsc', 'emph',
        'textrm', 'textsf', 'textmd', 'textup', 'textsl',
        'tiny', 'scriptsize', 'footnotesize', 'small', 'normalsize',
        'large', 'Large', 'LARGE', 'huge', 'Huge',
        'bfseries', 'itshape', 'ttfamily', 'scshape', 'mdseries',
        'centering', 'raggedright', 'raggedleft',
        'par', 'noindent', 'vspace', 'hspace', 'quad', 'qquad',
        'newline', 'linebreak', 'pagebreak',
        'label', 'ref', 'cite', 'caption', 'footnote',
        'section', 'subsection', 'subsubsection', 'paragraph',
        'item', 'input', 'include', 'usepackage', 'documentclass',
        'newcommand', 'renewcommand', 'providecommand', 'def',
        'setlength', 'addtolength',
        'resizebox', 'scalebox', 'rotatebox', 'raisebox', 'parbox', 'mbox',
        'fbox', 'framebox', 'makebox', 'colorbox', 'fcolorbox',
        'includegraphics', 'rule', 'hfill', 'vfill', 'fill',
        # Math
        'mathbb', 'mathbf', 'mathrm', 'mathcal', 'mathit', 'mathsf',
        'text', 'operatorname', 'frac', 'sqrt', 'sum', 'prod', 'int',
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'sigma', 'theta',
        'lambda', 'mu', 'pi', 'omega', 'phi', 'psi', 'rho', 'tau',
        'Rightarrow', 'Leftarrow', 'rightarrow', 'leftarrow',
        'leftrightarrow', 'Leftrightarrow', 'geq', 'leq', 'neq',
        'times', 'cdot', 'ldots', 'cdots', 'in', 'infty',
        # TikZ/PGF
        'node', 'draw', 'fill', 'path', 'coordinate', 'pic',
        'foreach', 'pgfmathsetmacro', 'tikzset', 'tikzstyle',
        'definecolor', 'color', 'textcolor',
        'usetikzlibrary', 'pgfplotsset',
    }

    stubs = []
    for cmd in used - builtins:
        # Only stub simple commands (no numbers, short names)
        if len(cmd) >= 2 and cmd.isalpha():
            stubs.append(f'\\providecommand{{\\{cmd}}}{{}}')

    if stubs:
        return '\n'.join(stubs) + '\n'
    return ''


def _attempt_tikz_fix(block: str) -> Optional[str]:
    """Try common mechanical fixes for TikZ syntax errors.

    Returns the fixed string, or None if no fix was attempted.
    """
    fixed = block

    # Fix: "below left=8mm and 10mm of node" -> "below left=of node"
    # The 'and' syntax requires specific TikZ library versions; simplify.
    fixed = re.sub(
        r'(above|below|left|right|above left|above right|below left|below right)'
        r'\s*=\s*[\d.]+\s*(?:mm|cm|pt|em)\s+and\s+[\d.]+\s*(?:mm|cm|pt|em)\s+of\s+',
        r'\1=of ',
        fixed,
    )

    # Fix: Remove stray lone $ inside node text (common LLM artifact)
    fixed = re.sub(r'(?<!\$)\$(?!\$)', '', fixed)

    if fixed != block:
        return fixed
    return None


def _crosscheck_citations(
    tex_dir: str,
    bib_path: str,
    main_tex_path: Optional[str] = None,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Cross-check that every \\cite key in .tex files has a matching .bib entry.

    Scans all .tex files in tex_dir (and optionally main_tex_path) for
    \\cite{key1,key2,...} commands and verifies each key exists in the .bib
    file.  Dangling keys are removed from the \\cite commands; empty \\cite{}
    commands are deleted entirely.

    Returns a dict with:
      - missing_keys: set of keys cited but not in .bib
      - files_fixed: number of .tex files modified
      - keys_removed: total number of dangling key occurrences removed
    """
    bib_keys = _load_bib_keys(bib_path)
    bib_keys_lower = {k.lower() for k in bib_keys}

    if verbose:
        print(f"  Loaded {len(bib_keys)} .bib keys for cross-check")

    # Safety: if .bib has no parseable keys, skip removal to avoid
    # destroying all citations due to a bad path or empty file.
    if not bib_keys:
        if verbose:
            print("  ⚠️  No .bib keys found — skipping cross-check to avoid data loss")
        return {'missing_keys': set(), 'files_fixed': 0, 'keys_removed': 0}

    missing_keys: set = set()
    files_fixed = 0
    keys_removed = 0

    # Collect all .tex files to scan
    tex_files = []
    if os.path.isdir(tex_dir):
        tex_files.extend(
            os.path.join(tex_dir, f)
            for f in sorted(os.listdir(tex_dir))
            if f.endswith('.tex')
        )
    if main_tex_path and os.path.isfile(main_tex_path):
        if main_tex_path not in tex_files:
            tex_files.append(main_tex_path)

    for file_path in tex_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        original = content
        removed_in_file = 0

        def _fix_cite(m: re.Match) -> str:
            nonlocal removed_in_file
            keys_str = m.group(1)
            keys = [k.strip() for k in keys_str.split(',') if k.strip()]
            kept = []
            for k in keys:
                if k.lower() in bib_keys_lower:
                    kept.append(k)
                else:
                    missing_keys.add(k)
                    removed_in_file += 1
            if not kept:
                return ''
            return '\\cite{' + ','.join(kept) + '}'

        content = re.sub(r'\\cite\{([^}]*)\}', _fix_cite, content)

        # Clean up artifacts from removed citations
        content = re.sub(r'  +', ' ', content)
        content = re.sub(r' ([.,;:])', r'\1', content)

        if content != original:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_fixed += 1
                keys_removed += removed_in_file
                if verbose:
                    print(f"  ✅ Removed {removed_in_file} dangling key(s) from {os.path.basename(file_path)}")
            except Exception:
                pass

    if verbose:
        if missing_keys:
            print(f"  ⚠️  {len(missing_keys)} unique key(s) not found in .bib: {', '.join(sorted(missing_keys)[:10])}")
        else:
            print("  ✅ All cited keys have matching .bib entries")

    return {
        'missing_keys': missing_keys,
        'files_fixed': files_fixed,
        'keys_removed': keys_removed,
    }


def _wrap_tikz_in_resizebox(tex_dir: str, verbose: bool = True) -> Dict[str, int]:
    """Wrap tikzpicture blocks in \\resizebox{\\linewidth}{!}{...} to prevent overflow.

    Skips blocks that are already inside a \\resizebox or \\scalebox command.

    Returns mapping of file_path -> number of blocks wrapped.
    """
    results: Dict[str, int] = {}
    tikz_block_re = re.compile(
        r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})',
        re.DOTALL,
    )

    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    for tex_file in sorted(tex_files):
        file_path = os.path.join(tex_dir, tex_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            results[file_path] = 0
            continue

        blocks = list(tikz_block_re.finditer(content))
        if not blocks:
            results[file_path] = 0
            continue

        wrapped = 0
        # Process in reverse so indices stay valid
        for m in reversed(blocks):
            start = m.start()
            # Check if already wrapped in \resizebox or \scalebox
            prefix = content[max(0, start - 80):start]
            if '\\resizebox' in prefix or '\\scalebox' in prefix:
                continue
            replacement = '\\resizebox{\\linewidth}{!}{%\n' + m.group(1) + '\n}'
            content = content[:start] + replacement + content[m.end():]
            wrapped += 1

        if wrapped > 0:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                results[file_path] = wrapped
                if verbose:
                    print(f"  ✅ Wrapped {wrapped} TikZ block(s) in {tex_file}")
            except Exception:
                results[file_path] = 0
        else:
            results[file_path] = 0

    return results
