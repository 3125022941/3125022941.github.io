from pathlib import Path
import re
import unittest


SITE = Path(__file__).resolve().parents[1] / "index.html"
PROJECTS = Path(__file__).resolve().parents[1] / "projects.html"
NOW = Path(__file__).resolve().parents[1] / "now.html"
ABOUT = Path(__file__).resolve().parents[1] / "about.html"
PORTAL_CSS = Path(__file__).resolve().parents[1] / "portal.css"
PORTAL_JS = Path(__file__).resolve().parents[1] / "portal.js"


class JiuweiProjectArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = SITE.read_text(encoding="utf-8")

    def test_homepage_is_a_functional_launchpad(self):
        for text in (
            "九尾",
            "Jiuwei",
            "项目",
            "笔记",
            "当前构建",
            "关于",
            "当前状态",
        ):
            self.assertIn(text, self.html)
        for route in ("projects.html", "notes.html", "now.html", "about.html"):
            self.assertIn(f'href="{route}"', self.html)
        for removed_module in ("projects-module", "notes-module", "about-module"):
            self.assertNotIn(removed_module, self.html)
        self.assertIn("min-height: calc(100dvh - 128px)", PORTAL_CSS.read_text(encoding="utf-8"))
        self.assertNotIn('id="friends"', self.html)
        self.assertNotIn('id="support"', self.html)

    def test_published_projects_have_honest_destinations(self):
        self.assertTrue(PROJECTS.exists())
        projects_html = PROJECTS.read_text(encoding="utf-8")
        works = re.search(
            r'<section class="[^"]*projects-module[^"]*" id="projects".*?</section>',
            projects_html,
            re.DOTALL,
        )
        self.assertIsNotNone(works)
        cards = re.findall(
            r'<article class="[^"]*project-card[^"]*">.*?</article>',
            works.group(0),
            re.DOTALL,
        )
        self.assertEqual(len(cards), 3)
        self.assertEqual(
            re.findall(r"<h3>(.*?)</h3>", "\n".join(cards), re.DOTALL),
            ["Agent Scaffold", "AI Architecture Canvas", "Agent Ops"],
        )
        self.assertEqual(projects_html.count("data-work-link"), 1)
        self.assertIn('href="https://github.com/3125022941/agent-scaffold"', projects_html)
        self.assertIn("筹备中", projects_html)

    def test_current_build_uses_confirmed_agent_scaffold_facts(self):
        self.assertTrue(NOW.exists())
        now_html = NOW.read_text(encoding="utf-8")
        for text in ("Java 17", "Spring AI", "Google ADK", "DDD", "MCP", "Skills", "Workflow"):
            self.assertIn(text, now_html)

    def test_portal_function_pages_share_navigation_and_theme_control(self):
        for page in (PROJECTS, NOW, ABOUT):
            self.assertTrue(page.exists())
            html = page.read_text(encoding="utf-8")
            self.assertIn("data-theme-toggle", html)
            for route in ("index.html", "projects.html", "notes.html", "now.html", "about.html"):
                self.assertIn(f'href="{route}"', html)

    def test_theme_control_uses_a_persistent_sun_moon_state(self):
        shared_source = self.html + PORTAL_CSS.read_text(encoding="utf-8") + PORTAL_JS.read_text(encoding="utf-8")
        for token in (
            "data-theme-toggle",
            'data-theme-icon="sun"',
            'data-theme-icon="moon"',
            "syncThemeToggle",
            "切换到夜间模式",
            "切换到日间模式",
        ):
            self.assertIn(token, shared_source)

    def test_closed_mobile_navigation_is_not_focusable(self):
        css = PORTAL_CSS.read_text(encoding="utf-8")
        closed_nav = next(
            (
                match
                for match in re.finditer(
                    r"\.side-nav\s*\{(?P<rules>[^}]*)\}",
                    css,
                    re.DOTALL,
                )
                if "opacity: 0;" in match.group("rules")
            ),
            None,
        )
        open_nav = re.search(
            r"\.side-nav\.is-open\s*\{(?P<rules>[^}]*)\}",
            css,
            re.DOTALL,
        )
        self.assertIsNotNone(closed_nav)
        self.assertIsNotNone(open_nav)
        self.assertRegex(closed_nav.group("rules"), r"visibility:\s*hidden;")
        self.assertRegex(closed_nav.group("rules"), r"pointer-events:\s*none;")
        self.assertRegex(open_nav.group("rules"), r"visibility:\s*visible;")
        self.assertRegex(open_nav.group("rules"), r"pointer-events:\s*auto;")

    def test_mobile_workbench_stacks_without_page_overflow(self):
        css = PORTAL_CSS.read_text(encoding="utf-8")
        self.assertRegex(
            css,
            r"@media \(max-width: 780px\)[\s\S]*?\.portal\s*\{[^}]*grid-template-columns:\s*1fr;",
        )

    def test_old_template_identifiers_and_fake_contact_are_removed(self):
        for text in ("River", "MindStick", "ChatPaper", "Flowgram", "hello@example.com", "example.com"):
            self.assertNotIn(text, self.html)


if __name__ == "__main__":
    unittest.main()
