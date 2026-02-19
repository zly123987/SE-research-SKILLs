# Pre-Submission Checklist

[← Back to Main](../SKILL.md)

Complete checklist before submitting to SE venues.

---

## Content Checklist

### Introduction
- [ ] Problem stated clearly in first paragraph
- [ ] Limitation of existing work explained
- [ ] "This paper" paragraph describes approach
- [ ] **Key insight paragraph present and specific**
- [ ] Contributions list (3-4 bullets)
- [ ] Claims match evaluation results

### Background & Motivation
- [ ] Background concepts defined (only what's needed)
- [ ] Motivating example is **real** (not synthetic)
- [ ] Example shows actual code/config
- [ ] Why existing tools fail explained
- [ ] Challenges extracted from example

### Methodology
- [ ] Problem formalization (input/output/goal)
- [ ] Architecture diagram/figure
- [ ] Written as **prose** (not bullets)
- [ ] Design decisions justified (WHY, not just WHAT)
- [ ] Running example walkthrough
- [ ] Novel contribution has dedicated subsection

### Evaluation
- [ ] RQs defined at section start (3-5)
- [ ] Experimental setup complete:
  - [ ] Dataset with size, source, characteristics
  - [ ] Baselines with citations and brief descriptions
  - [ ] Metrics precisely defined
  - [ ] Environment (hardware, software, LLM model)
- [ ] Each RQ has ~1 page
- [ ] "Answering RQ" boxes at END of each subsection
- [ ] Statistical tests with effect sizes
- [ ] Ablation study present
- [ ] Error analysis categorizing failures

### Threats to Validity
- [ ] Internal validity addressed
- [ ] External validity addressed
- [ ] Construct validity addressed
- [ ] Conclusion validity addressed
- [ ] Mitigations explained for each threat

### Related Work
- [ ] Organized by approach type (not chronologically)
- [ ] Each work has 3-5 sentences of substantive discussion
- [ ] Differentiation clear for each work
- [ ] Subsections end with positioning summary
- [ ] Recent work (last 2-3 years) included

### Conclusion
- [ ] Summary restates problem and solution
- [ ] Key results with numbers
- [ ] Future work is concrete (specific directions)
- [ ] Tool URL included (if applicable)

---

## Formatting Checklist

### Page Limit
- [ ] Within page limit (references don't count)
- [ ] No content in margins

### Document Class
- [ ] Correct document class for venue
- [ ] Correct options (review, anonymous, etc.)

### Tables
- [ ] Using `booktabs` (`\toprule`, `\midrule`, `\bottomrule`)
- [ ] No `\hline` used
- [ ] Caption ABOVE table
- [ ] Best results bolded
- [ ] Referenced in text

### Figures
- [ ] High resolution (PDF preferred)
- [ ] Readable at 50% zoom
- [ ] Caption below figure
- [ ] Referenced in text

### Algorithms
- [ ] Professional formatting (algorithm2e)
- [ ] `\KwIn`, `\KwOut` for inputs/outputs
- [ ] Referenced in text

### Code Listings
- [ ] Syntax highlighting
- [ ] Line numbers if discussed in text
- [ ] Caption and label

### References
- [ ] Non-breaking spaces before citations (`~\cite{}`)
- [ ] Consistent BibTeX formatting
- [ ] All cited works verified to exist

---

## Anonymization Checklist (Double-Blind)

- [ ] Author names removed from paper
- [ ] Institution names removed
- [ ] Self-citations anonymized
- [ ] GitHub links anonymized or removed
- [ ] Acknowledgments removed or anonymized
- [ ] PDF metadata cleared:
  ```bash
  exiftool -all= paper.pdf
  ```

---

## BibTeX Validation Checklist

- [ ] All entries verified against DBLP/Scholar
- [ ] No fabricated citations
- [ ] Titles exactly match published versions
- [ ] Authors all present and correctly spelled
- [ ] Venues and years correct
- [ ] DOIs included where available

---

## Technical Checklist

### LaTeX Compilation
- [ ] Compiles without errors
- [ ] No overfull hbox warnings
- [ ] All references resolved (no "??")
- [ ] Bibliography generates correctly

### PDF Quality
- [ ] Fonts embedded
- [ ] PDF renders correctly on different viewers
- [ ] Links work (if hyperref used)
- [ ] No artifacts from editing

---

## Artifact Checklist (If Required)

- [ ] Public repository created
- [ ] README with:
  - [ ] Installation instructions
  - [ ] Usage examples
  - [ ] Reproduction steps
- [ ] Code runs without errors
- [ ] requirements.txt with pinned versions
- [ ] Data included or linked
- [ ] LICENSE file
- [ ] Zenodo DOI created (if required)

---

## Final Verification

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

---

## Quick Reference: Page Allocations

| Section | Technique Paper |
|---------|-----------------|
| Introduction | 1.5-2 pages |
| Background | 1-1.5 pages |
| Methodology | 2-3 pages |
| Implementation | 0.5-1 page |
| Evaluation | 4-6 pages |
| Threats | 0.5 page |
| Related Work | 1-1.5 pages |
| Conclusion | 0.5 page |
| **Total** | **11 pages** |

---

## Emergency Fixes

### Over Page Limit
1. Reduce figure sizes
2. Combine small tables
3. Tighten prose (remove redundancy)
4. Move details to appendix (if allowed)

### Missing Baselines
1. Search DBLP for recent work
2. Contact authors for artifacts
3. Explain exclusions in paper

### Missing Statistics
1. Run appropriate test (Fisher's, Wilcoxon)
2. Calculate effect size (Cliff's d)
3. Add to "Answering RQ" boxes

[Back to Main →](../SKILL.md)
