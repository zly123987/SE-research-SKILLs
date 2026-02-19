---
name: evaluating-with-defects4j
description: Standard benchmark of real-world Java bugs for evaluating bug detection and automated program repair tools. Use when evaluating APR techniques, bug localization methods, or testing-related research. Contains 800+ bugs from 17 open-source projects with test suites.
version: 1.0.0
author: SE Research Skills
license: MIT
tags: [Bug Detection, Automated Program Repair, APR, Benchmark, Java, Testing]
dependencies: [java>=8, git, svn, perl]
---

# Defects4J: Real-World Java Bug Benchmark

Defects4J is the standard benchmark for evaluating automated program repair (APR) and bug detection tools in SE research. It contains 835+ real bugs from 17 open-source Java projects, each with a test suite that exposes the bug.

## When to Use Defects4J

**Use Defects4J when:**
- Evaluating automated program repair (APR) tools
- Benchmarking bug localization techniques
- Testing fault localization methods
- Comparing bug detection approaches
- Need reproducible Java bug experiments

**Consider alternatives when:**
- Working with Python → Use BugsInPy
- Need security vulnerabilities → Use CVEfixes
- Need multi-language bugs → Use ManyBugs/IntroClass
- Need C/C++ bugs → Use ManyBugs or Codeflaws

## Quick Start

### Installation

```bash
# Clone Defects4J
git clone https://github.com/rjust/defects4j.git
cd defects4j

# Initialize (downloads project repos, ~30 min)
./init.sh

# Add to PATH
export PATH=$PATH:$(pwd)/framework/bin

# Verify installation
defects4j info -p Lang
```

### Basic Usage: Checkout a Bug

```bash
# Checkout buggy version of project
defects4j checkout -p Lang -v 1b -w /tmp/Lang_1_buggy

# Checkout fixed version
defects4j checkout -p Lang -v 1f -w /tmp/Lang_1_fixed

# Run tests on buggy version (should fail)
cd /tmp/Lang_1_buggy
defects4j test
```

---

## Core Workflows

### Workflow 1: Evaluate an APR Tool

```
APR Evaluation Checklist:
- [ ] Step 1: Select bug subset (e.g., Defects4J v1.2 or v2.0)
- [ ] Step 2: For each bug, checkout buggy version
- [ ] Step 3: Run bug localization (or use provided fault locations)
- [ ] Step 4: Apply APR tool to generate patches
- [ ] Step 5: Validate patches with test suite
- [ ] Step 6: Check patch correctness (plausible vs correct)
- [ ] Step 7: Report metrics (# correct, # plausible, time)
```

**Step 1: Get Bug List**

```bash
# List all bugs in a project
defects4j bids -p Lang

# Get info about a specific bug
defects4j info -p Lang -b 1
```

**Step 2-3: Setup Evaluation Script**

```python
#!/usr/bin/env python3
"""Evaluate APR tool on Defects4J bugs."""
import subprocess
import json
from pathlib import Path

DEFECTS4J = "defects4j"
WORK_DIR = Path("/tmp/d4j_eval")

def checkout_bug(project: str, bug_id: int, version: str = "b") -> Path:
    """Checkout a buggy or fixed version."""
    work_path = WORK_DIR / f"{project}_{bug_id}_{version}"
    if work_path.exists():
        return work_path

    cmd = [DEFECTS4J, "checkout",
           "-p", project,
           "-v", f"{bug_id}{version}",
           "-w", str(work_path)]
    subprocess.run(cmd, check=True)
    return work_path

def get_fault_locations(project: str, bug_id: int) -> list[dict]:
    """Get fault locations for a bug."""
    work_path = checkout_bug(project, bug_id, "b")

    # Get modified classes
    cmd = [DEFECTS4J, "export", "-p", "classes.modified", "-w", str(work_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    classes = result.stdout.strip().split("\n")

    # Get source directory
    cmd = [DEFECTS4J, "export", "-p", "dir.src.classes", "-w", str(work_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    src_dir = result.stdout.strip()

    return [{"class": c, "src_dir": src_dir} for c in classes]

def run_tests(work_path: Path) -> dict:
    """Run tests and return results."""
    cmd = [DEFECTS4J, "test", "-w", str(work_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Parse test results
    failing_tests = []
    for line in result.stdout.split("\n"):
        if line.startswith("Failing tests:"):
            count = int(line.split(":")[1].strip())
        elif line.strip().startswith("-"):
            failing_tests.append(line.strip()[2:])

    return {
        "exit_code": result.returncode,
        "failing_count": len(failing_tests),
        "failing_tests": failing_tests,
    }
```

