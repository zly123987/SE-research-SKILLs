# Section 4: Evaluation

[← Back to Main](../SKILL.md) | [← Methodology](03-methodology.md)

The evaluation section is typically the longest (4-5 pages) and most scrutinized section. Organize around explicit Research Questions (RQs).

## Structure Overview

```latex
\section{Evaluation}
\label{sec:evaluation}

We evaluate \tool{} to answer the following research questions:
\begin{description}
    \item[RQ1 (Effectiveness):] How effective is \tool{} compared to baselines, and what types of errors remain?
    \item[RQ2 (Application):] How well does \tool{} perform on real-world projects outside the benchmark?
    \item[RQ3 (Ablation):] How does each component contribute?
    \item[RQ4 (Efficiency):] What is the runtime and cost? % OPTIONAL: include for LLM/cost-sensitive tools
\end{description}

\subsection{Experimental Setup}
% Dataset, baselines, metrics, environment

\subsection{RQ1: Effectiveness}
% ~1.5 pages: main results + error analysis integrated
% Error analysis belongs HERE, not as a standalone RQ

\subsection{RQ2: Real-World Application}
% ~1 page: projects outside benchmark with test suites

\subsection{RQ3: Ablation Study}
% ~1 page

\subsection{RQ4: Efficiency}  % OPTIONAL
% ~0.5 page: runtime, cost, LLM calls
% Recommended for LLM-based tools or tools with significant runtime
```

## Research Questions Format

### Common RQ Types

| RQ Type | Purpose | Example |
|---------|---------|---------|
| **Effectiveness** | Main results vs baselines + error analysis | "How effective is TOOL, and what errors remain?" |
| **Application** | Real-world case study outside benchmark | "How well does TOOL work on real projects?" |
| **Ablation** | Component contribution | "How does each component contribute?" |
| **Efficiency** | Runtime, memory, cost | "What is the runtime overhead?" |
| **Sensitivity** | Parameter effects | "How sensitive is TOOL to threshold T?" |
| **Generalizability** | Cross-domain performance | "Does TOOL generalize to other languages?" |

### RQ Guidelines
- 3-4 RQs is typical
- Each RQ should occupy ~1 page
- RQs should be independent (answerable separately)
- RQ1 is always effectiveness/main results, with error analysis integrated (not a standalone RQ)
- RQ2 is typically a real-world application study showing the tool works beyond the benchmark
- Error analysis should be part of RQ1's narrative: results → breakdown by category → error taxonomy → answering box
- Efficiency (runtime, cost) is optional but recommended for tools that consume significant time or money (e.g., LLM-based tools with API costs, tools with long runtimes). Not mandatory for all tools.

## Experimental Setup (REQUIRED Elements)

Every evaluation must explicitly describe:

```latex
\subsection{Experimental Setup}


\textbf{Benchmark Dataset.}
% Source, size, selection criteria, characteristics
We evaluate on the PyEGo benchmark~\cite{wang2020pyego}, a curated dataset
of 50 real-world Python projects with documented dependency conflicts.
Projects span diverse domains (web: 30\%, data science: 25\%, security: 20\%,
utilities: 25\%) with dependency counts ranging from 5 to 200+.

\textbf{Baselines.}
% Name, citation, brief description
\begin{itemize}[leftmargin=*]
    \item \textbf{PyEGo}~\cite{wang2020pyego}: State-of-the-art knowledge
      graph approach from ESEC/FSE 2020.
    \item \textbf{Static-only}: Our static detection layer in isolation.
    \item \textbf{Pip-only}: Dynamic detection through pip's resolver.
    \item \textbf{Hybrid}: Static + dynamic without LLM reasoning.
\end{itemize}

\textbf{Metrics.}
% Precise definition of each metric
\begin{itemize}[leftmargin=*]
    \item \textbf{Detection Rate}: Percentage of projects where conflicts
      are correctly identified.
    \item \textbf{Resolution Rate}: Percentage of detected conflicts for
      which repairs are generated.
    \item \textbf{ISR}: Percentage of repairs that pass \texttt{pip install}.
\end{itemize}

\textbf{Environment.}
% Hardware, software, LLM model. Ensure the correct LLM model is confirmed by viewing the settings or configs of this project.
Ubuntu 22.04, Python 3.10, GPT-4o via OpenAI API (temperature 0.0),
4 parallel workers, Intel i7-12700K, 32GB RAM.
```
## Dataset Selection Guidelines

