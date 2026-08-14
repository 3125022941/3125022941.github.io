# Portal Launchpad Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the homepage a compact functional launchpad, with standalone pages for projects, current work and personal information.

**Architecture:** Keep the static-site approach and reuse the existing visual variables, header controls and theme script. `index.html` becomes a single-screen launchpad; `projects.html`, `now.html` and `about.html` share a small duplicated static shell so every destination is independently addressable and shareable.

**Tech Stack:** HTML5, embedded CSS, vanilla JavaScript, Python `unittest`.

## Global Constraints

- Preserve paper texture, deep olive palette, Chinese serif headings, day/night theme and its local persistence.
- Homepage must not put the full project archive, current-build detail or biography below the fold.
- Only Agent Scaffold uses `https://github.com/3125022941/agent-scaffold`; preparation-stage projects have no outbound project URL.
- Keep the complete project notes at `notes.html` and GitHub profile at `https://github.com/3125022941`.

## File Structure

- `index.html`: compact four-entry homepage and current-status summary.
- `projects.html`: standalone project archive.
- `now.html`: standalone Agent Scaffold progress page.
- `about.html`: standalone personal overview page.
- `tests/test_jiuwei_v1.py`: launchpad and standalone-page contracts.
- `tests/test_site_structure.py`: link resolution and approved external destinations.

## Tasks

### Task 1: Add the launchpad test contract

**Files:** modify `tests/test_jiuwei_v1.py`, `tests/test_site_structure.py`.

- [ ] Add a failing test that requires `projects.html`, `notes.html`, `now.html`, and `about.html` in the homepage anchors, and rejects the old `projects-module`, `notes-module`, and `about-module` long sections in `index.html`.
- [ ] Add a failing test that each new HTML file exists and contains both `data-theme-toggle` and links to the four functional destinations.
- [ ] Run `python -m unittest discover -s tests -v`; the new tests must fail before the page split.
- [ ] Commit with `git add -f tests/test_jiuwei_v1.py tests/test_site_structure.py && git commit -m "Test portal launchpad routes"`.

### Task 2: Reduce the homepage to functional entry cards

**Files:** modify `index.html`.

- [ ] Replace the scrolling `publication-feed` with four clear cards: 项目 → `projects.html`, 笔记 → `notes.html`, 当前构建 → `now.html`, 关于 → `about.html`.
- [ ] Keep the left navigation and status rail, but turn their destinations into pages rather than fragments.
- [ ] Retain the existing theme toggle, mobile menu focus behavior and `data-nav` JavaScript interface.
- [ ] Run `python -m unittest discover -s tests -v`; homepage route and old-section checks pass.
- [ ] Commit with `git add index.html && git commit -m "Turn homepage into portal launchpad"`.

### Task 3: Create the independent function pages

**Files:** create `projects.html`, `now.html`, `about.html`.

- [ ] Create each page with the shared paper/olive visual shell, a visible return-to-home link, header navigation to all four destinations and the persisted theme control.
- [ ] Projects page shows Agent Scaffold as the sole outbound project and labels AI Architecture Canvas and Agent Ops as 筹备中.
- [ ] Now page shows the verified Agent Scaffold stack: Java 17, Spring AI, Google ADK, DDD, MCP, Skills and Workflow.
- [ ] About page includes the user’s AI engineering, automation and open-source focus plus the verified GitHub profile.
- [ ] Run `python -m unittest discover -s tests -v` and commit with `git add projects.html now.html about.html && git commit -m "Add portal function pages"`.

### Task 4: Verify and publish

**Files:** modify tests only if a check revealed an incorrectly encoded link or missing route.

- [ ] Use desktop and 390px browser views to verify all homepage entry cards, internal navigation, theme persistence, no horizontal overflow and no console errors.
- [ ] Run `git diff --check && python -m unittest discover -s tests -v`.
- [ ] Push with `git push origin main` and verify `https://3125022941.github.io/?v=<latest-commit>` includes the four standalone destination filenames.
