"""Build the public Agent Scaffold notes archive from the local Markdown source."""

from __future__ import annotations

import os
import re
from html import escape
from pathlib import Path

import markdown


DEFAULT_SOURCE = Path(r"F:\obsidian_agent\agent\the way to the agent\项目4：脚手架")
OUTPUT = Path(__file__).with_name("notes.html")


def note_number(path: Path) -> int:
    match = re.match(r"(\d+)", path.stem)
    if not match:
        raise ValueError(f"Note filename must begin with a number: {path.name}")
    return int(match.group(1))


def note_title(path: Path) -> str:
    return re.sub(r"^\d+\s*", "", path.stem)


def render_note(path: Path) -> str:
    number = note_number(path)
    title = note_title(path)
    source = path.read_text(encoding="utf-8")
    # Public notes may show local endpoint examples, but never their credentials.
    source = re.sub(r"(?i)(apikey=)[A-Za-z0-9_-]+", r"\1REDACTED", source)
    body = markdown.markdown(
        source,
        extensions=["extra", "fenced_code", "sane_lists", "nl2br"],
        output_format="html5",
    )
    return f'''<article class="note-document" id="note-{number:02d}">
  <header class="document-header">
    <p>{number:02d} / Agent Scaffold</p>
    <h1>{escape(title)}</h1>
  </header>
  <div class="markdown-body">{body}</div>
</article>'''


