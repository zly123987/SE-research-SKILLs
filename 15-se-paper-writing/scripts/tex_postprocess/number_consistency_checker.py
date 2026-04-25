"""Check that quantitative claims in abstract/intro match the evaluation section.

Extracts numbers from abstract, introduction, and evaluation sections, then
cross-checks for inconsistencies (e.g., abstract says "87%" but evaluation
says "86.8%", or abstract says "50 projects" but evaluation says "48").

This is a REPORT-ONLY step — it flags mismatches but does not auto-fix,
because the correct value may be in either location.
"""

import os
import re
from typing import Any


# Patterns that capture quantitative claims
_NUMBER_PATTERNS = [
    # Percentages: 87%, 86.8%, 0.87
    re.compile(r'(\d+\.?\d*)\s*\\?%'),
    re.compile(r'(\d+\.\d+)(?=\s+(?:precision|recall|F1|accuracy|F-score|AUC))'),
    # Counts with context: "50 projects", "1,234 bugs", "22 version pairs"
    re.compile(r'(\d[\d,]*)\s+((?:project|subject|benchmark|dataset|librar|bug|vulnerabilit|'
               r'issue|commit|test|file|method|function|class|package|version|pair|system|'
               r'attack|categor|field|paper|tool|baseline|RQ|case|scenario)[\w]*)'),
    # p-values: p<0.05, p=0.001
    re.compile(r'p\s*[<>=]\s*(\d+\.?\d*)'),
    # Speedup/improvement: 3,150x, 14pp
    re.compile(r'(\d[\d,]*\.?\d*)\s*[xX×]'),
    re.compile(r'(\d+\.?\d*)\s*(?:pp|percentage point)'),
]

# Section markers in LaTeX
_SECTION_MARKERS = {
    'abstract': [r'\\begin\{abstract\}', r'\\abstract\{'],
    'introduction': [r'\\section\{[Ii]ntroduction\}', r'\\section\*?\{[Ii]ntro'],
    'evaluation': [
        r'\\section\{[Ee]valuation\}',
        r'\\section\{[Rr]esults?\}',
        r'\\section\{[Ee]xperiment',
        r'\\section\{[Ss]tudy [Rr]esults',
        r'\\section\{[Ee]mpirical',
    ],
    'conclusion': [r'\\section\{[Cc]onclusion'],
}

_SECTION_END_MARKERS = {
    'abstract': [r'\\end\{abstract\}', r'\\maketitle'],
    'introduction': [r'\\section\{'],  # next section
    'evaluation': [r'\\section\{'],
    'conclusion': [r'\\section\{', r'\\bibliography', r'\\end\{document\}'],
}


def _extract_section(content: str, section_name: str) -> str:
    """Extract content of a named section from LaTeX source."""
    start_patterns = _SECTION_MARKERS.get(section_name, [])
    end_patterns = _SECTION_END_MARKERS.get(section_name, [])

    # Find section start
    start_pos = -1
    for pat in start_patterns:
        m = re.search(pat, content)
        if m:
            start_pos = m.end()
            break

    if start_pos < 0:
        return ""

    # Find section end (next section or specific end marker)
    section_text = content[start_pos:]
    end_pos = len(section_text)

    for pat in end_patterns:
        # Find the FIRST occurrence after the start (but skip the one that started this section)
        for m in re.finditer(pat, section_text):
            if m.start() > 10:  # skip if too close to start (same marker)
                end_pos = min(end_pos, m.start())
                break

    return section_text[:end_pos]


def _extract_claims(text: str) -> list[dict[str, Any]]:
    """Extract quantitative claims from LaTeX text."""
    # Strip comments
    lines = []
    for line in text.split('\n'):
        # Remove comments but keep the rest
        comment_pos = -1
        for i, ch in enumerate(line):
            if ch == '%' and (i == 0 or line[i-1] != '\\'):
                comment_pos = i
                break
        if comment_pos >= 0:
            line = line[:comment_pos]
        lines.append(line)
    clean_text = '\n'.join(lines)

    claims = []
    for pattern in _NUMBER_PATTERNS:
        for m in pattern.finditer(clean_text):
            # Get surrounding context (30 chars each side)
            start = max(0, m.start() - 40)
            end = min(len(clean_text), m.end() + 40)
            context = clean_text[start:end].replace('\n', ' ').strip()

            # Normalize the number
            number_str = m.group(1).replace(',', '')
            try:
                number = float(number_str)
            except ValueError:
                continue

            claims.append({
                'number': number,
                'raw': m.group(0).strip(),
                'context': context,
                'match_start': m.start(),
            })

    return claims


