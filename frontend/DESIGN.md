# Psychology Research Lab — Design System

> **Project:** Psychology Research Lab
> **Stack:** Next.js + Tailwind CSS + TypeScript
> **Purpose:** Academic research discovery, organization, analysis, and eventually research writing
> **Design direction:** Scientific editorial × research instrument × modern digital laboratory

---

# 1. Design Philosophy

Psychology Research Lab should **not look like a conventional AI SaaS product**.

Avoid:

* Generic blue/purple gradients
* Giant glowing blobs
* Excessive glassmorphism
* Floating AI sparkles
* Stock photographs of people
* Generic dashboard cards
* Excessive rounded rectangles
* "AI-powered" visual clichés
* Overly playful animations
* Excessive shadows

The product should feel like a tool that a researcher could actually use for hours.

The visual identity should communicate:

> **Precision. Curiosity. Evidence. Depth.**

The website should feel somewhere between:

* an academic journal
* a modern research laboratory
* a sophisticated note-taking application
* an archival system
* a scientific instrument

The interface should be **quiet when idle and alive when interacted with**.

---

# 2. Core Visual Concept

## "The Research Instrument"

The website should behave visually like a scientific instrument.

Static interfaces feel like documents.

Psychology Research Lab should instead feel like the user is **operating a research system**.

Examples:

* Search fields react when focused.
* Search results progressively appear rather than instantly materializing.
* Project cards subtly reveal metadata on hover.
* Saved papers visually "lock" into a project.
* Sections reveal themselves through controlled motion.
* Background elements subtly move with the cursor.
* Research statistics animate into view.
* Search results can transition between states.
* Hovering over academic metadata exposes additional information.
* The interface responds to the user's actions rather than simply displaying content.

The animation should never distract from research.

### Rule

**Motion communicates state, hierarchy, and causality.**

It should not exist simply because animation is possible.

---

# 3. Brand Personality

The product should feel:

| Attribute    | Direction |
| ------------ | --------- |
| Scientific   | High      |
| Academic     | High      |
| Technical    | High      |
| Minimal      | High      |
| Experimental | Medium    |
| Human        | Medium    |
| Playful      | Low       |
| Corporate    | Low       |
| Futuristic   | Medium    |
| AI-like      | Low       |

The product should feel intelligent without constantly telling the user that it is intelligent.

---

# 4. Color System

The primary visual system is built around **warm paper**, **charcoal ink**, and a distinctive **research green**.

This avoids the extremely common blue/purple AI aesthetic.

## 4.1 Base Colors

### `paper`

```text
#F5F3EE
```

Primary page background.

Use for:

* Main website background
* Dashboard background
* Large empty surfaces
* Hero background

Tailwind:

```js
paper: "#F5F3EE"
```

---

### `paper-deep`

```text
#ECE9E1
```

Use for:

* Secondary sections
* Input backgrounds
* Card backgrounds
* Dividers with enough contrast

---

### `paper-light`

```text
#FAF9F6
```

Use for:

* Elevated cards
* Search results
* Modals
* Navigation surfaces

---

## 4.2 Ink

### `ink`

```text
#171816
```

Primary text.

Use for:

* Headings
* Navigation
* Important labels
* Primary UI text

---

### `ink-soft`

```text
#363832
```

Secondary text.

---

### `ink-muted`

```text
#6E7068
```

Use for:

* Metadata
* Timestamps
* Secondary descriptions
* Empty-state explanations

---

### `ink-faint`

```text
#A5A69E
```

Use sparingly for:

* Disabled states
* Extremely low-priority metadata
* Placeholder text

---

# 5. Accent Color

The primary accent should be a **deep research green**, rather than blue.

## `research`

```text
#315C4A
```

This represents:

* Research
* Discovery
* Trust
* Progress
* Knowledge

Use for:

* Primary buttons
* Active states
* Links
* Search focus
* Selected navigation
* Important interactive elements

---

## Accent variations

### `research-dark`

```text
#244536
```

Hover / pressed state.

### `research-light`

```text
#DCE8E1
```

Background for:

* Selected cards
* Active filters
* Success messages

### `research-pale`

```text
#EEF4F0
```

Very subtle research-related surfaces.

---

# 6. Secondary Accent

Use a muted **burnt amber** to represent discovery and attention.

```text
#B56A3C
```

Tailwind:

