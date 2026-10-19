---
description: "This skill should be used when the user asks about 'Fusemachines syllabus', 'AI fellowship coursework', 'check week N assignment', 'review fellowship quiz', 'text-to-sql architecture', 'telco churn pipeline', 'tree ensembles with SHAP', 'forecasting ensemble S&P 500', 'NEU steel defect CNN', 'OpenCV FreshTrack pipeline', 'Vision Transformers CLIP zero-shot', 'customer support NER CRF', 'agentic routing SLM', 'production RAG assistant', 'agentic eval harness', 'dual-track MLOps Airflow MLflow', 'BiasAperture vision audit', or when /adaptive-workflow requires an instructor-grade reference architecture, mentor-rated benchmark, or SOTA best practice across machine learning, computer vision, NLP, and agentic AI systems."
---

# AI Engineering Fellowship & Instructor Reference Engine (`ai-engineering-fellowship`)

Authoritative AI/ML engineering knowledge base, instructor-grade reference architecture engine, and SOTA best practices repository grounded in Aaradhya's performance across the 24-week **Fusemachines AI Fellowship 2026** (Weeks 1–17 + BiasAperture Capstone).

This skill serves as the primary AI engineering reference module in Aaradhya's **Skill Cluster**, interfacing directly with [`/adaptive-workflow`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/.agents/skills/adaptive-workflow/SKILL.md) to provide mentor-graded architectures, anti-pattern guards, classroom quiz traps, and verified codebases.

---

## 1. Resolution Protocol: Local-First with GitHub Fallback (`INV-RESOLVE-FUSE`)

Whenever retrieving code, configs, or artifacts for any week, execute this two-tier resolution:

1. **Local-First Probe (`F:\FuseAIF2026`)**:
   - Check if the local path `F:\FuseAIF2026\M{X}\WK{Y}` exists on disk.
   - If present: inspect and reuse local files directly (zero latency, zero network overhead, offline-resilient).
