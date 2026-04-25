"""Detect and rewrite AI-flavored wording in LaTeX files.

AI-generated academic text has telltale patterns that reviewers can spot:
em-dashes used as parentheticals, overuse of certain adverbs, formulaic
transitions, and hedging words that real researchers rarely use.

This module detects these patterns and rewrites them to sound more natural
and human-written, preserving the original meaning.
"""

import os
import re
from typing import Dict, Any, List, Tuple


# ---------------------------------------------------------------------------
# AI wording rules: (pattern, description, replacement_fn_or_str)
# ---------------------------------------------------------------------------

# Each rule is: (compiled_regex, human-readable name, fix_function)
# fix_function takes a Match and returns the replacement string.
# If fix_function is None, the rule is detect-only (manual review needed).

def _fix_em_dash_parenthetical(m: re.Match) -> str:
    """Replace 'X — Y — Z' or 'X — Y' parenthetical with natural alternatives."""
    before = m.group(1).rstrip()
    middle = m.group(2).strip()
    after = m.group(3).strip() if m.group(3) else ""

    # If there's a closing em-dash, use parentheses or 'which'
    if after:
        # "X — Y — Z" -> "X (Y) Z" or "X, which Y, Z"
        return f"{before} ({middle}) {after}"
    else:
        # "X — Y" at end -> "X, which is Y" or "X, namely Y"
        # Heuristic: if middle starts with a/an/the or a noun phrase, use "namely"
        if re.match(r'^(a |an |the |its |their |our )', middle, re.I):
            return f"{before}, namely {middle}"
        else:
            return f"{before}, which is {middle}"


def _fix_single_em_dash(m: re.Match) -> str:
    """Replace single em-dash 'X — Y' with natural connector."""
    before = m.group(1).rstrip()
    after = m.group(2).strip()

    # Skip if before ends with } (likely LaTeX command boundary)
    if before.rstrip().endswith('}'):
        return m.group(0)

    # Context-dependent replacement
    lower_after = after.lower()

    # "X — such as Y" -> "X, such as Y"
    if lower_after.startswith(('such as', 'for example', 'e.g.')):
        return f"{before}, {after}"

    # "X — but/yet/however" -> "X; however, Y" or "X, but Y"
    if lower_after.startswith(('but ', 'yet ', 'however')):
        return f"{before}, {after}"

    # "X — which/that/where/when" -> "X, which/that Y"
    if lower_after.startswith(('which ', 'that ', 'where ', 'when ')):
        return f"{before}, {after}"

    # "X — a/an/the Y" -> "X, i.e., Y"
    if re.match(r'^(a |an |the )', lower_after):
        return f"{before}, i.e., {after}"

    # "X — it/they/this/these" -> "X; Y" (independent clause)
    if re.match(r'^(it |they |this |these |there )', lower_after):
        return f"{before}; {after}"

    # "X — not Y" -> "X, not Y"  (contrast)
    if lower_after.startswith('not '):
        return f"{before}, {after}"

    # "X — Y" where Y is a sentence continuation -> "X, and Y" or "X; Y"
    # If Y starts with a verb or participle, likely a clause
    if re.match(r'^(runs?|makes?|shows?|gives?|is |are |was |were |has |have |had )', lower_after):
        return f"{before}; {after}"

    # Default: just use comma
    return f"{before}, {after}"