```js
signal: "#B56A3C"
```

Use for:

* Important findings
* Research highlights
* New papers
* Notifications
* Experimental indicators

Do not use this as a general UI color.

---

# 7. Semantic Colors

## Success

```text
#3D7658
```

Background:

```text
#E5EFE8
```

---

## Warning

```text
#A66B2E
```

Background:

```text
#F4EBDD
```

---

## Error

```text
#A64942
```

Background:

```text
#F3E3E1
```

---

## Information

```text
#526C73
```

Background:

```text
#E5ECEE
```

---

# 8. Complete Tailwind Color Reference

Recommended `tailwind.config.ts`:

```ts
colors: {
  paper: {
    DEFAULT: "#F5F3EE",
    light: "#FAF9F6",
    deep: "#ECE9E1",
  },

  ink: {
    DEFAULT: "#171816",
    soft: "#363832",
    muted: "#6E7068",
    faint: "#A5A69E",
  },

  research: {
    DEFAULT: "#315C4A",
    dark: "#244536",
    light: "#DCE8E1",
    pale: "#EEF4F0",
  },

  signal: {
    DEFAULT: "#B56A3C",
    light: "#F4EBDD",
  },

  success: {
    DEFAULT: "#3D7658",
    light: "#E5EFE8",
  },

  warning: {
    DEFAULT: "#A66B2E",
    light: "#F4EBDD",
  },

  error: {
    DEFAULT: "#A64942",
    light: "#F3E3E1",
  },

  info: {
    DEFAULT: "#526C73",
    light: "#E5ECEE",
  },
}
```

---

# 9. Color Usage Rules

Do not use every color equally.

The visual hierarchy should approximately be:

```text
Paper       55%
Ink         25%
Research    10%
Paper Deep   5%
Signal       3%
Semantic     2%
```

The accent should feel valuable because it is relatively rare.

---

# 10. Typography

The typography should combine:

### Display / editorial font

**Instrument Serif**

Use for:

* Hero headlines
* Major section headings
* Research quotes
* Large editorial moments

This creates the academic/editorial character.

---

### Interface font

**Inter**

Use for:

* Navigation
* Buttons
* Inputs
* Metadata
* Cards
* Dashboard UI
* Body text

---

### Technical font

**JetBrains Mono**

Use for:

* DOI
* OpenAlex IDs
* Search queries
* Research statistics
* Technical metadata
* Status labels
* Small numerical indicators

---

# 11. Typography Hierarchy

## Hero

```text
font-family: Instrument Serif
font-size: clamp(4rem, 8vw, 8rem)
line-height: 0.9
letter-spacing: -0.04em
```

The headline should be visually dominant.

---

## Section heading

```text
font-family: Instrument Serif
font-size: clamp(2.5rem, 5vw, 5rem)
line-height: 0.95
```

---

## Body

```text
font-family: Inter
font-size: 1rem
line-height: 1.7
```

---

## Metadata

```text
font-family: JetBrains Mono
font-size: 0.7rem
letter-spacing: 0.04em
text-transform: uppercase
```

---

# 12. Grid System

The website should use a visible but extremely subtle editorial grid.

Desktop:

```text
12 columns
24px gutters
64px outer margins
```

Tablet:

```text
8 columns
20px gutters
32px margins
```

Mobile:

```text
4 columns
16px gutters
20px margins
```

---

# 13. Grid Lines

Use extremely subtle grid lines:

```text
#D9D7D0
```

Opacity:

```text
30–50%
```

Example:

```css
background-image:
  linear-gradient(
    to right,
    rgba(23, 24, 22, 0.035) 1px,
    transparent 1px
  );
```

The grid should only become obvious when the user looks for it.

---

# 14. Navigation

The navbar should be minimal.

Structure:

```text
PSYCHOLOGY
RESEARCH LAB

        Research    Understand    Write

                         Sign in    Start researching
```

The brand should occupy the left.

Navigation remains centered.

Authentication actions remain right aligned.

---

# 15. Navbar Behavior

Initial state:

```text
transparent
```

As the user scrolls:

```text
background: #FAF9F6
border-bottom: 1px solid #ECE9E1
backdrop-blur
```

Animate:

```text
height
background
border
opacity
```

Duration:

```text
300ms
```

Use Framer Motion.

---

# 16. Navbar Logo Animation

The logo should contain a tiny animated research indicator.