2. **GitHub Fallback (`https://github.com/AaradhyaDT/fuseAiF_*`)**:
   - If running in a cloud VM, Google Colab runtime, or fresh clone where `F:\` is unmounted:
   - Resolve to the corresponding GitHub repository link or clone via `gh repo clone AaradhyaDT/fuseAiF_wk*`.

```
Local Root: F:\FuseAIF2026
GitHub Profile: https://github.com/AaradhyaDT
Workspace Mirror: https://github.com/Aaradhya-Dev-Tamrakar/FuseAIF2026
```

---

## 2. Relevancy & Quality Tiers (Mentor-Graded `/100`)

Every project pattern is calibrated by actual mentor marks from Google Classroom (`849624491859`):

- 🌟 **`GOLDEN_REFERENCE` (Score $\ge$ 95/100)**: Peerless reference standard. Direct architectural blueprint for production. Zero architectural penalties.
- ⚖️ **`CALIBRATED_REFERENCE` (Score 80–94/100)**: Production-viable baseline, with specific mentor calibrations or evaluation deltas noted.
- ⚠️ **`CAUTIONARY_ANTI_PATTERN` (Score < 80/100)**: Structurally penalized by the mentor. Must enforce the corrective architectural mandate before re-use.

---

## 3. Master Curriculum, Ratings & Directory Matrix

| Wk | Topic & Core Focus | Mentor Score | Tier | Local Path (`F:\FuseAIF2026\`) | GitHub Remote Fallback |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **01** | Data Wrangling & SQL | **100/100** | `GOLDEN` | [`M1/WK1`](file:///F:/FuseAIF2026/M1/WK1) | `AaradhyaDT/fuseAiF_wk1_data_wrangling` |
| **02** | Software Dev & FastAPI | **75/100** | `CAUTION` | [`M1/WK2`](file:///F:/FuseAIF2026/M1/WK2) | `AaradhyaDT/fuseAiF_wk2_customer_api_app` |
| **03** | GenAI & Text-to-SQL | **100/100** | `GOLDEN` | [`M1/WK3`](file:///F:/FuseAIF2026/M1/WK3) | `AaradhyaDT/fuseAiF_wk3_text2sql` |
| **04** | Statistical ML: Linear Models | **88/100** | `CALIB` | [`M1/WK4`](file:///F:/FuseAIF2026/M1/WK4) | `AaradhyaDT/fuseAiF_wk4_linear_models` |
| **05** | Tree Ensembles & SHAP | **100/100** | `GOLDEN` | [`M2/WK5`](file:///F:/FuseAIF2026/M2/WK5) | `AaradhyaDT/fuseAiF_wk5_telco_churn_ensembles` |
| **06** | Probabilistic Models (PyMC) | **100/100** | `GOLDEN` | [`M2/WK6`](file:///F:/FuseAIF2026/M2/WK6) | `AaradhyaDT/fuseAiF_wk6_probabilistic_models` |
| **07** | Customer Segmentation (RFM) | **93/100** | `CALIB` | [`M2/WK7`](file:///F:/FuseAIF2026/M2/WK7) | `AaradhyaDT/fuseAiF_wk7_customer_segmentation` |
| **08** | S&P 500 Forecasting Ensemble | **100/100** | `GOLDEN` | [`M2/WK8`](file:///F:/FuseAIF2026/M2/WK8) | `AaradhyaDT/fuseAiF_wk8_sp500_forecasting` |
| **09** | Deep Learning CNN Defect (NEU) | **100/100** | `GOLDEN` | [`M3/WK9`](file:///F:/FuseAIF2026/M3/WK9) | `AaradhyaDT/fuseAiF_wk9_neu_defect_cnn` |
| **10** | Image Processing (OpenCV) | **100/100** | `GOLDEN` | [`M3/WK10`](file:///F:/FuseAIF2026/M3/WK10) | `AaradhyaDT/fuseAiF_wk10_image_processing` |
| **11** | Vision Transformers & CLIP | **100/100** | `GOLDEN` | [`M3/WK11`](file:///F:/FuseAIF2026/M3/WK11) | `AaradhyaDT/fuseAiF_wk11_vision_transformers` |
| **12** | NLP & NER Sequence Labeling | **100/100** | `GOLDEN` | [`M3/WK12`](file:///F:/FuseAIF2026/M3/WK12) | `AaradhyaDT/fuseAiF_wk12_ner_customer_support` |
| **13** | Sequence Learning & LSTMs | **100/100** | `GOLDEN` | [`M4/WK13`](file:///F:/FuseAIF2026/M4/WK13) | `AaradhyaDT/fuseAiF_wk13_lstm_text_classification` |
| **14** | Transformers & Agentic Routing | **100/100** | `GOLDEN` | [`M4/WK14`](file:///F:/FuseAIF2026/M4/WK14) | `AaradhyaDT/fuseAiF_wk14_agentic_routing` |
| **15** | Engineering AI Systems (RAG) | **86/100** | `CALIB` | [`M4/WK15`](file:///F:/FuseAIF2026/M4/WK15) | `AaradhyaDT/fuseAiF_wk15_ai_assistant_rag` |
| **16** | Agentic Loop & Eval Harness | **85/100** | `CALIB` | [`M4/WK16`](file:///F:/FuseAIF2026/M4/WK16) | `AaradhyaDT/fuseAiF_wk16_agentic_assistant` |
| **17** | Production MLOps (Dual Track) | **Turned In** | `GOLDEN` | [`M5/WK17`](file:///F:/FuseAIF2026/M5/WK17) | `AaradhyaDT/fuseAiF_wk17_telco_churn_mlops`<br>`AaradhyaDT/fuseAiF_wk17_agentic_mlops` |
| **18** | Trustworthy AI: Guardrails | **Turned In** | `GOLDEN` | [`M5/WK18`](file:///F:/FuseAIF2026/M5/WK18) | `AaradhyaDT/fuseAiF_wk18_trustworthy_ai_guardrails` |
| **Cap** | BiasAperture (Fairness Audit) | **Live Mod 7** | `GOLDEN` | [`fuseai-fellowship/...`](file:///F:/FuseAIF2026/fuseai-fellowship) | `AaradhyaDT/BiasAperture` |

---

## 4. The Three-Layer Framework: First-Principles Engineering Authority

To avoid the **Commodity Trap** (merely teaching or generating syntax and API calls that LLMs produce in seconds), all fellowship codebases, learning modules, and reference architectures are structured around the **Hierarchy of AI Value**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. FIRST-PRINCIPLES ANCHOR (The Non-Commodity Human Question)          │
│    - What is the underlying physical, economic, or data invariant?     │
│    - Why will a naive off-the-shelf model silently fail here?          │
├────────────────────────────────────────────────────────────────────────┤
│ 2. COMMODITY SCAFFOLDING (What You Let AI Generate)                   │
│    - Boilerplate training loops, standard PyTorch/Scikit-Learn code,   │
│      FastAPI routers, and baseline hyperparameters.                    │
├────────────────────────────────────────────────────────────────────────┤
│ 3. EPISTEMIC RED-TEAMING (The Reality & Invariant Filter)             │
│    - How can this model lie to us? (Data leakage, spurious shortcuts)  │
│    - Hard verification gates (Group splits, Bootstrap CIs, Edge tests) │
└────────────────────────────────────────────────────────────────────────┘
```

