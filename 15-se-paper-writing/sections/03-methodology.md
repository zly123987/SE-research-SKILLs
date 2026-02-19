# Section 3: Methodology

[← Back to Main](../SKILL.md) | [← Background](02-background.md)

The methodology section describes HOW your approach works. This is where you demonstrate technical depth and novelty.

## Critical Writing Rule

**Write methodology as flowing prose paragraphs, NOT bullet points.**

### Bad (bullet-heavy):
```latex
\paragraph{Detection Phase}
\begin{itemize}[leftmargin=*]
    \item Parse requirements.txt
    \item Extract version constraints
    \item Check for conflicts
\end{itemize}
```

### Good (prose-based with technical depth):
```latex
\subsection{Static Conflict Detection}

The static detection layer analyzes project configuration files to identify
constraint-based conflicts without executing the dependency resolver. We
parse dependency specifications from \texttt{requirements.txt},
\texttt{setup.py}, and \texttt{pyproject.toml}, extracting version
constraints into a normalized representation that captures the acceptable
version range for each package.

Conflict detection proceeds through constraint intersection. For packages
appearing multiple times across configuration files, we compute the
intersection of their version ranges. An empty intersection indicates an
explicit conflict---for example, if one file specifies
\texttt{requests>=2.28} while another requires \texttt{requests<2.25},
no version can satisfy both constraints simultaneously.
```

## Required Structure (in order)

### 1. Problem Definition (first subsection)

Begin with a formal problem definition:

```latex
\subsection{Problem Definition}

\textbf{Input.} A Python project $P$ consisting of dependency configuration
files $\{f_1, f_2, ..., f_n\}$ where each $f_i$ specifies dependencies as
package-constraint pairs $(p, c)$.

\textbf{Output.} A set of detected conflicts $C$ where each conflict
$c \in C$ identifies the conflicting packages and constraints, and a
repair $R$ specifying version changes to resolve the conflict.

\textbf{Goal.} Maximize detection coverage (identify all conflicts) while
ensuring repair validity (repairs pass installation).
```

### Formal Notation for Structured Problems

When the problem has a formal structure (optimization, constraint satisfaction, graph transformation, etc.), use mathematical formulas to make the definition precise. Formulas help reviewers grasp the problem quickly and demonstrate rigor.

```latex
% Good: formal objective with constraints
Given a migration site set $S = \{s_1, \ldots, s_m\}$ and a mapping
function $\mu: S \rightarrow T$ that assigns each site a target API
transformation, we seek $\mu^*$ that maximizes correctness subject to
inter-site constraints:
\[
  \mu^* = \arg\max_{\mu} \sum_{s_i \in S} \mathbb{1}[\mu(s_i) \text{ correct}]
  \quad \text{s.t.} \quad \forall (s_i, s_j) \in E:\; \textsc{Compatible}(\mu(s_i), \mu(s_j))
\]
where $E$ captures data flow and coupling edges between sites.
```

Use formal notation when:
- The problem is naturally an optimization, constraint satisfaction, or graph problem
- A formula conveys the structure more precisely than prose alone
- The notation will be referenced later in the component descriptions

Do NOT use formulas when:
- The problem is purely procedural (just describe the pipeline)
- The formula would be trivially simple and adds no clarity over prose

### 2. Methodology Overview (second subsection)

Provide a high-level overview before diving into details:

```latex
\subsection{Overview}

Figure~\ref{fig:architecture} shows the architecture of \tool{}.
Given a project with dependency files, \tool{} applies three detection
layers hierarchically: (1) static pattern matching for explicit
constraints, (2) dynamic pip validation for resolver-level conflicts,
and (3) LLM semantic analysis for domain-specific conflicts.

This hierarchical design serves two purposes. First, cheaper detection
methods are applied before expensive LLM queries, reducing API costs.
Second, each layer addresses a distinct class of conflicts: static
analysis catches constraint violations visible in files, dynamic
validation catches transitive conflicts, and LLM reasoning catches
semantic conflicts requiring ecosystem knowledge.
```

### 3. Component Details (subsequent subsections)

For each component, provide:
- Technical description in flowing prose
- Formal notation where the procedure has mathematical structure (see below)
- Algorithm/pseudocode where complexity warrants it
- Running example showing the component in action
- Discussion of design decisions when introducing the details instead of listing a standalone paragraph

### Formal Notation in Component Details

