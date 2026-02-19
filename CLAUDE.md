# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Software Engineering Research Skills Library** - A comprehensive open-source library of SE research skills designed to enable AI agents to autonomously conduct software engineering research experiments. Each skill provides expert-level guidance (200-600 lines) with real code examples, troubleshooting guides, and production-ready workflows.

**Mission**: Enable AI agents to autonomously conduct SE research from hypothesis to experimental verification, covering program analysis, software testing, bug detection, code generation, and empirical studies for top-tier SE venues (ICSE, FSE, ASE, ISSTA, MSR, EMSE).

## Repository Architecture

### Directory Structure (Skills Across 15 Categories)

Skills are organized into numbered categories representing the SE research lifecycle:

- `01-program-analysis/` - Static/dynamic analysis (tree-sitter, CodeQL, Joern, WALA, Soot)
- `02-software-testing/` - Testing frameworks (AFL++, LibFuzzer, pytest, mutation testing)
- `03-code-generation/` - Code synthesis (CodeLlama, StarCoder, Copilot evaluation)
- `04-bug-detection-repair/` - APR tools (GumTree, Defects4J, RepairLLM)
- `05-mining-software-repos/` - MSR tools (PyGithub, GHTorrent, SourcererCC)
- `06-software-security/` - Security analysis (Semgrep, Snyk, SAST/DAST tools)
- `07-dependency-management/` - Package managers (pip, npm, cargo, dependency resolution)
- `08-code-review-quality/` - Code quality (SonarQube, code smell detection, review automation)
- `09-devops-cicd/` - Build systems (GitHub Actions, Docker, Kubernetes)
- `10-empirical-se/` - Empirical methods (survey design, statistical analysis, replication)
- `11-requirements-engineering/` - Requirements (traceability, NLP for requirements)
- `12-software-architecture/` - Architecture (design patterns, microservices, dependency analysis)
- `13-human-aspects-se/` - Human factors (developer productivity, code comprehension)
- `14-ai-ml-for-se/` - AI4SE tools (CodeBERT, GraphCodeBERT, LLM4Code evaluation)
- `15-se-paper-writing/` - Paper writing for ICSE, FSE, ASE, ISSTA, MSR

### Skill File Structure

Each skill follows a standardized format:
```
skill-name/
├── SKILL.md                    # Main guidance (200-600 lines with YAML frontmatter)
├── references/                 # Deep documentation (300KB+ target)
│   ├── README.md              # From official docs
│   ├── api.md                 # API reference
│   ├── tutorials.md           # Step-by-step guides
│   ├── issues.md              # Real GitHub issues & solutions
│   └── releases.md            # Version history
├── scripts/                    # Helper scripts (optional)
├── templates/                  # Code templates (optional)
└── examples/                   # Example implementations (optional)
```

## Skill Quality Standards

### YAML Frontmatter Requirements (CRITICAL)

All `SKILL.md` files MUST include YAML frontmatter with these exact fields:

```yaml
---
name: skill-name-here              # kebab-case, no quotes, gerund form preferred
description: Third-person description of what AND when to use this skill  # No quotes, max 1024 chars
version: 1.0.0                     # Semantic versioning
author: SE Research Skills         # Standard author
license: MIT                       # Standard license
tags: [Tag One, Tag Two]          # Title Case (except UPPERCASE acronyms like AST, CFG, APR)
dependencies: [pkg>=1.0.0]         # Optional, with version constraints
---
```

**Critical Rules**:
- `name`: Use gerund form (e.g., `parsing-code`, `analyzing-programs`, `fuzzing-binaries`)
- `description`: Third person ("Provides guidance for..."), include WHAT it does AND WHEN to use it
- `tags`: Title Case for regular words, UPPERCASE for acronyms (AST, CFG, PDG, APR, MSR)
- No quotes around any field values (except in arrays)
- Dependencies should include version constraints: `tree-sitter>=0.20.0`

### Content Quality Standards

**Core Requirements** (based on Anthropic official best practices):
- ✅ SKILL.md body: **200-500 lines** (under 500 lines is critical for performance)
- ✅ Progressive disclosure: SKILL.md as overview, details in separate reference files
- ✅ Workflows with copy-paste checklists for complex tasks
- ✅ "When to use vs alternatives" guidance section
- ✅ Common issues section with solutions
- ✅ Concise content: assume Claude is smart, no over-explaining basics
- ✅ Code examples with language detection (```python, ```bash, etc.)
- ✅ References ONE level deep from SKILL.md (no nested references)

