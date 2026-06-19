# Software Engineering Research `Skills` Library

> An open-source library of skills for AI agents conducting software-engineering research.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<sub>📚 This library is collected and organised **solely for academic use** with full commitment to research integrity and responsible scholarship. It is shared **for scholarly exchange and learning purposes only** (仅供学术交流学习使用), and must not be used to fabricate results, plagiarise, circumvent peer review, evade detection, or otherwise undermine the integrity of software-engineering research or any other field. By using these skills you agree to apply them ethically and to take full responsibility for any output they produce.</sub>

## Scope

The library is organised into numbered categories spanning the SE research lifecycle. **Currently 7 of 15 planned categories have published content**; the remainder are placeholders being populated incrementally.

<details>
<summary><b>15 Planned Categories (7 currently published)</b></summary>

| | | |
|:---:|:---:|:---:|
| **01 Program Analysis** ✅ | **02 Agent Construction** ✅ | 03 Code Generation 🚧 |
| **04 Bug Detection & Repair** ✅ | 05 Mining Software Repos 🚧 | 06 Software Security 🚧 |
| 07 Dependency Management 🚧 | 08 Code Review & Quality 🚧 | 09 DevOps & CI/CD 🚧 |
| 10 Empirical SE 🚧 | **11 Experiment Design** ✅ | 12 Software Architecture 🚧 |
| 13 Human Aspects of SE 🚧 | 14 AI/ML for SE 🚧 | **15 SE Paper Writing** ✅ |
| **16 Rebuttal** ✅ | **17 Revision** ✅ | |

✅ published — 🚧 in progress

</details>

---

## Table of Contents

