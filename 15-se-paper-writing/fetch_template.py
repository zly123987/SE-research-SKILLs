#!/usr/bin/env python3
"""
Fetch latest LaTeX templates for SE conferences with venue-specific requirements.
Supports ACM (acmart) and IEEE (IEEEtran) templates.

IMPORTANT: Document class options MUST match official venue CFP requirements.
This script maintains a database of venue-specific requirements that should be
verified against official CFPs before submission.

Usage:
    python fetch_template.py --venue ISSTA2026 --output ./paper/
    python fetch_template.py --venue ICSE2026 --output ./paper/
    python fetch_template.py --venue FSE2026 --output ./paper/ --create-main
"""

import argparse
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile
from datetime import datetime

# Template sources from CTAN
TEMPLATE_SOURCES = {
    "acm": {
        "url": "https://www.ctan.org/tex-archive/macros/latex/contrib/acmart.zip",
        "cls_file": "acmart.cls",
        "bst_file": "ACM-Reference-Format.bst",
        "generate_cmd": "latex acmart.ins",
    },
    "ieee": {
        "url": "https://www.ctan.org/tex-archive/macros/latex/contrib/IEEEtran.zip",
        "cls_file": "IEEEtran.cls",
        "bst_file": "IEEEtran.bst",
        "generate_cmd": None,
    },
}

