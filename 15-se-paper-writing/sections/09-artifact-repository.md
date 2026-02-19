# Section 9: Artifact Repository Setup

[← Back to Main](../SKILL.md) | [← Final Check](08-final-check.md)

Run this step **after the paper is finalized** (all sections drafted, final check passed, PDF compiles cleanly). This step collects your implementation, data, and evaluation scripts into a standalone, anonymous artifact repository suitable for double-blind review.

---

## 1. Goal

Create a self-contained repository that allows reviewers and future researchers to:
- **Reproduce** every table and figure in the paper's evaluation
- **Understand** the tool's architecture from the README alone
- **Run** the tool on new inputs beyond the paper's dataset

The repo link is embedded in the paper's Data Availability section so reviewers can inspect it during review.

---

## 2. Repository Structure

```
artifact-repo/
├── README.md                 # Concise reproduction guide (see template below)
├── LICENSE                   # MIT or Apache 2.0
├── requirements.txt          # Pinned dependency versions
├── src/                      # Core tool implementation
│   ├── <core_module>.py      # Main pipeline / entry point
│   └── ...                   # Supporting modules
├── data/                     # Evaluation dataset (or download script if large)
│   ├── README.md             # Dataset description and provenance
│   └── ...
├── scripts/                  # Evaluation reproduction scripts
│   ├── run_rq1.py            # One script per RQ (or a unified runner)
│   ├── run_rq2.py
│   └── generate_tables.py    # Script that produces paper tables from raw results
├── results/                  # Pre-computed results for quick verification
│   ├── rq1/
│   ├── rq2/
│   └── ...
├── knowledge/                # External knowledge bases, configs, prompts
│   └── ...
└── .gitignore
```

### What to include

| Category | Include | Exclude |
|----------|---------|---------|
| **Source code** | All modules needed to run the tool end-to-end | IDE configs, `__pycache__`, `.pyc` |
| **Data** | Benchmark data, test cases, ground truth | Raw downloads > 100 MB (provide download script instead) |
| **Scripts** | Evaluation scripts that reproduce each RQ | Ad-hoc debugging scripts, notebooks with hardcoded paths |
| **Results** | Pre-computed outputs for every RQ | Intermediate checkpoints, logs |
| **Knowledge** | Prompts, API mapping files, knowledge bases | API keys, credentials |
| **Config** | `requirements.txt`, `.gitignore`, `LICENSE` | `.env`, `config.ini` with secrets |

### What to **never** include

- API keys, tokens, or credentials (use environment variables)
- Author names, institution names, or identifying information (double-blind)
- Git history from the research repo (start a fresh repo)
- Unrelated project files, paper LaTeX source, or progress notes

---

## 3. Anonymization Checklist

Double-blind venues require the artifact to be anonymous during review:

- [ ] **No author names** in README, code comments, docstrings, or commit messages
- [ ] **No institution names** or lab URLs
- [ ] **No personal GitHub account** — use a throwaway anonymous account or organization
- [ ] **Git history is clean** — either a fresh repo with a single commit, or history scrubbed of identifying info
- [ ] **No paper PDF** included in the repo (the paper links to the repo, not the reverse)
- [ ] **Tool name is OK** — tool names (e.g., "Astra") are conventional and not deanonymizing
- [ ] **Commit messages are generic** — e.g., "Initial artifact release" (not "John's fix for RQ2")
- [ ] **Config files sanitized** — no hardcoded paths like `/home/username/...`

---

## 4. README Template

The README is the single most important file. Reviewers read it first and may not look further if it's unclear.

```markdown
# [ToolName]: [One-Line Description]

Artifact repository for the paper "[Paper Title]" submitted to [Venue Year].

## Overview

[2-3 sentences: what the tool does, what problem it solves, key approach.]

**Main Results (from paper):**
- [Metric 1]: [value] (e.g., "90.9% per-change accuracy on [benchmark]")
- [Metric 2]: [value]
- [Metric 3]: [value]

## Requirements

- Python 3.10+
- [Other system requirements]
- API key for [LLM provider] (set as environment variable `[VAR_NAME]`)

## Installation

    git clone [repo-url]
    cd [repo-name]
    pip install -r requirements.txt

## Reproducing Paper Results

### RQ1: [RQ Title]

    python scripts/run_rq1.py

Expected output: [brief description of what it produces and where]

### RQ2: [RQ Title]

    python scripts/run_rq2.py

[Repeat for each RQ]

### Generating Tables

    python scripts/generate_tables.py

Produces the tables from the paper in `results/tables/`.

## Pre-Computed Results

If you want to verify results without re-running (e.g., to avoid LLM API costs):

    ls results/          # Pre-computed outputs for all RQs

## Directory Structure

| Path | Description |
|------|-------------|
| `src/` | [Brief description of core implementation] |
| `data/` | [Brief description of dataset] |
| `scripts/` | [Brief description of evaluation scripts] |
| `results/` | [Brief description of pre-computed results] |
| `knowledge/` | [Brief description of knowledge bases / prompts] |

## License

MIT License
```

### README quality bar

- A reviewer should be able to reproduce RQ1 within **10 minutes** of cloning
- Every command in the README must be copy-pasteable (no `[placeholders]` in commands)
- If LLM API access is required, state the estimated cost and provide pre-computed results as alternative

