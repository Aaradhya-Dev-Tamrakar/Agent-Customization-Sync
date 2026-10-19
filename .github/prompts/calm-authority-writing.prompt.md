---
description: "This skill should be used when the user asks for 'calm authority writing', 'calm engineering authority', 'write an engineering blog post', 'write a release report', 'draft a system card', 'create a technical announcement', 'write a developer migration guide', 'audit technical writing', 'write a case study', 'brainstorm an architecture spec', or mentions drafting publications, benchmarks, hardware/ML specs, or safety/fairness dossiers in a calm-authority engineering voice."
---

# Calm Authority Writing — The Multi-Domain Engineering Standard (v2.2)

This skill codifies a mechanism-first, zero-hype technical writing standard that adapts to the evidence available in each project. Verify project maturity and implementation status against current source artifacts before drafting; repository names and prior examples do not establish current state.

---

## 1. Core Philosophy: The Whiteboard Test & Empirical Proof

The foundation of high-trust technical communication is **calm authority**:
> **Write as though you are mapping a real system for a sharp colleague at a whiteboard, or submitting an unredacted technical disclosure to a rigorous auditor. State the physical or computational constraint, explain the mechanism that resolves it, and anchor the outcome in either verifiable data (`E3`/`E4`) or falsifiable first-principles bounds (`E1`/`E2`).**

Trust is governed by an immutable relationship:
$$\text{Trust} = \text{Precision} + \text{Scope Boundaries} + \text{Calibrated Proof}$$

### The Three Pillars
1. **Functional Precision**: Define systems by their mechanical inputs, state transitions, and outputs rather than promotional abstractions.
2. **Explicit Scope Boundaries**: Proactively declare what the system *cannot* do. Stating non-goals, hardware/runtime bottlenecks, and unsupported failure modes is the strongest signal of engineering credibility.
3. **Stage-Calibrated Proof**: Match the proof standard to the system's lifecycle state—using first-principles capacity envelopes and falsification criteria during ideation (`E1`–`E2`), cycle-accurate qualifiers in simulation (`E3 Sim`), and measured hardware/dataset traces in production (`E4`).

---

## 2. 2D Pre-Flight Router: Depth Tier (L1–L5) × Use-Case Domain (U0–U5)

Before drafting, resolve the task's **2D routing coordinate `(Tier, UseCase)`**:
- **Axis 1 (`L1`–`L5`)** governs document length, structural template, and execution posture.
- **Axis 2 (`U0`–`U5`)** governs domain-specific proof standards, required technical artifacts, and ecosystem hooks.

### Axis 1: Surface Depth Tiers (`L1`–`L5`)
| Tier | Surface & Intent | Word Count | Default Execution Mode | Loaded Structural Reference |
| :--- | :--- | :--- | :--- | :--- |
| **`L1`** | **Micro-Surface**: Issue specs, RFC stubs, PRs, commit notes, 3-bullet portfolio blurbs. | 100–300 | Solo Fast-Path (0 files) | Execute inline via Sections 3 & 4. |
| **`L2`** | **Editorial Narrative**: Sim-to-real post-mortems, engineering blog posts, build logs. | 800–1,500 | Solo Direct | `references/narrative-and-case-studies.md` |
| **`L3`** | **Technical Spec**: Architecture RFCs, firmware/hardware contracts, MCP tool schemas. | 1,000–3,000 | Solo Direct | `references/migration-and-developer-specs.md` |
| **`L4`** | **Empirical Evaluation**: Quantization ablations, control-loop & simulation benchmarks. | 2,000–5,000 | Solo or `/agent-teams` | `references/benchmarks-and-ablations.md` |
| **`L5`** | **System Audit & Dossier**: Regulatory compliance dossiers, full thesis/capstone reports. | 5,000–30,000+ | `/agent-teams` or `/fleet-orch` | `references/audits-governance-and-safety.md` |

