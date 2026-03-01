# Design System Reference

Detailed reference for layout patterns, decorations, annotations, and data visualization components. Used by the AI when composing per-slide HTML/CSS/JS.

---

## Canvas & Safe Area

```
┌─────────────────────────────────────────┐
│ 1920 × 1080                             │
│  ┌─────────────────────────────────────┐ │
│  │ #content (80px padding all sides)   │ │
│  │ 1760 × 920 usable area             │ │
│  │                                     │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Fonts (Pre-loaded via CDN)

| Variable | Font | Use For | Size Range |
|----------|------|---------|------------|
| `var(--font-heading)` | Caveat + Noto Sans TC | Headings, titles | 56-96px |
| `var(--font-body)` | Patrick Hand + Noto Sans TC | Body text, bullets | 28-38px |
| `var(--font-annotation)` | Kalam + Noto Sans TC | Captions, notes | 22-28px |

## Colors

**CSS Variables** (set automatically per slide by accent_index):

| Variable | Purpose |
|----------|---------|
| `var(--accent)` | Primary accent color |
| `var(--accent-light)` | Light background tint |
| `var(--accent-dark)` | Darker accent variant |
| `var(--bg)` | Page background (`#fffdf7` warm white) |
| `var(--text)` | Main text (`#1a1a2e`) |
| `var(--text-muted)` | Secondary text (`#495057`) |

**Accent Palette** (rotates by slide index):

| Index | Color | Hex | Light |
|-------|-------|-----|-------|
| 0 | Blue | `#1971c2` | `#d0ebff` |
| 1 | Green | `#2f9e44` | `#d3f9d8` |
| 2 | Orange | `#e8590c` | `#ffe8cc` |
| 3 | Purple | `#7048e8` | `#e5dbff` |
| 4 | Red | `#c92a2a` | `#ffe3e3` |
| 5 | Cyan | `#0c8599` | `#c3fae8` |

## Base CSS (Already Applied)

- `h1`: 80px, `h2`: 56px, `h3`: 42px (all `--font-heading`)
- `p, li, span`: 32px, `--font-body`
- `ul li`: custom bullet with accent color, 34px, 16px margin-bottom, 40px left padding
- `.accent-text`: colored text, `.accent-bg`: light tint background
- `.annotation`: Kalam font, muted color

---

## rough.js Decoration Cookbook

Available helper functions (called in `shapes_js`). All helpers respect the deck-level `STYLE` object (roughness, strokeWidth, accent colors).

### Functions

```javascript
drawRect(x, y, width, height, opts)    // Hand-drawn rectangle
drawEllipse(cx, cy, width, height, opts) // Hand-drawn ellipse
drawLine(x1, y1, x2, y2, opts)         // Hand-drawn line
drawCircle(cx, cy, diameter, opts)      // Hand-drawn circle
```

**Common options**: `{ stroke, strokeWidth, roughness, fill, fillStyle, fillWeight }`

### Decoration Patterns

**Page border frame:**
```javascript
drawRect(30, 30, 1860, 1020, { strokeWidth: 2, roughness: 2.5 });
```

**Double border:**
```javascript
drawRect(20, 20, 1880, 1040, { strokeWidth: 1.5, roughness: 2 });
drawRect(40, 40, 1840, 1000, { strokeWidth: 1.5, roughness: 2 });
```

**Corner accents (top-left + bottom-right):**
```javascript
drawLine(30, 30, 200, 30, { strokeWidth: 3 });
drawLine(30, 30, 30, 200, { strokeWidth: 3 });
drawLine(1890, 1050, 1720, 1050, { strokeWidth: 3 });
drawLine(1890, 1050, 1890, 880, { strokeWidth: 3 });
```

**Horizontal divider line:**
```javascript
drawLine(200, 540, 1720, 540, { strokeWidth: 2, roughness: 2 });
```

**Underline beneath heading (at y ~ heading bottom):**
```javascript
drawLine(80, 180, 800, 180, { strokeWidth: 3, roughness: 1.5 });
```

**Accent circle around an element:**
```javascript
drawCircle(960, 400, 300, { strokeWidth: 2.5, roughness: 2 });
```

**Filled accent rectangle (highlight box):**
```javascript
drawRect(100, 300, 500, 200, {
  fill: 'var(--accent-light)', fillStyle: 'solid',
  strokeWidth: 2, roughness: 1.5
});
```

**Wavy separator:**
```javascript
for (let x = 200; x < 1700; x += 60) {
  drawLine(x, 540 + (x % 120 === 0 ? -8 : 8), x + 60, 540 + ((x+60) % 120 === 0 ? -8 : 8), { strokeWidth: 2 });
}
```

**Arrow (hand-drawn):**
```javascript
drawLine(400, 500, 800, 500, { strokeWidth: 2.5 });
drawLine(780, 485, 800, 500, { strokeWidth: 2.5 });
drawLine(780, 515, 800, 500, { strokeWidth: 2.5 });
```

**Background grid dots:**
```javascript
for (let x = 100; x < 1850; x += 80) {
  for (let y = 100; y < 1000; y += 80) {
    drawCircle(x, y, 3, { fill: '#e9ecef', stroke: '#e9ecef', roughness: 0.5 });
  }
}
```

---

## rough-notation Annotation Cookbook

Available via `annotateElement(id, opts)` in `annotations_js`. The element must have a matching `id` attribute in the HTML.

### Annotation Types

```javascript
annotateElement('title', { type: 'underline', strokeWidth: 3 });
annotateElement('keyword', { type: 'highlight', color: 'var(--accent-light)' });
annotateElement('important', { type: 'box', strokeWidth: 2 });
annotateElement('stat', { type: 'circle', strokeWidth: 2, padding: 10 });
annotateElement('old', { type: 'strike-through', strokeWidth: 2 });
annotateElement('callout', { type: 'bracket', brackets: ['left', 'right'], strokeWidth: 2 });
```

**Available types**: `underline`, `highlight`, `box`, `circle`, `strike-through`, `crossed-off`, `bracket`

---

## Layout Patterns Library

Use these CSS patterns as building blocks. Mix and combine freely — don't use the same layout twice in a row.

