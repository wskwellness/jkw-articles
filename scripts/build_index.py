#!/usr/bin/env python3
"""Rebuild the landing page (index.html) from the article folders vNiN/<id>/index.html."""
import html, re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
issues = {}
for f in sorted(root.glob("v*i*/*/index.html")):
    text = f.read_text(encoding="utf-8", errors="ignore")[:200000]
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    title = html.unescape(m.group(1).strip()) if m else f.parent.name
    issue, art = f.parent.parent.name, f.parent.name
    issues.setdefault(issue, []).append((int(art) if art.isdigit() else 0, art, title))

def label(issue):
    m = re.match(r"v(\d+)i(\d+)", issue)
    return f"Volume {m.group(1)}, Number {m.group(2)}" if m else issue

parts = []
for issue in sorted(issues, reverse=True):
    parts.append(f"<h2>{label(issue)}</h2>\n<ul>")
    for _, art, title in sorted(issues[issue], reverse=True):
        doi = f"10.56980/jkw.{issue}.{art}"
        parts.append(
            f'<li><a href="{issue}/{art}/">{html.escape(title)}</a>'
            f'<br><span class="doi"><a href="https://doi.org/{doi}">doi.org/{doi}</a></span></li>'
        )
    parts.append("</ul>")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JKW Articles</title>
<style>
  body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; max-width: 52rem;
         margin: 0 auto; padding: 1.5rem 1rem 3rem; line-height: 1.5; color: #1d2733; background: #fff; }}
  header {{ border-bottom: 3px solid #2780e3; margin-bottom: 1.5rem; }}
  h1 {{ font-size: 1.5rem; margin: 0 0 .25rem; }}
  h2 {{ font-size: 1.15rem; margin-top: 2rem; }}
  ul {{ padding-left: 1.1rem; }} li {{ margin-bottom: .8rem; }}
  a {{ color: #1a5fb4; }} .doi {{ font-size: .85rem; }} .doi a {{ color: #555; }}
</style>
</head>
<body>
<header>
  <h1>Journal of Kinesiology and Wellness</h1>
  <p>HTML versions of published articles. The journal's home and the PDF versions are at
  <a href="https://jkw.wskw.org/index.php/jkw">jkw.wskw.org</a>.</p>
</header>
{chr(10).join(parts)}
</body>
</html>
"""
(root / "index.html").write_text(page, encoding="utf-8")
print(f"index.html: {sum(len(v) for v in issues.values())} articles")
