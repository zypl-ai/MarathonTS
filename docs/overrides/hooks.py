"""MkDocs hooks: the home page shows README.md, whose links point into docs/ and to files of the repository root
(on the site they are rewritten relative to docs/ and to the repository); a figure page shows its figure (the SVG
written next to the PDF by docs/figures/src/make_figures.py) under its title, with a link to the vector PDF."""
import re
from pathlib import Path

REPO = "https://github.com/zypl-ai/MarathonTS/blob/main/"
README = Path(__file__).resolve().parents[2] / "README.md"
DOCS = README.parent / "docs"


def _home(markdown, page):
    if page.file.src_uri != "index.md":
        return markdown
    text = README.read_text().replace("](docs/", "](").replace('src="docs/', 'src="')
    # links to pages of docs/ stay; links to other files (LICENSE, CHANGELOG.md, code) → the repository
    return re.sub(r"\]\((?!https?://|#)([^)\s]+)\)",
                  lambda m: f"]({m.group(1)})" if (DOCS / m.group(1).split("#")[0]).is_file() else f"]({REPO}{m.group(1)})",
                  text)


FIG = re.compile(r"^figures/(fig\d+_[\w]+)\.md$")


def _figure(markdown, name):
    """The figure under the page title (on a white card, so that it reads in the dark theme too)."""
    if not (DOCS / "figures" / f"{name}.svg").is_file():
        return markdown
    img = (f'![{name}]({name}.svg){{ style="background:#fff;padding:12px;border-radius:6px;max-width:100%" }}\n\n'
           f"[Vector PDF]({name}.pdf)\n\n")
    head, sep, rest = markdown.partition("\n")
    return f"{head}{sep}\n{img}{rest}" if head.startswith("# ") else img + markdown


def on_page_markdown(markdown, page, **kwargs):
    m = FIG.match(page.file.src_uri)
    if m:
        return _figure(markdown, m.group(1))
    return _home(markdown, page)
