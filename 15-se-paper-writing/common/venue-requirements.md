# Venue Requirements

[← Back to Main](../SKILL.md)

Page limits, formats, and specific requirements for major SE venues.

## Conference Requirements

| Venue | Type | Pages | Format | Document Class | Key Requirement |
|-------|------|-------|--------|----------------|-----------------|
| **ICSE 2026** | Technical | 11 | 2-col | IEEEtran | Data availability |
| **ICSE 2026** | SEIP | 10 | 2-col | IEEEtran | Industry relevance |
| **FSE 2026** | Research | 18 | 1-col | acmart acmsmall | Artifacts encouraged |
| **ASE 2026** | Full | 11 | 2-col | IEEEtran | Reproducibility package |
| **ISSTA 2026** | Full | 11 | 1-col | acmart acmsmall | Test artifact required |
| **MSR 2026** | Full | 11 | 2-col | IEEEtran | Data track available |
| **OOPSLA 2026** | Full | 23 | 1-col | acmart acmsmall | Extensive evaluation |
| **PLDI 2026** | Full | 12+2 | 1-col | acmart acmsmall | Formal content |

## Journal Requirements

| Journal | Pages | Format | Special Notes |
|---------|-------|--------|---------------|
| **TSE** | ~25 | IEEE 1-col | Extended evaluation expected |
| **TOSEM** | ~30 | ACM | Longer related work |
| **EMSE** | ~30 | Springer | Replication package required |

## Universal Requirements

All top-tier SE venues require:

- **Double-blind review**: Anonymize submissions
- **References**: Don't count toward page limit
- **Artifacts**: Expected (not always mandatory)
- **Threats to validity**: Required section
- **Statistical analysis**: Effect sizes for empirical claims

---

## Document Class Details

### ACM Venues (FSE, ISSTA, OOPSLA, PLDI)

**IMPORTANT**: Different ACM venues use different document classes:

| Format | Document Class | Venues | Layout |
|--------|----------------|--------|--------|
| `acmsmall` | Single-column | ISSTA, FSE, OOPSLA, PLDI | Journal-style |
| `sigconf` | Two-column | CCS, SIGMOD | Conference-style |

### ISSTA/FSE/OOPSLA (acmsmall)

```latex
\documentclass[acmsmall,screen,review,anonymous]{acmart}

% Disable ACM-specific items for submission
\settopmatter{printacmref=false}
\renewcommand\footnotetextcopyrightpermission[1]{}
\pagestyle{plain}

\begin{document}
\title{Your Paper Title}

% ... content ...

% REQUIRED for ISSTA: Data Availability
\section*{Data Availability}
Our replication package is available at: [URL].

\bibliographystyle{ACM-Reference-Format}
\bibliography{references}
\end{document}
```

### IEEE Venues (ICSE, ASE, MSR)

```latex
\documentclass[conference]{IEEEtran}

\begin{document}
\title{Your Paper Title}

\author{\IEEEauthorblockN{Anonymous Author(s)}
\IEEEauthorblockA{Anonymous Institution}}

\maketitle

\begin{abstract}
Your abstract here...
\end{abstract}

% ... content ...

\bibliographystyle{IEEEtran}
\bibliography{references}
\end{document}
```

---

## Venue-Specific Requirements

### ICSE

- **Technical Track**: 11 pages
- **SEIP Track**: 10 pages (industry focus)
- **Demo Track**: 4 pages
- **Data availability statement** encouraged
- Format: IEEE two-column

### FSE

- **Research Track**: 18 pages
- **Industry Track**: 10 pages
- **Artifacts strongly encouraged**
- Format: ACM single-column (acmsmall)

### ISSTA

- **Full Papers**: 11 pages
- **Tool Papers**: 6 pages
- **Test artifact required** for evaluation
- **Data Availability section required**
- Format: ACM single-column (acmsmall)

### ASE

- **Full Papers**: 11 pages
- **Short Papers**: 6 pages
- **Tool Track**: 4 pages
- Reproducibility package expected
- Format: IEEE two-column

### MSR

- **Full Papers**: 11 pages
- **Short Papers**: 4 pages
- **Data Track**: Separate submission for datasets
- Mining-focused evaluation expected
- Format: IEEE two-column

---

## Template Sources

| Format | Source | URL |
|--------|--------|-----|
| ACM | CTAN acmart | https://www.ctan.org/pkg/acmart |
| IEEE | CTAN IEEEtran | https://www.ctan.org/pkg/ieeetran |
| ACM | GitHub | https://github.com/borisveytsman/acmart |

### Fetching Templates

Always fetch the latest templates before submission:

```bash
# Check venue requirements first
python fetch_template.py --venue ISSTA2026 --info-only

# Fetch and create main.tex
python fetch_template.py --venue ISSTA2026 --output ./paper/ --create-main
```

---

## Anonymization Requirements

For double-blind venues:

- [ ] Author names removed from paper
- [ ] Institution names removed
- [ ] Self-citations anonymized ("Prior work [anonymous]" or "Our prior work [omitted]")
- [ ] GitHub links anonymized or use anonymous submission URL
- [ ] Acknowledgments removed or anonymized
- [ ] PDF metadata cleared

---

## CFP Links (2026)

- **ICSE**: https://conf.researchr.org/track/icse-2026/icse-2026-research-track
- **FSE**: https://conf.researchr.org/track/fse-2026/fse-2026-research-papers
- **ASE**: https://conf.researchr.org/home/ase-2026
- **ISSTA**: https://conf.researchr.org/track/issta-2026/issta-2026-research-papers
- **MSR**: https://conf.researchr.org/home/msr-2026

**Always verify requirements against the official CFP** before submission—requirements may change.

[Back to Main →](../SKILL.md)