Example:

```text
●
PSYCHOLOGY
RESEARCH LAB
```

The dot can subtly pulse.

Do not make it a glowing neon effect.

Animation:

```text
opacity: 0.45 → 1 → 0.45
duration: 2.5s
ease: easeInOut
repeat: infinite
```

---

# 17. Hero Section

The hero should not look like:

> "AI-powered research platform"

Instead, use an editorial statement.

Example visual structure:

```text
RESEARCH / 001


      Questions
      become
      evidence.

Search academic literature,
organize what you find,
and build research from it.

                    [ Begin research ]
```

The exact marketing copy can evolve independently of the design system.

---

# 18. Hero Animation

On page load:

### Stage 1

Small metadata appears.

```text
RESEARCH / 001
```

Fade + slight vertical movement.

---

### Stage 2

Hero heading reveals line-by-line.

Each line:

```text
opacity: 0 → 1
y: 30px → 0
```

Duration:

```text
600–800ms
```

Stagger:

```text
100ms
```

---

### Stage 3

Description appears.

---

### Stage 4

CTA appears.

---

### Stage 5

Background research grid activates.

---

# 19. Interactive Hero Background

Create a very subtle "research field".

Possible implementation:

* CSS grid
* SVG lines
* small particles
* cursor interaction

When the cursor moves:

```text
nearest grid points move ~4–8px
```

Do not create a particle explosion.

The effect should resemble manipulating a scientific visualization.

---

# 20. Hero Research Visualization

Instead of an illustration, display a dynamic research graph.

Example:

```text
             ●
            / \
           /   ●
          /   / \
         ●---●---●
          \     /
           \---●
```

Each node represents a paper.

Nodes slowly drift.

Connections remain subtle.

On hover:

* node enlarges
* title appears
* connected nodes become slightly more visible

This becomes a recurring visual language throughout the product.

---

# 21. Research Graph

Color:

```text
nodes: #315C4A
lines: #D0D1C9
active: #B56A3C
```

Inactive opacity:

```text
0.35
```

Active opacity:

```text
1
```

---

# 22. Features Section

Do not use six identical cards.

Instead use a **horizontal research process**.

```text
01
RESEARCH

Find the literature.

        ↓

02
UNDERSTAND

Build context.

        ↓

03
WRITE

Turn evidence into knowledge.
```

Each section should have a different interaction.

---

# 23. Research Feature

Visual:

Search interface.

As the user hovers:

```text
"reinforcement learning robotics"
```

appears to be typed into the search field.

Results begin appearing.

Paper cards slide upward.

This should be a simulated visualization rather than a real API request on the landing page.

---

# 24. Understand Feature

Visual:

A paper appears in the center.

Around it:

```text
Concept
Method
Population
Finding
Citation
```

Hovering a concept highlights connections.

This visually foreshadows the future semantic-search system.

---

# 25. Write Feature

Visual:

A research document.

Citation markers appear:

```text
[01]
[02]
[03]
```

Hovering a citation reveals the associated paper.

This communicates the eventual citation assistant without pretending that V1 already has it.

---

# 26. Scroll Animation

Every major section should use scroll-triggered entrance animation.

Preferred behavior:

```text
opacity: 0 → 1
transform: translateY(40px) → 0
```

Duration:

```text
700ms
```

Ease:

```text
cubic-bezier(0.16, 1, 0.3, 1)
```

Avoid:

```text
bounce
elastic
large rotations
```

The movement should feel precise.

---

# 27. Paper Cards

Paper cards should feel like archival records.

Structure:

```text
RESEARCH PAPER

The Effects of ...

Author 01 · Author 02 · 2026

Journal / Conference

Abstract preview...

DOI
────────────────────

SAVE TO PROJECT →
```

Avoid large colorful thumbnails.

Academic papers generally do not need image-heavy cards.

---

# 28. Paper Card Hover

On hover:

```text
translateY(-4px)
```

Border becomes slightly darker.

Metadata becomes more visible.

A small accent line animates from:

```text
width: 0
```

to:

```text
width: 100%
```

The card should feel like it is being inspected.

---

# 29. Save Animation

When saving a paper:

1. Save icon compresses.
2. Paper card briefly highlights.
3. Icon changes state.
4. Small line travels toward the project indicator.
5. Toast appears.

Example:

```text
Paper
  ↓
Project
```