### Centered Hero

```html
<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center;">
  <h1 id="title" style="font-size:96px; color:var(--accent);">Title Here</h1>
  <p style="font-size:36px; color:var(--text-muted); margin-top:24px;">Subtitle here</p>
</div>
```

### Title + Bullet List

```html
<h1 style="font-size:72px; color:var(--accent); margin-bottom:40px;">Heading</h1>
<ul>
  <li>Point one with detail</li>
  <li>Point two with detail</li>
  <li>Point three with detail</li>
</ul>
```

### Two-Column Split

```html
<h1 style="font-size:64px; color:var(--accent); margin-bottom:40px; text-align:center;">Heading</h1>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:60px; height:calc(100% - 120px);">
  <div>
    <h2 style="font-size:44px; color:var(--accent); margin-bottom:20px;">Left Title</h2>
    <ul><li>Item A</li><li>Item B</li></ul>
  </div>
  <div>
    <h2 style="font-size:44px; color:var(--accent); margin-bottom:20px;">Right Title</h2>
    <ul><li>Item C</li><li>Item D</li></ul>
  </div>
</div>
```

### Big Number / Statistic

```html
<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center;">
  <span id="big-num" style="font-family:var(--font-heading); font-size:160px; font-weight:900; color:var(--accent);">42%</span>
  <p style="font-size:40px; margin-top:16px;">of developers prefer hand-drawn slides</p>
  <p class="annotation" style="font-size:24px; margin-top:24px;">Source: Made-up Survey 2025</p>
</div>
```

### Quote Block

```html
<div style="display:flex; flex-direction:column; justify-content:center; height:100%; padding:0 120px;">
  <p style="font-size:48px; font-style:italic; line-height:1.6; color:var(--text);">
    &ldquo;<span id="quote-text">The best way to predict the future is to invent it.</span>&rdquo;
  </p>
  <p style="font-size:32px; color:var(--accent); margin-top:32px; text-align:right;">— Alan Kay</p>
</div>
```

### Icon/Emoji Grid (3-4 columns)

```html
<h1 style="font-size:64px; color:var(--accent); text-align:center; margin-bottom:40px;">Features</h1>
<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:40px; text-align:center;">
  <div>
    <div style="font-size:64px; margin-bottom:12px;">&#x1F680;</div>
    <h3 style="font-size:36px;">Fast</h3>
    <p style="font-size:26px; color:var(--text-muted);">Lightning speed</p>
  </div>
  <div>
    <div style="font-size:64px; margin-bottom:12px;">&#x1F3A8;</div>
    <h3 style="font-size:36px;">Beautiful</h3>
    <p style="font-size:26px; color:var(--text-muted);">Hand-drawn style</p>
  </div>
  <div>
    <div style="font-size:64px; margin-bottom:12px;">&#x1F4E6;</div>
    <h3 style="font-size:36px;">Modular</h3>
    <p style="font-size:26px; color:var(--text-muted);">Component based</p>
  </div>
</div>
```

### Timeline (Horizontal)

```html
<h1 style="font-size:64px; color:var(--accent); text-align:center; margin-bottom:60px;">Timeline</h1>
<div style="display:flex; justify-content:space-between; align-items:flex-start; padding:0 40px; margin-top:80px;">
  <div style="text-align:center; flex:1;">
    <div style="font-family:var(--font-heading); font-size:48px; color:var(--accent); font-weight:700;">2020</div>
    <p style="font-size:28px; margin-top:24px;">Founded the company</p>
  </div>
  <div style="text-align:center; flex:1;">
    <div style="font-family:var(--font-heading); font-size:48px; color:var(--accent); font-weight:700;">2022</div>
    <p style="font-size:28px; margin-top:24px;">Series A funding</p>
  </div>
  <div style="text-align:center; flex:1;">
    <div style="font-family:var(--font-heading); font-size:48px; color:var(--accent); font-weight:700;">2024</div>
    <p style="font-size:28px; margin-top:24px;">Global expansion</p>
  </div>
</div>
```
*Pair with `shapes_js`: `drawLine(200, 420, 1720, 420, {strokeWidth:3});` and circles at each year position.*

### Process Flow (Steps)

```html
<h1 style="font-size:64px; color:var(--accent); text-align:center; margin-bottom:40px;">Process</h1>
<div style="display:flex; justify-content:space-around; align-items:center; flex:1;">
  <div style="text-align:center; width:250px;">
    <div style="font-family:var(--font-heading); font-size:64px; color:var(--accent);">1</div>
    <h3 style="font-size:32px; margin-top:8px;">Research</h3>
    <p style="font-size:24px; color:var(--text-muted);">Gather data</p>
  </div>
  <div style="text-align:center; width:250px;">
    <div style="font-family:var(--font-heading); font-size:64px; color:var(--accent);">2</div>
    <h3 style="font-size:32px; margin-top:8px;">Design</h3>
    <p style="font-size:24px; color:var(--text-muted);">Create layout</p>
  </div>
  <div style="text-align:center; width:250px;">
    <div style="font-family:var(--font-heading); font-size:64px; color:var(--accent);">3</div>
    <h3 style="font-size:32px; margin-top:8px;">Build</h3>
    <p style="font-size:24px; color:var(--text-muted);">Implement</p>
  </div>
</div>
```
*Pair with `shapes_js`: arrows between step boxes.*

### Full-Bleed Statement

```html
<div style="display:flex; justify-content:center; align-items:center; height:100%; padding:0 160px;">
  <h1 id="statement" style="font-size:80px; text-align:center; line-height:1.3;">
    The key takeaway goes here in <span id="highlight" style="color:var(--accent);">bold emphasis</span>
  </h1>
</div>
```

### Section Break

```html
<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%;">
  <span class="annotation" style="font-size:120px; color:var(--accent-light); font-weight:900;">01</span>
  <h1 style="font-size:72px; margin-top:16px;">Section Title</h1>
  <p style="font-size:30px; color:var(--text-muted); margin-top:12px;">What this section covers</p>
</div>
```
*Pair with `shapes_js`: flanking horizontal lines.*

### Closing / Thank You

