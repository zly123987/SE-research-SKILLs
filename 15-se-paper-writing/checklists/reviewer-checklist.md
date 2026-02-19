# What SE Reviewers Look For

[← Back to Main](../SKILL.md)

Understanding reviewer expectations helps you write stronger papers.

## Review Criteria

| Criterion | Questions Reviewers Ask |
|-----------|------------------------|
| **Novelty** | Is the technique/insight new? Not just "apply X to Y"? |
| **Soundness** | Are claims supported by evidence? |
| **Significance** | Does this matter to the community? |
| **Evaluation** | Appropriate benchmarks? Strong baselines? Statistics? |
| **Presentation** | Clear writing? Good figures? Easy to follow? |
| **Reproducibility** | Can I replicate this? Is code available? |

---

## Novelty Evaluation

### What Counts as Novel

- New algorithm or technique
- New combination of existing techniques with insight
- New application domain with non-trivial adaptation
- Significant improvement over SOTA with analysis of why

### What Doesn't Count

- "We applied LLM to X" (without insight)
- Minor parameter tuning of existing methods
- Straightforward combination without synergy

### Reviewer Questions

- "What's the key insight enabling this approach?"
- "How does this differ from [recent work]?"
- "Why couldn't existing tools do this?"

---

## Soundness Evaluation

### What Reviewers Check

- Do results support claims?
- Are comparisons fair?
- Is methodology reproducible?
- Are threats acknowledged?

### Common Issues

| Issue | How Reviewers Catch It |
|-------|------------------------|
| Cherry-picked results | Missing error analysis, no failed cases |
| Unfair baselines | Old versions, wrong configurations |
| Overclaiming | Claims broader than evaluation scope |
| Missing ablation | No evidence components are necessary |

---

## Significance Evaluation

### Questions Reviewers Ask

- "Would practitioners use this?"
- "Does this advance the research area?"
- "Is the problem important enough?"
- "Are the improvements meaningful?"

### How to Demonstrate Significance

- Concrete motivation with real-world impact
- Substantial improvement (not marginal gains)
- Broad applicability (not narrow edge case)
- Clear contribution to knowledge

---

## Evaluation Criteria

### Reviewers Expect

| Element | Expectation |
|---------|-------------|
| **Benchmarks** | Standard, diverse, appropriate size |
| **Baselines** | Recent SOTA (last 2-3 years) |
| **Metrics** | Standard for the domain |
| **Statistics** | Tests + effect sizes |
| **Ablation** | Each component justified |
| **Error analysis** | Failures categorized |

### Red Flags

- No comparison to recent work
- Only toy examples
- Missing statistical analysis
- No error analysis
- Ablation shows some components unnecessary

---

## Presentation Evaluation

### What Makes Good Presentation

- Clear problem statement in first page
- Concrete motivating example
- Key insight explicitly stated
- Architecture diagram
- Well-formatted tables and figures
- Flowing prose (not bullet lists)

### Red Flags

- Vague problem description
- No concrete examples
- Missing figures/diagrams
- Excessive formatting (bold/italic overuse)
- Bullet-heavy methodology

---

## Common Rejection Reasons

### 1. Incremental Contribution

**Symptom:** "This is X + Y without new insight"

**Fix:**
- Articulate key insight clearly
- Explain why combination is non-trivial
- Show synergy, not just addition

### 2. Weak Evaluation

**Symptom:** "Only tested on 5 small projects"

**Fix:**
- Use established benchmarks
- Include diverse subjects
- Report on full dataset

### 3. Missing Baselines

**Symptom:** "Doesn't compare to [recent paper]"

**Fix:**
- Search last 3 years of ICSE/FSE/ASE
- Include recent SOTA
- Justify any exclusions

### 4. Overclaiming

**Symptom:** "Claims don't match evidence"

**Fix:**
- Scope claims precisely
- Claims must match evaluation
- Acknowledge limitations

### 5. Poor Presentation

**Symptom:** "Couldn't understand the approach"

**Fix:**
- Add architecture diagram
- Include running example
- Write clear prose

---

## Self-Review Checklist

Before submission, ask yourself:

### Novelty
- [ ] Key insight explicitly stated?
- [ ] Differentiation from prior work clear?
- [ ] Contribution is non-trivial?

### Soundness
- [ ] All claims supported by evidence?
- [ ] Comparisons are fair?
- [ ] Threats acknowledged?

### Significance
- [ ] Problem is important?
- [ ] Improvements are meaningful?
- [ ] Community would care?

### Evaluation
- [ ] Benchmarks are standard?
- [ ] Baselines are recent?
- [ ] Statistics with effect sizes?
- [ ] Ablation study present?
- [ ] Error analysis included?

### Presentation
- [ ] Introduction clear in first page?
- [ ] Motivating example concrete?
- [ ] Architecture diagram present?
- [ ] Methodology is prose (not bullets)?

### Reproducibility
- [ ] Artifact available?
- [ ] Instructions clear?
- [ ] Data accessible?

---

## Responding to Reviews

### Accept Feedback Gracefully

Even harsh reviews often contain valid points. Look for:
- Legitimate concerns about methodology
- Missing comparisons or experiments
- Unclear explanations

### Common Rebuttal Mistakes

- Dismissing concerns ("Reviewer misunderstood")
- Promising future work ("We will add this")
- Arguing without evidence ("We disagree because...")

### Effective Rebuttals

- Acknowledge the concern
- Provide evidence addressing it
- If needed, commit to specific changes

---

## Reviewer Score Interpretation

| Score | Meaning | Your Paper |
|-------|---------|------------|
| **Strong Accept** | Exceptional, must publish | Rare; significant contribution |
| **Accept** | Good paper, should publish | Solid work, minor issues |
| **Weak Accept** | Borderline positive | Concerns but promising |
| **Borderline** | Could go either way | Needs improvement |
| **Weak Reject** | Borderline negative | Significant issues |
| **Reject** | Major problems | Fundamental flaws |
| **Strong Reject** | Seriously flawed | Should not publish |

Most accepted papers have 2+ positive reviews and no strong negatives.

[Back to Main →](../SKILL.md)