### Axis 2: Domain Use-Case Overlays (`U0`–`U5`)
| Code | Use-Case Domain | Canonical Repository Anchor | Mandatory Proof & Artifact Standard | Linter Flag & Ecosystem Hook |
| :--- | :--- | :--- | :--- | :--- |
| **`U0`** | **Systems Ideation & Architecture RFCs** | `Aaradhya-Dev-Tamrakar/brainstorm` (`E1`–`E2`) | Back-of-the-envelope (BotE) resource bounds, rejected alternatives matrix, and explicit falsification test criteria. | `--domain brainstorm` (`graphify` `[[wikilinks]]`) |
| **`U1`** | **Embedded, Robotics & Parametric CAD** | `Aaradhya-Dev-Tamrakar/SPARK` (thesis/report evidence; verify current status)<br>`AaradhyaDT/Gesture-Controlled-Self-Balancing-Robot` (verify current artifacts) | Report measured hardware values only when supported by logs or bench records; clearly label targets and simulations. SPARK's documented training convention is 100 Hz with 200-sample windows; the planned 200 Hz logger is not evidence of an implemented logger. | `--domain embedded` (`super-nlm` unit spacing) |
| **`U2`** | **Architecture & Network Simulation** | `STRANGLER-IPU` (`E3 Sim`), `epanet-mcp` | Pin simulator assumptions, line-rate (`6G sub-THz`), interconnect spec (`CXL 3.0`), queue depth, and $p99$ tail latency. | `--domain arch-sim` (Enforce `E3 Sim` qualifiers) |
| **`U3`** | **Applied ML & Fairness Auditing** | `AaradhyaDT/BiasAperture` (research diagnostic; verify current report and implementation) | Pin dataset split and sample size. State the actual CI method and resample count per metric; distinguish implemented surrogate attribution from deferred SHAP; suppress scored values for $n < 30$. Do not claim regulatory compliance. | `--domain ml-audit` ($n < 30$ `.badge-guard` suppression) |
| **`U4`** | **AI Infra, DSP & MCP Servers** | `Claude Desktop DSP`, `typora-mcp`, `localsend-mcp`, `google-classroom-mcp` | Deterministic JSON-RPC / MCP input-output schemas, token-budget deltas, idempotency guarantees, and failure codes. | `--domain mcp-infra` (Runnable JSON schema diffs) |
| **`U5`** | **Knowledge Synthesis & Portfolio** | `aaradhyadt.github.io`, `super-nlm`, `graphify`, `portfolio-project-manager` | 3 active-verb impact bullets, `schema.org` JSON-LD blocks, Obsidian `[[wikilinks]]`, and synced lifecycle badges. | `--domain knowledge` (`scripts/add_project.py`) |

---

## 3. Whiteboard Rhetoric & Epistemic Calibration

### 3.1 The Constraint $\rightarrow$ Mechanism $\rightarrow$ Consequence Arc
Never introduce a module by listing its features in isolation:
1. **Constraint**: State the physical, mathematical, or operational bottleneck, citing a trace or labelling it as a hypothesis.
2. **Mechanism**: Explain the verified transformation, or label a proposed mechanism as a design target.
3. **Consequence**: Report a measured outcome only when a reproducible result supports it; otherwise state the planned measurement.

### 3.2 Concrete Trace Before Abstract Law
Anchor the reader in a concrete failure log, register state, JSON payload, or physical oscillation before stating the general architectural principle.

### 3.3 Evidence Gate (`E1`–`E4` Verb Calibration)
Match verb certainty strictly to the project's maturity state:
- **`E1` (Conceptual / `brainstorm` RFC)**: Use *models, proposes, targets, bounds theoretically*. Must include a **Falsification Gate** stating what physical measurement or benchmark will invalidate the design.
- **`E2` (Bench Prototype / Isolated Module)**: State explicitly which subsystem is hardware-verified and which remains mocked or stubbed.
- **`E3 Sim` (Cycle / Numerical Simulation — e.g., `STRANGLER-IPU`)**: Prefix performance claims with explicit simulation scope (*"Under cycle-accurate CXL 3.0 simulation..."*). Never use unqualified hardware-completion verbs.
- **`E4` (specific physical hardware / full dataset evaluation verified)**: Use deterministic verbs only for the subsystem and evaluation supported by physical traces or a complete, reproducible split. A project or report is not automatically E4 as a whole.

---

## 4. The 10 Universal Invariant Writing Rules

1. **Title = Statement of Factual State**: Use a declarative sentence or precise noun phrase stating what exists, what changed, or what trade-off is bounded. Never use clickbait, listicles, or rhetorical questions.
2. **1-Sentence Empirical or Bounding Thesis**: Open with a self-contained thesis stating the core mechanism and either its sourced outcome (`E3`–`E4`) or its explicitly theoretical capacity envelope (`E1`–`E2`). Never invent a number to fill the sentence.
3. **Dual Lexical & Syntactic Anti-AI Blacklist**:
   - **Lexical Ban**: Prohibit promotional superlatives (*revolutionary, game-changing, groundbreaking, unleash, supercharge, seamless, cutting-edge, magic, effortlessly, next-gen, robust, delve*). Consult `references/vocabulary_cheatsheet.md`.
   - **Syntactic Ban**: Prohibit negation-contrast clichés (*"It is not X, it is Y"*, *"Not selling. Just explaining."*), hollow participial tail clauses (*"...ensuring high reliability and enabling seamless scaling"*), verb nominalizations (*"performs quantization of"* $\rightarrow$ *"quantizes"*), and compulsive three-item adjective lists.