```html
<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; text-align:center;">
  <h1 style="font-size:88px; color:var(--accent);">Thank You!</h1>
  <p style="font-size:36px; margin-top:32px; color:var(--text-muted);">Questions & Discussion</p>
  <div style="margin-top:48px;">
    <p class="annotation" style="font-size:26px;">email@example.com</p>
    <p class="annotation" style="font-size:26px;">github.com/username</p>
  </div>
</div>
```

---

## Data Visualization Components

### Mermaid.js Diagrams

Embed directly in the `html` field. Mermaid is pre-loaded in `base.html.j2` with hand-drawn theme.

```html
<h1 style="font-size:64px; color:var(--accent); text-align:center; margin-bottom:24px;">Architecture</h1>
<div style="display:flex; justify-content:center; align-items:center; flex:1;">
  <pre class="mermaid" style="width:100%;">
graph LR
  A[Client] --> B[API Gateway]
  B --> C[Service]
  C --> D[Database]
  </pre>
</div>
```

**Mermaid CSS** (add to `css` field):
```css
.mermaid svg { width: 100% !important; min-width: 1400px; max-width: 1700px; max-height: 780px; height: auto !important; }
```

Supported: `graph` (flowchart), `sequenceDiagram`, `stateDiagram`, `gantt`, `pie`, `classDiagram`, `erDiagram`, etc.

### Chart.js Charts

Embed a `<canvas>` in `html` and initialize in `shapes_js`. Chart.js is pre-loaded.

**HTML:**
```html
<h1 style="font-size:64px; color:var(--accent); text-align:center; margin-bottom:16px;">Revenue Growth</h1>
<div style="display:flex; justify-content:center; align-items:center; flex:1; padding:0 80px;">
  <canvas id="myChart"></canvas>
</div>
```

**shapes_js:**
```javascript
const chartColors = ['#1971c2','#2f9e44','#e8590c','#7048e8','#c92a2a','#0c8599'];
const chartColorsAlpha = chartColors.map(c => {
  const r = parseInt(c.slice(1,3),16), g = parseInt(c.slice(3,5),16), b = parseInt(c.slice(5,7),16);
  return `rgba(${r},${g},${b},0.6)`;
});
Chart.defaults.font.family = "'Patrick Hand', 'Noto Sans TC', cursive";
Chart.defaults.font.size = 20;
const ctx = document.getElementById('myChart').getContext('2d');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['2021', '2022', '2023', '2024'],
    datasets: [{ label: 'Revenue ($B)', data: [16.7, 26.9, 27.0, 60.9],
      backgroundColor: chartColorsAlpha.slice(0,4), borderColor: chartColors.slice(0,4), borderWidth: 2 }]
  },
  options: { responsive: true, maintainAspectRatio: true }
});
```

Supported chart types: `bar`, `line`, `pie`, `doughnut`, `radar`, `polarArea`, `scatter`, `bubble`.

---

## Native Element Position Templates

Standard `elements[]` coordinates (in px, 1920×1080 canvas) for each layout type. Use these as starting points when generating dual-layer slides.

### Centered Hero

```json
"elements": [
  { "type": "textbox", "x": 160, "y": 300, "w": 1600, "h": 180,
    "paragraphs": [{ "text": "Title", "font": "heading", "size": 80, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 360, "y": 500, "w": 1200, "h": 80,
    "paragraphs": [{ "text": "Subtitle text", "font": "body", "size": 36, "align": "center", "color": "var(--text-muted)" }] }
]
```

### Title + Bullet List

```json
"elements": [
  { "type": "textbox", "x": 80, "y": 60, "w": 1760, "h": 120,
    "paragraphs": [{ "text": "Heading", "font": "heading", "size": 64, "bold": true, "color": "var(--accent)" }] },
  { "type": "textbox", "x": 80, "y": 220, "w": 1760, "h": 700,
    "paragraphs": [
      { "text": "First point with detail", "font": "body", "size": 32, "bullet": true },
      { "text": "Second point with detail", "font": "body", "size": 32, "bullet": true },
      { "text": "Third point with detail", "font": "body", "size": 32, "bullet": true }
    ] }
]
```

### Two-Column Split

```json
"elements": [
  { "type": "textbox", "x": 160, "y": 60, "w": 1600, "h": 100,
    "paragraphs": [{ "text": "Heading", "font": "heading", "size": 56, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 80, "y": 200, "w": 860, "h": 700,
    "paragraphs": [
      { "text": "Left Title", "font": "heading", "size": 40, "bold": true, "color": "var(--accent)" },
      { "text": "Left content point A", "font": "body", "size": 28, "bullet": true },
      { "text": "Left content point B", "font": "body", "size": 28, "bullet": true }
    ] },
  { "type": "textbox", "x": 980, "y": 200, "w": 860, "h": 700,
    "paragraphs": [
      { "text": "Right Title", "font": "heading", "size": 40, "bold": true, "color": "var(--accent)" },
      { "text": "Right content point C", "font": "body", "size": 28, "bullet": true },
      { "text": "Right content point D", "font": "body", "size": 28, "bullet": true }
    ] }
]
```

### Big Number / Statistic

```json
"elements": [
  { "type": "textbox", "x": 260, "y": 250, "w": 1400, "h": 250,
    "paragraphs": [{ "text": "42%", "font": "heading", "size": 140, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 310, "y": 520, "w": 1300, "h": 80,
    "paragraphs": [{ "text": "of developers prefer hand-drawn slides", "font": "body", "size": 36, "align": "center" }] },
  { "type": "textbox", "x": 460, "y": 640, "w": 1000, "h": 50,
    "paragraphs": [{ "text": "Source: Survey 2025", "font": "annotation", "size": 22, "align": "center", "color": "var(--text-muted)" }] }
]
```

### Quote Block

```json
"elements": [
  { "type": "textbox", "x": 200, "y": 250, "w": 1520, "h": 300,
    "paragraphs": [{ "text": "\u201cThe best way to predict the future is to invent it.\u201d", "font": "body", "size": 44, "italic": true, "align": "left" }] },
  { "type": "textbox", "x": 200, "y": 580, "w": 1520, "h": 60,
    "paragraphs": [{ "text": "\u2014 Alan Kay", "font": "heading", "size": 30, "align": "right", "color": "var(--accent)" }] }
]
```

