"""BibTeX Key Generator - Create robust, unique, and informative citation keys.

This module provides functions to generate better BibTeX keys that are:
1. Unique (include year and title fragment to avoid collisions)
2. Informative (author + year + keyword format)
3. Consistent (normalized casing and characters)
4. Compatible (only alphanumeric characters)

Format: authorlastname_year_keyword (e.g., zhang_2024_calibration)

Usage:
    from research_agency.tex_postprocess.bib_key_generator import generate_bib_key, normalize_bib_entry

    key = generate_bib_key(
        author="John Smith and Jane Doe",
        year="2024",
        title="Deep Learning for Image Classification"
    )
    # Returns: "smith_2024_deep"

    # Normalize an existing bib entry
    fixed_entry = normalize_bib_entry(bib_entry_string)
"""

import re
import unicodedata
from typing import Optional, Dict, Set


def normalize_text(text: str) -> str:
    """Normalize text by removing accents and special characters.

    Args:
        text: Input text to normalize

    Returns:
        Normalized ASCII text
    """
    if not text:
        return ""

    # Normalize unicode to decomposed form
    normalized = unicodedata.normalize('NFKD', text)

    # Remove non-ASCII characters
    ascii_text = normalized.encode('ASCII', 'ignore').decode('ASCII')

    # Replace common problematic patterns
    ascii_text = ascii_text.replace('&amp;', '&')
    ascii_text = ascii_text.replace('&#39;', "'")
    ascii_text = ascii_text.replace('&quot;', '"')

    return ascii_text.strip()


def extract_first_author_lastname(author_str: str) -> str:
    """Extract the last name of the first author.

    Handles formats:
    - "Smith, John" (comma-separated)
    - "John Smith" (space-separated)
    - "Smith, John and Doe, Jane" (multiple authors)
    - "John Smith and Jane Doe" (multiple authors)

    Args:
        author_str: Author string from BibTeX

    Returns:
        First author's last name in lowercase
    """
    if not author_str:
        return "unknown"

    # Clean the string
    author_str = normalize_text(author_str)

    # Get first author (before "and")
    first_author = author_str.split(' and ')[0].strip()

    # Remove any remaining braces
    first_author = first_author.replace('{', '').replace('}', '')

    if ',' in first_author:
        # Format: "Last, First"
        lastname = first_author.split(',')[0].strip()
    else:
        # Format: "First Last" or "First Middle Last"
        parts = first_author.split()
        if parts:
            lastname = parts[-1].strip()
        else:
            lastname = "unknown"

    # Clean and lowercase
    lastname = re.sub(r'[^a-zA-Z]', '', lastname).lower()

    return lastname if lastname else "unknown"


def extract_title_keyword(title: str, max_length: int = 15) -> str:
    """Extract a meaningful keyword from the title.

    Skips common stopwords and extracts the first substantive word.

    Args:
        title: Paper title
        max_length: Maximum keyword length

    Returns:
        Lowercase keyword from title
    """
    if not title:
        return "paper"

    # Clean the title
    title = normalize_text(title)

    # Skip if it's an arXiv query string (malformed)
    if 'arXiv Query' in title or 'search_query=' in title:
        return "arxiv"

    # Common stopwords to skip (includes 'unknown' which is a filename artifact, not a title word)
    stopwords = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
        'how', 'what', 'which', 'who', 'when', 'where', 'why', 'that', 'this',
        'using', 'via', 'towards', 'toward', 'about', 'into', 'over', 'under',
        'unknown', 'untitled',
    }

    # Extract words
    words = re.findall(r'[a-zA-Z]+', title.lower())

    # Find first non-stopword
    for word in words:
        if word not in stopwords and len(word) >= 3:
            return word[:max_length]

    # Fallback to first word if all are stopwords
    if words:
        return words[0][:max_length]

    return "paper"


