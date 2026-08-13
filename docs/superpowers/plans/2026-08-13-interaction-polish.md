# Interaction Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** Make every portfolio interaction useful, accessible, and consistent across the homepage and Agent Scaffold notes.

**Architecture:** Keep the static two-page site and existing URLs. Add semantic hooks in the existing HTML, CSS state classes for feedback, and two client-side controllers: one homepage focus controller and one notes table-of-contents controller. Both use standard DOM APIs and IntersectionObserver, with no dependency or scroll listener.

**Tech Stack:** Semantic HTML, native CSS, vanilla JavaScript, Python unittest, GitHub Pages.

## Global Constraints

- Preserve existing URL paths, anchor IDs, primary navigation labels, GitHub links, and Chinese editorial copy except when a Notes link needs to lead to the existing notes page.
- Keep the cream/ink token system and \`jiuwei-theme\` local-storage key.
- Use IntersectionObserver, never a scroll event listener.
- Keep motion limited and retain the reduced-motion rule.
- Theme buttons must be 44 by 44 pixels and interactive controls need visible keyboard focus.

---

### Task 1: Homepage interaction contracts

**Files:**

- Modify: \`tests/test_site_structure.py\`
- Modify: \`index.html\`

**Interfaces:**

- Produces \`data-work-link\`, \`data-focus-option\`, \`data-focus-copy\`, and \`data-focus-cta\` hooks.
- Produces one selected focus option with \`aria-pressed="true"\` and matching visible content.

- [ ] **Step 1: Write the failing test**

~~~python
def test_homepage_projects_and_focus_controls_have_real_destinations(self):
    html = SITE.read_text(encoding="utf-8")
    self.assertEqual(html.count('data-work-link'), 3)
    self.assertIn('href="notes.html"', html)
    self.assertIn('data-focus-option', html)
    self.assertIn('data-focus-copy', html)
    self.assertIn('aria-pressed="true"', html)
~~~

- [ ] **Step 2: Run test to verify it fails**

Run: \`python -m unittest tests.test_site_structure.SiteStructureTests.test_homepage_projects_and_focus_controls_have_real_destinations -v\`

Expected: FAIL because the cards only expose arrow links and the picker has no focus-content hooks.

- [ ] **Step 3: Write minimal implementation**

~~~html
<a class="work-card-link" data-work-link href="https://github.com/3125022941/agent-scaffold" target="_blank" rel="noreferrer" aria-label="打开 Agent Scaffold GitHub 仓库">…</a>
<button type="button" data-focus-option data-focus="learn" aria-pressed="true">LEARN</button>
<p data-focus-copy data-focus-copy-for="learn">理解系统如何被设计，再把理解沉淀成笔记。</p>
<a data-focus-cta href="notes.html">阅读 Agent Scaffold 笔记</a>
~~~

Wrap each card's existing visual and text content in a single existing-destination anchor. Convert LEARN / BUILD / AUTOMATE into focus buttons, add three matching copy blocks plus one CTA. Route homepage Notes links to \`notes.html\` or an existing chapter hash. Add full-card focus styling and show only active focus copy.

- [ ] **Step 4: Run test to verify it passes**

Run: \`python -m unittest tests.test_site_structure.SiteStructureTests.test_homepage_projects_and_focus_controls_have_real_destinations -v\`

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add index.html tests/test_site_structure.py
git commit -m "Improve homepage interaction targets"
~~~

### Task 2: Homepage stateful focus interaction

**Files:**

- Modify: \`tests/test_site_structure.py\`
- Modify: \`index.html\`

**Interfaces:**

- Consumes \`data-focus-option\`, \`data-focus-copy\`, and \`data-focus-cta\`.
- Produces a keyboard-operable focus controller that changes selected state, copy, CTA label, and CTA destination.

- [ ] **Step 1: Write the failing test**

~~~python
def test_homepage_focus_picker_uses_meaningful_content_mapping(self):
    html = SITE.read_text(encoding="utf-8")
    for token in ('const focusContent = {', 'notes.html', '#works', '#build'):
        self.assertIn(token, html)
    self.assertNotIn('data-amount', html)
~~~

- [ ] **Step 2: Run test to verify it fails**

Run: \`python -m unittest tests.test_site_structure.SiteStructureTests.test_homepage_focus_picker_uses_meaningful_content_mapping -v\`

Expected: FAIL because the page still only changes an amount label.

- [ ] **Step 3: Write minimal implementation**

~~~js
const focusContent = {
  learn: { copy: '理解系统如何被设计，再把理解沉淀成笔记。', label: '阅读 Agent Scaffold 笔记', href: 'notes.html' },
  build: { copy: '把理解转成可运行的 Agent 工程。', label: '查看已发布项目', href: '#works' },
  automate: { copy: '把可靠的重复动作交给可控的自动化流程。', label: '查看系统路径', href: '#build' }
};
~~~

Attach a delegated click handler to the focus-option container. It sets \`aria-pressed\`, applies the selected class, reveals its matching copy, and updates the CTA from \`focusContent\`. Remove the obsolete amount and toast handlers when unused.

- [ ] **Step 4: Run test to verify it passes**

Run: \`python -m unittest tests.test_site_structure.SiteStructureTests.test_homepage_focus_picker_uses_meaningful_content_mapping -v\`

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add index.html tests/test_site_structure.py
git commit -m "Make focus picker update real content"
~~~

### Task 3: Notes navigation and theme parity

**Files:**

- Modify: \`tests/test_site_structure.py\`
- Modify: \`notes.html\`

**Interfaces:**

- Produces \`data-toc-link\`, \`data-theme-icon="sun"\`, \`data-theme-icon="moon"\`, and \`is-current\` CSS state.
- IntersectionObserver maps each chapter ID to its table-of-contents anchor.

- [ ] **Step 1: Write the failing test**

~~~python
def test_notes_has_active_toc_and_shared_theme_control_contract(self):
    html = NOTES.read_text(encoding="utf-8")
    for token in ('data-toc-link', 'IntersectionObserver', 'is-current', 'data-theme-icon="sun"', 'data-theme-icon="moon"', 'width:44px', ':focus-visible'):
        self.assertIn(token, html)
    self.assertNotIn("window.addEventListener('scroll'", html)
~~~

- [ ] **Step 2: Run test to verify it fails**

Run: \`python -m unittest tests.test_site_structure.SiteStructureTests.test_notes_has_active_toc_and_shared_theme_control_contract -v\`

Expected: FAIL because the table of contents has no current-section controller and the notes theme button is text-only.

- [ ] **Step 3: Write minimal implementation**

~~~js
const tocLinks = [...document.querySelectorAll('[data-toc-link]')];
const chapters = [...document.querySelectorAll('.chapter[id]')];
const setCurrentChapter = (id) => {
  tocLinks.forEach((link) => link.classList.toggle('is-current', link.getAttribute('href') === '#' + id));
  history.replaceState(null, '', '#' + id);
};
const chapterObserver = new IntersectionObserver((entries) => {
  const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
  if (visible) setCurrentChapter(visible.target.id);
}, { rootMargin: '-18% 0px -68% 0px', threshold: 0 });
chapters.forEach((chapter) => chapterObserver.observe(chapter));
~~~

Replace notes text sun/moon characters with the same inline SVG pair and stateful sync rule used by the homepage. Expand both theme controls to 44px, add focus-visible rules, and add current state semantics. Preserve ordinary hash links.

- [ ] **Step 4: Run test to verify it passes**

Run: \`python -m unittest tests.test_site_structure.SiteStructureTests.test_notes_has_active_toc_and_shared_theme_control_contract -v\`

Expected: PASS.

- [ ] **Step 5: Commit**

~~~bash
git add notes.html tests/test_site_structure.py
git commit -m "Improve notes navigation and theme control"
~~~

### Task 4: Regression and publication

**Files:**

- Modify: \`README.md\`
- Modify: \`tests/test_site_structure.py\`

**Interfaces:**

- Documents \`python serve.py\` and the GitHub Pages address.

- [ ] **Step 1: Write the failing test**

~~~python
def test_readme_describes_jiuwei_site_and_local_preview(self):
    readme = (SITE.parent / 'README.md').read_text(encoding='utf-8')
    self.assertIn('Jiuwei', readme)
    self.assertIn('python serve.py', readme)
    self.assertIn('https://3125022941.github.io/', readme)
~~~

- [ ] **Step 2: Run test to verify it fails**

Run: \`python -m unittest tests.test_site_structure.SiteStructureTests.test_readme_describes_jiuwei_site_and_local_preview -v\`

Expected: FAIL because it retains obsolete River wording.

- [ ] **Step 3: Write minimal implementation**

~~~markdown
# Jiuwei personal site

Static portfolio and Agent Scaffold notes for Jiuwei.

## Preview

~~~powershell
python serve.py
~~~

Open http://127.0.0.1:8080/, or visit https://3125022941.github.io/.
~~~

- [ ] **Step 4: Run final verification**

Run: \`python -m unittest discover -s tests -v\`

Expected: every test PASS.

Run a local server and check both \`/\` and \`/notes.html\` for HTTP 200, keyboard focus, theme persistence, project destinations, active notes TOC, no console errors, and no horizontal overflow at desktop and mobile widths.

- [ ] **Step 5: Commit and publish**

~~~bash
git add README.md tests/test_site_structure.py
git commit -m "Document site preview and verify interactions"
git push origin main
~~~

Confirm https://3125022941.github.io/ and https://3125022941.github.io/notes.html return HTTP 200 after GitHub Pages deploys.