### Icon/Emoji Grid (3-column)

```json
"elements": [
  { "type": "textbox", "x": 160, "y": 60, "w": 1600, "h": 100,
    "paragraphs": [{ "text": "Features", "font": "heading", "size": 56, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 80, "y": 240, "w": 560, "h": 600,
    "paragraphs": [
      { "text": "Fast", "font": "heading", "size": 36, "bold": true, "align": "center" },
      { "text": "Lightning speed", "font": "body", "size": 24, "align": "center", "color": "var(--text-muted)" }
    ] },
  { "type": "textbox", "x": 680, "y": 240, "w": 560, "h": 600,
    "paragraphs": [
      { "text": "Beautiful", "font": "heading", "size": 36, "bold": true, "align": "center" },
      { "text": "Hand-drawn style", "font": "body", "size": 24, "align": "center", "color": "var(--text-muted)" }
    ] },
  { "type": "textbox", "x": 1280, "y": 240, "w": 560, "h": 600,
    "paragraphs": [
      { "text": "Modular", "font": "heading", "size": 36, "bold": true, "align": "center" },
      { "text": "Component based", "font": "body", "size": 24, "align": "center", "color": "var(--text-muted)" }
    ] }
]
```

### Section Break

```json
"elements": [
  { "type": "textbox", "x": 460, "y": 200, "w": 1000, "h": 180,
    "paragraphs": [{ "text": "01", "font": "annotation", "size": 100, "align": "center", "color": "var(--accent-light)" }] },
  { "type": "textbox", "x": 260, "y": 400, "w": 1400, "h": 120,
    "paragraphs": [{ "text": "Section Title", "font": "heading", "size": 64, "bold": true, "align": "center" }] },
  { "type": "textbox", "x": 360, "y": 540, "w": 1200, "h": 60,
    "paragraphs": [{ "text": "What this section covers", "font": "body", "size": 28, "align": "center", "color": "var(--text-muted)" }] }
]
```

### Closing / Thank You

```json
"elements": [
  { "type": "textbox", "x": 260, "y": 250, "w": 1400, "h": 150,
    "paragraphs": [{ "text": "Thank You!", "font": "heading", "size": 80, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 360, "y": 430, "w": 1200, "h": 70,
    "paragraphs": [{ "text": "Questions & Discussion", "font": "body", "size": 34, "align": "center", "color": "var(--text-muted)" }] },
  { "type": "textbox", "x": 460, "y": 560, "w": 1000, "h": 120,
    "paragraphs": [
      { "text": "email@example.com", "font": "annotation", "size": 24, "align": "center", "color": "var(--text-muted)" },
      { "text": "github.com/username", "font": "annotation", "size": 24, "align": "center", "color": "var(--text-muted)" }
    ] }
]
```

### Image Placeholder (for user-inserted photos)

```json
{ "type": "image", "x": 960, "y": 200, "w": 800, "h": 500, "src": null, "label": "[Insert photo]" }
```

Common placements:
- **Right half**: `x: 960, y: 200, w: 880, h: 600`
- **Left half**: `x: 80, y: 200, w: 880, h: 600`
- **Center**: `x: 460, y: 200, w: 1000, h: 600`
- **Small inset**: `x: 1300, y: 600, w: 500, h: 350`

### Coordinate Reference

```
Canvas: 1920 × 1080
Safe area: 80px padding → usable 1760 × 920 (x: 80-1840, y: 80-1000)
1 px = 6350 EMU (for gen_pptx.py conversion)
```

---

## Visual-First Layout Patterns

Visual-heavy layouts where imagery or diagrams dominate the slide. Use these when the slide's message is best conveyed through visuals rather than text alone.

### Split Visual (Image + Text)

Image on one side, text on the other. Default: image left, text right. Flip with the variant note below.

**HTML/CSS:**
```html
<div style="display:grid; grid-template-columns:3fr 2fr; gap:40px; height:100%; align-items:center;">
  <div id="image-area" style="display:flex; justify-content:center; align-items:center; height:100%; padding:40px;">
    <!-- Image placeholder area — rough.js frame drawn via shapes_js -->
    <div style="width:100%; height:80%; background:var(--accent-light); border-radius:8px; display:flex; justify-content:center; align-items:center;">
      <p class="annotation" style="font-size:28px; color:var(--text-muted);">[Insert image / diagram]</p>
    </div>
  </div>
  <div style="display:flex; flex-direction:column; justify-content:center; padding-right:40px;">
    <h1 style="font-size:56px; color:var(--accent); margin-bottom:28px;">Heading</h1>
    <ul>
      <li>Key point one with supporting detail</li>
      <li>Key point two with supporting detail</li>
      <li>Key point three with supporting detail</li>
    </ul>
  </div>
</div>
```

**Variant — image on right:** Change `grid-template-columns` to `2fr 3fr` and swap the two child `<div>` elements.

**Elements template:**
```json
"elements": [
  { "type": "image", "x": 80, "y": 120, "w": 1040, "h": 780, "src": null, "label": "[Insert image]" },
  { "type": "textbox", "x": 1160, "y": 200, "w": 680, "h": 100,
    "paragraphs": [{ "text": "Heading", "font": "heading", "size": 52, "bold": true, "color": "var(--accent)" }] },
  { "type": "textbox", "x": 1160, "y": 340, "w": 680, "h": 500,
    "paragraphs": [
      { "text": "Key point one", "font": "body", "size": 30, "bullet": true },
      { "text": "Key point two", "font": "body", "size": 30, "bullet": true },
      { "text": "Key point three", "font": "body", "size": 30, "bullet": true }
    ] }
]
```

**`shapes_js` decorations:** Draw a rough.js frame around the image area to give it a hand-drawn border. Add optional corner accents on the text side.
```javascript
// Frame around image area
drawRect(70, 110, 1060, 800, { strokeWidth: 2.5, roughness: 2.5 });
// Corner accent on text side (top-right)
drawLine(1820, 180, 1820, 300, { strokeWidth: 2.5, roughness: 1.5 });
drawLine(1700, 180, 1820, 180, { strokeWidth: 2.5, roughness: 1.5 });
```