def generate_bib_key(
    author: str = "",
    year: str = "",
    title: str = "",
    existing_keys: Optional[Set[str]] = None,
) -> str:
    """Generate a unique, informative BibTeX key.

    Format: authorlastname_year_keyword
    Example: smith_2024_deep

    If collision detected, appends suffix: smith_2024_deep_b

    Args:
        author: Author string
        year: Publication year
        title: Paper title
        existing_keys: Set of already-used keys for collision detection

    Returns:
        Unique BibTeX key
    """
    # Extract components
    lastname = extract_first_author_lastname(author)
    keyword = extract_title_keyword(title)

    # Normalize year
    year_str = ""
    if year:
        year_match = re.search(r'(\d{4})', str(year))
        if year_match:
            year_str = year_match.group(1)

    # Build base key
    parts = [lastname]
    if year_str:
        parts.append(year_str)
    parts.append(keyword)

    base_key = '_'.join(parts)

    # Ensure only alphanumeric and underscore
    base_key = re.sub(r'[^a-z0-9_]', '', base_key.lower())

    # Handle collisions if existing_keys provided
    if existing_keys is not None:
        final_key = base_key
        suffix_idx = 0
        suffixes = ['', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

        while final_key in existing_keys:
            suffix_idx += 1
            if suffix_idx < len(suffixes):
                final_key = f"{base_key}_{suffixes[suffix_idx]}" if suffixes[suffix_idx] else base_key
            else:
                final_key = f"{base_key}_{suffix_idx}"

        return final_key

    return base_key


def fix_malformed_title(title: str, arxiv_id: str = "") -> str:
    """Fix malformed arXiv titles that contain query strings.

    Args:
        title: Original title (possibly malformed)
        arxiv_id: arXiv ID if available

    Returns:
        Fixed title or placeholder
    """
    if not title:
        return "Untitled"

    # Check if title is malformed (contains arXiv query string)
    if 'arXiv Query' in title or 'search_query=' in title or 'id_list=' in title:
        if arxiv_id:
            return f"arXiv:{arxiv_id}"
        return "arXiv Paper (title unavailable)"

    # Fix HTML entities
    title = title.replace('&amp;', '&')
    title = title.replace('&lt;', '<')
    title = title.replace('&gt;', '>')
    title = title.replace('&#39;', "'")
    title = title.replace('&quot;', '"')

    # Fix encoding issues (common mojibake patterns)
    title = title.replace('â€"', '—')  # em-dash
    title = title.replace('â€"', '–')  # en-dash
    title = title.replace('â€™', "'")  # right single quote
    title = title.replace('â€œ', '"')  # left double quote
    title = title.replace('â€', '"')   # right double quote
    title = title.replace('""', '--')  # corrupted dash from encoding issues

    return title.strip()


def normalize_bib_entry(
    bib_entry: str,
    new_key: Optional[str] = None,
    fix_title: bool = True,
) -> str:
    """Normalize a BibTeX entry by fixing common issues.

    Fixes:
    - HTML entities in all fields
    - Encoding issues (mojibake)
    - Malformed arXiv titles
    - Replaces key if new_key provided

    Args:
        bib_entry: Original BibTeX entry string
        new_key: Optional new key to replace existing
        fix_title: Whether to fix malformed titles

    Returns:
        Normalized BibTeX entry
    """
    if not bib_entry:
        return ""

    # Fix HTML entities throughout
    entry = bib_entry.replace('&amp;', '&')
    entry = entry.replace('&lt;', '<')
    entry = entry.replace('&gt;', '>')
    entry = entry.replace('&#39;', "'")
    entry = entry.replace('&quot;', '"')

    # Fix common encoding issues
    entry = entry.replace('â€"', '—')
    entry = entry.replace('â€"', '–')
    entry = entry.replace('â€™', "'")
    entry = entry.replace('â€œ', '"')
    entry = entry.replace('â€', '"')
    entry = entry.replace('""', '--')  # corrupted dash (ASCII)

    # Fix unicode curly quotes that shouldn't be there
    entry = entry.replace('"', '"')  # left double quote -> straight quote
    entry = entry.replace('"', '"')  # right double quote -> straight quote
    entry = entry.replace(''', "'")  # right single quote
    entry = entry.replace(''', "'")  # left single quote

    # Fix curly quotes used as dashes in page ranges (common pdf2bib issue)
    # Handle both ASCII and Unicode curly quotes
    import re as _re
    # Unicode: " = \u201c, " = \u201d, „ = \u201e
    quote_pattern = r'["\u201c\u201d\u201e"\u00ab\u00bb]+'
    entry = _re.sub(r'\{(\d+)' + quote_pattern + r'(\d+)\}', r'{\1--\2}', entry)

    # Fix non-breaking spaces
    entry = entry.replace('\xa0', ' ')

    # Escape ampersands in journal/title fields for LaTeX compatibility
    # But don't escape if already escaped or in URLs
    def escape_ampersand_in_field(match):
        field_name = match.group(1)
        field_value = match.group(2)
        # Don't escape in URL fields
        if field_name.lower() in ('url', 'doi'):
            return match.group(0)
        # Escape unescaped ampersands
        field_value = _re.sub(r'(?<!\\)&', r'\\&', field_value)
        return f'{field_name}={{{field_value}}}'

    entry = _re.sub(r'(journal|title|booktitle|publisher)\s*=\s*\{([^}]+)\}',
                    escape_ampersand_in_field, entry, flags=_re.IGNORECASE)

    # Replace key if provided
    if new_key:
        entry = re.sub(
            r'@(\w+)\{([^,]+)',
            f'@\\1{{{new_key}',
            entry,
            count=1
        )

    # Fix malformed arXiv titles
    if fix_title and ('arXiv Query' in entry or 'search_query=' in entry):
        # Extract eprint ID if available
        eprint_match = re.search(r'eprint\s*=\s*\{?\s*([^},\s]+)', entry)
        arxiv_id = eprint_match.group(1).strip() if eprint_match else ""

        # Replace malformed title
        def fix_title_field(match):
            prefix = match.group(1)
            old_title = match.group(2)
            if 'arXiv Query' in old_title or 'search_query=' in old_title:
                new_title = f"arXiv:{arxiv_id}" if arxiv_id else "arXiv Paper"
                return f'{prefix}{{{new_title}}}'
            return match.group(0)

        entry = re.sub(
            r'(title\s*=\s*)\{([^}]+)\}',
            fix_title_field,
            entry,
            flags=re.IGNORECASE
        )

    return entry


def regenerate_bib_keys(bib_content: str) -> str:
    """Regenerate all keys in a BibTeX file with improved format.

    Args:
        bib_content: Full content of BibTeX file

    Returns:
        BibTeX content with regenerated keys
    """
    # Track used keys to avoid collisions
    used_keys: Set[str] = set()

    # Split into entries
    entries = re.split(r'\n(?=@)', bib_content)

    new_entries = []
    key_mapping: Dict[str, str] = {}  # old_key -> new_key

    for entry in entries:
        entry = entry.strip()
        if not entry or not entry.startswith('@'):
            new_entries.append(entry)
            continue

        # Extract current key
        key_match = re.match(r'@\w+\{([^,]+)', entry)
        if not key_match:
            new_entries.append(entry)
            continue

        old_key = key_match.group(1).strip()

        # Extract metadata for new key
        author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        year_match = re.search(r'year\s*=\s*\{?\s*(\d{4})', entry, re.IGNORECASE)
        title_match = re.search(r'title\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)

        author = author_match.group(1) if author_match else ""
        year = year_match.group(1) if year_match else ""
        title = title_match.group(1) if title_match else ""

        # Generate new key
        new_key = generate_bib_key(author, year, title, used_keys)
        used_keys.add(new_key)
        key_mapping[old_key] = new_key

        # Normalize entry with new key
        normalized = normalize_bib_entry(entry, new_key)
        new_entries.append(normalized)

    # Print key mapping for reference
    print(f"Regenerated {len(key_mapping)} BibTeX keys")

    return '\n\n'.join(new_entries), key_mapping


def update_tex_citations(tex_content: str, key_mapping: Dict[str, str]) -> str:
    """Update citation keys in LaTeX content based on key mapping.

    Args:
        tex_content: LaTeX content
        key_mapping: Dictionary mapping old keys to new keys

    Returns:
        Updated LaTeX content
    """
    def replace_cite(match):
        keys_str = match.group(1)
        keys = [k.strip() for k in keys_str.split(',')]
        new_keys = [key_mapping.get(k, k) for k in keys]
        return f"\\cite{{{', '.join(new_keys)}}}"

    return re.sub(r'\\cite\{([^}]+)\}', replace_cite, tex_content)


# Example usage and testing
if __name__ == "__main__":
    # Test key generation
    print("Testing BibTeX key generation...")

    test_cases = [
        ("John Smith and Jane Doe", "2024", "Deep Learning for Image Classification"),
        ("Zhang, Wei", "2023", "Calibration of Neural Networks"),
        ("", "2022", "A Study on AI Systems"),
        ("Brown", "", "Meta-Learning Approaches"),
        ("García-López, María", "2021", "Uncertainty Quantification Methods"),
    ]

    used = set()
    for author, year, title in test_cases:
        key = generate_bib_key(author, year, title, used)
        used.add(key)
        print(f"  {author[:20]:20} | {year:4} | {title[:30]:30} -> {key}")

    print("\nTesting title normalization...")

    malformed_titles = [
        " arXiv Query: search_query=&amp;id_list=1806.08640v1&amp;start=0&amp;max_results=10 ",
        "Deep Learning &amp; Neural Networks",
        "Analysis of â€œSmart Systemsâ€",
    ]

    for title in malformed_titles:
        fixed = fix_malformed_title(title, "1806.08640")
        print(f"  {title[:50]:50} -> {fixed}")

    print("\n✅ BibTeX key generator module ready")
