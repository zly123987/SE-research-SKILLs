# SE Paper Types

[← Back to Main](../SKILL.md)

Identify your paper type first—it determines structure, evaluation expectations, and page limits.

## Paper Type Overview

| Paper Type | What It Contributes | Typical Venues | Evaluation Focus |
|------------|---------------------|----------------|------------------|
| **Technique Paper** | New method + tool + evaluation | ICSE, FSE, ASE | Effectiveness, baselines |
| **Empirical Study** | Large-scale analysis | FSE, MSR, EMSE | RQs, statistical analysis |
| **Tool Paper** | Mature, available tool | ICSE Demo, ASE Tool | Usefulness, features |
| **Benchmark Paper** | Dataset for community | MSR Data, ISSTA | Quality, diversity |
| **Replication Study** | Reproduce + extend | MSR, EMSE | Original vs. replicated |
| **Experience Report** | Industry lessons | ICSE SEIP | Practical insights |

---

## Technique Paper

The most common SE paper type. Presents a new method/algorithm, implements it as a tool, and evaluates against baselines.

### Structure

```
1. Introduction (1.5-2 pages)
2. Background and Motivation (1-1.5 pages)
3. Approach / Methodology (2-3 pages)
4. Implementation (0.5-1 page)
5. Evaluation (4-6 pages)
6. Discussion (0.5-1 page)
   - Threats to validity (required)
   - Limitations (recommended)
7. Related Work (1-1.5 pages)
8. Conclusion (0.5 page)
```

### Evaluation Requirements
- 3-5 research questions
- Multiple baselines (including recent SOTA)
- Ablation study
- Statistical analysis with effect sizes
- Error analysis

### Key Sections
- **Methodology**: Technical depth, novelty articulation
- **Evaluation**: Largest section (~1 page per RQ)

---

## Empirical Study

Large-scale analysis answering research questions about software practices, tools, or phenomena.

### Structure

```
1. Introduction (1.5 pages)
   - Research gap
   - RQ1-RQ4 preview
   - Key findings

2. Background (0.5-1 page)
   - Definitions
   - Prior work context

3. Study Design (2-3 pages)
   - Data collection methodology
   - Subject selection criteria
   - Variables and metrics
   - Analysis approach

4. Results (4-5 pages, ~1 page per RQ)
   - Per-RQ findings
   - Statistical results
   - "Answering RQ" boxes

5. Discussion (1-1.5 pages)
   - Implications for researchers
   - Implications for practitioners
   - Surprising findings

6. (Optional) Lessons Learned (0-0.5 page)
   - Include only if non-redundant and actionable

7. Related Work (1 page)

8. Conclusion (0.5 page)
```

### Evaluation Requirements
- Clear RQs (research questions)
- Large dataset (typically 100+ subjects)
- Statistical analysis
- Effect sizes and confidence intervals
- Reproducibility package

### Key Differences from Technique Papers
- No tool implementation required
- Study design section instead of methodology
- Discussion section emphasized
- Findings focus on insights, not tool performance

---

## Tool Paper / Demo Paper

Presents a mature, publicly available tool with novel features. Shorter format focused on demonstrating capabilities.

### Structure (ICSE Demo - 4 pages)

```
1. Introduction (0.5-1 page)
   - Tool purpose
   - Key features
   - Availability

2. Tool Overview (1-1.5 pages)
   - Architecture
   - Main features
   - Usage workflow

3. Implementation (0.5 page)
   - Technology stack
   - Scale/performance

4. Evaluation / Case Study (1 page)
   - Usage examples
   - Comparison with alternatives

5. Related Tools (0.5 page)

6. Conclusion (0.25 page)
```

### Requirements
- Tool must be publicly available
- Demo video often required
- Focus on usability and features
- Less emphasis on novelty, more on engineering

---

## Benchmark / Dataset Paper

Contributes a new dataset or benchmark for community use.

### Structure

```
1. Introduction
   - Need for this benchmark
   - Gap in existing datasets

2. Related Benchmarks
   - Comparison with existing datasets

3. Benchmark Design
   - Collection methodology
   - Curation criteria
   - Quality assurance

4. Benchmark Statistics
   - Size, diversity, coverage
   - Distribution analysis

5. Baseline Evaluation
   - Run existing tools on benchmark
   - Establish baseline metrics

6. Availability and Maintenance
   - How to access
   - Maintenance plan

7. Conclusion
```

### Requirements
- Dataset must be publicly available
- Clear collection methodology
- Baseline results from existing tools
- Maintenance commitment

---

## Replication Study

Reproduces and extends prior work to validate or challenge findings.

### Structure

```
1. Introduction
   - Original study
   - Why replicate

2. Original Study Summary
   - Methods
   - Key findings

3. Replication Design
   - What's replicated exactly
   - Extensions/variations

4. Results
   - Comparison: original vs. replicated
   - New findings from extensions

5. Discussion
   - Confirmations
   - Discrepancies and explanations

6. Discussion
   - Threats to validity (required)
   - Limitations

7. Conclusion
```

### Types of Replication
| Type | Description |
|------|-------------|
| **Exact** | Same data, same methodology |
| **Conceptual** | Different data, same methodology |
| **Extension** | Same foundation, new aspects |

---

## Experience Report (ICSE SEIP)

Industry-focused paper sharing practical lessons from real deployments.

### Structure

```
1. Introduction
   - Industry context
   - Problem addressed

2. Background
   - Company/project context
   - Technical environment

3. Approach / Solution
   - What was implemented
   - Key decisions

4. Results / Lessons Learned
   - Quantitative outcomes
   - Qualitative insights

5. Discussion
   - What worked
   - What didn't
   - Recommendations

6. Related Work

7. Conclusion
```

### Requirements
- Real industry deployment
- Concrete data/metrics
- Generalizable lessons
- Practitioner focus

---

## Choosing Your Paper Type

| If your contribution is... | Paper Type |
|---------------------------|------------|
| New algorithm + tool + evaluation | Technique |
| Large-scale data analysis | Empirical Study |
| Polished, available tool | Tool/Demo |
| New dataset for benchmarking | Benchmark |
| Validating prior work | Replication |
| Industry deployment lessons | Experience Report |

[Back to Main →](../SKILL.md)
