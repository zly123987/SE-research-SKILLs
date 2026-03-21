"""Utility to normalize citation keys to alphabetical-only format.

Reads all BibTeX entries, creates normalized (alphabetical-only) citation keys,
updates the .bib file, and synchronizes all .tex files to use the new keys.
"""

import os
import re
from typing import Dict, List, Tuple, Optional


def extract_bib_keys(bib_path: str) -> List[Tuple[str, int]]:
    """Extract all citation keys from a BibTeX file.
    
    Args:
        bib_path: Path to the .bib file
        
    Returns:
        List of (citation_key, line_number) tuples
    """
    if not os.path.isfile(bib_path):
        return []
    
    keys = []
    bib_entry_pattern = re.compile(r'@\w+\{([^,]+),')
    
    try:
        with open(bib_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                matches = bib_entry_pattern.finditer(line)
                for match in matches:
                    key = match.group(1).strip()
                    keys.append((key, line_num))
    except Exception as e:
        print(f"❌ Error reading BibTeX file: {e}")
        return []
    
    return keys


def normalize_citation_key(key: str) -> str:
    """Normalize a citation key to alphabetical-only format.
    
    Removes all non-alphabetic characters (including LaTeX math mode, special chars, numbers)
    and converts to lowercase. Preserves meaningful parts by extracting words from camelCase/PascalCase.
    
    Args:
        key: Original citation key (e.g., "reyes2022breaking", "SmartFix2023", "Ztd${java}$")
        
    Returns:
        Normalized key (e.g., "reyesbreaking", "smartfix", "ztdjava")
    """
    if not key:
        return "citation"
    
    # Convert to string and lowercase
    normalized = key.lower()
    
    # Remove LaTeX math mode: ${...}$ or $...$ or \{...\}
    normalized = re.sub(r'\$\{[^}]*\}\$', '', normalized)  # ${...}$
    normalized = re.sub(r'\$[^$]*\$', '', normalized)  # $...$
    normalized = re.sub(r'\\\{[^}]*\\\}', '', normalized)  # \{...\}
    
    # Remove other LaTeX commands and special characters
    normalized = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', normalized)  # \command{...}
    normalized = re.sub(r'\\[^a-zA-Z]', '', normalized)  # \special chars
    
    # Split camelCase/PascalCase into words
    # Insert space before capital letters that follow lowercase
    normalized = re.sub(r'([a-z])([A-Z])', r'\1 \2', normalized)
    # Also split on numbers and special characters
    normalized = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', normalized)
    normalized = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', normalized)
    
    # Remove all non-alphabetic characters (keep only letters)
    normalized = re.sub(r'[^a-z ]', '', normalized)
    
    # Extract all words (sequences of letters)
    words = re.findall(r'[a-z]+', normalized)
    
    # Combine words into single string
    result = ''.join(words)
    
    # Fallback if no words found
    if not result:
        result = "citation"
    
    return result


def create_key_mapping(bib_path: str, verbose: bool = True) -> Dict[str, str]:
    """Create a mapping from original to normalized citation keys.
    
    Handles collisions by appending numbers (a, b, c, etc.).
    
    Args:
        bib_path: Path to the .bib file
        verbose: If True, print progress
        
    Returns:
        Dictionary mapping original_key -> normalized_key
    """
    keys_with_lines = extract_bib_keys(bib_path)
    
    if not keys_with_lines:
        if verbose:
            print(f"⚠️  No citation keys found in {bib_path}")
        return {}
    
    # Create initial mapping
    key_mapping = {}
    normalized_counts = {}
    
    for original_key, line_num in keys_with_lines:
        normalized = normalize_citation_key(original_key)
        
        # Handle collisions
        if normalized in normalized_counts:
            # Already exists, append a suffix
            normalized_counts[normalized] += 1
            suffix = chr(96 + normalized_counts[normalized])  # a, b, c, ...
            normalized_key = normalized + suffix
        else:
            normalized_counts[normalized] = 0
            normalized_key = normalized
        
        # Track used normalized keys
        used_keys = set(key_mapping.values())
        while normalized_key in used_keys:
            normalized_counts[normalized] += 1
            suffix = chr(96 + normalized_counts[normalized])
            normalized_key = normalized + suffix
        
        key_mapping[original_key] = normalized_key
    
    if verbose:
        print(f"📚 Found {len(key_mapping)} citation key(s)")
        collisions = sum(1 for count in normalized_counts.values() if count > 0)
        if collisions:
            print(f"  ⚠️  {collisions} key(s) had collisions and were suffixed")
    
    return key_mapping


def update_bib_file(bib_path: str, key_mapping: Dict[str, str], verbose: bool = True) -> Tuple[int, List[str]]:
    """Update citation keys in a BibTeX file.
    
    Args:
        bib_path: Path to the .bib file
        key_mapping: Dictionary mapping original_key -> normalized_key
        verbose: If True, print progress
        
    Returns:
        Tuple of (number_of_replacements, list_of_changes)
    """
    if not os.path.isfile(bib_path):
        if verbose:
            print(f"❌ BibTeX file not found: {bib_path}")
        return 0, []
    
    try:
        with open(bib_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        if verbose:
            print(f"❌ Error reading BibTeX file: {e}")
        return 0, []
    
    original_content = content
    changes = []
    replacements = 0
    
    # Replace citation keys in @entry{key, format
    # Match @entrytype{key, where key needs to be replaced
    for original_key, normalized_key in key_mapping.items():
        if original_key == normalized_key:
            continue
        
        # Pattern to match @entrytype{original_key,
        pattern = re.compile(
            r'(@\w+\{)' + re.escape(original_key) + r'(\s*,)',
            re.MULTILINE
        )
        
        def replace_key(match):
            nonlocal replacements
            replacements += 1
            changes.append(f"{original_key} -> {normalized_key}")
            return match.group(1) + normalized_key + match.group(2)
        
        content = pattern.sub(replace_key, content)
    
    # Write back if changes were made
    if content != original_content:
        try:
            with open(bib_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if verbose:
                print(f"✅ Updated {replacements} citation key(s) in {bib_path}")
                if len(changes) <= 10:
                    for change in changes:
                        print(f"  - {change}")
                else:
                    for change in changes[:10]:
                        print(f"  - {change}")
                    print(f"  ... and {len(changes) - 10} more")
            
            return replacements, changes
        except Exception as e:
            if verbose:
                print(f"❌ Error writing BibTeX file: {e}")
            return 0, []
    else:
        if verbose:
            print(f"ℹ️  No citation keys to update in {bib_path}")
        return 0, []


def update_tex_file(tex_path: str, key_mapping: Dict[str, str], verbose: bool = True) -> Tuple[int, List[str]]:
    """Update citation keys in a LaTeX file.
    
    Args:
        tex_path: Path to the .tex file
        key_mapping: Dictionary mapping original_key -> normalized_key
        verbose: If True, print progress
        
    Returns:
        Tuple of (number_of_replacements, list_of_changes)
    """
    if not os.path.isfile(tex_path):
        if verbose:
            print(f"❌ LaTeX file not found: {tex_path}")
        return 0, []
    
    try:
        with open(tex_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        if verbose:
            print(f"❌ Error reading LaTeX file: {e}")
        return 0, []
    
    original_content = content
    changes = []
    total_replacements = 0
    
    # Replace citations in \cite{key}, \citep{key}, \citet{key}, etc.
    # Also handle \cite{key1,key2,key3} format
    # Process all keys in one pass to handle citations with multiple keys
    
    # Pattern to match citation commands: \cite{keys}, \citep{keys}, etc.
    cite_command_pattern = re.compile(r'\\(cite[a-z]*(?:p|t|s)?)\{([^}]+)\}')
    
    def replace_all_keys_in_citation(match):
        """Replace all keys in a citation command."""
        cmd = match.group(1)
        keys_str = match.group(2)
        
        # Split keys by comma
        keys = [k.strip() for k in keys_str.split(',')]
        replaced_count = 0
        
        # Replace each key if it's in the mapping
        # Also handle keys that might be in different formats (e.g., normalized versions)
        for i, key in enumerate(keys):
            # Direct match
            if key in key_mapping and key != key_mapping[key]:
                keys[i] = key_mapping[key]
                replaced_count += 1
            else:
                # Try to find a match by normalizing the key
                normalized_key = normalize_citation_key(key)
                # Find original key that normalizes to this
                for orig_key, norm_key in key_mapping.items():
                    if normalized_key == norm_key and orig_key != norm_key:
                        keys[i] = norm_key
                        replaced_count += 1
                        break
        
        if replaced_count > 0:
            return f'\\{cmd}{{' + ','.join(keys) + '}'
        return match.group(0)
    
    # Apply replacement to all citation commands
    new_content = cite_command_pattern.sub(replace_all_keys_in_citation, content)
    
    if new_content != content:
        # Count replacements by comparing before/after
        # Find all citation commands and check what changed
        original_citations = cite_command_pattern.findall(content)
        new_citations = cite_command_pattern.findall(new_content)
        
        # Count how many keys changed
        for orig_match, new_match in zip(original_citations, new_citations):
            orig_keys = [k.strip() for k in orig_match[1].split(',')]
            new_keys = [k.strip() for k in new_match[1].split(',')]
            
            for orig_key, new_key in zip(orig_keys, new_keys):
                if orig_key != new_key:
                    total_replacements += 1
                    change_desc = f"{orig_key} -> {new_key}"
                    if change_desc not in changes:
                        changes.append(change_desc)
        
        content = new_content
    
    # Additional pass: Find and replace keys in tex files that aren't in the mapping
    # This handles cases like Ztd${java}$ that appear in tex but not in bib
    # Find all citation keys in the content that aren't already normalized
    all_citation_keys = set()
    for match in cite_command_pattern.finditer(content):
        keys_str = match.group(2)
        keys = [k.strip() for k in keys_str.split(',')]
        all_citation_keys.update(keys)
    
    # Create a reverse mapping: normalized -> original (from bib)
    normalized_to_original = {}
    for orig, norm in key_mapping.items():
        if norm not in normalized_to_original:
            normalized_to_original[norm] = []
        normalized_to_original[norm].append(orig)
    
    # For each citation key found in tex, normalize it
    tex_key_replacements = {}
    for key in all_citation_keys:
        normalized = normalize_citation_key(key)
        # If normalized key exists in bib mapping, replace tex key with it
        if normalized in normalized_to_original and key != normalized:
            # Use the normalized version
            tex_key_replacements[key] = normalized
    
    # Apply tex key replacements
    if tex_key_replacements:
        for orig_tex_key, norm_key in tex_key_replacements.items():
            # Replace in citation commands
            pattern = re.compile(
                r'(\\(?:cite[a-z]*(?:p|t|s)?)\{[^}]*)' + 
                re.escape(orig_tex_key) + 
                r'([^}]*\})',
                re.IGNORECASE
            )
            def replace_tex_key(m):
                keys_str = m.group(1) + norm_key + m.group(2)
                return keys_str
            
            new_content = pattern.sub(replace_tex_key, content)
            if new_content != content:
                count = len(pattern.findall(content))
                total_replacements += count
                content = new_content
                change_desc = f"{orig_tex_key} -> {norm_key}"
                if change_desc not in changes:
                    changes.append(change_desc)
    
    # Write back if changes were made
    if content != original_content:
        try:
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if verbose:
                print(f"✅ Updated {total_replacements} citation(s) in {tex_path}")
                if changes and len(changes) <= 5:
                    for change in changes:
                        print(f"  - {change}")
            
            return total_replacements, changes
        except Exception as e:
            if verbose:
                print(f"❌ Error writing LaTeX file: {e}")
            return 0, []
    else:
        return 0, []


def normalize_citations_in_project(
    bib_path: str,
    tex_dir: str,
    verbose: bool = True
) -> Dict[str, any]:
    """Normalize all citation keys in a project.
    
    Args:
        bib_path: Path to the .bib file
        tex_dir: Directory containing .tex files
        verbose: If True, print progress
        
    Returns:
        Dictionary with statistics about the normalization
    """
    if verbose:
        print(f"{'='*60}")
        print("Normalizing citation keys to alphabetical-only format")
        print(f"{'='*60}\n")
    
    # Step 1: Create key mapping from BibTeX file
    if verbose:
        print("Step 1: Analyzing BibTeX file...")
    key_mapping = create_key_mapping(bib_path, verbose=verbose)
    
    if not key_mapping:
        if verbose:
            print("❌ No citation keys found. Aborting.")
        return {"bib_updates": 0, "tex_updates": 0, "files_updated": 0}
    
    # Step 2: Update BibTeX file
    if verbose:
        print(f"\nStep 2: Updating BibTeX file...")
    bib_replacements, bib_changes = update_bib_file(bib_path, key_mapping, verbose=verbose)
    
    # Step 3: Update all .tex files
    if verbose:
        print(f"\nStep 3: Updating LaTeX files...")
    
    if not os.path.isdir(tex_dir):
        if verbose:
            print(f"⚠️  Tex directory not found: {tex_dir}")
        return {"bib_updates": bib_replacements, "tex_updates": 0, "files_updated": 0}
    
    tex_files = [f for f in os.listdir(tex_dir) if f.endswith('.tex')]
    
    total_tex_replacements = 0
    files_updated = 0
    
    for tex_file in sorted(tex_files):
        tex_path = os.path.join(tex_dir, tex_file)
        replacements, _ = update_tex_file(tex_path, key_mapping, verbose=verbose)
        if replacements > 0:
            total_tex_replacements += replacements
            files_updated += 1
    
    # Summary
    if verbose:
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  BibTeX: {bib_replacements} key(s) updated")
        print(f"  LaTeX:  {total_tex_replacements} citation(s) updated in {files_updated} file(s)")
        print(f"{'='*60}")
    
    return {
        "bib_updates": bib_replacements,
        "tex_updates": total_tex_replacements,
        "files_updated": files_updated,
        "key_mapping": key_mapping
    }


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python normalize_citations.py <bib_file> <tex_directory>")
        print("  Normalizes all citation keys to alphabetical-only format")
        print("  Updates both .bib and .tex files")
        sys.exit(1)
    
    bib_file = sys.argv[1]
    tex_dir = sys.argv[2]
    
    normalize_citations_in_project(bib_file, tex_dir, verbose=True)

