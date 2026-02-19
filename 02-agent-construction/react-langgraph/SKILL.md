---
name: react-agent-langgraph
description: Build ReAct (Reasoning + Acting) agents using LangGraph for SE research tools. Provides architecture patterns for planning, working memory, long-term memory, and tool orchestration. Use when building autonomous analysis tools that need to reason about complex problems and adaptively choose analysis strategies.
version: 1.0.0
author: SE Research Skills
license: MIT
tags: [Agent, LangGraph, ReAct, Planning, Memory, Tool Use, LLM]
dependencies: [langgraph>=0.2.0, langchain>=0.2.0, pydantic>=2.0]
---

# ReAct Agent Construction with LangGraph

Build autonomous SE research tools using the ReAct (Reasoning + Acting) paradigm with LangGraph. This skill covers architecture patterns for agents that can plan, reason, use tools, and learn from experience.

## When to Use ReAct Agents

**Use ReAct agents when:**
- Analysis requires adaptive strategy selection
- Problem has multiple valid solution paths
- Need to handle ambiguous or complex inputs
- Semantic understanding beyond pattern matching is needed
- Tool orchestration depends on intermediate results

**Consider simpler approaches when:**
- Problem has deterministic solution → Use pipeline/sequential
- Pattern matching is sufficient → Use static analysis
- Speed is critical, accuracy secondary → Use rule-based
- No reasoning needed → Use direct tool calls

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ReAct Agent Architecture                          │
│                                                                          │
│   ┌──────────────┐                                                      │
│   │   Input      │                                                      │
│   └──────┬───────┘                                                      │
│          │                                                              │
│          ▼                                                              │
│   ┌──────────────┐     ┌──────────────────────────────────────────┐    │
│   │   PLANNER    │────▶│        WORKING MEMORY (Scratchpad)       │    │
│   │  (Identify   │     │  - Current goal                          │    │
│   │   problem,   │     │  - Observations from tools               │    │
│   │   decompose) │     │  - Reasoning chain                       │    │
│   └──────┬───────┘     └──────────────────────────────────────────┘    │
│          │                           │                                  │
│          │ Plan                      │ Context                          │
│          ▼                           ▼                                  │
│   ┌──────────────────────────────────────────────────────────────┐     │
│   │                    REASONING LOOP                             │     │
│   │                                                               │     │
│   │   ┌──────────┐    ┌──────────┐    ┌──────────┐              │     │
│   │   │  THINK   │───▶│   ACT    │───▶│ OBSERVE  │───┐          │     │
│   │   │ (Reason) │    │ (Tool)   │    │ (Result) │   │          │     │
│   │   └──────────┘    └──────────┘    └──────────┘   │          │     │
│   │        ▲                                          │          │     │
│   │        └──────────────────────────────────────────┘          │     │
│   │                     (iterate until done)                     │     │
│   └──────────────────────────────────────────────────────────────┘     │
│          │                                                              │
│          │ Final Answer                                                 │
│          ▼                                                              │
│   ┌──────────────┐     ┌──────────────────────────────────────────┐    │
│   │  VALIDATOR   │────▶│        LONG-TERM MEMORY                  │    │
│   │  (Check      │     │  - Successful strategies                 │    │
│   │   result)    │     │  - Failure patterns                      │    │
│   └──────┬───────┘     │  - Domain knowledge                      │    │
│          │             └──────────────────────────────────────────┘    │
│          ▼                                                              │
│   ┌──────────────┐                                                      │
│   │   Output     │                                                      │
│   └──────────────┘                                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
pip install langgraph langchain-anthropic pydantic
```

### Basic ReAct Agent Structure

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# 1. Define State Schema
class AgentState(TypedDict, total=False):
    """Agent state passed between nodes."""
    # Input
    input: str

    # Working Memory
    messages: Annotated[list, add_messages]  # Conversation/reasoning history
    current_plan: list[str]                   # Decomposed steps
    observations: list[dict]                  # Tool results

    # Control
    next_action: str | None
    iteration: int

    # Output
    result: dict | None
    error: str | None


# 2. Define Tools
def analyze_code_tool(code: str) -> dict:
    """Analyze code for patterns."""
    # Your static analysis logic here
    return {"patterns_found": [...], "risk_score": 0.5}

def search_knowledge_tool(query: str) -> list[dict]:
    """Search long-term memory for relevant knowledge."""
    # Your knowledge retrieval logic here
    return [{"pattern": "...", "solution": "..."}]


# 3. Define Nodes
def planner_node(state: AgentState) -> AgentState:
    """Decompose problem into steps."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    prompt = f"""Analyze this problem and create a plan:

Input: {state['input']}

Break this into 3-5 concrete steps. Output as JSON:
{{"plan": ["step1", "step2", ...]}}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    plan = parse_json(response.content)

    return {**state, "current_plan": plan.get("plan", [])}


def think_node(state: AgentState) -> AgentState:
    """Reason about next action based on observations."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    prompt = f"""Based on your observations, decide the next action.

Plan: {state['current_plan']}
Observations so far: {state['observations']}
Current step: {state['iteration']}

Available tools:
- analyze_code: Analyze code for patterns
- search_knowledge: Search for similar past cases

Output JSON: {{"action": "tool_name or 'finish'", "input": "..."}}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    decision = parse_json(response.content)

    return {**state, "next_action": decision.get("action")}


def act_node(state: AgentState) -> AgentState:
    """Execute the chosen tool."""
    action = state.get("next_action")

    if action == "analyze_code":
        result = analyze_code_tool(state["input"])
    elif action == "search_knowledge":
        result = search_knowledge_tool(state["input"])
    elif action == "finish":
        return state
    else:
        result = {"error": f"Unknown action: {action}"}

    observations = state.get("observations", []) + [result]
    iteration = state.get("iteration", 0) + 1

    return {**state, "observations": observations, "iteration": iteration}


def validator_node(state: AgentState) -> AgentState:
    """Validate and format final result."""
    # Combine all observations into final result
    result = {
        "input": state["input"],
        "analysis": state.get("observations", []),
        "conclusion": summarize_observations(state["observations"]),
    }
    return {**state, "result": result}


# 4. Define Routing
def should_continue(state: AgentState) -> str:
    """Decide whether to continue reasoning or finish."""
    if state.get("next_action") == "finish":
        return "validate"
    if state.get("iteration", 0) >= 5:  # Max iterations
        return "validate"
    return "think"


# 5. Build Graph
def build_react_agent():
    """Build the ReAct agent graph."""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("plan", planner_node)
    graph.add_node("think", think_node)
    graph.add_node("act", act_node)
    graph.add_node("validate", validator_node)

    # Add edges
    graph.set_entry_point("plan")
    graph.add_edge("plan", "think")
    graph.add_edge("think", "act")
    graph.add_conditional_edges("act", should_continue, {
        "think": "think",
        "validate": "validate",
    })
    graph.add_edge("validate", END)

    return graph.compile()


# 6. Run Agent
agent = build_react_agent()
result = agent.invoke({"input": "Analyze this code for security issues..."})
print(result["result"])
```

