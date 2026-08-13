from pathlib import Path
import re
import unittest


SITE = Path(__file__).resolve().parents[1] / "index.html"


class JiuweiProjectArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = SITE.read_text(encoding="utf-8")

    def test_homepage_is_a_publication_workbench(self):
        for text in (
            "九尾",
            "Jiuwei",
            "发布",
            "项目",
            "笔记",
            "关于",
            "最新发布",
            "当前状态",
        ):
            self.assertIn(text, self.html)
        for section_id in ("publication", "projects", "notes", "about"):
            self.assertIn(f'id="{section_id}"', self.html)
        self.assertIn('class="workbench shell"', self.html)
        self.assertNotIn('id="friends"', self.html)
        self.assertNotIn('id="support"', self.html)

    def test_published_projects_have_honest_destinations(self):
        works = re.search(
            r'<section class="[^"]*projects-module[^"]*" id="projects".*?</section>',
            self.html,
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
        self.assertEqual(self.html.count("data-work-link"), 1)
        self.assertIn('href="https://github.com/3125022941/agent-scaffold"', self.html)
        self.assertIn("筹备中", self.html)

    def test_current_build_uses_confirmed_agent_scaffold_facts(self):
        for text in ("Java 17", "Spring AI", "Google ADK", "DDD", "MCP", "Skills", "Workflow"):
            self.assertIn(text, self.html)

    def test_theme_control_uses_a_persistent_sun_moon_state(self):
        for token in (
            "data-theme-toggle",
            'data-theme-icon="sun"',
            'data-theme-icon="moon"',
            "syncThemeToggle",
            "切换到夜间模式",
            "切换到日间模式",
        ):
            self.assertIn(token, self.html)

    def test_closed_mobile_navigation_is_not_focusable(self):
        closed_nav = next(
            (
                match
                for match in re.finditer(
                    r"\.side-nav\s*\{(?P<rules>.*?)\n\s*\}",
                    self.html,
                    re.DOTALL,
                )
                if "opacity: 0;" in match.group("rules")
            ),
            None,
        )
        open_nav = re.search(
            r"\.side-nav\.is-open\s*\{(?P<rules>.*?)\n\s*\}",
            self.html,
            re.DOTALL,
        )
        self.assertIsNotNone(closed_nav)
        self.assertIsNotNone(open_nav)
        self.assertRegex(closed_nav.group("rules"), r"visibility:\s*hidden;")
        self.assertRegex(closed_nav.group("rules"), r"pointer-events:\s*none;")
        self.assertRegex(open_nav.group("rules"), r"visibility:\s*visible;")
        self.assertRegex(open_nav.group("rules"), r"pointer-events:\s*auto;")

    def test_mobile_workbench_stacks_without_page_overflow(self):
        mobile_rules = re.search(
            r"@media \(max-width: 780px\) \{(?P<rules>.*?)\n    \}",
            self.html,
            re.DOTALL,
        )
        self.assertIsNotNone(mobile_rules)
        self.assertRegex(
            mobile_rules.group("rules"),
            r"\.workbench\s*\{[^}]*grid-template-columns:\s*1fr;",
        )

    def test_old_template_identifiers_and_fake_contact_are_removed(self):
        for text in ("River", "MindStick", "ChatPaper", "Flowgram", "hello@example.com", "example.com"):
            self.assertNotIn(text, self.html)


if __name__ == "__main__":
    unittest.main()
