---
name: se-paper-writing
description: Write publication-ready papers for top-tier SE venues (ICSE, FSE, ASE, ISSTA, MSR, TSE, EMSE). Use when drafting papers from research projects, structuring empirical studies, preparing tool papers, or formatting camera-ready submissions. Includes LaTeX templates, reviewer guidelines, and SE-specific writing patterns.
version: 1.0.0
author: SE Research Skills
license: MIT
tags: [Academic Writing, ICSE, FSE, ASE, ISSTA, MSR, TSE, LaTeX, Paper Writing, Software Engineering]
dependencies: [texlive-full, bibtex]
---

# SE Paper Writing for Top-Tier Venues

Guidance for writing papers targeting **ICSE, FSE/ESEC, ASE, ISSTA, MSR, TSE, TOSEM, and EMSE**. This skill combines SE research writing conventions with practical tools: LaTeX templates, evaluation checklists, and venue-specific requirements. Treat the output as drafts that require author review — see the repository's [integrity notice](../CLAUDE.md#use--integrity-notice).

## Quick Navigation

This skill is organized into modular files for easy reference:

### Paper Sections
| Section | File | Description |
|---------|------|-------------|
| Abstract | [sections/00-abstract.md](sections/00-abstract.md) | 5-sentence structure: background→problem→difficulty→solution→results |
| Introduction | [sections/01-introduction.md](sections/01-introduction.md) | Funnel structure, key insight, contributions |
| Background & Motivation | [sections/02-background.md](sections/02-background.md) | Background concepts, motivating examples |
| Methodology | [sections/03-methodology.md](sections/03-methodology.md) | Approach writing, ReAct pattern, algorithms |
| Evaluation | [sections/04-evaluation.md](sections/04-evaluation.md) | RQs, baselines, metrics, error analysis |
| Discussion | [sections/05-discussion.md](sections/05-discussion.md) | Threats to validity (required), limitations, optional lessons learned |
| Related Work | [sections/06-related-work.md](sections/06-related-work.md) | Organization, differentiation, depth |
| Conclusion | [sections/07-conclusion.md](sections/07-conclusion.md) | Summary and future work |
| **Final Check** | [sections/08-final-check.md](sections/08-final-check.md) | Whole-paper audit: page budget, reviewer focus, claim traceability, language quality |
| **Artifact Repo** | [sections/09-artifact-repository.md](sections/09-artifact-repository.md) | Standalone anonymous repo setup, README template, anonymization, GitHub push |

### Common Guidelines
| Topic | File | Description |
|-------|------|-------------|
| Paper Types | [common/paper-types.md](common/paper-types.md) | Technique, empirical, tool papers |
| Venue Requirements | [common/venue-requirements.md](common/venue-requirements.md) | Page limits, formats per venue |
| Writing Style | [common/writing-style.md](common/writing-style.md) | SE terminology, precision, avoiding overclaims |
| Citations | [common/citations.md](common/citations.md) | Citation workflow, BibTeX validation |
| Statistical Analysis | [common/statistics.md](common/statistics.md) | Tests, effect sizes, reporting |
| Artifacts | [common/artifacts.md](common/artifacts.md) | Reproducibility packages, badges, Zenodo |
| **Compliance** | [common/compliance.md](common/compliance.md) | Template compliance check & auto-remediation |

