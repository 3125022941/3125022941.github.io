# Interaction polish design

## Goal

Make the portfolio's existing interactions feel direct and useful without changing its information architecture, public URLs, navigation labels, or editorial voice. The audience remains recruiters and technical peers. This is a targeted evolution: variance 6, motion 4, density 5.

## Scope

1. **Project discovery**: make each published project card one coherent interactive target. The established GitHub destination for Agent Scaffold stays unchanged. Projects without a public repository lead to the relevant on-page context instead of a dead arrow target.
2. **Notes reading flow**: route homepage note entry points to `notes.html`; add keyboard-visible focus treatments, a persistent table of contents, active-section state, and hash updates while reading.
3. **Current focus**: replace the existing decorative LEARN / BUILD / AUTOMATE picker with a content switcher. Choosing a lens changes the supporting copy and routes the primary action to an existing, relevant destination.
4. **Theme and touch parity**: use the same stateful sun/moon SVG control on the homepage and notes page, preserve the `jiuwei-theme` preference, and give the control a 44px touch target.

## Behaviour and accessibility

- Controls preserve explicit `aria-label`, selected state, keyboard operation, and visible `:focus-visible` feedback.
- Notes navigation uses `IntersectionObserver`, not a scroll event listener. At any time exactly one visible chapter is marked as current. Clicking a chapter still uses ordinary hash navigation.
- Motion is limited to existing small state transitions. `prefers-reduced-motion: reduce` removes transition movement.
- Mobile behavior is a first-class path: cards retain one tappable target, the table of contents keeps usable inline links, and the theme control is at least 44 by 44 pixels.

## Out of scope

- No new project pages, external profiles, analytics, content rewrite, route migration, or redesign of the visual system.
- No fabricated project progress, demos, or contact links.

## Verification

- Automated structure tests verify the real links, theme parity, card interaction contract, and notes active-state hooks.
- Browser checks cover keyboard focus, mobile navigation, touch targets, dark-mode persistence, hash navigation, and no console errors or horizontal overflow.