---

### Visual Hero (Centered Illustration)

Large centered rough.js illustration occupying 60-70% of slide area. Small title at top, caption at bottom. Best for concept slides where a single visual conveys the idea.

**HTML/CSS:**
```html
<div style="display:flex; flex-direction:column; height:100%; text-align:center;">
  <h2 style="font-size:48px; color:var(--accent); margin-bottom:16px;">Concept Title</h2>
  <div id="illustration-area" style="flex:1; position:relative; min-height:600px;">
    <!-- rough.js illustration drawn here via shapes_js -->
  </div>
  <p class="annotation" style="font-size:26px; color:var(--text-muted); margin-top:auto; padding-bottom:20px;">
    Caption or explanatory note about the illustration
  </p>
</div>
```

**Elements template:**
```json
"elements": [
  { "type": "textbox", "x": 360, "y": 60, "w": 1200, "h": 80,
    "paragraphs": [{ "text": "Concept Title", "font": "heading", "size": 48, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 260, "y": 920, "w": 1400, "h": 60,
    "paragraphs": [{ "text": "Caption or explanatory note", "font": "annotation", "size": 24, "align": "center", "color": "var(--text-muted)" }] }
]
```

**`shapes_js` decorations:** The concept illustration IS the primary decoration. Use the rough.js helpers to draw the concept (see Rough.js Concept Illustration Cookbook below). No additional frames needed — they would compete with the illustration.

---

### Comparison (Side by Side)

Two columns with rough.js outlined boxes, each containing an icon/image placeholder and label. A visual divider or "vs" element separates them.

**HTML/CSS:**
```html
<h1 style="font-size:56px; color:var(--accent); text-align:center; margin-bottom:40px;">Comparison Title</h1>
<div style="display:grid; grid-template-columns:1fr auto 1fr; gap:20px; height:calc(100% - 140px); align-items:center;">
  <div style="text-align:center; padding:40px;">
    <div style="font-size:64px; margin-bottom:20px;">&#x1F4E6;</div>
    <h2 style="font-size:44px; color:var(--accent); margin-bottom:16px;">Option A</h2>
    <ul style="text-align:left;">
      <li>Advantage one</li>
      <li>Advantage two</li>
      <li>Advantage three</li>
    </ul>
  </div>
  <div style="display:flex; align-items:center; justify-content:center;">
    <span style="font-family:var(--font-heading); font-size:48px; color:var(--text-muted); font-weight:700;">vs</span>
  </div>
  <div style="text-align:center; padding:40px;">
    <div style="font-size:64px; margin-bottom:20px;">&#x1F680;</div>
    <h2 style="font-size:44px; color:var(--accent); margin-bottom:16px;">Option B</h2>
    <ul style="text-align:left;">
      <li>Advantage one</li>
      <li>Advantage two</li>
      <li>Advantage three</li>
    </ul>
  </div>
</div>
```

**Elements template:**
```json
"elements": [
  { "type": "textbox", "x": 260, "y": 60, "w": 1400, "h": 100,
    "paragraphs": [{ "text": "Comparison Title", "font": "heading", "size": 52, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 80, "y": 220, "w": 840, "h": 100,
    "paragraphs": [{ "text": "Option A", "font": "heading", "size": 40, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 80, "y": 340, "w": 840, "h": 500,
    "paragraphs": [
      { "text": "Advantage one", "font": "body", "size": 28, "bullet": true },
      { "text": "Advantage two", "font": "body", "size": 28, "bullet": true },
      { "text": "Advantage three", "font": "body", "size": 28, "bullet": true }
    ] },
  { "type": "textbox", "x": 920, "y": 440, "w": 80, "h": 60,
    "paragraphs": [{ "text": "vs", "font": "heading", "size": 40, "bold": true, "align": "center", "color": "var(--text-muted)" }] },
  { "type": "textbox", "x": 1000, "y": 220, "w": 840, "h": 100,
    "paragraphs": [{ "text": "Option B", "font": "heading", "size": 40, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 1000, "y": 340, "w": 840, "h": 500,
    "paragraphs": [
      { "text": "Advantage one", "font": "body", "size": 28, "bullet": true },
      { "text": "Advantage two", "font": "body", "size": 28, "bullet": true },
      { "text": "Advantage three", "font": "body", "size": 28, "bullet": true }
    ] }
]
```

**`shapes_js` decorations:** Box outlines per column. Optional "vs" divider line between them.
```javascript
// Left column box
drawRect(60, 180, 870, 740, { strokeWidth: 2, roughness: 2.5 });
// Right column box
drawRect(990, 180, 870, 740, { strokeWidth: 2, roughness: 2.5 });
// Vertical "vs" divider line
drawLine(960, 240, 960, 860, { strokeWidth: 1.5, roughness: 2, stroke: 'var(--text-muted)' });
```

---

### Annotated Diagram (Central Diagram + Callout Labels)

A central rough.js diagram (boxes + arrows) with text callout labels positioned around it. Best for architecture, system design, or workflow explanation slides.

**HTML/CSS:**
```html
<h1 style="font-size:52px; color:var(--accent); text-align:center; margin-bottom:20px;">System Overview</h1>
<div style="position:relative; flex:1; height:calc(100% - 100px);">
  <!-- Central diagram drawn via shapes_js -->
  <!-- Callout labels positioned absolutely around the diagram -->
  <div style="position:absolute; top:80px; left:40px; max-width:300px;">
    <p class="annotation" style="font-size:24px; background:var(--accent-light); padding:12px 16px; border-radius:6px;">
      <strong>Label A:</strong> Explanation of this component
    </p>
  </div>
  <div style="position:absolute; top:80px; right:40px; max-width:300px;">
    <p class="annotation" style="font-size:24px; background:var(--accent-light); padding:12px 16px; border-radius:6px;">
      <strong>Label B:</strong> Explanation of this component
    </p>
  </div>
  <div style="position:absolute; bottom:60px; left:40px; max-width:300px;">
    <p class="annotation" style="font-size:24px; background:var(--accent-light); padding:12px 16px; border-radius:6px;">
      <strong>Label C:</strong> Explanation of this component
    </p>
  </div>
  <div style="position:absolute; bottom:60px; right:40px; max-width:300px;">
    <p class="annotation" style="font-size:24px; background:var(--accent-light); padding:12px 16px; border-radius:6px;">
      <strong>Label D:</strong> Explanation of this component
    </p>
  </div>
</div>
```

