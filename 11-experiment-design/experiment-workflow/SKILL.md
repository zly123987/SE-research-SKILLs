# Experiment Design Skill: Phased Validation Workflow

## Overview

This skill guides you through a systematic experiment workflow for validating research tools before full-scale evaluation. The phased approach minimizes wasted effort and enables early comparison against baselines.

## Core Principle: Fail Fast, Validate Early

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     PHASED EXPERIMENT WORKFLOW                              │
│                                                                             │
│   Phase 1: Partial Test        Phase 2: Baseline           Phase 3: Full   │
│   ┌─────────────────┐          ┌─────────────────┐         ┌─────────────┐ │
│   │ Your Tool       │          │ Implement       │         │ Full Test   │ │
│   │ on 10-20% sample│  ───►    │ Baselines       │  ───►   │ All Systems │ │
│   │                 │          │                 │         │             │ │
│   └────────┬────────┘          └────────┬────────┘         └──────┬──────┘ │
│            │                            │                         │        │
│            ▼                            ▼                         ▼        │
│   ┌─────────────────┐          ┌─────────────────┐         ┌─────────────┐ │
│   │ Working?        │          │ Compare Results │         │ RQ Analysis │ │
│   │ If NO → Debug   │          │ Better? Same?   │         │ Ablation    │ │
│   │ If YES → Next   │          │ Worse?          │         │ Statistics  │ │
│   └─────────────────┘          └─────────────────┘         └─────────────┘ │
│                                                                             │
│   DECISION GATES:                                                          │
│   ═══════════════                                                          │
│   Gate 1: Tool works on sample → Proceed to baselines                      │
│   Gate 2: Tool outperforms baselines → Proceed to full test                │
│   Gate 3: Results are statistically significant → Proceed to paper         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Partial Test (Your Tool)

### Purpose
Verify your tool works correctly on a representative sample before investing in full evaluation.

### Sample Selection

```
SAMPLE SELECTION CRITERIA:

□ Size: 10-20% of dataset (min 20-30 cases)
  - Small enough for quick iteration
  - Large enough for meaningful signal

□ Representativeness:
  - Include easy, medium, and hard cases
  - Cover all case categories/types
  - Include edge cases if known

□ Stratified Sampling (when applicable):
  - Same distribution as full dataset
  - E.g., if 30% are type A, sample should have ~30% type A
```

### Partial Test Protocol

```python
# Example: Partial Test Script
def run_partial_test(tool, dataset, sample_ratio=0.15):
    """Run tool on stratified sample."""

    # 1. Sample selection
    sample = stratified_sample(dataset, ratio=sample_ratio)
    print(f"Testing on {len(sample)} / {len(dataset)} cases ({sample_ratio*100:.0f}%)")

    # 2. Run tool
    results = []
    for case in sample:
        try:
            output = tool.analyze(case)
            results.append({
                "case": case.id,
                "success": True,
                "output": output,
            })
        except Exception as e:
            results.append({
                "case": case.id,
                "success": False,
                "error": str(e),
            })

    # 3. Calculate metrics
    success_rate = sum(1 for r in results if r["success"]) / len(results)

    # 4. Report
    print(f"Success Rate: {success_rate*100:.1f}%")
    return results

# Decision gate
if success_rate >= 0.7:
    print("✓ Gate 1 PASSED: Proceed to baseline comparison")
else:
    print("✗ Gate 1 FAILED: Debug tool before proceeding")
```

### What to Check

```
PARTIAL TEST CHECKLIST:

□ Functionality
  - Tool runs without crashing
  - Produces expected output format
  - Handles edge cases gracefully

□ Performance
  - Reasonable execution time
  - Memory usage acceptable
  - No infinite loops

□ Quality
  - Manual inspection of sample outputs
  - Obvious errors detected?
  - Plausible results?
```

---

## Phase 2: Baseline Implementation & Comparison

### Why Baselines Matter

