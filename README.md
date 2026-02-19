# Software Engineering Research `Skills` Library

> **The most comprehensive open-source library of SE research engineering skills for AI agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<div align="center">

### **Skills Powering SE Research in 2026**

</div>

<details>
<summary><b>View All 15 Categories</b></summary>

<div align="center">

| | | |
|:---:|:---:|:---:|
| **Program Analysis** | **Software Testing** | **Code Generation** |
| **Bug Detection & Repair** | **Mining Software Repos** | **Software Security** |
| **Dependency Management** | **Code Review & Quality** | **DevOps & CI/CD** |
| **Empirical SE** | **Requirements Engineering** | **Software Architecture** |
| **Human Aspects of SE** | **AI/ML for SE** | **SE Paper Writing** |

</div>

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

| Skill | Description | Lines |
|-------|-------------|-------|
| **[tree-sitter](01-program-analysis/tree-sitter/)** | Fast incremental parsing for 100+ languages, AST manipulation, syntax highlighting | 450+ |
| **[CodeQL](01-program-analysis/codeql/)** | GitHub's semantic code analysis, query language for finding vulnerabilities | 400+ |
| **[Joern](01-program-analysis/joern/)** | Code property graph analysis, inter-procedural data flow | 350+ |
| **[WALA](01-program-analysis/wala/)** | IBM's static analysis for Java/JavaScript, call graph construction | 300+ |
| **[Soot](01-program-analysis/soot/)** | Java optimization framework, Jimple IR, points-to analysis | 350+ |

### 02 - Software Testing

Frameworks for test generation, fuzzing, and mutation testing.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[AFL++](02-software-testing/aflpp/)** | State-of-the-art fuzzer, coverage-guided, QEMU mode | 400+ |
| **[LibFuzzer](02-software-testing/libfuzzer/)** | In-process fuzzing, LLVM-based, corpus management | 300+ |
| **[pytest](02-software-testing/pytest/)** | Python testing framework, fixtures, parametrization | 350+ |
| **[mutation-testing](02-software-testing/mutation-testing/)** | PIT, mutmut, mutation score analysis | 300+ |
| **[EvoSuite](02-software-testing/evosuite/)** | Automated test generation for Java, search-based | 350+ |

### 03 - Code Generation

LLM-based code synthesis and evaluation.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[CodeLlama](03-code-generation/codellama/)** | Meta's code LLM, infilling, instruction-tuned variants | 400+ |
| **[StarCoder](03-code-generation/starcoder/)** | BigCode's open code LLM, 15B params, multi-language | 350+ |
| **[code-evaluation](03-code-generation/code-evaluation/)** | HumanEval, MBPP, pass@k metrics, execution-based eval | 400+ |
| **[copilot-evaluation](03-code-generation/copilot-evaluation/)** | Evaluating AI code assistants, productivity metrics | 300+ |

### 04 - Bug Detection & Repair

Automated program repair and bug localization.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[Defects4J](04-bug-detection-repair/defects4j/)** | Java bug benchmark, 800+ real bugs, test suites | 400+ |
| **[BugsInPy](04-bug-detection-repair/bugsinpy/)** | Python bug benchmark, 500+ bugs, pytest integration | 300+ |
| **[GumTree](04-bug-detection-repair/gumtree/)** | AST differencing, edit scripts, code change analysis | 350+ |
| **[repair-llm](04-bug-detection-repair/repair-llm/)** | LLM-based program repair, few-shot, chain-of-thought | 400+ |

### 05 - Mining Software Repositories

Tools for large-scale repository analysis.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[PyGithub](05-mining-software-repos/pygithub/)** | GitHub API wrapper, repository mining, rate limiting | 350+ |
| **[GHTorrent](05-mining-software-repos/ghtorrent/)** | GitHub event archive, MongoDB/MySQL, historical data | 300+ |
| **[SourcererCC](05-mining-software-repos/sourcerercc/)** | Large-scale clone detection, token-based, scalable | 350+ |
| **[RepoReapers](05-mining-software-repos/reporeapers/)** | Repository quality scoring, filtering engineered projects | 250+ |

