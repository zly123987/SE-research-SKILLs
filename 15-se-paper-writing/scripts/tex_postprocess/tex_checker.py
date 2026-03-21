"""LaTeX grammar checker utility for validating .tex files.

Checks for:
- Unmatched braces/brackets
- Unclosed LaTeX environments
- Unmatched citation commands
- Common LaTeX syntax errors
"""

import os
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TexError:
    """Represents a LaTeX error with location and description."""
    line_number: int
    column: Optional[int]
    error_type: str
    message: str
    context: str  # The line or relevant context


@dataclass
class TexFix:
    """Represents a fix applied to a LaTeX file."""
    line_number: int
    fix_type: str
    description: str
    original: str
    fixed: str


def check_tex_file(tex_path: str, verbose: bool = False) -> List[TexError]:
    """Check a single .tex file for common errors.
    
    Args:
        tex_path: Path to the .tex file
        verbose: If True, print errors as they are found
        
    Returns:
        List of TexError objects found in the file
    """
    if not os.path.isfile(tex_path):
        return [TexError(0, None, "FILE_NOT_FOUND", f"File not found: {tex_path}", "")]
    
    errors = []
    
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = ''.join(lines)
    except Exception as e:
        return [TexError(0, None, "READ_ERROR", f"Error reading file: {e}", "")]
    
    # Check 1: Unmatched braces
    brace_errors = _check_braces(lines, content)
    errors.extend(brace_errors)
    
    # Check 2: Unmatched brackets
    bracket_errors = _check_brackets(lines, content)
    errors.extend(bracket_errors)
    
    # Check 3: Unclosed environments
    env_errors = _check_environments(lines, content)
    errors.extend(env_errors)
    
    # Check 4: Unmatched citation commands
    cite_errors = _check_citations(lines, content)
    errors.extend(cite_errors)
    
    # Check 5: Common LaTeX command errors
    cmd_errors = _check_commands(lines, content)
    errors.extend(cmd_errors)
    
    # Check 6: Mismatched math delimiters
    math_errors = _check_math_delimiters(lines, content)
    errors.extend(math_errors)
    
    # Sort errors by line number
    errors.sort(key=lambda e: e.line_number)
    
    if verbose:
        _print_errors(tex_path, errors)
    
    return errors


def _check_braces(lines: List[str], content: str) -> List[TexError]:
    """Check for unmatched curly braces."""
    errors = []
    brace_stack = []
    
    # Track braces, ignoring those in comments
    in_comment = False
    for line_num, line in enumerate(lines, 1):
        i = 0
        while i < len(line):
            if line[i] == '%' and (i == 0 or line[i-1] != '\\'):
                break  # Comment starts, ignore rest of line
            
            if i < len(line) - 1 and line[i:i+2] == '\\\\':
                i += 2
                continue
            
            # Skip escaped braces
            if line[i] == '\\' and i + 1 < len(line):
                if line[i+1] in ['{', '}']:
                    i += 2
                    continue
            
            if line[i] == '{':
                brace_stack.append((line_num, i + 1))
            elif line[i] == '}':
                if brace_stack:
                    brace_stack.pop()
                else:
                    errors.append(TexError(
                        line_num, i + 1, "UNMATCHED_CLOSE_BRACE",
                        "Unmatched closing brace '}'",
                        line.rstrip()
                    ))
            
            i += 1
    
    # Report unclosed braces
    for line_num, col in brace_stack:
        errors.append(TexError(
            line_num, col, "UNMATCHED_OPEN_BRACE",
            "Unmatched opening brace '{'",
            lines[line_num - 1].rstrip()
        ))
    
    return errors