def render_page(notes: list[Path]) -> str:
    toc = "\n".join(
        f'<a href="#note-{note_number(path):02d}" data-toc-link>{note_number(path):02d} <span>{escape(note_title(path))}</span></a>'
        for path in notes
    )
    articles = "\n\n".join(render_note(path) for path in notes)
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="Agent Scaffold 的完整工程笔记：从需求、架构、配置到 Agent 装配、MCP、会话与 Skills。" />
  <meta name="theme-color" content="#f3f0e9" />
  <title>Agent Scaffold 完整笔记 · 九尾</title>
  <style>
    :root { --page:#f3f0e9; --card:#fbf9f4; --ink:#191a16; --soft:#57584f; --muted:#787870; --line:rgba(25,26,22,.14); --olive:#6f7957; --pale:#dfe3d5; --shell:min(1240px,calc(100% - 48px)); --read:760px; --serif:"Iowan Old Style","Palatino Linotype","Songti SC",STSong,serif; --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; --mono:"SFMono-Regular",Consolas,monospace; }
    html[data-theme="ink"] { --page:#12140f; --card:#1b1e18; --ink:#f1eee6; --soft:#c5c4bb; --muted:#9c9c91; --line:rgba(241,238,230,.14); --olive:#b5bd96; --pale:#30382a; }
    * { box-sizing:border-box; }
    html { background:var(--page); scroll-behavior:smooth; }
    body { min-width:320px; margin:0; color:var(--ink); background:radial-gradient(circle at 90% 0,rgba(213,218,195,.32),transparent 25rem),var(--page); font-family:var(--sans); line-height:1.75; }
    a { color:inherit; text-decoration:none; }
    button { font:inherit; }
    .shell { width:var(--shell); margin-inline:auto; }
    .skip-link { position:fixed; z-index:30; top:10px; left:10px; padding:9px 13px; color:var(--page); background:var(--ink); border-radius:8px; transform:translateY(-170%); }
    .skip-link:focus { transform:translateY(0); }
    a:focus-visible,button:focus-visible { outline:2px solid var(--olive); outline-offset:4px; }
    .site-header { position:sticky; z-index:10; top:0; border-bottom:1px solid var(--line); background:color-mix(in srgb,var(--page) 88%,transparent); -webkit-backdrop-filter:blur(14px); backdrop-filter:blur(14px); }
    .header-inner { min-height:72px; display:flex; justify-content:space-between; align-items:center; gap:20px; }
    .brand { font-family:var(--serif); font-size:22px; font-weight:700; letter-spacing:.06em; }
    .brand span { color:var(--olive); }
    .header-actions { display:flex; align-items:center; gap:15px; }
    .back-link { font-size:13px; font-weight:650; }
    .theme-toggle { width:44px; height:44px; display:grid; place-items:center; padding:0; color:var(--ink); background:var(--card); border:1px solid var(--line); border-radius:50%; cursor:pointer; }
    .theme-symbol { position:relative; width:18px; height:18px; display:grid; place-items:center; }
    .theme-symbol span { position:absolute; font-size:19px; line-height:1; transition:opacity .2s ease,transform .2s ease; }
    .theme-symbol [data-theme-icon="moon"] { opacity:0; transform:rotate(-20deg) scale(.7); }
    html[data-theme="ink"] .theme-symbol [data-theme-icon="sun"] { opacity:0; transform:rotate(20deg) scale(.7); }
    html[data-theme="ink"] .theme-symbol [data-theme-icon="moon"] { opacity:1; transform:rotate(0) scale(1); }
    .series-head { padding:76px 0 56px; border-bottom:1px solid var(--line); }
    .eyebrow,.document-header p { color:var(--olive); font-family:var(--mono); font-size:10px; letter-spacing:.14em; text-transform:uppercase; }
    .series-head h1 { max-width:880px; margin-top:17px; font-family:var(--serif); font-size:clamp(45px,6vw,78px); font-weight:500; letter-spacing:-.065em; line-height:1.06; }
    .series-head > .shell > p:last-child { max-width:670px; margin-top:23px; color:var(--soft); font-size:16px; }
    .series-meta { display:flex; flex-wrap:wrap; gap:8px; margin-top:28px; }
    .series-meta span { padding:5px 9px; color:var(--soft); border:1px solid var(--line); border-radius:999px; font-family:var(--mono); font-size:10px; }
    .note-layout { display:grid; grid-template-columns:252px minmax(0,1fr); gap:clamp(36px,7vw,100px); padding:52px 0 110px; }
    .toc { position:sticky; top:94px; max-height:calc(100dvh - 118px); padding:13px 16px; overflow:auto; background:color-mix(in srgb,var(--card) 88%,transparent); border:1px solid var(--line); border-radius:13px; }
    .toc > p { margin:5px 0 10px; color:var(--muted); font-family:var(--mono); font-size:10px; letter-spacing:.12em; text-transform:uppercase; }
    .toc a { display:grid; grid-template-columns:28px 1fr; gap:7px; padding:7px 0; color:var(--soft); font-size:12px; line-height:1.45; transition:color .18s ease,transform .18s ease; }
    .toc a:hover,.toc a.is-current { color:var(--olive); }
    .toc a.is-current { font-weight:700; transform:translateX(3px); }
    .documents { max-width:var(--read); }
    .note-document { scroll-margin-top:92px; padding:0 0 76px; margin-bottom:76px; border-bottom:1px solid var(--line); }
    .note-document:last-child { margin-bottom:0; border-bottom:0; }
    .document-header { padding-bottom:28px; margin-bottom:29px; border-bottom:1px solid var(--line); }
    .document-header p { margin:0 0 10px; }
    .document-header h1 { margin:0; font-family:var(--serif); font-size:clamp(34px,4vw,54px); font-weight:500; letter-spacing:-.055em; line-height:1.12; }
    .markdown-body { color:var(--soft); font-size:16px; overflow-wrap:anywhere; }
    .markdown-body > :first-child { margin-top:0; }
    .markdown-body h2,.markdown-body h3,.markdown-body h4,.markdown-body h5 { color:var(--ink); font-family:var(--serif); font-weight:500; letter-spacing:-.035em; line-height:1.22; }
    .markdown-body h2 { margin:52px 0 18px; font-size:clamp(28px,3vw,39px); }
    .markdown-body h3 { margin:36px 0 14px; font-size:clamp(23px,2.4vw,31px); }
    .markdown-body h4 { margin:28px 0 11px; font-size:21px; }
    .markdown-body h5 { margin:22px 0 9px; font-size:18px; }
    .markdown-body p { margin:0 0 17px; }
    .markdown-body ul,.markdown-body ol { padding-left:23px; margin:0 0 18px; }
    .markdown-body li + li { margin-top:7px; }
    .markdown-body blockquote { margin:24px 0; padding:16px 20px; color:var(--soft); background:var(--pale); border-left:3px solid var(--olive); }
    .markdown-body blockquote p:last-child { margin-bottom:0; }
    .markdown-body img { display:block; width:100%; height:auto; margin:25px 0; border:1px solid var(--line); border-radius:10px; background:var(--card); }
    .markdown-body a { color:var(--olive); text-decoration:underline; text-decoration-color:color-mix(in srgb,var(--olive) 45%,transparent); text-underline-offset:3px; }
    .markdown-body strong { color:var(--ink); }
    .markdown-body code { padding:.14em .36em; color:var(--ink); background:var(--pale); border-radius:4px; font-family:var(--mono); font-size:.88em; }
    .markdown-body pre { margin:23px 0; padding:18px; overflow:auto; color:#e9e7dd; background:#1b2119; border-radius:10px; line-height:1.6; }
    .markdown-body pre code { padding:0; color:inherit; background:transparent; font-size:13px; }
    .markdown-body table { width:100%; margin:23px 0; border-collapse:collapse; font-size:14px; }
    .markdown-body th,.markdown-body td { padding:10px; text-align:left; border:1px solid var(--line); }
    .markdown-body th { color:var(--ink); background:var(--pale); }
    .site-footer { padding:28px 0; border-top:1px solid var(--line); color:var(--muted); font-size:12px; }
    @media (max-width:780px) { :root { --shell:min(100% - 32px,760px); } .series-head { padding:52px 0 41px; } .note-layout { display:block; padding-top:31px; } .toc { position:static; max-height:none; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:0 14px; margin-bottom:45px; } .toc > p { grid-column:1/-1; } .toc a { font-size:11px; } .note-document { padding-bottom:54px; margin-bottom:54px; } .markdown-body { font-size:15px; } }
    @media (max-width:460px) { :root { --shell:min(100% - 28px,760px); } .back-link { display:none; } .toc { grid-template-columns:1fr; } .markdown-body pre { padding:14px; border-radius:7px; } }
    @media (prefers-reduced-motion:reduce) { *,*::before,*::after { scroll-behavior:auto !important; transition-duration:.01ms !important; animation-duration:.01ms !important; } .toc a.is-current { transform:none; } }
  </style>
</head>
<body>
  <a class="skip-link" href="#notes">跳到笔记</a>
  <header class="site-header"><div class="shell header-inner"><a class="brand" href="index.html#top" aria-label="返回九尾首页">九尾<span>.</span></a><div class="header-actions"><a class="back-link" href="index.html#works">← 返回项目</a><button class="theme-toggle" type="button" data-theme-toggle aria-label="切换到夜间模式" title="切换到夜间模式"><span class="theme-symbol" aria-hidden="true"><span data-theme-icon="sun">☼</span><span data-theme-icon="moon">☾</span></span></button></div></div></header>
  <main id="notes">
    <section class="series-head"><div class="shell"><p class="eyebrow">Agent Scaffold / Complete Notes</p><h1>从需求到可运行的 Agent。</h1><p>完整保留 Agent Scaffold 的 22 篇工程笔记。这里记录需求、架构、实现、代码、验证与持续增强，而不是事后的摘要。</p><div class="series-meta"><span>22 篇原始笔记</span><span>Java 17</span><span>Spring AI</span><span>Google ADK</span><span>DDD</span><span>MCP</span><span>Skills</span></div></div></section>
    <div class="shell note-layout"><nav class="toc" aria-label="完整笔记目录"><p>全部章节 / 00–21</p>__TOC__</nav><div class="documents">__ARTICLES__</div></div>
  </main>
  <footer class="site-footer"><div class="shell">© <span data-year></span> Jiuwei. Agent Scaffold Complete Notes.</div></footer>
  <script>
  (() => {
    const root = document.documentElement;
    const toggle = document.querySelector('[data-theme-toggle]');
    if (localStorage.getItem('jiuwei-theme') === 'ink') root.dataset.theme = 'ink';
    const syncThemeToggle = () => { const label = root.dataset.theme === 'ink' ? '切换到日间模式' : '切换到夜间模式'; toggle?.setAttribute('aria-label', label); toggle?.setAttribute('title', label); };
    syncThemeToggle();
    toggle?.addEventListener('click', () => { if (root.dataset.theme === 'ink') { delete root.dataset.theme; localStorage.setItem('jiuwei-theme', 'cream'); } else { root.dataset.theme = 'ink'; localStorage.setItem('jiuwei-theme', 'ink'); } syncThemeToggle(); });
    const links = [...document.querySelectorAll('[data-toc-link]')];
    const notes = [...document.querySelectorAll('.note-document')];
    const setCurrent = (id) => links.forEach((link) => { const active = link.getAttribute('href') === `#${id}`; link.classList.toggle('is-current', active); if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
    const requested = location.hash.slice(1);
    if (requested && document.getElementById(requested)) setCurrent(requested); else if (notes[0]) setCurrent(notes[0].id);
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => { const visible = entries.filter((entry) => entry.isIntersecting).sort((a,b) => a.boundingClientRect.top - b.boundingClientRect.top)[0]; if (visible) setCurrent(visible.target.id); }, { rootMargin:'-15% 0px -72% 0px', threshold:0 });
      notes.forEach((note) => observer.observe(note));
    }
    document.querySelector('[data-year]').textContent = new Date().getFullYear();
  })();
  </script>
</body>
</html>""".replace("__TOC__", toc).replace("__ARTICLES__", articles)


def main() -> None:
    source = Path(os.environ.get("AGENT_SCAFFOLD_NOTES_SOURCE", DEFAULT_SOURCE))
    notes = sorted(source.glob("*.md"), key=note_number)
    if len(notes) != 22:
        raise RuntimeError(f"Expected 22 Markdown notes in {source}, found {len(notes)}")
    OUTPUT.write_text(render_page(notes), encoding="utf-8")
    print(f"Generated {OUTPUT.name} from {len(notes)} source notes.")


if __name__ == "__main__":
    main()
