#!/usr/bin/env python3
"""
Build script for kaenoodle.au

Takes the shared shell in src/base.html, drops each content fragment from
src/pages/ into it, and writes finished HTML files to the repo root where
Azure Static Web Apps will serve them.

The point of this file is that the navigation, the <head>, and the footer
exist in exactly one place. Add a page to the PAGES list below and it
appears in the nav on all seven pages automatically.

Run it with:  python build.py
"""

from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

# ---------------------------------------------------------------------------
# Every page on the site. Order here is the order in the navigation.
#
#   slug        the filename without .html, and the URL
#   label       what the nav link says
#   title       the browser tab and search result heading
#   colourway   the CSS class that sets this page's accent colour
#   swatch      the hex used for the nav chip, so it matches the page
#   description the meta description search engines show
# ---------------------------------------------------------------------------
PAGES = [
    {
        "slug": "index",
        "label": "Home",
        "title": "Kae — foam, fur and code",
        "colourway": "cw-home",
        "swatch": "#FF3D8B",
        "description": "Fursuit maker, artist and computer science student in Perth, Western Australia.",
    },
    {
        "slug": "projects",
        "label": "Projects",
        "title": "Projects — Kae",
        "colourway": "cw-projects",
        "swatch": "#C6FF3D",
        "description": "Software I have built for university, for fun, or because something needed fixing.",
    },
    {
        "slug": "fursuits",
        "label": "Fursuits",
        "title": "Fursuits — Kae",
        "colourway": "cw-fursuits",
        "swatch": "#29D9E8",
        "description": "Fursuit builds and build logs, from foam base through to finished head.",
    },
    {
        "slug": "art",
        "label": "Art",
        "title": "Art — Kae",
        "colourway": "cw-art",
        "swatch": "#FF8A3D",
        "description": "Digital and traditional artwork, reference sheets and badges.",
    },
    {
        "slug": "about",
        "label": "About",
        "title": "About — Kae",
        "colourway": "cw-about",
        "swatch": "#A67BFF",
        "description": "Who I am, what I study, and how the making and the code fit together.",
    },
    {
        "slug": "commissions",
        "label": "Commissions",
        "title": "Commissions — Kae",
        "colourway": "cw-commissions",
        "swatch": "#FFD23D",
        "description": "Commission tiers, pricing, current availability and how the process works.",
    },
    {
        "slug": "contact",
        "label": "Contact",
        "title": "Contact — Kae",
        "colourway": "cw-contact",
        "swatch": "#FFF4E6",
        "description": "Email and social links for commission enquiries and everything else.",
    },
]


def url_for(slug):
    """Home lives at / rather than /index, which is tidier in the address bar."""
    return "/" if slug == "index" else f"/{slug}"


def build_nav(current_slug):
    """
    Return the <li> rows for the navigation, marking the current page.

    aria-current="page" is the accessible way to say 'you are here'. Screen
    readers announce it, and the stylesheet also uses it to draw the active
    state, so there is only one source of truth for which link is active.
    """
    rows = []
    for page in PAGES:
        is_current = page["slug"] == current_slug
        current_attr = ' aria-current="page"' if is_current else ""
        rows.append(
            f'        <li><a class="chip" href="{url_for(page["slug"])}"'
            f' style="--swatch:{page["swatch"]}"{current_attr}>'
            f'<i></i>{page["label"]}</a></li>'
        )
    return "\n".join(rows)


def build_page(page, shell):
    """Fill the shell with one page's content and write it to the repo root."""
    fragment = (SRC / "pages" / f"{page['slug']}.html").read_text(encoding="utf-8")

    html = shell
    for placeholder, value in {
        "{{title}}": page["title"],
        "{{description}}": page["description"],
        "{{colourway_class}}": page["colourway"],
        "{{nav}}": build_nav(page["slug"]),
        "{{content}}": fragment,
    }.items():
        html = html.replace(placeholder, value)

    out = ROOT / f"{page['slug']}.html"
    out.write_text(html, encoding="utf-8")
    return out


def main():
    shell = (SRC / "base.html").read_text(encoding="utf-8")
    for page in PAGES:
        out = build_page(page, shell)
        print(f"  wrote {out.name}")
    print(f"\nBuilt {len(PAGES)} pages.")


if __name__ == "__main__":
    main()
