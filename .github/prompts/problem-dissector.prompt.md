---
description: ">-"
---

# Problem Dissector Skill (`problem-dissector`)

High-leverage cognitive router and problem deconstruction engine operating inside [`F:\Aaradhya-Dev-Tamrakar\Problem-Dissector`](file:///F:/Aaradhya-Dev-Tamrakar/Problem-Dissector).

Deconstructs raw competitive programming problem statements into structured **Agent Dissection Contracts** so coding agents (Fleet workers, Copilot, LLMs) receive razor-sharp cognitive anchors rather than struggling with raw 3-page problem statements.

---

## 1. Core Operating Principles

1. **Deconstruction Over Solving**: Do not write the full solution code. Produce the deterministic contract specifying Big-O ceilings, invariants, edge cases, and forbidden pitfalls.
2. **Deterministic Fast Path (<20ms)**: Derives asymptotic bounds purely through mathematical constraint analysis ($N \leq 10^5 \implies O(N \log N)$), costing $0.00 and avoiding LLM latency.
3. **Context Firebreak (`INV-CTX-FIREBREAK`)**: When called by subagents or swarms, run as an Antigravity background task to keep main orchestrator contexts lean.

---

## 2. CLI Execution Modes

Working directory: `F:\Aaradhya-Dev-Tamrakar\Problem-Dissector`

### Mode A: Emit Pure Agent Contract (JSON to stdout or Pipe)
```powershell
python cli/dissect.py --slug matrix_exploration --contract
```

### Mode B: Full Problem Dissection (Interactive Terminal Card)
```powershell
python cli/dissect.py --slug 0-k-multiple
```

### Mode C: Export Artifacts (Markdown + JSON + Contract)
Exports to `outputs/<slug>.md`, `outputs/<slug>.json`, and `outputs/contracts/<slug>.contract.json`:
```powershell
python cli/dissect.py --slug matrix_exploration --export
```

### Mode D: Batch Dissection Background Daemon (Antigravity Task)
Pre-dissects $N$ tasks in the background without blocking execution:
```powershell
python cli/dissect.py --all --limit 50 --quiet
```

---

## 3. Contract Schema & Downstream Consumption

The downstream agent receives an `AgentDissectionContract`:
```json
{
  "task_slug": "matrix_exploration",
  "asymptotics": {
    "time_complexity": "O(N^2)",
    "space_complexity": "O(N^2) or O(N)",
    "ops_budget": 100000000,
    "dominant_dimension": "N <= 1000"
  },
  "archetype_id": "02",
  "archetype_name": "Graph Theory & Network Flows",
  "core_invariants": [
    "State can be modeled as implicit 2D/3D graph where transitions are restricted to 4 or 8 neighboring cells."
  ],
  "forbidden_approaches": [
    "Using signed 32-bit int for accumulated sums/products — triggers silent integer overflow.",
    "Unbuffered slow standard I/O streams without fast I/O optimization."
  ],
  "guidelines": {
    "recommended_language": "C++20",
    "data_structures": ["std::vector<std::vector<int>> (Adjacency list)", "std::queue (BFS)"],
    "overflow_risk": true,
    "integer_types": "long long / int64_t"
  },
  "agent_prompt_summary": "Implement in C++20 with O(N^2) time and O(N^2) or O(N) space complexity..."
}
```

---

## 4. Integration with Fleet-Orchestrator & Azmuth Ultimatrix

When dispatching tasks to `Fleet-Orchestrator` workers:
1. Orchestrator invokes `python cli/dissect.py --slug <slug> --contract > contract.json`.
2. Worker receives the `contract.json` payload inside its isolated `.worktrees/<task_id>` folder.
3. Worker writes code adhering strictly to `asymptotics` and `guidelines`.

### Algorithmic Gene Resolution (Azmuth Ultimatrix)
The contract directly maps into the **Azmuth Ultimatrix Genomic Tiers (Tier 0 to Tier 4)**:
- **Tier 0 (Hardware Substrate)**: Unbuffered I/O streams (`FAST_IO_STREAM_UNTIE`, `INTERACTIVE_STREAM_IO`)
- **Tier 1 (Language Runtime)**: Modular arithmetic, `SplitMix64`, recursion unbounding (`FAST_MODULAR_EXPONENTIATION`)
- **Tier 2 (Primitives)**: Graph and tree archetypes (`DISJOINT_SET_UNION`, `SEGMENT_TREE_RANGE_QUERY`, `DIJKSTRA_SHORTEST_PATH`)
- **Tier 3 (Dimensional Collapse)**: Cubic breakers for $N \le 5000$ (`DINIC_MAX_FLOW`, `TWO_SAT_SOLVER`, bitset Floyd-Warshall)
- **Tier 4 (Frontier CAS)**: Number theory & high-degree polynomials (`POLLARDS_RHO_PRIME_FACTORIZATION`, `NTT`)

Automated gene resolution and solution assembly:
```powershell
python tools/ultimatrix_splicer.py --task <slug> --output solution.cpp
```
