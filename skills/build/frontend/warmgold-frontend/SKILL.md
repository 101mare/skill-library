---
name: warmgold-frontend
description: |
  Design system and component patterns for warm, iOS-inspired vanilla frontends.
  Use when building UI components, pages, or styling with HTML/CSS/JS.
  Recognizes: "warmgold", "warmgold design", "warm gold colors", "warm gold style",
  "stone palette", "iOS-style UI", "warm gray", "gold accent"
---

# Warmgold Design System

Warm, iOS-inspired UI built with vanilla HTML, CSS Custom Properties, and semantic HTML5. No frameworks, no build tools.

## Design Philosophy

- **Warm, not cold**: Gold accents, warm grays (stone palette), never blue-ish grays
- **iOS-inspired**: Generous radii, subtle shadows, system fonts, segmented controls
- **Restraint**: Max 0.05 opacity on shadows, accent color for emphasis only
- **Accessible**: WCAG AA contrast, keyboard navigation, reduced motion support

## Composition

This design system provides concrete tokens and components. For broader design principles (typography choices, anti-AI-slop patterns, layout creativity), it composes naturally with the `frontend-design` skill. When both are loaded: use warmgold tokens for implementation, use frontend-design principles for creative direction.

## Core Tokens

```css
:root {
    /* Accent */
    --color-accent: #bda477;
    --color-accent-light: rgba(189, 164, 119, 0.1);
    --color-accent-medium: rgba(189, 164, 119, 0.3);

    /* Backgrounds */
    --color-bg-app: #FAFAF9;
    --color-bg-card: #FFFFFF;
    --color-bg-sidebar: #F5F5F4;

    /* Text (WCAG AA compliant) */
    --color-text-heading: #1c1c1e;
    --color-text-body: #57534e;
    --color-text-muted: #78716c;

    /* Borders & Shadows */
    --color-border: #e7e5e4;
    --color-border-light: #f5f5f4;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03);

    /* Status */
    --color-success: #16a34a;
    --color-success-bg: #f0fdf4;
    --color-error: #dc2626;
    --color-error-bg: #fef2f2;
    --color-warning: #d97706;
    --color-warning-bg: #fffbeb;

    /* Radii */
    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 24px;
    --radius-pill: 100px;

    /* Typography */
    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", Arial, sans-serif;
    --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    --font-size-xs: 0.75rem;    /* 12px */
    --font-size-sm: 0.875rem;   /* 14px */
    --font-size-base: 1rem;     /* 16px */
    --font-size-lg: 1.125rem;   /* 18px */
    --font-size-xl: 1.5rem;     /* 24px */
    --font-size-2xl: 2rem;      /* 32px */

    /* Spacing (8pt grid) */
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-5: 20px;
    --space-6: 24px;
    --space-8: 32px;
    --space-10: 40px;
    --space-12: 48px;

    /* Motion */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
}
```

## Dark Mode

Override the light tokens. Never add new custom properties — redefine existing ones.

Two modes: automatic (OS preference) and manual (user toggle via `data-theme` attribute).

```css
/* Manual toggle (takes priority when set) */
[data-theme="dark"] {
    --color-bg-app: #1c1917;
    --color-bg-card: #292524;
    --color-bg-sidebar: #1c1917;
    --color-text-heading: #fafaf9;
    --color-text-body: #d6d3d1;
    --color-text-muted: #a8a29e;
    --color-border: #44403c;
    --color-border-light: #292524;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
}

/* Auto fallback (only when no data-theme is set) */
@media (prefers-color-scheme: dark) {
    :root:not([data-theme]) {
        --color-bg-app: #1c1917;
        --color-bg-card: #292524;
        --color-bg-sidebar: #1c1917;
        --color-text-heading: #fafaf9;
        --color-text-body: #d6d3d1;
        --color-text-muted: #a8a29e;
        --color-border: #44403c;
        --color-border-light: #292524;
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
}
```

## Component Quick Reference

| Component | Key Styles |
|-----------|-----------|
| **Button Primary** | `background: var(--color-accent); color: white; border-radius: var(--radius-md); padding: 12px 24px;` |
| **Button Secondary** | `background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: var(--radius-md);` |
| **Button Danger** | Default: muted gray. Hover: `background: var(--color-error-bg); color: var(--color-error);` |
| **Card** | `background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: var(--radius-lg); box-shadow: var(--shadow-sm);` |
| **Hero Card** | Card + `border-radius: var(--radius-xl); box-shadow: var(--shadow-lg);` |
| **Badge/Pill** | `border-radius: var(--radius-pill); background: var(--color-accent-light); color: var(--color-accent);` |
| **Input** | `border: 1px solid var(--color-border); border-radius: var(--radius-md);` Focus: `border-color: var(--color-text-muted);` |
| **Toast Success** | `background: var(--color-bg-sidebar); color: var(--color-text-heading);` + green icon |
| **Toast Error** | `background: var(--color-error-bg); color: #991B1B;` + red icon |
| **Nav Active** | White bg, shadow, 3px gold left border |

