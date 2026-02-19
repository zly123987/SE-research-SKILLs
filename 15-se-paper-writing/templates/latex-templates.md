# LaTeX Templates

[← Back to Main](../SKILL.md)

Templates and setup for SE venues.

## Document Class by Venue

| Venue | Document Class | Options | Layout |
|-------|---------------|---------|--------|
| **ISSTA, FSE, OOPSLA, PLDI** | `acmsmall` | `screen,review,anonymous` | Single-column |
| **CCS, SIGMOD** | `sigconf` | `review,anonymous` | Two-column |
| **ICSE, ASE, MSR** | `IEEEtran` | `conference` | Two-column |

---

## ACM Single-Column (ISSTA, FSE, OOPSLA)

```latex
\documentclass[acmsmall,screen,review,anonymous]{acmart}

% Disable ACM-specific items for submission
\settopmatter{printacmref=false}
\renewcommand\footnotetextcopyrightpermission[1]{}
\pagestyle{plain}

% Packages
\usepackage{booktabs}
\usepackage{algorithm}
\usepackage[ruled,vlined,linesnumbered]{algorithm2e}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{tcolorbox}
\tcbuselibrary{skins}

% Tool macro
\newcommand{\tool}{PyVersionHealer}

\begin{document}

\title{Your Paper Title: A Subtitle If Needed}

\begin{abstract}
Your abstract here (150-250 words).
\end{abstract}

\maketitle

\section{Introduction}
\label{sec:intro}
% Content...

\section{Background and Motivation}
\label{sec:background}
% Content...

\section{Approach}
\label{sec:approach}
% Content...

\section{Evaluation}
\label{sec:evaluation}
% Content...

\section{Discussion}
\label{sec:discussion}
\subsection{Threats to Validity}
% Content...

\section{Related Work}
\label{sec:related}
% Content...

\section{Conclusion}
\label{sec:conclusion}
% Content...

% REQUIRED for ISSTA: Data Availability
\section*{Data Availability}
Our replication package is available at: [URL].

\bibliographystyle{ACM-Reference-Format}
\bibliography{references}

\end{document}
```

---

## IEEE Two-Column (ICSE, ASE, MSR)

```latex
\documentclass[conference]{IEEEtran}

% Packages
\usepackage{booktabs}
\usepackage{algorithm}
\usepackage[ruled,vlined,linesnumbered]{algorithm2e}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{url}
\usepackage{hyperref}

% Tool macro
\newcommand{\tool}{PyVersionHealer}

\begin{document}

\title{Your Paper Title}

\author{\IEEEauthorblockN{Anonymous Author(s)}
\IEEEauthorblockA{Anonymous Institution}}

\maketitle

\begin{abstract}
Your abstract here (150-250 words).
\end{abstract}

\section{Introduction}
\label{sec:intro}
% Content...

\section{Background and Motivation}
\label{sec:background}
% Content...

\section{Approach}
\label{sec:approach}
% Content...

\section{Evaluation}
\label{sec:evaluation}
% Content...

\section{Discussion}
\label{sec:discussion}
\subsection{Threats to Validity}
% Content...

\section{Related Work}
\label{sec:related}
% Content...

\section{Conclusion}
\label{sec:conclusion}
% Content...

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
```

---

## Common Preamble Packages

```latex
% Essential
\usepackage{booktabs}        % Professional tables
\usepackage{graphicx}        % Figures
\usepackage{xcolor}          % Colors

% Algorithms
\usepackage{algorithm}
\usepackage[ruled,vlined,linesnumbered]{algorithm2e}

% Code listings
\usepackage{listings}

% Boxes for "Answering RQ"
\usepackage{tcolorbox}
\tcbuselibrary{skins}

% Diagrams (optional)
\usepackage{tikz}
\usetikzlibrary{shapes,arrows,positioning}

% URLs and hyperlinks
\usepackage{url}
\usepackage{hyperref}
```

---

## Code Listing Style

```latex
% Define colors
\definecolor{codegreen}{rgb}{0.1,0.5,0.1}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.5,0.0,0.5}
\definecolor{codeblue}{rgb}{0.1,0.2,0.6}
\definecolor{backcolor}{rgb}{0.97,0.97,0.97}

% SE style
\lstdefinestyle{sestyle}{
    backgroundcolor=\color{backcolor},
    commentstyle=\color{codegreen}\itshape,
    keywordstyle=\color{codeblue}\bfseries,
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\small,
    breaklines=true,
    numbers=left,
    numbersep=5pt,
    frame=single,
    xleftmargin=1em,
    framexleftmargin=0.5em
}

\lstset{style=sestyle}

% Python style
\lstdefinestyle{python}{
    language=Python,
    morekeywords={self, True, False, None, async, await},
    style=sestyle
}

% Config file style (no syntax highlighting)
\lstdefinestyle{config}{
    basicstyle=\ttfamily\small,
    frame=single,
    backgroundcolor=\color{backcolor},
    xleftmargin=1em,
    framexleftmargin=0.5em
}
```

