# Publication Workbench Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the homepage as a responsive publishing workbench for projects and notes.

**Architecture:** Keep this a dependency-free static site. Replace only `index.html` markup, embedded styles and its small interaction script; keep the generated `notes.html` archive separate. Use real anchor navigation plus only confirmed GitHub and note destinations.

**Tech Stack:** HTML5, embedded CSS, vanilla JavaScript, Python `unittest`.

## Global Constraints

- Preserve paper texture, deep olive palette, Chinese serif headings, theme toggle and theme persistence.
- Desktop uses a three-column workbench; at 780px or below content stacks without horizontal overflow.
- Do not add fake dashboard widgets, unverified links, or external dependencies.
- The only public project URL is `https://github.com/3125022941/agent-scaffold`; the note archive is `notes.html`.

## File Structure

- `index.html`: semantic modules, workbench layout and responsive rules.
- `tests/test_jiuwei_v1.py`: homepage content, workbench and mobile contracts.
- `tests/test_site_structure.py`: fragment and external-link validation.

## Tasks

### Task 1: Establish the content contract

**Files:** modify `tests/test_jiuwei_v1.py`, `tests/test_site_structure.py`.

- [ ] Add a failing `test_homepage_is_a_publication_workbench` that requires `publication`, `projects`, `notes`, `about`, and the labels `发布`, `项目`, `笔记`, `关于`, `最新发布`, `当前状态`.
- [ ] Add checks that `#publication`, `#projects`, `#notes`, and `#about` each resolve to a page ID.
- [ ] Run `python -m unittest discover -s tests -v`; the new checks must fail against the old linear homepage.
- [ ] Commit with `git add -f tests/test_jiuwei_v1.py tests/test_site_structure.py && git commit -m "Test publication workbench homepage"`.

### Task 2: Build the desktop workbench

**Files:** modify `index.html`.

- [ ] Replace the main hierarchy with `<main id="main-content" class="workbench shell">`, a `.workbench-nav` aside, a `.publication-feed` containing `publication`, `projects`, `notes`, `about` sections, and a `.status-rail` aside.
- [ ] The `publication` module contains Agent Scaffold to `https://github.com/3125022941/agent-scaffold` and complete project notes to `notes.html`.
- [ ] The `projects` module lists Agent Scaffold as public and names AI Architecture Canvas and Agent Ops only as preparing; no link is created for either.
- [ ] The `notes` module links to `notes.html#note-00`, `notes.html#note-06`, and `notes.html#note-10`; the `about` module retains the short identity copy and GitHub profile link.
- [ ] Add `.workbench { display: grid; grid-template-columns: 220px minmax(0, 1fr) 260px; gap: 24px; padding-block: 34px 72px; }`, sticky side rails, and card styles based exclusively on existing `--paper`, `--card`, `--ink`, `--olive`, `--line`, `--shadow`, `--serif`, and `--sans` variables.
- [ ] Preserve `data-theme-toggle`, both theme icons, `syncThemeToggle`, and closed mobile navigation focus behavior.
- [ ] Run `python -m unittest discover -s tests -v` and commit with `git add index.html && git commit -m "Build publication workbench homepage"`.

### Task 3: Complete responsive and interaction behavior

**Files:** modify `index.html`, `tests/test_jiuwei_v1.py`.

- [ ] Add a failing mobile test requiring `.workbench` to declare `grid-template-columns: 1fr` inside `@media (max-width: 780px)`.
- [ ] Add mobile rules: `.workbench { grid-template-columns: 1fr; gap: 16px; padding-block: 18px 42px; }`, `.workbench-nav, .status-rail { position: static; }`, and a one-column status rail at 480px or below.
- [ ] Check that internal navigation scrolls to all four modules, two live cards use their real destinations, theme state survives reload, and no console error or horizontal overflow exists at desktop and 390px.
- [ ] Run `git diff --check && python -m unittest discover -s tests -v` and commit with `git add -f tests/test_jiuwei_v1.py index.html && git commit -m "Polish responsive publication workbench"`.

### Task 4: Publish

**Files:** modify `README.md` only if it no longer describes the personal project and notes site.

- [ ] Confirm `README.md` still includes `Jiuwei` and `https://3125022941.github.io/`.
- [ ] Push with `git push origin main`.
- [ ] Request `https://3125022941.github.io/?v=<latest-commit>` and verify that it includes `最新发布` and `href="notes.html"`.