# Venue-specific requirements database
# CRITICAL: These MUST be verified against official CFPs before submission
# Last updated: 2026-01-26
VENUE_REQUIREMENTS = {
    # ==========================================================================
    # ACM VENUES - Use acmart.cls
    # ==========================================================================
    "ISSTA": {
        "template": "acm",
        "doc_class": "acmsmall",
        "options": ["screen", "review", "anonymous"],
        "page_limit": 18,
        "page_limit_note": "18 pages for content, unlimited references",
        "layout": "single-column",
        "required_sections": ["Data Availability"],
        "cfp_url": "https://conf.researchr.org/track/issta-2026/issta-2026-research-papers",
        "submission_url": "https://issta2026.hotcrp.com/",
        "notes": [
            "Published in PACMSE (Proceedings of the ACM on Software Engineering)",
            "Data Availability section required before references",
            "Experience papers: add '(Experience Paper)' to title",
            "Replicability studies: add '(Replicability Study)' to title",
        ],
    },
    "FSE": {
        "template": "acm",
        "doc_class": "acmsmall",
        "options": ["screen", "review", "anonymous"],
        "page_limit": 18,
        "page_limit_note": "18 pages for content, unlimited references",
        "layout": "single-column",
        "required_sections": ["Data Availability"],
        "cfp_url": "https://conf.researchr.org/track/fse-2026/fse-2026-research-papers",
        "notes": ["Published in PACMSE", "Artifacts strongly encouraged"],
    },
    "OOPSLA": {
        "template": "acm",
        "doc_class": "acmsmall",
        "options": ["screen", "review", "anonymous"],
        "page_limit": 25,
        "page_limit_note": "25 pages including everything except references",
        "layout": "single-column",
        "cfp_url": "https://2026.splashcon.org/track/splash-2026-oopsla",
        "notes": ["Published in PACMPL"],
    },
    "PLDI": {
        "template": "acm",
        "doc_class": "acmsmall",
        "options": ["screen", "review", "anonymous"],
        "page_limit": 25,
        "layout": "single-column",
        "cfp_url": "https://pldi26.sigplan.org/",
        "notes": ["Published in PACMPL"],
    },
    "POPL": {
        "template": "acm",
        "doc_class": "acmsmall",
        "options": ["screen", "review", "anonymous"],
        "page_limit": 25,
        "layout": "single-column",
        "cfp_url": "https://popl26.sigplan.org/",
        "notes": ["Published in PACMPL"],
    },
    "CCS": {
        "template": "acm",
        "doc_class": "sigconf",
        "options": ["anonymous", "review"],
        "page_limit": 15,
        "page_limit_note": "15 pages excluding references and appendices",
        "layout": "two-column",
        "cfp_url": "https://www.sigsac.org/ccs/CCS2026/call-for/call-for-papers.html",
        "notes": ["Double-blind review"],
    },
    "CHI": {
        "template": "acm",
        "doc_class": "sigchi",
        "options": ["review", "anonymous"],
        "page_limit": None,
        "page_limit_note": "No strict page limit; length should match contribution",
        "layout": "single-column",
        "cfp_url": "https://chi2026.acm.org/",
        "notes": ["Single-column format for review"],
    },
    "SIGMOD": {
        "template": "acm",
        "doc_class": "sigconf",
        "options": ["anonymous", "review"],
        "page_limit": 12,
        "layout": "two-column",
        "cfp_url": "https://2026.sigmod.org/",
    },
    "SOSP": {
        "template": "acm",
        "doc_class": "sigconf",
        "options": ["anonymous", "review"],
        "page_limit": 12,
        "layout": "two-column",
        "cfp_url": "https://sosp2026.mpi-sws.org/",
    },
    "ASPLOS": {
        "template": "acm",
        "doc_class": "sigconf",
        "options": ["anonymous", "review"],
        "page_limit": 11,
        "layout": "two-column",
        "cfp_url": "https://asplos-conference.org/",
    },
    # ==========================================================================
    # IEEE VENUES - Use IEEEtran.cls
    # ==========================================================================
    "ICSE": {
        "template": "ieee",
        "doc_class": "IEEEtran",
        "options": ["conference"],
        "page_limit": 11,
        "page_limit_note": "11 pages including figures and tables, +2 for references",
        "layout": "two-column",
        "cfp_url": "https://conf.researchr.org/track/icse-2026/icse-2026-research-track",
        "notes": [
            "Double-blind review",
            "Data availability badge available",
            "Must anonymize supplementary materials",
        ],
    },
    "ASE": {
        "template": "ieee",
        "doc_class": "IEEEtran",
        "options": ["conference"],
        "page_limit": 11,
        "page_limit_note": "11 pages + 2 for references",
        "layout": "two-column",
        "cfp_url": "https://conf.researchr.org/track/ase-2026/ase-2026-research",
        "notes": ["Reproducibility package expected"],
    },
    "ICSME": {
        "template": "ieee",
        "doc_class": "IEEEtran",
        "options": ["conference"],
        "page_limit": 11,
        "layout": "two-column",
        "cfp_url": "https://conf.researchr.org/home/icsme-2026",
    },
    "SANER": {
        "template": "ieee",
        "doc_class": "IEEEtran",
        "options": ["conference"],
        "page_limit": 11,
        "layout": "two-column",
        "cfp_url": "https://conf.researchr.org/home/saner-2026",
    },
    "MSR": {
        "template": "ieee",
        "doc_class": "IEEEtran",
        "options": ["conference"],
        "page_limit": 11,
        "page_limit_note": "11 pages + 2 for references",
        "layout": "two-column",
        "cfp_url": "https://conf.researchr.org/home/msr-2026",
        "notes": ["Data track available for dataset papers"],
    },
    "ISSRE": {
        "template": "ieee",
        "doc_class": "IEEEtran",
        "options": ["conference"],
        "page_limit": 11,
        "layout": "two-column",
        "cfp_url": "https://issre.net/",
    },
    "ICST": {
        "template": "ieee",
        "doc_class": "IEEEtran",
        "options": ["conference"],
        "page_limit": 11,
        "layout": "two-column",
        "cfp_url": "https://conf.researchr.org/home/icst-2026",
    },
    "S&P": {
        "template": "ieee",
        "doc_class": "IEEEtran",
        "options": ["conference"],
        "page_limit": 13,
        "page_limit_note": "13 pages excluding bibliography and appendices",
        "layout": "two-column",
        "cfp_url": "https://sp2026.ieee-security.org/",
        "notes": ["Appendices don't count toward limit but reviewers may skip"],
    },
}


def get_venue_config(venue: str) -> dict:
    """Get venue configuration, stripping year suffix."""
    venue_base = "".join(c for c in venue if not c.isdigit()).strip().upper()

    # Handle common aliases
    aliases = {
        "ESEC/FSE": "FSE",
        "ESECFSE": "FSE",
        "IEEE S&P": "S&P",
        "IEEE SP": "S&P",
        "OAKLAND": "S&P",
    }
    venue_base = aliases.get(venue_base, venue_base)

    if venue_base in VENUE_REQUIREMENTS:
        return VENUE_REQUIREMENTS[venue_base]

    # Try partial match
    for v in VENUE_REQUIREMENTS:
        if v in venue_base or venue_base in v:
            print(f"Note: Matched '{venue}' to '{v}'")
            return VENUE_REQUIREMENTS[v]

    print(f"WARNING: Unknown venue '{venue}'. Using default ACM sigconf format.")
    print("Please verify requirements at the official CFP before submission.")
    return {
        "template": "acm",
        "doc_class": "sigconf",
        "options": ["anonymous", "review"],
        "page_limit": 11,
        "layout": "two-column",
        "notes": ["UNKNOWN VENUE - verify requirements manually"],
    }


