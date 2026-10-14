#!/usr/bin/env python3
"""
build.py — PVKcoreMUN

Turns config.py, emblems.py and templates/shell.html into out/, a folder of
static pages that can be uploaded to any host as-is. Standard library only:
no pip, no bundler, no build service.

    python3 build.py           build into out/
    python3 build.py --check   build, then verify every internal link resolves
    python3 build.py --serve   build, then serve out/ on http://localhost:8080
"""

import argparse
import functools
import html
import os
import re
import shutil
import sys

import config
import emblems
import ornaments

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
THEME = os.path.join(ROOT, "theme")
TEMPLATES = os.path.join(ROOT, "templates")

esc = html.escape


# --- small pieces of markup ------------------------------------------------

def rule(cls="foot-rule"):
    return '<div class="%s" aria-hidden="true"></div>' % cls


def divider(kind):
    """A drawn rule to break a section, cycling through the three shapes."""
    return ('<div class="divider" aria-hidden="true">%s</div>'
            % ornaments.flourish(kind))


DIVIDER_CYCLE = ("vine", "lozenge", "wing")


def dividers(count):
    return "\n".join(divider(DIVIDER_CYCLE[i % len(DIVIDER_CYCLE)])
                     for i in range(count))


def head(text, anchor=None):
    """A section heading, optionally doubling as an anchor target."""
    idattr = ' id="%s"' % anchor if anchor else ""
    return '<h2 class="section-head"%s>%s</h2>' % (idattr, esc(text))


def illuminated(line):
    """Rubricate the opening capital of a slogan line."""
    return ('<span class="cap">%s</span>%s'
            % (esc(line[0]), esc(line[1:])))


def marginalia(text):
    return '<p class="marginalia">%s</p>' % esc(text)


def epigraph(text, source):
    return ('<blockquote class="epigraph">%s<cite>%s</cite></blockquote>'
            % (esc(text), esc(source)))


def write(relpath, body, title, description):
    """Render one page through the shell and drop it in out/."""
    path = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(os.path.join(TEMPLATES, "shell.html"), encoding="utf-8") as fh:
        shell = fh.read()

    page = (shell
            .replace("{{title}}", esc(title))
            .replace("{{description}}", esc(description))
            .replace("{{nav}}", nav_html(current=relpath))
            .replace("{{content}}", body)
            .replace("{{corners}}", corner_markup())
            .replace("{{stain}}", stain_markup())
            .replace("{{seal}}", ornaments.wax_seal())
            .replace("{{root}}", "/")
            .replace("{{email}}", config.CONTACT_EMAIL)
            .replace("{{venue}}", config.VENUE_URL)
            .replace("{{dates}}", esc(config.DATES))
            .replace("{{site_name}}", esc(config.SITE["name"])))

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return relpath


# --- navigation ------------------------------------------------------------

def nav_html(current):
    """The nav strip, with the current page marked for screen readers."""
    parts = []
    for label, path in config.NAV:
        here = (path == "/" and current == "index.html")
        mark = ' aria-current="page"' if here else ""
        parts.append('    <a href="%s"%s>%s</a>' % (path, mark, esc(label)))
    return "\n".join(parts)


def corner_markup():
    """The same bracket, turned into each of the folio's four corners."""
    return "\n    ".join(
        '<span class="corner c%d">%s</span>' % (i, ornaments.corner())
        for i in range(1, 5)
    )


def stain_markup():
    """Two ink accidents, in opposite margins, clear of the text."""
    return ('<span class="stain s1">%s</span>\n    '
            '<span class="stain s2">%s</span>'
            % (ornaments.splatter(3, n=11), ornaments.splatter(8, n=9)))


# --- the long folio --------------------------------------------------------

def frontispiece():
    s = config.SLOGAN
    return """
<section class="frontispiece">
  <div class="rose" aria-hidden="true">%s</div>
  <p class="illum">
    <span class="line">%s</span>
    <span class="line">%s</span>
    <span class="gloss">%s</span>
  </p>
  <p class="dates">%s</p>
  <p class="venue-line">
    <a href="%s" rel="noopener">the venue</a>
  </p>
  <div class="gutter">
    <p class="lede dropcap reveal">%s</p>
    %s
  </div>
</section>
""" % (ornaments.compass_rose(),
       illuminated(s["first"]), illuminated(s["second"]),
       esc(s["gloss"]), esc(config.DATES), config.VENUE_URL,
       esc(config.INTRO), marginalia("begin here —"))


