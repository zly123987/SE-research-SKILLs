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

### Do Not Use `\paragraph{...}` (HARD RULE)

**Do not use the `\paragraph{...}` LaTeX heading anywhere in the body of the paper.** This rule is non-negotiable: every paragraph that uses `\paragraph{...}` opens with the heading itself, and reviewers read that as a sub-thread *within* a thought rather than the start of a new one — a tell of disorganised drafting and a chronic source of "the section is just a list of micro-headings" criticism. Use inline bold lead-ins (`\noindent\textbf{Heading.}`) followed by flowing prose instead, or write the prose without a lead-in label at all.

**Bad** (uses `\paragraph` to chunk content):
```latex
\paragraph{Setup.}
We run the detector on 25 confirmed cases and 25 informative
secure siblings...

\paragraph{Results.}
The detector achieves F1 = 0.83 ...
```

**Good** (inline bold lead-ins, paragraphs flow as normal prose):
```latex
\noindent\textbf{Setup.}
We run the detector on 25 confirmed cases and 25 informative
secure siblings...

\noindent\textbf{Results.}
The detector achieves F1 = 0.83 ...
```

**Better** (no lead-in label at all; the paragraph itself signals the topic):
```latex
We evaluate the detector on a curated benchmark of 25 confirmed cases
and 25 informative secure siblings, and report precision, recall, and
F1 against six baseline tools. The detector achieves F1 = 0.83 ...
```

**How to fix violations.** Mechanical: replace every `\paragraph{X}` with `\noindent\textbf{X}` on the same source line; the next source line (without a blank line between) will attach as the same paragraph and render as bold-heading-followed-by-prose. This preserves the existing structure and visual rhythm while satisfying the rule. The deeper fix — collapsing micro-headings into prose — is preferred when the section reads like an itemised list.

This applies to all sections of the paper: methodology, evaluation, discussion, related work, threats to validity. It also applies to `\subparagraph{}`. The only acceptable place for `\paragraph` in a final manuscript is inside a definition/theorem block where some publishers require it — and even there, prefer inline `\textbf{}` if the venue allows.

**Detection script** (run before submission):
```bash
grep -n '^\\paragraph{' main.tex && echo "VIOLATION: convert each line above to \\noindent\\textbf{}"
```
A clean paper produces no output from this command.

### Use `\noindent\textbf{...}` Lead-Ins Sparingly

Inline bold lead-ins (`\noindent\textbf{Heading.}`) are an acceptable substitute for `\paragraph{...}` headings, but they are not free. A section that opens every paragraph with a bold label still reads as a list of micro-headings — only the typesetting changed. Apply the same restraint as with `\paragraph{...}`: prefer flowing prose where the topic is signalled by the topic sentence itself.

**Heuristic for keeping vs. collapsing:**
- **Keep** the lead-in only when (a) the paragraph genuinely defines a *named* concept that is referenced elsewhere ("**Internal validity.** ..."), (b) the section is a true enumeration with parallel structure (e.g., **For library maintainers.** / **For ecosystem tooling.** / **For the security research community.**), or (c) the bold label serves as a re-finding handle a reviewer would page-flip back to.
- **Collapse** otherwise. A "Setup." or "Method." or "Results." label inside an evaluation subsection rarely earns its keep — the topic is obvious from context and a topic sentence does the same work without typographic noise.

**Bad** (every paragraph has a redundant bold lead-in):
```latex
\noindent\textbf{Setup.}
We run the detector on 50 benchmark cases...

\noindent\textbf{Results.}
The detector achieves F1 = 0.83 ...

\noindent\textbf{Per-domain analysis.}
The detector performs uniformly across...
```

**Good** (topic emerges from prose; one lead-in earns its keep as a signpost):
```latex
We run the detector on the 50-case benchmark and report
precision, recall, and F1 against six baselines. The detector
achieves F1 = 0.83 on confirmed cases (P = 0.87, R = 0.80) and
performs uniformly across the five composition rules: ...

\noindent\textbf{Ablation.}
Removing the symbolic leg drops F1 to 0.62; removing the neural
leg drops it to 0.00 ...
```

**Pre-submission check:** count `\noindent\textbf{` occurrences. As a soft rule, more than ~10 in a body section, or more than ~25 across the whole paper, suggests the section reads as a list rather than an argument; collapse the weakest ones.

