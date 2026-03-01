"""
render_slides.py — Render JSON slide deck to PNG images using Jinja2 + Playwright.

Usage:
    python render_slides.py --deck deck.json --outdir slides_tmp/ [--mode full|bg_only|both]

Each slide in the JSON deck provides its own HTML/CSS/JS content, which gets
injected into base.html.j2 via dynamic.html.j2. This allows AI-generated
layouts with infinite variation instead of fixed templates.

The deck JSON can include a top-level "style" object to set visual theme
variables (bg, text, roughness, stroke_width, etc.) that apply to all slides.

Modes:
    full    — Render complete slides (default, backwards-compatible)
    bg_only — Render decorations only (text/images made transparent via ghost CSS)
    both    — Render both full and bg_only PNGs per slide

Output: JSON manifest to stdout with { "rendered": [...] }
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

# Accent color rotation (6 colors)
ACCENT_COLORS = [
    {"accent": "#1971c2", "accent_light": "#d0ebff", "accent_dark": "#1864ab"},  # blue
    {"accent": "#2f9e44", "accent_light": "#d3f9d8", "accent_dark": "#2b8a3e"},  # green
    {"accent": "#e8590c", "accent_light": "#ffe8cc", "accent_dark": "#d9480f"},  # orange
    {"accent": "#7048e8", "accent_light": "#e5dbff", "accent_dark": "#6741d9"},  # purple
    {"accent": "#c92a2a", "accent_light": "#ffe3e3", "accent_dark": "#b02525"},  # red
    {"accent": "#0c8599", "accent_light": "#c3fae8", "accent_dark": "#0b7285"},  # cyan
]

# Ghost CSS: makes all #content text/images transparent while keeping
# rough.js canvas decorations visible. Used in bg_only mode so that
# annotations_js targets still exist at correct positions.
GHOST_CSS = """
#content, #content * {
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    border-color: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
}
#content img, #content svg.mermaid-svg, #content canvas {
    opacity: 0 !important;
}
"""

TEMPLATES_DIR = Path(__file__).parent / "templates"


def build_jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=False,
    )


def get_accent(index: int) -> dict:
    return ACCENT_COLORS[index % len(ACCENT_COLORS)]


async def _render_one(page_factory, template, slide: dict, style: dict,
                      index: int, outdir: Path, suffix: str,
                      extra_css: str = "") -> dict:
    """Render a single slide variant (full or bg_only)."""
    slide_id = slide.get("id", index + 1)
    out_path = outdir / f"slide_{slide_id:02d}{suffix}.png"

    accent = get_accent(slide.get("accent_index", index))

    has_mermaid = "mermaid" in slide.get("html", "")
    has_chart = "Chart(" in slide.get("shapes_js", "") or "new Chart" in slide.get("shapes_js", "")

    context_vars = {**style, **accent}

    slide_css = slide.get("css", "")
    if extra_css:
        slide_css = extra_css + "\n" + slide_css

    page_html = template.render(
        html=slide.get("html", ""),
        css=slide_css,
        shapes_js=slide.get("shapes_js", ""),
        annotations_js=slide.get("annotations_js", ""),
        **context_vars,
    )

    page = await page_factory()
    await page.set_content(page_html, wait_until="networkidle")
    wait_ms = 1500 if (has_mermaid or has_chart) else 800
    await page.wait_for_timeout(wait_ms)
    await page.screenshot(path=str(out_path), type="png")
    await page.close()

    print(f"  Rendered slide {slide_id} -> {out_path.name}", file=sys.stderr)
    return {"id": slide_id, "path": str(out_path)}


async def render_deck(deck: dict, outdir: Path, mode: str = "full") -> dict:
    from playwright.async_api import async_playwright

    outdir.mkdir(parents=True, exist_ok=True)
    env = build_jinja_env()
    template = env.get_template("dynamic.html.j2")

    style = deck.get("style", {})
    rendered = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1,
        )
        page_factory = context.new_page

        slides = deck.get("slides", [])
        for i, slide in enumerate(slides):
            slide_id = slide.get("id", i + 1)
            render_mode = slide.get("render_mode", "dual")
            is_image_only = render_mode == "image_only"

            do_full = mode in ("full", "both")
            do_bg = mode in ("bg_only", "both") and not is_image_only

            entry = {"id": slide_id}

            if do_full:
                info = await _render_one(
                    page_factory, template, slide, style, i, outdir, "")
                entry["path"] = info["path"]

            if do_bg:
                info = await _render_one(
                    page_factory, template, slide, style, i, outdir, "_bg",
                    extra_css=GHOST_CSS)
                entry["bg_path"] = info["path"]

            # image_only slides in bg_only-only mode still need a full render
            if mode == "bg_only" and is_image_only:
                info = await _render_one(
                    page_factory, template, slide, style, i, outdir, "")
                entry["path"] = info["path"]

            rendered.append(entry)

        await browser.close()

    return {"rendered": rendered}


def main():
    parser = argparse.ArgumentParser(description="Render slide deck JSON to PNG images")
    parser.add_argument("--deck", required=True, help="Path to JSON deck file")
    parser.add_argument("--outdir", required=True, help="Output directory for PNGs")
    parser.add_argument(
        "--mode", choices=["full", "bg_only", "both"], default="full",
        help="Render mode: full (default), bg_only (decorations only), both",
    )
    args = parser.parse_args()

    deck_path = Path(args.deck)
    if not deck_path.exists():
        print(f"ERROR: Deck file not found: {deck_path}", file=sys.stderr)
        sys.exit(1)

    with open(deck_path, "r", encoding="utf-8") as f:
        deck = json.load(f)

    outdir = Path(args.outdir)
    manifest = asyncio.run(render_deck(deck, outdir, mode=args.mode))

    # Output manifest to stdout
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
