---
name: gsd-ui-developer
description: Specialized workflow for UI/frontend phase execution and review. Handles UI specification creation, visual implementation, browser-based verification, screenshot comparison, and accessibility checks. Leverages Manus browser tools for visual validation. Use when executing or reviewing phases that involve user interface work.
---

# GSD UI Developer

Specialized workflow for UI/frontend phases. Adds visual verification, UI specification, and browser-based validation on top of standard phase execution.

For `.gsd/` directory conventions and file formats, see `references/gsd-conventions.md`.

## Quick Start

When the user says "execute UI phase", "build the frontend", "implement the UI", or when a phase involves frontend/UI work:

1. Check for UI-SPEC.md (create if missing)
2. Execute the phase with visual verification
3. Use browser tools for validation

## UI Phase Detection

A phase is a UI phase if any of these are true:
- Phase name contains "UI", "frontend", "interface", "design", "layout"
- Phase plans reference CSS, HTML, React, Vue, Angular, Svelte files
- Phase requirements mention visual elements, responsiveness, or user interaction

When a UI phase is detected, this skill's workflow should be used instead of standard `gsd-phase-executor`.

## UI Specification Workflow

### Step 1: Check for UI-SPEC.md

Look for `XX-UI-SPEC.md` in the phase directory. If missing, create one.

### Step 2: Create UI-SPEC.md

Ask the user about visual requirements:

- **Layout** — What's the page structure? (sidebar, header, grid, etc.)
- **Components** — What UI components are needed? (forms, tables, cards, modals)
- **Responsive** — What breakpoints? (mobile, tablet, desktop)
- **Interactions** — What happens on click, hover, scroll?
- **Branding** — Colors, fonts, spacing conventions?

Write `XX-UI-SPEC.md`:

```markdown
# Phase [X]: [Name] — UI Specification

**Created:** [date]

## Layout
[Description of page/component layout]

## Components
| Component | Purpose | States |
|---|---|---|
| [component] | [what it does] | default, hover, active, disabled |

## Responsive Breakpoints
| Breakpoint | Width | Layout Changes |
|---|---|---|
| Mobile | < 768px | [changes] |
| Tablet | 768-1024px | [changes] |
| Desktop | > 1024px | [changes] |

## Interactions
- [Element] on [event] → [behavior]

## Visual Standards
- **Primary Color:** [hex]
- **Font Family:** [font]
- **Spacing Unit:** [px/rem]
- **Border Radius:** [px]
```

### Step 3: Execute UI Plans

Execute plans as normal (see `gsd-phase-executor`), but with additional UI-specific steps:

1. After implementing each component, use the Manus `browser` tool to navigate to the running application and visually verify
2. Check responsive behavior at each breakpoint
3. Verify interactive states work correctly

### Step 4: Browser-Based Verification

After implementation, start the development server and use Manus browser tools:

```bash
# Start dev server (detect framework)
npm run dev &  # or python manage.py runserver, etc.
```

Then use the `browser` tool to:
1. Navigate to each page/route
2. Verify layout matches UI-SPEC.md
3. Check responsive behavior (viewport resize)
4. Test interactive elements (click, form submission)
5. Check for visual regressions

### Step 5: Accessibility Check

Verify basic accessibility:
- All images have alt text
- Form inputs have labels
- Color contrast is sufficient
- Keyboard navigation works
- ARIA attributes present where needed

Use browser developer tools or run:
```bash
npx lighthouse <url> --only-categories=accessibility --output=json
```

## UI Review Workflow

When reviewing UI work (extends `gsd-code-reviewer`):

### Visual Review

1. Use browser to navigate to each page
2. Compare against UI-SPEC.md
3. Check all responsive breakpoints
4. Verify all interactive states

### Code Review (UI-Specific)

In addition to standard code review, check:
- Component structure and reusability
- CSS organization (no inline styles, consistent naming)
- Responsive implementation (media queries, flexbox/grid)
- Performance (image optimization, lazy loading, bundle size)
- Accessibility compliance

### Write UI Review

Extend the standard REVIEWS.md with a UI section:

```markdown
## UI-Specific Findings

### Visual Accuracy
- [x] Layout matches UI-SPEC.md
- [x] Responsive breakpoints work correctly
- [ ] Mobile navigation needs adjustment

### Accessibility
- [x] Alt text on images
- [ ] Missing ARIA labels on [component]
- [x] Keyboard navigation works

### Performance
- [x] Images optimized
- [ ] Bundle size exceeds 500KB target
```

## Component Library Integration

If the project uses a component library (Material UI, Tailwind, Shadcn, etc.):

1. Verify correct component usage per library docs
2. Check for custom overrides that break library patterns
3. Ensure consistent theming across components
4. Verify tree-shaking is configured for bundle size

## Related Skills

- `gsd-phase-executor` — Standard execution that this skill extends
- `gsd-code-reviewer` — Standard review that this skill extends
- `gsd-research` — Research UI frameworks and patterns
- `gsd-testing` — Generate UI/component tests
