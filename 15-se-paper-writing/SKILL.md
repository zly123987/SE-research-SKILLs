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

Expert-level guidance for writing publication-ready papers targeting **ICSE, FSE/ESEC, ASE, ISSTA, MSR, TSE, TOSEM, and EMSE**. This skill combines SE research writing conventions with practical tools: LaTeX templates, evaluation checklists, and venue-specific requirements.

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
| **Visual Overflow Checker** | [scripts/check_visual_overflow.py](scripts/check_visual_overflow.py) | Post-compilation PDF visual inspection using Claude vision. Detects text/table/figure overflow, applies fixes, recompiles until clean. Integrated into `compile_and_fix_loop()` automatically. |

---

## When to Use This Skill

Use this skill when:
- **Starting from a research project** to write for SE venues
- **Drafting technique papers** with tool evaluation
- **Writing empirical studies** with statistical analysis
- **Preparing tool/demo papers** for ICSE/ASE
- **Formatting** for SE conference submission
- **Converting** between venues (ICSE → FSE, etc.)

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

3. Approach / Methodology (2-3 pages)  → sections/03-methodology.md
   - Overview/architecture diagram
   - Technical details as flowing prose
   - Algorithm or pseudocode if needed
   - Running example walkthrough

4. Implementation (0.5-1 page)
   - Tool name and availability
   - Key implementation choices

5. Evaluation (4-6 pages)              → sections/04-evaluation.md
   - Research questions defined
   - Experimental setup
   - Results per RQ with "Answering RQ" boxes
   - Error analysis and ablation

6. Discussion (0.5-1 page)             → sections/05-discussion.md
   - Threats to validity (required)
   - Limitations (recommended for prototype papers)
   - Lessons learned (optional, typically for empirical studies)

7. Related Work (1-1.5 pages)          → sections/06-related-work.md

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

---

## Common Pitfalls

| Issue | Problem | Fix |
|-------|---------|-----|
| Weak Motivation | Jumps to solution without need | Add concrete motivating example |
| Missing Baselines | No comparison to recent work | Include last 3 years of SOTA |
| No Statistics | Raw numbers only | Add Wilcoxon + effect sizes |
| Overclaiming | Claims exceed evidence | Scope claims precisely |
| Bullet-heavy | Lists instead of prose | Write flowing paragraphs |
| Bullets without leftmargin=* | No option listed for itemize or enumerate | Add leftmargin=* with package |
| Use Dash | use dashes everywhere | Use comma or phrase which-is |
| Overly use \emph or \textbf | Use many commands | Only use them when necessary |
| Repeated expressions | One meaning is repeated with different wording  | Use concise expressions |
| Missing references | ?? in pdf  | Consistent references |
---

---

## Exemplar Writing Patterns (Final Step)

After completing your draft, verify it follows these patterns observed in award-winning SE papers (CORAL [ICSE'23 Distinguished Paper], Ranger [ASE'23], Sembid [ASE'22]):

### 1. Problem-Driven Narrative
**Pattern:** Problem → Mechanism of Harm → Why Hard → Solution Directly Addresses Difficulty

Each paper opens by showing *what breaks* (not just "affects X%"):
- CORAL: "ineffective remediation could induce side effects, such as compilation failures"
- Sembid: "users could still confront abnormal execution and crash after upgrades"
- Ranger: "vulnerabilities persistent in the Maven ecosystem (e.g., the notorious Log4Shell)"

**Checklist:**
- [ ] Does the problem statement name specific failures (build, crash, security)?
- [ ] Is the difficulty explained (not just "existing tools are limited")?
- [ ] Does the solution directly address the stated difficulty?

### 2. Empirical-First Structure
**Pattern:** Empirical study → Findings motivate tool design → Tool evaluated against findings

Strong papers don't just propose tools—they first *study the problem empirically*:
- Sembid: "conducted an empirical study on 180 SemB issues to understand the root causes"
- Ranger: "first carried out an empirical study to examine the prevalence of persistent vulnerabilities"
- CORAL: empirical study reveals 21.55% vulnerabilities impossible to fix by upgrading

**Checklist:**
- [ ] Is there an empirical study/analysis before proposing the solution?
- [ ] Do empirical findings directly motivate design decisions?
- [ ] Does evaluation connect back to initial empirical observations?

### 3. Concrete Quantitative Claims
**Pattern:** Specific numbers with baselines and statistical context

Avoid vague claims. Use precise numbers with comparisons:
- "87.56% of vulnerabilities fixed (best competitor: 75.32%)"
- "90.26% recall and 81.29% precision"
- "detected over 3× more SemB APIs than unit tests"

**Checklist:**
- [ ] Are all claims backed by specific percentages?
- [ ] Is there always a baseline for comparison?
- [ ] Are improvements stated as concrete deltas (not "significantly better")?

### 4. Layered Contribution Structure
**Pattern:** Mixed empirical + technical contributions, clearly enumerated

Contributions combine study findings with technical novelty:
```
1. Empirical study revealing [finding] on [N] subjects
2. Technique/tool [Name] that [addresses finding]
3. Evaluation showing [quantitative improvement]
4. [Optional] Dataset/benchmark for future research
```

### 5. Memorable Tool Naming
**Pattern:** Short, pronounceable names that hint at function

- CORAL → "Compatible Remediation"
- Ranger → "Range Restoration"
- Sembid → "Semantic Breaking Issue Detector"
- PANACEA → universal remedy (fitting for dependency healing)

### 6. Tight Problem-Solution Correspondence
**Pattern:** Every difficulty mentioned must map to a solution component

| Stated Difficulty | Solution Component |
|-------------------|-------------------|
| "implicit constraints require domain knowledge" | LLM-based semantic reasoning |
| "transitive conflicts invisible in project files" | dynamic resolution |
| "compilation failures from incompatible fixes" | validation layer |

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
