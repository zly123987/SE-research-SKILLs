# Statistical Analysis for SE Papers

[← Back to Main](../SKILL.md)

SE venues expect proper statistical analysis for empirical claims.

## Core Principle

**Always report: metric, test, p-value, effect size.**

```latex
Our approach achieves 85.2\% precision compared to 72.1\% for the baseline
(Wilcoxon signed-rank test, $p < 0.001$, Cliff's $d = 0.42$, medium effect).
```

---

## Choosing the Right Test

### Decision Tree

```
Is data paired (same subjects, before/after)?
├── YES: Are differences normally distributed?
│   ├── YES: Paired t-test
│   └── NO: Wilcoxon signed-rank test
└── NO: Are groups independent?
    ├── YES: Are values normally distributed?
    │   ├── YES: Independent t-test
    │   └── NO: Mann-Whitney U test
    └── NO: (Not applicable)

For categorical/binary outcomes:
├── 2x2 table: Fisher's exact test
├── Larger tables: Chi-square test
└── Paired categorical: McNemar's test
```

### Common Tests in SE Papers

| Test | Use When | Python |
|------|----------|--------|
| **Fisher's exact** | 2x2 contingency (success/fail × tool) | `scipy.stats.fisher_exact` |
| **Chi-square** | Categorical outcomes, >2 categories | `scipy.stats.chi2_contingency` |
| **Wilcoxon signed-rank** | Paired numeric, non-normal | `scipy.stats.wilcoxon` |
| **Mann-Whitney U** | Independent numeric, non-normal | `scipy.stats.mannwhitneyu` |
| **Paired t-test** | Paired numeric, normal | `scipy.stats.ttest_rel` |

---

## Effect Size (ALWAYS Required)

P-values tell you if a difference exists; effect size tells you if it matters.

### Cliff's Delta (Non-parametric)

Use for ordinal or non-normal data:

| |d| | Interpretation |
|-----|----------------|
| < 0.147 | Negligible |
| 0.147 - 0.33 | Small |
| 0.33 - 0.474 | Medium |
| > 0.474 | Large |

```python
from cliffs_delta import cliffs_delta

d, interpretation = cliffs_delta(our_results, baseline_results)
# Returns: (0.42, 'medium')
```

### Cohen's d (Parametric)

Use for normal data:

| |d| | Interpretation |
|-----|----------------|
| < 0.2 | Negligible |
| 0.2 - 0.5 | Small |
| 0.5 - 0.8 | Medium |
| > 0.8 | Large |

```python
from scipy.stats import ttest_rel
import numpy as np

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std
```

---

## Complete Analysis Example

```python
from scipy import stats
from cliffs_delta import cliffs_delta

def compare_approaches(baseline: list, our_tool: list) -> dict:
    """Proper statistical comparison for SE papers."""

    # 1. Test for normality (Shapiro-Wilk)
    _, p_normal = stats.shapiro(baseline)

    # 2. Choose appropriate test
    if p_normal > 0.05:
        # Parametric: paired t-test
        stat, p_value = stats.ttest_rel(baseline, our_tool)
        test_name = "paired t-test"
    else:
        # Non-parametric: Wilcoxon signed-rank
        stat, p_value = stats.wilcoxon(baseline, our_tool)
        test_name = "Wilcoxon signed-rank"

    # 3. Effect size (ALWAYS required)
    d, magnitude = cliffs_delta(our_tool, baseline)

    return {
        "test": test_name,
        "statistic": stat,
        "p_value": p_value,
        "effect_size": d,
        "magnitude": magnitude,
    }
```

---

## Reporting Results

### LaTeX Format

```latex
% Full statistical report
\tool{} achieves 80\% detection rate compared to PyEGo's 66\%
(Fisher's exact test, $p = 0.032$, Cliff's $\delta = 0.21$, small effect).

% In tables
\begin{tabular}{lrrcc}
\toprule
\textbf{Approach} & \textbf{Rate} & \textbf{$\Delta$} & \textbf{$p$} & \textbf{$d$} \\
\midrule
PyEGo & 66\% & --- & --- & --- \\
\textbf{Ours} & \textbf{80\%} & +14\% & 0.032* & 0.21 \\
\bottomrule
\end{tabular}
```

### Significance Markers

| Symbol | Meaning |
|--------|---------|
| * | p < 0.05 |
| ** | p < 0.01 |
| *** | p < 0.001 |

---

## Statistical Power

Ensure your study has sufficient power to detect effects.

### Sample Size Guidelines

| Effect Size | Samples Needed (80% power, α=0.05) |
|-------------|-----------------------------------|
| Large (d=0.8) | ~26 per group |
| Medium (d=0.5) | ~64 per group |
| Small (d=0.2) | ~394 per group |

### Reporting Power

```latex
With 50 subjects per group, our study has 80\% power to detect
medium effects ($d = 0.5$) at $\alpha = 0.05$.
```

---

## Multiple Comparisons

When testing multiple hypotheses, adjust for multiple comparisons:

### Bonferroni Correction

Divide α by number of comparisons:

```latex
We compare against 4 baselines, using Bonferroni-corrected
significance threshold $\alpha = 0.05/4 = 0.0125$.
```

### When NOT to Correct

If RQs address distinct, independent questions (not multiple comparisons within one hypothesis), correction may not be needed—explain this:

```latex
We did not apply multiple comparison correction because our RQs
address distinct questions rather than multiple comparisons
within a single hypothesis.
```

---

## Common Mistakes

### 1. P-value Only

**Bad:** "p = 0.03, so the difference is significant."
**Good:** "p = 0.03, Cliff's d = 0.42 (medium effect)."

### 2. Wrong Test

**Bad:** Using t-test on non-normal data
**Good:** Test normality first, use Wilcoxon if non-normal

### 3. No Power Analysis

**Bad:** "We used 10 subjects."
**Good:** "With 50 subjects, we have 80% power to detect medium effects."

### 4. P-hacking

**Bad:** Running multiple tests until something is significant
**Good:** Pre-specify tests, report all results (positive and negative)

---

## Quick Reference

### For Binary Outcomes (Success/Fail)

```python
# 2x2 contingency table: [[our_success, our_fail], [base_success, base_fail]]
from scipy.stats import fisher_exact

table = [[40, 10], [33, 17]]  # [ours, baseline]
odds_ratio, p_value = fisher_exact(table)
```

### For Continuous Outcomes

```python
from scipy.stats import wilcoxon
from cliffs_delta import cliffs_delta

# Paired comparison
stat, p = wilcoxon(baseline_scores, our_scores)
d, interp = cliffs_delta(our_scores, baseline_scores)
```

---

## Checklist

- [ ] Normality tested before choosing parametric vs non-parametric
- [ ] Appropriate statistical test selected
- [ ] P-value reported
- [ ] Effect size reported with interpretation
- [ ] Sample size justified (power analysis)
- [ ] Multiple comparison correction if applicable
- [ ] Results reported in both text and tables

[Back to Main →](../SKILL.md)