**Elements template:**
```json
"elements": [
  { "type": "textbox", "x": 360, "y": 40, "w": 1200, "h": 80,
    "paragraphs": [{ "text": "System Overview", "font": "heading", "size": 48, "bold": true, "align": "center", "color": "var(--accent)" }] },
  { "type": "textbox", "x": 80, "y": 180, "w": 340, "h": 120,
    "paragraphs": [
      { "text": "Label A", "font": "heading", "size": 24, "bold": true, "color": "var(--accent)" },
      { "text": "Explanation of component", "font": "annotation", "size": 20, "color": "var(--text-muted)" }
    ] },
  { "type": "textbox", "x": 1500, "y": 180, "w": 340, "h": 120,
    "paragraphs": [
      { "text": "Label B", "font": "heading", "size": 24, "bold": true, "color": "var(--accent)" },
      { "text": "Explanation of component", "font": "annotation", "size": 20, "color": "var(--text-muted)" }
    ] },
  { "type": "textbox", "x": 80, "y": 800, "w": 340, "h": 120,
    "paragraphs": [
      { "text": "Label C", "font": "heading", "size": 24, "bold": true, "color": "var(--accent)" },
      { "text": "Explanation of component", "font": "annotation", "size": 20, "color": "var(--text-muted)" }
    ] },
  { "type": "textbox", "x": 1500, "y": 800, "w": 340, "h": 120,
    "paragraphs": [
      { "text": "Label D", "font": "heading", "size": 24, "bold": true, "color": "var(--accent)" },
      { "text": "Explanation of component", "font": "annotation", "size": 20, "color": "var(--text-muted)" }
    ] }
]
```

**`shapes_js` decorations:** The diagram IS the primary decoration. Draw boxes and arrows in the central area (x: 480-1440, y: 250-750). Add callout lines from diagram components to the surrounding labels.
```javascript
// Central diagram: 3 boxes with connecting arrows
drawRect(580, 300, 280, 140, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
drawRect(820, 550, 280, 140, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
drawRect(1060, 300, 280, 140, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
// Arrow: box1 → box3
drawLine(860, 370, 1060, 370, { strokeWidth: 2 });
drawLine(1040, 355, 1060, 370, { strokeWidth: 2 });
drawLine(1040, 385, 1060, 370, { strokeWidth: 2 });
// Arrow: box1 → box2
drawLine(720, 440, 820, 550, { strokeWidth: 2 });
drawLine(810, 530, 820, 550, { strokeWidth: 2 });
drawLine(830, 535, 820, 550, { strokeWidth: 2 });
// Callout lines from labels to diagram
drawLine(420, 240, 580, 320, { strokeWidth: 1, roughness: 1.5, stroke: 'var(--text-muted)' });
drawLine(1500, 240, 1340, 320, { strokeWidth: 1, roughness: 1.5, stroke: 'var(--text-muted)' });
```

---

## Rough.js Concept Illustration Cookbook

Reusable rough.js illustration patterns using the available helper functions. Use these in `shapes_js` for visual-hero slides or as decorative elements in other layouts.

All patterns use the 1920x1080 canvas coordinate system and are designed to occupy the central illustration area (roughly x: 400-1520, y: 200-850).

| Pattern | Use For |
|---------|---------|
| Funnel | Filtering, pipeline stages |
| Cycle | Iterative processes, feedback loops |
| Layered Stack | Architecture layers, tech stacks |
| Tree/Hierarchy | Org charts, taxonomies |
| Before-After | Transformation, improvement |
| Venn Diagram | Relationships, intersections |
| Scale/Balance | Trade-offs, comparisons |
| Network/Graph | Relationships, connections |
| Growth Arrow | Progress, trends |
| Shield/Lock | Security, protection |

### Funnel

```javascript
// Funnel: 3 stages narrowing from top to bottom
// Stage 1 — wide top (x:560-1360, y:200)
drawLine(560, 200, 1360, 200, { strokeWidth: 2.5, roughness: 2 });
drawLine(560, 200, 700, 420, { strokeWidth: 2.5, roughness: 2 });
drawLine(1360, 200, 1220, 420, { strokeWidth: 2.5, roughness: 2 });
// Stage 2 — mid (x:700-1220, y:420)
drawLine(700, 420, 1220, 420, { strokeWidth: 2, roughness: 2 });
drawLine(700, 420, 820, 620, { strokeWidth: 2.5, roughness: 2 });
drawLine(1220, 420, 1100, 620, { strokeWidth: 2.5, roughness: 2 });
// Stage 3 — narrow bottom (x:820-1100, y:620)
drawLine(820, 620, 1100, 620, { strokeWidth: 2, roughness: 2 });
drawLine(820, 620, 900, 800, { strokeWidth: 2.5, roughness: 2 });
drawLine(1100, 620, 1020, 800, { strokeWidth: 2.5, roughness: 2 });
drawLine(900, 800, 1020, 800, { strokeWidth: 2, roughness: 2 });
// Fill stages with accent tints
drawRect(680, 210, 560, 200, { fill: 'var(--accent-light)', fillStyle: 'solid', stroke: 'none', strokeWidth: 0 });
```

### Cycle

```javascript
// Cycle: 4 nodes in a circular arrangement with curved arrows
var cx = 960, cy = 500, r = 220;
// 4 node circles at compass points
drawCircle(cx, cy - r, 100, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });  // top
drawCircle(cx + r, cy, 100, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });  // right
drawCircle(cx, cy + r, 100, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });  // bottom
drawCircle(cx - r, cy, 100, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });  // left
// Connecting arrows (top→right, right→bottom, bottom→left, left→top)
drawLine(cx + 40, cy - r + 30, cx + r - 40, cy - 30, { strokeWidth: 2 });
drawLine(cx + r - 30, cy + 40, cx + 40, cy + r - 30, { strokeWidth: 2 });
drawLine(cx - 40, cy + r - 30, cx - r + 40, cy + 30, { strokeWidth: 2 });
drawLine(cx - r + 30, cy - 40, cx - 40, cy - r + 30, { strokeWidth: 2 });
// Arrowheads on each connecting line (right end)
drawLine(cx + r - 55, cy - 20, cx + r - 40, cy - 30, { strokeWidth: 2 });
drawLine(cx + r - 30, cy - 20, cx + r - 40, cy - 30, { strokeWidth: 2 });
```

