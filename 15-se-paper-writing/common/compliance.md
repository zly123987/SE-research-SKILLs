# Template Compliance & Automated Remediation

[← Back to Main](../SKILL.md)

Automated workflow for checking and fixing venue template compliance.
The **metacognition layer** reads this file to know what to check, how to fix,
and what OPTIONS to present to the user for supervision.

---

## Compliance Check Workflow

When a paper directory exists, run these checks **before** any writing proceeds:

```
1. DETECT  — Parse main.tex for document class, options, bib style
2. COMPARE — Check against venue requirements (see venue-requirements.md)
3. REPORT  — Show pass/fail/warn for each check
4. REMEDIATE — If failures found, present OPTIONS to user
```

### Checks (in order)

| # | Check | Source | Pass Condition |
|---|-------|--------|----------------|
| 1 | Document class | `\documentclass{...}` in main.tex | Matches venue's required class |
| 2 | Class options | `\documentclass[...]{...}` | Contains all required options |
| 3 | Bibliography style | `\bibliographystyle{...}` | Matches venue's required style |
| 4 | Anonymization | `\author{...}` content | No real names for double-blind venues |
| 5 | Page count | Compiled PDF page count | Within venue page limit |
| 6 | References | references.bib entry count | 25+ for top-tier venues |
| 7 | Sections | sections/*.tex file count | 6+ non-empty section files |

**Important**: Only check active (non-commented) LaTeX lines — lines starting with `%` are excluded.

---

## Template Download Sources

The actuator downloads template files from CTAN (the authoritative source).

### ACM Templates (FSE, ISSTA, OOPSLA, PLDI, CCS)

| File | Direct URL | Notes |
|------|-----------|-------|
| Full package (zip) | `https://ctan.org/tex-archive/macros/latex/contrib/acmart.zip` | Contains .dtx + .ins source |
| `ACM-Reference-Format.bst` | `https://tug.ctan.org/macros/latex/contrib/acmart/ACM-Reference-Format.bst` | Direct download |

**To generate `acmart.cls` from the zip**:
```bash
cd <extracted_dir>
latex acmart.ins    # Generates acmart.cls from acmart.dtx
```

**Alternative** (pre-built, third-party mirror):
- `https://raw.githubusercontent.com/conference-websites/acmart-sigproc-template/master/acmart.cls`

### IEEE Templates (ICSE, ASE, MSR, SANER)

| File | Direct URL | Notes |
|------|-----------|-------|
| `IEEEtran.cls` | `https://tug.ctan.org/macros/latex/contrib/IEEEtran/IEEEtran.cls` | Direct download (v1.8b) |
| `IEEEtran.bst` | `https://tug.ctan.org/biblio/bibtex/contrib/IEEEtran/IEEEtran.bst` | Direct download (v1.14) |

### Download Procedure

The actuator should use `fetch_template.py` from this skill:

```bash
# Info only — show venue requirements
python SE-research-SKILLs/15-se-paper-writing/fetch_template.py \
    --venue FSE2026 --info-only

# Download template files to paper directory
python SE-research-SKILLs/15-se-paper-writing/fetch_template.py \
    --venue FSE2026 --output <paper_dir>

# Download and create a fresh main.tex
python SE-research-SKILLs/15-se-paper-writing/fetch_template.py \
    --venue FSE2026 --output <paper_dir> --create-main
```

---

## Remediation Workflow (Metacog → User → Actuator)

When compliance check finds failures, the metacognition layer presents OPTIONS
to the user for approval before the actuator acts.

### Decision Tree

```
COMPLIANCE CHECK RESULT
│
├── All PASS → Proceed with paper writing
│
├── Document class FAIL
│   └── OPTIONS:
│       A. [RECOMMENDED] Download venue template and convert main.tex
│          - Actuator: fetch_template.py → download .cls + .bst
│          - Actuator: Rewrite main.tex preamble to use correct class
│          - Actuator: Recompile and verify
│       B. Keep current format for drafting, convert later
│          - Risk: Page count estimates will be inaccurate
│       C. Manual fix — user will handle template setup
│
├── Bibliography style WARN
│   └── OPTIONS:
│       A. [RECOMMENDED] Auto-fix bibliography style
│          - Actuator: Replace \bibliographystyle{X} with correct style
│          - Actuator: Download .bst file if not present
│       B. Keep current style for now
│
├── Page count FAIL
│   └── OPTIONS:
│       A. [RECOMMENDED] Convert to venue template first (fixes page count)
│          - 2-column format typically halves single-column page count
│       B. Trim content to fit page limit
│       C. Defer — expected when using draft format
│
├── Anonymization WARN
│   └── OPTIONS:
│       A. [RECOMMENDED] Auto-anonymize author information
│       B. User will handle anonymization
│
└── Multiple FAILs
    └── OPTIONS:
        A. [RECOMMENDED] Full template conversion
           - Download all template files
           - Convert main.tex to venue format
           - Fix bibliography style
           - Recompile and re-check
        B. Fix issues one by one (interactive)
        C. Defer all fixes to later
```

### Full Template Conversion Steps

When user approves Option A (full conversion), the actuator executes:

```
Step 1: Download template files
  → Run: fetch_template.py --venue <VENUE> --output <paper_dir>
  → Verify: .cls and .bst files exist in paper_dir

Step 2: Update main.tex preamble
  → Replace \documentclass line with venue-correct version
  → Replace \bibliographystyle with venue-correct version
  → Add/remove venue-specific preamble (e.g., \settopmatter for ACM)
  → Preserve all \input{sections/...} lines
  → Preserve all custom \newcommand definitions

Step 3: Recompile
  → Run: pdflatex main && bibtex main && pdflatex main && pdflatex main
  → Check for compilation errors
  → If errors: diagnose and fix (missing packages, incompatible commands)

Step 4: Re-check compliance
  → Run compliance check again
  → Report updated status to user
```

### What to Preserve During Conversion

When converting main.tex from one format to another, the actuator MUST preserve:

- All `\input{sections/...}` includes
- All `\newcommand` and `\renewcommand` definitions
- All `\usepackage` lines (check compatibility with new class)
- All custom color definitions (`\definecolor`)
- All listing style definitions (`\lstdefinestyle`)
- The `\bibliography{references}` line
- Any `\tikzlibrary` imports

### What to Change During Conversion

- `\documentclass` line → venue-correct class and options
- `\bibliographystyle` → venue-correct style
- `\author` block → format-specific (ACM vs IEEE have different syntax)
- Remove `\geometry` package (class handles margins)
- Add ACM-specific: `\settopmatter`, `\footnotetextcopyrightpermission`
- Add IEEE-specific: `\IEEEauthorblockN`, `\IEEEauthorblockA`

---

## Metacognition Responsibilities

The metacognition layer (NOT the actuator) is responsible for:

1. **Reading this skill** to understand the compliance workflow
2. **Running the compliance check** on the paper directory
3. **Interpreting results** against venue requirements
4. **Presenting OPTIONS** to the user with one marked RECOMMENDED
5. **Dispatching the actuator** only after user approves
6. **Verifying actuator output** (re-check compliance after fix)
7. **Logging the decision** for reproducibility

### Example Metacog Flow

```
METACOG: "Paper compliance check for FSE 2026:"
METACOG: "  Document class: FAIL (article → should be acmart)"
METACOG: "  Bibliography:   WARN (plainnat → should be ACM-Reference-Format)"
METACOG: "  Page count:     FAIL (22 pages, limit 18)"
METACOG: ""
METACOG: "OPTIONS:"
METACOG: "  A. [RECOMMENDED] Full template conversion"
METACOG: "     → Download acmart.cls + ACM-Reference-Format.bst"
METACOG: "     → Convert main.tex to \documentclass[acmsmall,screen,review,anonymous]{acmart}"
METACOG: "     → Recompile and verify"
METACOG: "  B. Fix one issue at a time"
METACOG: "  C. Keep current format (draft mode)"
USER:    → selects A
METACOG: "Dispatching actuator to convert template..."
ACTUATOR: → downloads templates, converts main.tex, recompiles
METACOG: "Re-checking compliance..."
METACOG: "  All checks: PASS"
```

---

## Visual Overflow Check (Post-Compilation Quality Gate)

After the paper compiles cleanly (all 7 checks above pass), a **visual overflow check** inspects the compiled PDF using Claude's vision capability to catch layout problems that LaTeX warnings miss or understate.

### Script

**`SE-research-SKILLs/15-se-paper-writing/scripts/check_visual_overflow.py`** — standalone CLI wrapper.

**Core module**: `research_agency/paper_utils/visual_checker.py` — integrated into `compile_and_fix_loop()` automatically.

### What It Catches

| Issue | Example | LaTeX Warning? |
|-------|---------|----------------|
| Table wider than column | 7-column table in 2-col format | Sometimes (Overfull hbox) |
| Figure beyond margins | TikZ diagram not in resizebox | Sometimes |
| Code listing overflow | Long lines in lstlisting | No |
| URL overflow | Long URLs without `\url{}` | Sometimes |
| Text/figure overlap | Float placement collision | No |
| Margin violations | Content crossing into margins | Partial |

### How It Works

```
1. Render each PDF page to PNG (PyMuPDF, 200 DPI)
2. Send page image to Claude SDK (allowed_tools=["Read"])
3. Claude inspects visually → returns JSON array of issues
4. Map issues to .tex source (via aux file + source_hint grep)
5. Apply targeted fixes (resizebox, breaklines, width=\columnwidth, etc.)
6. Recompile (single pdflatex pass)
7. Re-check ONLY affected pages (token efficiency)
8. Repeat up to 3 iterations
```

### Usage

```bash
# Standalone check + fix
python SE-research-SKILLs/15-se-paper-writing/scripts/check_visual_overflow.py \
    projects/my-project/paper/ASE2026/

# Check only (no auto-fix)
python SE-research-SKILLs/15-se-paper-writing/scripts/check_visual_overflow.py \
    projects/my-project/paper/ASE2026/ --check-only

# Check specific pages
python SE-research-SKILLs/15-se-paper-writing/scripts/check_visual_overflow.py \
    projects/my-project/paper/ASE2026/ --pages 3,5,7-10
```

### Integration

The visual checker runs **automatically** at the end of `compile_and_fix_loop()` after successful compilation. Results appear in the return dict:

```python
result = compile_and_fix_loop(paper_dir)
visual = result.get("visual_check", {})
if visual.get("remaining_issues", 0) > 0:
    # Some issues could not be auto-fixed
    for detail in visual.get("remaining_issues_detail", []):
        print(f"  Page {detail['page']}: {detail['type']} — {detail['description']}")
```

### Auto-Fix Strategies

| Issue Type | Fix Applied |
|-----------|-------------|
| `table_overflow` | Wrap `tabular` in `\resizebox{\columnwidth}{!}{...}` |
| `figure_overflow` | Set `\includegraphics` width to `\columnwidth` |
| `listing_overflow` | Add `breaklines=true` to lstlisting options |
| `text_overflow` | Add `\usepackage{microtype}`, wrap URLs in `\url{}` |
| `overlap` | Adjust float placement to `[!htbp]` |

---

## Notes

- **FSE 2026** uses `acmsmall` (single-column), NOT `sigconf` (two-column).
  The page limit is 18 pages in single-column format.
  See: https://conf.researchr.org/track/fse-2026/fse-2026-research-papers
- **ICSE 2026** uses IEEE `IEEEtran` two-column, 11 pages.
- Template files should be downloaded to the **paper directory** (not system-wide)
  so each project is self-contained.
- Always verify against the official CFP — venue requirements may change.

[Back to Main →](../SKILL.md)