**Prioritize the datasets published in the previous work if they are applicable.**

**Elaborate an unbiased dataset collection approach for newly collected dataset with why**


## Baseline Selection Guidelines

**Every baseline must be justified. Reviewers will ask "Why these baselines?"**

**Naive Regex is usually not considered a valid baseline**

**Raw LLMs are great baseline usually accompanied with zero shots or few shots for comprehensiveness if necessary**

### Include Baselines with Rationale

```latex
\textbf{Baselines.} We compare against four approaches spanning the
solution space:

\begin{itemize}[leftmargin=*]
    \item PyEGo~\cite{wang2020pyego}: The state-of-the-art knowledge graph
      approach, selected as the primary baseline because it represents
      the most recent published work (ESEC/FSE 2020).
    \item Static-only and Pip-only: Ablation variants isolating individual
      detection strategies.
    \item Hybrid (Static+Pip): Multi-strategy baseline without LLM.
\end{itemize}
```

### Explain Excluded Baselines

```latex
We do not compare against PLLM~\cite{chen2024pllm} because its
implementation is not publicly available. We contacted the authors
but did not receive responses by submission time.
```

### Valid Exclusion Reasons
- Artifact unavailable (code not released)
- Infrastructure requirements prevent reproduction
- Input format incompatibility
- Authors unresponsive
- Tool deprecated

## Metrics Selection Guidelines

### Use Established Metrics with Citations

```latex
\textbf{Metrics.} Following the evaluation methodology of prior
dependency conflict research~\cite{wang2020pyego, chen2024pllm}:

\begin{itemize}[leftmargin=*]
    \item \textbf{Detection Rate}: Standard effectiveness metric used
      by PyEGo~\cite{wang2020pyego}.
    \item \textbf{Installation Success Rate (ISR)}: We introduce this
      metric to measure repair reliability---addressing the validation
      gap in prior work.
\end{itemize}
```

### Justify New Metrics

If introducing a metric not used in prior work, explain why:

```latex
We introduce Installation Success Rate (ISR) because prior work
evaluates repairs through manual inspection or does not validate
repairs at all. ISR provides an objective, reproducible measure.
```

## Writing Each RQ (~1 page per RQ)

### Structure

1. **Results table/figure** with data
2. **Comparison with baselines** - explain WHY
3. **Error analysis** - categorize failures
4. **"Answering RQ" box** - summary at END

### Example: RQ1 (Effectiveness)

```latex
\subsection{RQ1: Effectiveness}

Table~\ref{tab:main-results} shows the detection and resolution rates.

\begin{table}[t]
\centering
\caption{Main Results on PyEGo Benchmark (50 cases)}
\label{tab:main-results}
\begin{tabular}{@{}lrrr@{}}
\toprule
\textbf{Approach} & \textbf{Detected} & \textbf{Rate} & \textbf{$\Delta$} \\
\midrule
Static-only & 33/50 & 66\% & --- \\
Pip-only & 14/50 & 28\% & $-$38\% \\
PyEGo~\cite{wang2020pyego} & 33/50 & 66\% & --- \\
\midrule
\textbf{Hybrid++ (Ours)} & \textbf{40/50} & \textbf{80\%} & \textbf{+14\%} \\
\bottomrule
\end{tabular}
\end{table}

\textbf{Comparison with Baselines.}
The 14-percentage-point improvement over PyEGo stems from three
capabilities that complement PyEGo's knowledge graph approach:
(1) dynamic detection catches 3 transitive conflicts invisible to
static analysis; (2) LLM semantic detection identifies 4 ecosystem
conflicts (package bundling, renames); (3) validation prevents false
positives that PyEGo would report.

\textbf{Error Analysis.}
% Make \textbf{Error Analysis} bold for clarity. The analysis should be detailed and attributed to irresistable reasons instead of the some easily solvable reasons. 
% Should not focus on the absolute numbers of failures too much to avoid the bad impression of ineffective tool.
\tool failed to detect conflicts in 10 cases. We categorize:

\begin{itemize}[leftmargin=*]
    \item \textbf{Runtime-only conflicts (3 cases)}: Issues that manifest
      only during code execution, fundamentally beyond installation-time
      analysis.
    \item \textbf{Undocumented constraints (3 cases)}: Implicit requirements
      not specified in any package metadata.
    \item \textbf{Optional dependencies (4 cases)}: Conflicts in
      \texttt{extras\_require}---straightforward future work.
\end{itemize}

\begin{tcolorbox}[title=Answering RQ1,colback=gray!10,colframe=gray!50]
\tool{} achieves 80\% detection rate, outperforming PyEGo (66\%) by
14 percentage points. The improvement is statistically significant
(Fisher's exact test, $p = 0.032$, Cliff's $\delta = 0.21$).
\end{tcolorbox}
```