# Patterns that are ALWAYS replaced (high confidence)
AUTO_FIX_RULES: List[Tuple[re.Pattern, str, Any]] = [
    # --- Em-dash patterns (most common AI tell) ---
    # Paired em-dashes: "X --- Y --- Z" or "X — Y — Z"
    (
        re.compile(r'([^\n{%]+?)\s*(?:---|—)\s*(.+?)\s*(?:---|—)\s*(\S.*)'),
        "paired em-dash parenthetical",
        _fix_em_dash_parenthetical,
    ),
    # Single em-dash: "X --- Y" or "X — Y" (not in LaTeX commands)
    (
        re.compile(r'([^\n{%\\]+?)\s*(?:---|—)\s*(\S.+)'),
        "single em-dash",
        _fix_single_em_dash,
    ),

    # --- Overused AI transition words ---
    (
        re.compile(r'\bFurthermore,\s', re.I),
        "furthermore (AI-favored transition)",
        lambda m: m.group(0).replace("Furthermore", "Moreover").replace("furthermore", "moreover"),
    ),
    (
        re.compile(r'\bAdditionally,\s', re.I),
        "additionally (AI-favored transition)",
        lambda m: m.group(0).replace("Additionally", "In addition").replace("additionally", "in addition"),
    ),
    (
        re.compile(r'\bIt is worth noting that\s', re.I),
        "it is worth noting that (AI filler)",
        lambda m: "Notably, " if m.group(0)[0].isupper() else "notably, ",
    ),
    (
        re.compile(r'\bIt is important to note that\s', re.I),
        "it is important to note that (AI filler)",
        lambda m: "Note that " if m.group(0)[0].isupper() else "note that ",
    ),
    (
        re.compile(r'\bIn order to\s', re.I),
        "in order to (verbose, use 'to')",
        lambda m: "To " if m.group(0)[0].isupper() else "to ",
    ),

    # --- AI hedging / filler ---
    (
        re.compile(r'\bplay(?:s)? a (?:crucial|pivotal|vital|key|critical) role in\b', re.I),
        "'plays a crucial/pivotal/vital role in' (AI cliche)",
        lambda m: m.group(0).replace("play a crucial role in", "are central to")
                            .replace("plays a crucial role in", "is central to")
                            .replace("play a pivotal role in", "are central to")
                            .replace("plays a pivotal role in", "is central to")
                            .replace("play a vital role in", "are essential for")
                            .replace("plays a vital role in", "is essential for")
                            .replace("play a key role in", "are important for")
                            .replace("plays a key role in", "is important for")
                            .replace("play a critical role in", "are essential for")
                            .replace("plays a critical role in", "is essential for"),
    ),
    (
        re.compile(r'\bLeverag(?:e|es|ing|ed)\b'),
        "'leverage/leveraging' (AI-favored, use 'use/exploit/employ')",
        lambda m: {"Leverage": "Use", "leverage": "use",
                   "Leverages": "Uses", "leverages": "uses",
                   "Leveraging": "Using", "leveraging": "using",
                   "Leveraged": "Used", "leveraged": "used"}.get(m.group(0), m.group(0)),
    ),
    (
        re.compile(r'\bUtiliz(?:e|es|ing|ed)\b'),
        "'utilize/utilizing' (AI-favored, use 'use')",
        lambda m: {"Utilize": "Use", "utilize": "use",
                   "Utilizes": "Uses", "utilizes": "uses",
                   "Utilizing": "Using", "utilizing": "using",
                   "Utilized": "Used", "utilized": "used"}.get(m.group(0), m.group(0)),
    ),
    (
        re.compile(r'\bfacilitat(?:e|es|ing|ed)\b', re.I),
        "'facilitate' (AI-favored, use 'enable/support/allow')",
        lambda m: {"facilitate": "enable", "Facilitate": "Enable",
                   "facilitates": "enables", "Facilitates": "Enables",
                   "facilitating": "enabling", "Facilitating": "Enabling",
                   "facilitated": "enabled", "Facilitated": "Enabled"}.get(m.group(0), m.group(0)),
    ),
    (
        re.compile(r'\bDelve(?:s|d)?\s+(?:into|deeper)\b', re.I),
        "'delve into' (AI-favored, use 'examine/investigate/explore')",
        lambda m: re.sub(r'(?i)delves?\s+(?:into|deeper)', 'examine', m.group(0))
                    if m.group(0)[0].islower()
                    else re.sub(r'(?i)delves?\s+(?:into|deeper)', 'Examine', m.group(0)),
    ),
    (
        re.compile(r'\bresearch landscape\b', re.I),
        "'research landscape' (AI-favored, use 'research field/area')",
        lambda m: m.group(0).replace("landscape", "field").replace("Landscape", "Field"),
    ),
    (
        re.compile(r'\bholistic(?:ally)?\b', re.I),
        "'holistic' (AI-favored, use 'comprehensive/complete/overall')",
        lambda m: {"holistic": "comprehensive", "Holistic": "Comprehensive",
                   "holistically": "comprehensively", "Holistically": "Comprehensively"
                   }.get(m.group(0), m.group(0)),
    ),
    (
        re.compile(r'\brealm\b', re.I),
        "'realm' (AI-favored, use 'area/domain/field')",
        lambda m: "domain" if m.group(0).islower() else "Domain",
    ),
    (
        re.compile(r'\bunprecedented\b', re.I),
        "'unprecedented' (AI superlative, usually overclaiming)",
        lambda m: "significant" if m.group(0).islower() else "Significant",
    ),
    (
        re.compile(r'\bseamless(?:ly)?\b', re.I),
        "'seamless/seamlessly' (AI-favored, use 'smooth/transparent')",
        lambda m: {"seamless": "smooth", "Seamless": "Smooth",
                   "seamlessly": "transparently", "Seamlessly": "Transparently"
                   }.get(m.group(0), m.group(0)),
    ),
    (
        re.compile(r'\bCrucially,\s'),
        "'Crucially,' (AI emphasis, use 'Importantly,' or restructure)",
        lambda m: "Importantly, ",
    ),
    (
        re.compile(r'\bNotably,\s(?=.*\bnotab)', re.I),
        "repeated 'notably' (AI pattern)",
        lambda m: "In particular, ",
    ),
    (
        re.compile(r'\brobust(?:ly|ness)?\b(?!\s*(?:regression|test|check|optim))', re.I),
        "'robust' outside technical context (AI-favored filler)",
        lambda m: {"robust": "reliable", "Robust": "Reliable",
                   "robustly": "reliably", "Robustly": "Reliably",
                   "robustness": "reliability", "Robustness": "Reliability"
                   }.get(m.group(0), m.group(0)),
    ),
    (
        re.compile(r'(?<![_\\])(?:This |these |which |results? )\bunderscor(?:e|es|ing|ed)\b', re.I),
        "'underscore' as verb (AI-favored, use 'highlight/emphasize/show')",
        lambda m: m.group(0).replace("underscore", "highlight")
                            .replace("Underscore", "Highlight")
                            .replace("underscores", "highlights")
                            .replace("Underscores", "Highlights")
                            .replace("underscoring", "highlighting")
                            .replace("Underscoring", "Highlighting")
                            .replace("underscored", "highlighted")
                            .replace("Underscored", "Highlighted"),
    ),
    (
        re.compile(r'\bparadigm\b(?!\s*shift)', re.I),
        "'paradigm' (AI-favored, use 'approach/model/framework')",
        lambda m: "approach" if m.group(0).islower() else "Approach",
    ),
    (
        re.compile(r'\bmultifaceted\b', re.I),
        "'multifaceted' (AI-favored, use 'complex/diverse')",
        lambda m: "complex" if m.group(0).islower() else "Complex",
    ),
    (
        re.compile(r'\bin conclusion,?\s', re.I),
        "'in conclusion' (AI essay ending, not used in papers)",
        lambda m: "To summarize, " if m.group(0)[0].isupper() else "to summarize, ",
    ),
    (
        re.compile(r'\bOverall,\s(?=.*\b(?:we|our|this|the)\b)', re.I),
        "'Overall,' at start (AI summary pattern)",
        lambda m: "In summary, ",
    ),
]

