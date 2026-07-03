---
name: handling-major-revision
description: Use when running a major-revision cycle for a top-tier SE conference (OOPSLA/ISSTA/ICSE/FSE/ASE), where deliverables include a revised paper PDF with blue \revision{...} highlights, a response-to-reviewers document quoting each comment, follow-up empirical work to address methodology challenges, and an updated anonymized artifact repository. Covers response-doc structure, paper-edit discipline, mini-study patterns for empirical follow-ups, and reproducible artifact updates.
version: 1.0.0
author: SE Research Skills
license: MIT
tags: [Major Revision, Rebuttal, Empirical SE, Artifact Evaluation]
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

### 1. Triage the reviews 

Make a flat list of every actionable comment. Group by:
- **Concedeable** — reviewer is right; narrow the claim, drop the comparison.
- **Clarification** — wording/definition fix; usually one paragraph in the paper.
- **Empirical follow-up** — needs new experiment, new sample, or new validation.
- **Out-of-scope** — politely decline with one sentence of justification.

For each comment also note: which reviewer (A/B/C/Meta), explicit Q1/Q2 numbering if present, and which paper section it touches.

### 2. Draft the response document 

Order items as the reviewer wrote them — do not re-sort to a "more logical" order. **The literal macro names vary per paper/venue, but the underlying per-item structure is the same.**

**Per-item structure — four blocks repeated for every reviewer comment.** Whether the item is `Meta-R1`, `Question A-Q1`, or `Comment B3`, it should always carry these four things in this order:

```latex
% 1. ANCHOR — \phantomsection + \label{} for \hyperref cross-references
\phantomsection \label{resp:<reviewer>-<item-id>}

% 2. COMMENT — the reviewer's text, quoted verbatim (never truncate)
\<commentMacro>{<reviewer + item id>}{<full reviewer quote>}

% 3. RESPONSE — your reply, 2–4 sentences: acknowledge → answer → name the section that changes
\<replyMacro>{<your response>}

% 4. PAPER QUOTE — the exact new prose now in the revised paper PDF, with a "where in the paper" lead-in
\<paperEditPointer>{In Section X, we added:}
\begin{<paperQuoteEnv>}
<verbatim new paper text, copied from the revised PDF>
\end{<paperQuoteEnv>}
```

**Naming variants seen in the wild** — pick whichever the paper template (or a prior submission in the same project) already defines:

| Block | Common macro / environment names |
|---|---|
| Comment quote | `\pointRaised{}{}`, `\revcomment{}`, `\rcomment{}`, `\reviewercomment{}` |
| Response | `\reply{}`, `\ourresponse{}`, `\authorreply{}`, `\resp{}` |
| "Where in the paper" pointer | `\revised{...}`, `\edit{...}`, `\paperedit{...}` (often just blue inline text) |
| Paper-quote container | `\paperquote{}` (tcolorbox), `shadedquotation` / `shaded` (framed shaded box), `quote` + blue colour |

Either family works. **Do not invent new macros mid-revision** — reviewers tolerate any consistent style but flag inconsistency.

**Visual conventions (orthogonal to macro names):**
- Reviewer comments in **bold** or with a coloured header (commonly grey or red).
- "Response:" lead-in in bold black.
- New paper prose in **blue text** AND/OR a **shaded background box** (colour varies by venue convention — `LavenderBlush2`, `yellow!10`, `gray!20`, etc.).
- "How to read this rebuttal" callout box at the top of the document showing the four-block pattern visually — reviewers triage in 30 seconds.

**Starter template**: [`templates/major_response_template.tex`](templates/major_response_template.tex) — a complete LaTeX scaffold with one filled-in macro family (`\pointRaised + \reply + \revised + shadedquotation`) and `<TODO>` placeholders for the content. Copy it as `response/major_response.tex` and adapt the macro names if your venue prefers a different family.