```
BASELINE PURPOSE:

1. SANITY CHECK: Does your tool beat trivial approaches?
   - If not, your contribution may be insufficient

2. NOVELTY VALIDATION: Is the improvement meaningful?
   - Marginal gains over baselines = weak paper

3. ABLATION PREPARATION: What components matter?
   - Baselines inform which features are important
```

### Baseline Categories

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BASELINE TAXONOMY                                    │
│                                                                         │
│  1. TRIVIAL BASELINES (Sanity Check)                                   │
│     ├── Random baseline                                                 │
│     ├── Majority class baseline                                         │
│     └── Simple heuristic (e.g., keyword matching)                       │
│                                                                         │
│  2. TRADITIONAL BASELINES (What existed before LLMs)                    │
│     ├── Rule-based systems                                              │
│     ├── Static analysis tools                                           │
│     └── Pattern matching approaches                                     │
│                                                                         │
│  3. LLM BASELINES (If your tool uses LLM)                              │
│     ├── Zero-shot LLM prompt                                            │
│     ├── Few-shot LLM prompt                                             │
│     └── Chain-of-thought LLM prompt                                     │
│                                                                         │
│  4. SOTA BASELINES (Recent published work)                              │
│     ├── Tools from related papers                                       │
│     └── Commercial tools (if applicable)                                │
│                                                                         │
│  5. ABLATION BASELINES (Components of your tool)                        │
│     ├── Tool without component A                                        │
│     ├── Tool without component B                                        │
│     └── Single-component versions                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Baseline Implementation Template

```python
# Baseline Implementation Pattern
from abc import ABC, abstractmethod

class Baseline(ABC):
    """Abstract base class for baselines."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique baseline name."""
        pass

    @abstractmethod
    def analyze(self, input_data) -> dict:
        """Run analysis and return results."""
        pass


class KeywordBaseline(Baseline):
    """Simple keyword matching baseline."""

    name = "keyword_only"

    def __init__(self, keywords: list[str]):
        self.keywords = keywords

    def analyze(self, input_data) -> dict:
        content = input_data.get("content", "")
        matches = [kw for kw in self.keywords if kw.lower() in content.lower()]
        return {"matches": matches, "count": len(matches)}


class LLMOnlyBaseline(Baseline):
    """Direct LLM prompt baseline (no tool orchestration)."""

    name = "llm_zero_shot"

    def __init__(self, llm):
        self.llm = llm

    def analyze(self, input_data) -> dict:
        prompt = f"""Analyze this content and extract relevant information.

Content:
{input_data.get("content", "")[:3000]}

Output JSON with your analysis."""

        response = self.llm.invoke(prompt)
        return {"raw_response": response}


class CodeOnlyBaseline(Baseline):
    """Static code analysis only (no NL understanding)."""

    name = "code_only"

    def analyze(self, input_data) -> dict:
        # Only analyze code blocks, ignore NL
        code_blocks = extract_code_blocks(input_data.get("content", ""))
        return static_analyze(code_blocks)
```

### Comparison Protocol

```python
def compare_approaches(tool, baselines: list[Baseline], test_set):
    """Compare tool against all baselines on same test set."""

    results = {"tool": [], "baselines": {b.name: [] for b in baselines}}

    for case in test_set:
        # Run main tool
        tool_result = tool.analyze(case)
        results["tool"].append(evaluate(tool_result, case.ground_truth))

        # Run each baseline
        for baseline in baselines:
            baseline_result = baseline.analyze(case)
            results["baselines"][baseline.name].append(
                evaluate(baseline_result, case.ground_truth)
            )

    # Calculate aggregate metrics
    summary = {
        "tool": aggregate_metrics(results["tool"]),
    }
    for name, res in results["baselines"].items():
        summary[name] = aggregate_metrics(res)

    return summary


def print_comparison_table(summary):
    """Print comparison as markdown table."""
    print("| Approach | Precision | Recall | F1 |")
    print("|----------|-----------|--------|-----|")
    for name, metrics in summary.items():
        print(f"| {name} | {metrics['precision']:.1%} | {metrics['recall']:.1%} | {metrics['f1']:.1%} |")
```

### Decision Gate 2