**Step 4-5: Validate Patches**

```python
def validate_patch(project: str, bug_id: int, patch_file: Path) -> dict:
    """Apply patch and validate with tests."""
    # Checkout fresh buggy version
    work_path = checkout_bug(project, bug_id, "b")

    # Apply patch
    cmd = ["patch", "-p1", "-i", str(patch_file)]
    result = subprocess.run(cmd, cwd=work_path, capture_output=True)

    if result.returncode != 0:
        return {"status": "patch_failed", "error": result.stderr.decode()}

    # Run tests
    test_result = run_tests(work_path)

    if test_result["failing_count"] == 0:
        return {"status": "plausible", "test_result": test_result}
    else:
        return {"status": "failing", "test_result": test_result}
```

**Step 6: Check Correctness**

```python
def check_semantic_correctness(project: str, bug_id: int, patch_file: Path) -> bool:
    """
    Check if patch is semantically equivalent to developer fix.
    NOTE: This requires manual inspection or additional tooling.
    """
    # Get developer fix
    buggy_path = checkout_bug(project, bug_id, "b")
    fixed_path = checkout_bug(project, bug_id, "f")

    # Compare with generated patch
    # Options:
    # 1. Manual inspection
    # 2. Semantic diff tools
    # 3. Additional test suite
    # 4. Symbolic execution

    # For research, typically requires manual labeling
    return None  # Requires human verification
```

---

### Workflow 2: Fault Localization Evaluation

```
Fault Localization Checklist:
- [ ] Step 1: Checkout buggy version
- [ ] Step 2: Collect test coverage (JaCoCo/GZoltar)
- [ ] Step 3: Run fault localization technique
- [ ] Step 4: Compare with ground truth (modified lines)
- [ ] Step 5: Compute metrics (Top-1, Top-5, MFR, MAR)
```

**Step 1-2: Collect Coverage**

```bash
# Defects4J includes coverage infrastructure
cd /tmp/Lang_1_buggy

# Compile with coverage
defects4j compile

# Run tests with coverage collection
defects4j coverage
```

**Step 3-4: Fault Localization with GZoltar**

```python
def run_gzoltar(work_path: Path) -> list[dict]:
    """Run GZoltar spectrum-based fault localization."""
    # GZoltar integrates with Defects4J
    cmd = [DEFECTS4J, "compile", "-w", str(work_path)]
    subprocess.run(cmd, check=True)

    # Run tests with GZoltar agent
    # (Requires GZoltar setup - see references/gzoltar.md)

    # Parse GZoltar output
    sfl_file = work_path / "gzoltar" / "sfl" / "txt" / "ochiai.ranking.csv"
    rankings = []
    with open(sfl_file) as f:
        for line in f:
            parts = line.strip().split(";")
            rankings.append({
                "class": parts[0],
                "line": int(parts[1]),
                "score": float(parts[2])
            })

    return rankings

def get_ground_truth(project: str, bug_id: int) -> list[dict]:
    """Get ground truth buggy lines from Defects4J."""
    work_path = checkout_bug(project, bug_id, "b")

    # Get modified source files
    cmd = [DEFECTS4J, "export", "-p", "classes.modified", "-w", str(work_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    modified_classes = result.stdout.strip().split("\n")

    # Diff buggy vs fixed to get exact lines
    fixed_path = checkout_bug(project, bug_id, "f")

    buggy_lines = []
    for cls in modified_classes:
        # Convert class name to file path
        file_path = cls.replace(".", "/") + ".java"
        # ... diff logic to get modified lines

    return buggy_lines
```