---

## AI-Flavor Reduction (HARD RULE)

LLM-generated prose has a distinctive register that experienced reviewers pattern-match instantly: vague intensifiers, metaphorical verbs used in technical contexts, hedging phrases that add no information, and a rhythm of three-item lists for emphasis. Modern PCs increasingly flag this register and discount the work — even when the underlying research is sound. Aggressively scrub for it before submission.

### The AI-Tell Wordlist

Any one of these in isolation is fine; clusters of them (3+ per paragraph) signal an LLM origin. Replace with concrete, plain alternatives.

**Vague intensifiers / hedges** (delete or replace):
| AI tell | Why it's wrong | Plain replacement |
|---------|---------------|-------------------|
| Notably / Notably, | empty emphasis | delete, or replace with the specific reason |
| Importantly / Crucially / Remarkably / Significantly (as opener) | author telling reader what to think | delete |
| It is worth noting that / It should be noted that | filler | delete; just state the fact |
| Comprehensive / Comprehensively | unfalsifiable claim | "complete," "covers all X," or specify scope |
| Robust / Robustly | vague | "tolerant of X," "stable under Y," or specify |
| Sophisticated / Advanced | marketing | name the actual technique |
| Cutting-edge / State-of-the-art (used loosely) | hype | name the specific baseline beaten |
| Seamless / Seamlessly | marketing | "without manual intervention" or specify |
| Holistic | vague | name the components |

**Metaphorical verbs in technical prose** (replace with concrete verbs):
| AI tell | Plain replacement |
|---------|-------------------|
| Leverage | use |
| Facilitate | allow / enable / cause |
| Delve into / Dive into | study / examine / analyse |
| Navigate (a problem) | solve / address / handle |
| Unlock / Unlocks | enable / makes possible |
| Showcase | show / demonstrate |
| Underscore | emphasise / show |
| Bolster | strengthen |
| Foster | encourage / produce |
| Streamline | simplify |