### 06 - Software Security

Vulnerability detection and security analysis.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[Semgrep](06-software-security/semgrep/)** | Lightweight static analysis, custom rules, CI integration | 400+ |
| **[Snyk](06-software-security/snyk/)** | Dependency vulnerability scanning, fix suggestions | 300+ |
| **[CVEfixes](06-software-security/cvefixes/)** | Vulnerability dataset, 5K+ CVEs, fix commits | 300+ |
| **[CodeBERT-vuln](06-software-security/codebert-vuln/)** | Neural vulnerability detection, fine-tuning | 350+ |

### 07 - Dependency Management

Package managers and dependency resolution.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[pip-resolver](07-dependency-management/pip-resolver/)** | Python dependency resolution, version conflicts | 400+ |
| **[npm-analysis](07-dependency-management/npm-analysis/)** | npm ecosystem analysis, dependency graphs | 300+ |
| **[cargo-deps](07-dependency-management/cargo-deps/)** | Rust dependency analysis, feature flags | 300+ |
| **[dependency-graphs](07-dependency-management/dependency-graphs/)** | Cross-ecosystem dependency visualization | 350+ |

### 08 - Code Review & Quality

Code quality analysis and review automation.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[SonarQube](08-code-review-quality/sonarqube/)** | Code quality platform, rules, quality gates | 400+ |
| **[code-smells](08-code-review-quality/code-smells/)** | Detection tools, refactoring suggestions | 350+ |
| **[review-automation](08-code-review-quality/review-automation/)** | Automated code review, bot integration | 300+ |

### 09 - DevOps & CI/CD

Build systems and deployment pipelines.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[github-actions](09-devops-cicd/github-actions/)** | CI/CD workflows, matrix builds, artifacts | 400+ |
| **[docker-research](09-devops-cicd/docker-research/)** | Container analysis, Dockerfile mining | 300+ |
| **[build-systems](09-devops-cicd/build-systems/)** | Make, CMake, Gradle analysis | 350+ |

### 10 - Empirical SE

Methods for empirical software engineering research.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[statistical-analysis](10-empirical-se/statistical-analysis/)** | Effect sizes, significance tests, Cliff's delta | 400+ |
| **[survey-design](10-empirical-se/survey-design/)** | Developer surveys, sampling, validity threats | 350+ |
| **[replication-studies](10-empirical-se/replication-studies/)** | Replication packages, artifact evaluation | 300+ |
| **[qualitative-methods](10-empirical-se/qualitative-methods/)** | Coding, grounded theory, thematic analysis | 300+ |

### 11 - Requirements Engineering

Requirements analysis and traceability.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[nlp-requirements](11-requirements-engineering/nlp-requirements/)** | NLP for requirements, ambiguity detection | 350+ |
| **[traceability](11-requirements-engineering/traceability/)** | Requirements-to-code tracing, link recovery | 300+ |

### 12 - Software Architecture

Design patterns and architectural analysis.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[architecture-recovery](12-software-architecture/architecture-recovery/)** | Architecture extraction from code | 350+ |
| **[microservices-analysis](12-software-architecture/microservices-analysis/)** | Service decomposition, API analysis | 300+ |
| **[design-patterns](12-software-architecture/design-patterns/)** | Pattern detection, anti-patterns | 300+ |

### 13 - Human Aspects of SE

Developer productivity and code comprehension.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[developer-productivity](13-human-aspects-se/developer-productivity/)** | SPACE framework, metrics, studies | 350+ |
| **[code-comprehension](13-human-aspects-se/code-comprehension/)** | Eye-tracking, cognitive load, studies | 300+ |

### 14 - AI/ML for SE

Machine learning techniques for SE tasks.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[CodeBERT](14-ai-ml-for-se/codebert/)** | Pre-trained model for code, clone detection, search | 400+ |
| **[GraphCodeBERT](14-ai-ml-for-se/graphcodebert/)** | Data flow-aware code model | 350+ |
| **[code-embeddings](14-ai-ml-for-se/code-embeddings/)** | Code2vec, doc2vec, semantic similarity | 350+ |
| **[llm4code-eval](14-ai-ml-for-se/llm4code-eval/)** | Evaluating LLMs on SE tasks, benchmarks | 400+ |