# Patterns that are detected and reported but NOT auto-fixed
# (require human judgment or context awareness)
DETECT_ONLY_RULES: List[Tuple[re.Pattern, str]] = [
    (
        re.compile(r'\b(?:aim|seek|strive)s? to (?:bridge|address|tackle|mitigate) (?:this|the) gap\b', re.I),
        "'bridge/address the gap' (AI formulaic claim — consider rephrasing)",
    ),
    (
        re.compile(r'\bpaves? the way\b', re.I),
        "'pave the way' (AI cliche — consider rephrasing)",
    ),
    (
        re.compile(r'\bsheds? light on\b', re.I),
        "'shed light on' (AI cliche — use 'reveals/clarifies/explains')",
    ),
    (
        re.compile(r'\bgarnered significant attention\b', re.I),
        "'garnered significant attention' (AI boilerplate — use 'received growing interest')",
    ),
    (
        re.compile(r'\bhas gained (?:significant |increasing |growing )?(?:traction|attention|popularity)\b', re.I),
        "'has gained traction/attention' (AI boilerplate — rephrase)",
    ),
    (
        re.compile(r'\bstate-of-the-art\b.*\bstate-of-the-art\b', re.I),
        "repeated 'state-of-the-art' in same sentence (AI pattern)",
    ),
    (
        re.compile(r'\bThis (?:paper|work|study) (?:presents|proposes|introduces)\b.*\bnovel\b', re.I),
        "'This paper presents a novel...' (AI opening formula — restructure intro)",
    ),
]