The animation should communicate **where the paper went**.

---

# 30. Search Interface

The search bar should be one of the most visually important components.

Large search field:

```text
┌───────────────────────────────────────────────┐
│ What are you researching?                  ↵ │
└───────────────────────────────────────────────┘
```

Border:

```text
#D2D1C9
```

Focus:

```text
#315C4A
```

Background:

```text
#FAF9F6
```

---

# 31. Search Interaction

On focus:

```text
border-color → research
box-shadow → 0 0 0 4px research-light
```

Placeholder subtly moves upward or disappears.

Search button transforms from:

```text
→
```

to:

```text
SEARCH
```

on desktop.

---

# 32. Search Loading State

Do not use a generic spinner.

Instead show:

```text
SEARCHING LITERATURE

● ─── ● ───── ● ── ●
```

The line progressively moves across.

Alternatively:

A small research graph builds itself.

This is much more aligned with the product.

---

# 33. Empty Search State

Instead of:

> No results found.

Use:

```text
NO LITERATURE FOUND

The question produced no matching
academic records.

Try broadening the terminology.
```

Include suggestions.

---

# 34. Dashboard Design

The dashboard should look more like a research workstation than an admin panel.

Structure:

```text
┌──────────────────────────────────────────────┐
│ Research Lab                         Account │
├──────────────┬───────────────────────────────┤
│ PROJECTS     │                               │
│              │ Current research              │
│ + New        │                               │
│              │                               │
│ Psychology   │                               │
│ Sleep        │                               │
│ Memory       │                               │
│              │                               │
└──────────────┴───────────────────────────────┘
```

---

# 35. Dashboard Sidebar

Background:

```text
#ECE9E1
```

Active project:

```text
#FAF9F6
```

Active indicator:

```text
#315C4A
```

The sidebar should remain relatively static.

The content area is where most interaction occurs.

---

# 36. Project Cards

Project cards should display:

```text
PROJECT / 004

The relationship between
sleep and memory

24 PAPERS

UPDATED
02 OCT 2026
```

Use monospaced metadata.

On hover:

```text
card → translateY(-3px)
arrow → translateX(4px)
```

---

# 37. Project Creation

The project creation UI should feel like opening a new research notebook.

Example:

```text
NEW PROJECT

What are you investigating?

[ Research question........................ ]

PROJECT NAME

[ Memory and Sleep......................... ]

                    CREATE PROJECT →
```

When submitted, animate:

```text
form
 ↓
project record
 ↓
workspace
```

This makes the product feel continuous rather than page-based.

---

# 38. Project Workspace

Header:

```text
PROJECT / 004

The relationship between
sleep and memory

24 PAPERS
LAST UPDATED 2H AGO
```

Navigation:

```text
Research     Understand     Write
```

These should correspond directly to the product's three core concepts.

---

# 39. Research Tab

Main components:

```text
Search literature

Filters

Search results

Saved papers
```

Filters:

* Year
* Author
* Journal
* Open access
* Type

Filters should animate open rather than abruptly appearing.

---

# 40. Understand Tab

Although advanced understanding functionality is V2/V3/V4, reserve the design space now.

Possible future UI:

```text
CONCEPT MAP

     Memory
      /   \
 Sleep     Recall
   |        |
 Stress   Learning
```

The design system should make this feel native when eventually implemented.

---

# 41. Write Tab

V1 can display:

```text
WRITING WORKSPACE

Coming later

Your saved research will eventually
become the foundation of your paper.
```

Do not make it look like a dead placeholder.

Use a partially animated document interface.

---

# 42. Microinteractions

Every important interaction should have feedback.

Examples:

### Button

```text
hover:
translateY(-1px)

active:
translateY(0)

duration:
150ms
```

### Link

Underline expands from left to right.

### Icon

Slight movement toward intended action.

### Checkbox

Checkmark draws itself.

### Toggle

Slider moves using spring animation.

### Save

Paper visibly transitions into saved state.

---

# 43. Motion System

Use **Framer Motion** / Motion for React.

Recommended motion presets:

## Fast

```text
150ms
```

Microinteractions.

## Normal

```text
300ms
```

UI state transitions.

## Slow

```text
600–900ms
```

Page/section entrances.

## Editorial

```text
900–1400ms
```

Hero animations and large visual transitions.

---

# 44. Easing

Primary:

