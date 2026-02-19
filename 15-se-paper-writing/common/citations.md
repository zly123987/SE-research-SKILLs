# Citation Guidelines

[← Back to Main](../SKILL.md)

Comprehensive citation is expected in SE papers. Reviewers expect thorough literature coverage.

## Citation Density Guidelines

| Section | Expected Citations |
|---------|-------------------|
| Introduction | 5-10 |
| Background | 3-5 |
| Methodology | 2-5 |
| Evaluation | 3-5 |
| Related Work | 15-25 |
| **Total** | **30-50** |

---

## What Requires Citation

### Cite ALL Concepts Not Original to This Paper

**Bad (using terms without citation):**
```latex
We use static analysis to detect conflicts. The LLM performs
Chain-of-Thought reasoning to identify semantic issues.
```

**Good (properly cited):**
```latex
We use static analysis~\cite{nielson2015principles} to detect conflicts.
The LLM performs Chain-of-Thought reasoning~\cite{wei2022chain} to
identify semantic issues.
```

### Concepts Requiring Citation

| Category | Examples |
|----------|----------|
| **Techniques** | Static analysis, symbolic execution, fuzzing, program repair |
| **Statistical tests** | Fisher's exact test, McNemar's test, Cliff's delta |
| **Paradigms** | ReAct agents, Chain-of-Thought, RAG |
| **Metrics** | Precision, recall (if not universally known) |
| **Tools** | pip, Poetry, Docker (if discussing technically) |
| **Prior approaches** | Any tool you compare against or build upon |

---

## Finding Citations

### Primary Sources

| Source | URL | Best For |
|--------|-----|----------|
| **DBLP** | https://dblp.org | SE venues (authoritative) |
| **Semantic Scholar** | https://semanticscholar.org | Related work discovery |
| **ACM DL** | https://dl.acm.org | ACM venues |
| **IEEE Xplore** | https://ieeexplore.ieee.org | IEEE venues |
| **arXiv** | https://arxiv.org | Recent preprints |

### DBLP Search Example

```python
import requests

def get_dblp_bibtex(query: str) -> str:
    """Search DBLP and get BibTeX."""
    resp = requests.get(
        "https://dblp.org/search/publ/api",
        params={"q": query, "format": "json", "h": 5}
    )
    results = resp.json()["result"]["hits"]["hit"]

    if not results:
        return None

    key = results[0]["info"]["key"]
    bibtex_url = f"https://dblp.org/rec/{key}.bib"
    return requests.get(bibtex_url).text
```

---

## BibTeX Validation (CRITICAL)

### Never Hallucinate Citations

**Before including any citation, VERIFY it exists:**

1. Search DBLP/Semantic Scholar for the paper
2. Verify it was actually published
3. Fetch BibTeX from DBLP (most reliable)
4. If uncertain, mark as `[CITATION NEEDED]`

### Validation Workflow

```
FOR EACH entry in references.bib:
  1. SEARCH online using title and authors
     - Primary: DBLP
     - Secondary: Google Scholar, Semantic Scholar
     - Tertiary: ACM DL, IEEE Xplore, arXiv

  2. VERIFY fields match:
     - Title: Exact match (check capitalization)
     - Authors: All authors present, correctly spelled
     - Venue: Correct conference/journal name and year
     - Pages: Verify if available
     - DOI: Verify it resolves

  3. FLAG issues:
     - ❌ NOT FOUND: Paper doesn't exist (hallucination)
     - ⚠️ MISMATCH: Details don't match online source
     - ✅ VERIFIED: Entry matches authoritative source

  4. FIX or REMOVE problematic entries
```

### Validation Report Format

```markdown
## BibTeX Validation Report

### ✅ Verified (N entries)
- wang2020pyego: PyEGo (ESEC/FSE 2020) - DBLP verified
- wei2022chain: Chain-of-Thought (NeurIPS 2022) - Scholar verified

### ⚠️ Needs Correction (M entries)
- zhang2024learning: Year should be 2023, not 2024
- fan2023large: Missing page numbers

### ❌ Not Found / Suspicious (K entries)
- chen2024pllm: Could not find - verify existence
```

---

## Citation Format

### In-Sentence vs Parenthetical

```latex
% In-sentence (author as subject)
Wang et al.~\cite{wang2020pyego} propose a knowledge graph approach.

% Parenthetical (idea as subject)
Knowledge graphs have been applied to dependency analysis~\cite{wang2020pyego}.
```

### Multiple Citations

```latex
% Group related work
Prior approaches use knowledge graphs~\cite{wang2020pyego, ye2022pycre}
and LLM-based analysis~\cite{chen2024pllm, bouzenia2024repairagent}.
```

### Self-Citations (Double-Blind)

```latex
% Option 1: Anonymous placeholder
Prior work by [anonymous]~\cite{anonymous2023} showed...

% Option 2: Omitted reference
Our prior work~\cite{omitted_for_review} established...

% Option 3: Third-person self-reference
Prior work by the authors~\cite{self2023} demonstrated...
```

---

## BibTeX Best Practices

### Required Fields by Entry Type

| Entry Type | Required Fields |
|------------|-----------------|
| `@inproceedings` | author, title, booktitle, year |
| `@article` | author, title, journal, year, volume |
| `@misc` (arXiv) | author, title, howpublished, year |

### Example Entries

```bibtex
% Conference paper
@inproceedings{wang2020pyego,
  author    = {Wang, Kaifeng and Ye, Xin and Sun, Yanhua},
  title     = {PyEGo: Automatically Handling Python Environment
               Configuration Errors},
  booktitle = {Proceedings of the 28th ACM Joint Meeting on European
               Software Engineering Conference and Symposium on the
               Foundations of Software Engineering},
  series    = {ESEC/FSE '20},
  year      = {2020},
  pages     = {839--851},
  doi       = {10.1145/3368089.3409697},
}

% Journal article
@article{decan2019empirical,
  author    = {Decan, Alexandre and Mens, Tom and Claes, Maelick},
  title     = {An empirical comparison of dependency issues in OSS
               packaging ecosystems},
  journal   = {Empirical Software Engineering},
  volume    = {24},
  number    = {4},
  pages     = {2291--2340},
  year      = {2019},
}

% arXiv preprint
@misc{chen2024pllm,
  author       = {Chen, Qiuyu and Zhang, Yue and Li, Wen},
  title        = {PLLM: A Python LLM-based Dependency Fixer},
  howpublished = {arXiv preprint arXiv:2401.12345},
  year         = {2024},
}
```

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inconsistent author format | Use "Last, First" consistently |
| Missing DOI | Add DOI for all recent papers |
| Wrong venue abbreviation | Use full venue name in booktitle |
| Fabricated citation | Verify existence before including |

---

## Include Papers Beyond Top Venues

Related work should include relevant papers from:
- Workshop papers (recent techniques)
- arXiv preprints (SOTA not yet published)
- Tool papers (important baselines)
- Industry reports (practical context)

---

## Checklist

- [ ] 30-50 total citations
- [ ] All concepts not original to paper are cited
- [ ] BibTeX entries validated against DBLP/Scholar
- [ ] No fabricated or hallucinated citations
- [ ] Self-citations anonymized for double-blind
- [ ] Non-breaking spaces before citations (`~\cite{}`)
- [ ] Related work covers last 2-3 years
- [ ] Consistent BibTeX formatting

[Back to Main →](../SKILL.md)
