# -*- coding: utf-8 -*-
"""Bundle the 31 chapter pages into one self-contained HTML reader."""
import io, os, re, json, hashlib, sys

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SRC, "index.html")
HERE = os.path.dirname(os.path.abspath(__file__))

V1 = "Volume 1 — Design Problems"
V2 = "Volume 2 — Design Problems"

CHAPTERS = [
    (0,  "Foreword",                                           "Start Here"),
    (1,  "Join the Community",                                 "Start Here"),
    (2,  "Scale From Zero To Millions Of Users",               "Foundations"),
    (3,  "Back-of-the-envelope Estimation",                    "Foundations"),
    (4,  "A Framework For System Design Interviews",           "Foundations"),
    (5,  "Design A Rate Limiter",                              V1),
    (6,  "Design Consistent Hashing",                          V1),
    (7,  "Design A Key-value Store",                           V1),
    (8,  "Design A Unique ID Generator In Distributed Systems", V1),
    (9,  "Design A URL Shortener",                             V1),
    (10, "Design A Web Crawler",                               V1),
    (11, "Design A Notification System",                       V1),
    (12, "Design A News Feed System",                          V1),
    (13, "Design A Chat System",                               V1),
    (14, "Design A Search Autocomplete System",                V1),
    (15, "Design YouTube",                                     V1),
    (16, "Design Google Drive",                                V1),
    (17, "Proximity Service",                                  V2),
    (18, "Nearby Friends",                                     V2),
    (19, "Google Maps",                                        V2),
    (20, "Distributed Message Queue",                          V2),
    (21, "Metrics Monitoring and Alerting System",             V2),
    (22, "Ad Click Event Aggregation",                         V2),
    (23, "Hotel Reservation System",                           V2),
    (24, "Distributed Email Service",                          V2),
    (25, "S3-like Object Storage",                             V2),
    (26, "Real-time Gaming Leaderboard",                       V2),
    (27, "Payment System",                                     V2),
    (28, "Digital Wallet",                                     V2),
    (29, "Stock Exchange",                                     V2),
    (30, "The Learning Continues",                             "Wrap Up"),
]


def extract_article(s):
    """Return the balanced <article>...</article> region."""
    low = s.lower()
    i = low.find("<article")
    if i == -1:
        return None
    depth, pos = 0, i
    while pos < len(s):
        o = low.find("<article", pos)
        c = low.find("</article", pos)
        if c == -1:
            return None
        if o != -1 and o < c:
            depth += 1
            pos = o + 8
        else:
            depth -= 1
            if depth == 0:
                return s[i:low.find(">", c) + 1]
            pos = c + 9
    return None


def strip_scripts(h):
    return re.sub(r"<script[^>]*>.*?</script>", "", h, flags=re.S | re.I)


# ---------- pass 1: styles + articles ----------
style_index = {}
style_blocks = []
articles = []

for n, t, g in CHAPTERS:
    path = os.path.join(SRC, "%d. %s.html" % (n, t))
    s = io.open(path, encoding="utf-8", errors="replace").read()

    idxs = []
    for css in re.findall(r"<style[^>]*>(.*?)</style>", s, re.S | re.I):
        h = hashlib.md5(css.encode("utf-8", "replace")).hexdigest()
        if h not in style_index:
            style_index[h] = len(style_blocks)
            style_blocks.append(css)
        pos = style_index[h]
        if pos not in idxs:
            idxs.append(pos)

    art = extract_article(s)
    if art is None:
        sys.exit("no <article> found in chapter %d" % n)
    articles.append([n, t, g, strip_scripts(art), idxs])
    print("  ch %-2d  article %7d chars  styles %2d" % (n, len(art), len(idxs)))

# ---------- pass 2: dedupe base64 payloads ----------
DATA_RE = re.compile(r"data:(?:image|font)/[a-zA-Z0-9.+-]+;base64,[A-Za-z0-9+/=]+")
blob_index, blobs = {}, []


def tokenize(html):
    def sub(m):
        uri = m.group(0)
        if uri not in blob_index:
            blob_index[uri] = len(blobs)
            blobs.append(uri)
        return "@@B%d@@" % blob_index[uri]
    return DATA_RE.sub(sub, html)


raw_total = sum(len(a[3]) for a in articles)
for a in articles:
    a[3] = tokenize(a[3])
tok_total = sum(len(a[3]) for a in articles)
blob_total = sum(len(b) for b in blobs)

print("")
print("articles raw       : %7.2f MB" % (raw_total / 1e6))
print("articles tokenized : %7.2f MB" % (tok_total / 1e6))
print("unique blobs       : %d (%.2f MB)" % (len(blobs), blob_total / 1e6))
print("unique styles      : %d (%.2f MB)" % (len(style_blocks),
                                             sum(len(c) for c in style_blocks) / 1e6))


def payload(obj):
    """JSON that is safe to sit inside a <script> element."""
    return (json.dumps(obj, ensure_ascii=False)
            .replace("</", "<\\/")
            .replace("<!--", "<\\u0021--"))


# ---------- shell CSS comes from the reader we already built ----------
# the reader shell lives in docs/ (root index.html is the generated bundle)
shell = io.open(os.path.join(SRC, "docs", "index.html"), encoding="utf-8").read()
shell_css = re.search(r"<style>(.*?)</style>", shell, re.S).group(1)

EXTRA_CSS = """
  /* ---- embedded chapter stage ---- */
  .stage{flex:1;min-height:0;position:relative;background:#fff}
  #doc{height:100%;overflow-y:auto;background:#fff;-webkit-overflow-scrolling:touch}
  .loading{
    position:absolute;inset:0;display:none;place-items:center;background:var(--panel);
    z-index:3;color:var(--ink-3);font-size:13.5px;
  }
  .loading.show{display:grid}
  .spin{
    width:16px;height:16px;border-radius:50%;border:2px solid var(--line);
    border-top-color:var(--accent);animation:spin .7s linear infinite;
    display:inline-block;vertical-align:-3px;margin-right:9px;
  }
  @keyframes spin{to{transform:rotate(360deg)}}
  .toTop{
    position:absolute;right:20px;bottom:20px;z-index:4;width:38px;height:38px;
    border-radius:50%;border:1px solid var(--line);background:var(--panel);color:var(--ink-2);
    cursor:pointer;display:none;place-items:center;box-shadow:var(--shadow);
  }
  .toTop.show{display:grid}
  .toTop svg{width:16px;height:16px}
  .toTop:hover{color:var(--accent);border-color:var(--accent)}
"""

template = io.open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
head, tail = template.split("<!--PAYLOAD-->")

meta = [{"n": a[0], "t": a[1], "g": a[2], "css": a[4]} for a in articles]

parts = [head.replace("/*SHELL_CSS*/", shell_css + EXTRA_CSS)]
parts.append('<script type="application/json" id="meta">%s</script>\n' % payload(meta))
parts.append('<script type="application/json" id="blobs">%s</script>\n' % payload(blobs))
for i, css in enumerate(style_blocks):
    parts.append('<script type="application/json" id="css%d">%s</script>\n' % (i, payload(css)))
for a in articles:
    parts.append('<script type="application/json" id="art%d">%s</script>\n' % (a[0], payload(a[3])))
parts.append(tail)

out = "".join(parts)
io.open(OUT, "w", encoding="utf-8").write(out)
print("")
print("wrote: %s" % OUT)
print("size : %.2f MB" % (len(out.encode("utf-8")) / 1e6))
