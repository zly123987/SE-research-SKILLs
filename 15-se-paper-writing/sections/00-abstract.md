# Abstract Writing for SE Papers

The abstract is the most-read part of your paper. It must immediately communicate the problem's significance and your contribution in 150-250 words.

## The Narrative Chain: Problem → Consequence → Difficulty → Solution

**CRITICAL**: A strong abstract tells a coherent story where each element leads to the next:

```
PROBLEM (what) → CONSEQUENCE (so what) → DIFFICULTY (why hard) → SOLUTION (our answer)
                                              ↓
                                    [Solution MUST address the difficulty directly]
```

The solution's design should **directly correspond** to the stated difficulty. If the difficulty is "implicit constraints are hard to spot," the solution should explain how it spots them.

---

## Structure: The 5-Part Abstract

### 1. Problem Statement (1 sentence)
State the specific problem. Include prevalence if you have data.

**Weak:**
> Dependency conflicts affect 25-40% of Python projects and waste significant developer time.

**Problem:** States prevalence but doesn't explain *what happens* or *why it matters*.

**Strong:**
> Dependency conflicts affect 25-40% of Python projects, causing build failures that block CI/CD pipelines and runtime crashes that corrupt production systems.

**Why better:** Explains the *mechanism of harm*—not just "wastes time" but specifically how: build failures, runtime crashes, production impact.

---

### 2. Consequence: Why This Matters (1 sentence)
Explain the **downstream impact** if the problem isn't solved. Be specific about who suffers and how.

**Weak:**
> This wastes developer time.

**Strong:**
> Because dependency graphs form complex webs of transitive constraints, a single conflict can cascade into dozens of broken packages, forcing developers to manually trace version incompatibilities across hundreds of dependency paths.

**Why better:** Explains the *amplification effect*—one conflict → dozens of breaks → manual tracing. This is much more severe than "wastes time."

---

### 3. Difficulty: Why This is Hard (1-2 sentences)
Explain **why existing approaches fail** and what makes the problem fundamentally challenging. This is where you set up your solution.

**CRITICAL:** The difficulty you describe must **directly correspond** to your solution's novelty.

**Weak:**
> Existing tools are limited.

**Strong:**
> Prior approaches rely on pattern-based detection of explicit version constraints, but many conflicts arise from *implicit* semantic relationships—package bundling, API deprecations, ecosystem transitions—that are not declared in metadata and require deep domain knowledge to identify.

**Why better:**
- Identifies the specific gap: "implicit semantic relationships"
- Names concrete examples: bundling, deprecations, transitions
- States what's missing: "deep domain knowledge"

**The narrative setup:** If the difficulty is "implicit constraints require domain knowledge," your solution MUST explain how it provides that knowledge (e.g., LLM reasoning).

---

### 4. Our Solution (1-2 sentences)
Present your approach. **Explicitly connect it to the stated difficulty.**

**Pattern:**
> We present [Tool], which [addresses difficulty] by [novel mechanism].

**Weak:**
> We present PyVersionHealer, a hybrid approach combining static analysis and LLM reasoning.

**Problem:** Doesn't explain *why* this combination solves the stated difficulty.

**Strong:**
> We present PANACEA, which addresses both explicit and implicit conflicts through a hybrid strategy: static analysis detects declared constraint violations, dynamic resolution catches transitive conflicts invisible in project files, and LLM-based semantic reasoning identifies implicit relationships that require ecosystem knowledge—directly addressing the domain knowledge gap that pattern-based approaches cannot fill.

**Why better:** Each component of the solution maps to a specific part of the difficulty:
- Static analysis → explicit constraints
- Dynamic resolution → transitive conflicts
- LLM reasoning → implicit relationships requiring domain knowledge

---

### 5. Results (1-2 sentences)
Quantitative results with baseline comparison and statistical significance.

**Pattern:**
> On [benchmark], [Tool] achieves [metrics], a [X]-point improvement over [baseline] (p=[significance]).

**Example:**
> On 50 real-world Python projects, PANACEA achieves 80% detection rate and 100% installation success rate for generated repairs, a statistically significant 14-point improvement over pattern-based approaches (Fisher's exact, p=0.032).

---

## Complete Abstract Example (Strong Version)

> Dependency conflicts affect 25-40% of Python projects, causing build failures that block CI/CD pipelines and runtime crashes that corrupt production systems. Because dependency graphs form complex webs of transitive constraints, a single conflict can cascade into dozens of broken packages, forcing developers to manually trace version incompatibilities across hundreds of dependency paths. Prior approaches rely on pattern-based detection of explicit version constraints, but many conflicts arise from implicit semantic relationships—package bundling, API deprecations, ecosystem transitions—that require deep domain knowledge to identify. We present PANACEA, a hybrid approach that addresses both explicit and implicit conflicts: static analysis detects declared constraint violations, dynamic resolution catches transitive conflicts invisible in project files, and LLM-based semantic reasoning identifies implicit relationships that pattern-based methods miss. On 50 real-world Python projects, PANACEA achieves 80% detection rate and 100% installation success rate, a statistically significant 14-point improvement over the state-of-the-art (p=0.032).

**Word count:** 156 words

**Narrative coherence check:**
- ✅ Problem: Conflicts cause build failures and runtime crashes (specific harm)
- ✅ Consequence: Cascading failures, manual tracing of hundreds of paths (amplification)
- ✅ Difficulty: Implicit semantic relationships require domain knowledge (specific gap)
- ✅ Solution: Hybrid with LLM reasoning for domain knowledge (directly addresses gap)
- ✅ Results: Quantitative improvement with statistical significance

---

## The "So What" Test

For each sentence in your abstract, ask: **"So what?"**

| Statement | So What? | Improved |
|-----------|----------|----------|
| "Affects 25% of projects" | So what happens to them? | "...causing build failures and runtime crashes" |
| "Wastes developer time" | Why specifically? | "...manually tracing incompatibilities across hundreds of paths" |
| "Existing tools are limited" | Limited how? | "...cannot detect implicit semantic relationships" |
| "We use LLM reasoning" | Why does that help? | "...to identify implicit relationships that require ecosystem knowledge" |

---

## Common Abstract Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| **Prevalence without consequence** | "Affects X%" but no harm explained | Add specific harm mechanism |
| **Vague consequences** | "Wastes time" without explaining how | Name specific failures (build, runtime, production) |
| **Difficulty doesn't match solution** | Says problem is X, solution addresses Y | Ensure solution directly addresses stated difficulty |
| **Solution without rationale** | "We use technique X" without why | Explain why X addresses the specific difficulty |
| **Missing amplification** | Single problem stated | Show cascading/compounding effects |

---

## Abstract Checklist

Before finalizing your abstract:

- [ ] Does it explain the **mechanism of harm** (not just "wastes time")?
- [ ] Does it show **amplification** (how one problem cascades)?
- [ ] Does the difficulty explain **why existing approaches fail**?
- [ ] Does the solution **directly address** the stated difficulty?
- [ ] Are results quantitative with **baseline comparison and significance**?
- [ ] Is there a **coherent narrative chain** from problem to solution?
- [ ] Is it within the word limit (typically 150-250)?

---

## Venue-Specific Requirements

| Venue | Word Limit | Notes |
|-------|------------|-------|
| ICSE | 150 words | Strict limit |
| FSE | 200 words | Strict limit |
| ASE | 200 words | |
| ISSTA | 150 words | Strict limit |
| TSE | 250 words | Journal, more space |
| EMSE | 250 words | Journal |