**Rules (apply to either style):**
- **Quote reviewers verbatim** — never truncate; the surrounding framing shows the reviewer you understood their point.
- **Preserve reviewer order** within each reviewer section.
- **Merge by topic, not by co-location.** A "Soundness preamble" + a later detailed item that asks the same question should be one merged entry with both reviewer-comment quotes and one consolidated response.
- **Each promised change is immediately followed by its `\shadedquotation` / `\paperquote`** showing the new paper prose. Don't write "list of changes ... then list of paperquotes" — reviewer shouldn't scroll between them.
- **Anchor every reproduced finding with provenance:** `(Finding N, RQX, Section Y.Z)`.
- **`\phantomsection \label{resp:meta-rN}` (or equivalent) before each item** for `\hyperref` linking from the top "how to read" box.
- **Top-of-doc "how to read" callout box** summarising how each meta-review item was addressed with `\hyperref` anchors. Match the visual style of recent accepted responses for the target venue (e.g., authors often use red-tint boxes for OOPSLA and yellow for ISSTA, but there is no official venue specification — check the call-for-papers and look at prior accepted submissions). Reviewers triage in 30 seconds.
- **Simple TOC** (Meta + each reviewer). Don't over-engineer with sub-entries.
- **Strip ACM boilerplate from the response doc when using `acmart`**: `\settopmatter{printacmref=false, printccs=false}`, drop abstract/keywords, `\renewcommand\footnotetextcopyrightpermission[1]{}`. If using the bundled `article` template, this is already handled. The response is not a publication.

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

For OOPSLA-style submissions where the venue asks for both the revised PDF and a *diff* PDF showing changes, use `latexdiff` with a custom post-processor for tables. If the current workspace already has a project-specific `generate_diff.sh`, adapt it; otherwise use the essential pattern below:

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
# Build a small Python script that handles, at minimum:
#   - new_table_keywords = [...]              ← caption keywords that identify ENTIRELY-NEW tables
#   - new_row_markers   = [...]               ← row text that marks where added rows start in changed tables
#   - blue_cells()      splits on & and wraps each cell, preserving \\ and \hline
#   - blue_multicolumn() prepends \color{blue} (since \multicolumn breaks normal wrapping)
#   - macro post-fix: }\<yourMacro>\DIFadd{ → }\DIFadd{\<yourMacro>   (latexdiff splits around user macros)

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
- text that includes user-defined macros (e.g. `\tool`, `\sys`, `\name`); latexdiff splits its `\DIFadd{}` around the macro call.

The post-processor uses caption keywords and row-marker strings that are **specific to each paper's tables** — there is no one-size-fits-all keyword list. Maintain the list inline at the top of the script so the next revision cycle can edit it without reading the regex bodies.

**Sanity checks after compiling `diff.pdf`:**
- Every reviewer-promised change visible as blue text in the PDF.
- No accidentally-blue regions that didn't change (usually a macro-collision artefact — adjust the `--config=PICTUREENV` regex).
- Page count of `diff.pdf` ≈ page count of the revised paper PDF. A jump indicates a float reflow.
- Bibliography compiled (no missing `??` citation markers).

### 4. Empirical follow-ups (the hardest track)

When a reviewer challenges a methodology claim ("did you really measure X?", "is your sample representative?", "is your evaluation metric the right one?"), the strongest response is a **bounded mini-study** — not more prose. Time budget: 1–3 days of execution, not weeks. A new RQ/table in the revised paper plus a sub-study report in the response doc is usually enough.

#### General recipe — challenge → bounded mini-study

1. **Quote the reviewer's exact concern.** It almost always falls into one of:
   - **Correctness/soundness** — your metric proves the build passed, not that the output is right
   - **Representativeness** — your sample is too small, too skewed, or hand-picked
   - **External validity** — your results only hold under condition X
   - **Comparability** — your baseline is unfair, outdated, or misconfigured
2. **Design the smallest experiment that produces a decisive signal.** Pre-specify success criteria in the response doc before running: "if X out of N cases produce signal Y, we claim Z." Reviewers respect declared methodology more than post-hoc rationalisation.
3. **Use a stratified sample that mirrors the original distribution.** If the original 1000-case evaluation was 60% type-A / 30% type-B / 10% type-C, the validation sample (say 30 cases) should hold those proportions. Same-distribution > random.
4. **Discriminate by domain-specific signal, not exit code.** "Command exited 0" is rarely a sufficient witness. The check needs an artefact-specific signal — assertion message, output equivalence on held-out inputs, behaviour difference on the exact failure-inducing input, exception message rather than exception class, etc.
5. **Acknowledge sample-size bounds honestly.** When N is small because the underlying resource is scarce (ground-truth labels, public exploits, reproducible bug reports, expert annotations), call out the **scarcity-bound** explicitly: *"N is bounded by [resource], not by methodology. The protocol is artefact-agnostic and O(1) per case once [resource] is available."* This turns "small N" from a weakness into a documented scope limit.

#### Common mini-study shapes in SE revisions

