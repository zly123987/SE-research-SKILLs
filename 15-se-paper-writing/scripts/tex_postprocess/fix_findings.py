"""Utility to renumber Finding entries in \mybox{} blocks.

Finds all \mybox{} blocks containing "Finding" entries and renumbers them
sequentially (1, 2, 3, 4...) instead of having duplicates or wrong numbers.
"""

import os
import re
from typing import List, Tuple

# Find all \mybox{} blocks by matching braces carefully
    # We'll use a more robust approach: find \mybox{ and then match the content by counting braces
def find_mybox_blocks(text):
    """Find all \mybox{...} blocks with properly matched braces."""
    blocks = []
    i = 0
    while i < len(text):
        # Look for \mybox{
        start = text.find('\\mybox{', i)
        if start == -1:
            break
        
        # Start after \mybox{
        brace_start = start + 7
        brace_count = 1
        j = brace_start
        
        # Find matching closing brace
        while j < len(text) and brace_count > 0:
            if text[j] == '\\' and j + 1 < len(text):
                j += 2  # Skip escaped characters
                continue
            elif text[j] == '{':
                brace_count += 1
            elif text[j] == '}':
                brace_count -= 1
            j += 1
        
        if brace_count == 0:
            # Found matching brace
            end = j
            box_content = text[brace_start:end-1]  # Exclude closing brace
            blocks.append((start, end, box_content))
            i = end
        else:
            i = brace_start + 1
    
    return blocks

    
def renumber_findings_in_file(tex_path: str, verbose: bool = True) -> Tuple[int, List[str]]:
    """Renumber all Finding entries in \mybox{} blocks to sequential order.
    
    Args:
        tex_path: Path to the .tex file
        verbose: If True, print what was fixed
        
    Returns:
        Tuple of (number_of_fixes, list_of_fixed_lines_descriptions)
    """
    if not os.path.isfile(tex_path):
        if verbose:
            print(f"❌ File not found: {tex_path}")
        return 0, []
    
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        if verbose:
            print(f"❌ Error reading file: {e}")
        return 0, []
    
    original_content = content
    fixes_applied = []
    
    
    
    def renumber_findings_in_box(box_content):
        """Renumber findings within a single \mybox{} block content."""
        # Find all "Finding X:" patterns (case-insensitive, flexible spacing)
        finding_pattern = re.compile(r'(Finding\s+)(\d+)(\s*:)', re.IGNORECASE)
        
        findings = list(finding_pattern.finditer(box_content))
        
        if not findings:
            return box_content, []
        
        # Renumber sequentially starting from 1
        fixed_box_content = box_content
        box_fixes = []
        offset = 0
        
        for idx, finding_match in enumerate(findings, start=1):
            old_number = finding_match.group(2)
            new_number = str(idx)
            
            if old_number != new_number:
                # Calculate position in the original string
                start_pos = finding_match.start() + offset
                end_pos = finding_match.end() + offset
                
                # Replace the number
                replacement = finding_match.group(1) + new_number + finding_match.group(3)
                fixed_box_content = (
                    fixed_box_content[:start_pos] + 
                    replacement + 
                    fixed_box_content[end_pos:]
                )
                
                # Update offset for subsequent replacements
                offset += len(new_number) - len(old_number)
                
                # Calculate approximate line number
                line_num = box_content[:finding_match.start()].count('\n') + 1
                box_fixes.append(
                    f"Line {line_num}: Finding {old_number} -> Finding {new_number}"
                )
        
        return fixed_box_content, box_fixes
    
    # Process all \mybox{} blocks and renumber findings globally (across all boxes)
    blocks = find_mybox_blocks(content)
    fixed_content = content
    
    # First pass: collect all findings from all boxes to determine global numbering
    all_findings = []
    for start, end, box_content in blocks:
        finding_pattern = re.compile(r'(Finding\s+)(\d+)(\s*:)', re.IGNORECASE)
        findings = list(finding_pattern.finditer(box_content))
        for finding_match in findings:
            all_findings.append((start, end, finding_match, box_content))
    
    # Second pass: renumber findings globally (1, 2, 3, 4...)
    if all_findings:
        # Process from end to start to preserve positions
        global_finding_num = len(all_findings)
        for start, end, finding_match, box_content in reversed(all_findings):
            # Find the box this finding belongs to
            for box_start, box_end, box_content_inner in blocks:
                if box_start == start and box_end == end:
                    # Get the full box content
                    fixed_box_content = box_content_inner
                    
                    # Replace this specific finding with global number
                    old_number = finding_match.group(2)
                    new_number = str(global_finding_num)
                    
                    if old_number != new_number:
                        # Find this finding in the box content and replace it
                        finding_start = finding_match.start()
                        finding_end = finding_match.end()
                        
                        replacement = finding_match.group(1) + new_number + finding_match.group(3)
                        fixed_box_content = (
                            fixed_box_content[:finding_start] + 
                            replacement + 
                            fixed_box_content[finding_end:]
                        )
                        
                        # Reconstruct the \mybox{} with fixed content
                        fixed_box = f"\\mybox{{{fixed_box_content}}}"
                        fixed_content = fixed_content[:box_start] + fixed_box + fixed_content[box_end:]
                        
                        # Track fix
                        line_num = box_content_inner[:finding_match.start()].count('\n') + 1
                        fixes_applied.append(
                            f"Box at line ~{content[:box_start].count(chr(10)) + 1}, Finding {old_number} -> Finding {new_number}"
                        )
                    
                    global_finding_num -= 1
                    break
    
    # Write back if changes were made
    if fixed_content != original_content:
        try:
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            if verbose:
                print(f"✅ Fixed {len(fixes_applied)} finding number(s) in {tex_path}")
                for fix_desc in fixes_applied:
                    print(f"  - {fix_desc}")
            
            return len(fixes_applied), fixes_applied
        except Exception as e:
            if verbose:
                print(f"❌ Error writing fixed content: {e}")
            return 0, []
    else:
        if verbose:
            print(f"ℹ️  No findings to renumber in {tex_path}")
        return 0, []


