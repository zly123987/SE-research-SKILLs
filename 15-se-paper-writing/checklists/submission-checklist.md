# Pre-Submission Checklist

[← Back to Main](../SKILL.md)

Run this checklist **after all sections are drafted** and the paper compiles. These checks require seeing the paper as a whole — they cannot be done section by section.

---

## 1. Page Budget

- [ ] Body content fits within venue page limit (typically 10 pages for double-column, 18–20 for single-column journals)
- [ ] Body is within the venue page limit; being slightly under is fine if no essential evaluation or method detail is missing
- [ ] Section page allocations match recommended targets (within 0.5 pages)
- [ ] Evaluation is the longest section (or tied with methodology)
- [ ] Related work is not the longest section
- [ ] Conclusion is under 0.5 pages
- [ ] References do not count toward body limit (verify with CFP)

See [common/venue-requirements.md](../common/venue-requirements.md) for full venue details.

### Recommended Allocation (Technique Paper, 10 Body Pages)

| Section | Target | Acceptable Range | Over-budget Signal |
|---------|--------|------------------|--------------------|
| Abstract + Intro | 2 pages | 1.5–2.5 | Introduction is rambling |
| Background & Motivation | 1.25 pages | 1–1.5 | Too much tutorial content |
| Methodology | 4 pages | 3–5 | Missing detail OR bloated |
| Implementation | 0.5 pages | 0.25–0.75 | Either too thin or over-detailed |
| Evaluation | 3 pages | 2.5–4 | Most important — can flex up |
| Discussion (Threats) | 0.5 pages | 0.25–0.75 | Should not exceed 0.75 |
| Related Work | 1.0 pages | 0.75–1.25 | Over-surveying wastes pages |
| Conclusion | 0.25 pages | 0.2–0.5 | Keep tight |
| **Total** | **~10** | — | — |

### Common Budget Violations

- Introduction too long (>2.5 pages): Usually caused by repeating motivation in multiple ways. Tighten.
- Related work too long (>1.5 pages): Survey-style writing. Condense each work to 2-3 sentences.
- Evaluation too short (<2.5 pages): Missing error analysis, ablation, or statistical detail. Expand.
- Methodology too short (<2 pages): Reviewers will ask "how does this actually work?"

### Page Reclamation Strategies

When over budget, reclaim space in this priority order:

1. **Related work**: Condense verbose descriptions to 2-3 sentences each
2. **Background**: Remove tutorial content the target audience already knows
3. **Introduction**: Eliminate repeated phrasing of the same motivation
4. **Discussion**: Tighten threats — one sentence per threat + mitigation
5. **Conclusion**: Trim to 4-5 sentences total
6. **Methodology**: Last resort — never sacrifice technical clarity for space

When under budget, invest extra space in this priority order:

1. **Evaluation**: Add error analysis depth, more baselines, deeper ablation
2. **Methodology**: Add running examples, algorithm pseudocode, design rationale
3. **Background**: Add a richer motivating example

---

## 2. Reviewer Focus

- [ ] Identified paper identity (technique / empirical / tool / LLM-based)
- [ ] Page investment matches what reviewers prioritize for this paper type
- [ ] Each section has minimum required depth (see table below)
- [ ] Evaluation section would satisfy a skeptical reviewer

### Paper Identity → Reviewer Expectations

| Paper Identity | What Reviewers Most Want to See | Where to Invest Pages |
|----------------|----------------------------------|----------------------|
| **New technique** | How it works + why it's better than SOTA | Methodology (2.5–3 pages) + Evaluation (3.5+ pages) |
| **Empirical study** | Study design rigor + actionable findings | Study Design (3 pages) + Findings (3 pages) |
| **Tool paper** | Usability + real-world applicability | Demo/Features (2 pages) + User study (2 pages) |
| **LLM-based approach** | Prompt engineering depth + cost/reproducibility + non-LLM baselines | Methodology (2.5 pages) + Evaluation with ablation (3.5 pages) |

### Technique Paper Reviewer Priorities (Most to Least)

1. **Evaluation** — "Does it actually work? Is the comparison fair?"
2. **Methodology** — "What's the key insight? Can I understand how it works?"
3. **Introduction** — "Is the problem real? Is the motivation convincing?"
4. **Ablation** — "Is every component necessary?"
5. **Related work** — "Do the authors know the field?"
6. **Threats** — "Are the authors honest about limitations?"

