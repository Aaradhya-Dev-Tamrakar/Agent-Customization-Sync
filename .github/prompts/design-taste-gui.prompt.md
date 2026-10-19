---
description: "Master native desktop, mobile, and client application GUI design system embodying Aaradhya's signature design language (The ADT Application Standard). Enforces high-craft visual ergonomics, calm telemetry palettes, anti-emoji policy, 3-tier AI-slop disqualification gate, dynamic theme switching, self-healing geometry and font cascades, and OS shell integration."
---

# Master GUI Design & The ADT Application Standard

This skill establishes the authoritative, production-level visual identity, architectural ergonomics, and interaction standards for all native desktop, mobile, and client GUI applications developed by Antigravity across Aaradhya's ecosystem.

It ensures that every GUI—regardless of programming language (Python, C#, Rust, C++, Kotlin) or UI framework (Tkinter/TTK, PyQt/PySide, WPF/WinUI, Tauri/Webview, Jetpack Compose)—shares the unmistakable **ADT Signature Taste of Design**: calm, high-craft, distraction-free, and mathematically grounded.

---

## 1. Core Architectural Axioms (The ADT Design DNA)

1. **Context & Telemetry Over Chrome**:
   Navigation and application chrome must be ambient and whisper-quiet. The user's cognitive bandwidth belongs 100% to inspecting data, monitoring agents, running workflows, or reading code—never wrestling with flashy UI noise.
2. **Easy on the Eye (Visual Ergonomics & Glare Elimination)**:
   - Zero high-frequency visual vibration or harsh pure `#000000` pitch blacks.
   - Grounded, warm, paper-adjacent dark slate canvases (`#0a0d12` to `#0f141c`).
   - Text contrast strictly satisfies WCAG AAA ($\ge 7:1$ for body prose/telemetry, $\ge 4.5:1$ for headers).
3. **The Single-Temperature Accent Discipline**:
   - The primary brand and telemetry accent is **Architectural Hardware Gold** (`#d4a85a`).
   - The interactive control accent is **Electric Research Cobalt** (`#2563eb` / `#3b82f6`).
   - Semantic status indicators use calibrated single-hues: Cactus Green (`#22c55e`) for active, Amber (`#f59e0b`) for pending/warning, Terracotta (`#ef4444`) for stopped/error, Muted Slate (`#94a3b8`) for idle/standby.
4. **The Anti-Emoji Policy in Production UI [STRICT ENFORCEMENT]**:
   - Never use raw system emojis (⚡, 📊, 🤖, 📋, 🪟, 📜, 🔄, 🚀, 🛑) in window titles, header bars, notebook tabs, table rows, or interface buttons.
   - Use clean monochrome typographic glyphs (`●`, `▶`, `■`, `↻`, `✦`, `⌘`, `⌥`) or vector icons with uniform line weights.
5. **Ergonomic Table & Grid Geometry**:
   - Treeview and table rows must maintain `rowheight >= 28px` (standard: `30px`) to prevent cramped data density.
   - Numbers and metrics right-aligned; status dots center-aligned; text labels left-aligned.
   - IDs, hex SHAs, SKU codes, and quotas must be rendered in high-legibility monospace fonts (`Cascadia Code`, `JetBrains Mono`).

---

## 2. The 3-Tier AI-Slop Disqualification Matrix & Zero-Tolerance Gate

Any agent or code generation proposing patterns in the "Disqualified AI-Slop" column **fails the verification gate** and must be rewritten with the "ADT Grounded Engineering Standard":

| Tier | Disqualified AI-Slop Pattern (IMMEDIATE REJECTION) | ADT Grounded Engineering Standard (MANDATORY) |
| :--- | :--- | :--- |
| **Tier 1: Visual & Aesthetic Slop** | • Neon AI-purple/violet gradients (`#a855f7`, `#8b5cf6`, `#7c3aed`)<br/>• Faux-cyber glowing borders (`box-shadow: 0 0 25px`)<br/>• Raw system emojis in chrome (⚡, 📊, 🤖, 📋, 🪟, 📜, 🔄, 🚀, 🛑)<br/>• Cartoonish bubbly radii or uncalibrated full-pill widgets | • Grounded Obsidian Slate (`#0a0d12` / `#0f141c`)<br/>• Subtle 1px borders (`#1e2736`) with zero visual vibration<br/>• Optical status dots (`●`) and clean unicode glyphs (`▶`, `■`, `↻`, `✦`)<br/>• Tight, disciplined radii (`4px` to `8px`) matching Windows 11 Fluent geometry |
| **Tier 2: Content & Copywriting Slop** | • Sycophantic AI buzzwords (*supercharge, unleash, delve, tapestry, plethora, revolutionary, cutting-edge, seamlessly orchestrate*)<br/>• Vague, ungrounded performance claims (*10x faster, ultimate solution*)<br/>• Redundant placeholder prose (*This is where your items appear*) | • Crisp factual telemetry (*27x pooled Copilot workers · 5,400 monthly quota*)<br/>• Exact subsystem metrics, Big-O bounds, and authentic commit hashes<br/>• Actionable empty-state hints (*Press ✦ Submit SKU [Ctrl+N] or F5 to refresh*) |
| **Tier 3: Engineering & Code Slop** | • Bare `except: pass` silencing critical UI failures<br/>• Hardcoded fixed-coordinate layouts (`place(x=120, y=80)`) breaking on high-DPI<br/>• Synthetic fake mock datasets or static simulated graphs<br/>• Hallucinated widget attributes or non-portable third-party binary wheels | • Defensive logging with exact error triage<br/>• Responsive grid/pack geometry with Per-Monitor DPI v2 awareness<br/>• Live runtime state from real SSOT ledgers (`active_fleet.json`, tasks)<br/>• 100% standard-library portability (`tkinter`, `ttk`, ctypes) |

---

## 3. Dynamic, Self-Healing & Future/Feature Progressive Invariants

### A. Dynamic Architecture
1. **Dynamic Theme Switching**:
   Applications must support seamless runtime switching (`Ctrl+T` or toolbar button) between **ADT Telemetry Dark Slate** and **ADT Editorial Paper/Ink** without requiring application restarts.
2. **Dynamic DPI Scaling & Zoom Ladder**:
   Provide smooth viewport zooming (`Ctrl + =` / `Ctrl + -` / `Ctrl + 0` and `Ctrl + MouseWheel`) stepping through scale factors `[0.75x, 0.85x, 1.0x, 1.15x, 1.25x, 1.5x, 1.75x, 2.0x]`.
3. **Fluid Viewport Reflow**:
   Avoid fixed-size canvas locks. Main layout containers must expand and reflow gracefully from 1080x700 laptops up to 4K desktop monitors.

### B. Self-Healing Substrate
1. **Off-Screen Geometry Sanitizer**:
   When reading saved window coordinates (`x`, `y`, `width`, `height`), the application must validate that the window bounds intersect the active virtual screen area (`GetSystemMetrics(SM_CXVIRTUALSCREEN)`). If the window was previously closed on a detached external monitor, it **self-heals** by recentering on the primary display.
2. **Resilient Font Cascade (`resolve_safe_font`)**:
   Never crash on missing fonts. Typography must cascade through safe fallbacks:
   - Primary display: `Segoe UI Variable Display` $\rightarrow$ `Segoe UI Semibold` $\rightarrow$ `Helvetica Neue` $\rightarrow$ `Arial`.
   - Primary body: `Segoe UI Variable Text` $\rightarrow$ `Segoe UI` $\rightarrow$ `Inter` $\rightarrow$ `system-ui`.
   - Monospace telemetry: `Cascadia Code` $\rightarrow$ `Consolas` $\rightarrow$ `JetBrains Mono` $\rightarrow$ `monospace`.
3. **Daemon Circuit Breaker with Exponential Backoff**:
   Background telemetry loops and API pollers must never crash or block the UI thread on connection drops. They transition to an ambient "Reconnecting..." state and retry with exponential backoff (e.g. 1s, 2s, 4s, max 15s).
4. **Safe Ledger Defaults**:
   If state JSON files or task folders are missing on disk, the application initializes empty schema-valid structures in memory rather than raising unhandled exceptions.

### C. Future & Feature Progressive
1. **Modular Subsystem Registry**:
   Tabs, SKU pipelines, worker adapters, and telemetry graphs must be structured as modular components registered in a central registry, allowing new capabilities to be added without modifying core window loops.
2. **Progressive Disclosure**:
   The default interface view shows high-level, calm KPI telemetry. Granular diagnostics, task parameters, and raw JSON payloads are revealed via expandable side-drawers or sub-inspectors.

---

## 4. Color Science & Token Specification

### A. Dual Canonical Archetypes

#### Archetype 1: ADT Telemetry Dark Slate (Command Centers, Swarm Monitors, Terminals)
```python
ADT_CANVAS_BASE = "#0a0d12"      # Deep obsidian substrate
ADT_SURFACE_MAIN = "#0f141c"     # Primary container surface
ADT_SURFACE_CARD = "#141923"     # Elevated card surface
ADT_SURFACE_CARD_ALT = "#19202c" # Hover / secondary card surface
ADT_SURFACE_INPUT = "#0c1017"    # Inset input & terminal background

ADT_BORDER_SUBTLE = "#1e2736"    # Whisper-quiet 1px divider
ADT_BORDER_ACTIVE = "#2d3a50"    # Focused or selected border

ADT_TEXT_PRIMARY = "#f1f5f9"     # High-contrast prose & values
ADT_TEXT_SECONDARY = "#94a3b8"   # Secondary labels & headers
ADT_TEXT_MUTED = "#64748b"       # Timestamps & inactive captions

ADT_GOLD = "#d4a85a"             # ADT Monogram & Quota Telemetry
ADT_COBALT = "#3b82f6"           # Primary Interactive Control
ADT_COBALT_HOVER = "#2563eb"     # Control Hover
ADT_CACTUS = "#22c55e"           # Active / Online / Running
ADT_TERRACOTTA = "#ef4444"       # Fault / Error / Aborted
ADT_AMBER = "#f59e0b"            # Pending / Warning / Queued
```

#### Archetype 2: ADT Editorial Paper & Ink (Document Readers, Note Workbenches)
```python
ADT_PAPER_GROUND = "#f6f4ef"     # Warm editorial newsprint
ADT_PAPER_SURFACE = "#ffffff"    # Crisp tactile paper card
ADT_PAPER_SUBTLE = "#eae6de"     # Recessed panels
ADT_PAPER_BORDER = "#ded8cb"     # Paper-and-ink 1px border

ADT_INK_PRIMARY = "#141518"      # Deep typographic ink
ADT_INK_SECONDARY = "#4a4c52"    # Secondary body text
ADT_INK_MUTED = "#7b7e87"        # Footnotes and captions

ADT_PAPER_COBALT = "#2563eb"     # Editorial electric research blue
ADT_PAPER_TERRACOTTA = "#d97757" # Claude clay / warm terracotta
ADT_PAPER_CACTUS = "#556862"     # Sage / cactus fluency
```

---

## 5. Interaction & Ergonomics Standard

### A. Power-User Keyboard Layer
Every ADT application must bind these universal hotkeys:
- `F5` / `Ctrl+R`: Force immediate global refresh of all telemetry.
- `Ctrl+1` through `Ctrl+9`: Switch directly to tab index.
- `Ctrl+F` or `Ctrl+K`: Focus search/filter input.
- `Ctrl+T`: Toggle between Dark Slate and Paper/Ink theme.
- `Ctrl+=` / `Ctrl+-` / `Ctrl+0`: Zoom in, zoom out, reset zoom (100%).
- `Esc`: Clear search filters, dismiss drawers, or close dialogs.
- **Footer Status Bar Legend**: The bottom status bar must display clean keycap hints:
  `F5 Refresh  ·  Ctrl+1..5 Tabs  ·  Ctrl+T Theme  ·  Esc Dismiss`

### B. Designed Empty-State Watermarks
Never display a plain empty rectangle. If a table, queue, or search view has 0 items, render a centered typographic empty state:
- Clean unicode emblem: `✦` or `⌥` (size: 20pt, color: `ADT_TEXT_MUTED`).
- Title: Semibold primary text (e.g., `No Tasks in Queue`).
- Actionable Hint: Secondary text with keyboard shortcut (e.g., `Press ✦ Submit SKU [Ctrl+N] or F5 to refresh telemetry.`).

### C. In-Window Floating Toasts & Transient Status Flashes
- **No Blocking Dialogs for Routine Feedback**: Do not use `messagebox.showinfo()` for normal actions.
- Use an **In-Window Floating Toast**: A floating card pill anchored in the bottom-right or top-center that slides in, displays the confirmation (`● SKU submitted successfully`), and automatically fades after 3 seconds.
- Modal dialogs (`messagebox.askyesno`) are reserved **strictly for irreversible destructive operations** (e.g., "Kill all 27 worker processes?").

### D. Window Geometry Persistence
Applications must automatically serialize window geometry on close:
```json
{
  "x": 140,
  "y": 80,
  "width": 1280,
  "height": 860,
  "is_maximized": false,
  "active_tab": "Overview & Telemetry",
  "theme": "dark"
}
```
On startup, coordinates must be passed through the self-healing sanitizer before applying to `geometry()`.

---

## 6. Multi-Toolkit Rosetta Stone Recipes

### A. Python Tkinter & TTK (Zero-Dependency Engine)
```python
import ctypes
import tkinter as tk
from tkinter import ttk

def enable_windows_high_dpi_and_dark_titlebar(root: tk.Tk):
    """Enforce Per-Monitor DPI v2 and native Windows 11 dark titlebar."""
    if ctypes.windll:
        try:
            # Per-Monitor DPI v2 (-4)
            ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
        except Exception:
            pass
        root.update_idletasks()
        try:
            hwnd = ctypes.windll.user32.GetParent(root.winfo_id()) or root.winfo_id()
            value = ctypes.c_int(1)
            # DWMWA_USE_IMMERSIVE_DARK_MODE = 20 (Windows 11) / 19 (Windows 10)
            for attr in (20, 19):
                if ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    ctypes.c_void_p(hwnd), ctypes.c_uint(attr), ctypes.byref(value), ctypes.sizeof(value)
                ) == 0:
                    break
        except Exception:
            pass

def init_adt_ttk_theme(style: ttk.Style, is_light: bool = False):
    """Configure TTK clam theme with ADT Telemetry Dark Slate tokens."""
    style.theme_use("clam")
    bg_main = "#0f141c" if not is_light else "#f6f4ef"
    bg_card = "#141923" if not is_light else "#ffffff"
    text_primary = "#f1f5f9" if not is_light else "#141518"
    border = "#1e2736" if not is_light else "#ded8cb"
    
    style.configure(".", background=bg_main, foreground=text_primary, font=("Segoe UI Variable Text", 9))
    style.configure("Treeview", background=bg_card, foreground=text_primary, fieldbackground=bg_card,
                    rowheight=30, borderwidth=0)
    style.configure("Treeview.Heading", background=bg_main, foreground="#94a3b8",
                    font=("Segoe UI Variable Text", 8, "bold"), relief="flat", borderwidth=1)
    style.configure("TNotebook", background=bg_main, borderwidth=0, tabmargins=[14, 6, 14, 0])
    style.configure("TNotebook.Tab", background=bg_card, foreground="#94a3b8", padding=[16, 8],
                    font=("Segoe UI Variable Display", 9, "bold"), borderwidth=0)
    style.map("TNotebook.Tab",
              background=[("selected", "#19202c" if not is_light else "#eae6de")],
              foreground=[("selected", text_primary)])
```

### B. Python / C++ PyQt6 & PySide6 (QSS Stylesheet)
```css
QMainWindow {
    background-color: #0a0d12;
}
QWidget {
    color: #f1f5f9;
    font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
    font-size: 13px;
}
QTabWidget::pane {
    border: 1px solid #1e2736;
    background-color: #0f141c;
    border-radius: 6px;
}
QTabBar::tab {
    background-color: #141923;
    color: #94a3b8;
    padding: 8px 18px;
    font-weight: 600;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #19202c;
    color: #f1f5f9;
    border-bottom: 2px solid #3b82f6;
}
QTableView {
    background-color: #141923;
    alternate-background-color: #0f141c;
    border: 1px solid #1e2736;
    gridline-color: #1e2736;
    selection-background-color: #1e2736;
    selection-color: #ffffff;
}
QHeaderView::section {
    background-color: #0f141c;
    color: #94a3b8;
    font-weight: bold;
    border: none;
    border-bottom: 1px solid #1e2736;
    padding: 6px;
}
```

### C. C# / WPF & XAML (ResourceDictionary)
```xml
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <!-- ADT Signature Dark Slate Brushes -->
    <SolidColorBrush x:Key="AdtCanvasBase" Color="#0A0D12" />
    <SolidColorBrush x:Key="AdtSurfaceMain" Color="#0F141C" />
    <SolidColorBrush x:Key="AdtSurfaceCard" Color="#141923" />
    <SolidColorBrush x:Key="AdtBorderSubtle" Color="#1E2736" />
    <SolidColorBrush x:Key="AdtTextPrimary" Color="#F1F5F9" />
    <SolidColorBrush x:Key="AdtTextSecondary" Color="#94A3B8" />
    <SolidColorBrush x:Key="AdtGold" Color="#D4A85A" />
    <SolidColorBrush x:Key="AdtCobalt" Color="#3B82F6" />
    <SolidColorBrush x:Key="AdtCactus" Color="#22C55E" />

    <!-- Modern Flat Card Style -->
    <Style x:Key="AdtCard" TargetType="Border">
        <Setter Property="Background" Value="{StaticResource AdtSurfaceCard}" />
        <Setter Property="BorderBrush" Value="{StaticResource AdtBorderSubtle}" />
        <Setter Property="BorderThickness" Value="1" />
        <Setter Property="CornerRadius" Value="6" />
        <Setter Property="Padding" Value="14" />
    </Style>
</ResourceDictionary>
```

---

## 7. OS Shell Integration & Win32 Invariants

1. **Per-Monitor DPI v2 Awareness**:
   Must call `SetProcessDpiAwarenessContext(-4)` before window creation to guarantee crisp fonts and sharp vector graphics across all display scaling levels.
2. **Native Dark Mode Titlebar**:
   Must call `DwmSetWindowAttribute` with attribute `20` (or `19`) to instruct Windows Desktop Window Manager to render dark chrome.
3. **Interactive Thread Desktop Attachment**:
   On Windows, background agent processes spawning GUI windows must call `OpenDesktopW("Default")` and `SetThreadDesktop()` to safely bridge WinSta0 session isolation.

---

## 8. The Strict 10-Point Verification Checklist

Before closing any GUI task, the agent must certify:
- [ ] **1. No Banned AI-Purple**: Zero occurrences of `#a855f7`, `#8b5cf6`, or neon purple gradients.
- [ ] **2. No Raw Emojis in Chrome**: Window title, tabs, buttons, and status tables use clean typographic glyphs (`●`, `▶`, `■`, `↻`, `✦`).
- [ ] **3. No Copywriting Slop**: Zero filler buzzwords (*supercharge, unleash, delve, tapestry*); factual telemetry only.
- [ ] **4. 28px+ Table Row Height**: Tables and Treeviews configured with `rowheight >= 28` (target `30px`).
- [ ] **5. Windows 11 DWM Dark Titlebar**: Native dark titlebar active on Windows 10/11.
- [ ] **6. High-DPI v2 Awareness**: Application scale-aware with zero DPI blurriness.
- [ ] **7. Self-Healing Geometry**: Validates coordinates against virtual screen bounds to prevent off-screen launches.
- [ ] **8. Resilient Font Cascade**: Tested with graceful fallback fonts; zero unhandled font exceptions.
- [ ] **9. Universal Hotkeys Bound**: `F5`, `Ctrl+1..5`, `Ctrl+F`, `Ctrl+T`, and `Esc` operational with footer legend.
- [ ] **10. 100% Clean Test Passes**: All unit tests in `pytest tests/` pass cleanly without regressions.

---

## 9. Authoritative Reference Implementations in Ecosystem

1. **`Fleet-Orchestrator/tools/fleet_gui.py`**:
   - The canonical multi-tab desktop mission control interface implementing the full ADT standard.
   - Highlights: Silicon Topology (NPU/iGPU/CPU), 31-worker Copilot pool telemetry, interactive CPM DAG badges, and DNA Splicer / Codon genome browser.
2. **`Fleet-Orchestrator/tools/azmuth_gui.py`**:
   - The canonical 60FPS dynamic canvas graph visualizer and phylogenetic tree explorer.
   - Highlights: Per-Monitor High-DPI scaling (`GetDpiForWindow`), center-bounded geometry (`min(w * 0.90, 1050 * scale)`), 8-level interactive zoom ladder (`Ctrl+=`, `Ctrl+-`, `Ctrl+0`, `Ctrl+MouseWheel`), and dynamic runtime Light/Dark theme switching (`Ctrl+T`).
