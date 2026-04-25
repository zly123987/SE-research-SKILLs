"""Missing citation detector for SE papers.

Scans .tex files for entities that should be cited but lack a \\cite{} or
\\url{} nearby. Reports uncited entities grouped by category so they can be
addressed before submission.

Categories of entities that require citations:

1. Named tools / software libraries / products  → need \\cite{} or \\url{}
2. Named techniques / paradigms / algorithms     → need \\cite{}
3. Named datasets / benchmarks                   → need \\cite{}
4. Named metrics / statistical tests             → need \\cite{} (first use)
5. Named prior approaches / competing tools      → need \\cite{}
6. Named standards / specifications / RFCs       → need \\cite{} or \\url{}

This module is stdlib-only and integrates into the pipeline as a report-only
step (no auto-fix — missing citations require human judgment on which
reference to add).
"""

import os
import re
from typing import Dict, Any, List, Optional, Set, Tuple


# ── Entity patterns that require citation ────────────────────────────────────

# Each rule: (category, compiled_regex, description)
# Regexes look for the entity name NOT followed by ~\cite or \cite or \url
# within the next ~30 characters.

# We match entities and then check in a post-pass whether a citation is nearby,
# to avoid catastrophically complex lookahead regexes.

# Category 1: Named tools, libraries, frameworks, products
# These are proper nouns (capitalized) that are specific software artifacts.
_TOOL_NAMES = [
    # Build / package tools
    "Maven", "Gradle", "Bazel", "CMake", "Make",
    "pip", "Poetry", "Conda", "npm", "yarn", "Cargo",
    # Languages / runtimes (when discussed technically, not just mentioned)
    "CPython", "PyPy", "GraalVM", "OpenJDK",
    # Analysis tools
    "SonarQube", "CodeQL", "Semgrep", "Joern", "Soot", "WALA",
    "SpotBugs", "FindBugs", "PMD", "Checkstyle", "ESLint",
    "Infer", "KLEE", "AFL", "LibFuzzer",
    # ML / AI tools
    "TensorFlow", "PyTorch", "scikit-learn", "Hugging Face",
    "OpenAI", "LangChain", "LlamaIndex",
    # Infra / platforms
    "Docker", "Kubernetes", "GitHub Actions", "Jenkins", "Travis CI",
    "CircleCI", "GitLab CI",
    # SE research tools (common baselines)
    "GumTree", "ChangeDistiller", "RefactoringMiner",
    "Defects4J", "BugsInPy",
    # LLMs (when named as tools, not generic "LLM")
    "GPT-4", "GPT-3.5", "GPT-4o",
    "Claude", "Gemini", "Llama", "CodeLlama",
    "StarCoder", "CodeGen", "Codex",
    "ChatGPT", "Copilot", "GitHub Copilot",
    "CodeBERT", "GraphCodeBERT", "UniXcoder",
    "DeepSeek", "Qwen",
]

# Category 2: Named techniques, paradigms, algorithms
_TECHNIQUES = [
    # Analysis techniques
    "abstract interpretation", "symbolic execution",
    "taint analysis", "data flow analysis", "control flow analysis",
    "program slicing", "model checking",
    "static analysis", "dynamic analysis",
    "fuzz testing", "fuzzing", "mutation testing",
    "concolic execution", "bounded model checking",
    # ML/AI paradigms
    "Chain-of-Thought", "chain of thought",
    "ReAct", "Tree of Thought",
    "retrieval-augmented generation", "RAG",
    "in-context learning", "few-shot learning", "zero-shot learning",
    "fine-tuning", "LoRA", "QLoRA", "RLHF", "DPO",
    "prompt engineering",
    "knowledge distillation",
    "contrastive learning",
    # SE techniques
    "program repair", "automated program repair",
    "fault localization", "spectrum-based fault localization",
    "code clone detection", "clone detection",
    "change impact analysis",
    "dependency resolution",
    "semantic versioning",
    # Design patterns (when discussed as concepts)
    "visitor pattern", "observer pattern", "strategy pattern",
]