---

## Core Components

### Component 1: Planning Module

The planner decomposes complex problems into manageable steps.

```python
class PlannerConfig:
    """Configuration for the planning module."""
    max_steps: int = 5
    decomposition_strategy: str = "hierarchical"  # or "sequential", "parallel"


def planner_with_memory(state: AgentState, long_term_memory: LongTermMemory) -> AgentState:
    """Plan with awareness of past successful strategies."""

    # Retrieve similar past problems
    similar_cases = long_term_memory.search(state["input"], top_k=3)

    prompt = f"""Create a plan for this problem.

Problem: {state['input']}

Similar past cases and their successful strategies:
{format_cases(similar_cases)}

Create a plan that:
1. Identifies the core problem type
2. Breaks into 3-5 concrete steps
3. Leverages successful patterns from similar cases
4. Avoids known failure modes

Output JSON: {{"problem_type": "...", "plan": [...], "rationale": "..."}}
"""
    # ... execute LLM call
```

### Component 2: Working Memory (Scratchpad)

Working memory maintains state during the reasoning loop.

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class WorkingMemory:
    """Scratchpad for in-progress reasoning."""

    # Current goal/task
    current_goal: str = ""

    # Decomposed plan
    plan_steps: list[str] = field(default_factory=list)
    current_step_idx: int = 0

    # Observations from tool executions
    observations: list[dict] = field(default_factory=list)

    # Reasoning chain (think steps)
    reasoning_chain: list[str] = field(default_factory=list)

    # Intermediate results
    partial_results: dict[str, Any] = field(default_factory=dict)

    def add_observation(self, tool: str, result: dict):
        """Record tool execution result."""
        self.observations.append({
            "tool": tool,
            "result": result,
            "step": self.current_step_idx,
        })

    def add_thought(self, thought: str):
        """Record a reasoning step."""
        self.reasoning_chain.append(thought)

    def get_context_for_llm(self) -> str:
        """Format working memory as context for LLM."""
        return f"""
Current Goal: {self.current_goal}

Plan:
{chr(10).join(f"  {'[x]' if i < self.current_step_idx else '[ ]'} {step}"
              for i, step in enumerate(self.plan_steps))}

Recent Observations:
{chr(10).join(f"  - {obs['tool']}: {obs['result']}" for obs in self.observations[-3:])}

Reasoning So Far:
{chr(10).join(f"  {i+1}. {t}" for i, t in enumerate(self.reasoning_chain[-5:]))}
"""

    def advance_step(self):
        """Move to next plan step."""
        self.current_step_idx += 1