def committees_section():
    cards = []
    for c in config.COMMITTEES:
        cards.append(
            '      <li><a class="card" href="/committees/%s/">'
            '%s'
            '<h3>%s</h3>'
            '<p class="cname">%s</p>'
            '<p class="cmandate">%s</p>'
            '</a></li>'
            % (c["slug"], emblems.emblem(c["slug"]), esc(c["abbr"]),
               esc(c["name"]), esc(c["mandate"]))
        )
    return """
<section class="section reveal" id="committees">
  %s
  <div class="gutter">
    <ul class="cards">
%s
    </ul>
    %s
  </div>
</section>
""" % (head("The Committees", "committees"),
       "\n".join(cards),
       marginalia("eight rooms, two days —"))


def programme_section():
    days = []
    for title, date, slots in config.PROGRAMME:
        rows = []
        for label, where in slots:
            rows.append(
                '        <div class="slot"><span class="t">—</span>'
                '<span class="w">%s<small>%s</small></span></div>'
                % (esc(label), esc(where))
            )
        days.append(
            '    <div class="day">\n'
            '      <h3>%s</h3>\n'
            '      <p class="date">%s</p>\n'
            '%s\n'
            '    </div>'
            % (esc(title), esc(date), "\n".join(rows))
        )
    return """
<section class="section reveal" id="programme">
  %s
  <div class="gutter">
    <div class="days">
%s
    </div>
    <p class="foot-contact" style="margin-top:1.4rem">
      gavel times are fixed in the <a href="/brochure/">brochure</a>.
    </p>
    %s
  </div>
</section>
""" % (head("The Programme", "programme"),
       "\n".join(days),
       marginalia("times to be gaveled —"))


def delegation_section():
    return """
<section class="section reveal" id="delegation">
  %s
  <div class="gutter">
    <p class="lede" style="margin-left:0">%s</p>
    <p>
      <a href="/registrations/">Registrations</a> are opening soon, and the
      <a href="/country-matrix/">country matrix</a> is revealing soon.
    </p>
    %s
  </div>
</section>
""" % (head("Delegation", "delegation"),
       esc(config.DELEGATION),
       marginalia("apply when the seal lifts —"))


def rules_section():
    items = []
    for term, body in config.RULES:
        items.append(
            '      <div><dt>%s</dt><dd>%s</dd></div>'
            % (esc(term), esc(body))
        )
    return """
<section class="section reveal" id="rules">
  %s
  <dl class="defs">
%s
  </dl>
</section>
""" % (head("Rules & Procedure", "rules"), "\n".join(items))


def sealed_strip():
    rows = []
    for p in config.SEALED:
        rows.append(
            '      <li><a class="sealed-card" href="/%s/">'
            '<span class="pending">coming soon</span>'
            '<h3>%s</h3><small>%s</small></a></li>'
            % (p["slug"], esc(p["title"]), esc(p["note"]))
        )
    return """
<section class="section reveal" id="sealed">
  %s
  <div class="gutter">
    <ul class="cards">
%s
    </ul>
  </div>
</section>
""" % (head("Still Sealed", "sealed"), "\n".join(rows))


def index_page():
    parts = [frontispiece()]
    sections = [committees_section(), programme_section(),
                delegation_section(), rules_section(), sealed_strip()]
    for i, sec in enumerate(sections):
        if i:
            parts.append(divider(DIVIDER_CYCLE[i % len(DIVIDER_CYCLE)]))
        parts.append(sec)

    return write("index.html", "\n".join(parts),
                 config.SITE["title"], config.SITE["description"])


# --- committee leaves ------------------------------------------------------