def _numbers_match(a: float, b: float) -> bool:
    """Check if two numbers are essentially the same (allowing rounding)."""
    if a == b:
        return True
    # Allow rounding: 86.8 matches 87, 0.868 matches 86.8%
    if a == 0 or b == 0:
        return False
    ratio = max(a, b) / min(a, b)
    if ratio < 1.02:  # within 2%
        return True
    # Check if one is percentage of other (0.87 vs 87)
    if abs(a * 100 - b) < 0.5 or abs(b * 100 - a) < 0.5:
        return True
    return False


def check_number_consistency(
    tex_path: str,
    verbose: bool = True,
) -> dict[str, Any]:
    """Check number consistency across abstract, intro, evaluation, and conclusion.

    Returns a dict with:
      - 'mismatches': list of inconsistencies found
      - 'abstract_claims': numbers found in abstract
      - 'intro_claims': numbers found in introduction
      - 'eval_claims': numbers found in evaluation
      - 'conclusion_claims': numbers found in conclusion
    """
    if not os.path.isfile(tex_path):
        return {'error': f'File not found: {tex_path}', 'mismatches': []}

    with open(tex_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Extract sections
    sections = {}
    for name in ['abstract', 'introduction', 'evaluation', 'conclusion']:
        sections[name] = _extract_section(content, name)

    # Extract claims from each section
    section_claims = {}
    for name, text in sections.items():
        section_claims[name] = _extract_claims(text)

    eval_claims = section_claims.get('evaluation', [])
    if not eval_claims:
        if verbose:
            print("  No evaluation section found or no numbers in it — skipping consistency check")
        return {
            'mismatches': [],
            'abstract_claims': len(section_claims.get('abstract', [])),
            'intro_claims': len(section_claims.get('introduction', [])),
            'eval_claims': 0,
            'conclusion_claims': len(section_claims.get('conclusion', [])),
        }

    eval_numbers = {c['number'] for c in eval_claims}

    # Check abstract and intro claims against evaluation
    mismatches = []

    for check_section in ['abstract', 'introduction', 'conclusion']:
        for claim in section_claims.get(check_section, []):
            num = claim['number']
            # Skip very small numbers (likely not result claims) and very common ones
            if num < 2 and num not in {0.0, 1.0}:
                # Could be a p-value or proportion — check if it has % context
                if '%' not in claim['raw'] and 'p' not in claim['context'][:5].lower():
                    continue

            # Check if this number appears in evaluation
            found_match = False
            for eval_num in eval_numbers:
                if _numbers_match(num, eval_num):
                    found_match = True
                    break

            if not found_match and num > 1:
                # Only flag if the number looks like a result claim (not a count like "Section 3")
                context_lower = claim['context'].lower()
                # Skip section/figure/table references
                if any(skip in context_lower for skip in [
                    'section', 'figure', 'table', 'fig.', 'tab.', 'eq.',
                    'step', 'line', 'page', 'chapter', 'appendix',
                    'rq1', 'rq2', 'rq3', 'rq4', 'rq5',
                ]):
                    continue

                mismatches.append({
                    'section': check_section,
                    'number': num,
                    'raw': claim['raw'],
                    'context': claim['context'],
                    'issue': f"Number {claim['raw']} in {check_section} has no matching value in evaluation section",
                })

    if verbose:
        if mismatches:
            print(f"  Found {len(mismatches)} potential inconsistencies:")
            for m in mismatches:
                print(f"    [{m['section'].upper()}] {m['raw']}: {m['issue']}")
                print(f"      Context: ...{m['context']}...")
        else:
            print(f"  All numbers consistent across sections")

        for name in ['abstract', 'introduction', 'evaluation', 'conclusion']:
            count = len(section_claims.get(name, []))
            if count:
                print(f"  {name.capitalize()}: {count} quantitative claims")

    return {
        'mismatches': mismatches,
        'abstract_claims': len(section_claims.get('abstract', [])),
        'intro_claims': len(section_claims.get('introduction', [])),
        'eval_claims': len(eval_claims),
        'conclusion_claims': len(section_claims.get('conclusion', [])),
    }
