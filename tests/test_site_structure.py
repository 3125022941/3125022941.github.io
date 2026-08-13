from html.parser import HTMLParser
from pathlib import Path
import unittest


SITE = Path(__file__).resolve().parents[1] / "index.html"
NOTES = Path(__file__).resolve().parents[1] / "notes.html"


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.hrefs.append(attributes["href"])


class SiteStructureTests(unittest.TestCase):
    def test_homepage_projects_and_focus_controls_have_real_destinations(self):
        html = SITE.read_text(encoding="utf-8")
        self.assertEqual(html.count("data-work-link"), 3)
        self.assertIn('href="notes.html"', html)
        self.assertIn("data-focus-option", html)
        self.assertIn("data-focus-copy", html)
        self.assertIn('aria-pressed="true"', html)

    def test_homepage_focus_picker_uses_meaningful_content_mapping(self):
        html = SITE.read_text(encoding="utf-8")
        for token in ("const focusContent = {", "notes.html", "#works", "#build"):
            self.assertIn(token, html)
        self.assertNotIn("data-amount", html)
        self.assertIn("document.querySelector('[data-focus-cta]')", html)

    def test_notes_has_active_toc_and_shared_theme_control_contract(self):
        html = NOTES.read_text(encoding="utf-8")
        for token in (
            "data-toc-link",
            "IntersectionObserver",
            "is-current",
            'data-theme-icon="sun"',
            'data-theme-icon="moon"',
            "width:44px",
            ":focus-visible",
        ):
            self.assertIn(token, html)
        self.assertNotIn("window.addEventListener('scroll'", html)
        self.assertIn("const findCurrentChapter", html)
        self.assertIn("let tocHashReady = !hashChapter", html)

    def test_homepage_theme_control_has_a_44px_touch_target(self):
        html = SITE.read_text(encoding="utf-8")
        theme_rules = html.split(".theme-toggle {", 1)[1].split("}", 1)[0]
        self.assertIn("width: 44px", theme_rules)
        self.assertIn("height: 44px", theme_rules)

    def test_readme_describes_jiuwei_site_and_local_preview(self):
        readme = (SITE.parent / "README.md").read_text(encoding="utf-8")
        self.assertIn("Jiuwei", readme)
        self.assertIn("python serve.py", readme)
        self.assertIn("https://3125022941.github.io/", readme)

    def test_fragment_links_resolve_and_confirmed_github_links_are_available(self):
        parser = LinkCollector()
        parser.feed(SITE.read_text(encoding="utf-8"))
        fragments = [href[1:] for href in parser.hrefs if href.startswith("#")]
        self.assertTrue(fragments)
        self.assertTrue(all(fragment in parser.ids for fragment in fragments))
        external = [href for href in parser.hrefs if href.startswith(("http://", "https://", "mailto:"))]
        self.assertEqual(
            external,
            [
                "https://github.com/3125022941/agent-scaffold",
                "https://github.com/3125022941",
            ],
        )

    def test_agent_scaffold_notes_page_has_real_chapter_anchors(self):
        self.assertTrue(NOTES.exists())
        parser = LinkCollector()
        notes_html = NOTES.read_text(encoding="utf-8")
        parser.feed(notes_html)
        for chapter in ("foundation", "assembly", "workflow", "experience"):
            self.assertIn(chapter, parser.ids)
            self.assertIn(f"#{chapter}", parser.hrefs)

        index_html = SITE.read_text(encoding="utf-8")
        for href in (
            "notes.html#foundation",
            "notes.html#assembly",
            "notes.html#workflow",
            "notes.html#experience",
        ):
            self.assertIn(href, index_html)

        for note in (
            "脚手架需求分析",
            "系统架构设计",
            "AiApiNode",
            "ChatModelNode",
            "AgentWorkflowNode",
            "RunnerNode",
            "本地 MCP 与回调插件",
            "Skills 增强装配",
        ):
            self.assertIn(note, notes_html)


if __name__ == "__main__":
    unittest.main()