## Effectiveness Writing Guidelines

### Humble Claims

**Bad (criticizing prior work):**
> "PyEGo's approach is fundamentally limited and fails..."

**Good (humble acknowledgment):**
> "PyEGo's knowledge graph approach provides a strong foundation,
> achieving 66% coverage. \tool{} builds upon this by adding
> complementary strategies."

### Error Analysis Requirements

**CRITICAL**: Failures must be fundamentally beyond scope—not fixable bugs.

**Valid failure categories:**
- Runtime-only issues requiring dynamic execution
- Undocumented constraints not in metadata
- Fundamentally unresolvable conflicts

**Invalid failure categories (should have been fixed):**
- Parser limitations that could be extended
- Missing patterns that could be added

## Ablation Study (RQ3)

Every evaluation needs ablation. Show each component's contribution:

```latex
\subsection{RQ3: Ablation Study}

\begin{table}[t]
\centering
\caption{Ablation Study: Component Contribution}
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Configuration} & \textbf{Detection} & \textbf{$\Delta$} \\
\midrule
Full \tool{} & 80\% & --- \\
$-$ Static Detection & 34\% & $-$46\% \\
$-$ Dynamic Detection & 74\% & $-$6\% \\
$-$ LLM Detection & 72\% & $-$8\% \\
\bottomrule
\end{tabular}
\end{table}

\begin{tcolorbox}[title=Answering RQ3,colback=gray!10,colframe=gray!50]
Each component contributes uniquely. Static detection is most critical
($-$46\%), but dynamic (+6\%) and LLM (+8\%) layers each add coverage
that static analysis cannot achieve.
\end{tcolorbox}
```

## "Answering RQ" Box Format

**Place at END of each RQ subsection.** Use tcolorbox:

```latex
% Add to preamble
\usepackage{tcolorbox}
\tcbuselibrary{skins}

% Usage
\begin{tcolorbox}[title=Answering RQ1,colback=gray!10,colframe=gray!50]
Summary with numbers and statistical significance.
\end{tcolorbox}
```

If no tcolorbox, use simple box:
```latex
\noindent\fbox{\parbox{\linewidth}{
\textbf{Answering RQ1:} Summary...
}}
```

## Statistical Analysis

See [common/statistics.md](../common/statistics.md) for full details.

Quick reference:
```latex
% Report: metric, test, p-value, effect size
Our approach achieves 85.2\% precision compared to 72.1\% for the baseline
(Wilcoxon signed-rank test, $p < 0.001$, Cliff's $d = 0.42$, medium effect).
```

## Table Formatting

Use `booktabs` for professional tables:

```latex
\usepackage{booktabs}

\begin{tabular}{@{}lrrr@{}}
\toprule
\textbf{Approach} & \textbf{Detected} & \textbf{Rate} & \textbf{$\Delta$} \\
\midrule
Baseline & 33/50 & 66\% & --- \\
\textbf{Ours} & \textbf{40/50} & \textbf{80\%} & \textbf{+14\%} \\
\bottomrule
\end{tabular}
```

### Table Guidelines
- Use `\toprule`, `\midrule`, `\bottomrule` (NEVER `\hline`)
- Bold your approach's row and best results
- Include $\Delta$ column showing improvement
- Caption ABOVE table

## Checklist

- [ ] 3-5 RQs defined at section start
- [ ] Experimental setup covers dataset, baselines, metrics, environment
- [ ] Baselines are justified (why included, why excluded)
- [ ] Metrics are defined precisely with citations
- [ ] Each RQ has ~1 page of content
- [ ] Each RQ has results → comparison → error analysis → "Answering RQ"
- [ ] "Answering RQ" boxes at END of each subsection
- [ ] Statistical tests with effect sizes included
- [ ] Ablation study present
- [ ] Tables use booktabs formatting
- [ ] After RQs, no need to add a discussion subsection which should be placed in the discussion sections for empirical studies. 
- [ ] Total length 4-6 pages

[← Methodology](03-methodology.md) | [Next: Discussion →](05-discussion.md)
