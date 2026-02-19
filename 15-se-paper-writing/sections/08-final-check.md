# Section 8: Final Whole-Paper Check

[← Back to Main](../SKILL.md) | [← Conclusion](07-conclusion.md)

Run this checklist **after all sections are drafted** and the paper compiles. These checks require seeing the paper as a whole — they cannot be done section by section.

## 1. Page Budget Audit

### 1.1 Body Page Count

Most top-tier SE venues with double columns allow 10 pages of body content + 1--2 pages of references (often 12 total). References usually do **not** count toward the body limit, but always verify the specific CFP.
For single-column journals, limits are usually larger (often 18--20 body pages plus references), but this also varies by venue.

**Check:** Compile the PDF and count body pages (from first page of introduction through end of conclusion, including abstract on page 1). It is mandantory that the body not only must fit within the venue limit, but also should be exactly at the max length. 

See [common/venue-requirements.md](../common/venue-requirements.md) for full venue details.

### 1.2 Section Page Allocation vs Budget

Compare actual page lengths against the recommended allocation. Flag any section that deviates by more than 0.5 pages.

**Recommended allocation (technique paper, 10 body pages):**

| Section | Target | Acceptable Range | Over-budget Signal |
|---------|--------|------------------|--------------------|
| Abstract + Intro | 2 pages | 1.5–2.5 | Introduction is rambling |
| Background & Motivation | 1.25 pages | 1–1.5 | Too much tutorial content |
| Methodology | 4 pages | 3-5 | Missing detail OR bloated |
| Implementation | 0.5 pages | 0.25–0.75 | Either too thin or over-detailed |
| Evaluation | 3 pages | 2.5–4 | Most important — can flex up |
| Discussion (Threats) | 0.5 pages | 0.25–0.75 | Should not exceed 0.75 |
| Related Work | 1.0 pages | 0.75–1.25 | Over-surveying wastes pages |
| Conclusion | 0.25 pages | 0.2–0.5 | Keep tight |
| **Total** | **~10** | — | — |

**Common budget violations:**
- Introduction too long (>2.5 pages): Usually caused by repeating motivation in multiple ways. Tighten.
- Related work too long (>1.5 pages): Survey-style writing. Condense each work to 2-3 sentences.
- Evaluation too short (<2.5 pages): Missing error analysis, ablation, or statistical detail. Expand.
- Methodology too short (<2 pages): Reviewers will ask "how does this actually work?"

### 1.3 Page Reclamation Strategies

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

## 2. Reviewer Focus Analysis

### 2.1 Identify What This Paper Is Really About

Read the abstract and contribution list. Classify the paper's primary identity:

| Paper Identity | What Reviewers Most Want to See | Where to Invest Pages |
|----------------|----------------------------------|----------------------|
| **New technique** | How it works + why it's better than SOTA | Methodology (2.5–3 pages) + Evaluation (3.5+ pages) |
| **Empirical study** | Study design rigor + actionable findings | Study Design (3 pages) + Findings (3 pages) |
| **Tool paper** | Usability + real-world applicability | Demo/Features (2 pages) + User study (2 pages) |
| **LLM-based approach** | Prompt engineering depth + cost/reproducibility + non-LLM baselines | Methodology (2.5 pages) + Evaluation with ablation (3.5 pages) |

### 2.2 Reviewer Priority Matrix

For each paper identity, reviewers prioritize sections differently. Ensure your page allocation matches their priorities:

**Technique paper reviewer priorities (most to least):**

1. **Evaluation** — "Does it actually work? Is the comparison fair?"
2. **Methodology** — "What's the key insight? Can I understand how it works?"
3. **Introduction** — "Is the problem real? Is the motivation convincing?"
4. **Ablation** — "Is every component necessary?"
5. **Related work** — "Do the authors know the field?"
6. **Threats** — "Are the authors honest about limitations?"

**Rule of thumb (technique papers):** Evaluation should usually be at least as long as methodology. Reviewers spend the most time scrutinizing claims, not reading how the tool works.

### 2.3 Content Depth Check

For each section, ask: **"Would a skeptical reviewer be satisfied with this level of detail?"**

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