def _check_brackets(lines: List[str], content: str) -> List[TexError]:
    """Check for unmatched square brackets (but allow optional arguments)."""
    errors = []
    bracket_stack = []
    
    # Track brackets, but be lenient with LaTeX optional arguments
    for line_num, line in enumerate(lines, 1):
        i = 0
        while i < len(line):
            if line[i] == '%' and (i == 0 or line[i-1] != '\\'):
                break
            
            # Skip escaped brackets
            if line[i] == '\\' and i + 1 < len(line):
                i += 2
                continue
            
            if line[i] == '[':
                bracket_stack.append((line_num, i + 1))
            elif line[i] == ']':
                if bracket_stack:
                    bracket_stack.pop()
                else:
                    # This might be intentional (closing an optional arg), but warn
                    errors.append(TexError(
                        line_num, i + 1, "POSSIBLE_UNMATCHED_BRACKET",
                        "Unmatched closing bracket ']' (might be intentional)",
                        line.rstrip()
                    ))
            
            i += 1
    
    # Only report if there are many unclosed brackets (likely an error)
    if len(bracket_stack) > 2:
        for line_num, col in bracket_stack:
            errors.append(TexError(
                line_num, col, "UNMATCHED_OPEN_BRACKET",
                "Unmatched opening bracket '['",
                lines[line_num - 1].rstrip()
            ))
    
    return errors


def _check_environments(lines: List[str], content: str) -> List[TexError]:
    """Check for unclosed LaTeX environments."""
    errors = []
    env_stack = []
    
    # Pattern to match \begin{env} and \end{env}
    begin_pattern = re.compile(r'\\begin\{([^}]+)\}')
    end_pattern = re.compile(r'\\end\{([^}]+)\}')
    
    for line_num, line in enumerate(lines, 1):
        # Check for \begin{...}
        for match in begin_pattern.finditer(line):
            env_name = match.group(1)
            # Skip comment lines
            comment_pos = line.find('%')
            if comment_pos != -1 and match.start() > comment_pos:
                continue
            env_stack.append((line_num, env_name))
        
        # Check for \end{...}
        for match in end_pattern.finditer(line):
            env_name = match.group(1)
            comment_pos = line.find('%')
            if comment_pos != -1 and match.start() > comment_pos:
                continue
            
            if env_stack:
                expected_line, expected_env = env_stack[-1]
                if expected_env == env_name:
                    env_stack.pop()
                else:
                    errors.append(TexError(
                        line_num, match.start() + 1, "MISMATCHED_ENV",
                        f"\\end{{{env_name}}} does not match \\begin{{{expected_env}}} (opened at line {expected_line})",
                        line.rstrip()
                    ))
            else:
                errors.append(TexError(
                    line_num, match.start() + 1, "UNMATCHED_END",
                    f"\\end{{{env_name}}} without matching \\begin",
                    line.rstrip()
                ))
    
    # Report unclosed environments
    for line_num, env_name in env_stack:
        errors.append(TexError(
            line_num, None, "UNCLOSED_ENV",
            f"\\begin{{{env_name}}} not closed",
            lines[line_num - 1].rstrip()
        ))
    
    return errors


def _check_citations(lines: List[str], content: str) -> List[TexError]:
    """Check for unmatched citation commands."""
    errors = []
    
    # Pattern for \cite{...}, \citep{...}, \citet{...}, etc.
    cite_pattern = re.compile(r'\\(cite[a-z]*(?:p|t|s)?)\{([^}]*)\}')
    
    for line_num, line in enumerate(lines, 1):
        comment_pos = line.find('%')
        
        for match in cite_pattern.finditer(line):
            # Skip if in comment
            if comment_pos != -1 and match.start() > comment_pos:
                continue
            
            cite_key = match.group(2)
            # Check for empty citation
            if not cite_key.strip():
                errors.append(TexError(
                    line_num, match.start() + 1, "EMPTY_CITATION",
                    f"Empty citation in {match.group(0)}",
                    line.rstrip()
                ))
            # Check for unmatched braces in citation (shouldn't happen if braces are matched, but double-check)
            open_count = cite_key.count('{')
            close_count = cite_key.count('}')
            if open_count != close_count:
                errors.append(TexError(
                    line_num, match.start() + 1, "MALFORMED_CITATION",
                    f"Malformed citation with unmatched braces: {match.group(0)}",
                    line.rstrip()
                ))
    
    return errors