4. **Functional Precision in Definition**: Define any mechanism, component, or pipeline stage in 10 to 20 concrete words stating its input, transformation, and output.
5. **Explicit Scope Boundaries & Non-Goals**: Dedicate explicit prose to what the system *does not* do. Declare unsupported hardware configurations, rejected design alternatives (`U0`), and out-of-distribution failure modes prominently.
6. **Controlled Baselines & Environmental Pinning**: Always pin the execution or modeling environment (MCU clock/SRAM, simulator parameters, precision format `FP32` vs. `INT8`, dataset split, sample size $N$, and baseline comparator).
7. **Multi-Objective Tradeoff & Pareto Transparency**: Never report a gain in one metric without stating its cost in another (e.g., accuracy vs. INT8 SRAM footprint, balancing response vs. stepper resonance, or throughput vs. tail latency).
8. **Causal Flow & Cadence Variance**:
   - Keep one primary claim per paragraph (2 to 5 sentences).
   - Connect sentences via explicit cause-and-effect transitions (*because, consequently, when, whereas*) rather than meta-signposting (*"In this section, we will discuss..."*).
   - Vary sentence length: follow a complex multi-clause mechanical explanation with a short declarative consequence.
9. **Deterministic, Verifiable Artifacts**: Code blocks, firmware snippets, and CLI invocations must be copy-pasteable and runnable. Architecture and MCP specs (`U4`) must include concrete before/after configuration or JSON schema diffs.
10. **Actionable Next Steps over Redundant Summaries**: Never restate the introduction in the conclusion. Conclude with reproducible CLI commands, issue/PR pointers, falsification experiments (`U0`), or open engineering questions.

---

## 5. Intentional Dual-Namespace Governance (`Aaradhya-Dev-Tamrakar` vs. `AaradhyaDT`)

The author maintains an intentional two-namespace GitHub architecture separating active R&D workspaces from curated production releases. **Never rewrite or normalize URLs across namespaces:**

### Namespace A: `Aaradhya-Dev-Tamrakar` (Active R&D, Ideation & In-Flight Capstone)
1. **`brainstorm` (`E1`–`E2` — Ecosystem Ideation, RFCs & Architecture Exploration)**:
   - **Canonical URL**: `https://github.com/Aaradhya-Dev-Tamrakar/brainstorm`
   - **Default Routing**: `(L1–L3, U0)`
   - **Role**: Staging ground for multi-domain system designs, trade-off matrices, and tool orchestration workflows before promotion to standalone repositories.
2. **`SPARK` (wearable fall-detection thesis; implementation status varies by subsystem)**:
   - **Canonical URL**: `https://github.com/Aaradhya-Dev-Tamrakar/SPARK` (Issue Tracker: `https://github.com/Aaradhya-Dev-Tamrakar/SPARK/issues`)
   - **Default Routing**: `(L1/L3/L4, U1)`
   - **Role**: Thesis reports describe a wearable fall-detection system. The archived model evaluation is offline; firmware inference, sensor acquisition, transports, and on-device performance must not be described as implemented without new evidence. The documented training convention is 100 Hz and 200 samples over 2 seconds; 200 Hz was a planned logger target. Do not infer hardware or clinical validation from offline model metrics.

### Namespace B: `AaradhyaDT` (Curated Production, Release & Portfolio Namespace)
3. **`BiasAperture` (diagnostic fairness-audit research project)**:
   - **Canonical URL**: `https://github.com/AaradhyaDT/BiasAperture`
   - **Default Routing**: `(L4/L5, U3)`
   - **Role**: A diagnostic research platform evaluated with FairFace; UTKFace was removed from scope. Describe the active backend and statistical implementation from current code. The subgroup bootstrap path currently uses percentile intervals with a 200-resample default; the separate global path uses BCa and a larger resample budget. Surrogate attribution models demographic-label association and is not image-level SHAP or causal explanation. Reports support analysis and do not establish compliance or regulatory readiness.
4. **`Gesture-Controlled-Self-Balancing-Robot` (`E4 Completed` — Control Systems & Robotics)**:
   - **Canonical URL**: `https://github.com/AaradhyaDT/Gesture-Controlled-Self-Balancing-Robot`
   - **Default Routing**: `(L2/L4, U1)`
   - **Role**: Completed hardware-verified two-wheeled self-balancing robot (C++ PID control, MPU6050 sensor fusion, DRV8825 stepper actuation, MediaPipe gesture routing) documenting the MATLAB-to-hardware transfer and turn-induced pitch stabilization.

---