**AI-favourite framings** (rewrite the sentence):
| AI tell | Why | Fix |
|---------|-----|-----|
| In the realm of X / In the world of X | filler | "In X," or delete |
| The tapestry / landscape / fabric of | metaphor abuse | name the thing |
| At the heart of / At its core | filler | delete |
| In recent years (as opener) | generic | name the specific recent thing |
| In conclusion / To summarize / In summary | unnecessary in research papers (the reader knows it's the conclusion) | delete the phrase, keep the sentence |
| Fundamentally / Intrinsically | quasi-philosophical | "by construction," "by definition," or delete |
| The essence of X is | vague | state X directly |
| Pave the way for | filler | "enable" |
| A new paradigm / A paradigm shift | overclaim | describe the actual change |

**Sentence-level tells:**
- **Three-item lists for rhythm**: "fast, accurate, and reliable" — pick the one that's actually new and drop the other two.
- **Em-dashes used as catch-alls**: AI-text uses em-dashes (—) liberally. In formal academic writing, prefer parentheses, commas, or two clauses joined by "and"/"because"/"so."
- **Sentences that end with "and beyond" / "and more"**: vague gesture; either name the additional items or stop.
- **Generic openings** ("This work presents...", "In this paper, we...") — the abstract already said this; jump straight to the substantive claim.

### Formality vs. Casual

Top-tier SE/security venues expect formal register. Common casual constructions to replace:

| Casual | Formal |
|--------|--------|
| Let's | "We" or "Consider" |
| Don't / Won't / Can't (in body prose) | spell out: do not / will not / cannot |
| A lot of / Lots of | many / numerous / a substantial fraction of |
| Pretty (much) / Quite | qualify precisely or delete |
| Stuff / Things | name the actual entities |
| Get / Got (as main verb) | obtain, receive, become, achieve |
| Pretty good / Decent | report the metric |
| Big / Huge | "large" with a number; or "substantial" |
| Easy / Hard (without measure) | "with low/high overhead," "in O(n^2) time," or specify the difficulty |
| Real-world (loosely) | "deployed," "production," or name the artefact |

### Detection Heuristics

**Per-paragraph audit:** Count AI-tells (above) per paragraph. More than 2 in one paragraph → rewrite the paragraph.

**Per-paper audit (run before submission):**
```bash
# Catch the most common AI tells
egrep -n '\b(Notably|Importantly|Crucially|Remarkably|Comprehensive|leverage|facilitate|navigate|delve|seamless|robust|holistic|tapestry|realm|underscore|showcase|paradigm|essence)\b' main.tex \
  | grep -v '%' | head -50
```
Each hit deserves a manual review; most should be replaced.

**Re-read test:** After a rewrite pass, read three paragraphs aloud. If they sound like a marketing brochure or a TED talk, they still have AI flavour. Aim for the register of a focused research engineer explaining a result to a senior colleague: short sentences, specific claims, no flourishes.

---

## Use `\texttt{...}` Sparingly (HARD RULE)

`\texttt{}` (and `\code{}`/`\path{}`) is for code, not for emphasis. Every monospace span tells the reader "this is a literal identifier you must read carefully." When the span isn't actually a literal identifier, the reader pays a comprehension cost for no information gain — and the page acquires a noisy, code-dump appearance that signals undisciplined drafting.

**Use `\texttt{}` only when the literal token matters.**

| Use `\texttt{}` | Don't use `\texttt{}` |
|-----------------|----------------------|
| Function or method signatures the reader must match against the artefact (`\texttt{compose\_and\_test\_rce}`) | Library names already obvious from prose ("the Bottle library" not "the \texttt{bottle} library") |
| Specific API calls referenced in a code listing or formal definition (`\texttt{escape}` in $\bp(\texttt{escape})$) | General library names mentioned in passing |
| Exact configuration values, error codes, file paths, or shell commands | Common compound nouns ("URL-encoding" not "\texttt{URL}-encoding") |
| Symbols whose typographic identity (case, punctuation, special characters) carries semantic meaning | Quoted concepts ("the trust marker" not "\texttt{trust\_marker}") |
| Code-listing fragments (`Markup("hello")`) | Repeated mentions of the same library on every line of a paragraph |

**Specific rules:**
- **Library names**: write naturally on first mention (e.g., "we use Bottle for the demo"); use `\texttt{}` only when the library's literal package identifier matters (`pip install bottle` example, or distinguishing `bottle` the package from the noun "bottle"). Once introduced, repeat references in plain text.
- **Method/API names mentioned in passing**: spell out in prose. *"`escape` then `unquote`"* → "the escape step, then the URL-decode step" — unless we are specifically tracking the call sequence's literal identifiers.
- **CWE/CVE identifiers**: never `\texttt{}` (e.g., write `CWE-79`, not `\texttt{CWE-79}`).
- **Concept names** (HMAC, XSS, JSON, etc.): never `\texttt{}` — they are concepts, not literal tokens.
- **Configuration parameters quoted in prose**: only if the literal name and value matter; otherwise describe ("set HMAC verification to strict mode" not "set \texttt{verify=True}").

**Bad** (acceptable in a code listing, intolerable in flowing prose):
> *We compose `\texttt{markupsafe.escape}` with `\texttt{urllib.parse.unquote}` in a typical `\texttt{Flask}` view, then render the result via `\texttt{render\_template}`. The `\texttt{Markup}` wrapper marks the string trusted...*

**Good** (one literal identifier per pair, prose for the rest):
> *We compose markupsafe's escape function with urllib's URL-decode in a typical Flask view, then render the result via the template engine. The Markup wrapper marks the string trusted...*

**Pre-submission check** (run before submission):
```bash
grep -c '\\texttt{' main.tex
```
A typical 18-page security paper carries 30–80 `\texttt{}` spans. If your count is over 150, the prose is over-monospaced; revisit each occurrence and ask whether the literal token matters or whether prose would carry the meaning.

**Heuristic for borderline cases:** if you can read the sentence aloud and the listener cannot tell whether a span was monospaced or not, the monospace was unnecessary.

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

## Confident Soft-Positioning, Never Apologetic Hedging (HARD RULE)

In academic papers, **never undermine novelty with apologetic hedges, even when trying to sound rigorous.** Reviewers do not reward "honesty" disclaimers like *"we make no claim X is new"* or *"the contribution is not Y"* — they read those as the authors admitting no real contribution exists, which collapses to *"then why publish?"*. There is no path on which a reviewer accepts a paper because the authors voluntarily wrote that they have no novelty.

**Soft tone $\neq$ apologetic tone.** A *soft* claim says "we found something meaningful that others overlooked." An *apologetic* claim says "we did not find the most important thing ever." The first invites the reviewer to agree; the second invites them to reject.

### Banned phrasings

These structures negate a claim without supplying a positive replacement claim. They read as concessions of inadequacy:

- *"We make no claim that..."*
- *"The contribution is not the discovery of..."*
- *"The novelty of the paper is not..."*
- *"We do not claim X is new / novel / the first..."*
- *"Some of these are well-known..."* (as a leading sentence of a contribution-positioning paragraph)
- Any sentence whose grammatical structure is *negation of claim X* without a *positive replacement claim Y*.

### Preferred phrasings

These affirm meaningfulness with confident soft-positioning. They name what the work does, what it identifies, what it deliberately includes, never what it lacks:

- *"Our position is that these compositions form a coherent attack surface that current tooling overlooks..."*
- *"The benchmark deliberately mixes X with Y because [positive reason]..."*
- *"We include both kinds because the empirical finding concerns A rather than B..."*
- *"Together these results identify [structural gap / blind spot / attack surface] that [stakeholders] systematically overlook."*
- *"We retain X deliberately, because [reason that strengthens the case]."*

### Reframing weaker exemplars

If your benchmark contains items some reviewer might call "already known," do not call them "limitations of the benchmark." Reframe them as deliberate design choices that strengthen the structural argument:

- ❌ *"Three of our patterns are already documented in prior literature."*
- ✅ *"Three of our patterns echo single-library pitfalls already discussed in the literature; we include them as documented-but-undetected cases that sharpen the tooling-gap argument: if the standard analyser stack misses even the textbook composition pitfalls, it will also miss the genuinely emergent ones."*

### Where the apologetic temptation is strongest (be vigilant)

- **Abstract closing sentences** — do not end with a hedge; end with a positioning claim.
- **Intro lead-in to contributions** — open with assertive position, not with concession.
- **Discussion subsections that compare to prior work** — don't admit overlap; reframe as deliberate scope choice.
- **Threats-to-validity sections** — state the threat *and* the mitigation, never the threat alone.

### Worked rewrites

**Apologetic (bad):**
> *Our contribution is the formalisation, the detector, and the benchmark that together expose this analysis gap; we make no claim that every individual pattern in the benchmark is newly discovered.*

**Soft-positioning (good):**
> *Together these results identify a coherent attack surface — composition-level assumption gaps between independently-correct libraries — that current security tooling and ecosystem advisories systematically overlook, and provide a formal definition, an automated detector, and a public benchmark for studying it.*

**Apologetic (bad):**
> *The contribution of this paper is not the discovery of new vulnerability primitives but the structural argument that a recurring class of security failures lives at the library-composition boundary.*

**Soft-positioning (good):**
> *Our position is that these compositions are not isolated curiosities but a coherent attack surface that the standard analyser stack overlooks; the paper develops the formal vocabulary, the automated detector, and the empirical evidence to make that case.*

**Apologetic (bad):**
> *The novelty of the paper is not the empirical discovery of every single pair we study.*

**Soft-positioning (good):**
> *The benchmark deliberately mixes patterns that are emergent from composition with patterns whose single-library aspects are already established in the security literature.*

## Checklist

- [ ] Claims are precise with numbers
- [ ] No overclaiming beyond evaluation evidence
- [ ] Methodology written as prose, not bullets
- [ ] SE terminology used correctly
- [ ] Minimal formatting (no excessive bold/italic)
- [ ] Consistent voice (we vs impersonal)
- [ ] Numbers formatted correctly
- [ ] Non-breaking spaces before citations/refs
- [ ] Humble tone in comparisons (humble $\neq$ apologetic)
- [ ] No "we make no claim" / "the contribution is not" hedges
- [ ] Abstract and intro contributions open with positive positioning
- [ ] Documented-but-undetected items framed as evidence-strengthening
- [ ] Limitations acknowledged
- [ ] All tables fit column width — zero overfull hbox from tables
- [ ] No redundant table+figure pairs showing the same data

[Back to Main →](../SKILL.md)