### Domain Enforcement Invariants:
1. **Tabular ML & Churn (Weeks 4 & 5)**:
   - *First Principle*: In customer churn, temporal ordering matters. Random K-Fold splits cause temporal data leakage.
   - *Epistemic Gate*: SHAP is used as a **data leakage detector** (flagging features like `total_charges` or `tenure` that artificially dominate with near-zero error), not as cosmetic chart padding.
2. **Computer Vision & Defect Detection (Weeks 9 & 11)**:
   - *First Principle*: Industrial cameras suffer from orientation jitter, vibration, and lighting drift. Fixed-crop 99% accuracy models collapse when rotated.
   - *Epistemic Gate*: Out-of-distribution physical stress testing (synthetic rotation, illumination attenuation) verifies the network learned physical defect morphology rather than background texture.
3. **Agentic AI & RAG Systems (Weeks 14–16)**:
   - *First Principle*: Non-deterministic LLMs evaluating non-deterministic LLM agents is circular reasoning.
   - *Epistemic Gate*: Enforce deterministic evaluation harnesses (ground-truth citation matching, context firebreaks `INV-CTX-FIREBREAK`, and low-latency $<50\text{ms}$ SLM routing).
4. **Capstone: BiasAperture (Demographic Bias Auditing)**:
   - *First Principle*: An uncurated dataset with missing provenance cannot legally or scientifically audit fairness.
   - *Epistemic Gate*: Enforce immutable sample-ID manifests, stratified subgroup bootstrap confidence intervals ($B \ge 1000$ for small cells $n < 30$), and strict demarcation ($\text{VERIFIED LIVE} \neq \text{PROPOSED}$).

---

## 5. How `/adaptive-workflow` Interacts with This Skill

When `/adaptive-workflow` triages an incoming objective:
1. **Domain Routing**: Matches user requirements against the 17 fellowship domains.
2. **Relevancy Check**:
   - If adopting a pattern with **$\ge 95/100$**, adopt as a direct golden architecture.
   - If adopting a pattern with **80–94/100**, adopt baseline but review the identified delta in the dossier.
   - If building a FastAPI microservice, consult **Week 2** to enforce the mentor's `APIRouter` structure and reject single-file monolithic layouts.
3. **Progressive Reference Loading**:
   - Instruct Antigravity to load only the specific week reference (`references/weeks/wk{N}_*.md`) required for the active subtask to preserve token headroom.

---

## 6. Supporting Documentation & Resources

### SOTA Best Practices Index
- **`references/best_practices_index.md`**: Cross-cutting synthesis of modern production patterns (SQL, ML pipelines, PyTorch, RAG, and MLOps).

### Classroom Quiz Bank
- **`references/quiz_bank.md`**: Consolidated question bank, edge-case traps, and mathematical formulas extracted across all 17 weekly quizzes.

### Fast Local Query CLI Utility
- Run `python scripts/fuse_cli.py list` to inspect curriculum status and paths.
- Run `python scripts/fuse_cli.py lookup "<topic>"` to retrieve golden templates and anti-patterns.
- Run `python scripts/fuse_cli.py resolve <N>` to test local vs GitHub fallback resolution.