### 15 - SE Paper Writing

Writing for top-tier SE venues.

| Skill | Description | Lines |
|-------|-------------|-------|
| **[se-paper-writing](15-se-paper-writing/)** | ICSE, FSE, ASE paper writing, LaTeX templates, reviewing | 600+ |

---

## Skill Structure

Each skill follows a battle-tested format for maximum usefulness:

```
skill-name/
├── SKILL.md                    # Quick reference (200-500 lines)
│   ├── Metadata (name, description, version)
│   ├── When to use this skill
│   ├── Quick patterns & examples
│   └── Links to references
│
├── references/                 # Deep documentation (300KB+)
│   ├── README.md              # From GitHub/official docs
│   ├── api.md                 # API reference
│   ├── tutorials.md           # Step-by-step guides
│   ├── issues.md              # Real GitHub issues & solutions
│   └── releases.md            # Version history
│
├── scripts/                    # Helper scripts (optional)
└── templates/                  # Code templates (optional)
```

<details>
<summary><b>Quality Standards</b></summary>

- 300KB+ documentation from official sources
- Real GitHub issues & solutions (when available)
- Code examples with language detection
- Version history & breaking changes
- Links to official docs

</details>

## Roadmap

We're building towards 60+ comprehensive skills across the full SE research lifecycle.

### Phase 1 (Current): Core Analysis Tools
- [x] Program analysis (tree-sitter, CodeQL, Joern)
- [x] Software testing (AFL++, EvoSuite, mutation testing)
- [x] Bug detection (Defects4J, BugsInPy, GumTree)

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
├── docs/                        ← Additional documentation
├── demos/                       ← Demo gallery
├── 01-program-analysis/         (5 skills planned)
├── 02-software-testing/         (5 skills planned)
├── 03-code-generation/          (4 skills planned)
├── 04-bug-detection-repair/     (4 skills planned)
├── 05-mining-software-repos/    (4 skills planned)
├── 06-software-security/        (4 skills planned)
├── 07-dependency-management/    (4 skills planned)
├── 08-code-review-quality/      (3 skills planned)
├── 09-devops-cicd/              (3 skills planned)
├── 10-empirical-se/             (4 skills planned)
├── 11-requirements-engineering/ (2 skills planned)
├── 12-software-architecture/    (3 skills planned)
├── 13-human-aspects-se/         (2 skills planned)
├── 14-ai-ml-for-se/             (4 skills planned)
└── 15-se-paper-writing/         (1 skill - comprehensive)
```

## Use Cases

### For SE Researchers
"I need to evaluate my bug detection tool on standard benchmarks"
→ **04-bug-detection-repair/defects4j/** - 800+ real Java bugs with test suites

### For PhD Students
"How do I write a paper for ICSE?"
→ **15-se-paper-writing/** - Templates, examples, reviewing criteria

### For Tool Builders
"I want to build a static analyzer"
→ **01-program-analysis/tree-sitter/** - Fast parsing for 100+ languages

### For Empirical Researchers
"How do I analyze my experiment results?"
→ **10-empirical-se/statistical-analysis/** - Effect sizes, significance tests

### For Security Researchers
"I need to detect vulnerabilities in code"
→ **06-software-security/semgrep/** - Custom rules, CI integration

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

## License

MIT License - See [LICENSE](LICENSE) for details.

**Note**: Individual skills may reference libraries with different licenses. Please check each project's license before use.

## Acknowledgments

Built with inspiration from:
- [AI-research-SKILLs](https://github.com/zechenzhangAGI/AI-research-SKILLs) by Orchestra Research
- The Software Engineering research community
- Open source SE tools maintainers

## Contributing

We welcome contributions from the SE research community! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*Maintained for the SE research community. Star if you find it useful!*