| Reviewer concern | Mini-study shape |
|---|---|
| "Tool output is plausible but unverified" | Stratified subset + manual verification by an agreed protocol; two-author inter-rater agreement; report Cohen's κ if claims are subjective |
| "Sample is unrepresentative" | Re-sample with explicit strata; report original vs new distribution side-by-side |
| "Baseline is unfair / outdated" | Re-run baseline with author-recommended config or newest released version; report the gap shrinking (or not) — concede if it does |
| "Behaviour-change claim not validated" | Witness experiment: a specific input that fails before and succeeds after (or vice versa), measured directly rather than via aggregate metric |
| "Newer LLM/tool/framework would change result" | Sensitivity study: re-run the pipeline with 1–2 alternative models/tools/versions; show conclusions hold (or report how they shift) |
| "Correctness, not just plausibility" (e.g., generated patch, synthesised test, repaired program) | Per-case ground-truth check against an oracle the reviewer agrees with: developer-written test, upstream fix, manual review, formal property |

#### Reporting the mini-study in the response doc

- Lead with the **numeric result** before the methodology paragraph. Reviewers triage on the number.
- Show the **protocol** explicitly enough that a reviewer could redo it. Two authors? Random seed? Tie-breaking rule? Disclose it.
- Tabulate **per-stratum success/failure counts**, not just totals — the table is where reviewers spot uneven coverage.
- Drop a one-line **scope statement** at the end: *"This sub-study validates correctness on the stratified sample; generalising to the full population is left to future work."* Bounded claims survive.

### 5. Update the anonymized artifact (during revision, before camera-ready)

If the venue permits artifact updates during the revision/rebuttal window, use this to add the mini-study data, new experiments, or expanded results from Section 4. Check the call/submission-system policy first: some venues or tracks freeze artifacts after first submission, require all changes to be disclosed, or impose additional anonymity constraints.

**Anonymization checklist before pushing:**
- Strip `/Users/<name>` (or `/home/<name>`) paths from scripts; use relative paths or env vars.
- Grep for institution names, ORCID, personal email addresses, institutional cloud-drive URLs.
- Exclude build outputs (`target/`, `build/`, `dist/`, `__pycache__/`, `node_modules/`) and IDE config (`.DS_Store`, `.idea/`, `.vscode/`).
- Don't change `git config user.name/email` mid-history (existing commits already show the author); use a pre-existing anonymous account for the pushing repo.
- Don't push to a repo whose URL contains the author's name or institution.
- For OOPSLA/ICSE/FSE/ASE/ISSTA: most venues now accept author-name-revealing artifact URLs *during revision* but not at *initial submission* — re-read the venue's current policy each cycle, it has changed in recent years.

**Single-command reproduction is the goal.** A reviewer should reach the headline result with one `docker run` (or `make`, or `bash run.sh`). The container/script should print a clearly-formatted final line (e.g., `RESULT: 47/50 passed` or `EVAL: F1=0.83 on N=300`) so the reviewer can confirm the result in 30 seconds without parsing logs.

```dockerfile
# Generic template — adapt the base image, deps, and entrypoint to your stack
FROM <base-image-matching-your-runtime>           # e.g. python:3.11, eclipse-temurin:17, rust:1.78
RUN <install system deps>                          # apt-get / apk / etc.
WORKDIR /artifact
COPY <required source/data/scripts> ./
RUN <build / install / preprocess>                 # done at image-build time, not run time
ENTRYPOINT ["./run_eval.sh"]                       # prints headline metric and exits 0/1
```

**Multi-arch matters.** Reviewers run a mix of Intel CI, Apple Silicon laptops, and ARM cloud instances:
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t <name> --push .
```
If a dependency only exists for `amd64`, document that in the README so reviewers on Apple Silicon know to use `--platform linux/amd64` (Rosetta) rather than silently failing.

## Statistical framing for empirical claims

- **"Full-population observational" beats "we didn't run hypothesis tests."** When the data covers the entire population in scope rather than a sample drawn from a larger one, frequentist p-values lose their sampling-distribution interpretation. Report descriptively and defer cross-population generalization to future work.
- **Prefer "conservative lower bound" over "complete."** A bounded claim survives reviewer scrutiny; an absolute claim attracts counterexamples.
- **Prefer "dataset-specific" over "generalizable"** unless strong cross-dataset evidence exists.

## Citation hygiene during revision

- **Verify every new bib entry against Crossref / DBLP / publisher page** before adding. Authors, title, venue, year, pages, DOI. Never invent metadata.
- **Run the whole `.bib` through a bib-checker** before submitting the revision. The checker catches stale arXiv-only entries that now have a venue, missing DOIs, wrong author orderings, broken pages, and ICSE/FSE proceedings-name drift. Options:
  - **Local:** `bibtex-tidy --duplicates --check-quality file.bib` or a small `crossref-lookup` script for batch DOI validation.
  - **Hosted:** [`https://bib-check.remedius.cc/`](https://bib-check.remedius.cc/) — paste or upload the `.bib`, returns per-entry suggestions.
  - **Other hosted/commercial checkers** such as BibTeX Tidy's web UI, JabRef's online consistency check, or Mendeley/Zotero validators. Before uploading to any hosted service, check that it is appropriate for any unpublished or embargoed citation metadata your `.bib` may contain.
