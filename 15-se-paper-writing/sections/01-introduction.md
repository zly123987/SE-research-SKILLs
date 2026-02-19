# Section 1: Introduction

[← Back to Main](../SKILL.md)

The introduction is the most important section of your paper. Reviewers use it to understand your contribution and decide whether to continue reading carefully.

## Structure: The Funnel

The introduction follows a "funnel" structure, moving from broad context to specific contribution:

```latex
% Paragraph 1: Context and background that introduce the concepts from common sense. Need to introduce the problem with layman words initially without definition(broad)
Software systems increasingly rely on X... The X is important because... X has a problem causing...

% Paragraph 2: Issues of Existing approaches to emphasize why X is hard to resolve. Better with proofs either from other papers or reports or our own evaluations in this paper with references (narrow)
The problem of X needs solutions. However, current approaches to X suffer from Y...This leads to problems such as Z in practice...

% Paragraph 3: Proposal with a general description of the essential methodology, such as knowledge-driven specification-based agent framwork. This paragraph can be merged with paragraph 4 if too short
To this end, we present TOOLNAME to address X which overcomes Y and effectively address Z, based on approach A. 

% Paragraph 4: Challenges correspond to the core novelty of our methodology of A. Challenges also map to the core gaps that are not addressed by current approaches. It is mandantory to have 3 challenges. Do not use bullets.
To achieve A, we face some challenges C1, C2, C3. TOOLNAME has Step S1, S2, S3... C1 is addressed by ... C2 is addressed by... C3 is addressed by...

% Paragraph 5: What are the results of the evaluations with real-world implications. Evaluations can be detached as a standalone paragraph if they are too long.
 Eventually, in the evaluation, TOOLNAME outperforms the current approaches by... The real-world applicability has also proved by...


% Paragraph 7: Contributions (bulleted)
In summary, this paper makes the following contributions:
\begin{itemize}[leftmargin=*]
  \item A technique for X that achieves Y
  \item An implementation, TOOLNAME, publicly available at...
  \item An evaluation on N benchmarks showing Z
\end{itemize}
```

## The "Key Insight" Paragraph

**This is the most important paragraph in your paper.** Reviewers use it to understand your contribution.

### Bad (describes what, not why):
> "We use machine learning to detect bugs."

### Good (explains the insight):
> "The key insight is that bug-introducing commits exhibit distinctive patterns in their AST diffs that are learnable from historical data, even when the bugs themselves are diverse."

### Writing Tips for Key Insight

1. **Be specific**: What exactly is the insight?
2. **Explain why it works**: Not just what you do, but why it succeeds
3. **Connect to the problem**: How does this insight address the gap?
4. **Be non-trivial**: The insight should not be obvious

## Contributions Format

Always list 3-4 contributions as bullets. Standard format:

```latex
In summary, this paper makes the following contributions:
\begin{itemize}[leftmargin=*]
  \item A technique for [PROBLEM] that [CAPABILITY]. (Section~\ref{sec:approach})
  \item An implementation, \tool{}, publicly available at [URL]. (Section~\ref{sec:impl})
  \item An evaluation on [N] [BENCHMARKS] showing [RESULT]. (Section~\ref{sec:eval})
\end{itemize}
```

### Contribution Types

| Type | Example |
|------|---------|
| **Technique** | A novel algorithm for detecting X |
| **Tool** | An implementation, TOOLNAME, available at... |
| **Empirical** | A study of N projects revealing... |
| **Dataset** | A benchmark of N cases for... |
| **Insight** | An analysis showing that Y causes Z |

## Length Guidelines

- **Total**: 1.5-2 pages
- **Context + Problem + Consequence**: ~0.5 pages
- **Gap + This Paper**: ~0.5 pages
- **Key Insight**: 1 paragraph (4-6 sentences)
- **Contributions**: ~0.25 pages

## Common Mistakes

### 1. Missing Key Insight
The introduction describes the approach but never explains WHY it works.

### 2. Vague Problem Statement
**Bad**: "Dependency management is hard."
**Good**: "Python projects frequently fail to install due to transitive dependency conflicts that are invisible until runtime."

### 3. Overclaiming
**Bad**: "We solve the dependency problem."
**Good**: "Our approach detects 80% of version conflicts in Python projects."

### 4. No Gap Analysis
**Bad**: Jumps from problem to solution without mentioning prior work.
**Good**: "Prior work (PyEGo, PLLM) addresses X but fails on Y because..."

### 5. Claims Don't Match Evaluation
Ensure your contribution claims match exactly what you evaluate and demonstrate.

## Checklist

- [ ] Context paragraph establishes broad relevance with problem introduction and consequences
- [ ] Existing work's issues paragraph is specific and concrete with proofs better and explains limitations
- [ ] "This paper" paragraph introduces your approach with intuition that it should be able to bridge the gap. 
- [ ] Key insight paragraph explains WHY your approach works with challenges.
- [ ] Contributions are 3-4 bullets matching evaluation results
- [ ] No overclaiming; claims are precise and supported
- [ ] No redundant expressions and keep the wording concise and sharp
- [ ] Do not overly use \emph or \textbf
- [ ] Do not use dash, use comma or which is instead
- [ ] Length is 1.5-2 pages

[Next: Background & Motivation →](02-background.md)