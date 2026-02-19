# Section 2: Background and Motivation

[← Back to Main](../SKILL.md) | [← Introduction](01-introduction.md)

This section serves two purposes: (1) provide background concepts readers need, and (2) motivate your work with a concrete example.

## Section Naming

Name this section **"Background and Motivation"** or simply **"Background"**. Do NOT call it just "Motivation"—reviewers expect background concepts to be covered.

## Structure

```latex
\section{Background and Motivation}
\label{sec:background}

\subsection{[Domain Topic]}
% Background: explain key concepts readers need

\subsection{Motivating Example}
% Concrete example showing the problem
% What the example reveals briefly; why existing tools fail in short summary to motivate our tool
```

## Subsection 1: Background Concepts

Define key concepts readers need to understand your approach. Be concise—only include what's necessary.

### Example

```latex
\subsection{Python Dependency Management}

Python projects specify dependencies in configuration files such as
\texttt{requirements.txt}, \texttt{setup.py}, and \texttt{pyproject.toml}.
Each dependency can include version constraints using comparison operators:
\texttt{>=}, \texttt{<=}, \texttt{==}, \texttt{\~{}=}, and \texttt{!=}.

When installing a project, pip's dependency resolver attempts to find
versions of all packages that satisfy all constraints simultaneously.
If no such combination exists, pip reports a \textit{resolution conflict}
and aborts installation.

Conflicts can be \textit{direct}---specified in the project's own
configuration files---or \textit{transitive}---arising from constraints
in dependencies' own requirements. Transitive conflicts are particularly
difficult to diagnose because they do not appear in the project's
configuration files.
```

### Tips
- Define only concepts that appear later in your approach
- Use examples to clarify definitions
- Keep it to 0.5-1 page

## Subsection 2: Motivating Example

Show a **concrete, real-world example** that illustrates the problem. This is crucial—reviewers need to see the problem is real.

### Requirements
1. **Real**: Use an actual project, not a synthetic example
2. **Concrete**: Show actual code/configuration, not abstract descriptions
3. **Demonstrates the problem**: The example should clearly show the challenge
4. **Sets up your solution**: The example should hint at what's needed

### Example

```latex
\subsection{Motivating Example}

We illustrate the problem through Vxscan, a popular security scanner
with 2.3K GitHub stars. Vxscan's \texttt{requirements.txt} specifies:

\begin{lstlisting}[style=config]
requests>=2.28.0
urllib3>=1.26.0,<2.0.0
\end{lstlisting}

Attempting to install these dependencies fails with:

\begin{lstlisting}[style=config]
ERROR: Cannot install requests>=2.28.0 and urllib3<2.0.0
because requests 2.28+ requires urllib3>=2.0.0
\end{lstlisting}

This conflict is \textit{implicit}: the constraint \texttt{urllib3>=2.0.0}
does not appear in Vxscan's configuration files but is introduced
transitively through requests 2.28+. Furthermore, this conflict only
emerged when requests updated its urllib3 requirement in version 2.28.0---
Vxscan's configuration was valid when originally written.

Existing tools fail on this case:
\begin{itemize}[leftmargin=*]
    \item \textbf{Static analysis} (PyEGo) cannot detect the conflict
      because the transitive constraint is not in the project's files.
    \item \textbf{Pip alone} detects the conflict but provides no repair
      suggestion.
    \item \textbf{LLM-only approaches} may suggest invalid repairs due to
      lack of version history knowledge.
\end{itemize}
```

### Visual Aid

Consider including a figure showing the conflict structure:

```latex
\begin{figure}[t]
\centering
\begin{tikzpicture}[...]
% Dependency graph visualization
\end{tikzpicture}
\caption{Dependency conflict in Vxscan. The implicit constraint
  \texttt{urllib3>=2.0.0} from \texttt{requests} conflicts with
  the explicit constraint \texttt{urllib3<2.0.0}.}
\label{fig:motivating}
\end{figure}
```

## Length Guidelines

- **Background concepts**: 0.5-1 page
- **Motivating example**: 0.5-1 page (including figures)

- **Total**: 0.5-1 pages

## Common Mistakes

### 1. No Concrete Example
**Bad**: "Dependency conflicts are common in Python projects."
**Good**: Show actual requirements.txt, actual error message, actual project.

### 2. Synthetic Example
**Bad**: Made-up example that's too clean.
**Good**: Real project with real complexity and real failure.

### 3. Background Too Long
Don't write a tutorial. Include only what readers need to understand your approach.

### 5. Example Doesn't Connect to Solution
The motivating example should set up your solution. If your solution addresses challenges A, B, C, the example should demonstrate A, B, C.

## Checklist

- [ ] Section named "Background and Motivation" or "Background"
- [ ] Background concepts are necessary and concise
- [ ] Motivating example is real (not synthetic)
- [ ] Example shows actual code/configuration
- [ ] Existing tools' failures on this example are explained
- [ ] Challenges extracted from example are clear
- [ ] Challenges connect to your solution's components
- [ ] Length is 1-1.5 pages

[← Introduction](01-introduction.md) | [Next: Methodology →](03-methodology.md)