### Layered Stack

```javascript
// Layered Stack: 4 horizontal layers stacked vertically
var stackX = 560, stackW = 800;
var layers = [
  { y: 220, h: 120, label: 'Presentation' },
  { y: 370, h: 120, label: 'Business Logic' },
  { y: 520, h: 120, label: 'Data Access' },
  { y: 670, h: 120, label: 'Infrastructure' }
];
layers.forEach(function(l, i) {
  drawRect(stackX, l.y, stackW, l.h, {
    strokeWidth: 2, roughness: 2,
    fill: i === 0 ? 'var(--accent-light)' : (i === 1 ? '#e9ecef' : (i === 2 ? '#dee2e6' : '#ced4da')),
    fillStyle: 'solid'
  });
});
// Vertical connecting lines between layers
drawLine(960, 340, 960, 370, { strokeWidth: 2, roughness: 1 });
drawLine(960, 490, 960, 520, { strokeWidth: 2, roughness: 1 });
drawLine(960, 640, 960, 670, { strokeWidth: 2, roughness: 1 });
```

### Tree/Hierarchy

```javascript
// Tree: 1 root, 3 children, branching lines
// Root node
drawRect(810, 200, 300, 100, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
// Child nodes
drawRect(380, 480, 260, 100, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
drawRect(830, 480, 260, 100, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
drawRect(1280, 480, 260, 100, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
// Branch lines: root → children
drawLine(960, 300, 510, 480, { strokeWidth: 2, roughness: 1.5 });
drawLine(960, 300, 960, 480, { strokeWidth: 2, roughness: 1.5 });
drawLine(960, 300, 1410, 480, { strokeWidth: 2, roughness: 1.5 });
// Grandchild nodes (2 under middle child)
drawRect(740, 700, 200, 80, { strokeWidth: 1.5, roughness: 2, fill: '#e9ecef', fillStyle: 'solid' });
drawRect(980, 700, 200, 80, { strokeWidth: 1.5, roughness: 2, fill: '#e9ecef', fillStyle: 'solid' });
drawLine(920, 580, 840, 700, { strokeWidth: 1.5, roughness: 1.5 });
drawLine(1000, 580, 1080, 700, { strokeWidth: 1.5, roughness: 1.5 });
```

### Before-After

```javascript
// Before → After: two boxes with a transformation arrow
// "Before" box
drawRect(160, 280, 600, 440, { strokeWidth: 2.5, roughness: 2.5 });
// "After" box
drawRect(1160, 280, 600, 440, { strokeWidth: 2.5, roughness: 2.5, fill: 'var(--accent-light)', fillStyle: 'solid' });
// Transformation arrow in the middle
drawLine(800, 500, 1120, 500, { strokeWidth: 3, roughness: 1.5 });
drawLine(1095, 480, 1120, 500, { strokeWidth: 3 });
drawLine(1095, 520, 1120, 500, { strokeWidth: 3 });
// "X" marks in before box (representing problems)
drawLine(300, 380, 360, 440, { strokeWidth: 2, roughness: 2, stroke: '#c92a2a' });
drawLine(360, 380, 300, 440, { strokeWidth: 2, roughness: 2, stroke: '#c92a2a' });
drawLine(300, 500, 360, 560, { strokeWidth: 2, roughness: 2, stroke: '#c92a2a' });
drawLine(360, 500, 300, 560, { strokeWidth: 2, roughness: 2, stroke: '#c92a2a' });
// Checkmarks in after box (representing solutions)
drawLine(1300, 420, 1330, 450, { strokeWidth: 2.5, roughness: 1, stroke: '#2f9e44' });
drawLine(1330, 450, 1380, 390, { strokeWidth: 2.5, roughness: 1, stroke: '#2f9e44' });
drawLine(1300, 540, 1330, 570, { strokeWidth: 2.5, roughness: 1, stroke: '#2f9e44' });
drawLine(1330, 570, 1380, 510, { strokeWidth: 2.5, roughness: 1, stroke: '#2f9e44' });
```

### Venn Diagram

```javascript
// Venn Diagram: 2 overlapping ellipses
// Left circle
drawEllipse(720, 500, 500, 400, { strokeWidth: 2.5, roughness: 2, fill: 'rgba(25,113,194,0.15)', fillStyle: 'solid' });
// Right circle
drawEllipse(1200, 500, 500, 400, { strokeWidth: 2.5, roughness: 2, fill: 'rgba(47,158,68,0.15)', fillStyle: 'solid' });
// Overlap highlight — small ellipse in intersection area
drawEllipse(960, 500, 180, 300, { strokeWidth: 0, fill: 'var(--accent-light)', fillStyle: 'solid' });
```

### Scale/Balance

```javascript
// Scale: fulcrum triangle + two pans
// Fulcrum triangle
drawLine(960, 700, 880, 800, { strokeWidth: 2.5, roughness: 2 });
drawLine(960, 700, 1040, 800, { strokeWidth: 2.5, roughness: 2 });
drawLine(880, 800, 1040, 800, { strokeWidth: 2.5, roughness: 2 });
// Balance beam (slightly tilted for visual interest)
drawLine(460, 440, 1460, 400, { strokeWidth: 3, roughness: 1.5 });
// Beam to fulcrum
drawLine(960, 420, 960, 700, { strokeWidth: 2, roughness: 1 });
// Left pan
drawRect(360, 300, 280, 140, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
// Right pan
drawRect(1280, 260, 280, 140, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
// Pan suspensions
drawLine(500, 440, 500, 300, { strokeWidth: 1.5, roughness: 1 });
drawLine(1420, 400, 1420, 260, { strokeWidth: 1.5, roughness: 1 });
```