**Rule of thumb (technique papers):** Evaluation should usually be at least as long as methodology, unless the venue or paper type strongly rewards methodological depth.

### Content Depth Check

| Section | Minimum Depth Required |
|---------|----------------------|
| Motivation | At least one concrete, real-world example (not hypothetical) |
| Methodology | Enough detail for a grad student to reimplement |
| Evaluation setup | Dataset size, selection criteria, baseline versions, hardware, LLM model+temp |
| Results | Per-RQ table + comparison + error analysis + statistical test + answering box |
| Ablation | One table showing each component's delta |
| Error analysis | Taxonomy of failure categories with counts and examples |

---

## 3. Claim-Evidence Traceability

- [ ] Every abstract claim traced to evaluation data
- [ ] Every contribution bullet mapped to a validating RQ or section
- [ ] Numbers consistent across abstract, intro, evaluation, conclusion
- [ ] No "orphan claims" (claims without supporting evidence)
- [ ] Every threshold/cutoff stated in the paper has a verifiable justification (sensitivity sweep, prior-work citation, or formal derivation) — see Section 3.5

### 3.5 Threshold Justification Audit

Every numeric threshold or cutoff in the paper must be justified. Grep the
manuscript for cutoffs and verify each one has a reason a reviewer can
check.

**Grep targets** (run on `main.tex`):
```bash
grep -nE 'top[- ]?(k|[0-9]+)|≥ *0\.|>= *0\.|>=? *0\.|p *< *0\.|threshold|cutoff|similarity|confidence|agreement|window|frequency' main.tex
```

**For each hit, the surrounding prose must contain one of:**
1. An **empirical sweep**: "we swept τ ∈ {0.5, 0.6, 0.7, 0.8} and selected
   0.7 as the knee point (Fig. N)"
2. A **prior-work citation**: "following the threshold of 0.7 used by
   Smith et al. [N] for the same task"
3. A **formal derivation**: "τ corresponds to the 95th percentile of the
   negative-class similarity distribution (§4.2)"

**Common failures (reviewer red flags):**
- "We use a similarity threshold of 0.7" with no citation, no sweep, no derivation
- "Top-5 results were retained" with no rationale for 5
- "p < 0.05" cited without naming the test and correction (if multiple tests)
- "Cohen's κ ≥ 0.8 was considered substantial agreement" without citing
  Landis & Koch or equivalent
- Inter-rater agreement threshold chosen post-hoc to match the data

**If a threshold cannot be justified, either:**
- Run the sweep/sensitivity analysis and add a paragraph + figure, OR
- Remove the hard threshold and report ranked/continuous results instead

### Abstract → Evaluation Mapping

Every quantitative claim in the abstract must appear in the evaluation section with supporting data.

```
For each claim in the abstract:
  1. Find the exact number in the evaluation section
  2. Verify the number matches (no rounding inconsistency)
  3. Verify the baseline comparison matches
  4. Verify the metric name matches
```

**Common failures:**
- Abstract says "87%" but evaluation table says "86.8%" — pick one and be consistent
- Abstract claims "outperforms all baselines" but one baseline ties on one metric
- Abstract mentions a metric not defined in the evaluation setup

### Contribution → RQ Mapping

| Contribution | Validated By |
|-------------|-------------|
| "An empirical study of X on N subjects" | Section 2 or 3 (study itself) |
| "A technique/tool that does Y" | Section 3 (methodology) + RQ1 (effectiveness) |
| "An evaluation showing Z" | Section 5 (evaluation RQs) |
| "A dataset of W" | Section 4 (experimental setup) + artifact |

**Red flag:** A contribution bullet with no corresponding evaluation = overclaiming.

### Number Consistency Audit

The same metric value appears in up to four places. All must match exactly:
- Abstract result numbers = Evaluation table numbers
- Introduction preview numbers = Evaluation table numbers
- Conclusion summary numbers = Evaluation table numbers
- "Answering RQ" box numbers = Evaluation table numbers

---

## 4. Language Quality