```text
cubic-bezier(0.16, 1, 0.3, 1)
```

Secondary:

```text
cubic-bezier(0.4, 0, 0.2, 1)
```

Never use linear motion for important interface transitions unless it represents a process.

---

# 45. Cursor Interactions

Desktop only.

Use subtle cursor-following effects.

Examples:

* Hero research graph
* Feature visualization
* Paper card accent
* Background grid

Maximum movement:

```text
8px
```

The cursor should influence the interface, not dominate it.

Disable these effects on:

```text
prefers-reduced-motion
mobile
low-power devices
```

---

# 46. Page Transitions

Navigation between major sections can use a short editorial transition.

Example:

```text
current page
opacity → 0
clip-path → inset(...)
new page
clip-path → inset(...)
opacity → 1
```

Keep duration below:

```text
500ms
```

Do not create dramatic cinematic transitions.

---

# 47. Scroll Behavior

Use smooth scrolling where appropriate.

Sections should reveal:

```text
label
↓
heading
↓
description
↓
visual
```

rather than everything appearing simultaneously.

---

# 48. Background Details

The website should have subtle visual texture.

Recommended:

* Grid
* Fine paper noise
* Very subtle radial gradients
* Thin lines
* Research graph nodes
* Editorial dividers

Avoid:

* Large blobs
* Neon gradients
* 3D abstract objects
* Excessive particles

---

# 49. Paper Texture

A very subtle noise texture can be applied globally.

Opacity:

```text
0.025–0.04
```

The user should not consciously notice it.

It should simply prevent the background from feeling like a perfectly flat digital canvas.

---

# 50. Borders

Default:

```text
#DCDAD2
```

Strong:

```text
#C9C7BF
```

Accent:

```text
#315C4A
```

Borders should generally be:

```text
1px
```

Avoid heavy card borders.

---

# 51. Border Radius

The design should intentionally use relatively restrained rounding.

Default:

```text
8px
```

Inputs:

```text
8px
```

Cards:

```text
10px
```

Large surfaces:

```text
12px
```

Buttons:

```text
6px
```

Do not use:

```text
rounded-full
```

for most UI.

Pills should only be used for tags/statuses.

---

# 52. Shadows

Shadows should be almost invisible.

Default:

```css
box-shadow:
0 4px 20px rgba(23, 24, 22, 0.05);
```

Hover:

```css
box-shadow:
0 12px 30px rgba(23, 24, 22, 0.08);
```

Avoid dark shadows.

---

# 53. Buttons

## Primary

Background:

```text
#315C4A
```

Text:

```text
#FAF9F6
```

Hover:

```text
#244536
```

---

## Secondary

Background:

```text
transparent
```

Border:

```text
#C9C7BF
```

Text:

```text
#171816
```

Hover:

```text
#ECE9E1
```

---

## Destructive

Background:

```text
#A64942
```

Use sparingly.

---

# 54. Button Animation

Primary buttons should have a small directional movement.

Example:

```text
[ Begin research → ]
```

Hover:

```text
arrow translateX(4px)
```

The button itself moves only:

```text
1px
```

This gives the interaction a physical quality.

---

# 55. Icons

Use:

**Lucide React**

Reasons:

* Minimal
* Consistent
* Open source
* Works naturally with Tailwind
* Fits the editorial/scientific aesthetic

Avoid giant illustrated icons.

Icon stroke width:

```text
1.5–1.75
```

---

# 56. Recommended Libraries

## Required

### Motion

```bash
npm install motion
```

Use for:

* Page transitions
* Scroll animations
* Microinteractions
* Graph animations

---

### Lucide

```bash
npm install lucide-react
```

---

## Optional

### Lenis

For highly polished scrolling:

```bash
npm install lenis
```

Use only if the default browser scrolling does not provide the desired feel.

Do not sacrifice accessibility for smooth scrolling.

---

### React Aria

Useful for accessible advanced components:

```bash
npm install react-aria-components
```

Particularly useful for:

* Dialogs
* Dropdowns
* Selects
* Tabs
* Menus

---

# 57. Do Not Overuse Libraries

Do not install:

* Three.js just for visual effects
* GSAP unless Motion becomes insufficient
* Particle libraries
* Heavy animation frameworks
* Multiple UI component libraries

The design should primarily come from:

```text
CSS
+
Tailwind
+
Motion
+
SVG
```

