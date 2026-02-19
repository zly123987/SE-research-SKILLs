# Section 6: Related Work

[← Back to Main](../SKILL.md) | [← Discussion](05-discussion.md)

Related work demonstrates you understand the research landscape and positions your contribution clearly.

## Structure

Organize by **approach type** (not chronologically):

```latex
\section{Related Work}


\subsection{Most relevant tools or studies}
% Discuss the most relevant tools especially the baselines
% End with differentiation summary

\subsection{LLM-Based Approaches}
% Discuss as many tools as possible
% End with differentiation summary

\subsection{Traditional Tools}
% Discuss 7-8 tools max if possible
% End with differentiation summary
```

## Per-Work Discussion Requirements

For each related work, provide **substantive discussion** (1 sentence):

1. **What the work does with a brief how and the contribution** (1 sentence)

### Bad (too shallow and short sentences):
```latex
PyEGo~\cite{wang2020pyego} detects Python dependency conflicts using
knowledge graphs. PyCRE~\cite{ye2022pycre} extends PyEGo with SAT solvers.
Our tool differs by using LLMs.
```

### Good (substantive):
```latex
PyEGo~\cite{wang2020pyego} pioneered knowledge graph-based Python
environment inference by constructing a graph of package compatibility
relationships from historical PyPI data, achieving
strong detection of explicit constraint conflicts but cannot identify
semantic conflicts requiring domain knowledge.
```

## Formatting Guidelines

### Do NOT bold tool names:
```latex
% BAD
\textbf{PyEGo}~\cite{wang2020pyego} detects conflicts...

% GOOD
PyEGo~\cite{wang2020pyego} detects conflicts...
```

### Do NOT use "Our differentiation:" labels:
```latex
% BAD
PyEGo achieves strong detection.
\textit{Our differentiation:} \tool{} adds LLM-based detection...

% GOOD
PyEGo achieves strong detection but cannot identify semantic conflicts.
\tool{} subsumes PyEGo's capabilities while adding LLM-based semantic
detection for ecosystem conflicts invisible to structural analysis.
```

## Subsection Summary Requirement

**End each subsection with a positioning statement**:

```latex
\subsection{Knowledge Graph Approaches}

% Discuss PyEGo, PyCRE, ReadPyE...

% END with positioning summary:
While knowledge graph approaches excel at detecting explicit constraint
conflicts through structural analysis, they fundamentally cannot capture
semantic conflicts requiring ecosystem knowledge. \tool{} builds on this
foundation by incorporating runtime validation and LLM reasoning to
address the semantic gap.
```

## Complete Subsection Example

```latex
\subsection{LLM-Based Approaches}

PLLM~\cite{chen2024pllm} applies large language models to Python
dependency fixing using a single-agent architecture with Docker-based
validation. While effective at generating repairs, PLLM queries the LLM
for every project regardless of conflict complexity, incurring high API
costs. \tool{} differs by invoking LLM analysis for only 18\% of cases
through hierarchical detection, reducing costs by 5$\times$ while
achieving higher detection coverage through complementary strategies.

RepairAgent~\cite{bouzenia2024repairagent} and
AutoCodeRover~\cite{zhang2024autocoderover} demonstrate multi-agent
architectures for automated program repair. These tools address code-level
bugs through iterative refinement with execution feedback. \tool{} adapts
the multi-agent paradigm to the dependency management domain, with
specialized components for detection, resolution, and validation that
operate on package constraints rather than source code.

LLM-based SE tools have proliferated for tasks including code
generation~\cite{chen2021codex}, bug detection~\cite{pearce2022examining},
and test generation~\cite{lemieux2023codamosa}. These tools demonstrate
the potential of language models for software engineering automation.
\tool{} contributes by demonstrating effective LLM application to
dependency management, a domain previously dominated by structural
approaches, while using hierarchical design to minimize LLM costs.
```

## What to Include

| Category | Include | Purpose |
|----------|---------|---------|
| **Direct competitors** | Most similar tools/techniques | Show how you differ |
| **Foundation work** | Techniques you build on | Acknowledge intellectual debt |
| **Adjacent domains** | Related but different problems | Show awareness of broader landscape |
| **Baselines** | Tools compared in evaluation | Explain why they were chosen |

## Citation Density

- Related work section: 15-25 citations
- Each subsection: 4-8 citations
- Each individual work: 3-5 sentences of discussion

## Common Mistakes

### 1. Just Listing Papers
**Bad**: "X does A. Y does B. Z does C."
**Good**: Substantive discussion of how each works and how you differ.

### 2. Chronological Organization
**Bad**: "In 2018, X... In 2019, Y... In 2020, Z..."
**Good**: Organized by approach type or theme.

### 3. Missing Recent Work
Reviewers expect coverage of work from the last 2-3 years.

### 4. Differentiation for each work
No need to differentiate every work, but only those very relevant works to highlight the novelty.

### 5. Separate "Positioning" Subsection
If each subsection ends with positioning, don't add a redundant positioning section.

## Length Guidelines

- Total: 0.7-1 page
- Each subsection: 0.2-0.3 pages
- 2-4 subsections typical

## Checklist

- [ ] Organized by approach type (not chronologically)
- [ ] Each work has 1 sentence of substantive discussion (can be long if very necessary)
- [ ] Each subsection ends with positioning summary
- [ ] No bolded tool names
- [ ] No "Our differentiation:" labels
- [ ] Recent work (last 0-5 years) included
- [ ] Baselines from evaluation are discussed
- [ ] Length is 0.7-1 pages
- [ ] 20-40 total citations in this section

[← Discussion](05-discussion.md) | [Next: Conclusion →](07-conclusion.md)
