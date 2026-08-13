# Project Archive Redesign

## Goal

Turn the homepage into Jiuwei's personal project archive. The page should help a first-time visitor understand who Jiuwei is, what is being built now, and where to find project work, notes, and exploration.

## Design direction

Use the reference site's personal-entry and recent-content rhythm, without copying its avatar, calendar, illustration, or layout. The visual language remains quiet, editorial, and Chinese-first: warm paper, ink, olive accent, generous space, and restrained motion.

Design dials: variance 6, motion 3, density 4.

## Information hierarchy

1. Compact hero: `把好奇心做成可以运行的项目。` and a short self-introduction.
2. Current build: Agent Scaffold, with its real GitHub link and accurate technology stack.
3. Project archive: Agent Scaffold, AI Architecture Canvas, and Agent Ops. Only Agent Scaffold receives an external link because it is the only confirmed destination.
4. Project notes: four direct entry points into the existing notes page.
5. Exploration: X-Plore as an evolving map rather than a separate brand campaign.
6. About: study direction, internship availability, GitHub, and the existing public-output proof point.

## Navigation and interaction

Navigation is Chinese-first: `作品`, `笔记`, `探索`, `关于`. It has a 44px theme switcher and an accessible mobile menu. Hero actions link to current work and the project archive. Motion is limited to entrance reveal and clear hover/focus feedback. No scroll listeners, fake dashboards, fake screenshots, fabricated links, Friends section, or standalone Principles control.

## Accessibility and theme

Retain semantic section landmarks, visible keyboard focus, mobile navigation that is hidden and non-focusable while closed, `prefers-reduced-motion` support, and persistent light/dark theme state.

## Verification

Tests assert the new storyline, section anchors, confirmed links, honest project count/link behavior, theme controls, mobile navigation contract, and existing notes anchors. Browser checks cover desktop and mobile layout, theme switching, menu behaviour, fragments, and no console errors.