---

# 58. Accessibility

Animations must respect:

```css
@media (prefers-reduced-motion: reduce)
```

When enabled:

```text
disable decorative motion
reduce transitions
remove parallax
remove cursor effects
```

Do not disable essential state feedback.

---

# 59. Responsive Design

## Desktop

The full research visualization system can be active.

Use:

* Grid
* Graph
* Hover states
* Cursor interactions
* Horizontal layouts

---

## Tablet

Reduce:

* Graph complexity
* Decorative motion
* Sidebar width

---

## Mobile

Prioritize:

```text
content
navigation
search
papers
projects
```

Remove:

* Cursor effects
* Complex graph animations
* Large decorative backgrounds

---

# 60. Mobile Navigation

Use a simple full-screen menu.

Animation:

```text
clip-path: inset(0 0 100% 0)
```

to:

```text
clip-path: inset(0)
```

Menu links should stagger into view.

---

# 61. Loading States

Never display a blank page.

Use skeletons that resemble actual content.

Example paper skeleton:

```text
────────────────────────────
██████████████████

████████████████████████

██████████████

████████
────────────────────────────
```

Use:

```text
#E7E5DE
```

for skeleton blocks.

Animation should be a subtle horizontal shimmer.

---

# 62. Error States

Error states should feel like the rest of the application.

Example:

```text
RESEARCH INTERRUPTED

The literature service could not be reached.

Try again.

[ Retry ]
```

Avoid generic:

```text
Something went wrong :)
```

---

# 63. Toasts

Toasts should appear in the bottom-right.

Example:

```text
✓
Paper saved to "Sleep Research"
```

Animation:

```text
opacity
x: 20 → 0
```

Duration:

```text
300ms
```

Auto-dismiss:

```text
4 seconds
```

---

# 64. Landing Page Structure

The complete landing page should follow:

```text
NAVBAR

        ↓

HERO

        ↓

RESEARCH VISUALIZATION

        ↓

THE PROBLEM

        ↓

RESEARCH / UNDERSTAND / WRITE

        ↓

INTERACTIVE PRODUCT DEMO

        ↓

HOW IT WORKS

        ↓

RESEARCH GRAPH

        ↓

FINAL CTA

        ↓

FOOTER
```

---

# 65. Problem Section

Keep this editorial.

Example structure:

```text
RESEARCH IS NOT
A SEARCH BOX.

The difficult part isn't finding
one paper.

It's understanding the landscape
around a question.
```

The typography should carry the section.

Minimal decoration.

---

# 66. Product Demonstration

Create a simulated workspace.

User enters:

```text
How does sleep affect memory consolidation?
```

Then:

```text
Searching literature...
```

Then papers appear.

Then:

```text
12 relevant papers
```

Then one paper is saved.

This entire sequence can be automatically animated.

The animation should loop slowly.

---

# 67. Interactive Demo State Machine

Conceptually:

```text
idle
 ↓
typing
 ↓
searching
 ↓
results
 ↓
inspect
 ↓
save
 ↓
saved
```

Each state should have its own visual transition.

This is significantly better than an animated screenshot.

---

# 68. Research Graph Section

The graph should communicate that research is interconnected.

Example:

```text
              Memory
             /      \
          Sleep     Recall
          /           \
     Consolidation   Learning
          \           /
             Stress
```

Nodes can represent:

```text
paper
concept
author
topic
```

This becomes the visual foundation for future semantic search.

---

# 69. Final CTA

Do not end with:

> Start using our AI platform.

Instead:

```text
YOUR NEXT QUESTION
IS ALREADY WAITING.

Begin with a question.
Build from evidence.

[ Enter the lab → ]
```

Use the largest typography after the hero.

---

# 70. Footer

Minimal.

Left:

```text
PSYCHOLOGY
RESEARCH LAB
```

Middle:

```text
Research
Understand
Write
```

Right:

```text
GitHub
Privacy
Terms
```

Bottom:

```text
A research instrument for curious minds.
```

---

# 71. Dashboard Design Tokens

Suggested spacing:

```text
page padding: 32px
section gap: 64px
card padding: 24px
input padding: 14px 16px
button padding: 12px 18px
```

Mobile:

```text
page padding: 20px
section gap: 40px
card padding: 18px
```

---

# 72. Z-Index System

Keep the hierarchy predictable.

