---
name: handling-major-revision
description: Use when running a major-revision cycle for a top-tier SE conference (OOPSLA/ISSTA/ICSE/FSE/ASE), where deliverables include a revised paper PDF with blue \revision{...} highlights, a response-to-reviewers document quoting each comment, follow-up empirical work to address methodology challenges, and an updated anonymized artifact repository. Covers response-doc structure, paper-edit discipline, empirical PoC-validation patterns for security claims, and Docker-based artifact reproduction.
version: 1.0.0
author: SE Research Skills
license: MIT
tags: [Major Revision, Rebuttal, Empirical SE, Artifact Evaluation, Security Validation, PoC]
---

# Handling Major Revision

Use this skill for a **full major-revision cycle** — not a one-page rebuttal. A major revision typically requires (a) a revised paper PDF with visible blue highlights, (b) a response-to-reviewers document quoting each reviewer comment, (c) follow-up empirical work to answer specific methodology challenges, and (d) an updated anonymized artifact repository. For single-shot rebuttals to first-round reviews use the sibling skill `paper-rebuttal` in `16-rebuttal/`.

## When to use vs alternatives

| Situation | Use |
|---|---|
| First-round response to reviewers (no revised PDF) | `16-rebuttal/SKILL.md` |
| Full major revision: revised PDF + response doc + new experiments | **this skill** |
| Camera-ready edits after accept | a `camera-ready` skill (not in this library) |
| Artifact Evaluation submission | separate AE-track instructions from the venue |

## Workflow

A major revision has four parallel tracks that must stay synchronized:

```
┌───────────────────────────────────────────────────────────────┐
│ 1. Review triage  →  2. Response doc  →  3. Paper edits      │
│                      ↓                     ↓                  │
│                   4. Empirical follow-ups  ↓                  │
│                                            ↓                  │
│                                       5. Artifact updates    │
└───────────────────────────────────────────────────────────────┘
```

### 1. Triage the reviews (≈30 min)

Make a flat list of every actionable comment. Group by:
- **Concedeable** — reviewer is right; narrow the claim, drop the comparison.
- **Clarification** — wording/definition fix; usually one paragraph in the paper.
- **Empirical follow-up** — needs new experiment, new sample, or new validation.
- **Out-of-scope** — politely decline with one sentence of justification.

For each comment also note: which reviewer (A/B/C/Meta), explicit Q1/Q2 numbering if present, and which paper section it touches.

### 2. Draft the response document (≈1 day)

Order items as the reviewer wrote them — do not re-sort to a "more logical" order. **The exact macro names vary per paper/venue** — pick a style that matches what the venue accepts and the prior submissions of the project use.

**Starter template**: [`templates/major_response_template.tex`](templates/major_response_template.tex) — a clean, anonymized scaffold distilled from a real OOPSLA major-response document. Copy it as `response/major_response.tex`, search-and-replace the `<TODO ...>` and `<TOOL_NAME>` placeholders, and add `\pointRaised + \reply + \revised + shadedquotation` blocks for each reviewer comment.

Two real macro families we have used:

**Style A — OOPSLA-style (used in `Oopsla_2026_New_Remediation_____Lyuye/revision/response/major_response.tex`)**

```latex
\newcommand{\pointRaised}[2]{\smallskip
{{\fontseries{b}\selectfont #1}: \textbf{#2}}\newline}
\newcommand{\reply}[1]{\textbf{{Response}}:\ {#1} \smallskip }
\newcommand{\revised}[1]{{\color{blue}#1}}
\newcommand{\responsed}[1]{{\color{black}#1}}

\colorlet{shadecolor}{LavenderBlush2}
\newenvironment{shadedquotation}{\begin{shaded*}\quoting[leftmargin=0pt,vskip=0pt]}{\endquoting\end{shaded*}}

\title{Response to Reviewers' Comments\\[0.3em]
\large <Paper title>}
\begin{document}\maketitle
\textit{We sincerely thank the reviewers ...}
\tableofcontents

% Top-of-doc red-tint "how to read" box (NOT a yellow box; venue convention varies)
\mybox[red!8]{
  {\Large\textcolor{red!70!black}{\textbf{How to read this rebuttal}}}
  \begin{quote}\pointRaised{Reviewer-A}{Question from Reviewer A}\end{quote}
  \begin{quote}\reply{\responsed{Response.}}\end{quote}
  \begin{quote}\revised{In Section~x, we added:}
    \begin{shadedquotation}\responsed{Revised manuscript text.}\end{shadedquotation}
  \end{quote}
}

\section{Response to Meta-Review}\label{sec:meta}
\phantomsection\label{resp:meta-r1}
\pointRaised{Meta-R1}{<Quote the meta-review item verbatim>}
\reply{\responsed{<Your response, 2–4 sentences. Acknowledge → answer → name the section that changes.>}}
\revised{In Section~2.2, we added:}
\begin{shadedquotation}
<Verbatim new prose from the paper, including any added table.>
\end{shadedquotation}
```