**Step 5: Compute Metrics**

```python
def compute_fl_metrics(rankings: list[dict], ground_truth: list[dict]) -> dict:
    """Compute fault localization metrics."""
    # Find rank of first buggy line
    gt_set = {(gt["class"], gt["line"]) for gt in ground_truth}

    first_rank = None
    for rank, item in enumerate(rankings, 1):
        if (item["class"], item["line"]) in gt_set:
            if first_rank is None:
                first_rank = rank
            break

    # Compute metrics
    return {
        "top_1": 1 if first_rank == 1 else 0,
        "top_5": 1 if first_rank and first_rank <= 5 else 0,
        "top_10": 1 if first_rank and first_rank <= 10 else 0,
        "mfr": first_rank,  # Mean First Rank
    }
```

---

## Defects4J Projects and Statistics

### Version 2.0 Projects (17 total)

| Project | ID | # Bugs | Description |
|---------|-----|--------|-------------|
| JFreeChart | Chart | 26 | Charting library |
| Closure Compiler | Closure | 176 | JavaScript compiler |
| Apache Commons CLI | Cli | 40 | Command line parsing |
| Apache Commons Codec | Codec | 18 | Encoders/decoders |
| Apache Commons Collections | Collections | 4 | Data structures |
| Apache Commons Compress | Compress | 47 | Compression library |
| Apache Commons CSV | Csv | 16 | CSV parser |
| Google Gson | Gson | 18 | JSON library |
| Jackson Core | JacksonCore | 26 | JSON processor |
| Jackson Databind | JacksonDatabind | 112 | JSON data binding |
| Jackson XML | JacksonXml | 6 | XML support for Jackson |
| JSoup | Jsoup | 93 | HTML parser |
| JXPath | JxPath | 22 | XPath for Java objects |
| Apache Commons Lang | Lang | 65 | Java utilities |
| Apache Commons Math | Math | 106 | Math library |
| Mockito | Mockito | 38 | Mocking framework |
| Joda-Time | Time | 27 | Date/time library |

### Bug Selection for Studies

```python
# Common subsets used in papers

# Original Defects4J 1.0 (395 bugs, 6 projects)
DEFECTS4J_V1 = ["Chart", "Closure", "Lang", "Math", "Mockito", "Time"]

# Defects4J 2.0 additions (440+ bugs, 11 new projects)
DEFECTS4J_V2_NEW = ["Cli", "Codec", "Collections", "Compress", "Csv",
                    "Gson", "JacksonCore", "JacksonDatabind", "JacksonXml",
                    "Jsoup", "JxPath"]

def get_bugs_for_study(version: str = "1.0") -> list[tuple[str, int]]:
    """Get standard bug set for replication."""
    bugs = []
    projects = DEFECTS4J_V1 if version == "1.0" else DEFECTS4J_V1 + DEFECTS4J_V2_NEW

    for project in projects:
        # Get bug IDs
        cmd = [DEFECTS4J, "bids", "-p", project]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        for bug_id in result.stdout.strip().split("\n"):
            bugs.append((project, int(bug_id)))

    return bugs
```

---

## Command Reference

### Core Commands

```bash
# List available projects
defects4j pids

# List bugs in a project
defects4j bids -p <project>

# Bug information
defects4j info -p <project> -b <bug_id>

# Checkout version
defects4j checkout -p <project> -v <version> -w <work_dir>
# version: Xb (buggy) or Xf (fixed), e.g., 1b, 1f

# Compile project
defects4j compile -w <work_dir>

# Run all tests
defects4j test -w <work_dir>

# Run specific test
defects4j test -w <work_dir> -t <test_class>::<test_method>

# Run only relevant (triggering) tests
defects4j test -w <work_dir> -r

# Export project properties
defects4j export -p <property> -w <work_dir>
```