# Integration with state
class AgentState(TypedDict, total=False):
    input: str
    working_memory: WorkingMemory
    # ... other fields
```

### Component 3: Long-Term Memory

Long-term memory stores knowledge for cross-session learning.

```python
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class MemoryEntry:
    """A single memory entry."""
    id: str
    problem_type: str
    problem_summary: str
    solution_strategy: list[str]
    outcome: str  # "success" | "partial" | "failure"
    tools_used: list[str]
    insights: list[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class LongTermMemory:
    """Persistent knowledge store for the agent."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index_file = storage_path / "index.json"
        self.entries: dict[str, MemoryEntry] = {}
        self._load()

    def _load(self):
        """Load memory from disk."""
        if self.index_file.exists():
            data = json.loads(self.index_file.read_text())
            self.entries = {k: MemoryEntry(**v) for k, v in data.items()}

    def _save(self):
        """Persist memory to disk."""
        data = {k: asdict(v) for k, v in self.entries.items()}
        self.index_file.write_text(json.dumps(data, indent=2))

    def store(self, entry: MemoryEntry):
        """Store a new memory entry."""
        self.entries[entry.id] = entry
        self._save()

    def search(self, query: str, top_k: int = 5) -> list[MemoryEntry]:
        """Search for relevant memories.

        For production, use vector embeddings. This is a simple keyword match.
        """
        scored = []
        query_lower = query.lower()

        for entry in self.entries.values():
            # Simple scoring: count keyword matches
            score = sum(1 for word in query_lower.split()
                       if word in entry.problem_summary.lower())
            if score > 0:
                scored.append((score, entry))

        scored.sort(key=lambda x: -x[0])
        return [entry for _, entry in scored[:top_k]]

    def get_successful_strategies(self, problem_type: str) -> list[list[str]]:
        """Get strategies that worked for similar problems."""
        return [
            entry.solution_strategy
            for entry in self.entries.values()
            if entry.problem_type == problem_type and entry.outcome == "success"
        ]

    def get_failure_patterns(self, problem_type: str) -> list[str]:
        """Get insights from failed attempts."""
        insights = []
        for entry in self.entries.values():
            if entry.problem_type == problem_type and entry.outcome == "failure":
                insights.extend(entry.insights)
        return insights


# Usage in agent
def store_experience(state: AgentState, memory: LongTermMemory):
    """Store the completed analysis as a memory entry."""
    entry = MemoryEntry(
        id=generate_id(),
        problem_type=state.get("problem_type", "unknown"),
        problem_summary=state["input"][:200],
        solution_strategy=state.get("current_plan", []),
        outcome="success" if state.get("result") else "failure",
        tools_used=list(set(obs["tool"] for obs in state.get("observations", []))),
        insights=extract_insights(state),
    )
    memory.store(entry)
```

### Component 4: Tool Definitions

Tools are the actions the agent can take.

```python
from typing import Callable, Any
from dataclasses import dataclass

@dataclass
class Tool:
    """Tool definition for the agent."""
    name: str
    description: str
    function: Callable[..., Any]
    parameters: dict  # JSON schema for parameters

    def execute(self, **kwargs) -> dict:
        """Execute the tool with given parameters."""
        try:
            result = self.function(**kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ToolRegistry:
    """Registry of available tools."""

    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Register a tool."""
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        """Get tool by name."""
        return self.tools.get(name)

    def get_tool_descriptions(self) -> str:
        """Format tool descriptions for LLM prompt."""
        lines = []
        for tool in self.tools.values():
            lines.append(f"- {tool.name}: {tool.description}")
            lines.append(f"  Parameters: {json.dumps(tool.parameters)}")
        return "\n".join(lines)

    def execute(self, name: str, **kwargs) -> dict:
        """Execute a tool by name."""
        tool = self.get(name)
        if not tool:
            return {"success": False, "error": f"Unknown tool: {name}"}
        return tool.execute(**kwargs)


# Example: Register analysis tools
def create_analysis_tools() -> ToolRegistry:
    """Create tools for code analysis agent."""
    registry = ToolRegistry()

    registry.register(Tool(
        name="parse_nl_instructions",
        description="Extract permission requirements from natural language instructions",
        function=parse_nl_instructions,  # Your implementation
        parameters={"content": {"type": "string", "description": "Text to analyze"}},
    ))

    registry.register(Tool(
        name="analyze_code_ast",
        description="Analyze code using AST for dangerous patterns",
        function=analyze_python_code,
        parameters={"code": {"type": "string", "description": "Python code to analyze"}},
    ))

    registry.register(Tool(
        name="detect_tool_references",
        description="Detect references to Claude tools in text",
        function=analyze_claude_tools,
        parameters={"content": {"type": "string", "description": "Text to analyze"}},
    ))

    registry.register(Tool(
        name="semantic_analysis",
        description="Use LLM for semantic understanding of ambiguous text",
        function=semantic_llm_analysis,
        parameters={"text": {"type": "string"}, "question": {"type": "string"}},
    ))

    return registry
```

---

## Advanced Patterns

### Pattern 1: Self-Reflection

Add a reflection step after each action to improve reasoning.

```python
def reflect_node(state: AgentState) -> AgentState:
    """Reflect on the last action and its result."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    last_observation = state["observations"][-1] if state["observations"] else None

    prompt = f"""Reflect on your last action:

Action taken: {state.get('last_action')}
Result: {last_observation}

Consider:
1. Was this action effective? Why or why not?
2. What did you learn from this result?
3. Should you adjust your strategy?

Output JSON: {{"reflection": "...", "strategy_adjustment": "...", "confidence": 0.0-1.0}}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    reflection = parse_json(response.content)

    # Store reflection in working memory
    working_memory = state.get("working_memory", WorkingMemory())
    working_memory.add_thought(f"Reflection: {reflection.get('reflection', '')}")

    return {**state, "working_memory": working_memory}


# Add to graph
graph.add_node("reflect", reflect_node)
graph.add_edge("act", "reflect")
graph.add_conditional_edges("reflect", should_continue, {...})
```

### Pattern 2: Hierarchical Planning

For complex problems, use hierarchical decomposition.

```python
def hierarchical_planner(state: AgentState) -> AgentState:
    """Create hierarchical plan with sub-goals."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    prompt = f"""Create a hierarchical plan for this problem.

Problem: {state['input']}

Create a plan with:
- High-level phases (3-4)
- Specific steps under each phase
- Dependencies between steps

Output JSON:
{{
  "phases": [
    {{
      "name": "Phase 1: ...",
      "goal": "...",
      "steps": ["step1", "step2"],
      "depends_on": []
    }}
  ]
}}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    plan = parse_json(response.content)

    return {**state, "hierarchical_plan": plan.get("phases", [])}
```

### Pattern 3: Parallel Tool Execution

Execute independent tools in parallel for efficiency.

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def parallel_act_node(state: AgentState) -> AgentState:
    """Execute multiple independent tools in parallel."""
    actions = state.get("parallel_actions", [])

    if not actions:
        return state

    # Execute tools in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for action in actions:
            future = executor.submit(
                tool_registry.execute,
                action["tool"],
                **action["params"]
            )
            futures.append((action["tool"], future))

        results = []
        for tool_name, future in futures:
            result = future.result()
            results.append({"tool": tool_name, "result": result})

    observations = state.get("observations", []) + results
    return {**state, "observations": observations}
```

### Pattern 4: Confidence-Based Routing

Route based on confidence level.

```python
def confidence_router(state: AgentState) -> str:
    """Route based on confidence in current analysis."""
    confidence = state.get("confidence", 0.0)

    if confidence >= 0.9:
        return "validate"  # High confidence, proceed to output
    elif confidence >= 0.5:
        return "refine"    # Medium confidence, refine analysis
    else:
        return "backtrack" # Low confidence, try different approach


graph.add_conditional_edges("think", confidence_router, {
    "validate": "validate",
    "refine": "act",
    "backtrack": "replan",
})
```

---

## SE Research Tool Template

Complete template for building an SE research analysis tool.

```python
"""
SE Research Tool Template using ReAct Agent Architecture

This template provides a complete structure for building
analysis tools that use planning, memory, and tool orchestration.
"""

from __future__ import annotations
from typing import TypedDict, Annotated, Any
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic


# =============================================================================
# 1. State and Memory Definitions
# =============================================================================

@dataclass
class WorkingMemory:
    """In-progress reasoning state."""
    goal: str = ""
    plan: list[str] = field(default_factory=list)
    current_step: int = 0
    observations: list[dict] = field(default_factory=list)
    thoughts: list[str] = field(default_factory=list)

    def to_context(self) -> str:
        return f"Goal: {self.goal}\nPlan: {self.plan}\nObservations: {self.observations[-3:]}"


class AgentState(TypedDict, total=False):
    """Agent state schema."""
    # Input
    input: str
    input_type: str

    # Memory
    working_memory: WorkingMemory

    # Control flow
    current_phase: str
    next_action: str
    iteration: int
    max_iterations: int

    # Results
    result: dict
    confidence: float
    error: str


# =============================================================================
# 2. Tool Definitions (Customize for your analysis)
# =============================================================================

class AnalysisTools:
    """Tools available to the agent."""

    @staticmethod
    def static_analysis(content: str) -> dict:
        """Run static pattern matching analysis."""
        # Your Layer 2 implementation
        return {"patterns": [], "risk_score": 0.0}

    @staticmethod
    def semantic_analysis(text: str, question: str) -> dict:
        """Use LLM for semantic understanding."""
        llm = ChatAnthropic(model="claude-sonnet-4-20250514")
        response = llm.invoke([{
            "role": "user",
            "content": f"Question: {question}\n\nText: {text}"
        }])
        return {"answer": response.content}

    @staticmethod
    def knowledge_lookup(query: str, memory_path: Path) -> list[dict]:
        """Search long-term memory for relevant knowledge."""
        # Your knowledge retrieval implementation
        return []


# =============================================================================
# 3. Agent Nodes
# =============================================================================

def plan_node(state: AgentState) -> AgentState:
    """Create analysis plan."""
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    prompt = f"""Analyze this input and create a plan:

Input: {state['input']}
Type: {state.get('input_type', 'unknown')}

Create 3-5 steps to analyze this. Output JSON:
{{"plan": ["step1", ...], "problem_type": "..."}}
"""
    response = llm.invoke([{"role": "user", "content": prompt}])
    plan_data = json.loads(response.content)

    working_memory = WorkingMemory(
        goal=f"Analyze: {state['input'][:100]}",
        plan=plan_data.get("plan", []),
    )

    return {
        **state,
        "working_memory": working_memory,
        "current_phase": "execute",
        "iteration": 0,
        "max_iterations": 10,
    }


def think_node(state: AgentState) -> AgentState:
    """Decide next action based on observations."""
    wm = state["working_memory"]
    llm = ChatAnthropic(model="claude-sonnet-4-20250514")

    prompt = f"""Based on observations, decide next action.

{wm.to_context()}

Available actions:
- static_analysis: Run pattern matching
- semantic_analysis: Use LLM for understanding
- knowledge_lookup: Search past cases
- finish: Complete analysis

Output JSON: {{"action": "...", "params": {{...}}, "reasoning": "..."}}
"""
    response = llm.invoke([{"role": "user", "content": prompt}])
    decision = json.loads(response.content)

    wm.thoughts.append(decision.get("reasoning", ""))

    return {
        **state,
        "working_memory": wm,
        "next_action": decision.get("action"),
    }


def act_node(state: AgentState) -> AgentState:
    """Execute chosen action."""
    action = state.get("next_action")
    wm = state["working_memory"]

    if action == "static_analysis":
        result = AnalysisTools.static_analysis(state["input"])
    elif action == "semantic_analysis":
        result = AnalysisTools.semantic_analysis(state["input"], "What permissions are needed?")
    elif action == "knowledge_lookup":
        result = AnalysisTools.knowledge_lookup(state["input"], Path("./memory"))
    else:
        result = {"info": "No action taken"}

    wm.observations.append({"action": action, "result": result})
    wm.current_step += 1

    return {
        **state,
        "working_memory": wm,
        "iteration": state.get("iteration", 0) + 1,
    }


def validate_node(state: AgentState) -> AgentState:
    """Validate and format final result."""
    wm = state["working_memory"]

    # Aggregate observations into result
    result = {
        "input": state["input"],
        "analysis": wm.observations,
        "reasoning": wm.thoughts,
        "conclusion": "...",  # Generate from observations
    }

    return {**state, "result": result, "confidence": 0.8}


# =============================================================================
# 4. Routing Logic
# =============================================================================

def should_continue(state: AgentState) -> str:
    """Determine next step."""
    if state.get("next_action") == "finish":
        return "validate"
    if state.get("iteration", 0) >= state.get("max_iterations", 10):
        return "validate"
    if state.get("error"):
        return "error"
    return "think"


# =============================================================================
# 5. Build and Run
# =============================================================================

def build_agent() -> StateGraph:
    """Build the complete agent graph."""
    graph = StateGraph(AgentState)

    graph.add_node("plan", plan_node)
    graph.add_node("think", think_node)
    graph.add_node("act", act_node)
    graph.add_node("validate", validate_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "think")
    graph.add_edge("think", "act")
    graph.add_conditional_edges("act", should_continue, {
        "think": "think",
        "validate": "validate",
    })
    graph.add_edge("validate", END)

    return graph.compile()


def main():
    """Example usage."""
    agent = build_agent()

    result = agent.invoke({
        "input": "Your analysis input here...",
        "input_type": "skill_file",
    })

    print(json.dumps(result["result"], indent=2))


if __name__ == "__main__":
    main()
```

---

## Testing ReAct Agents

```python
import pytest
from your_agent import build_agent, AgentState

class TestReActAgent:
    """Tests for the ReAct agent."""

    def test_planning(self):
        """Test that planner creates valid plan."""
        agent = build_agent()
        state = agent.invoke({"input": "Test input"})

        assert "working_memory" in state
        assert len(state["working_memory"].plan) > 0

    def test_tool_execution(self):
        """Test that tools are executed correctly."""
        # Test individual tools
        result = AnalysisTools.static_analysis("def foo(): pass")
        assert "patterns" in result

    def test_max_iterations(self):
        """Test that agent respects max iterations."""
        agent = build_agent()
        state = agent.invoke({
            "input": "Complex input that might loop",
            "max_iterations": 3,
        })

        assert state["iteration"] <= 3

    def test_end_to_end(self):
        """Test complete analysis flow."""
        agent = build_agent()
        state = agent.invoke({"input": "Real analysis input"})

        assert state.get("result") is not None
        assert state.get("confidence", 0) > 0
```

---

## References

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **ReAct Paper**: "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2023)
- **LangChain Tools**: https://python.langchain.com/docs/modules/agents/tools/
- **Anthropic Claude**: https://docs.anthropic.com/claude/docs