def committee_page(c):
    body = """
<section class="leaf">
  <div class="leaf-head">
    <div class="leaf-mark">%s</div>
    <h1 class="leaf-title">%s</h1>
    <p class="leaf-sub">%s</p>
  </div>

  <div class="plate" aria-hidden="true">%s</div>

  <div class="leaf-body">
    <div class="gutter">
      %s
      %s
    </div>

    <h3>Mandate</h3>
    <p>%s</p>

    <h3>The brief</h3>
    <p>The full mandate, the resolution topic, and the working papers will be
       published in the <a href="/brochure/">brochure</a>.</p>

    <h3>Who sits here</h3>
    <p>Delegates are allotted from the
       <a href="/country-matrix/">country matrix</a>. The gavel and the
       speaker's list are the chair's business, and the chair is
       <a href="/chairs/">revealing soon</a>.</p>

    <a class="back-link" href="/#committees">back to the committees</a>
  </div>
</section>
""" % (emblems.emblem(c["slug"]), esc(c["name"]), esc(c["mandate"]),
       ornaments.study(c["slug"]),
       epigraph(c["epigraph"], c["source"]),
       marginalia(c["abbr"].lower() + " —"),
       esc(c["mandate"]))

    return write("committees/%s/index.html" % c["slug"], body,
                 "%s — %s" % (c["name"], config.SITE["name"]),
                 "%s at %s. %s" % (c["name"], config.SITE["name"],
                                   config.SITE["description"]))


# --- sealed pages ----------------------------------------------------------

def sealed_page(p):
    body = """
<section class="sealed reveal">
  <p class="stamp">coming soon</p>
  <h1>%s</h1>
  <p>%s</p>
  <a class="back-link" href="/">back to the frontispiece</a>
</section>
""" % (esc(p["title"]), esc(p["note"]))

    return write("%s/index.html" % p["slug"], body,
                 "%s — %s" % (p["title"], config.SITE["name"]),
                 "%s. %s" % (p["title"], config.SITE["description"]))


# --- build -----------------------------------------------------------------

def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    pages = [index_page()]
    pages += [committee_page(c) for c in config.COMMITTEES]
    pages += [sealed_page(p) for p in config.SEALED]

    for name in os.listdir(THEME):
        src = os.path.join(THEME, name)
        dest = os.path.join(OUT, name)
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)

    return pages


# --- link checking ---------------------------------------------------------

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
ID_RE = re.compile(r'\bid="([^"]+)"')


def resolve(url):
    """Map a site-absolute URL to the file it should point at. None if external."""
    if url.startswith(("http://", "https://", "mailto:", "//", "data:")):
        return None
    path, _, frag = url.partition("#")
    if not path:
        return ("", frag)
    path = path.lstrip("/")
    if path == "":
        path = "index.html"
    elif path.endswith("/"):
        path += "index.html"
    elif "." not in os.path.basename(path):
        path += "/index.html"
    return (path, frag)


def check():
    pages = []
    for dirpath, _, files in os.walk(OUT):
        for name in files:
            if name.endswith(".html"):
                pages.append(os.path.join(dirpath, name))

    problems = []
    for page in pages:
        rel = os.path.relpath(page, OUT)
        with open(page, encoding="utf-8") as fh:
            doc = fh.read()
        for url in set(LINK_RE.findall(doc)):
            target = resolve(url)
            if target is None:
                continue
            path, frag = target
            dest = os.path.join(OUT, path)
            if not os.path.exists(dest):
                problems.append("%s -> %s (no such file)" % (rel, url))
                continue
            if frag and path.endswith(".html"):
                with open(dest, encoding="utf-8") as fh:
                    if frag not in ID_RE.findall(fh.read()):
                        problems.append("%s -> %s (no #%s)" % (rel, url, frag))
    return problems


def main():
    ap = argparse.ArgumentParser(description="Build PVKcoreMUN into out/")
    ap.add_argument("--check", action="store_true",
                    help="verify every internal link resolves")
    ap.add_argument("--serve", action="store_true",
                    help="serve out/ on http://localhost:8080")
    args = ap.parse_args()

    pages = build()
    print("built %d pages -> out/" % len(pages))

    if args.check:
        problems = check()
        if problems:
            print("\nbroken links:")
            for p in problems:
                print("  " + p)
            sys.exit(1)
        print("all internal links resolve")

    if args.serve:
        import functools
        import http.server
        import socketserver
        handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                    directory=OUT)
        with socketserver.TCPServer(("", 8080), handler) as httpd:
            print("serving out/ on http://localhost:8080  (ctrl-c to stop)")
            httpd.serve_forever()


if __name__ == "__main__":
    main()