- **Cite named tools/libraries in motivating examples.** If you mention `tokio-tar`, cite it (as `@misc` GitHub if no formal pub) and add a one-line gloss in the paragraph.
- **Don't claim "much higher than prior work"** if prior work didn't measure the comparable quantity. Either drop the comparison or anchor it on a specific number from a specific paper.

## Style preferences

- Avoid em-dashes in paper prose if the project style avoids them; use en-dashes only for ranges.
- No AI-flavour openers ("It is worth noting," "Importantly," "We thank the reviewer for…"). The thank-you belongs in the response doc once at the top of each reviewer section, not inside each item.
- No structured "Finding./Impact./Summary." micro-labels appended to bullets.
- Paper prose must not sound like a response to reviewer feedback. Phrases like "as noted by reviewers" or "we acknowledge that" belong in the response doc, not the paper.
- No mid-sentence line wraps in source — one long line per paragraph in both paper and response. Easier to diff.
- Short paragraphs over long ones. Remove throat-clearing.

## Common pitfalls

| Failure mode | How to avoid |
|---|---|
| Answering a nearby question instead of the exact one | Quote the reviewer comment verbatim and re-read it after drafting the response |
| Hedging instead of conceding | If the reviewer is right, drop the claim — don't wrap it in a qualifier |
| Inflating empirical effort | Count categories honestly (X reused + Y curated + Z newly produced = total). If the math doesn't add up, fix it before submitting |
| Overclaiming provenance of a resource | Specify exactly what was verified vs assumed. "14 datapoints verified against upstream commits" beats "~30 datapoints from various sources" |
| Stale numbers in supporting docs | After a count changes during revision, grep every supporting doc/README/appendix/abstract for the old number |
| Anonymity leak via push history | Use a pre-existing anonymous git account; check `git log --pretty=format:%ae` before pushing |
| Stratum skew without justification | If your validation sample is heavier in one class than the original distribution, explain the structural reason (resource scarcity, validation-cost asymmetry, intentional oversampling of edge cases) — don't hide it |
| Promising experiments you can't run | Don't write "we will additionally evaluate X in the camera-ready" unless X is genuinely feasible. Reviewers remember these promises |
| Paper page-limit overrun after additions (which is not a problem during draft phase) | Adding a new RQ / new tables / new method prose pushes the paper past the venue cap — condense related work and existing evaluation prose first; move detail tables to the appendix; keep the diff "old text removed, new text added" at roughly equal size (already a Section 3 rule) |

## Reproducibility checklist before final push

- [ ] Every numeric claim in the response doc matches the paper PDF and the artifact data; no stale numbers from a prior draft.
- [ ] Headline-result script / `make` target / `docker run` produces the same number a reviewer would read in the paper, from a fresh clone, in under 30 seconds of human attention.
- [ ] Container image (if any) builds on both `linux/amd64` and `linux/arm64`, or the platform constraint is documented.
- [ ] No `/Users/<name>` (or `/home/<name>`) paths, no `git config` author leak, no institutional URL anywhere in the artifact.
- [ ] Response doc compiles cleanly; every paper-quote block matches the revised PDF exactly (copy-paste, don't retype).
- [ ] Paper PDF page count within the venue limit AFTER all blue additions land; no overfull hboxes in revised regions.
- [ ] Bib entries verified against Crossref / DBLP for every new citation, AND the whole `.bib` run through a bib-checker (e.g., `bibtex-tidy --check-quality` locally, or `https://bib-check.remedius.cc/`).
- [ ] Diff PDF visibly shows every reviewer-promised change as blue text; no accidentally-blue unchanged regions.
