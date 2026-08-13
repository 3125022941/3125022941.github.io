# Agent Scaffold Complete Notes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a complete, readable public archive from the 22 Agent Scaffold Markdown notes.

**Architecture:** A small Python build script converts the local Markdown source of truth to a static `notes.html` artifact. The generated page supplies its own responsive reading styles and minimal client-side theme and table-of-contents behavior; the homepage links to the generated anchors.

**Tech Stack:** Python 3, Python-Markdown 3.10.2, static HTML/CSS/JavaScript, Python unittest.

## Global Constraints

- Source files are read in numerical order from `F:\obsidian_agent\agent\the way to the agent\项目4：脚手架`.
- Preserve source text, links, code blocks, and remote images without summarization.
- Keep the output deployable as a static GitHub Pages page.
- Retain the existing visual theme contract and accessible navigation.

---

### Task 1: Define source completeness tests

**Files:**
- Modify: `tests/test_site_structure.py`

- [ ] Assert generated content has all `note-00` through `note-21` anchors and 22 article entries.
- [ ] Assert selected source-only copy and a known remote image URL appear in the output.
- [ ] Assert homepage quick links target `note-00`, `note-06`, `note-10`, and `note-15`.
- [ ] Run the tests and confirm the old summary fails.

### Task 2: Add the deterministic note generator

**Files:**
- Create: `build_notes.py`
- Modify: `notes.html`

- [ ] Read sorted Markdown files, convert using Python-Markdown extensions, and create one article per file.
- [ ] Generate the complete reading template, table of contents, and stable anchors.
- [ ] Run `python build_notes.py` and the test suite.

### Task 3: Reconnect project-page shortcuts

**Files:**
- Modify: `index.html`
- Test: `tests/test_site_structure.py`

- [ ] Point the four existing notes shortcuts to their first source chapter anchors.
- [ ] Run the full test suite and verify all fragment destinations exist.

### Task 4: Verify the public reading experience

**Files:**
- Verify: `notes.html`

- [ ] Check desktop and mobile long-form reading, active table of contents, theme persistence, images, and console output.
- [ ] Run the full test suite and generated-file freshness check.