```text
base: 0
decorative: 1
content: 10
sticky navigation: 50
dropdown: 100
modal backdrop: 200
modal: 300
toast: 400
```

---

# 73. Animation Architecture

Create reusable Motion variants.

Example conceptual system:

```ts
fadeUp
fadeIn
scaleIn
staggerContainer
pageEnter
pageExit
cardHover
buttonHover
```

Do not write completely different animation logic for every component.

---

# 74. Reusable Components

Create:

```text
Navbar
Button
MagneticButton
SectionLabel
ResearchGrid
ResearchGraph
PaperCard
PaperMetadata
ProjectCard
SearchBar
SearchResult
SaveButton
Toast
Modal
AnimatedCounter
Reveal
Stagger
```

---

# 75. Design Component Naming

Use semantic names.

Good:

```tsx
<PaperCard />
<ResearchGraph />
<ProjectCard />
```

Bad:

```tsx
<GreenBox />
<BigCard />
<Thing />
```

---

# 76. Landing Page Component Structure

Recommended:

```text
app/
├── page.tsx
├── layout.tsx
└── components/
    ├── landing/
    │   ├── Navbar.tsx
    │   ├── Hero.tsx
    │   ├── ResearchGraph.tsx
    │   ├── Problem.tsx
    │   ├── ResearchProcess.tsx
    │   ├── ProductDemo.tsx
    │   ├── HowItWorks.tsx
    │   ├── FinalCTA.tsx
    │   └── Footer.tsx
    │
    └── ui/
        ├── Button.tsx
        ├── SectionLabel.tsx
        ├── Reveal.tsx
        └── MagneticButton.tsx
```

---

# 77. Dashboard Component Structure

```text
app/
└── app/
    ├── page.tsx
    ├── projects/
    │   └── [id]/
    │       └── page.tsx
    │
    └── components/
        ├── Sidebar.tsx
        ├── ProjectList.tsx
        ├── ProjectCard.tsx
        ├── ProjectHeader.tsx
        ├── ResearchSearch.tsx
        ├── PaperCard.tsx
        ├── PaperList.tsx
        └── SavedPapers.tsx
```

---

# 78. Design Principle for V1

V1 should **look more sophisticated than it functionally is**, but it must never pretend that functionality exists when it does not.

For example:

The landing page can demonstrate future semantic research visually.

The actual V1 workspace should only expose:

```text
Projects
Search
Save
Remove
```

Do not create fake AI functionality in the real application.

---

# 79. Future-Proof Visual Language

The roadmap should progressively activate existing visual concepts.

## V1

```text
Research
```

Search academic papers.

---

## V2

```text
Understand
```

PDF extraction and notes.

The document visualization becomes functional.

---

## V3

Semantic graph becomes functional.

---

## V4

AI answers appear inside the research graph.

Citations connect answers to papers.

---

## V5

Reddit appears as a second evidence source.

---

## V6

Themes emerge from Reddit.

---

## V7

Scientific literature and lived experience can be compared visually.

Example:

```text
SCIENTIFIC LITERATURE

        ↕
     COMPARISON
        ↕

LIVED EXPERIENCE
```

---

## V8

Writing becomes a complete research environment.

The entire visual system should therefore feel like it was designed for this future from the beginning.

---

# 80. Reddit Visual Language

When Reddit is eventually introduced, do not visually make it equal to academic literature.

Scientific literature:

```text
structured
formal
high-confidence
```

Lived experiences:

```text
messy
personal
contextual
```

They should have distinct visual treatments while remaining part of the same system.

For example:

```text
ACADEMIC
research green

LIVED EXPERIENCE
burnt amber
```

This distinction can become a major visual feature of V7.

---

# 81. Research Confidence

Eventually, confidence can be visually represented through opacity and line weight rather than giant badges.

Example:

```text
Strong evidence
██████████

Moderate evidence
███████

Limited evidence
████
```

Do not use simplistic "AI confidence: 97%" interfaces.

---

# 82. Data Visualization

Charts should use the existing palette.

Primary:

```text
#315C4A
```

Secondary:

```text
#B56A3C
```

Neutral:

```text
#A5A69E
```

Background:

```text
#FAF9F6
```

Charts should remain editorial rather than looking like financial dashboards.

---

# 83. Dark Mode

Do not implement dark mode immediately.

The light theme is central to the brand.