def fetch_template(template_type: str, output_dir: Path) -> dict:
    """Download and extract template files from CTAN."""
    template = TEMPLATE_SOURCES[template_type]
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        zip_path = tmppath / "template.zip"

        print(f"Downloading {template_type.upper()} template from CTAN...")
        urlretrieve(template["url"], zip_path)

        print("Extracting...")
        with ZipFile(zip_path) as zf:
            zf.extractall(tmppath / "extracted")

        extracted = tmppath / "extracted"
        pkg_dirs = list(extracted.iterdir())
        pkg_dir = pkg_dirs[0] if len(pkg_dirs) == 1 and pkg_dirs[0].is_dir() else extracted

        if template["generate_cmd"]:
            print(f"Generating {template['cls_file']}...")
            subprocess.run(template["generate_cmd"], shell=True, cwd=pkg_dir, capture_output=True)

        files_copied = []
        for fname in [template["cls_file"], template["bst_file"]]:
            matches = list(pkg_dir.rglob(fname))
            if matches:
                shutil.copy2(matches[0], output_dir / fname)
                files_copied.append(fname)
                print(f"Copied: {fname}")

        # Extract version
        cls_path = output_dir / template["cls_file"]
        version = "unknown"
        if cls_path.exists():
            with open(cls_path) as f:
                for line in f:
                    if "[" in line and ("ProvidesClass" in line or "v" in line):
                        try:
                            version = line.split("[")[1].split("]")[0]
                            break
                        except IndexError:
                            pass

    return {"version": version, "files": files_copied}


def create_main_tex(output_dir: Path, venue: str, config: dict):
    """Create main.tex with venue-specific document class options."""
    options_str = ",".join([config["doc_class"]] + config.get("options", []))

    if config["template"] == "acm":
        # Check if microtype fix is needed (for older TeX installations)
        preamble_fix = """% Disable microtype font expansion (compatibility fix for older TeX installations)
\\PassOptionsToPackage{expansion=false,protrusion=false}{microtype}

"""
        content = f'''{preamble_fix}\\documentclass[{options_str}]{{acmart}}

% =============================================================================
% VENUE: {venue}
% CFP: {config.get("cfp_url", "Check official website")}
% Page limit: {config.get("page_limit", "Check CFP")} pages {config.get("page_limit_note", "")}
% Layout: {config.get("layout", "Check CFP")}
% Generated: {datetime.now().strftime("%Y-%m-%d")}
% =============================================================================

% Disable ACM-specific items for anonymous submission
\\settopmatter{{printacmref=false}}
\\renewcommand\\footnotetextcopyrightpermission[1]{{}}
\\pagestyle{{plain}}

% Packages
\\usepackage{{booktabs}}
\\usepackage{{subcaption}}
\\usepackage{{xspace}}
\\usepackage{{listings}}

% Listings configuration
\\lstset{{
    basicstyle=\\ttfamily\\small,
    breaklines=true,
    frame=single,
    xleftmargin=1em,
    framexleftmargin=0.5em
}}

% Custom commands
\\newcommand{{\\tool}}{{YourTool\\xspace}}

\\begin{{document}}

\\title{{Your Paper Title}}

\\author{{Anonymous Author(s)}}
\\affiliation{{\\institution{{Anonymous Institution}}}}
\\email{{anonymous@example.com}}

\\begin{{abstract}}
Your abstract here.
\\end{{abstract}}

\\maketitle

\\section{{Introduction}}
\\label{{sec:intro}}

Your introduction here.

% TODO: Add your content sections here

\\section{{Discussion}}
\\label{{sec:discussion}}

\\subsection{{Threats to Validity}}
% Required for SE papers

'''
        # Add required sections if specified
        if "Data Availability" in config.get("required_sections", []):
            content += '''\\section*{Data Availability}
% Required for this venue - describe where data and artifacts can be accessed
Our replication package, including source code and evaluation data, is available at: [URL].

'''

        content += '''\\bibliographystyle{ACM-Reference-Format}
\\bibliography{references}

\\end{document}
'''
    else:  # IEEE
        content = f'''\\documentclass[{options_str}]{{IEEEtran}}

% =============================================================================
% VENUE: {venue}
% CFP: {config.get("cfp_url", "Check official website")}
% Page limit: {config.get("page_limit", "Check CFP")} pages {config.get("page_limit_note", "")}
% Layout: {config.get("layout", "Check CFP")}
% Generated: {datetime.now().strftime("%Y-%m-%d")}
% =============================================================================

\\usepackage{{cite}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}
\\usepackage{{xspace}}
\\usepackage{{booktabs}}
\\usepackage{{listings}}
\\usepackage{{url}}

% For anonymous submission
\\usepackage{{blindtext}}

% Custom commands
\\newcommand{{\\tool}}{{YourTool\\xspace}}

\\begin{{document}}

\\title{{Your Paper Title}}

\\author{{\\IEEEauthorblockN{{Anonymous Author(s)}}
\\IEEEauthorblockA{{Anonymous Institution}}}}

\\maketitle

\\begin{{abstract}}
Your abstract here.
\\end{{abstract}}

\\section{{Introduction}}
\\label{{sec:intro}}

Your introduction here.

% TODO: Add your content sections here

\\section{{Discussion}}
\\label{{sec:discussion}}

\\subsection{{Threats to Validity}}
% Required for SE papers

\\bibliographystyle{{IEEEtran}}
\\bibliography{{references}}

\\end{{document}}
'''

    main_path = output_dir / "main.tex"
    main_path.write_text(content)
    print(f"Created: main.tex")
    print(f"  Document class: \\documentclass[{options_str}]{{{config['template']}art}}")


