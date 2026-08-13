# Agent Scaffold Complete Notes Design

## Goal

Publish the complete Agent Scaffold notes in the source order instead of maintaining a four-section summary.

## Source of truth

The 22 Markdown files in `F:\obsidian_agent\agent\the way to the agent\项目4：脚手架` are the source of truth. Their titles, body text, code blocks, links, and remote images must appear in the generated public page without summarization or content substitution.

## Page structure

`notes.html` becomes one searchable long-form reading page. It has a compact series introduction, a sticky table of contents with all 22 chapter titles, and one article for each source file in numeric order. Article anchors are stable as `#note-00` through `#note-21`. The four project-home shortcuts move to the first chapter of each existing project stage: 00, 06, 10, and 15.

## Generation

`build_notes.py` reads the source directory and writes `notes.html`. It uses the installed Python Markdown package with fenced code and table support. The page is a static GitHub Pages artifact, so visitors do not depend on the local Obsidian directory. Re-running the script is the only update step when the notes change.

## Presentation and safety

Use a readable editorial code-and-document layout. Preserve heading depth, code blocks, links, block quotes, and images. Retain theme persistence, 44px theme control, keyboard focus, responsive navigation, active table-of-contents state, and reduced-motion support. Do not invent, alter, or omit original note content.

## Verification

Tests assert all 22 note anchors and titles, selected source-only sentences and images, source-order rendering, source count, the four homepage note links, theme controls, and fragment resolution. Browser verification checks chapter navigation, long-form layout, image loading behavior, responsive overflow, and console errors.