def _check_commands(lines: List[str], content: str) -> List[TexError]:
    """Check for common LaTeX command errors."""
    errors = []
    
    for line_num, line in enumerate(lines, 1):
        comment_pos = line.find('%')
        
        # Check for commands that should have arguments but don't
        # \textbf, \textit, etc. without braces
        text_cmd_pattern = re.compile(r'\\(textbf|textit|emph|textsc|texttt|textmd|textup|textsl|textsf)(?![\[{])')
        for match in text_cmd_pattern.finditer(line):
            if comment_pos == -1 or match.start() < comment_pos:
                # Check if followed by whitespace or newline (likely missing braces)
                remaining = line[match.end():].lstrip()
                if not remaining or remaining[0] not in ['{', '[']:
                    errors.append(TexError(
                        line_num, match.start() + 1, "MISSING_ARG_BRACE",
                        f"Command \\{match.group(1)} may be missing braces",
                        line.rstrip()
                    ))
    
    return errors


def _check_math_delimiters(lines: List[str], content: str) -> List[TexError]:
    """Check for mismatched math mode delimiters."""
    errors = []
    
    # Track math mode: 0 = text, 1 = \(...\), 2 = $...$, 3 = \[...\], 4 = $$...$$
    math_stack = []
    
    dollar_pattern = re.compile(r'\$\$?')
    display_pattern = re.compile(r'\\[\[\]]')
    inline_pattern = re.compile(r'\\[()]')
    
    for line_num, line in enumerate(lines, 1):
        i = 0
        comment_pos = line.find('%')
        
        while i < len(line):
            if comment_pos != -1 and i >= comment_pos:
                break
            
            # Check for $$
            if i < len(line) - 1 and line[i:i+2] == '$$':
                if math_stack and math_stack[-1] == (line_num, '$$'):
                    math_stack.pop()
                else:
                    math_stack.append((line_num, '$$'))
                i += 2
                continue
            
            # Check for $ (single)
            if line[i] == '$' and (i == 0 or line[i-1] != '\\'):
                if math_stack and math_stack[-1][1] == '$':
                    math_stack.pop()
                else:
                    math_stack.append((line_num, '$'))
                i += 1
                continue
            
            # Check for \[ and \]
            if i < len(line) - 1:
                if line[i:i+2] == '\\[':
                    math_stack.append((line_num, '\\['))
                    i += 2
                    continue
                elif line[i:i+2] == '\\]':
                    if math_stack and math_stack[-1][1] == '\\[':
                        math_stack.pop()
                    else:
                        errors.append(TexError(
                            line_num, i + 1, "UNMATCHED_MATH_CLOSE",
                            "Unmatched \\]",
                            line.rstrip()
                        ))
                    i += 2
                    continue
            
            # Check for \( and \)
            if i < len(line) - 1:
                if line[i:i+2] == '\\(':
                    math_stack.append((line_num, '\\('))
                    i += 2
                    continue
                elif line[i:i+2] == '\\)':
                    if math_stack and math_stack[-1][1] == '\\(':
                        math_stack.pop()
                    else:
                        errors.append(TexError(
                            line_num, i + 1, "UNMATCHED_MATH_CLOSE",
                            "Unmatched \\)",
                            line.rstrip()
                        ))
                    i += 2
                    continue
            
            i += 1
    
    # Report unclosed math modes
    for line_num, math_type in math_stack:
        errors.append(TexError(
            line_num, None, "UNCLOSED_MATH",
            f"Unclosed math mode: {math_type}",
            lines[line_num - 1].rstrip()
        ))
    
    return errors


def _print_errors(tex_path: str, errors: List[TexError]):
    """Print errors in a readable format."""
    if not errors:
        print(f"✅ {tex_path}: No errors found")
        return
    
    print(f"\n❌ {tex_path}: {len(errors)} error(s) found")
    for error in errors:
        loc = f"line {error.line_number}"
        if error.column:
            loc += f", column {error.column}"
        print(f"  [{error.error_type}] {loc}: {error.message}")
        if error.context:
            print(f"    Context: {error.context}")