---

## 5. Workflow: From Research Project to Artifact Repo

### Step 1: Create or initialize the repo

```bash
# Option A: Create new repo on GitHub (private for review, public after acceptance)
gh repo create anonymous-org/tool-artifact --private \
    --description "Artifact for [Paper Title] at [Venue Year]"

# Option B: Use an existing empty repo
cd /path/to/existing-repo
```

### Step 2: Copy implementation files

Copy only the files needed to run the tool. Do NOT copy the entire research project.

```bash
# Core implementation
cp -r /path/to/project/src/ artifact-repo/src/

# Dataset
cp -r /path/to/project/data/ artifact-repo/data/

# Evaluation scripts (select only the ones that reproduce RQs)
mkdir -p artifact-repo/scripts/
cp /path/to/project/src/run_rq*.py artifact-repo/scripts/
cp /path/to/project/src/run_baselines.py artifact-repo/scripts/

# Knowledge bases, prompts, configs
mkdir -p artifact-repo/knowledge/
cp /path/to/project/data/knowledge_base.json artifact-repo/knowledge/

# Pre-computed results
cp -r /path/to/project/results/ artifact-repo/results/
```

### Step 3: Sanitize

```bash
# Remove __pycache__, .pyc, IDE files
find artifact-repo/ -type d -name __pycache__ -exec rm -rf {} +
find artifact-repo/ -name "*.pyc" -delete
find artifact-repo/ -name ".DS_Store" -delete

# Remove any hardcoded paths
grep -rn "/home/" artifact-repo/src/ artifact-repo/scripts/
# Fix any matches to use relative paths or environment variables

# Remove any API keys or credentials
grep -rn "sk-" artifact-repo/
grep -rn "api_key" artifact-repo/
# Fix any matches to use environment variables

# Remove author/institution names
grep -rni "author_name\|university_name\|lab_name" artifact-repo/
```

### Step 4: Create supporting files

```bash
# requirements.txt — pin versions
pip freeze | grep -E "openai|tiktoken|..." > artifact-repo/requirements.txt

# .gitignore
cat > artifact-repo/.gitignore << 'EOF'
__pycache__/
*.pyc
.env
*.log
.DS_Store
EOF

# LICENSE (MIT)
# Use standard MIT license text
```

### Step 5: Write the README

Follow the template in Section 4. Fill in every placeholder. Test every command.

### Step 6: Verify reproducibility

Before pushing, verify:

```bash
cd artifact-repo/
pip install -r requirements.txt
python scripts/run_rq1.py  # Should produce results matching the paper
```

### Step 7: Push and get the link

```bash
cd artifact-repo/
git add .
git commit -m "Initial artifact release"
git push -u origin main
```

The repo URL (e.g., `https://github.com/anonymous-org/tool-artifact`) goes into the paper.

### Step 8: Update paper's Data Availability section

In the conclusion/data-availability section of the LaTeX source:

```latex
\section*{Data Availability}
Our replication package (source code, evaluation data, and reproduction
scripts) is available at \url{https://github.com/xxx/tool-artifact}.
```

For Zenodo archival (post-acceptance):
```latex
Our replication package is archived at
\url{https://doi.org/10.5281/zenodo.XXXXXXX}.
```

---

## 6. Decision Checklist

Before pushing the artifact repo:

### Repository
- [ ] Fresh git history (no research-repo history leaking)
- [ ] `.gitignore` covers `__pycache__`, `.env`, `*.pyc`, logs
- [ ] No files > 50 MB (use Git LFS or download scripts for large data)
- [ ] LICENSE file present (MIT or Apache 2.0)

### Anonymization
- [ ] No author names, institution names, or identifying URLs
- [ ] Anonymous GitHub account or organization
- [ ] Commit messages are generic
- [ ] No hardcoded paths containing usernames

### README
- [ ] Paper title and venue stated
- [ ] Tool overview in 2-3 sentences
- [ ] Main results summarized (matching paper numbers exactly)
- [ ] Installation steps are copy-pasteable
- [ ] Reproduction commands for every RQ
- [ ] Pre-computed results documented as alternative
- [ ] Directory structure table with descriptions
- [ ] Estimated cost / time for full reproduction

### Code
- [ ] `requirements.txt` with pinned versions
- [ ] All scripts run without errors from a clean install
- [ ] No API keys or credentials in code (use env vars)
- [ ] Paths are relative, not absolute

### Data
- [ ] Benchmark data included (or download script provided)
- [ ] Data format documented
- [ ] Ground truth labels included for evaluation

### Results
- [ ] Pre-computed results for every RQ
- [ ] Results match the numbers in the paper

### Paper Link
- [ ] Data Availability section updated with repo URL
- [ ] URL uses anonymous account (not personal GitHub)

---

## 7. Post-Acceptance Steps

After the paper is accepted:

1. **Make repo public** (if it was private during review)
2. **Create a GitHub release** (tag `v1.0.0`)
3. **Archive on Zenodo** (link GitHub → Zenodo for automatic DOI)
4. **Update paper** with Zenodo DOI in camera-ready
5. **Add author information** to README and code

---

[← Final Check](08-final-check.md) | [Back to Main →](../SKILL.md)
