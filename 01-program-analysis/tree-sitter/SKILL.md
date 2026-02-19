---
name: parsing-with-tree-sitter
description: Fast incremental parsing library for 100+ programming languages. Use when building code analysis tools, extracting ASTs, implementing syntax highlighting, or processing code at scale for SE research. Supports Python, JavaScript, Java, C/C++, Go, Rust, and many more.
version: 1.0.0
author: SE Research Skills
license: MIT
tags: [Program Analysis, AST, Parsing, Static Analysis, Code Analysis]
dependencies: [tree-sitter>=0.20.0, tree-sitter-python>=0.20.0]
---

# Tree-sitter: Fast Incremental Parsing

Tree-sitter is a parser generator tool and incremental parsing library used extensively in SE research for AST extraction, code analysis, and building program analysis tools. It's used by GitHub for syntax highlighting and code navigation.

## When to Use Tree-sitter

**Use tree-sitter when:**
- Building code analysis tools that need ASTs
- Processing large codebases (incremental parsing is fast)
- Need language-agnostic analysis across multiple languages
- Extracting code features for ML models
- Building IDE-like tooling (syntax highlighting, code folding)

**Consider alternatives when:**
- Need full semantic analysis → Use language-specific compilers (javac, rustc)
- Need type information → Use CodeQL, Soot, or language LSPs
- Simple pattern matching → Consider Semgrep or regex

## Quick Start

### Installation

```bash
# Python bindings
pip install tree-sitter tree-sitter-python tree-sitter-javascript tree-sitter-java

# For building custom grammars
pip install tree-sitter-cli
```

### Basic Usage: Parse Code to AST

```python
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Initialize parser
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

# Parse source code
source_code = b"""
def hello(name):
    return f"Hello, {name}!"
"""

tree = parser.parse(source_code)
root = tree.root_node

# Print AST structure
def print_tree(node, indent=0):
    print("  " * indent + f"{node.type}: {repr(node.text[:50])}")
    for child in node.children:
        print_tree(child, indent + 1)

print_tree(root)
```

### Output:
```
module: b'\ndef hello(name):\n    return f"Hello, {name}!"'
  function_definition: b'def hello(name):\n    return f"Hello, {name}!"'
    name: b'hello'
    parameters: b'(name)'
      identifier: b'name'
    block: b'return f"Hello, {name}!"'
      return_statement: b'return f"Hello, {name}!"'
        string: b'f"Hello, {name}!"'
```

---

## Core Workflows

### Workflow 1: Extract All Functions from a Codebase

```
Function Extraction Checklist:
- [ ] Step 1: Set up parser for target language
- [ ] Step 2: Define query pattern for functions
- [ ] Step 3: Walk codebase and parse each file
- [ ] Step 4: Extract function metadata (name, params, body)
- [ ] Step 5: Output structured data (JSON/CSV)
```

**Step 1-2: Set Up Parser and Query**

```python
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query
from pathlib import Path
import json

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

# Query to find all function definitions
FUNC_QUERY = Query(PY_LANGUAGE, """
(function_definition
  name: (identifier) @func_name
  parameters: (parameters) @params
  body: (block) @body) @function
""")
```

**Step 3-4: Extract Functions from Files**

```python
def extract_functions(file_path: Path) -> list[dict]:
    """Extract all functions from a Python file."""
    source = file_path.read_bytes()
    tree = parser.parse(source)

    functions = []
    captures = FUNC_QUERY.captures(tree.root_node)

    # Group captures by function
    current_func = {}
    for node, name in captures:
        if name == "function":
            if current_func:
                functions.append(current_func)
            current_func = {
                "file": str(file_path),
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1,
            }
        elif name == "func_name":
            current_func["name"] = node.text.decode()
        elif name == "params":
            current_func["params"] = node.text.decode()
        elif name == "body":
            current_func["body"] = node.text.decode()

    if current_func:
        functions.append(current_func)

    return functions
```

**Step 5: Process Entire Codebase**