If dark mode is eventually added:

```text
background: #151714
surface: #1E211D
text: #F2F0E9
muted: #A9AAA2
research: #76A58E
signal: #D08A60
```

Dark mode should be treated as a separate visual system rather than simply inverting colors.

---

# 84. Performance Requirements

Animations must not compromise the research experience.

Prefer:

```text
transform
opacity
clip-path
```

Avoid animating:

```text
width
height
top
left
box-shadow
```

unless necessary.

Use:

```text
will-change
```

only where appropriate.

Do not animate hundreds of DOM elements simultaneously.

---

# 85. Motion Accessibility

Respect:

```text
prefers-reduced-motion
```

For reduced motion:

```text
fade only
```

No:

```text
parallax
graph movement
cursor following
large transforms
```

---

# 86. Performance Budget for Decorative Effects

At any point:

```text
≤ 1 major animated background
≤ 1 interactive graph
≤ 3 simultaneous decorative motion systems
```

The interface should never look like a landing-page template overloaded with effects.

---

# 87. Visual Hierarchy Rule

Every page should answer these questions immediately:

### 1. Where am I?

Project / Research / Understand / Write.

### 2. What am I doing?

Searching, reading, organizing, etc.

### 3. What can I interact with?

Clear visual affordances.

### 4. What changed?

Motion and state feedback.

---

# 88. The Most Important Design Rule

The interface should feel **alive because information is moving through it**.

Not because random objects are floating around.

Good:

```text
question
 ↓
search
 ↓
papers
 ↓
project
 ↓
evidence
```

Bad:

```text
random blob
 ↓
sparkles
 ↓
floating cards
 ↓
gradient
```

Every animation should reinforce the research process.

---

# 89. Final Visual Identity

The final product should feel like:

> **A digital research laboratory built inside an academic journal.**

Not:

> another AI research SaaS dashboard.

The visual signature is:

```text
Warm paper
+
Dark editorial typography
+
Deep research green
+
Burnt amber signals
+
Fine grid
+
Academic metadata
+
Research graph
+
Controlled motion
+
Precise microinteractions
```

---

# 90. Final Implementation Checklist

## Brand

* [ ] Instrument Serif installed
* [ ] Inter installed
* [ ] JetBrains Mono installed
* [ ] Color tokens implemented
* [ ] Typography tokens implemented

## Landing Page

* [ ] Animated navbar
* [ ] Hero entrance animation
* [ ] Interactive research graph
* [ ] Problem section
* [ ] Research / Understand / Write section
* [ ] Interactive product demo
* [ ] Research graph section
* [ ] Final CTA
* [ ] Footer

## Dashboard

* [ ] Animated sidebar
* [ ] Project cards
* [ ] Project creation
* [ ] Project workspace
* [ ] Search interface
* [ ] Search loading animation
* [ ] Paper cards
* [ ] Save animation
* [ ] Saved papers
* [ ] Empty states
* [ ] Error states
* [ ] Toasts

## Motion

* [ ] Motion installed
* [ ] Shared animation variants
* [ ] Scroll reveal
* [ ] Hover states
* [ ] Page transitions
* [ ] Reduced-motion support
* [ ] Mobile motion reduction

## Accessibility

* [ ] Keyboard navigation
* [ ] Visible focus states
* [ ] Semantic HTML
* [ ] ARIA labels where necessary
* [ ] Reduced-motion support
* [ ] Sufficient contrast

## Responsive

* [ ] Desktop
* [ ] Tablet
* [ ] Mobile
* [ ] Mobile navigation
* [ ] Mobile search
* [ ] Graph simplification

## Quality

* [ ] No unnecessary UI library
* [ ] No excessive gradients
* [ ] No decorative animation without purpose
* [ ] No mock data in production workspace
* [ ] Loading states implemented
* [ ] Error states implemented
* [ ] Empty states implemented
* [ ] Performance checked

```

# 91. One-Sentence Design Brief

**Psychology Research Lab is a calm, editorial research instrument where warm paper, precise typography, scientific data visualization, and purposeful motion turn the act of finding and organizing evidence into an interactive experience.**

For implementation, I would use **Motion + Lucide React** as the core additions and avoid adding a large component library. The distinctive parts—research graph, animated search, paper transitions, grid, and editorial motion—should be custom-built so the site does not end up looking like a Tailwind template.
```