```
GATE 2 CRITERIA:

Your tool should:
□ Beat ALL trivial baselines significantly (>10% improvement)
□ Beat traditional baselines meaningfully (>5% improvement)
□ If using LLM: beat pure LLM baselines (shows orchestration adds value)
□ Be competitive with SOTA (within 5% or better)

If your tool DOES NOT beat trivial baselines:
→ The problem may be too easy
→ Or your tool has bugs
→ Do NOT proceed to full test

If your tool is SIMILAR to LLM-only:
→ Your contribution may be weak
→ Consider what your tool adds beyond just prompting
→ Focus on efficiency gains or specific capabilities
```

---

## Phase 3: Full Test & RQ Design

### When to Proceed

```
PROCEED TO FULL TEST IF:

✓ Gate 1 passed: Tool works on sample
✓ Gate 2 passed: Tool outperforms baselines
✓ Confident in methodology
✓ Ground truth labels available or obtainable

DO NOT PROCEED IF:

✗ Tool still buggy on partial test
✗ No improvement over baselines
✗ Unclear what contribution is
```

### Research Question Design

```
RQ DESIGN TEMPLATE:

RQ1: Effectiveness
"How effective is [Tool] at [Task] compared to baselines?"
- Metrics: Precision, Recall, F1, Accuracy
- Comparison: All baselines

RQ2: Efficiency
"How efficient is [Tool] compared to baselines?"
- Metrics: Time per case, API calls, Cost
- Comparison: Especially vs LLM-heavy approaches

RQ3: Ablation
"What is the contribution of each component?"
- Systematically remove components
- Measure performance impact

RQ4: Generalization (Optional)
"Does [Tool] generalize to different [domains/datasets]?"
- Cross-dataset evaluation
- Different case types
```

### Full Test Protocol

```python
def run_full_test(tool, baselines, full_dataset, output_dir):
    """Run comprehensive evaluation."""

    results = {
        "tool": {"predictions": [], "metrics": {}},
        "baselines": {b.name: {"predictions": [], "metrics": {}} for b in baselines},
        "ablations": {},
    }

    # 1. Run all systems on full dataset
    for case in tqdm(full_dataset, desc="Evaluating"):
        # Tool
        results["tool"]["predictions"].append({
            "case_id": case.id,
            "prediction": tool.analyze(case),
            "ground_truth": case.ground_truth,
        })

        # Baselines
        for baseline in baselines:
            results["baselines"][baseline.name]["predictions"].append({
                "case_id": case.id,
                "prediction": baseline.analyze(case),
                "ground_truth": case.ground_truth,
            })

    # 2. Calculate metrics
    for name in ["tool"] + [b.name for b in baselines]:
        data = results["tool" if name == "tool" else "baselines"][name]
        data["metrics"] = calculate_all_metrics(data["predictions"])

    # 3. Statistical tests
    results["statistics"] = statistical_analysis(results)

    # 4. Save results
    save_results(results, output_dir)

    return results
```

---

## Metrics & Statistical Analysis

### Metrics to Report

```
STANDARD METRICS:

For Classification/Detection:
- Precision, Recall, F1 (per class and macro)
- Accuracy
- AUC-ROC (if probabilistic)

For Generation/Extraction:
- Exact match accuracy
- Partial match (token overlap)
- BLEU/ROUGE (if text generation)

For Efficiency:
- Time per case (mean, median, std)
- API calls per case
- Cost per case (if applicable)

For Ranking:
- MRR (Mean Reciprocal Rank)
- nDCG
- Precision@k
```

### Statistical Tests