def check_tex_directory(tex_dir: str, verbose: bool = True, auto_fix: bool = True) -> Dict[str, List[TexError]]:
    """Check all .tex files in a directory and optionally auto-fix issues.
    
    Args:
        tex_dir: Directory containing .tex files
        verbose: If True, print errors as they are found
        auto_fix: If True, apply automatic fixes where possible
        
    Returns:
        Dictionary mapping file paths to lists of remaining errors
    """
    if not os.path.isdir(tex_dir):
        return {}
    
    results = {}
    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    
    if not tex_files:
        print(f"No .tex files found in {tex_dir}")
        return results
    
    print(f"Checking {len(tex_files)} .tex file(s) in {tex_dir}...\n")
    
    total_fixes = 0
    
    for tex_file in sorted(tex_files):
        tex_path = os.path.join(tex_dir, tex_file)
        if auto_fix:
            remaining_errors, fixes = fix_tex_file(tex_path, auto_fix=True, verbose=verbose)
            results[tex_path] = remaining_errors
            total_fixes += len(fixes)
        else:
            errors = check_tex_file(tex_path, verbose=verbose)
            results[tex_path] = errors
    
    # Summary
    total_errors = sum(len(errors) for errors in results.values())
    files_with_errors = sum(1 for errors in results.values() if errors)
    
    print(f"\n{'='*60}")
    if auto_fix:
        print(f"Summary: {total_fixes} fix(es) applied, {total_errors} error(s) remaining in {files_with_errors} file(s)")
    else:
        print(f"Summary: {total_errors} error(s) in {files_with_errors} file(s)")
    print(f"{'='*60}")
    
    return results


def check_single_tex_file(tex_path: str, verbose: bool = True) -> List[TexError]:
    """Convenience function to check a single file with output.
    
    Args:
        tex_path: Path to .tex file
        verbose: If True, print errors
        
    Returns:
        List of errors found
    """
    errors = check_tex_file(tex_path, verbose=verbose)
    
    if not errors:
        if verbose:
            print(f"✅ {tex_path}: No errors found")
    else:
        if verbose:
            _print_errors(tex_path, errors)
    
    return errors