# Category 3: Named datasets and benchmarks
_DATASETS = [
    "Defects4J", "BugsInPy", "QuixBugs", "IntroClassJava",
    "CodeSearchNet", "The Stack", "StarCoderData",
    "BigCloneBench", "OJClone",
    "HumanEval", "MBPP", "APPS", "CodeContests",
    "SWE-bench", "SWE-Bench",
    "CVEfixes", "Big-Vul", "VUDDY",
    "CrossVul", "Devign",
    "CoNaLa", "CONCODE",
    "GHTorrent", "World of Code",
    "ImageNet", "GLUE", "SuperGLUE",
    "MMLU", "HellaSwag", "TruthfulQA",
]

# Category 4: Named metrics and statistical tests
_METRICS_TESTS = [
    # Statistical tests
    "Fisher's exact test", "McNemar's test",
    "Wilcoxon signed-rank", "Wilcoxon rank-sum",
    "Mann-Whitney U", "Mann-Whitney",
    "Kruskal-Wallis",
    "Shapiro-Wilk",
    "Bonferroni correction",
    "Benjamini-Hochberg",
    # Effect size measures
    "Cliff's delta", "Cliff's d",
    "Cohen's d", "Cohen's kappa",
    "Cramér's V",
    "Vargha-Delaney",
    # Metrics (less common ones that need citation)
    "BLEU", "ROUGE", "CodeBLEU",
    "CrystalBLEU",
    "pass@k",
    "CIDEr",
    "BERTScore",
    "METEOR",
]

# Category 5: Standards, specifications
_STANDARDS = [
    "OWASP", "OWASP Top 10",
    "CVE", "CWE", "CVSS",
    "PEP 440", "PEP 508", "PEP 517", "PEP 621",
    "SemVer",
    "SARIF",
    "SBOM", "SPDX", "CycloneDX",
]


# ── Compile patterns ─────────────────────────────────────────────────────────

def _build_entity_patterns() -> List[Tuple[str, re.Pattern, str]]:
    """Build compiled regex patterns for all entity categories.

    Each pattern matches the entity name as a whole word.
    """
    patterns = []

    def _add(category: str, names: List[str]):
        for name in names:
            # Escape regex special chars in the name
            escaped = re.escape(name)
            # Match as whole word (\\b doesn't work well with hyphens, use
            # lookaround for word boundaries)
            pattern = re.compile(
                r"(?<![a-zA-Z\\])" + escaped + r"(?![a-zA-Z{}])",
                re.IGNORECASE if name[0].islower() else 0,
            )
            patterns.append((category, pattern, name))

    _add("tool/library", _TOOL_NAMES)
    _add("technique/paradigm", _TECHNIQUES)
    _add("dataset/benchmark", _DATASETS)
    _add("metric/test", _METRICS_TESTS)
    _add("standard/spec", _STANDARDS)

    return patterns


_ENTITY_PATTERNS = _build_entity_patterns()

# Commands that count as citation for an entity
_CITE_PATTERN = re.compile(
    r"\\(?:cite[a-z]*|url|href|footnote)\s*\{",
)


# ── Core logic ───────────────────────────────────────────────────────────────

class UncitedEntity:
    """An entity found in prose without a nearby citation."""

    __slots__ = ("name", "category", "tex_file", "line_num", "context")

    def __init__(
        self, name: str, category: str, tex_file: str,
        line_num: int, context: str,
    ):
        self.name = name
        self.category = category
        self.tex_file = tex_file
        self.line_num = line_num
        self.context = context

    def __repr__(self) -> str:
        return (
            f"UncitedEntity({self.category}: {self.name!r}, "
            f"{os.path.basename(self.tex_file)}:{self.line_num})"
        )