**Gold Standard** (aim for this):
- ✅ 2-3 complete workflows with step-by-step checklists
- ✅ Reference files for advanced topics (one level deep)
- ✅ Feedback loops (validate → fix → repeat) for quality-critical operations
- ✅ Consistent terminology throughout
- ✅ Concrete input/output examples
- ✅ Real GitHub issues with solutions (when available)

**NOT Acceptable**:
- ❌ SKILL.md over 500 lines (split into reference files instead)
- ❌ Over-explaining basics that Claude already knows
- ❌ First-person descriptions ("I can help you...")
- ❌ Vague skill names ("helper", "utils", "tools")
- ❌ Nested references (SKILL.md → ref1.md → ref2.md)
- ❌ Missing workflows with checklists for complex tasks

## SE Research Context

### Top-Tier SE Venues

| Venue | Focus | Deadline Pattern |
|-------|-------|------------------|
| **ICSE** | Flagship, broad SE | August (main), varies (tracks) |
| **FSE/ESEC** | Foundations, empirical | March/April |
| **ASE** | Automation in SE | May |
| **ISSTA** | Software testing | January |
| **MSR** | Mining repositories | January |
| **EMSE** | Journal, empirical | Rolling |
| **TSE** | Journal, broad SE | Rolling |

### Common SE Research Patterns

1. **Tool Paper**: New technique + implementation + evaluation
2. **Empirical Study**: Large-scale analysis of existing artifacts
3. **Benchmark Paper**: New dataset or benchmark suite
4. **Replication Study**: Reproduce and extend prior work
5. **Experience Paper**: Industry practice or lessons learned

### Key Datasets for SE Research

| Dataset | Purpose | Size |
|---------|---------|------|
| **Defects4J** | Java bugs with tests | 800+ bugs |
| **BugsInPy** | Python bugs | 500+ bugs |
| **CodeSearchNet** | Code search/generation | 6M functions |
| **The Stack** | Code pretraining | 6TB code |
| **BigCloneBench** | Clone detection | 8M clone pairs |
| **CVEfixes** | Security vulnerabilities | 5K+ CVEs |

## Development Workflow

### Adding a New Skill

1. **Choose skill from roadmap** (see README.md)
2. **Create directory structure** in appropriate category (01-15)
3. **Write SKILL.md** with YAML frontmatter following standards above
4. **Add reference documentation** (target 300KB+ from official sources)
5. **Validate quality**:
   - Check SKILL.md has YAML frontmatter
   - Verify SKILL.md is 200-500 lines
   - Ensure code blocks have language tags
   - Confirm references are one level deep from SKILL.md
   - Check documentation size: `du -sh skill-name/references/`
6. **Test the skill** with real use cases before submitting

### Quality Validation Commands

```bash
# Check YAML frontmatter exists
head -20 skill-name/SKILL.md

# Verify SKILL.md line count (target 200-500 lines)
wc -l skill-name/SKILL.md

# Check documentation size (target 300KB+)
du -sh skill-name/references/

# Verify code blocks have language tags
grep -A 1 '```' skill-name/SKILL.md | head -20

# Validate YAML frontmatter syntax
python -c "import yaml; yaml.safe_load(open('skill-name/SKILL.md').read().split('---')[1])"
```

## Key Files

- **README.md** - Project overview, all skills listed with descriptions
- **CONTRIBUTING.md** - Complete contribution guidelines and quality standards
- **docs/SKILL_TEMPLATE.md** - Copy-paste scaffold for new skills

## Important Conventions

### Naming Conventions

- **Skill names**: Use gerund form (verb + -ing) in kebab-case: `parsing-code`, `fuzzing-binaries`, `analyzing-dependencies`
- **Tags**: Title Case for words, UPPERCASE for acronyms (AST, CFG, PDG, APR, MSR, SAST, DAST)
- **Descriptions**: Third person, include what AND when to use

### Code Examples

Always use language detection in code blocks:
```python
# Good - has language tag
import tree_sitter
```

NOT:
```
# Bad - no language tag
import tree_sitter
```

### Progressive Disclosure Pattern

SKILL.md should link directly to reference files (one level deep):

```markdown
## Advanced Features

**API Reference**: See [references/api.md](references/api.md)
**Troubleshooting**: See [references/issues.md](references/issues.md)
```

## Philosophy

**Quality over Quantity**: This library maintains high standards by:
- Requiring 200-500 line SKILL.md files (focused, actionable guidance)
- Including 300KB+ documentation from official sources
- Providing real GitHub issues with solutions
- Following Anthropic's official best practices for skills
- Testing skills with real use cases before inclusion

Each skill represents expert-level knowledge distilled into a format optimized for AI agent consumption, specifically targeting SE research workflows.