```python
from scipy import stats

def statistical_analysis(results):
    """Perform statistical tests."""

    tool_scores = [r["f1"] for r in results["tool"]["predictions"]]

    comparisons = {}
    for baseline_name, baseline_data in results["baselines"].items():
        baseline_scores = [r["f1"] for r in baseline_data["predictions"]]

        # Wilcoxon signed-rank test (paired, non-parametric)
        stat, p_value = stats.wilcoxon(tool_scores, baseline_scores)

        # Effect size (Cliff's delta)
        cliff_d = cliffs_delta(tool_scores, baseline_scores)

        comparisons[baseline_name] = {
            "wilcoxon_stat": stat,
            "p_value": p_value,
            "significant": p_value < 0.05,
            "cliff_delta": cliff_d,
            "effect_size": interpret_cliff(cliff_d),
        }

    return comparisons


def interpret_cliff(d):
    """Interpret Cliff's delta effect size."""
    d = abs(d)
    if d < 0.147:
        return "negligible"
    elif d < 0.33:
        return "small"
    elif d < 0.474:
        return "medium"
    else:
        return "large"
```

---

## Results Reporting

### Table Format

```markdown
## RQ1: Effectiveness

| Approach | Precision | Recall | F1 | p-value | Effect |
|----------|-----------|--------|-----|---------|--------|
| **SkillGuard** | **85.2%** | **82.1%** | **83.6%** | - | - |
| LLM-only | 71.3% | 78.4% | 74.7% | <0.01 | medium |
| Keyword-only | 45.2% | 89.1% | 60.0% | <0.01 | large |
| Code-only | 52.1% | 41.2% | 46.0% | <0.01 | large |
```

### Chart Generation

```python
import matplotlib.pyplot as plt

def plot_comparison(results, output_path):
    """Generate comparison bar chart."""

    approaches = ["SkillGuard"] + list(results["baselines"].keys())
    f1_scores = [results["tool"]["metrics"]["f1"]] + [
        results["baselines"][b]["metrics"]["f1"] for b in results["baselines"]
    ]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(approaches, f1_scores)
    bars[0].set_color('green')  # Highlight our tool

    plt.ylabel("F1 Score")
    plt.title("Comparison of Approaches")
    plt.ylim(0, 1)

    # Add value labels
    for bar, score in zip(bars, f1_scores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{score:.1%}', ha='center')

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
```

---

## Checklist Summary

```
EXPERIMENT WORKFLOW CHECKLIST:

PHASE 1: PARTIAL TEST
□ Select representative sample (10-20%)
□ Run tool on sample
□ Check: Tool works without crashing?
□ Check: Output format correct?
□ Check: Results plausible (manual inspection)?
□ GATE 1: Success rate >= 70%?

PHASE 2: BASELINES
□ Implement trivial baseline (keyword/random)
□ Implement traditional baseline (rule-based)
□ Implement LLM baseline (if applicable)
□ Run all baselines on same sample
□ GATE 2: Tool beats all baselines?

PHASE 3: FULL TEST
□ Expand to full dataset
□ Run all systems (tool + baselines)
□ Calculate metrics (P/R/F1/etc)
□ Statistical tests (Wilcoxon, Cliff's d)
□ GATE 3: Results statistically significant?

PHASE 4: ANALYSIS
□ Ablation studies
□ Error analysis
□ Generate tables and figures
□ Write RQ sections
```

---

## Example: Security Analysis Tool

```
EXAMPLE WORKFLOW: Permission Detection Tool

PHASE 1: Partial Test
- Sample: 30 skills (15% of 200)
- Run SkillGuard agent
- Results: 27/30 analyzed successfully (90%)
- Manual check: Permissions look reasonable
- GATE 1: ✓ PASSED

PHASE 2: Baselines
- Implemented:
  1. keyword_only: Match "execute", "delete", etc.
  2. code_only: AST analysis without NL
  3. llm_zero_shot: Direct GPT-4 prompt
  4. llm_cot: Chain-of-thought prompt

- Sample results:
  | Approach | P | R | F1 |
  |----------|---|---|-----|
  | SkillGuard | 85% | 82% | 83% |
  | keyword_only | 45% | 90% | 60% |
  | code_only | 52% | 41% | 46% |
  | llm_zero_shot | 71% | 78% | 74% |
  | llm_cot | 75% | 80% | 77% |

- GATE 2: ✓ PASSED (beats all baselines)

PHASE 3: Full Test
- Run on all 200 skills
- Statistical tests: p < 0.01, effect size = medium
- GATE 3: ✓ PASSED

→ Proceed to RQ1 writing
```