Formal notation is not limited to problem definition. Use inline or display formulas within component descriptions whenever a procedure involves a well-defined mathematical operation. This demonstrates rigor and helps reviewers verify correctness.

Good candidates for formulas in component details:
- **Set operations**: site enumeration producing sets, union/intersection of constraints
- **Graph construction**: building edges from data flow (def-use chains, call graphs)
- **Scoring/ranking**: confidence scores, similarity measures, priority functions
- **Validation conditions**: formal predicates that must hold (type compatibility, coverage completeness)

```latex
% Good: formalizing a data flow analysis step
For each variable $v$ bound to a library-typed value at site $s_i$,
we compute the transitive closure of its def-use chain:
$\textsc{Uses}(v) = \{s_j \in S \mid s_j \text{ reads } v\}$.
Sites connected through shared variables form a migration unit
$U_k = \{s_i\} \cup \textsc{Uses}(v)$, and we add coupling edges
$(s_i, s_j) \in E$ for all $s_j \in \textsc{Uses}(v)$.

% Good: formalizing a validation condition
Coverage verification checks completeness:
$\textsc{Remaining}(P') = \{s \in \textsc{Discover}(P') \mid
  s \text{ references } L_s\} = \emptyset$.
Any non-empty result triggers targeted repair.
```

Keep formulas concise and embedded in prose. Avoid walls of notation without explanation.

**Equation overflow warning**: In two-column formats (IEEE, ACM sigconf), display equations easily overflow column width. For long formulas, use `\begin{multline}` or `\begin{aligned}` to break across lines. Always compile and visually check that no equation extends beyond the column margin.

## ReAct Agent Pattern

For LLM-based or agentic tools, follow the **ReAct (Reasoning + Acting)** pattern:

```latex
\subsection{Agent Architecture}

\tool{} employs a ReAct-style agent architecture that interleaves
reasoning and action. Given a project with dependency conflicts, the
agent first formulates a resolution plan based on conflict characteristics
detected in the initial analysis phase.

The agent autonomously orchestrates multiple resolution strategies:
static pattern matching executes first as a low-cost filter, followed
by dynamic pip validation for runtime verification. LLM reasoning is
invoked selectively---only when static and dynamic methods fail to
resolve the conflict---reducing API costs while preserving the ability
to handle semantically complex cases.

Results from each strategy are fused through a priority-based scheme:
validated resolutions take precedence, with confidence scores derived
from validation outcomes. The agent maintains working memory tracking
attempted resolutions and their outcomes, enabling informed backtracking
when initial strategies fail.
```

### Core Architecture Elements

| Element | Description |
|---------|-------------|
| **Planning Module** | Analyzes problem, formulates adaptive plan |
| **Tool Orchestration** | Autonomously calls static tools, decides when to invoke LLM |
| **Result Fusion** | Aggregates and reconciles results from multiple strategies |
| **Working Memory** | Tracks problem state, intermediate results, reasoning chain |
| **Long-term Memory** | (Optional) Persistent knowledge base for transfer learning |

## Formatting Guidelines

### Do NOT overuse formatting:
- Avoid excessive `\textbf{}` and `\emph{}`
- Bold sparingly (tool names, key metrics)
- Italics for definitions only
- Let content speak for itself

### Bad (over-formatted):
```latex
\emph{Standard library shadows.} PyPI packages that share names...

\emph{Ecosystem transitions.} Packages superseded by successors...
```

### Good (flowing prose):
```latex
The database covers four categories: (1) standard library shadows,
where PyPI packages share names with built-in modules; (2) ecosystem
transitions, where packages are superseded by incompatible successors;
(3) mutual exclusivity, where package pairs cannot coexist; and
(4) internal bundling, where packages vendor dependencies internally.
```

## Algorithm Formatting

Use algorithms sparingly—only when logic is complex enough to warrant formal specification.

```latex
\begin{algorithm}[t]
\caption{Hybrid Conflict Detection}
\label{alg:detection}
\KwIn{Project $P$ with dependency files}
\KwOut{Set of detected conflicts $C$}

$C \gets \emptyset$\;
\tcp{Layer 1: Static Detection}
\ForEach{config file $f \in P$}{
    $constraints \gets \textsc{ParseConstraints}(f)$\;
    $C \gets C \cup \textsc{CheckPatterns}(constraints)$\;
}
\If{$C = \emptyset$}{
    \tcp{Layer 2: Dynamic Detection}
    $result \gets \textsc{PipResolve}(P, \text{dry-run})$\;
    \If{result.failed}{
        $C \gets \textsc{ParseError}(result)$\;
    }
}
\Return{$C$}
\end{algorithm}
```

