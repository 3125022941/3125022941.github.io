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
    def test_homepage_keeps_notes_and_theme_contracts(self):
        html = SITE.read_text(encoding="utf-8")
        self.assertIn('href="notes.html"', html)
        theme_rules = html.split(".theme-toggle, .nav-toggle {", 1)[1].split("}", 1)[0]
        self.assertIn("width: 44px", theme_rules)
        self.assertIn("height: 44px", theme_rules)
        self.assertNotIn("window.addEventListener('scroll'", html)

    def test_fragment_links_resolve_and_external_links_are_confirmed(self):
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
                "https://github.com/3125022941/agent-scaffold",
                "https://github.com/3125022941",
            ],
        )

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

    def test_agent_scaffold_notes_page_preserves_every_source_document(self):
        self.assertTrue(NOTES.exists())
        parser = LinkCollector()
        notes_html = NOTES.read_text(encoding="utf-8")
        parser.feed(notes_html)
        for chapter in range(22):
            note_id = f"note-{chapter:02d}"
            self.assertIn(note_id, parser.ids)
            self.assertIn(f"#{note_id}", parser.hrefs)
        self.assertEqual(notes_html.count('class="note-document"'), 22)
        for source_text in (
            "脚手架需求分析",
            "系统架构设计",
            "2025年11月27日",
            "增强装配-本地mcp",
            "增强装配-skills",
        ):
            self.assertIn(source_text, notes_html)
        self.assertNotIn("DElk89iu8Ehhnbu", notes_html)
        self.assertNotIn("file:///Users/fuzhengwei", notes_html)
        self.assertNotIn('href="http:/#"', notes_html)
        self.assertIn('src="assets/agent-scaffold-notes/', notes_html)
        self.assertNotIn('src="https://article-images.zsxq.com/', notes_html)
        for language in ("java", "yaml", "xml", "json"):
            self.assertIn(f'class="code-block" data-language="{language}"', notes_html)
        self.assertTrue((SITE.parent / "assets" / "agent-scaffold-notes").is_dir())
        index_html = SITE.read_text(encoding="utf-8")
        for href in (
            "notes.html#note-00",
            "notes.html#note-06",
            "notes.html#note-10",
            "notes.html#note-15",
        ):
            self.assertIn(href, index_html)

    def test_readme_describes_jiuwei_site_and_local_preview(self):
        readme = (SITE.parent / "README.md").read_text(encoding="utf-8")
        self.assertIn("Jiuwei", readme)
        self.assertIn("python serve.py", readme)
        self.assertIn("https://3125022941.github.io/", readme)


if __name__ == "__main__":
    unittest.main()