def renumber_findings_in_directory(tex_dir: str, verbose: bool = True) -> dict:
    """Renumber findings in all .tex files in a directory globally (1, 2, 3... across all files).
    
    Args:
        tex_dir: Directory containing .tex files
        verbose: If True, print progress
        
    Returns:
        Dictionary mapping file paths to (fix_count, fix_descriptions)
    """
    if not os.path.isdir(tex_dir):
        if verbose:
            print(f"❌ Directory not found: {tex_dir}")
        return {}
    
    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    
    if not tex_files:
        if verbose:
            print(f"ℹ️  No .tex files found in {tex_dir}")
        return {}
    
    if verbose:
        print(f"Renumbering findings globally across {len(tex_files)} file(s)...\n")
    
    # Step 1: Collect all findings from all files with their positions
    all_findings_global = []  # (file_path, start_pos, end_pos, finding_match, box_content)
    
    for tex_file in sorted(tex_files):
        tex_path = os.path.join(tex_dir, tex_file)
        try:
            with open(tex_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            if verbose:
                print(f"⚠️  Error reading {tex_file}: {e}")
            continue
        
        # Find all \mybox{} blocks
        blocks = find_mybox_blocks(content)
        finding_pattern = re.compile(r'(Finding\s+)(\d+)(\s*:)', re.IGNORECASE)
        
        for start, end, box_content in blocks:
            findings = list(finding_pattern.finditer(box_content))
            for finding_match in findings:
                all_findings_global.append((tex_path, start, end, finding_match, box_content, content))
    
    if not all_findings_global:
        if verbose:
            print("ℹ️  No findings found to renumber")
        return {}
    
    # Step 2: Renumber globally (1, 2, 3, 4...)
    if verbose:
        print(f"Found {len(all_findings_global)} finding(s) to renumber globally\n")
    
    results = {}
    total_fixes = 0
    
    # Process each file and update findings
    files_to_update = {}  # file_path -> updated_content
    
    # Initialize with original content
    for tex_file in sorted(tex_files):
        tex_path = os.path.join(tex_dir, tex_file)
        try:
            with open(tex_path, 'r', encoding='utf-8') as f:
                files_to_update[tex_path] = f.read()
        except:
            continue
    
    # Renumber from last to first (to preserve positions)
    global_num = len(all_findings_global)
    for tex_path, start, end, finding_match, box_content, original_content in reversed(all_findings_global):
        if tex_path not in files_to_update:
            continue
        
        content = files_to_update[tex_path]
        
        # Find the box in current content
        box_start = content.find('\\mybox{', max(0, start - 50))
        if box_start == -1:
            continue
        
        # Extract box content
        brace_start = box_start + 7
        brace_count = 1
        j = brace_start
        
        while j < len(content) and brace_count > 0:
            if content[j] == '\\' and j + 1 < len(content):
                j += 2
                continue
            elif content[j] == '{':
                brace_count += 1
            elif content[j] == '}':
                brace_count -= 1
            j += 1
        
        if brace_count == 0:
            box_end = j
            current_box_content = content[brace_start:box_end-1]
            
            # Replace finding number
            finding_start = finding_match.start()
            finding_end = finding_match.end()
            old_number = finding_match.group(2)
            new_number = str(global_num)
            
            if old_number != new_number:
                replacement = finding_match.group(1) + new_number + finding_match.group(3)
                fixed_box_content = (
                    current_box_content[:finding_start] + 
                    replacement + 
                    current_box_content[finding_end:]
                )
                
                # Update content
                fixed_box = f"\\mybox{{{fixed_box_content}}}"
                files_to_update[tex_path] = (
                    content[:box_start] + fixed_box + content[box_end:]
                )
        
        global_num -= 1
    
    # Step 3: Write updated files
    for tex_path, updated_content in files_to_update.items():
        try:
            # Check if content changed
            original_path = tex_path
            with open(original_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            if updated_content != original_content:
                with open(tex_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                # Count fixes in this file
                fix_count = len([f for f_path, _, _, _, _, _ in all_findings_global 
                               if f_path == tex_path])
                results[tex_path] = (fix_count, [])
                total_fixes += fix_count
                
                if verbose:
                    print(f"✅ Updated {tex_path}")
        except Exception as e:
            if verbose:
                print(f"❌ Error writing {tex_path}: {e}")
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Summary: {total_fixes} finding(s) renumbered globally across {len(results)} file(s)")
        print(f"{'='*60}")
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python fix_findings.py <tex_file_or_directory>")
        print("  Renumbers Finding entries in \\mybox{} blocks sequentially (1, 2, 3, ...)")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.isfile(target):
        renumber_findings_in_file(target, verbose=True)
    elif os.path.isdir(target):
        renumber_findings_in_directory(target, verbose=True)
    else:
        print(f"❌ Path not found: {target}")