def print_venue_info(venue: str, config: dict):
    """Print venue-specific information for the user."""
    print("\n" + "=" * 60)
    print(f"VENUE: {venue}")
    print("=" * 60)
    print(f"Template type: {config['template'].upper()}")
    print(f"Document class: {config['doc_class']}")
    print(f"Options: {', '.join(config.get('options', []))}")
    print(f"Page limit: {config.get('page_limit', 'N/A')} pages")
    if config.get("page_limit_note"):
        print(f"  Note: {config['page_limit_note']}")
    print(f"Layout: {config.get('layout', 'N/A')}")
    if config.get("cfp_url"):
        print(f"CFP: {config['cfp_url']}")
    if config.get("submission_url"):
        print(f"Submit: {config['submission_url']}")
    if config.get("required_sections"):
        print(f"Required sections: {', '.join(config['required_sections'])}")
    if config.get("notes"):
        print("Notes:")
        for note in config["notes"]:
            print(f"  - {note}")
    print("=" * 60)
    print("\nIMPORTANT: Always verify requirements at the official CFP before submission!")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Fetch latest LaTeX templates with venue-specific requirements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --venue ISSTA2026 --output ./paper/
  %(prog)s --venue ICSE2026 --output ./paper/ --create-main
  %(prog)s --venue FSE2026 --output ./paper/ --info-only

Supported venues (verify CFP for current requirements):
  ACM: ISSTA, FSE, OOPSLA, PLDI, POPL, CCS, CHI, SIGMOD, SOSP, ASPLOS
  IEEE: ICSE, ASE, ICSME, SANER, MSR, ISSRE, ICST, S&P
        """
    )
    parser.add_argument("--venue", required=True, help="Venue name (e.g., ISSTA2026, ICSE2026)")
    parser.add_argument("--output", help="Output directory for template files")
    parser.add_argument("--create-main", action="store_true", help="Create main.tex with venue-specific settings")
    parser.add_argument("--info-only", action="store_true", help="Only print venue info, don't download")
    args = parser.parse_args()

    config = get_venue_config(args.venue)
    print_venue_info(args.venue, config)

    if args.info_only:
        return

    if not args.output:
        print("Error: --output is required unless using --info-only")
        sys.exit(1)

    output_dir = Path(args.output)

    info = fetch_template(config["template"], output_dir)
    print(f"\nTemplate version: {info['version']}")
    print(f"Files: {', '.join(info['files'])}")

    if args.create_main:
        create_main_tex(output_dir, args.venue, config)

    print("\nDone!")


if __name__ == "__main__":
    main()