**Style B — ISSTA-style (used in another revision in this project family)**

```latex
\section{Reviewer A}
\subsection*{Q1: <reviewer question>}
\revcomment{<full reviewer paragraph, never truncated>}
\ourresponse{<direct answer>}
\paperquote{<new prose from the paper, in \revision{} markup>}
```

Either macro family works — pick whichever the paper template already has, or copy one from a prior submission in the same project. **Do not invent new macros mid-revision**; reviewers tolerate any consistent style but flag inconsistency.

**Rules (apply to either style):**
- **Quote reviewers verbatim** — never truncate; the surrounding framing shows the reviewer you understood their point.
- **Preserve reviewer order** within each reviewer section.
- **Merge by topic, not by co-location.** A "Soundness preamble" + a later detailed item that asks the same question should be one merged entry with both reviewer-comment quotes and one consolidated response.
- **Each promised change is immediately followed by its `\shadedquotation` / `\paperquote`** showing the new paper prose. Don't write "list of changes ... then list of paperquotes" — reviewer shouldn't scroll between them.
- **Anchor every reproduced finding with provenance:** `(Finding N, RQX, Section Y.Z)`.
- **`\phantomsection \label{resp:meta-rN}` (or equivalent) before each item** for `\hyperref` linking from the top "how to read" box.
- **Top-of-doc "how to read" callout box** (red-tint for OOPSLA conventions, yellow for ISSTA — match the venue's expectation) summarising how each meta-review item was addressed with `\hyperref` anchors. Reviewers triage in 30 seconds.
- **Simple TOC** (Meta + each reviewer). Don't over-engineer with sub-entries.
- **Strip ACM boilerplate from the response doc**: `\settopmatter{printacmref=false, printccs=false}`, drop abstract/keywords, `\renewcommand\footnotetextcopyrightpermission[1]{}`. The response is not a publication.

### 3. Apply paper edits with visible discipline

The blue `\revision{...}` markup is the reviewer's signal that the paper actually changed. Treat it as a UX surface, not a tracking diff.

**Rules:**
- **A `\revision{}` must wrap a sentence or paragraph**, not a three-word qualifier. If the change is real, the blue should be obvious in the PDF.
- **Rewrite, don't append.** Major-revision page pressure is real. Condense existing related-work or evaluation paragraphs first; the diff should read "old text removed, new text added" at roughly equal size.
- **Wrap large contiguous chunks** rather than scattered word-level fragments. Scattered fragments read as cosmetic; one big blue block reads as "this region was rewritten."
- **Two locations, not three.** When defending one point, anchor it in at most two places (e.g., Intro + Tool section). Three or more reads as defensive.
- **Change the conclusion, not the qualifier.** When a reviewer says "X isn't supported by Y", drop the claim — don't hedge it. Wrapping a sentence in `\revision{in our dataset}` does not visibly change the paper and does not address the substance.
- **Don't claim priority.** "No prior work has done X" reads as offensive even when true. Drop the comparison; let the finding stand on its own.
- **Strict scope on Threats-to-Validity additions.** Strengthen only the threat the reviewer asked about. Volunteering more invites new attacks.

**LaTeX gotchas (acmart):**
- `\revision{}` around `\begin{figure}...\end{figure}` does NOT colour the `\caption{...}`. Wrap captions explicitly: `\caption{\revision{...}}`.
- TikZ inside `\revision{}` does NOT inherit the color. Replace `color=gray`/`color=black` inside tikz styles with `color=revisionblue`.
- `\paperquote{}` / `\shadedquotation` built on a breakable tcolorbox must use `coltext=revisionblue`; a bare `{\color{...}#1}` group drops on page breaks.
- acmart blocks `\section` redefinition and titlesec. If section/subsection sizes are too close, use wrapper macros (`\bigsection`, `\bigsubsection`) instead of patching the class.
- Rebuild after every non-trivial edit; watch page count as a layout signal (a sudden jump = float reflow or tcolorbox overrun).

#### Diff-PDF generation (the "blue highlights" PDF the venue expects)

For OOPSLA-style submissions where the venue asks for both the revised PDF and a *diff* PDF showing changes, use `latexdiff` with a custom post-processor for tables. A working pipeline is checked in at [`Oopsla_2026_New_Remediation_____Lyuye/revision/generate_diff.sh`](Oopsla_2026_New_Remediation_____Lyuye/revision/generate_diff.sh); the essential steps:

```bash
#!/bin/bash
# Layout: <project>/                  ← contains the original oopsla2026.tex (last submission)
#         <project>/revision/         ← contains the revised oopsla2026.tex + this script
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ORIGINAL_DIR="$(dirname "$SCRIPT_DIR")"

# Step 1 — flatten \input{tex/content} in both versions (latexdiff doesn't follow \input)
flatten() {
  if command -v latexpand &>/dev/null; then
    (cd "$(dirname "$1")" && latexpand "$(basename "$1")" -o "$2")
  else
    # sed fallback when latexpand is not installed
    sed '/\\input{tex\/content}/r '"$(dirname "$1")/tex/content.tex" "$1" | \
      sed '/\\input{tex\/content}/d' > "$2"
  fi
}
flatten "$ORIGINAL_DIR/oopsla2026.tex" "$SCRIPT_DIR/original_flat.tex"
flatten "$SCRIPT_DIR/oopsla2026.tex"   "$SCRIPT_DIR/revised_flat.tex"

# Step 2 — latexdiff with safe defaults for tables and listings
latexdiff \
  --type=CFONT \
  --math-markup=0 \
  --config="PICTUREENV=(?:picture|DIFnomarkup|table|table\*|tabular|tabular\*|lstlisting|algorithm)" \
  "$SCRIPT_DIR/original_flat.tex" "$SCRIPT_DIR/revised_flat.tex" > "$SCRIPT_DIR/diff.tex"

# Step 3 — Python post-process: latexdiff mangles \\ and & in tabular rows,
# so it leaves new tables / new rows uncoloured. Manually wrap them in \textcolor{blue}{...}.
# See the full Python block in generate_diff.sh — keywords:
#   - new_table_keywords = ['Motivating Example', 'Sensitivity']   ← lookahead in \begin{table}
#   - 'Self-made baselines' marks the start of new ablation rows in a changed table
#   - blue_cells() splits on & and wraps each cell, preserving \\ and \hline
#   - blue_multicolumn() prepends \color{blue} (since \multicolumn breaks normal wrapping)
#   - post-fix: }\tool\DIFadd{ → }\DIFadd{\tool   (latexdiff splits around \tool macro)

# Step 4 — compile twice (bibtex in between) so cross-refs settle
cd "$SCRIPT_DIR"
pdflatex -interaction=nonstopmode diff.tex || true
bibtex diff || true
pdflatex -interaction=nonstopmode diff.tex || true
pdflatex -interaction=nonstopmode diff.tex || true
rm -f original_flat.tex revised_flat.tex
```

**Why the Python post-processing is needed.** `latexdiff` cannot reliably colour:
- whole new tables (the `\begin{table}...\end{table}` is added but row contents stay default-coloured),
- new rows in a changed table (the row is added but `&`-split cells lose the colour),
- text that includes user macros like `\tool` (latexdiff splits `\DIFadd{}` around the macro call).

The post-processor in `generate_diff.sh` handles these cases by name-matching on table captions and row-marker keywords specific to *this* paper. **Adapt those keyword lists per paper** — they encode which tables are entirely new vs only-rows-added.

**Sanity checks after compiling `diff.pdf`:**
- Every reviewer-promised change visible as blue text in the PDF.
- No accidentally-blue regions that didn't change (usually a macro-collision artefact — adjust the `--config=PICTUREENV` regex).
- Page count of `diff.pdf` ≈ page count of revised `oopsla2026.pdf`. A jump indicates a float reflow.
- Bibliography compiled (`bibtex diff` ran without error).

### 4. Empirical follow-ups (the hardest track)

When a reviewer challenges a methodology claim ("did you really measure X?", "is your sample representative?", "does your patch actually fix the vuln?"), the strongest response is a new mini-study — not more prose.

#### Pattern A — PoC-based security-correctness validation

When the reviewer says *"build/test success does not prove the vulnerability is fixed,"* the response is a PoC sub-study:

1. **Sample a stratified subset** of the ported/remediated CVEs (typical: 30–50 spanning Type I/II/III+ porting difficulty).
2. **For each CVE, run the same 4-step protocol:**
   - Acquire the **vulnerable** dependency JAR.
   - Apply the patched source (or download the upstream-fixed JAR as stand-in).
   - Replay a public PoC against the vulnerable JAR — confirm `EXPLOIT_REACHED` / `DESERIALIZED` outcome.
   - Replay the same PoC against the patched JAR — confirm `BLOCKED` outcome.
3. **Discriminate by message, not exception class.** Many libraries throw the same exception class for "blocked" and "couldn't load gadget"; the *message* is what carries the signal (e.g., jackson `"prevented for security reasons"` vs `"no such class found"`).
4. **Anchor a few cases against real gadget JARs**, even if most use stub classes (most Java deserialization gadget libraries are no longer maintained on Maven Central). Real-gadget anchors prove the methodology generalizes; stubs prove the validator's name-based block works.

#### Pattern B — PoC provenance categorization

Reviewers will challenge synthesised PoCs. Categorize honestly:

| Source | What it is | Defensible because |
|---|---|---|
| **Public exploit repo** | Third-party security-researcher repo on GitHub (`Al1ex/CVE-XXXX-YYYY`, `jas502n/...`) catalogued in `trickest/CVE` or `nomi-sec/PoC-in-GitHub` | Independently authored, publicly dated, reviewer can verify URL |
| **Upstream test** | Test case bundled in the security-fix commit itself | Authoritative — the maintainer who wrote the fix wrote the test |
| **Curated from advisory** | Payload constructed by reading the advisory's attack-vector description and instantiating the library's documented exploit template with the gadget FQN taken verbatim from the patch diff | Reconstruction from authoritative documentation, not invention |

**Sweep platforms in this order** when looking for public PoCs: Exploit-DB → GitHub Security Advisories (GHSA) → NIST NVD reference links → Snyk Vulnerability DB → OSV → Vulhub → `trickest/CVE` → `nomi-sec/PoC-in-GitHub`. The last two are curated indexes that catalog hundreds of named third-party PoC repos.

#### Pattern C — Defending small empirical samples

When the reviewer asks "why only N validations out of 1,000+?" use the **scarcity-bound argument**:

> "The N is bounded by *public-PoC availability* in our research setting, not by the validation methodology. The harness pattern is library-agnostic and O(1) per CVE once an exploit witness exists; operational defenders with vendor advisories or commercial frameworks (Metasploit, Burp) can scale this further. Only public-PoC scarcity (~31% industry-wide, lower for Java library CVEs) constrains the academic sample."

### 5. Update the anonymized artifact (during revision, before camera-ready)

Most SIGPLAN venues allow updating the supplementary artifact repo during the revision/rebuttal window — the PDF is frozen, the URL is not. Use this to add the PoC sub-study, new experiments, or expanded data.

**Anonymization checklist before pushing:**
- Strip `/Users/<name>` paths from scripts; use relative paths.
- Grep for institution names, ORCID, email addresses, OneDrive personal URLs.
- Exclude `target/`, `classes/`, build logs (often contain host paths and timestamps).
- Exclude `.DS_Store`, `.idea/`, IDE config.
- Don't change `git config` user.name/email (commits show author); use a pre-existing anonymous account for pushes.
- Don't push to a repo whose URL contains the author's name.

**Docker-based reproduction recipe** (single `docker run` for reviewers):

```dockerfile
FROM eclipse-temurin:17-jdk
RUN apt-get update && apt-get install -y maven curl
# Add second JDK if needed (e.g., older lib builds need JDK 8):
RUN curl -sLf -o /tmp/z.tar.gz "https://cdn.azul.com/zulu/bin/<version>-linux_$(dpkg --print-architecture | sed 's/amd64/x64/').tar.gz" \
    && tar xzf /tmp/z.tar.gz -C /opt && mv /opt/zulu* /opt/zulu-jdk8
ENV JAVA8_HOME=/opt/zulu-jdk8
WORKDIR /artifact
COPY harnesses/ ./harnesses/
RUN for h in harnesses/*/; do (cd "$h" && mvn -q clean package -DskipTests); done
COPY deps/ payloads/ scripts/ ./
ENTRYPOINT ["scripts/run_audit.sh"]
```

The entrypoint script should print `Final: N pass, M fail` so a reviewer can see the result in 30 seconds. Multi-arch matters: `docker buildx build --platform linux/amd64,linux/arm64 ...` so reviewers on both Intel CI and Apple Silicon laptops succeed without fiddling.

## Statistical framing for empirical claims

- **"Full-population observational" beats "we didn't run hypothesis tests."** When the data covers the entire population in scope rather than a sample drawn from a larger one, frequentist p-values lose their sampling-distribution interpretation. Report descriptively and defer cross-population generalization to future work.
- **Prefer "conservative lower bound" over "complete."** A bounded claim survives reviewer scrutiny; an absolute claim attracts counterexamples.
- **Prefer "dataset-specific" over "generalizable"** unless strong cross-dataset evidence exists.

## Citation hygiene during revision

- **Verify every new bib entry against Crossref / DBLP / publisher page** before adding. Authors, title, venue, year, pages, DOI. Never invent metadata.
- **Cite named tools/libraries in motivating examples.** If you mention `tokio-tar`, cite it (as `@misc` GitHub if no formal pub) and add a one-line gloss in the paragraph.
- **Don't claim "much higher than prior work"** if prior work didn't measure the comparable quantity. Either drop the comparison or anchor it on a specific number from a specific paper.

## Style preferences

- No em-dashes; en-dashes only for ranges.
- No AI-flavour openers ("It is worth noting," "Importantly," "We thank the reviewer for…"). The thank-you belongs in the response doc once at the top of each reviewer section, not inside each item.
- No structured "Finding./Impact./Summary." micro-labels appended to bullets.
- Paper prose must not sound like a response to reviewer feedback. Phrases like "as noted by reviewers" or "we acknowledge that" belong in the response doc, not the paper.
- No mid-sentence line wraps in source — one long line per paragraph in both paper and response. Easier to diff.
- Short paragraphs over long ones. Remove throat-clearing.

## Common pitfalls

| Failure mode | How to avoid |
|---|---|
| Answering a nearby question instead of the exact one | Quote the reviewer comment verbatim in `\revcomment{}` and re-read it after drafting the response |
| Hedging instead of conceding | If the reviewer is right, drop the claim — don't wrap it in a qualifier |
| Inflating empirical effort | Count categories honestly (X reused + Y upstream + Z curated = total). If the math doesn't add up, fix it before submitting |
| Overclaiming PoC sourcing | Specify exactly what was verified vs assumed. "14 GitHub PoC URLs verified" beats "~30 PoCs from various sources" |
| Stale numbers in supporting docs | After a count changes (e.g., 28 → 50 CVEs), grep every supporting doc/README/appendix for the old number |
| Anonymity leak via push history | Use a pre-existing anonymous git account; check `git log --pretty=format:%ae` before pushing |
| Type-distribution skew without justification | If your sample is heavier in one porting/difficulty class, explain the structural reason (patch-corpus composition, validation-cost asymmetry, PoC density) — don't hide it |
| Promising experiments you can't run | Don't write "we will additionally evaluate X in the camera-ready" unless X is genuinely feasible. Reviewers remember these promises |
| Word-budget overrun | If the venue caps the rebuttal at N words, trim the longest section first; compress example lists; defer details to the appendix |

## Word-budget compression tactics

When a 1500-word rebuttal must fit a 700-word limit:

1. **Drop bullet lists of redundant signals** (e.g., 6 per-CVE exception-message excerpts → one representative + "Full per-CVE evidence in `pocs/`").
2. **Collapse 3-source provenance to 2** when one source is small (e.g., merge upstream-tests into public-PoC count).
3. **Replace "we will X, Y, Z" with "we will X" — drop Y and Z if they're obvious or in the appendix.**
4. **Cut "we appreciate this careful reading" and similar throat-clearing** — once at the top of each reviewer section is enough.
5. **Use parenthetical math when the count is contested** (e.g., "(22 + 28 = 50)") — preempts a reviewer asking "the numbers don't add up."

## Reproducibility checklist before final push

- [ ] All cited CVE numbers in rebuttal text exist in `results.csv` and have matching payload files.
- [ ] Audit script runs `N pass, 0 fail` from a fresh clone of the artifact.
- [ ] Docker build succeeds on both `linux/amd64` and `linux/arm64`.
- [ ] No `/Users/<name>`, no `git config` author leak, no institutional URL.
- [ ] Response doc compiles; `\paperquote` excerpts match the paper PDF exactly.
- [ ] Paper PDF page count fits the venue limit; no overfull hboxes in revised regions.
- [ ] Bib entries verified against Crossref / DBLP for every new citation.
- [ ] Word counts within venue limits for both rebuttal text and response doc.