def fix_tex_file(tex_path: str, auto_fix: bool = True, verbose: bool = True) -> Tuple[List[TexError], List[TexFix]]:
    """Check and automatically fix straightforward issues in a .tex file.
    
    Args:
        tex_path: Path to the .tex file
        auto_fix: If True, apply automatic fixes
        verbose: If True, print errors and fixes
        
    Returns:
        Tuple of (remaining_errors, applied_fixes)
    """
    if not os.path.isfile(tex_path):
        return [TexError(0, None, "FILE_NOT_FOUND", f"File not found: {tex_path}", "")], []
    
    # First, check for errors
    errors = check_tex_file(tex_path, verbose=False)
    
    if not errors:
        if verbose:
            print(f"✅ {tex_path}: No errors found")
        return [], []
    
    fixes = []
    remaining_errors = []
    
    if not auto_fix:
        remaining_errors = errors
        if verbose:
            _print_errors(tex_path, errors)
        return remaining_errors, fixes
    
    # Read the file
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [TexError(0, None, "READ_ERROR", f"Error reading file: {e}", "")], []
    
    original_lines = lines.copy()
    fixed_lines = lines.copy()
    
    # Group errors by type and fix what we can
    for error in errors:
        line_idx = error.line_number - 1
        
        if line_idx < 0 or line_idx >= len(fixed_lines):
            remaining_errors.append(error)
            continue
        
        original_line = fixed_lines[line_idx]
        
        # Fix 1: Unmatched closing brace (remove extra })
        if error.error_type == "UNMATCHED_CLOSE_BRACE" and error.column:
            if fixed_lines[line_idx][error.column - 1] == '}':
                fixed_line = fixed_lines[line_idx][:error.column - 1] + fixed_lines[line_idx][error.column:]
                fixes.append(TexFix(
                    error.line_number, "REMOVED_EXTRA_BRACE",
                    "Removed extra closing brace",
                    original_line.rstrip(),
                    fixed_line.rstrip()
                ))
                fixed_lines[line_idx] = fixed_line
                continue
        
        # Fix 2: Unmatched closing bracket (remove extra ])
        if error.error_type == "POSSIBLE_UNMATCHED_BRACKET" and error.column:
            if fixed_lines[line_idx][error.column - 1] == ']':
                # Only fix if it's clearly not part of an optional argument
                # Check if preceded by text (not a command)
                before = fixed_lines[line_idx][:error.column - 1].rstrip()
                if before and before[-1] not in ['[', '{', '\\']:
                    fixed_line = fixed_lines[line_idx][:error.column - 1] + fixed_lines[line_idx][error.column:]
                    fixes.append(TexFix(
                        error.line_number, "REMOVED_EXTRA_BRACKET",
                        "Removed extra closing bracket",
                        original_line.rstrip(),
                        fixed_line.rstrip()
                    ))
                    fixed_lines[line_idx] = fixed_line
                    continue
        
        # Fix 3: Missing closing brace at end of line (add })
        if error.error_type == "UNMATCHED_OPEN_BRACE":
            # Count braces in the line
            line_text = fixed_lines[line_idx]
            open_braces = line_text.count('{') - line_text.count('\\{')
            close_braces = line_text.count('}') - line_text.count('\\}')
            
            if open_braces > close_braces:
                # Add missing closing brace at end of line (before comment if present)
                comment_pos = line_text.find('%')
                if comment_pos != -1:
                    # Insert before comment
                    fixed_line = line_text[:comment_pos].rstrip() + '}' + line_text[comment_pos:]
                else:
                    fixed_line = line_text.rstrip() + '}\n'
                
                fixes.append(TexFix(
                    error.line_number, "ADDED_MISSING_BRACE",
                    f"Added missing closing brace (had {open_braces - close_braces} unmatched)",
                    original_line.rstrip(),
                    fixed_line.rstrip()
                ))
                fixed_lines[line_idx] = fixed_line
                continue
        
        # Fix 4: Empty citation - remove the citation
        if error.error_type == "EMPTY_CITATION":
            # Find and remove \cite{} or similar empty citations
            cite_pattern = re.compile(r'\\(cite[a-z]*(?:p|t|s)?)\{\s*\}')
            fixed_line = cite_pattern.sub('', fixed_lines[line_idx])
            if fixed_line != fixed_lines[line_idx]:
                fixes.append(TexFix(
                    error.line_number, "REMOVED_EMPTY_CITATION",
                    "Removed empty citation command",
                    original_line.rstrip(),
                    fixed_line.rstrip()
                ))
                fixed_lines[line_idx] = fixed_line
                continue
        
        # If we couldn't fix it, add to remaining errors
        remaining_errors.append(error)
    
    # Write fixes back to file if any were applied
    if fixes:
        try:
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            if verbose:
                print(f"\n🔧 Applied {len(fixes)} fix(es) to {tex_path}")
                for fix in fixes:
                    print(f"  [{fix.fix_type}] line {fix.line_number}: {fix.description}")
                    print(f"    Before: {fix.original[:80]}")
                    print(f"    After:  {fix.fixed[:80]}")
        except Exception as e:
            if verbose:
                print(f"❌ Error writing fixes to file: {e}")
            # Revert to original
            remaining_errors = errors
    
    # Print remaining errors
    if remaining_errors:
        if verbose:
            print(f"\n⚠️  {len(remaining_errors)} error(s) remaining (could not be auto-fixed):")
            _print_errors(tex_path, remaining_errors)
    elif verbose and fixes:
        print(f"✅ All fixable errors resolved!")
    
    return remaining_errors, fixes