## 6. Adaptive Execution Postures (Capability, Not Overhead)
```
[Task Scope]
├── Default (90% of tasks) ──> Solo Direct Execution (Immediate, zero subagents)
├── Explicit /agent-teams ───> Multi-Agent Team (Scout -> Reviewer -> Writer -> Lead)
└── Explicit /fleet-orch ───> Headless Batch Swarm (SKU DAG -> Pooled Workers -> Drive Sync)
```
1. **Mode 1: Solo Direct Execution (Default)**: Immediate execution for `L1`–`L3` tasks, `U0` brainstorming docs, and standard `L4` drafts.
2. **Mode 2: Multi-Agent Team Capability (`/agent-teams-orchestration`)**: For high-stakes `L4`/`L5` audits requiring adversarial verification (Scout $\rightarrow$ Reviewer $\rightarrow$ Writer). Consult `references/swarm-and-fleet-capabilities.md`.
3. **Mode 3: Fleet Swarm Capability (`/fleet-orchestrator`)**: Enqueues `assets/sku-templates/model_report_pack.json` into `orchestrator-state/tasks/`. Consult `references/swarm-and-fleet-capabilities.md`.

---

## 7. Ecosystem Compatibility Fast-Pointers

- **`compliance-report-harmonizer` (`U3`)**: Adhere to the 5-section hierarchy and suppress cohorts with $n < 30$ using `.badge-guard` and `<details class="insufficient-block">`.
- **`portfolio-project-manager` (`U5`)**: When onboarding tools via `scripts/add_project.py`, generate 3 active-verb, zero-hype bullet points matching Tier `L1` format and preserve exact namespace URLs (`Aaradhya-Dev-Tamrakar` vs. `AaradhyaDT`).
- **`github-workflow` (`U0`/`U1`)**: Use Tier `L1` format for `SPARK` and `brainstorm` issues and PR descriptions (declarative title, 1-sentence thesis, verification/falsification proof, explicit non-goals) so merged PRs cleanly close linked issues.
- **`super-nlm` (`U1`/`U5`)**: Include `schema.org` JSON-LD and LaTeX math blocks (with spaces before physical units, e.g., `200 Hz`, `0.5 mm`) for NotebookLM ingestion.
- **`graphify` (`U0`/`U5`)**: Connect `brainstorm` notes and research findings into the local Obsidian graph using `[[wikilinks]]`.

---

## 8. Deterministic Style Verification & Reference Tree

Audit any document against v2.2 standards (tier geometry, domain proof rules, syntactic anti-AI filters, and namespace preservation) via CLI:
```powershell
python "F:\Aaradhya-Dev-Tamrakar\brainstorm\.agents\skills\calm-authority-writing\scripts\audit_calm_writing.py" --tier L3 --domain embedded <path-to-file.md>
```

### Consolidated Reference Guides (`references/`)

- **`references/vocabulary_cheatsheet.md`** — Banned lexical hype list, banned syntactic AI patterns, and mechanical replacements.
- **`references/narrative-and-case-studies.md`** — `L2` structural formulas for engineering post-mortems (`GCSBR`) and architecture narratives.
- **`references/migration-and-developer-specs.md`** — `L3` RFCs (`brainstorm`), firmware contracts (`SPARK`), and MCP tool schemas (`U4`).
- **`references/benchmarks-and-ablations.md`** — `L4` pinned baseline tables, quantization/latency Pareto frontiers, and simulation bounds.
- **`references/audits-governance-and-safety.md`** — `L5` fairness auditing (`BiasAperture`), EU AI Act / NIST AI RMF mapping, and $n < 30$ suppression protocols.
- **`references/swarm-and-fleet-capabilities.md`** — Execution protocols for `/agent-teams` and `/fleet-orchestrator`.
- **`references/ecosystem-compatibility.md`** — Complete integration SOPs across the interacting ecosystem skills.

### Worked Examples (`examples/`)

Examples are writing patterns, not project evidence. Verify every project-specific statement against current artifacts before reuse. Benchmark and audit examples must use clearly marked placeholders unless they cite reproducible evidence.

- **`examples/l1-spark-issue-and-portfolio.md`** — `(L1, U1/U5)`: evidence-labelled issue and portfolio pattern for `SPARK`.
- **`examples/l2-gcsbr-sim-to-real-postmortem.md`** — `(L2, U1)`: `GCSBR` case study (`AaradhyaDT/Gesture-Controlled-Self-Balancing-Robot`).
- **`examples/l3-spark-edge-telemetry-spec.md`** — `(L3, U0/U1)`: proposed interface contract template; no implementation claim.
- **`examples/l4-spark-quantization-benchmarks.md`** — `(L4, U1)`: evidence-gated benchmark template; no fabricated hardware metrics.
- **`examples/l5-biasaperture-eu-ai-act-audit.md`** — `(L5, U3)`: diagnostic audit template; no compliance conclusion or invented subgroup results.
