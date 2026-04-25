# Writing Style for SE Papers

[← Back to Main](../SKILL.md)

Professional writing conventions for top-tier SE venues.

## Core Principles

### 1. Be Precise About Claims

**Bad (vague):**
> "Our tool works well on real-world programs."

**Good (precise):**
> "Our tool correctly repaired 45 of 50 bugs in the Defects4J benchmark,
> a 12% improvement over the previous state-of-the-art."

### 2. Avoid Overclaiming

**Bad (overclaiming):**
> "Our revolutionary approach solves the bug detection problem."

**Good (appropriately scoped):**
> "Our approach improves bug detection precision for null pointer
> exceptions in Java programs with complex control flow."

### 3. Write Prose, Not Bullets

Methodology and approach sections should be **flowing prose paragraphs**, not bullet lists.

**Bad:**
```latex
\paragraph{Detection Phase}
\begin{itemize}
    \item Parse requirements.txt
    \item Extract version constraints
    \item Check for conflicts
\end{itemize}
```

**Good:**
```latex
The detection phase analyzes project configuration files to identify
constraint-based conflicts. We parse dependency specifications from
\texttt{requirements.txt}, \texttt{setup.py}, and \texttt{pyproject.toml},
extracting version constraints into a normalized representation.
Conflict detection proceeds through constraint intersection...
```

---

## SE Terminology

Use SE terms correctly:

| Term | Correct Usage |
|------|---------------|
| **Bug vs Defect vs Fault** | Bug = colloquial; Fault = in code; Failure = observed behavior |
| **Precision vs Accuracy** | Precision = TP/(TP+FP); Accuracy = (TP+TN)/all |
| **Sound vs Complete** | Sound = no false negatives; Complete = no false positives |
| **Static vs Dynamic** | Static = without execution; Dynamic = with execution |
| **Intra- vs Inter-** | Intra = within (one function); Inter = across (multiple) |

---

## Formatting Guidelines

### Minimal Formatting

Do NOT overuse `\textbf{}` and `\emph{}`:

**Bad (over-formatted):**
```latex
\emph{Standard library shadows.} PyPI packages that share names...

\emph{Ecosystem transitions.} Packages superseded by successors...
```

**Good (flowing prose):**
```latex
The database covers four categories: (1) standard library shadows,
where PyPI packages share names with built-in modules; (2) ecosystem
transitions, where packages are superseded by incompatible successors;
(3) mutual exclusivity, where package pairs cannot coexist.
```

### When to Use Bold
- Tool names (first mention): **PyVersionHealer**
- Best results in tables: **80%**
- Column headers: **Approach**

### When to Use Italics
- Definitions (first use): A *transitive conflict* occurs when...
- Mathematical variables: Let *n* be the number of packages
- Emphasis (sparingly): This is *fundamentally* different

---

## Common Mistakes

### 1. Passive Voice Overuse

**Bad:** "The conflicts were detected by our tool."
**Good:** "Our tool detected the conflicts."

Use passive voice when the actor is unknown or unimportant, not as default.

### 2. Hedging Too Much

**Bad:** "Our approach might possibly help to somewhat improve..."
**Good:** "Our approach improves detection rate by 14%."

Be confident when evidence supports your claims.

### 3. Informal Language

**Bad:** "This stuff is really hard to deal with."
**Good:** "This challenge presents significant complexity."

### 4. First Person Inconsistency

Pick either "we" or impersonal and be consistent:

**Consistent:** "We implement... We evaluate... We find..."
**Also consistent:** "The tool implements... The evaluation shows..."

---

## Numbers and Units

### Spell Out vs Digits
- Spell out: one through nine
- Use digits: 10 and above, measurements, percentages

**Examples:**
- "We analyzed three projects..."
- "We analyzed 50 projects..."
- "achieving 80% accuracy..."
- "with a 5-minute timeout..."

### Statistical Values
- Always include: metric, test, p-value, effect size
- Format: "Wilcoxon signed-rank test, p < 0.001, Cliff's d = 0.42"

---

## Citations

### In-Sentence vs Parenthetical