```python
def analyze_codebase(root_dir: Path) -> list[dict]:
    """Extract all functions from a Python codebase."""
    all_functions = []

    for py_file in root_dir.rglob("*.py"):
        try:
            functions = extract_functions(py_file)
            all_functions.extend(functions)
        except Exception as e:
            print(f"Error parsing {py_file}: {e}")

    return all_functions

# Usage
functions = analyze_codebase(Path("./my_project"))
print(f"Found {len(functions)} functions")

# Save to JSON
with open("functions.json", "w") as f:
    json.dump(functions, f, indent=2)
```

---

### Workflow 2: Code Change Analysis (Diff-Aware)

Tree-sitter supports incremental parsing, making it ideal for analyzing code changes.

```
Change Analysis Checklist:
- [ ] Step 1: Parse original code
- [ ] Step 2: Apply edit to tree
- [ ] Step 3: Parse modified code incrementally
- [ ] Step 4: Compare AST changes
```

```python
def analyze_code_change(original: bytes, modified: bytes, edit_start: int, edit_end: int):
    """Analyze a code change using incremental parsing."""
    # Parse original
    tree = parser.parse(original)

    # Create edit description
    edit = tree.edit(
        start_byte=edit_start,
        old_end_byte=edit_end,
        new_end_byte=edit_start + len(modified) - len(original) + (edit_end - edit_start),
        start_point=(0, edit_start),
        old_end_point=(0, edit_end),
        new_end_point=(0, edit_start + len(modified) - len(original) + (edit_end - edit_start)),
    )

    # Re-parse incrementally (much faster for large files)
    new_tree = parser.parse(modified, tree)

    # Find changed ranges
    changed_ranges = tree.changed_ranges(new_tree)

    return {
        "changed_ranges": [(r.start_byte, r.end_byte) for r in changed_ranges],
        "old_root": tree.root_node.type,
        "new_root": new_tree.root_node.type,
    }
```

---

### Workflow 3: Extract Code Features for ML

Common in SE research for code representation learning.

```python
def extract_code_features(source: bytes, language: Language) -> dict:
    """Extract features for ML models from source code."""
    parser = Parser(language)
    tree = parser.parse(source)
    root = tree.root_node

    features = {
        "node_count": 0,
        "max_depth": 0,
        "node_types": {},
        "identifiers": [],
        "literals": [],
    }

    def traverse(node, depth=0):
        features["node_count"] += 1
        features["max_depth"] = max(features["max_depth"], depth)

        # Count node types
        node_type = node.type
        features["node_types"][node_type] = features["node_types"].get(node_type, 0) + 1

        # Collect identifiers and literals
        if node_type == "identifier":
            features["identifiers"].append(node.text.decode())
        elif node_type in ("string", "integer", "float"):
            features["literals"].append(node.text.decode())

        for child in node.children:
            traverse(child, depth + 1)

    traverse(root)
    return features
```

---

## Query Language Reference

Tree-sitter uses S-expression queries for pattern matching.

### Basic Patterns

```scheme
; Match any function definition
(function_definition)

; Match function with specific name
(function_definition
  name: (identifier) @name
  (#eq? @name "main"))

; Match function calls
(call
  function: (identifier) @func_name
  arguments: (argument_list) @args)

; Match method calls
(call
  function: (attribute
    object: (identifier) @object
    attribute: (identifier) @method))
```

### Capture Groups

```scheme
; Capture for extraction
(function_definition
  name: (identifier) @function.name
  parameters: (parameters) @function.params
  body: (block) @function.body) @function.def
```

### Predicates

```scheme
; Equality check
(#eq? @name "test")

; Regex match
(#match? @name "^test_")

; Not equal
(#not-eq? @name "__init__")
```

---

## Multi-Language Support

### Setting Up Multiple Languages

```python
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_java as tsjava
from tree_sitter import Language, Parser

LANGUAGES = {
    ".py": Language(tspython.language()),
    ".js": Language(tsjavascript.language()),
    ".java": Language(tsjava.language()),
}

def parse_file(file_path: Path):
    """Parse file based on extension."""
    suffix = file_path.suffix
    if suffix not in LANGUAGES:
        raise ValueError(f"Unsupported language: {suffix}")

    parser = Parser(LANGUAGES[suffix])
    source = file_path.read_bytes()
    return parser.parse(source)
```