### Usage

```latex
% Python code
\begin{lstlisting}[style=python,caption={Example code},label={lst:example}]
def detect_conflicts(project: Path) -> list[Conflict]:
    conflicts = static_detect(project)
    if conflicts:
        return conflicts
    return dynamic_detect(project)
\end{lstlisting}

% Config file
\begin{lstlisting}[style=config,caption={Requirements file}]
requests>=2.28.0
urllib3>=1.26.0,<2.0.0
\end{lstlisting}

% Inline code
The \texttt{requirements.txt} file specifies...
```

---

## Algorithm Style

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
    $result \gets \textsc{PipResolve}(P)$\;
    \If{result.failed}{
        $C \gets \textsc{ParseError}(result)$\;
    }
}
\Return{$C$}
\end{algorithm}
```

---

## Table Style

```latex
\begin{table}[t]
\centering
\caption{Detection Effectiveness Comparison}
\label{tab:detection}
\begin{tabular}{@{}lrrr@{}}
\toprule
\textbf{Approach} & \textbf{Detected} & \textbf{Rate} & \textbf{$\Delta$} \\
\midrule
Static-only & 33/50 & 66\% & --- \\
Pip-only & 14/50 & 28\% & $-$38\% \\
PyEGo~\cite{wang2020pyego} & 33/50 & 66\% & --- \\
\midrule
\textbf{\tool{} (Ours)} & \textbf{40/50} & \textbf{80\%} & \textbf{+14\%} \\
\bottomrule
\end{tabular}
\end{table}
```

### Table Guidelines

- Use `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`)
- NEVER use `\hline`
- Use `@{}` to remove outer padding
- Bold best results and your approach
- Caption ABOVE table
- Position with `[t]`

---

## "Answering RQ" Box

```latex
% With tcolorbox
\begin{tcolorbox}[title=Answering RQ1,colback=gray!10,colframe=gray!50]
\tool{} achieves 80\% detection rate, outperforming PyEGo (66\%) by
14 percentage points. The improvement is statistically significant
(Fisher's exact test, $p = 0.032$, Cliff's $\delta = 0.21$).
\end{tcolorbox}

% Without tcolorbox (simple box)
\noindent\fbox{\parbox{\linewidth}{
\textbf{Answering RQ1:} \tool{} achieves 80\% detection rate...
}}
```

---

## Figure Style

```latex
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{figures/architecture.pdf}
\caption{Architecture overview of \tool{}.}
\label{fig:architecture}
\end{figure}
```

### TikZ Architecture Diagram

```latex
\begin{figure}[t]
\centering
\begin{tikzpicture}[
    node distance=1.5cm,
    box/.style={rectangle, draw, minimum width=2.5cm, minimum height=0.8cm},
    arrow/.style={->, thick}
]
\node[box] (input) {Input Project};
\node[box, below of=input] (static) {Static Detection};
\node[box, below of=static] (dynamic) {Dynamic Detection};
\node[box, below of=dynamic] (output) {Conflicts};

\draw[arrow] (input) -- (static);
\draw[arrow] (static) -- node[right] {if $C = \emptyset$} (dynamic);
\draw[arrow] (dynamic) -- (output);
\end{tikzpicture}
\caption{\tool{} Architecture}
\label{fig:arch}
\end{figure}
```

---

## Useful Macros

```latex
% Tool name
\newcommand{\tool}{PyVersionHealer}

% Common formatting
\newcommand{\eg}{e.g.,\xspace}
\newcommand{\ie}{i.e.,\xspace}
\newcommand{\etc}{etc.\xspace}

% RQ references
\newcommand{\rqone}{RQ1\xspace}
\newcommand{\rqtwo}{RQ2\xspace}

% Code inline
\newcommand{\code}[1]{\texttt{#1}}
```

---

## Template Sources

| Format | Source |
|--------|--------|
| ACM | https://www.ctan.org/pkg/acmart |
| IEEE | https://www.ctan.org/pkg/ieeetran |
| ACM GitHub | https://github.com/borisveytsman/acmart |

Always fetch latest templates before submission.

[Back to Main →](../SKILL.md)
