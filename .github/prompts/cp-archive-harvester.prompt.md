---
description: ">-"
---

# Competitive Programming Archive Harvester & Replica Engine (`cp-archive-harvester`)

Autonomous, high-throughput Competitive Programming problem, contest, and optimal solution harvesting and provisioning engine. Operates inside [`F:\Aaradhya-Dev-Tamrakar\Competitive-Programming`](file:///F:/Aaradhya-Dev-Tamrakar/Competitive-Programming) using Chrome DevTools Protocol (CDP port 9222) to extract client-rendered Single Page Application (SPA) data, and programmatically provision/replicate contests on HackerRank without manual UI slicing.

---

## 1. Operating Rules & Pre-Flight Checks

1. **Working Directory:** All harvesting and automated runner commands execute from `F:\Aaradhya-Dev-Tamrakar\Competitive-Programming`.
2. **Chrome CDP Verification:** Before running the harvester or replica engine, verify port `9222` is active:
   ```powershell
   python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:9222/json')"
   ```
3. **Ergonomic Pacing Runner:** When submitting solutions during live competitions, always use `scripts/ergonomic_cdp_runner.py` to emulate realistic human typing, simulated reading pauses, and local test passes:
   ```powershell
   python scripts/ergonomic_cdp_runner.py --speed 1.0
   ```
4. **Starting Chrome with CDP (Safe Quoting):**
   When starting Chrome, **always use inner single quotes** around `--profile-directory` to prevent PowerShell array argument splitting:
   ```powershell
   Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList @(
       "--remote-debugging-port=9222",
       '--profile-directory=Profile 6',
       "--restore-last-session"
   )
   ```
5. **CDP WebSocket Handshake (Origin Suppression):**
   Modern Chrome rejects incoming WebSocket connections that send standard Origin headers unless `--remote-allow-origins=*` was set. When connecting via `websocket-client` or custom Python scripts, **always suppress the origin header**:
   ```python
   import websocket
   ws = websocket.create_connection(ws_url, suppress_origin=True)
   ```

---

## 2. Supported Platforms & Capabilities

### Platform A: CS Academy / PreXtreme (`harvesters/csacademy_harvester.py`)
- Full catalog discovery and task indexing (669 tasks).
- Single-task or batch ingestion with un-truncated source code from Ace editor buffers.
- KaTeX LaTeX math extraction into Markdown.

### Platform B: HackerRank Contest Harvesting (`platforms/hackerrank/<contest_slug>/`)
- Lossless extraction of problem statements (`statement.html`, `statement.md`), constraints, and score schemas (`problem.json`).
- Accepted submission extraction (`submissions/*.py`, `*.cpp`) and final leaderboard capture (`leaderboard.json`).

### Platform C: HackerRank Contest Hosting & Replica Provisioning (CDP 9222)
Automates the complete lifecycle of hosting mock contests, practice rounds, or competition replicas under **Brainstorm Research Lab**:
1. **Contest Provisioning (`/administration/contests/create`)**:
   - Programmatically configure Contest Name, Slug, Start/End times, Organization Type (`Bootcamp`), and Organization Name.
   - Populate Markdown Landing Page: Tagline, Description, Rules, Scoring, and Prizes.
2. **Headless Challenge Synthesis (`/administration/challenges/create`)**:
   - Inject problem specifications directly into HackerRank's CodeMirror instances (`cm.setValue(...)` & `cm.save()`) across:
     - `cm[0]`: Problem Statement
     - `cm[1]`: Input Format
     - `cm[2]`: Constraints
     - `cm[3]`: Output Format
   - Set Name, Preview Description, and Tags (`addTag`).
3. **Test Case Ingestion (`/administration/challenges/edit/{id}/testcases`)**:
   - Headlessly configure sample and hidden test cases with input/output buffers and point weights.
4. **Contest Challenge Binding (`/administration/contests/edit/{contest_id}/challenges`)**:
   - Bind newly created challenge slugs to the contest with configured score weights (e.g. 10–100 pts) via UI input or REST API.

### Platform D: IEEEXtreme Governance & Scoring Strategy (`platforms/ieeextreme/`)
Full compliance and game-theoretic strategy defined in [`platforms/ieeextreme/RULES_AND_CONTEST_STRATEGY.md`](file:///F:/Aaradhya-Dev-Tamrakar/Competitive-Programming/platforms/ieeextreme/RULES_AND_CONTEST_STRATEGY.md):
1. **Task Taxonomy & AI Policy**:
   - **Game-Type Tasks (AI Permitted)**: Interactive bot challenges over `stdin`/`stdout`. Autonomous simulation, heuristic search (Minimax/MCTS), and agentic drafting are authorized.
   - **Locked-Workspace Tasks (AI Prohibited)**: External copy-paste into the web editor is disabled. Solutions must be authored natively inside the competition workspace. Automated agents must not attempt external clipboard injections.
2. **Workspace Pre-Configuration (100 KB Library Budget)**:
   - Code libraries (up to 100 KB total) may be uploaded before the deadline at `https://csacademy.com/workspace/template`.
   - Pre-loaded files serve as legal internal reference sources for manual copying inside the locked workspace during the contest. Zero mid-contest modifications allowed once tasks begin.
3. **Dynamic Scoring Dynamics**:
   - Dynamic points: $\text{Task Score} = 30 + 70 \times (1 - \text{Average Points})$. Solves on rare/difficult tasks scale dynamically up to 100 points.
   - Partial credit awarded for passing subsets of hidden test cases.
   - **Zero penalty for failed submissions**: Teams should submit early and iteratively whenever incremental test coverage is achieved.
   - **Tie-Breaking**: Measured from individual task release timestamp, not contest start. Earliest optimal submission counts.
4. **Attribution & Anti-Plagiarism**:
   - All external algorithms or references must be cited in code comments.
   - Submissions undergo AST similarity screening. Uncurated AI output carries severe mutual disqualification risk if structural patterns overlap with other teams.

---

## 3. Harvester & Replica CLI Commands

### CS Academy Harvester:
```powershell
# Discover and catalog all tasks
python harvesters/csacademy_harvester.py --discover

# Harvest single task with solutions
python harvesters/csacademy_harvester.py --slug matrix_exploration

# Controlled batch
python harvesters/csacademy_harvester.py --max-tasks 20
```

### Deterministic Solver & Evaluation Bench:
```powershell
# Run deterministic CP solver
python scripts/deterministic_solver_engine.py

# Evaluate Python solutions via LLM benchmark harness (uv-first)
uv run scripts/eval_bench.py --language python --model gemini-3.8-flash

### Local WSL2 Simulation Judge (`scripts/csa_simulator.py`):
Simulate solutions locally under exact CS Academy / IEEEXtreme judge conditions:
```powershell
# C++23 simulation with <atcoder/all>, Boost, Eigen, and sub-ms CPU measurement:
python scripts/csa_simulator.py --solution solution.cpp --input input.txt --expected expected.txt -t 1000 -m 128

# Python 3 simulation:
python scripts/csa_simulator.py --solution solution.py --input input.txt --expected expected.txt

# Environment certification test:
python scripts/csa_simulator.py --solution tests/test_csa_env.cpp
```

### Interactive & Game-Type Task Harvester:
Harvest client-rendered SPA game bot tasks with KaTeX conversion:
```powershell
python scripts/harvest_prextreme.py
```
```

### Repository Synchronization (`sync.bat`):
All version control operations must follow `github-workflow` and run through `sync.bat`:
```powershell
.\sync.bat -m "feat(scope): detailed summary"
```

---

## 4. Corpus Storage Schema

```text
F:\Aaradhya-Dev-Tamrakar\Competitive-Programming/
├── harvesters/
│   ├── cdp_engine.py                    # Lightweight WebSocket CDP client (suppress_origin=True)
│   └── csacademy_harvester.py           # CS Academy pipeline runner
├── ledger/
│   ├── tasks_index.json                 # Master list of cataloged tasks
│   ├── jobs_queue.json                  # Pending & completed submission jobs
│   ├── archive_ledger.json              # Checkpoint ledger
│   └── corpus.db                       # SQLite database with FTS5 search
├── platforms/
│   ├── csacademy/tasks/<slug>/          # 662 archived tasks + optimal solutions
│   ├── hackerrank/<contest_slug>/       # Harvested contest runs (e.g. xtreme-shadows-2026)
│   │   ├── <task_slug>/
│   │   │   ├── problem.json             # Specs, constraints, difficulty, max score
│   │   │   ├── statement.html           # Rendered statement
│   │   │   ├── leaderboard.json         # Scoreboard snapshot
│   │   │   └── submissions/             # Accepted Python/C++ solutions
│   │   └── CONTEST_REPLICA_RUNBOOK.md   # Hosting runbook & expansion matrix
│   └── ieeextreme/
│       └── RULES_AND_CONTEST_STRATEGY.md # Official rules, AI governance & scoring strategy
└── scripts/
    ├── deterministic_solver_engine.py   # Zero-AI fast path solver
    ├── ergonomic_cdp_runner.py          # Human-paced CDP submission runner
    └── verify.py                        # Deterministic verification gate
```

---

## 5. Invariant Quality Checks

Before completing or committing harvested batches or contest replicas, verify:
* **KaTeX Math Conversion:** Problem statements must retain authentic LaTeX math (`$formula$` and `$$formula$$`).
* **CodeMirror Synchronization:** HackerRank challenge fields must be written to CodeMirror editor instances directly, ensuring DOM and Backbone model sync.
* **Un-truncated Source Code:** Code must be extracted from editor buffers (`ace.edit` or `CodeMirror`), never from truncated HTML previews.
* **Workspace Compliance:** Never attempt external clipboard injections into locked-workspace tasks; verify offline template library stays within the 100 KB limit.
* **Deterministic Verification:** Always pass `python scripts/verify.py` (zero synthetic commit SHAs, ledger integrity clean) before running `sync.bat`.