- [Our Mission](#our-mission)
- [Target Venues](#target-venues)
- [Available SE Research Engineering Skills](#available-se-research-engineering-skills)
- [Skill Structure](#skill-structure)
- [Roadmap](#roadmap)
- [Repository Structure](#repository-structure)
- [Use Cases](#use-cases)

## Our Mission

We provide the layer of **Engineering Ability** that **enables your coding agent to write and conduct software engineering research experiments**, including building analysis tools, running evaluations on benchmarks, mining repositories, and preparing submissions for top-tier SE venues.

```
┌─────────────────────────────────────────────────────────────┐
│                SE RESEARCH AGENT SYSTEM                     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Research   │  │   Analysis   │  │  Evaluation  │      │
│  │   Question   │──│    Tools     │──│   & Paper    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                 │               │
│         ▼                 ▼                 ▼               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              SE RESEARCH SKILLS                      │   │
│  │  Program Analysis | Testing | Bug Detection | MSR   │   │
│  │  Security | Dependencies | Code Review | DevOps     │   │
│  │  AI4SE | Empirical Methods | Paper Writing          │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Target Venues

These skills are designed to support research targeting top-tier SE venues:

| Venue | Type | Focus Area | Typical Deadline |
|-------|------|------------|------------------|
| **ICSE** | Conference | Flagship, broad SE | August |
| **FSE/ESEC** | Conference | Foundations, empirical | March/April |
| **ASE** | Conference | Automation in SE | May |
| **ISSTA** | Conference | Software testing & analysis | January |
| **MSR** | Conference | Mining software repositories | January |
| **EMSE** | Journal | Empirical software engineering | Rolling |
| **TSE** | Journal | Broad software engineering | Rolling |
| **TOSEM** | Journal | Methods and tools | Rolling |

## Available SE Research Engineering Skills

**Quality over quantity**: Each skill provides comprehensive, expert-level guidance with real code examples, troubleshooting guides, and production-ready workflows.

### 01 - Program Analysis

Tools for static and dynamic analysis of programs.

| Skill | Description |
|-------|-------------|
| **[tree-sitter](01-program-analysis/tree-sitter/)** | Incremental parsing for many languages, AST manipulation, syntax highlighting |

*Planned:* CodeQL, Joern, WALA, Soot.

### 02 - Agent Construction

Foundations for building LLM-driven agents that can carry out SE research tasks.

| Skill | Description |
|-------|-------------|
| **[react-langgraph](02-agent-construction/react-langgraph/)** | Building ReAct-style agents with LangGraph, including tool use, state machines, and evaluation |

### 03 - Code Generation

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to the existing modules listed above (especially **[01 - Program Analysis](#01---program-analysis)** for code-AST work and **[02 - Agent Construction](#02---software-testing)** for LLM-agent foundations).

### 04 - Bug Detection & Repair

Automated program repair and bug localization.

| Skill | Description |
|-------|-------------|
| **[Defects4J](04-bug-detection-repair/defects4j/)** | Java bug benchmark, real bugs with test suites |

*Planned:* BugsInPy, GumTree, repair-llm.

### 05 - Mining Software Repositories

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to **[11 - Experiment Design](#11---requirements-engineering)** for general empirical-study workflow and **[04 - Bug Detection & Repair](#04---bug-detection--repair)** for existing benchmark coverage.

### 06 - Software Security

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to **[01 - Program Analysis](#01---program-analysis)** for the analysis substrate most security tools build on.

### 07 - Dependency Management

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to the existing modules listed above.

### 08 - Code Review & Quality

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to the existing modules listed above.

### 09 - DevOps & CI/CD

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to the existing modules listed above.

### 10 - Empirical SE

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to **[11 - Experiment Design](#11---requirements-engineering)** for the closely-related experiment-workflow skill.

### 11 - Experiment Design

Workflow templates for designing and running SE experiments.

| Skill | Description |
|-------|-------------|
| **[experiment-workflow](11-experiment-design/experiment-workflow/)** | Designing controlled experiments, sampling, RQ formulation, validity threats |

### 12 - Software Architecture

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to the existing modules listed above.

### 13 - Human Aspects of SE

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to the existing modules listed above.

### 14 - AI/ML for SE

> 🚧 **We are updating this category.** No skills are published here yet. For now, please refer to **[02 - Agent Construction](#02---software-testing)** for LLM-agent foundations.

### 15 - SE Paper Writing

Writing for top-tier SE venues.

| Skill | Description |
|-------|-------------|
| **[se-paper-writing](15-se-paper-writing/)** | ICSE, FSE, ASE paper writing — modular section guides, LaTeX templates, reviewer checklists |

### 16 - Rebuttal

Writing one-shot rebuttals to first-round reviews under tight word limits.

| Skill | Description |
|-------|-------------|
| **[paper-rebuttal](16-rebuttal/SKILL.md)** | Concise direct responses to reviewer concerns, posture selection, compression tactics |

### 17 - Revision

Handling full major-revision cycles (revised PDF + response doc + new experiments + artifact update).

| Skill | Description |
|-------|-------------|
| **[handling-major-revision](17-revision/SKILL.md)** | Response-doc structure, paper-edit discipline, diff-PDF generation, empirical follow-up patterns |

---

## Skill Structure

Each skill follows a consistent format:

```
skill-name/
├── SKILL.md                    # Quick reference (target ~200-500 lines)
│   ├── Metadata (name, description, version)
│   ├── When to use this skill
│   ├── Quick patterns & examples
│   └── Links to references
│
├── references/                 # Deep documentation (optional, target where useful)
│   ├── README.md
│   ├── api.md                 # API reference
│   ├── tutorials.md           # Step-by-step guides
│   └── releases.md            # Version history
│
├── scripts/                    # Helper scripts (optional)
└── templates/                  # Code templates (optional)
```

<details>
<summary><b>Quality Targets</b></summary>

- SKILL.md focused (~200–500 lines), with the deeper material in linked reference files where useful
- Reference material drawn from official sources where useful
- Code examples with language tags
- Links to upstream docs for tools/datasets discussed

</details>

## Roadmap

The roadmap covers additional skills across the SE research lifecycle; coverage will grow incrementally.

### Phase 1 (Current): Core Analysis Tools
- [x] Program analysis (tree-sitter); CodeQL, Joern planned
- [x] Bug detection (Defects4J); BugsInPy, GumTree planned
- [ ] Software testing (AFL++, EvoSuite, mutation testing)

### Phase 2: AI/ML for SE
- [ ] Code models (CodeBERT, GraphCodeBERT, UniXcoder)
- [ ] LLM evaluation (HumanEval, MBPP, CrossCodeEval)
- [ ] Code generation (StarCoder, CodeLlama fine-tuning)

### Phase 3: Empirical & MSR
- [ ] Mining tools (PyGithub, GHTorrent)
- [ ] Statistical methods (effect sizes, meta-analysis)
- [ ] Survey design and analysis

### Phase 4: Specialized Domains
- [ ] Security analysis (Semgrep, vulnerability datasets)
- [ ] Dependency management (ecosystem analysis)
- [ ] DevOps research (CI/CD mining)

## Repository Structure

```
SE-research-SKILLs/
├── README.md                    ← You are here
├── CLAUDE.md                    ← Claude Code guidance
├── CONTRIBUTING.md              ← Contribution guide
├── 01-program-analysis/         ✅ published (tree-sitter)
├── 02-agent-construction/       ✅ published (react-langgraph)
├── 03-code-generation/          🚧 planned
├── 04-bug-detection-repair/     ✅ published (defects4j)
├── 05-mining-software-repos/    🚧 planned
├── 06-software-security/        🚧 planned
├── 07-dependency-management/    🚧 planned
├── 08-code-review-quality/      🚧 planned
├── 09-devops-cicd/              🚧 planned
├── 10-empirical-se/             🚧 planned
├── 11-experiment-design/        ✅ published (experiment-workflow)
├── 12-software-architecture/    🚧 planned
├── 13-human-aspects-se/         🚧 planned
├── 14-ai-ml-for-se/             🚧 planned
├── 15-se-paper-writing/         ✅ published
├── 16-rebuttal/                 ✅ published
└── 17-revision/                 ✅ published
```

## Use Cases

### For SE Researchers
"I need to evaluate my bug detection technique on standard benchmarks"
→ **[04-bug-detection-repair/defects4j/](04-bug-detection-repair/defects4j/)** — Java bug benchmark with test suites

### For PhD Students
"How do I write a paper for ICSE?"
→ **[15-se-paper-writing/](15-se-paper-writing/)** — Section-by-section guides, templates, reviewer criteria

### For Tool Builders
"I want to parse code in many languages"
→ **[01-program-analysis/tree-sitter/](01-program-analysis/tree-sitter/)** — Incremental parsing across languages

### For Empirical Researchers
"How do I design a controlled SE experiment?"
→ **[11-experiment-design/experiment-workflow/](11-experiment-design/experiment-workflow/)** — RQ formulation, sampling, validity threats

### For Agent Developers
"How do I build an LLM agent that uses tools?"
→ **[02-agent-construction/react-langgraph/](02-agent-construction/react-langgraph/)** — ReAct pattern, LangGraph state machines

## Key Datasets for SE Research

| Dataset | Domain | Size | URL |
|---------|--------|------|-----|
| **Defects4J** | Java bugs | 800+ bugs | [link](https://github.com/rjust/defects4j) |
| **BugsInPy** | Python bugs | 500+ bugs | [link](https://github.com/soarsmu/BugsInPy) |
| **CodeSearchNet** | Code search | 6M functions | [link](https://github.com/github/CodeSearchNet) |
| **The Stack** | Pretraining | 6TB code | [link](https://huggingface.co/datasets/bigcode/the-stack) |
| **BigCloneBench** | Clone detection | 8M pairs | [link](https://github.com/clonebench/BigCloneBench) |
| **CVEfixes** | Vulnerabilities | 5K+ CVEs | [link](https://github.com/secureIT-project/CVEfixes) |
| **CoCoMIC** | Commits | 32K repos | [link](https://github.com/LoyolaAI/CoCoMIC) |

> **Dataset usage note:** Check each dataset's licence and opt-out policy before use. Some datasets (e.g., The Stack) require honouring author opt-outs and may have specific terms for commercial vs research use. The links above are for reference only; this library does not redistribute any dataset.

## Disclaimer

These skills produce code, analyses, experimental results, drafted manuscripts, automated rebuttals, generated patches, security findings, and other artefacts intended to support software-engineering research. The library and its authors make **no warranty** of correctness, completeness, fitness for purpose, or compliance with any policy, contract, licence, ethical guideline, or venue rule.

**Users assume all risk for the use of any artefact produced by these skills.** Before relying on an output for any consequential decision — publication, peer review, deployment, citation, security claim, code merge, commercial use, or downstream research — the user is responsible for **independently verifying** that the output is correct, original, properly attributed, and appropriate for its intended purpose. Generated content should be treated as a draft that requires human review, not as a finished result.

By using these skills you acknowledge and accept this risk.

## License

MIT License - See [LICENSE](LICENSE) for details.

**Note**: Individual skills may reference libraries with different licenses. Please check each project's license before use.

## Acknowledgments

Repository structure was inspired by the public [AI-research-SKILLs](https://github.com/zechenzhangAGI/AI-research-SKILLs) project (MIT-licensed); no code was copied. Thanks also to the broader software-engineering research community and the maintainers of the open-source tools this library refers to.

## Contributing

Contributions from the SE research community are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*Maintained for the SE research community.*