### Useful Properties

```bash
# Source directory
defects4j export -p dir.src.classes -w /tmp/bug

# Test directory
defects4j export -p dir.src.tests -w /tmp/bug

# Modified classes (bug location)
defects4j export -p classes.modified -w /tmp/bug

# Relevant tests (expose the bug)
defects4j export -p tests.relevant -w /tmp/bug

# Triggering tests (fail on buggy, pass on fixed)
defects4j export -p tests.trigger -w /tmp/bug
```

---

## Common Issues and Solutions

### Issue: Checkout Fails with SVN Error

Some older bugs use SVN. Install SVN:

```bash
# Ubuntu/Debian
sudo apt-get install subversion

# macOS
brew install svn
```

### Issue: Tests Fail Due to Java Version

Defects4J bugs were collected with specific Java versions:

```bash
# Check required Java version
defects4j info -p Chart -b 1 | grep "Java"

# Use JAVA_HOME to switch versions
export JAVA_HOME=/path/to/java8
defects4j test -w /tmp/bug
```

### Issue: Out of Memory During Tests

Increase heap size:

```bash
export _JAVA_OPTIONS="-Xmx4g"
defects4j test -w /tmp/bug
```

### Issue: Flaky Tests

Some tests are flaky. Run multiple times or exclude known flaky tests:

```python
# Known flaky tests (maintain a list)
FLAKY_TESTS = {
    ("Lang", 10): ["org.apache.commons.lang3.SomeTest::testFlaky"],
}

def run_tests_excluding_flaky(project: str, bug_id: int, work_path: Path):
    """Run tests excluding known flaky ones."""
    flaky = FLAKY_TESTS.get((project, bug_id), [])
    # Use defects4j test with -t to exclude specific tests
```

---

## Integration with APR Tools

### With ARJA (Genetic Programming APR)

```bash
# ARJA uses Defects4J directly
java -jar arja.jar -DsrcJavaDir=/tmp/Lang_1_b/src \
    -DbinJavaDir=/tmp/Lang_1_b/target/classes \
    -DbinTestDir=/tmp/Lang_1_b/target/test-classes
```

### With TBar (Template-Based APR)

```bash
# TBar expects Defects4J checkout
java -jar TBar.jar -d4jHome /path/to/defects4j \
    -project Lang -bugId 1
```

### With LLM-Based Repair

```python
def prepare_llm_repair_prompt(project: str, bug_id: int) -> str:
    """Prepare prompt for LLM-based repair."""
    work_path = checkout_bug(project, bug_id, "b")

    # Get fault location
    locations = get_fault_locations(project, bug_id)

    # Read buggy code
    src_dir = work_path / locations[0]["src_dir"]
    buggy_file = src_dir / (locations[0]["class"].replace(".", "/") + ".java")
    buggy_code = buggy_file.read_text()

    # Get failing test
    cmd = [DEFECTS4J, "export", "-p", "tests.trigger", "-w", str(work_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    failing_test = result.stdout.strip().split("\n")[0]

    prompt = f"""Fix the bug in the following Java code.

Buggy code:
```java
{buggy_code}
```

The following test fails:
{failing_test}

Provide the fixed code.
"""
    return prompt
```

---

## References

- **Official Repository**: https://github.com/rjust/defects4j
- **Paper**: "Defects4J: A Database of Existing Faults" (ISSTA 2014)
- **Documentation**: https://github.com/rjust/defects4j/blob/master/README.md

For advanced usage, see:
- [references/api.md](references/api.md) - Complete command reference
- [references/issues.md](references/issues.md) - Known issues and workarounds
- [references/gzoltar.md](references/gzoltar.md) - Fault localization setup