- [ ] No vague quantifiers ("many", "several", "various") — replaced with exact counts
- [ ] No unsubstantiated superlatives ("the first", "significantly", "novel")
- [ ] Hedging is calibrated (confident where evidence supports, modest where it doesn't)
- [ ] Tense consistent within each section
- [ ] Voice consistent (either "we" or impersonal throughout)
- [ ] No redundant paragraphs across sections
- [ ] Dash style consistent in prose (ranges vs interruptions; see note below)
- [ ] SE terminology used precisely (sound, complete, precision, recall)

### Vague Language Detection

| Vague Phrase | Fix |
|-------------|-----|
| "significantly better" | "14 percentage points higher (p < 0.01)" |
| "substantially improves" | "improves from 66% to 80%" |
| "effectively handles" | "correctly handles 45 of 50 cases" |
| "state-of-the-art results" | "outperforms [specific baseline] by [specific delta]" |
| "in most cases" | "in 42 of 50 cases (84%)" |
| "a large number of" | "321 cases" |
| "competitive performance" | specify: better, equal, or within X% |
| "promising results" | specify what the results are |
| "various/several/many" | give the exact count |
| "recent work" | give year or citation |

### Overclaiming Detection

| Overclaim Pattern | Required Evidence |
|-------------------|-------------------|
| "the first to..." | Literature search confirming novelty |
| "solves the problem of..." | 100% effectiveness on benchmark |
| "outperforms all existing..." | Comparison with every relevant baseline |
| "novel approach" | Clear differentiation from all related work |
| "comprehensive evaluation" | Multiple datasets, baselines, metrics |

### Hedging Calibration

**Too hedged:** "Our approach might potentially offer some improvement in certain scenarios."
**Too bold:** "Our approach solves dependency conflicts."
**Calibrated:** "Our approach resolves 80% of dependency conflicts in our benchmark, a 14pp improvement over the state-of-the-art."

### Tense and Voice Consistency

| Section | Expected Tense | Expected Voice |
|---------|---------------|----------------|
| Abstract | Present ("We present", "achieves") | Active ("We") |
| Introduction | Present for problem, present for contributions | Active |
| Background | Present for facts ("Python uses...") | Mix |
| Methodology | Present ("The tool analyzes...") | Active |
| Evaluation | Past for what was done ("We evaluated"), present for observations ("Table 1 shows") | Active |
| Related work | Present for describing work ("X proposes...") | Active or third person |
| Conclusion | Past for summary ("We presented"), future for future work ("will extend") | Active |

### Repeated Expression Detection

Common redundancy sites:
- Abstract and introduction opening (some overlap is OK, verbatim copy is not)
- Motivation in introduction vs. background section (should be complementary, not duplicate)
- Evaluation results narrative vs. "Answering RQ" boxes (boxes summarize, don't repeat everything)
- Conclusion vs. abstract (conclusion should add future work, not just restate)

**Rule:** Each sentence should convey information not found elsewhere. If two paragraphs say the same thing, merge into the stronger version and delete the other.

### LaTeX Dash and Punctuation Consistency

For LaTeX source, check the **source form** and the **compiled PDF output** separately:

- `---` in LaTeX source = em dash in prose (interruption / parenthetical emphasis)
- `--` in LaTeX source = en dash for ranges (`10--20`, `2024--2026`)
- Do **not** expect the source file itself to contain the Unicode em dash character `—`
- Avoid forced spaces around em dashes in source such as `~---` unless there is a deliberate typography reason

**Common failures:**
- Using `--` for a prose interruption instead of `---`
- Using `---` for a numeric range instead of `--`
- Searching the `.tex` file for the literal Unicode `—` and concluding the dash was not replaced

### SE Terminology Precision

| Term | Correct Usage | Common Misuse |
|------|--------------|---------------|
| Sound | No false negatives (finds all issues) | Used loosely for "good" |
| Complete | No false positives (every report is real) | Confused with "comprehensive" |
| Precision | TP / (TP + FP) | Confused with accuracy |
| Recall | TP / (TP + FN) | Confused with detection rate |
| Statistically significant | p-value below threshold | Used without running a test |
| Scalable | Tested at increasing input sizes | Used without evidence |

See [common/writing-style.md](../common/writing-style.md) for the full terminology guide.

---

## 5. Structural Integrity

- [ ] Every figure and table referenced in text
- [ ] No `??` in compiled PDF
- [ ] Cross-references point to correct sections
- [ ] Methodology has at least one figure/diagram
- [ ] Evaluation has at least one table per RQ
- [ ] Tool name, metric names, baseline names consistent throughout
- [ ] All tables fit column width — zero overfull hbox from tables
- [ ] No redundant table+figure pairs showing the same data — one form per dataset

### Figure and Table Orphan Check

Every figure and table must be:
1. **Referenced** in the text at least once (no orphan floats)
2. **Placed near** the first reference (same page or next page)
3. **Discussed** — not just "see Figure 1" but analyzed in prose

**Audit:** List all `\label{fig:*}` and `\label{tab:*}` entries. For each, search for `\ref{fig:*}` or `\ref{tab:*}`. Any label without a reference is an orphan.

### Cross-Reference Integrity

Check for:
- `??` in compiled PDF (unresolved references)
- References to wrong sections ("as shown in Section 3" but it's actually Section 4)
- Forward references to content that was moved or deleted

### Visual Density Balance

| Section | Expected Visuals |
|---------|-----------------|
| Introduction | None required (text-focused) |
| Background | 1 motivating example (listing or figure) |
| Methodology | 1 architecture diagram + 1 algorithm or running example |
| Evaluation | 1-2 tables per RQ + optional figures |
| Related work | None required (comparison table optional) |

**Red flag:** Methodology section with zero figures = hard to follow.
**Red flag:** Evaluation section with zero tables = no data presented.
**Red flag:** A table AND a figure showing the same dataset = wasted space.

### Table Width Compliance

Tables MUST fit the column width in double-column formats. Overfull boxes from tables are not acceptable; underfull boxes are usually acceptable unless the table looks visibly loose or distorted.

| Format | Table Width Rule |
|--------|-----------------|
| Double-column (IEEEtran, sigconf) | `\begin{table}` with `tabular` fitting `\columnwidth`. Use `\begin{table*}` ONLY when the data genuinely needs full page width (7+ columns). |
| Single-column (acmsmall, article) | Table can be slightly narrower than `\textwidth` — acceptable. |

**Common fixes for overfull tables:**
- Reduce font size: `\footnotesize` or `\scriptsize` inside `tabular`
- Abbreviate column headers
- Use `\resizebox{\columnwidth}{!}{...}` as last resort (distorts font size)
- Split into two tables if more than 7 columns

### No Redundant Visualizations

Choose ONE ideal form per dataset. Do NOT include both a table and a figure showing the same numbers.

| Data Type | Best Form | Why |
|-----------|-----------|-----|
| Exact comparison numbers | **Table** | Readers need precise values for replication |
| Trends over time/versions | **Line chart** | Visual pattern recognition |
| Distribution/spread | **Box plot or violin** | Shows variance, outliers |
| Category proportions | **Stacked bar** | Part-to-whole relationship |
| Spatial/structural relationships | **Diagram/graph** | Topology matters |

**Decision rule:** If the finding is "method A scores 82.3% vs B's 71.1%", use a table. If the finding is "performance degrades as input size grows", use a figure. Never both.

### Notation and Naming Consistency

- Tool name spelled identically everywhere (including capitalization)
- Mathematical notation consistent (same symbol for same concept)
- Metric names consistent (don't switch between "detection rate" and "recall" for the same metric)
- Baseline names consistent (same abbreviation throughout)
- Dataset name consistent

---

## 6. Final Compilation Checks

### Post-Process Pipeline (Recommended; required only if your workflow or repo depends on it)

- [ ] `postprocess_paper.py` run on paper directory
- [ ] BibTeX sanitized (no non-ASCII, no duplicates)
- [ ] Citation keys normalized (no dangling keys, no nested cites)
- [ ] Citation context consistency checked (author/year match between prose and bib)
- [ ] Missing citations detected (uncited tools, techniques, datasets, metrics)
- [ ] LaTeX syntax errors auto-fixed
- [ ] Paper recompiled after postprocessing
- [ ] Visual overflow check passed (`--visual` flag, if Claude SDK available)
- [ ] Semantic citation consistency checked (`check_citation_consistency.py`, if Claude SDK available)

```bash
# Basic: BibTeX sanitization, citation normalization, syntax checks
python3 scripts/postprocess_paper.py /path/to/paper/dir

# With recompilation after fixes
python3 scripts/postprocess_paper.py /path/to/paper/dir --recompile

# Full: + visual overflow check via Claude Vision (uses Agent SDK credentials)
python3 scripts/postprocess_paper.py /path/to/paper/dir --visual --recompile

# With TikZ visual validation (step 10)
python3 scripts/postprocess_paper.py /path/to/paper/dir --visual-tikz --visual --recompile
```

The pipeline runs the following deterministic checks before any optional visual pass:
1. **BibTeX sanitization** — fix syntax errors, deduplicate, replace non-ASCII characters
2. **Citation key normalization** — normalize to alphabetical-only keys across .bib and .tex files
3. **Dangling citation removal** — remove `\cite{}` keys that have no matching .bib entry
4. **Nested citation fix** — flatten `\cite{\cite{key},other}` → `\cite{key,other}`
5. **TikZ validation** — compile-test each TikZ block, strip broken ones, wrap in `\resizebox`
6. **LaTeX syntax check** — auto-fix common errors (unclosed braces, mismatched environments)
7. **Finding renumbering** — renumber Finding entries in `\mybox{}` blocks globally
8. **RQ label enforcement** — ensure `\label{}` tags exist for all RQ sections
9. **Citation context consistency** — verify author names and years in prose match BibTeX entries (report-only, no auto-fix)
10. **Missing citation detection** — flag named tools, techniques, datasets, metrics, and standards that appear in prose without a nearby `\cite{}` or `\url{}`

Then optionally (with `--visual`):
11. **Visual overflow check** — sends each PDF page to Claude Vision to detect overflow, applies fixes, and recompiles until clean

Standalone semantic citation check (requires Claude SDK):
```bash
# Full check: deterministic + LLM semantic verification
python3 scripts/check_citation_consistency.py /path/to/paper/dir

# Deterministic only (no API calls)
python3 scripts/check_citation_consistency.py /path/to/paper/dir --level deterministic
```

### LaTeX Warnings

After compilation, check the `.log` file for:

```
Overfull \hbox    → Text extends into margins. Fix unless it is in a harmless hidden box.
Underfull \hbox   → Loose typesetting. Usually harmless; investigate only if visually ugly or repeated in body text.
Reference undefined → \ref{} or \cite{} pointing to nothing.
Citation undefined  → Missing BibTeX entry.
Float specifier changed → LaTeX moved your figure/table.
```

- [ ] No unresolved overfull warnings in body text or tables
- [ ] Underfull warnings reviewed; harmless ones left alone, ugly ones fixed
- [ ] All references resolved (no "??")
- [ ] Bibliography generates correctly

### Visual Overflow Check (Standalone)

```bash
# Check only (no fixes)
python3 scripts/check_visual_overflow.py /path/to/paper/dir --check-only

# Check and fix (up to 3 iterations)
python3 scripts/check_visual_overflow.py /path/to/paper/dir

# Check specific pages
python3 scripts/check_visual_overflow.py /path/to/paper/dir --pages 1,3,7-10
```

### PDF Metadata (Double-Blind)

- [ ] PDF metadata stripped for double-blind

```bash
# Check metadata
pdfinfo paper.pdf

# Strip metadata only if the venue or template workflow requires it
exiftool -all= paper.pdf
```

---

## 7. Anonymization (Double-Blind)

- [ ] Author names removed from paper
- [ ] Institution names removed
- [ ] Self-citations anonymized
- [ ] GitHub links anonymized or removed
- [ ] Acknowledgments removed or anonymized
- [ ] PDF metadata cleared

---

## 8. BibTeX Validation

- [ ] All entries verified against DBLP/Scholar
- [ ] No fabricated citations
- [ ] Titles exactly match published versions
- [ ] Authors all present and correctly spelled
- [ ] Venues and years correct
- [ ] DOIs included where available

---

## 9. Artifact Checklist (If Required)

- [ ] Public repository created
- [ ] README includes installation instructions
- [ ] README includes usage examples
- [ ] README includes reproduction steps
- [ ] Code runs without errors
- [ ] requirements.txt with pinned versions
- [ ] Data included or linked
- [ ] LICENSE file

---

## 10. Final Verification

### One Day Before

- [ ] Re-read abstract (most-read part)
- [ ] Re-read introduction
- [ ] Check all numbers match between text and tables
- [ ] Verify claims match evaluation results

### Submission Day

- [ ] Correct venue/track selected
- [ ] All co-authors added
- [ ] Conflicts of interest declared
- [ ] PDF uploaded (not source)
- [ ] Supplementary materials uploaded (if any)
- [ ] Abstract entered in submission system
- [ ] Keywords entered

### After Submission

- [ ] Download submitted PDF to verify
- [ ] Save submission confirmation
- [ ] Note rebuttal/revision dates

[Back to Main →](../SKILL.md)
