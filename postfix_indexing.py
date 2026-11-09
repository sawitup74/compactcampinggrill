# Indexing post-process (added 2026-11-09). Run after build: python3 postfix_indexing.py
# 1) 404.html: noindex, no canonical (it is served for every missing URL)
# 2) "Moved" stubs: keep canonical + instant redirect, drop noindex (mixed signal)
# 3) sitemap.xml: per-URL lastmod from the page's last git commit date
import re, os, subprocess, datetime
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8").write(s)
if os.path.exists("404.html"):
    s = rd("404.html")
    s = re.sub(r'<link rel="canonical" href="[^"]*">', "", s)
    if 'name="robots"' not in s:
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><meta name="robots" content="noindex">', 1)
    wr("404.html", s)
for f in os.listdir("."):
    if f.endswith(".html"):
        s = rd(f)
        if "<title>Moved</title>" in s and 'http-equiv="refresh"' in s and 'content="noindex"' in s:
            wr(f, s.replace('<meta name="robots" content="noindex">', ""))
if os.path.exists("sitemap.xml"):
    today = datetime.date.today().isoformat()
    def lm(m):
        loc = m.group(1)
        path = re.sub(r"^https?://[^/]+/", "", loc) or "index.html"
        if not path.endswith(".html"): path = path.rstrip("/") + "/index.html" if path else "index.html"
        try:
            d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], capture_output=True, text=True).stdout.strip()
        except Exception:
            d = ""
        return "<url><loc>%s</loc><lastmod>%s</lastmod></url>" % (loc, d or today)
    wr("sitemap.xml", re.sub(r"<url><loc>([^<]+)</loc><lastmod>[^<]*</lastmod></url>", lm, rd("sitemap.xml")))
