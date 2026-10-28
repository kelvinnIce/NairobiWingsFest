#!/usr/bin/env python3
"""Builds index.html from src/. Run: python3 build.py
The page ships as one self-contained file: fonts, images and scripts are inlined."""
import base64, os, random, re
ROOT = os.path.dirname(os.path.abspath(__file__))
S = lambda *p: os.path.join(ROOT, "src", *p)
def rd(*p): return open(S(*p), encoding="utf-8").read()
def b64(*p): return base64.b64encode(open(S(*p), "rb").read()).decode()
def webp(name): return "data:image/webp;base64," + b64("img", name)

def face(family, file, weight, stretch=None):
    s = f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
    if stretch: s += f"font-stretch:{stretch};"
    return s + f"font-display:swap;src:url(data:font/woff2;base64,{b64('fonts', file)}) format('woff2');}}\n"

tokens = {
  "__FONTS__": face("Anton", "anton.woff2", 400) + face("Instrument Sans", "instrument-sans.woff2", "400 700", "75% 100%"),
  "__COMMON_CSS__": rd("css", "common.css"),
  "__SHARED_JS__": rd("js", "shared.js") + "\n" + rd("js", "shared2.js"),
  "__BADGE__": "data:image/svg+xml;base64," + b64("img", "logo.svg"),
  "__TICKET__": rd("ticket.html"),
  "__TICKET_CSS__": rd("css", "ticket.css"),
  "__TICKET_JS__": rd("js", "ticket.js"),
}
# hero images (the four corner photos)
for n in ("basket", "eating", "saucy", "hand_s"):
    tokens[f"__IMG_{n}__"] = webp(f"hero-{n}.webp")
# What to expect pills
for i in range(1, 7):
    tokens[f"__IMG_P{i}__"] = webp(f"pill-p{i}.webp")
tokens["__IMG_PEEK__"] = webp("spots-drip.webp")        # 20 spots, cheese pile
tokens["__IMG_DOOR_V__"] = webp("door-cook.webp")       # Cook for the crown
tokens["__IMG_DOOR_S__"] = webp("door-partner.webp")    # Own a moment

CROWN = ('<svg class="crown-svg" viewBox="0 0 200 170" aria-hidden="true" focusable="false" fill="none" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M14 36 L62 70 L108 16 L128 80 L186 82 L150 148 L20 128 Z" stroke="currentColor" stroke-width="13"/>'
         '<path d="M54 104 L118 120" stroke="#F2922B" stroke-width="12"/></svg>')
tokens["__CROWN__"] = CROWN
tokens["__ARROW__"] = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M8 12h8M13 9l3 3-3 3" stroke-linecap="round" stroke-linejoin="round"/></svg>')

FAQ = [
 ("When and where is it?", "April 2027, in Nairobi. We are locking the venue and date now, and the early list hears first."),
 ("How does voting work?", "Each ticket has a QR code tied to it, which gives you one vote. Voting is open all day and the crowd counts for 70 percent of the final score."),
 ("Who are the judges?", "The panel is announced closer to the date. They score 30 percent of the final result."),
 ("How do I enter as a vendor?", "Use the early list form and pick Wings spot. We keep the field to 20 spots and choose with care."),
 ("Is it only wings?", "Wings are the centre of it. Around them you get a wing eating contest, chef masterclasses, hot sauce challenges, live music and DJs."),
 ("Can my brand get involved?", "Yes. Founding partner positions are open now, and select categories can be made exclusive."),
]
tokens["__FAQ__"] = "".join(f"<details{' open' if i==0 else ''}><summary>{q}</summary><p>{a}</p></details>" for i,(q,a) in enumerate(FAQ))

def qr(n=25, cell=8, fg="#3A0B14", bg="#F4E3D2"):
    random.seed(3)
    g = [[random.random() < .48 for _ in range(n)] for _ in range(n)]
    def finder(x0, y0):
        for y in range(-1, 8):
            for x in range(-1, 8):
                xx, yy = x0 + x, y0 + y
                if 0 <= xx < n and 0 <= yy < n:
                    g[yy][xx] = 0 <= x <= 6 and 0 <= y <= 6 and (x in (0, 6) or y in (0, 6) or (2 <= x <= 4 and 2 <= y <= 4))
    finder(0, 0); finder(n - 7, 0); finder(0, n - 7)
    rects = [f'<rect x="{x*cell}" y="{y*cell}" width="{cell}" height="{cell}"/>' for y in range(n) for x in range(n) if g[y][x]]
    s = n * cell
    return f'<svg viewBox="0 0 {s} {s}" role="img" aria-label="Illustrative QR code. Your real code arrives with your ticket." shape-rendering="crispEdges"><rect width="{s}" height="{s}" fill="{bg}"/><g fill="{fg}">{"".join(rects)}</g></svg>'

tokens["__QR_D__"] = qr()

# ticket tokens resolve first so tokens inside them get filled too
first = ["__TICKET__", "__TICKET_CSS__", "__TICKET_JS__"]
order = first + [t for t in tokens if t not in first]
html = rd("template.html")
for _ in range(3):
    for t in order: html = html.replace(t, tokens[t])
html = html.replace("__BTN__", "btn-cream")
left = set(re.findall(r"__[A-Za-z0-9_]+__", html))
assert not left, f"unfilled tokens: {left}"
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
print("index.html", round(len(html) / 1e3), "KB")