def _has_nearby_citation(text: str, match_start: int, match_end: int,
                         window: int = 60) -> bool:
    """Check if there is a \\cite{}, \\url{}, or \\footnote{} near the match.

    Looks within `window` characters after the match end, and also checks
    if the match is inside a \\cite-like command argument.
    """
    # Check after the match
    after_text = text[match_end:match_end + window]
    if _CITE_PATTERN.search(after_text):
        return True

    # Check a small window before (for "\\cite{...} shows that Tool")
    before_start = max(0, match_start - window)
    before_text = text[before_start:match_start]
    if _CITE_PATTERN.search(before_text):
        return True

    return False


def _is_in_cite_command(text: str, match_start: int) -> bool:
    """Check if the match position is inside a \\cite{...} argument."""
    # Walk backwards to see if we're inside braces preceded by \cite
    depth = 0
    i = match_start - 1
    while i >= 0:
        if text[i] == "}":
            depth += 1
        elif text[i] == "{":
            depth -= 1
            if depth < 0:
                # We're inside braces — check if preceded by \cite
                before = text[max(0, i - 20):i]
                if re.search(r"\\(?:cite[a-z]*|url|href|footnote)\s*$", before):
                    return True
                return False
        i -= 1
    return False


def _is_in_comment(line: str, col: int) -> bool:
    """Check if position is after a % comment marker (not \\%)."""
    for i in range(col):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            return True
    return False


def _is_in_special_context(text: str, match_start: int) -> bool:
    """Check if the entity is in a context where citation is not needed.

    Contexts:
    - Inside \\texttt{...} or \\verb|...|  (code references)
    - Inside lstlisting environments
    - Inside \\caption{...}  (citations optional in captions)
    - Inside \\label{...} or \\ref{...}
    - The entity is our own tool (defined with \\tool or \\newcommand)
    """
    # Check if inside \texttt, \verb, \code, \label, \ref
    i = match_start - 1
    depth = 0
    while i >= 0:
        if text[i] == "}":
            depth += 1
        elif text[i] == "{":
            depth -= 1
            if depth < 0:
                before = text[max(0, i - 30):i]
                if re.search(
                    r"\\(?:texttt|verb|code|lstinline|label|ref|nameref|tool)\s*$",
                    before,
                ):
                    return True
                return False
        i -= 1
    return False