def _is_in_latex_command(line: str, pos: int) -> bool:
    """Check if position is inside a LaTeX command argument (rough heuristic)."""
    # Look backwards for unmatched { or common commands
    before = line[:pos]
    brace_depth = before.count('{') - before.count('}')
    if brace_depth > 0:
        # Check if this is inside a command like \cite, \ref, \label, \url, etc.
        cmd_match = re.search(r'\\(?:cite|ref|label|url|href|texttt|textbf|emph|section|subsection|caption)\{[^}]*$', before)
        if cmd_match:
            return True
    return False


def _is_comment_line(line: str) -> bool:
    """Check if line is a LaTeX comment."""
    stripped = line.lstrip()
    return stripped.startswith('%')


def check_ai_wording(tex_path: str, auto_fix: bool = True, verbose: bool = True) -> Dict[str, Any]:
    """Check a single .tex file for AI-flavored wording and optionally fix.

    Args:
        tex_path: Path to .tex file
        auto_fix: Whether to apply automatic fixes
        verbose: Whether to print findings

    Returns:
        Dict with 'detections' (count), 'fixes_applied' (count), 'warnings' (list)
    """
    with open(tex_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original_content = content
    detections = 0
    fixes_applied = 0
    warnings: List[str] = []

    # Process line by line for context-aware fixing
    lines = content.split('\n')
    new_lines = []

    for line_num, line in enumerate(lines, 1):
        # Skip comment lines and lines inside verbatim/lstlisting
        if _is_comment_line(line):
            new_lines.append(line)
            continue

        original_line = line

        # Check auto-fix rules (always detect; only apply fixes if auto_fix=True)
        for pattern, name, fix_fn in AUTO_FIX_RULES:
            matches = list(pattern.finditer(line))
            if matches:
                for m in reversed(matches):  # reverse to preserve positions
                    if not _is_in_latex_command(line, m.start()):
                        detections += 1
                        if auto_fix:
                            replacement = fix_fn(m) if callable(fix_fn) else fix_fn
                            line = line[:m.start()] + replacement + line[m.end():]
                            fixes_applied += 1
                            if verbose:
                                print(f"  L{line_num}: [{name}]")
                                print(f"    - {original_line.strip()}")
                                print(f"    + {line.strip()}")
                        elif verbose:
                            print(f"  L{line_num}: [{name}]")
                            print(f"    > {original_line.strip()}")

        # Detect-only rules (just warn)
        for pattern, name in DETECT_ONLY_RULES:
            matches = list(pattern.finditer(line))
            for m in matches:
                if not _is_in_latex_command(line, m.start()):
                    detections += 1
                    warning = f"L{line_num}: {name}: '{m.group(0)}'"
                    warnings.append(warning)
                    if verbose:
                        print(f"  WARNING L{line_num}: {name}")
                        print(f"    > {line.strip()}")

        new_lines.append(line)

    # Write back if changes were made
    if auto_fix and fixes_applied > 0:
        new_content = '\n'.join(new_lines)
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return {
        'detections': detections,
        'fixes_applied': fixes_applied,
        'warnings': warnings,
    }


def check_ai_wording_directory(
    tex_dir: str,
    auto_fix: bool = True,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Check all .tex files in a directory for AI-flavored wording.

    Returns:
        Dict mapping filename -> check results
    """
    results: Dict[str, Any] = {}
    total_detections = 0
    total_fixes = 0
    total_warnings: List[str] = []

    if not os.path.isdir(tex_dir):
        if verbose:
            print(f"Directory not found: {tex_dir}")
        return results

    tex_files = sorted(f for f in os.listdir(tex_dir) if f.endswith('.tex'))

    for tex_file in tex_files:
        tex_path = os.path.join(tex_dir, tex_file)
        if verbose:
            print(f"\n  Checking {tex_file}...")

        file_result = check_ai_wording(tex_path, auto_fix=auto_fix, verbose=verbose)
        results[tex_file] = file_result
        total_detections += file_result['detections']
        total_fixes += file_result['fixes_applied']
        total_warnings.extend(file_result['warnings'])

    if verbose:
        print(f"\n  AI wording check: {total_detections} detection(s), "
              f"{total_fixes} auto-fixed, {len(total_warnings)} warning(s)")

    results['_summary'] = {
        'total_detections': total_detections,
        'total_fixes': total_fixes,
        'total_warnings': len(total_warnings),
        'warnings': total_warnings,
    }

    return results
