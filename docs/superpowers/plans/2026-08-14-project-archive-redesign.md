# Project Archive Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the homepage as a concise, Chinese-first personal project archive.

**Architecture:** Replace the oversized one-page presentation with a focused static HTML composition. Keep the existing notes page and confirmed GitHub destinations; use native CSS and a small progressive-enhancement script for theme persistence, mobile navigation, and reveal states.

**Tech Stack:** Static HTML, CSS, and browser JavaScript; Python unittest checks.

## Global Constraints

- Preserve only confirmed external links: Agent Scaffold and the Jiuwei GitHub profile.
- Use Chinese-first navigation: `作品`, `笔记`, `探索`, `关于`.
- Retain accessible dark mode and a 44px theme button.
- Do not add fake product screenshots, fabricated data, or new dependencies.

---

### Task 1: Define the new homepage contract

**Files:**
- Modify: `tests/test_jiuwei_v1.py`
- Modify: `tests/test_site_structure.py`

- [ ] Write assertions for the project-archive hierarchy, the six remaining section anchors, and removal of Friends/Principles.
- [ ] Assert that only Agent Scaffold is externally linked and that all fragment links resolve.
- [ ] Run `python -m unittest discover -s tests -v` and confirm the old homepage fails the new contract.

### Task 2: Rebuild the homepage shell and content hierarchy

**Files:**
- Modify: `index.html`

- [ ] Implement semantic header, hero, current-build, project archive, notes, exploration, and about sections.
- [ ] Keep the verified Agent Scaffold facts and direct notes anchors.
- [ ] Run `python -m unittest discover -s tests -v` and confirm the content checks pass.

### Task 3: Restore accessible theme and mobile interactions

**Files:**
- Modify: `index.html`

- [ ] Implement persistent theme state, descriptive icon labels, and a 44px touch target.
- [ ] Ensure the closed mobile menu has `visibility: hidden` and no pointer interaction; ensure the opened menu reverses both.
- [ ] Run the test suite and check JavaScript parses using `node --check`.

### Task 4: Validate in the local browser

**Files:**
- Verify: `index.html`

- [ ] Check desktop and mobile layouts, theme switching, menu opening, anchor navigation, and browser console output.
- [ ] Verify no horizontal overflow and no reduced-motion regression.
- [ ] Run the full test suite one final time.
