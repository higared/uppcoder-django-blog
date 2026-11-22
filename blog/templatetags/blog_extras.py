"""Tiny Markdown-ish renderer for post content.

No external dependency on purpose: Uppcoder's pixi env only has
django + gunicorn + psycopg, so `pip install markdown` in
requirements.txt would not be installed (same lesson as whitenoise).

Supports just what the blog needs:
- ImgBed Markdown image:  ![alt](https://...)
- Markdown link:          [text](https://...)
- Blank line = new paragraph, single newline = <br>

Everything else is HTML-escaped, so pasting a raw <script> or
<img> tag from elsewhere cannot run as code.
"""
import html
import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def _inline(text):
    # Escape first, then turn the two Markdown forms back into HTML.
    text = html.escape(text)

    def _img(m):
        alt = m.group(1)
        url = m.group(2)
        return (
            f'<img src="{url}" alt="{alt}" loading="lazy" '
            f'style="max-width:100%;height:auto;border-radius:8px;">'
        )

    def _link(m):
        label = m.group(1)
        url = m.group(2)
        return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'

    text = _IMG_RE.sub(_img, text)
    text = _LINK_RE.sub(_link, text)
    return text


@register.filter(name="render_content")
def render_content(value):
    if not value:
        return ""
    paragraphs = []
    for block in re.split(r"\n\s*\n", str(value).strip()):
        block = block.strip()
        if not block:
            continue
        paragraphs.append(f"<p>{_inline(block).replace(chr(10), '<br>')}</p>")
    return mark_safe("".join(paragraphs))
