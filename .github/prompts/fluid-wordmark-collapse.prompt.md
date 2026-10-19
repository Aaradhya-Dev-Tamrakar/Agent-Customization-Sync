---
description: "This skill has been unified and absorbed into the master frontend design system `design-taste-frontend`. Use `design-taste-frontend` for collapsible wordmarks, anti-displacement navigation grids, Anthropic Glasswing patterns, Fuse.ai editorial materiality, and Google M3 motion physics."
---

# Fluid Wordmark Collapse (Forwarding Pointer)

> [!NOTE]
> **Unified Architecture**: This skill has been codified and consolidated into the master frontend design system:
> 
> **[`design-taste-frontend`](../design-taste-frontend/SKILL.md)** — See **Section 4: Production-Level UI/UX Architecture & Navigation**.

### Key Invariants Preserved in Master Skill:
1. **The In-Place Syllable Decomposition Pattern**: Collapsing words into initials in-place (`<span class="nav-initial">A</span><span class="nav-rest">aradhya</span>`) rather than abrupt side-by-side disappearing text.
2. **The 3-Zone Fixed-Slot Layout (Anti-Displacement)**: Reserving `--nav-logo-slot: 260px` to lock adjacent navigation links in fixed coordinates and guarantee zero layout shift (`CLS = 0`).
3. **Accessibility Invariants**: `aria-label="Full Brand Name"` on parent anchor, `aria-hidden="true"` on decomposed visual spans.