### Available Language Bindings

Install via pip:
```bash
pip install tree-sitter-python tree-sitter-javascript tree-sitter-java
pip install tree-sitter-c tree-sitter-cpp tree-sitter-go tree-sitter-rust
pip install tree-sitter-typescript tree-sitter-ruby tree-sitter-php
```

Full list: https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers

---

## Common Issues and Solutions

### Issue: Encoding Errors

Tree-sitter expects bytes, not strings.

```python
# Wrong
tree = parser.parse(source_code)  # if source_code is str

# Correct
tree = parser.parse(source_code.encode('utf-8'))
# Or read as bytes
source = Path("file.py").read_bytes()
tree = parser.parse(source)
```

### Issue: Missing Node Types

Check the grammar's node-types.json for valid types:

```python
# Find all node types in a tree
def get_all_node_types(node, types=None):
    if types is None:
        types = set()
    types.add(node.type)
    for child in node.children:
        get_all_node_types(child, types)
    return types

tree = parser.parse(b"def foo(): pass")
print(sorted(get_all_node_types(tree.root_node)))
```

### Issue: Query Not Matching

Debug by checking the actual AST structure:

```python
def debug_ast(node, indent=0):
    """Print detailed AST for debugging queries."""
    print("  " * indent + f"({node.type}", end="")
    if node.child_count == 0:
        print(f" {repr(node.text.decode())})", end="")
    else:
        print()
        for child in node.children:
            debug_ast(child, indent + 1)
        print("  " * indent + ")", end="")
    if indent == 0:
        print()
```

---

## Performance Tips

### 1. Reuse Parser Instances

```python
# Bad: Creating parser per file
for file in files:
    parser = Parser(language)  # Expensive!
    tree = parser.parse(file.read_bytes())

# Good: Reuse parser
parser = Parser(language)
for file in files:
    tree = parser.parse(file.read_bytes())
```

### 2. Use Incremental Parsing for Edits

```python
# For IDE-like applications with frequent small edits
old_tree = parser.parse(old_source)
# ... user makes edit ...
new_tree = parser.parse(new_source, old_tree)  # Much faster
```

### 3. Parallelize for Large Codebases

```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def parse_file_worker(file_path: str) -> dict:
    """Worker function for parallel parsing."""
    # Note: Parser must be created in worker (not picklable)
    parser = Parser(Language(tspython.language()))
    source = Path(file_path).read_bytes()
    tree = parser.parse(source)
    return {"file": file_path, "node_count": count_nodes(tree.root_node)}

def parse_codebase_parallel(files: list[Path], max_workers: int = 4):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(parse_file_worker, [str(f) for f in files]))
    return results
```

---

## Integration with SE Research Tools

### With GumTree (AST Differencing)

```python
# Export tree-sitter AST to format compatible with GumTree
def to_gumtree_format(node, source: bytes) -> dict:
    """Convert tree-sitter node to GumTree-compatible format."""
    return {
        "type": node.type,
        "label": node.text.decode() if node.child_count == 0 else "",
        "pos": node.start_byte,
        "length": node.end_byte - node.start_byte,
        "children": [to_gumtree_format(child, source) for child in node.children]
    }
```

### With CodeBERT (Tokenization)

```python
def tokenize_with_ast(source: bytes, parser: Parser) -> list[tuple[str, str]]:
    """Create token-type pairs for CodeBERT-style models."""
    tree = parser.parse(source)
    tokens = []

    def collect_tokens(node):
        if node.child_count == 0:  # Leaf node
            tokens.append((node.text.decode(), node.type))
        for child in node.children:
            collect_tokens(child)

    collect_tokens(tree.root_node)
    return tokens
```

---

## References

- **Official Docs**: https://tree-sitter.github.io/tree-sitter/
- **Python Bindings**: https://github.com/tree-sitter/py-tree-sitter
- **Language Parsers**: https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers
- **Query Syntax**: https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries

For advanced usage, see:
- [references/api.md](references/api.md) - Complete API reference
- [references/queries.md](references/queries.md) - Query language deep dive
- [references/issues.md](references/issues.md) - Common issues from GitHub
