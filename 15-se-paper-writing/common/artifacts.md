# Artifact and Reproducibility

[← Back to Main](../SKILL.md)

Most SE venues now expect artifacts. This guide covers preparation, badges, and Zenodo DOIs.

## Artifact Package Contents

```
artifact/
├── README.md              # Setup instructions
├── INSTALL.md             # Dependencies and installation
├── STATUS.md              # Claimed artifact badges
├── LICENSE                # Open source license (MIT/Apache)
├── requirements.txt       # Dependencies with versions
├── Dockerfile             # For reproducibility
├── src/                   # Tool source code
├── data/                  # Datasets (or links if large)
├── scripts/               # Evaluation scripts
│   ├── run_evaluation.py
│   └── generate_tables.py
└── results/               # Pre-computed results for verification
```

---

## Artifact Badges

SE conferences offer badges for artifacts:

| Badge | Meaning | Requirements |
|-------|---------|--------------|
| **Available** | Publicly accessible | DOI, permanent URL |
| **Functional** | Code runs and produces results | README, tests pass |
| **Reusable** | Well-documented, extensible | Examples, good docs |
| **Replicated** | Results independently verified | Separate committee check |

### Badge Requirements

**Available:**
- Public repository (GitHub, GitLab)
- Permanent identifier (Zenodo DOI)
- Open license

**Functional:**
- Clear installation instructions
- Code runs without errors
- Produces claimed outputs

**Reusable:**
- Comprehensive documentation
- Example usage
- Extension guidance

---

## README Template

```markdown
# [Tool Name]: [Short Description]

[![DOI](https://zenodo.org/badge/DOI/xx.xxxx/zenodo.xxxxxxx.svg)](https://doi.org/xx.xxxx/zenodo.xxxxxxx)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Paper:** "[Full Paper Title]"
> **Venue:** [Conference] [Year]
> **Authors:** [Author List]

## Overview

[2-3 sentences describing what the tool does]

**Key Contributions:**
1. [Contribution 1]
2. [Contribution 2]
3. [Contribution 3]

**Main Results:**
- [Result 1: "80% detection rate"]
- [Result 2: "100% ISR"]

## Quick Start

### Installation

```bash
git clone https://github.com/xxx/tool-artifact
cd tool-artifact
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Basic Usage

```python
from tool import analyze
result = analyze("path/to/project")
print(result)
```

### Reproduce Paper Results

```bash
python scripts/run_evaluation.py --benchmark data/benchmark/
python scripts/generate_tables.py
```

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| `src/` | Core implementation |
| `data/` | Evaluation dataset |
| `scripts/` | Reproduction scripts |
| `results/` | Pre-computed results |

## Requirements

- Python 3.10+
- [Other requirements]

## Citation

```bibtex
@inproceedings{author2026tool,
  author = {Authors},
  title = {Paper Title},
  booktitle = {Venue},
  year = {2026},
}
```

## License

MIT License - see [LICENSE](LICENSE)
```

---

## Zenodo Integration

Zenodo provides permanent DOIs for research artifacts.

### Setup Process

1. **Link GitHub to Zenodo:**
   - Go to https://zenodo.org/account/settings/github/
   - Enable your repository

2. **Create GitHub Release:**
   - Tag version (e.g., v1.0.0)
   - Zenodo automatically archives and assigns DOI

3. **Add DOI Badge to README:**
   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
   ```

### Cite in Paper

```latex
Our tool and evaluation data are available at
\url{https://doi.org/10.5281/zenodo.XXXXXXX}.
```

---

## Dockerfile Template

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install tool
RUN pip install -e .

# Default command
CMD ["python", "scripts/run_evaluation.py"]
```

### Usage

```bash
# Build
docker build -t tool-artifact .

# Run evaluation
docker run -v $(pwd)/results:/app/results tool-artifact

# Interactive
docker run -it tool-artifact bash
```

---

## Pre-Submission Checklist

### Repository

- [ ] Public repository on GitHub/GitLab
- [ ] Clear, descriptive name
- [ ] LICENSE file (MIT/Apache 2.0)
- [ ] No hardcoded paths
- [ ] No API keys in code

### README

- [ ] Paper title and venue
- [ ] Overview and contributions
- [ ] Installation instructions
- [ ] Quick start / usage example
- [ ] How to reproduce results
- [ ] File structure explanation
- [ ] Requirements listed
- [ ] Citation BibTeX

### Code Quality

- [ ] Code runs without errors
- [ ] requirements.txt with pinned versions
- [ ] setup.py or pyproject.toml
- [ ] Tests pass

### Data

- [ ] Dataset included (or linked if large)
- [ ] Data format documented
- [ ] Scripts to regenerate tables/figures

### Documentation

- [ ] INSTALL.md with step-by-step setup
- [ ] Comments in complex code
- [ ] Example inputs/outputs

### Archival

- [ ] Zenodo integration enabled
- [ ] GitHub release created
- [ ] DOI badge in README

### Anonymization (Double-Blind)

- [ ] Author names removed from code comments
- [ ] Institution names removed
- [ ] Anonymous GitHub account if required

---

## Artifact Repository Creation Workflow

```bash
# 1. Create repository
gh repo create tool-artifact --public \
    --description "Artifact for Paper Title at Venue 2026"

# 2. Clone and populate
git clone https://github.com/username/tool-artifact
cd tool-artifact

# 3. Copy files
cp -r /path/to/project/src .
cp -r /path/to/project/data .
cp -r /path/to/project/scripts .

# 4. Create README, LICENSE, etc.
# (Use templates above)

# 5. Commit and push
git add .
git commit -m "Initial artifact release"
git push origin main

# 6. Create release for Zenodo
gh release create v1.0.0 --title "Paper Submission" \
    --notes "Artifact for Venue 2026 submission"
```

---

## Data Availability Statement

Include in paper (often required by ISSTA and others):

```latex
\section*{Data Availability}

Our tool, evaluation data, and reproduction scripts are publicly
available at \url{https://github.com/xxx/tool-artifact} and archived
at \url{https://doi.org/10.5281/zenodo.XXXXXXX}.
```

---

## Checklist Summary

| Category | Items |
|----------|-------|
| **Repo** | Public, licensed, no secrets |
| **README** | Title, usage, reproduction, citation |
| **Code** | Runs, tested, documented |
| **Data** | Included or linked, documented |
| **Archival** | Zenodo DOI, release tagged |
| **Paper** | Data availability statement |

[Back to Main →](../SKILL.md)