### Network/Graph

```javascript
// Network: 5 nodes with connecting edges
var nodes = [
  { x: 960, y: 300 },   // center-top
  { x: 600, y: 480 },   // left
  { x: 1320, y: 480 },  // right
  { x: 700, y: 720 },   // bottom-left
  { x: 1220, y: 720 }   // bottom-right
];
// Draw edges first (behind nodes)
drawLine(nodes[0].x, nodes[0].y, nodes[1].x, nodes[1].y, { strokeWidth: 1.5, roughness: 2 });
drawLine(nodes[0].x, nodes[0].y, nodes[2].x, nodes[2].y, { strokeWidth: 1.5, roughness: 2 });
drawLine(nodes[1].x, nodes[1].y, nodes[3].x, nodes[3].y, { strokeWidth: 1.5, roughness: 2 });
drawLine(nodes[2].x, nodes[2].y, nodes[4].x, nodes[4].y, { strokeWidth: 1.5, roughness: 2 });
drawLine(nodes[1].x, nodes[1].y, nodes[2].x, nodes[2].y, { strokeWidth: 1.5, roughness: 2 });
drawLine(nodes[3].x, nodes[3].y, nodes[4].x, nodes[4].y, { strokeWidth: 1.5, roughness: 2 });
// Draw nodes on top
nodes.forEach(function(n, i) {
  drawCircle(n.x, n.y, i === 0 ? 90 : 70, {
    strokeWidth: 2, roughness: 2,
    fill: i === 0 ? 'var(--accent-light)' : '#e9ecef', fillStyle: 'solid'
  });
});
```

### Growth Arrow

```javascript
// Growth Arrow: ascending arrow with step increments
// Base line
drawLine(300, 750, 1650, 750, { strokeWidth: 2, roughness: 1.5 });
// Vertical axis
drawLine(300, 750, 300, 200, { strokeWidth: 2, roughness: 1.5 });
// Step bars (ascending)
drawRect(420, 620, 160, 130, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
drawRect(660, 510, 160, 240, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
drawRect(900, 400, 160, 350, { strokeWidth: 2, roughness: 2, fill: 'var(--accent-light)', fillStyle: 'solid' });
drawRect(1140, 300, 160, 450, { strokeWidth: 2, roughness: 2, fill: 'var(--accent)', fillStyle: 'solid' });
// Trend arrow overlaid
drawLine(440, 600, 1280, 260, { strokeWidth: 3, roughness: 1.5, stroke: 'var(--accent)' });
drawLine(1255, 275, 1280, 260, { strokeWidth: 3, stroke: 'var(--accent)' });
drawLine(1265, 295, 1280, 260, { strokeWidth: 3, stroke: 'var(--accent)' });
```

### Shield/Lock

```javascript
// Shield shape: security / protection concept
// Shield outline using lines (pointed bottom)
drawLine(760, 220, 760, 560, { strokeWidth: 2.5, roughness: 2 });
drawLine(1160, 220, 1160, 560, { strokeWidth: 2.5, roughness: 2 });
drawLine(760, 220, 1160, 220, { strokeWidth: 2.5, roughness: 2 });
drawLine(760, 560, 960, 780, { strokeWidth: 2.5, roughness: 2 });
drawLine(1160, 560, 960, 780, { strokeWidth: 2.5, roughness: 2 });
// Shield fill
drawRect(770, 230, 380, 330, { fill: 'var(--accent-light)', fillStyle: 'solid', stroke: 'none', strokeWidth: 0 });
// Lock icon in center of shield
drawRect(910, 380, 100, 80, { strokeWidth: 2, roughness: 1.5, fill: 'var(--accent)', fillStyle: 'solid' });
// Lock shackle (arch)
drawEllipse(960, 370, 80, 70, { strokeWidth: 2.5, roughness: 1.5 });
// Keyhole
drawCircle(960, 410, 16, { fill: '#fffdf7', stroke: '#fffdf7', roughness: 0.5 });
drawLine(960, 418, 960, 440, { strokeWidth: 3, stroke: '#fffdf7', roughness: 0.5 });
```

---

## Decoration Selection Matrix

Maps layout types to recommended rough.js decorations. Use this to quickly choose appropriate `shapes_js` decorations for each slide layout.

| Layout Type | Primary Decoration | Secondary | Avoid |
|------------|-------------------|-----------|-------|
| split-visual | Frame around image area | Corner accents on text side | Full border on both sides |
| visual-hero | Concept illustration IS the decoration | Subtle underline on caption | Additional frames |
| big-number | Circle/ellipse around number | Underline on caption | Rectangles |
| title-bullets | Corner brackets | Bullet accent dots | Full frames |
| icon-grid | Card outlines per item | None needed | Connecting lines |
| comparison | Box outlines per column | "vs" divider line | Decorations inside boxes |
| annotated-diagram | Diagram IS the decoration | Callout lines to labels | Border frames |
| timeline | Timeline line + node circles | None needed | Full border |
| process-flow | Step boxes + connecting arrows | Number circles | Background fills |
| quote | Large quotation marks (drawn) | Subtle underline | Box frames |
| two-column | Vertical divider line | Corner accents | Double borders |
| section-break | Flanking horizontal lines | None needed | Full frames |
| closing | Decorative border frame | Corner accents | Heavy illustrations |
| full-bleed-statement | Underline on key phrase | Corner accents | Full borders |

**Guidelines:**

1. **One primary decoration per slide.** If the layout already contains a visual element (illustration, diagram, image), that IS the decoration — do not add a border frame on top.
2. **Secondary decorations are optional.** Only add them if the slide feels visually sparse after the primary decoration.
3. **"Avoid" items create visual clutter.** They compete with the layout's inherent structure and make the slide feel busy.
4. **Accent color consistency.** All decorations should use `var(--accent)` or `var(--accent-light)` to match the slide's color scheme. Avoid introducing new colors in decorations.
5. **Roughness consistency.** Keep roughness between 1.5-2.5 for decorations. Lower values (0.5-1) for small details like dots; higher values (2.5-3) for large background elements only.
