"""Render cv.html to assets/CV.pdf with headless Chromium (used by .github/workflows/cv-pdf.yml)."""
import pathlib
import sys

from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parent.parent
src = root / "cv.html"
out = root / "assets" / "CV.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    # Skip analytics so PDF builds are not counted as page views
    page.route("**/*googletagmanager.com/**", lambda route: route.abort())
    page.goto(src.as_uri(), wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    page.emulate_media(media="print")
    page.pdf(
        path=str(out),
        format="A4",
        print_background=True,
        prefer_css_page_size=True,
        display_header_footer=True,
        header_template="<span></span>",
        footer_template=(
            '<div style="width:100%;font-size:7pt;font-family:monospace;color:#999;'
            'text-align:center;">Kyungwon Kim · Curriculum Vitae · '
            '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
        ),
    )
    browser.close()

print(f"Wrote {out} ({out.stat().st_size} bytes)", file=sys.stderr)