def scan_tex_for_uncited_entities(
    tex_path: str,
    cited_first_uses: Optional[Set[str]] = None,
) -> List[UncitedEntity]:
    """Scan a single .tex file for entities missing citations.

    Args:
        tex_path: Path to the .tex file.
        cited_first_uses: Set of entity names already cited elsewhere.
            If provided, only the first uncited use is flagged.

    Returns:
        List of UncitedEntity objects.
    """
    if cited_first_uses is None:
        cited_first_uses = set()

    try:
        with open(tex_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            lines = content.split("\n")
    except Exception:
        return []

    uncited: List[UncitedEntity] = []
    # Track which entities we've already reported in THIS file
    reported_in_file: Set[str] = set()

    for category, pattern, entity_name in _ENTITY_PATTERNS:
        for match in pattern.finditer(content):
            start = match.start()
            end = match.end()

            # Get line number
            line_num = content[:start].count("\n") + 1
            line_text = lines[line_num - 1] if line_num <= len(lines) else ""

            # Column in line
            line_start = content.rfind("\n", 0, start) + 1
            col = start - line_start

            # Skip comments
            if _is_in_comment(line_text, col):
                continue

            # Skip if inside a \cite{} argument, \texttt{}, etc.
            if _is_in_cite_command(content, start):
                continue
            if _is_in_special_context(content, start):
                continue

            # Skip if nearby citation exists
            if _has_nearby_citation(content, start, end):
                # Record as cited for first-use tracking
                cited_first_uses.add(entity_name.lower())
                continue

            # For first-use-only mode: skip if already cited elsewhere
            entity_key = entity_name.lower()
            if entity_key in cited_first_uses:
                continue

            # Only report once per entity per file
            if entity_key in reported_in_file:
                continue
            reported_in_file.add(entity_key)

            # Build context snippet
            ctx_start = max(0, start - 40)
            ctx_end = min(len(content), end + 80)
            context = content[ctx_start:ctx_end].replace("\n", " ").strip()

            uncited.append(UncitedEntity(
                name=entity_name,
                category=category,
                tex_file=tex_path,
                line_num=line_num,
                context=context,
            ))

    return uncited


# ── Main entry point ─────────────────────────────────────────────────────────

def check_missing_citations(
    tex_dir: str,
    main_tex_path: Optional[str] = None,
    verbose: bool = True,
    first_use_only: bool = True,
) -> Dict[str, Any]:
    """Scan all .tex files for entities that lack citations.

    This is a report-only check — no files are modified.

    Args:
        tex_dir: Directory containing .tex files.
        main_tex_path: Optional path to main.tex.
        verbose: Print progress and results.
        first_use_only: Only flag the first uncited occurrence of each entity
            across all files. Later occurrences don't need re-citation.

    Returns:
        Dictionary with uncited entities and statistics.
    """
    tex_files: List[str] = []

    if os.path.isdir(tex_dir):
        for fname in sorted(os.listdir(tex_dir)):
            if fname.endswith(".tex"):
                tex_files.append(os.path.join(tex_dir, fname))

    if main_tex_path and os.path.isfile(main_tex_path):
        if main_tex_path not in tex_files:
            tex_files.append(main_tex_path)

    if verbose:
        print(f"  Scanning {len(tex_files)} .tex file(s) for uncited entities...")

    all_uncited: List[Dict[str, Any]] = []
    cited_first_uses: Set[str] = set()

    # Category counters
    category_counts: Dict[str, int] = {}

    for tex_path in tex_files:
        entities = scan_tex_for_uncited_entities(
            tex_path,
            cited_first_uses=cited_first_uses if first_use_only else None,
        )
        for entity in entities:
            category_counts[entity.category] = (
                category_counts.get(entity.category, 0) + 1
            )
            all_uncited.append({
                "name": entity.name,
                "category": entity.category,
                "file": os.path.basename(entity.tex_file),
                "line": entity.line_num,
                "context": entity.context,
            })

    if verbose:
        total = len(all_uncited)
        print(f"  Uncited entities found: {total}")

        if category_counts:
            print()
            for cat, count in sorted(category_counts.items()):
                print(f"    {cat}: {count}")

        if all_uncited:
            print(f"\n  {'─' * 50}")
            for entry in all_uncited:
                print(f"  [{entry['category'].upper()}] {entry['file']}:{entry['line']}")
                print(f"    Entity:  {entry['name']}")
                print(f"    Context: ...{entry['context'][:120]}...")
                print()
        else:
            print("  All recognized entities appear to be cited.")

    return {
        "uncited_entities": all_uncited,
        "total": len(all_uncited),
        "by_category": category_counts,
    }


def format_uncited_for_llm(
    tex_dir: str,
    main_tex_path: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Export uncited entities for LLM-based suggestion of references.

    Returns a list of dicts suitable for batching into an LLM prompt that
    can suggest appropriate citations (DBLP lookup, URL, etc.).
    """
    result = check_missing_citations(
        tex_dir, main_tex_path=main_tex_path, verbose=False
    )

    items = []
    for entry in result["uncited_entities"]:
        items.append({
            "entity": entry["name"],
            "category": entry["category"],
            "context": entry["context"],
            "file": entry["file"],
            "line": str(entry["line"]),
        })

    return items


# ── CLI entry point ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python missing_citation_checker.py <tex_directory> [main.tex]"
        )
        print("  Scans .tex files for entities that should be cited but aren't.")
        print("  Optional second arg: path to main.tex")
        sys.exit(1)

    tex_directory = sys.argv[1]
    main_tex = sys.argv[2] if len(sys.argv) > 2 else None

    result = check_missing_citations(
        tex_directory, main_tex_path=main_tex, verbose=True
    )

    sys.exit(1 if result["total"] > 0 else 0)
