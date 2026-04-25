"""Portable LaTeX post-processing toolkit.

Provides a complete pipeline for cleaning up LaTeX/BibTeX files:
- LaTeX syntax checking and auto-fixing
- Finding renumbering in \\mybox{} blocks
- BibTeX sanitization (duplicates, non-ASCII, syntax errors)
- Citation key normalization
- Nested citation fixing
- Dangling citation removal
- TikZ figure validation and auto-fixing (optionally via Claude CLI)

Usage:
    from tex_postprocess import post_process_tex_files

    results = post_process_tex_files(
        tex_dir="path/to/tex/sections",
        bib_path="path/to/refs.bib",
        main_tex_path="path/to/main.tex",
    )
"""

from .post_process import post_process_tex_files
from .tex_checker import check_tex_file, fix_tex_file, check_tex_directory
from .bib_sanitizer import sanitize_bib_file, sanitize_all_bib_files
from .normalize_citations import normalize_citations_in_project
from .fix_findings import renumber_findings_in_directory, renumber_findings_in_file
from .bib_key_generator import generate_bib_key, normalize_bib_entry
from .tikz_visual_validator import check_tikz_figures_in_directory
from .citation_context_checker import check_citation_context_consistency
from .missing_citation_checker import check_missing_citations

__all__ = [
    "post_process_tex_files",
    "check_tex_file",
    "fix_tex_file",
    "check_tex_directory",
    "sanitize_bib_file",
    "sanitize_all_bib_files",
    "normalize_citations_in_project",
    "renumber_findings_in_directory",
    "renumber_findings_in_file",
    "generate_bib_key",
    "normalize_bib_entry",
    "check_tikz_figures_in_directory",
    "check_citation_context_consistency",
    "check_missing_citations",
]