### Templates & Checklists
| Resource | File | Description |
|----------|------|-------------|
| LaTeX Templates | [templates/latex-templates.md](templates/latex-templates.md) | ACM, IEEE templates by venue |
| Reviewer Checklist | [checklists/reviewer-checklist.md](checklists/reviewer-checklist.md) | What reviewers look for |
| Submission Checklist | [checklists/submission-checklist.md](checklists/submission-checklist.md) | Pre-submission verification |
| **Exemplar Patterns** | [Jump to section](#exemplar-writing-patterns-final-step) | Writing style from award-winning papers |

### Scripts & Automation
| Script | File | Description |
|--------|------|-------------|
| **Post-Process Pipeline** | [scripts/postprocess_paper.py](scripts/postprocess_paper.py) | 13-step automated cleanup: BibTeX sanitization, citation normalization, TikZ validation, LaTeX syntax fixing, dangling citation removal. Run after paper is drafted, before final compilation. Use `--visual` to add Claude Vision overflow check. |
| **Visual Overflow Checker** | [scripts/check_visual_overflow.py](scripts/check_visual_overflow.py) | Post-compilation PDF visual inspection using a multimodal LLM (e.g., Anthropic's Claude via the Claude Agent SDK). Detects text/table/figure overflow, applies fixes, recompiles until clean. Called automatically by `postprocess_paper.py --visual`. Optional integration; subject to the provider's own terms and costs. |
| **Citation Consistency Checker** | [scripts/check_citation_consistency.py](scripts/check_citation_consistency.py) | Three-check citation verification: (1) context consistency — author/year mismatch between prose and BibTeX (Step 12b), (2) missing citations — uncited tools, techniques, datasets, metrics (Step 12c), (3) semantic consistency — LLM-based claim-vs-title check (requires Claude Agent SDK). |
| **Post-Process Module** | [scripts/tex_postprocess/](scripts/tex_postprocess/) | Self-contained Python package (stdlib only) implementing all pipeline steps; no external dependencies required. Key modules: `post_process.py` (orchestrator), `bib_sanitizer.py`, `normalize_citations.py`, `tex_checker.py`, `tikz_visual_validator.py`, `citation_context_checker.py`. |

---

## When to Use This Skill

Use this skill when:
- **Starting from a research project** to write for SE venues
- **Drafting technique papers** with tool evaluation
- **Writing empirical studies** with statistical analysis
- **Preparing tool/demo papers** for ICSE/ASE
- **Formatting** for SE conference submission
- **Converting** between venues (ICSE → FSE, etc.)
- **Reviewing** SE papers (use checklists to evaluate others' work)
---

## Core SE Paper Types

SE venues accept several distinct paper types. **Identify your paper type first**—it determines structure, evaluation expectations, and page limits.

| Paper Type | What It Contributes | Typical Venues |
|------------|---------------------|----------------|
| **Technique Paper** | New method/algorithm + tool + evaluation | ICSE, FSE, ASE |
| **Empirical Study** | Large-scale analysis answering research questions | FSE, MSR, EMSE |
| **Tool Paper** | Mature, publicly available tool with novel features | ICSE Demo, ASE Tool |
| **Benchmark Paper** | New dataset/benchmark for community use | MSR Data, ISSTA |
| **Replication Study** | Reproduce + extend prior work | MSR, EMSE |
| **Experience Report** | Industry practice or lessons learned | ICSE SEIP |

See [common/paper-types.md](common/paper-types.md) for detailed structure per type.

---

## Technique Paper Structure (Quick Reference)

The most common SE paper type. Full details in individual section files.

```
0. Abstract (150-250 words)           → sections/00-abstract.md
   - Background → Problem (immediate)
   - Problem severity (conservative, data-backed)
   - Why it's hard to solve
   - Our solution + key insight
   - Results with baseline comparison

1. Introduction (1.5-2 pages)         → sections/01-introduction.md
   - Problem and motivation
   - Limitations of existing approaches
   - Key insight/contribution
   - Contribution bullets (3-4 items)

2. Background and Motivation (1-1.5 pages)  → sections/02-background.md
   - Background: necessary concepts
   - Motivating example: concrete case
   - Why existing tools fail

3. Approach / Methodology (3-5 pages)  → sections/03-methodology.md
   - Overview/architecture diagram
   - Technical details as flowing prose
   - Algorithm or pseudocode if needed
   - Running example walkthrough

4. Implementation (0.5-1 page)
   - Tool name and availability
   - Key implementation choices

5. Evaluation (4-5 pages)              → sections/04-evaluation.md
   - Research questions defined
   - Experimental setup
   - Results per RQ with "Answering RQ" boxes
   - Error analysis and ablation

6. Discussion (0.5-1 page)             → sections/05-discussion.md
   - Threats to validity (required)
   - Limitations (recommended for prototype papers)
   - Lessons learned (optional, typically for empirical studies)

7. Related Work (0.75-1 page)          → sections/06-related-work.md

8. Conclusion (0.5 page)               → sections/07-conclusion.md
```

---

## Universal SE Requirements

All top-tier SE venues expect:

- **Double-blind review** (anonymize submissions)
- **References don't count** toward page limit
- **Artifact/replication package** expected (not always mandatory)
- **Threats to validity section** required
- **Statistical analysis** with effect sizes for empirical claims
- **Threshold justification (HARD RULE)**: every numeric threshold or cutoff
  appearing in the paper (similarity ≥ X, confidence > Y, top-k, agreement
  level, p-value cutoff, window size, frequency floor, decision boundary,
  etc.) MUST be justified in-text by one of: (a) an empirical sweep /
  sensitivity analysis on the actual data, (b) a citation to prior work that
  uses the same value for the same purpose, or (c) a formal derivation. A
  bare "we use 0.7" without a verifiable reason is treated by reviewers as
  arbitrary tuning and is a common ASE/ICSE rejection cause.

---

## Common Pitfalls

| Issue | Problem | Fix |
|-------|---------|-----|
| Weak Motivation | Jumps to solution without need | Add concrete motivating example |
| Missing Baselines | No comparison to recent work | Include last 3 years of SOTA |
| No Statistics | Raw numbers only | Add Wilcoxon + effect sizes |
| Overclaiming | Claims exceed evidence | Scope claims precisely |
| Bullet-heavy | Lists instead of prose | Write flowing paragraphs |
| Bullets without `leftmargin=*` | `itemize`/`enumerate` indented excessively | Add `[leftmargin=*]` (or use the `enumitem` package) |
| Excessive em-dashes | Dashes used in place of commas or restructured clauses | Replace with commas, parentheses, or rewritten sentences |
| Overuse of `\emph` / `\textbf` | Emphasis loses meaning when applied too often | Apply only where the emphasis is semantically necessary |
| Redundant phrasing | The same meaning repeated with different wording | Collapse repeated meanings into a single concise expression |
| Missing references | `??` in the rendered PDF | Re-run `bibtex` and recompile; ensure `\cite{}` keys match the `.bib` |
---

---

## Exemplar Writing Patterns (Final Step)

After completing your draft, verify it follows these patterns commonly observed in well-received SE papers at top venues. Each pattern is illustrated with a **generic template** rather than named paper quotes — adapt to your domain.

### 1. Problem-Driven Narrative
**Pattern:** Problem → Mechanism of Harm → Why Hard → Solution Directly Addresses Difficulty

Open by showing *what breaks* in concrete terms, not just an aggregate prevalence number. Strong opening sentences typically name a specific failure mode (compilation failure, runtime crash, exploited vulnerability, missed test, slow query) before any percentage figure appears.

**Checklist:**
- [ ] Does the problem statement name a specific failure (build, crash, security, performance)?
- [ ] Is the difficulty explained (not just "existing tools are limited")?
- [ ] Does the solution directly address the stated difficulty?

### 2. Empirical-First Structure
**Pattern:** Empirical study → Findings motivate tool design → Tool evaluated against findings

Strong technique papers often begin with an empirical study of the problem on a non-trivial corpus, then derive design decisions from the empirical findings, and finally evaluate the tool against the same observations. The empirical preamble both justifies the design and provides ready-made baselines for the evaluation.

**Checklist:**
- [ ] Is there an empirical study/analysis before proposing the solution?
- [ ] Do empirical findings directly motivate design decisions?
- [ ] Does the evaluation connect back to the initial empirical observations?

### 3. Concrete Quantitative Claims
**Pattern:** Specific numbers with baselines and statistical context

Avoid vague claims. Use precise numbers with explicit comparisons. For example:
- "X.X% of [items] [outcome] (best competitor: Y.Y%)"
- "X.X% recall and Y.Y% precision over [dataset]"
- "detected over N× more [items] than [baseline]"

**Checklist:**
- [ ] Are all claims backed by specific numbers?
- [ ] Is there always a baseline for comparison?
- [ ] Are improvements stated as concrete deltas (not "significantly better")?

### 4. Layered Contribution Structure
**Pattern:** Mixed empirical + technical contributions, clearly enumerated

Contributions in a technique paper typically combine study findings with technical novelty:
```
1. Empirical study revealing [finding] on [N] subjects
2. Technique/tool [Name] that [addresses finding]
3. Evaluation showing [quantitative improvement]
4. [Optional] Dataset/benchmark for future research
```

### 5. Memorable Tool Naming
**Pattern:** Short, pronounceable names that hint at function

A good tool name is one or two syllables, easy to say aloud, and either an acronym whose expansion describes the function or a metaphor that maps to the domain (e.g., a name evoking the artefact's effect on the system). Avoid names already used by widely-known tools or trademarks.

### 6. Tight Problem-Solution Correspondence
**Pattern:** Every difficulty mentioned must map to a solution component

Build a small table linking each stated difficulty to the specific solution component that addresses it. If a difficulty appears in the introduction without a corresponding entry in the approach/evaluation, reviewers will notice — either drop the difficulty or add the component.

| Stated Difficulty | Solution Component |
|-------------------|-------------------|
| (e.g., "implicit constraints require domain knowledge") | (e.g., domain-aware reasoning module) |
| (e.g., "cross-file dependencies invisible in single-file analysis") | (e.g., whole-program graph construction) |
| (e.g., "downstream breakage from local fixes") | (e.g., validation/regression layer) |

**If you state a difficulty but don't address it, reviewers will notice.**

### Quick Self-Check Before Submission

Read your abstract and introduction aloud. Ask:
1. **"So what?"** after each sentence—does the next sentence answer it?
2. **"Why is this hard?"**—is it specific (not "this is challenging")?
3. **"How does the solution address this?"**—is the connection explicit?

If any answer is unclear, revise until the narrative chain is tight.

---

## References

- **ICSE**: https://conf.researchr.org/home/icse-2026
- **FSE**: https://2026.esec-fse.org/
- **ASE**: https://conf.researchr.org/home/ase-2026
- **ISSTA**: https://conf.researchr.org/home/issta-2026
- **MSR**: https://conf.researchr.org/home/msr-2026