**In-sentence:** "Wang et al.~\cite{wang2020pyego} propose..."
**Parenthetical:** "Knowledge graphs have been used for dependency analysis~\cite{wang2020pyego}."

### Multiple Citations
Group related citations: `~\cite{wang2020pyego, ye2022pycre, chen2024pllm}`

### Self-Citations (Double-Blind)
```latex
Prior work by [anonymous]~\cite{omitted_for_review} showed...
% OR
Our prior work~\cite{anonymous2023} established...
```

---

## LaTeX Best Practices

### Lists (enumerate/itemize)

Always use `leftmargin=*` to remove the default indentation, which wastes precious column space in two-column formats. Requires `\usepackage{enumitem}` in the preamble.

```latex
% In preamble:
\usepackage{enumitem}

% ALWAYS use leftmargin=* :
\begin{itemize}[leftmargin=*]
    \item First item
    \item Second item
\end{itemize}

\begin{enumerate}[leftmargin=*]
    \item First item
    \item Second item
\end{enumerate}
```

### Non-Breaking Spaces
Use `~` before citations and references:
```latex
as shown by Wang~\cite{wang2020pyego}
see Section~\ref{sec:eval}
in Figure~\ref{fig:arch}
```

### Code and Tools
```latex
% Tool names
\tool{}  % define with \newcommand{\tool}{PyVersionHealer}

% Inline code
\texttt{requirements.txt}

% File paths
\texttt{src/main.py}
```

### Mathematical Notation
```latex
% Inline math
where $n$ is the number of packages

% Display math (equations)
\begin{equation}
  precision = \frac{TP}{TP + FP}
\end{equation}
```

---

## Tone Guidelines

### Be Humble About Comparisons

**Bad (disparaging prior work):**
> "PyEGo's approach is fundamentally flawed and fails..."

**Good (constructive):**
> "PyEGo provides a strong foundation, achieving 66% coverage.
> Our approach builds on this by adding complementary strategies."

### Acknowledge Limitations

**Bad:** "Our tool solves all dependency conflicts."
**Good:** "Our tool detects 80% of conflicts; runtime-only conflicts
remain beyond installation-time analysis."

### Credit Prior Work

**Bad:** "We are the first to address this problem."
**Good:** "Building on PyEGo's knowledge graph approach, we extend
detection to include semantic conflicts."

---

## Tables and Figures

### Table Width Rules

Tables MUST fit the column width exactly. In double-column format, this is non-negotiable — overfull hbox from tables causes visible margin overflow.

```latex
% GOOD: Table fits column width
\begin{table}[t]
\caption{Detection results across six libraries.}
\label{tab:results}
\footnotesize  % Use smaller font if needed to fit
\begin{tabular}{lrrr}
\toprule
Library & Precision & Recall & F1 \\
\midrule
...
\end{tabular}
\end{table}

% GOOD: Wide table spanning both columns (only when genuinely needed)
\begin{table*}[t]
\caption{Per-category results across all baselines.}
...
\end{table*}

% BAD: Forcing column-width table with too many columns
% → Fix: use table* or reduce columns or abbreviate headers
```

### No Redundant Visualizations

If a table already shows the results, do NOT add a bar chart of the same numbers. Choose the form that best communicates the finding:

- **Table**: when readers need exact numbers (comparisons, replication)
- **Bar/line chart**: when the finding is about trends, patterns, or relative differences
- **Heatmap**: when showing coverage or correlation matrices
- **Diagram**: when showing architecture, workflow, or relationships

**Rule:** One visualization per dataset. Every float must earn its column-inches.

## Checklist

- [ ] Claims are precise with numbers
- [ ] No overclaiming beyond evaluation evidence
- [ ] Methodology written as prose, not bullets
- [ ] SE terminology used correctly
- [ ] Minimal formatting (no excessive bold/italic)
- [ ] Consistent voice (we vs impersonal)
- [ ] Numbers formatted correctly
- [ ] Non-breaking spaces before citations/refs
- [ ] Humble tone in comparisons
- [ ] Limitations acknowledged
- [ ] All tables fit column width — zero overfull hbox from tables
- [ ] No redundant table+figure pairs showing the same data

[Back to Main →](../SKILL.md)
