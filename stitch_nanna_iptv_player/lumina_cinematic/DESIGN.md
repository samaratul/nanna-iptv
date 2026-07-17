---
name: Lumina Cinematic
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#3e484f'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#6e7980'
  outline-variant: '#bdc8d1'
  surface-tint: '#00668a'
  primary: '#00668a'
  on-primary: '#ffffff'
  primary-container: '#38bdf8'
  on-primary-container: '#004965'
  inverse-primary: '#7bd0ff'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#516072'
  on-tertiary: '#ffffff'
  tertiary-container: '#a3b2c7'
  on-tertiary-container: '#364557'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c4e7ff'
  primary-fixed-dim: '#7bd0ff'
  on-primary-fixed: '#001e2c'
  on-primary-fixed-variant: '#004c69'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#d4e4fa'
  tertiary-fixed-dim: '#b9c8de'
  on-tertiary-fixed: '#0d1c2d'
  on-tertiary-fixed-variant: '#39485a'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 72px
    fontWeight: '800'
    lineHeight: 80px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
  title-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  body-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '400'
    lineHeight: 32px
  body-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '400'
    lineHeight: 28px
  label-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  edge-margin: 80px
  gutter: 24px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
  section-gap: 80px
---

## Brand & Style

The design system is centered on a "Soft Cinematic Light" aesthetic, diverging from the traditional dark-mode dominance of streaming platforms to offer an airy, premium, and high-end experience. The brand personality is sophisticated and modern, aiming to evoke a sense of clarity and calm.

The visual style leverages **Glassmorphism** as its core structural pillar. Interfaces are built using translucent layers, frosted glass effects, and subtle background blurs that interact with vibrant, high-definition content. This approach ensures the UI feels like a lightweight overlay rather than a heavy barrier between the user and their media. The primary accent, a vibrant Electric Blue, is used sparingly to denote focus and active states, providing a high-energy contrast against the soft, neutral backdrop.

## Colors

The palette is anchored by a foundation of soft whites and cool grays to maintain an "airy" feel.

- **Primary (Electric Blue):** Used exclusively for focus states, progress bars, and critical action buttons. It represents the "energy" of the system.
- **Secondary (Slate Deep):** Reserved for high-contrast text and icon details to ensure legibility against light backgrounds.
- **Neutral (Cloud White):** The base surface color. It is often used with varying levels of opacity (80-95%) to create the glassmorphic effect.
- **Surface Tints:** Use subtle gradients of `#f8fafc` to `#e2e8f0` for container backgrounds to add depth without adding weight.

## Typography

This design system utilizes **Inter** for all roles to ensure maximum legibility at typical 10-foot TV viewing distances. The hierarchy is intentionally dramatic, using significant size differentials to guide the eye across a large screen.

- **Display & Headlines:** Use heavy weights (Bold/ExtraBold) with tight letter spacing for a cinematic, editorial feel.
- **Body Text:** Maintained at a minimum of 20px for accessibility on Smart TVs.
- **Labels:** Uppercase styling is recommended for category labels and metadata tags to provide a distinct visual rhythm compared to narrative text.

## Layout & Spacing

The layout follows a **Fixed Grid** model optimized for 16:9 displays. 

- **Safe Areas:** A generous 80px "overscan" margin is maintained on all sides to ensure content is never clipped by physical TV bezels.
- **Horizontal Flow:** Content is primarily organized in horizontal "Shelves" or "Carousels."
- **Grid Structure:** A 12-column system is used for dashboard views, while carousels use a "Peek" behavior where the last visible item is partially cut off to indicate further content.
- **Focus Scaling:** When an element (like a movie poster) gains focus, it should scale by 10-12% and increase its z-index, requiring extra "breathing room" in the spacing tokens to prevent overlapping neighboring text.

## Elevation & Depth

Depth is achieved through material properties rather than traditional drop shadows.

- **Glassmorphic Tiers:**
    - **Level 1 (Base):** Clean background content.
    - **Level 2 (Panels):** 60% opacity white with a 32px backdrop blur and a 1px inner white border (highlight).
    - **Level 3 (Focused Elements):** 90% opacity white, no blur, with a soft ambient shadow (Color: `#0f172a`, Alpha: 0.08, Blur: 40px).
- **Gradients:** Use linear gradients (Top-Left to Bottom-Right) of `white` at 20% to `white` at 5% to simulate light hitting a physical glass surface.

## Shapes

The shape language is defined by large, friendly radii that reinforce the premium feel.

- **Standard Containers:** Use `rounded-lg` (16px) for movie cards and standard panels.
- **Action Elements:** Buttons and focus indicators use `rounded-xl` (24px) to create a soft, inviting touchpoint.
- **Small Elements:** Tooltips and tags use a smaller 8px radius to maintain clarity at small scales.

## Components

### Buttons & Navigation
- **Primary Button:** Electric Blue background with white text. On focus, it pulses slightly.
- **Ghost Button:** Glassmorphic background (15% white) with a 1px border.
- **Sidebar:** A persistent or collapsible vertical bar using a heavy backdrop blur (60px) to keep the background content visible but non-distracting.

### Media Cards
- **Poster Cards:** 2:3 aspect ratio with a subtle 1px inner stroke. On focus, the title metadata appears below the card in a bold weight.
- **Live TV Tiles:** 16:9 aspect ratio featuring a progress bar at the bottom using the Electric Blue primary color.

### Selection Controls
- **Checkboxes/Radios:** Circular designs that use a "glow" effect when focused, echoing the Electric Blue accent.
- **Search Input:** A full-width glass bar that expands when active, using a large search icon for visibility.

### Focus Ring
- Instead of a traditional border, focused elements should utilize a "Glass Glow"—a 4px outer stroke of semi-transparent Electric Blue combined with a subtle increase in the element's internal brightness.