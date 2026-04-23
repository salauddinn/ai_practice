# Hello LangGraph

Learning LangGraph fundamentals through three progressive examples.

## Examples

### 1. `hello.py` — Basic Sequential Graph

A simple graph that populates a person's friends and family lists.

```
START → friends → family → END
```

- **State**: `name`, `friends`, `family`
- **Pattern**: Mutates and returns the full state object (works but not recommended)
- **Lesson**: Introduction to `StateGraph`, nodes, and edges

### 2. `partial.py` — Partial State Updates (Recommended Pattern)

A student clearance workflow where each department checks off independently.

```
START → fin → lib → sports → END
```

- **State**: `student_id`, `fin_dept`, `lib_dept`, `sports_dept`
- **Pattern**: Each node returns **only the keys it changed** (e.g., `{"fin_dept": True}`)
- **Lesson**: LangGraph automatically merges partial returns into the full state — you don't need to return everything

### 3. `partial_parallel.py` — Parallel Execution

Same student clearance workflow, but all departments run **at the same time**.

```
        ┌→ fin ──→┐
START ──┼→ lib ──→┼── END
        └→ sports →┘
```

- **State**: Same as `partial.py`
- **Pattern**: Multiple edges from `START` cause nodes to execute concurrently
- **Lesson**: Partial returns are essential for parallel execution — if nodes mutated shared state directly, you'd get race conditions

## Key Concepts

| Concept | Description |
|---|---|
| **StateGraph** | A graph that manages a typed state dict across nodes |
| **Node** | A function that receives state and returns changes |
| **Edge** | Defines execution order between nodes |
| **Partial Return** | Returning only changed keys — LangGraph merges the rest |
| **Parallel Edges** | Multiple edges from the same node run targets concurrently |

## Running

```bash
uv run python hello.py
uv run python partial.py
uv run python partial_parallel.py
```
