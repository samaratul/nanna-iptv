---
name: Cinematic Immersive
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#bdc8d1'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#87929a'
  outline-variant: '#3e484f'
  surface-tint: '#7bd0ff'
  primary: '#8ed5ff'
  on-primary: '#00354a'
  primary-container: '#38bdf8'
  on-primary-container: '#004965'
  inverse-primary: '#00668a'
  secondary: '#ffb95f'
  on-secondary: '#472a00'
  secondary-container: '#ee9800'
  on-secondary-container: '#5b3800'
  tertiary: '#56e5a9'
  on-tertiary: '#003824'
  tertiary-container: '#30c88f'
  on-tertiary-container: '#004e34'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#c4e7ff'
  primary-fixed-dim: '#7bd0ff'
  on-primary-fixed: '#001e2c'
  on-primary-fixed-variant: '#004c69'
  secondary-fixed: '#ffddb8'
  secondary-fixed-dim: '#ffb95f'
  on-secondary-fixed: '#2a1700'
  on-secondary-fixed-variant: '#653e00'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '400'
    lineHeight: 30px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  sidebar-width: 280px
  sidebar-collapsed-width: 88px
  grid-gutter: 24px
  screen-margin: 64px
  stack-gap: 16px
---

## Brand & Style
The design system is engineered for a high-end, cinematic lean-back experience. It prioritizes content immersion by utilizing a deep, dark canvas that recedes, allowing media artwork and live streams to take center stage. The target audience seeks a premium, theater-like atmosphere on Google TV.

The design style is **Corporate / Modern** with a **Glassmorphic** twist. It employs high-contrast focus states and subtle depth through translucent layers to ensure the interface feels responsive and premium. The emotional response is one of sophistication, reliability, and entertainment-first focus.

## Colors
The palette is rooted in deep navy and charcoal to minimize light bleed on large television screens. 

- **Primary**: A vivid sky blue (#38BDF8) used exclusively for active focus states and interactive highlights.
- **Secondary**: A rich gold (#F59E0B) used for "Premium" or "Featured" badges and star ratings.
- **Status Indicators**: Functional colors are used for connectivity states: `success` (green) for active streams and `error` (red) for offline channels.
- **Neutral**: The background is a solid #0F172A, with surface containers using #1E293B at varying opacities to create hierarchy.

## Typography
Legibility at a distance (the "10-foot UI") is the primary driver for this design system. Inter is utilized for its exceptional X-height and clarity.

- **Display & Headlines**: Bold weights are used for show titles and category headers to ensure they are scannable from across a room.
- **Body Text**: Maintain a minimum of 16px for secondary info; 20px is preferred for descriptions to avoid eye strain.
- **Labels**: Used for metadata (HD/4K, Duration, Genre). Label-lg uses uppercase styling with increased letter spacing for a technical, metadata-heavy look.

## Layout & Spacing
The layout follows a **Fixed Grid** model tailored for 16:9 television displays. 

- **Navigation**: A persistent left-hand sidebar. On focus, it expands to 280px; when navigating the main grid, it collapses to 88px showing only icons.
- **Main Content**: A 6-column grid on desktop/TV resolutions. 
- **Safe Areas**: A generous 64px outer margin ensures content is never cut off by physical bezel constraints or overscan.
- **Rhythm**: All spacing is derived from an 8px base unit to maintain strict alignment of cards and lists.

## Elevation & Depth
Depth is communicated through **Tonal Layers** and **Glassmorphism**. 

- **Level 0**: Base background (#0F172A).
- **Level 1**: Content cards and sidebar (#1E293B at 80% opacity with a 20px backdrop blur).
- **Level 2 (Focus State)**: When an element is focused via D-pad, it scales up by 5% and gains a 2px primary-colored solid border and a soft glow (15px blur) of the same color.
- **Overlays**: Modals and player controls use a 40% black tint with heavy backdrop blur to keep the background video visible but secondary.

## Shapes
The design system uses a very high corner radius to evoke a modern, friendly, and "app-like" feel common in premium streaming hardware.

- **Standard Elements**: Buttons and small inputs use `rounded-lg` (16px).
- **Channel Cards**: Use `rounded-xl` (24px) for a distinctive, pillowy aesthetic.
- **Focus Rings**: Must follow the exact outer radius of the element they wrap.

## Components
- **Channel Cards**: Aspect ratio 16:9 for live TV or 2:3 for VOD. Content includes a background poster, a bottom-aligned text gradient for titles, and a status dot in the top-right.
- **Sidebar Nav**: Icons should be 24px, accompanied by Label-lg text. The active state is indicated by a primary-colored vertical pill on the far left.
- **Status Indicators**: A 12px circular dot. 
    - *Active*: Vivid Green (#10B981) with a soft outer pulse animation.
    - *Inactive*: Slate Gray (#64748B).
- **Buttons**: All buttons have high contrast. The "Primary Action" button uses the Primary Color with dark text; "Secondary" uses a ghost style with a white outline.
- **Input Fields**: Darker than the surface (#0F172A) with a 1px border. Focus state changes the border to Primary Blue.
- **Progress Bars**: Used for "Now Playing" or "Recording" status. Thin (4px) height with the primary color for the fill and a low-opacity white for the track.