## Layout

```css
.app-layout {
    display: grid;
    grid-template-columns: 240px 1fr;
    min-height: 100vh;
}

.sidebar {
    background: var(--color-bg-sidebar);
    padding: var(--space-6);
    border-right: 1px solid var(--color-border);
}

.main-content {
    padding: var(--space-8);
    max-width: 1000px;
    margin: 0 auto;
}

/* Tablet: icon-only sidebar */
@media (max-width: 1024px) {
    .app-layout { grid-template-columns: 60px 1fr; }
    .sidebar { padding: var(--space-3); }
    .sidebar .nav-text { display: none; }
}

/* Mobile: stack, no sidebar */
@media (max-width: 768px) {
    .app-layout { grid-template-columns: 1fr; }
    .sidebar { display: none; }
    .main-content { padding: var(--space-4); }
}
```

## Page Template

```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App</title>
    <link rel="stylesheet" href="tokens.css">
    <link rel="stylesheet" href="layout.css">
    <link rel="stylesheet" href="components.css">
</head>
<body>
    <div class="app-layout">
        <aside class="sidebar">
            <nav aria-label="Hauptnavigation">
                <!-- nav items -->
            </nav>
        </aside>
        <main class="main-content">
            <header>
                <h1>Page Title</h1>
            </header>
            <section>
                <!-- content -->
            </section>
        </main>
    </div>
    <div aria-live="polite" class="sr-only" id="status-announcer"></div>
    <script src="app.js"></script>
</body>
</html>
```

## Accessibility

```css
:focus-visible {
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
}

.sr-only {
    position: absolute; width: 1px; height: 1px;
    padding: 0; margin: -1px; overflow: hidden;
    clip: rect(0, 0, 0, 0); border: 0;
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

Requirements: `<html lang>`, semantic tags (`<main>`, `<nav>`, `<aside>`, `<button>`), `aria-label` on icon buttons, 44x44px touch targets, 4.5:1 contrast, never color-only indicators.

## Security

```javascript
// XSS: Always escape before innerHTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Prefer textContent (auto-escapes)
element.textContent = userInput;

// URL validation
function isSafeUrl(url) {
    try {
        const parsed = new URL(url, window.location.origin);
        return ['http:', 'https:'].includes(parsed.protocol);
    } catch { return false; }
}

// Session data: sessionStorage. Preferences only: localStorage.
// NEVER store tokens/secrets in localStorage.
```

## File Organization

```
frontend/
├── index.html
├── css/
│   ├── tokens.css        # Design tokens only
│   ├── layout.css         # Grid, responsive
│   └── components.css     # All component styles
├── js/
│   ├── app.js             # Entry point
│   └── components/        # Per-component JS
└── assets/
    └── icons/             # Inline SVG preferred
```

## Constraints

**Use only:** Vanilla JS, CSS Custom Properties, semantic HTML5, system fonts, inline SVG, Fetch API.

**Never:** React/Vue/Angular/jQuery, Tailwind/SCSS/LESS, external fonts/icon CDNs, cool/blue grays, heavy shadows (>0.05 opacity), hardcoded colors, raw user input in innerHTML.

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Hardcoded hex colors | Use `var(--color-*)` tokens |
| Blue/cool grays | Use warm stone palette |
| Heavy drop shadows | Max 0.05 opacity |
| `innerHTML = userInput` | Use `textContent` or `escapeHtml()` |
| Inconsistent spacing | Use `var(--space-*)` scale |
| Missing focus styles | Add `:focus-visible` outline |
| No dark mode support | Use `prefers-color-scheme` media query |
| Fixed px font sizes | Use `rem` with `var(--font-size-*)` |

## Checklist

- [ ] All colors via CSS Custom Properties (no hardcoded values)
- [ ] Warm color palette (gold accent, stone grays)
- [ ] Dark mode works via `prefers-color-scheme` (auto) or `data-theme` attribute (manual toggle)
- [ ] `<html lang>` set, semantic tags used
- [ ] `:focus-visible` on all interactive elements
- [ ] Touch targets >= 44x44px
- [ ] `prefers-reduced-motion` respected
- [ ] No raw user input in innerHTML
- [ ] Responsive: stacks at 768px
- [ ] System fonts only, no external resources
