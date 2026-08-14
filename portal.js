(() => {
  const root = document.documentElement;
  const themeToggle = document.querySelector('[data-theme-toggle]');
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  const syncThemeToggle = () => {
    if (!themeToggle) return;
    const isInk = root.dataset.theme === 'ink';
    const label = isInk ? '切换到日间模式' : '切换到夜间模式';
    themeToggle.setAttribute('aria-label', label);
    themeToggle.title = label;
  };
  if (localStorage.getItem('jiuwei-theme') === 'ink') root.dataset.theme = 'ink';
  syncThemeToggle();
  themeToggle?.addEventListener('click', () => {
    if (root.dataset.theme === 'ink') { delete root.dataset.theme; localStorage.setItem('jiuwei-theme', 'cream'); }
    else { root.dataset.theme = 'ink'; localStorage.setItem('jiuwei-theme', 'ink'); }
    syncThemeToggle();
  });
  const closeNav = () => { navToggle?.setAttribute('aria-expanded', 'false'); nav?.classList.remove('is-open'); };
  navToggle?.addEventListener('click', () => {
    const open = navToggle.getAttribute('aria-expanded') !== 'true';
    navToggle.setAttribute('aria-expanded', String(open));
    nav?.classList.toggle('is-open', open);
  });
  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeNav));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') { closeNav(); navToggle?.focus(); } });
  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