### Algorithm Style Guidelines
- Use `\KwIn`, `\KwOut` for inputs/outputs
- Use `\tcp{}` for inline comments
- Use `\textsc{}` for function names
- Keep algorithms concise (15-25 lines max)
- Always reference: "Algorithm~\ref{alg:name} shows..."

## Highlighting Novel Contributions

After writing all components, **reorganize to highlight novelty**:

### 1. Identify Core Novel Contribution
What component(s) represent genuine novelty over prior work?

### 2. Create Standalone Subsection

```latex
\subsection{Iterative Validation Loop}
\label{sec:validation-loop}

% Design motivation - connect to prior work limitations
Prior LLM-based repair tools suffer from a fundamental limitation: they
treat validation as a binary gate, discarding repairs that fail initial
validation even when the defect is minor and correctable.

% Key insight
The key insight enabling our approach is that validation failures provide
structured feedback identifying specific defects. A hallucinated package
version, a violated constraint, or a transitive conflict each produces
diagnostic output that can guide targeted correction.

% Implementation details
We implement a closed-loop architecture where validation errors drive
iterative repair refinement...

% Why it works
This iterative architecture achieves higher repair success rates by
giving the agent multiple opportunities to correct defects.
```

### 3. Connect Back to Introduction
Ensure the novel subsection addresses challenges from the Introduction.

## Length Guidelines

- **Problem formalization**: 0.25-0.5 pages
- **Approach overview**: 0.5 pages (with figure)
- **Component details**: 1.5-2 pages total
- **Total**: 3-5 pages typical 4-4.5

## Common Mistakes

### 1. Too Simple
**Bad**: "We query GPT-4 and parse the output."
**Good**: Explain the architecture, prompting strategy, validation loop.

### 2. No Design Rationale
Don't just describe WHAT—explain WHY each design decision was made.

### 3. Missing Running Example
Walk through the motivating example from Section 2 with your approach.

### 4. No Novelty Articulation
Explicitly state what's novel compared to prior work.

## Implementation (appended to Methodology or standalone short section)

The Implementation section is brief (1-2 paragraphs, 0.5 pages max). It tells the reader what they need to reproduce the work, not how the code is structured internally.

Cover only:
- Programming language and version (e.g., Python 3.10+)
- Key libraries/frameworks used (e.g., `ast` module, OpenAI API)
- Foundation model and configuration (model name, temperature, context window)
- Environment constraints if any (e.g., Docker, specific OS)
- Lines of code (rough order of magnitude)
- Availability (replication package, Zenodo, anonymous repo)

Do NOT:
- Describe internal module structure in detail (that belongs in methodology)
- List every file and its LOC
- Repeat methodology content (e.g., re-describing the three phases)

```latex
\section{Implementation}
\label{sec:implementation}

We implement \tool{} in approximately 3,200 lines of Python. The site
discovery module uses Python's built-in \texttt{ast} module for parsing
and data flow analysis. Code transformation queries OpenAI's GPT-5.2
(\texttt{gpt-5.2-2026-01}) at temperature 0 with JSON-formatted output.
The knowledge base covers 134 library pairs with 2,847 API mappings,
serialized as JSON and loaded at runtime. Constraint enforcement operates
entirely on AST transformations without additional LLM queries.
The average cost per migration is \$0.08 (2.3 LLM calls, 4.2s median
latency). The complete source code, knowledge base, and evaluation
scripts will be available on Zenodo upon publication.
```

## Checklist

- [ ] Begins with problem formalization (input/output/goal, with formal notation if the problem is naturally structured as optimization/constraint/graph)
- [ ] Approach overview with architecture figure
- [ ] Written as flowing prose (no bullet lists)
- [ ] Each component has technical depth
- [ ] Design decisions are justified (WHY, not just WHAT)
- [ ] Running example walkthrough included
- [ ] Novel contribution has dedicated subsection
- [ ] Algorithms formatted professionally (if used)
- [ ] Minimal formatting (not over-bold/italic)
- [ ] Length is 3-5 pages

[← Background](02-background.md) | [Next: Evaluation →](04-evaluation.md)
