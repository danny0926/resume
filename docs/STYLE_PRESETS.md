# Style Presets

Six visual themes for hand-drawn slide decks. Each preset defines a `style` JSON object to include at the deck's top level, plus design guidance for that theme.

Pick the preset that matches the content's mood. If unsure, default to **Clean Sketch**.

---

## 1. Clean Sketch (Default)

Minimal, professional, lots of whitespace. Thin lines, gentle decorations.

**Best for:** formal reports, paper reviews, corporate presentations

```json
"style": {
  "bg": "#fffdf7",
  "text": "#1a1a2e",
  "text_muted": "#495057",
  "roughness": 1.5,
  "stroke_width": 2
}
```

**Decoration guidance:**
- Use thin single-line frames (`strokeWidth: 1.5-2`)
- Prefer corner accents over full borders
- Subtle underlines via `annotateElement`
- Max 2 rough.js shapes per slide
- Whitespace > 40% of each slide

---

## 2. Bold Marker

High contrast, thick strokes, filled shapes. Energetic and attention-grabbing.

**Best for:** keynotes, pitch decks, conference talks

```json
"style": {
  "bg": "#fffdf7",
  "text": "#1a1a2e",
  "text_muted": "#495057",
  "roughness": 2.5,
  "stroke_width": 3.5
}
```

**Decoration guidance:**
- Thick borders (`strokeWidth: 3-4`)
- Use filled rectangles with `fillStyle: 'hachure'` or `'solid'` + accent-light
- Bold `annotateElement` highlights (`strokeWidth: 4`)
- Double borders for emphasis
- 3-5 rough.js shapes per slide — more is more

---

## 3. Notebook

Grid-dot backgrounds, sticky-note color blocks, annotation-heavy. Casual study feel.

**Best for:** reading notes, study materials, tutorials, brainstorming

```json
"style": {
  "bg": "#f8f9fa",
  "text": "#212529",
  "text_muted": "#6c757d",
  "roughness": 2.0,
  "stroke_width": 2
}
```

**Decoration guidance:**
- Add grid dots in `shapes_js`: `for (let x=100;x<1850;x+=60) for (let y=100;y<1000;y+=60) drawCircle(x,y,3,{fill:'#dee2e6',stroke:'#dee2e6',roughness:0.3});`
- Use colored sticky-note blocks: `background: #fff3bf` (yellow), `#d3f9d8` (green), `#d0ebff` (blue)
- Heavy use of `annotateElement` (underline, highlight, circle)
- Handwritten-style annotations with `font-family: var(--font-annotation)`
- Informal, packed layouts — less whitespace than Clean Sketch

---

## 4. Blackboard

Dark background, light text, chalk-like strokes. Dramatic and focused.

**Best for:** tech talks, live demos, evening events, developer audiences

```json
"style": {
  "bg": "#1a1a2e",
  "text": "#e9ecef",
  "text_muted": "#adb5bd",
  "roughness": 3.0,
  "stroke_width": 2.5
}
```

**Accent color overrides for dark mode** — use brighter variants in slide HTML:
- Blue: `#74c0fc` (light: `#1c3d5a`)
- Green: `#69db7c` (light: `#1e3a21`)
- Orange: `#ff922b` (light: `#3d2810`)
- Purple: `#b197fc` (light: `#2d2150`)

**Decoration guidance:**
- High roughness (3.0+) for chalk feel
- Use lighter stroke colors: `stroke: '#adb5bd'` or `stroke: '#74c0fc'`
- Subtle glow effect via CSS: `text-shadow: 0 0 20px rgba(116,192,252,0.3)`
- Avoid filled shapes with dark fills — use `fill: 'transparent'`
- `annotateElement` colors should use bright variants: `color: '#74c0fc'`

---

## 5. Blueprint

Blue monochrome, technical grid lines, engineering-drawing feel.

**Best for:** architecture diagrams, system design, engineering proposals

```json
"style": {
  "bg": "#eef4fc",
  "text": "#1864ab",
  "text_muted": "#4dabf7",
  "roughness": 1.0,
  "stroke_width": 1.5
}
```

**Decoration guidance:**
- Low roughness (1.0) for precision feel
- All strokes in blue tones: `stroke: '#1864ab'`
- Add grid lines: `for (let x=80;x<1860;x+=80) drawLine(x,80,x,1000,{stroke:'#c5ddf5',strokeWidth:0.5,roughness:0.3});` (and same for horizontal)
- Technical labels with `font-family: monospace`
- Thin connection lines between elements
- Use `dashed` stroke style for secondary lines

---

## 6. Watercolor

Soft pastels, low-opacity filled shapes, gentle and artistic.

**Best for:** brand presentations, cultural topics, creative proposals, storytelling

```json
"style": {
  "bg": "#fdf8f0",
  "text": "#495057",
  "text_muted": "#868e96",
  "roughness": 2.0,
  "stroke_width": 1.5
}
```

**Accent color overrides** — use softer pastel variants in slide HTML:
- Rose: `#e599a3` (light: `#fce4ec`)
- Sage: `#8fbc8f` (light: `#e8f5e9`)
- Lavender: `#b39ddb` (light: `#ede7f6`)
- Sand: `#d4a574` (light: `#fff8e1`)

**Decoration guidance:**
- Filled shapes with low opacity: `fill: 'rgba(229,153,163,0.2)', fillStyle: 'solid'`
- Soft borders: `strokeWidth: 1-1.5`
- Large ellipses and organic shapes instead of rectangles
- Use `drawEllipse` more than `drawRect`
- Gentle `annotateElement` highlights with pastel colors
- Rounded CSS corners: `border-radius: 24px` on content blocks