### 3.1 Abstract → Evaluation Mapping

Every quantitative claim in the abstract must appear in the evaluation section with supporting data. Extract all claims from the abstract and trace each to its source.

**Audit procedure:**

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

### 3.2 Contribution → RQ Mapping

Each contribution bullet in the introduction must have a corresponding RQ or section that validates it.

| Contribution | Validated By |
|-------------|-------------|
| "An empirical study of X on N subjects" | Section 2 or 3 (study itself) |
| "A technique/tool that does Y" | Section 3 (methodology) + RQ1 (effectiveness) |
| "An evaluation showing Z" | Section 5 (evaluation RQs) |
| "A dataset of W" | Section 4 (experimental setup) + artifact |

**Red flag:** A contribution bullet with no corresponding evaluation = overclaiming.

### 3.3 Number Consistency Audit

The same metric value appears in up to four places: abstract, introduction, evaluation, conclusion. All four must match exactly.

**Check each of these pairs:**
- Abstract result numbers = Evaluation table numbers
- Introduction preview numbers = Evaluation table numbers
- Conclusion summary numbers = Evaluation table numbers
- "Answering RQ" box numbers = Evaluation table numbers

---

## 4. Language Quality Audit

### 4.1 Vague Language Detection

Search the manuscript for weasel words that weaken claims. Each occurrence should either be replaced with a precise number or removed.

**Flag these patterns:**

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

### 4.2 Overclaiming Detection

Search for absolute or superlative claims and verify each:

| Overclaim Pattern | Required Evidence |
|-------------------|-------------------|
| "the first to..." | Literature search confirming novelty |
| "solves the problem of..." | 100% effectiveness on benchmark |
| "outperforms all existing..." | Comparison with every relevant baseline |
| "novel approach" | Clear differentiation from all related work |
| "comprehensive evaluation" | Multiple datasets, baselines, metrics |

### 4.3 Hedging Calibration

Too much hedging weakens the paper. Too little sounds arrogant. Calibrate:

**Too hedged:** "Our approach might potentially offer some improvement in certain scenarios."
**Too bold:** "Our approach solves dependency conflicts."
**Calibrated:** "Our approach resolves 80% of dependency conflicts in our benchmark, a 14pp improvement over the state-of-the-art."

### 4.4 Tense and Voice Consistency

| Section | Expected Tense | Expected Voice |
|---------|---------------|----------------|
| Abstract | Present ("We present", "achieves") | Active ("We") |
| Introduction | Present for problem, present for contributions | Active |
| Background | Present for facts ("Python uses...") | Mix |
| Methodology | Present ("The tool analyzes...") | Active |
| Evaluation | Past for what was done ("We evaluated"), present for observations ("Table 1 shows") | Active |
| Related work | Present for describing work ("X proposes...") | Active or third person |
| Conclusion | Past for summary ("We presented"), future for future work ("will extend") | Active |

**Check:** Read through and flag any section that switches tense or voice mid-paragraph without reason.

### 4.5 Repeated Expression Detection

Search for the same idea expressed with different wording across sections. Common redundancy sites:

- Abstract and introduction opening (some overlap is OK, verbatim copy is not)
- Motivation in introduction vs. background section (should be complementary, not duplicate)
- Evaluation results narrative vs. "Answering RQ" boxes (boxes summarize, don't repeat everything)
- Conclusion vs. abstract (conclusion should add future work, not just restate)

**Rule:** Each sentence in the paper should convey information not found elsewhere. If two paragraphs say the same thing, merge them into the stronger version and delete the other.

### 4.6 SE Terminology Precision

Verify correct usage of domain-specific terms:

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

## 5. Structural Integrity Checks

### 5.1 Figure and Table Orphan Check

Every figure and table must be:
1. **Referenced** in the text at least once (no orphan floats)
2. **Placed near** the first reference (same page or next page)
3. **Discussed** — not just "see Figure 1" but analyzed in prose

**Audit:** List all `\label{fig:*}` and `\label{tab:*}` entries. For each, search for `\ref{fig:*}` or `\ref{tab:*}`. Any label without a reference is an orphan.

### 5.2 Cross-Reference Integrity

Check for:
- `??` in compiled PDF (unresolved references)
- References to wrong sections ("as shown in Section 3" but it's actually Section 4)
- Forward references to content that was moved or deleted

### 5.3 Visual Density Balance

No section should be a wall of text without visual breaks. Check:

| Section | Expected Visuals |
|---------|-----------------|
| Introduction | None required (text-focused) |
| Background | 1 motivating example (listing or figure) |
| Methodology | 1 architecture diagram + 1 algorithm or running example |
| Evaluation | 1-2 tables per RQ + optional figures |
| Related work | None required (comparison table optional) |

**Red flag:** Methodology section with zero figures = hard to follow.
**Red flag:** Evaluation section with zero tables = no data presented.

### 5.4 Notation and Naming Consistency

- Tool name spelled identically everywhere (including capitalization)
- Mathematical notation consistent (same symbol for same concept)
- Metric names consistent (don't switch between "detection rate" and "recall" for the same metric)
- Baseline names consistent (same abbreviation throughout)
- Dataset name consistent

---

## 6. Final Compilation Checks

### 6.1 LaTeX Warnings

After compilation, check the `.log` file for:

```
Overfull \hbox    → Text extends into margins. Fix by rewording.
Underfull \hbox   → Loose typesetting. Usually harmless but check.
Reference undefined → \ref{} or \cite{} pointing to nothing.
Citation undefined  → Missing BibTeX entry.
Float specifier changed → LaTeX moved your figure/table.
```

### 6.2 Visual Overflow Check

Use the visual overflow checker script ([scripts/check_visual_overflow.py](../scripts/check_visual_overflow.py)) to detect:
- Tables extending beyond column/page margins
- Figures cut off or overlapping text
- Code listings exceeding column width
- URLs breaking awkwardly

### 6.3 PDF Metadata

For double-blind submission (if required by the venue):
```bash
# Check metadata
pdfinfo paper.pdf

# Strip metadata only if the venue or template workflow requires it
exiftool -all= paper.pdf
```

---

## Master Checklist

### Page Budget
- [ ] Body content fits within venue page limit (typically 10 pages)
- [ ] Section page allocations match recommended targets (within 0.5 pages)
- [ ] Evaluation is the longest section (or tied with methodology)
- [ ] Related work is not the longest section
- [ ] Conclusion is under 0.5 pages
- [ ] The total page by default should be exactly long as the page limit (10 for double columnor 18 for single column) and there should be not be any over or any shorter. If the total page is not exactly the max limit, consider the following reviewr focus to expand critical sections with more detailed elaborations.

### Reviewer Focus
- [ ] Identified paper identity (technique / empirical / tool / LLM-based)
- [ ] Page investment matches what reviewers prioritize for this paper type
- [ ] Each section has minimum required depth (see table in 2.3)
- [ ] Evaluation section would satisfy a skeptical reviewer

### Claim-Evidence Traceability
- [ ] Every abstract claim traced to evaluation data
- [ ] Every contribution bullet mapped to a validating RQ or section
- [ ] Numbers consistent across abstract, intro, evaluation, conclusion
- [ ] No "orphan claims" (claims without supporting evidence)

### Language Quality
- [ ] No vague quantifiers ("many", "several", "various") — replaced with exact counts
- [ ] No unsubstantiated superlatives ("the first", "significantly", "novel")
- [ ] Hedging is calibrated (confident where evidence supports, modest where it doesn't)
- [ ] Tense consistent within each section
- [ ] Voice consistent (either "we" or impersonal throughout)
- [ ] No redundant paragraphs across sections
- [ ] SE terminology used precisely (sound, complete, precision, recall)

### Structural Integrity
- [ ] Every figure and table referenced in text
- [ ] No `??` in compiled PDF
- [ ] Cross-references point to correct sections
- [ ] Methodology has at least one figure/diagram
- [ ] Evaluation has at least one table per RQ
- [ ] Tool name, metric names, baseline names consistent throughout
- [ ] No LaTeX overfull/underfull warnings in body text
- [ ] PDF metadata stripped for double-blind

[← Conclusion](07-conclusion.md) | [Back to Main →](../SKILL.md)
