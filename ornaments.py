"""
ornaments.py — the drawings.

Everything here is inline SVG stroked in the current text colour, so each piece
takes whatever ink it is drawn in and none of it is an asset to load. The
geometry is computed rather than hand-typed: compass points, foil noise and
construction grids all come out of the same few helpers, which is why the lines
meet where they are supposed to.

All of it is decorative, so every piece is aria-hidden.
"""

import math
import random


# --- helpers ---------------------------------------------------------------

def svg(body, vb="0 0 200 200", cls="ornament", stroke=1.0):
    return ('<svg class="%s" viewBox="%s" aria-hidden="true" fill="none" '
            'stroke="currentColor" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>' % (cls, vb, stroke, body))


def pt(cx, cy, ang, r):
    return (cx + r*math.cos(ang), cy + r*math.sin(ang))


def poly(points, close=True):
    d = "M%.2f %.2f" % points[0] + "".join("L%.2f %.2f" % p for p in points[1:])
    return '<path d="%s%s"/>' % (d, "Z" if close else "")


def ticks(cx, cy, r, n, length, every=1):
    """Radial tick marks, like the degree ring on an instrument."""
    out = []
    for i in range(n):
        if i % every:
            continue
        a = 2*math.pi*i/n
        x1, y1 = pt(cx, cy, a, r)
        x2, y2 = pt(cx, cy, a, r-length)
        out.append("M%.2f %.2fL%.2f %.2f" % (x1, y1, x2, y2))
    return '<path d="%s"/>' % "".join(out)


def hatch(x, y, w, h, gap=5, angle=-45):
    """Parallel ruled lines inside a box — the engraver's shading.

    Each line is offset along the normal and then clipped to the box by
    Liang-Barsky, so the hatch fills the rectangle and stops dead at its edge.
    """
    dx, dy = math.cos(angle), math.sin(angle)
    segs = []
    reach = int((abs(w*dy) + abs(h*dx)) / gap) + 2
    for i in range(reach + 1):
        off = i*gap - (abs(w*dy) + abs(h*dx))/2
        px, py = x - dy*off, y + dx*off
        got = _clip(x, y, w, h, px, py, dx, dy)
        if got and math.hypot(got[1][0]-got[0][0], got[1][1]-got[0][1]) > 2:
            segs.append("M%.2f %.2fL%.2f %.2f" % (got[0][0], got[0][1],
                                                  got[1][0], got[1][1]))
    return '<path d="%s" opacity=".4"/>' % "".join(segs)


def _clip(x, y, w, h, px, py, dx, dy):
    """Liang-Barsky: clip the segment to the box, or None if it misses."""
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, px - x), (dx, x + w - px),
                 (-dy, py - y), (dy, y + h - py)):
        if abs(p) < 1e-9:
            if q < 0:
                return None
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return None
            t0 = max(t0, r)
        else:
            if r < t0:
                return None
            t1 = min(t1, r)
    return ((px + t0*dx, py + t0*dy), (px + t1*dx, py + t1*dy))


def mirror(body):
    """Emit an element and its reflection about the centre of a 200-wide box."""
    return (body,
            body.replace("<path ", '<path transform="translate(200 0) scale(-1 1)" ')
                 .replace("<circle ", '<circle transform="translate(200 0) scale(-1 1)" '))


def wave(cx, cy, r, seed, wob=0.05, n=72):
    """A circle whose radius is nudged by a cheap deterministic noise."""
    pts = []
    for i in range(n):
        a = 2*math.pi*i/n
        k = (math.sin(a*3 + seed) + math.sin(a*5 + seed*1.7) * .5
             + math.sin(a*9 + seed*2.3) * .25)
        rr = r * (1 + wob*k/1.75)
        pts.append((cx + rr*math.cos(a), cy + rr*math.sin(a)))
    return pts


# --- the frontispiece furniture --------------------------------------------

def compass_rose(size=200):
    """An instrument rose: eight points, degree ring, inked and half-shaded."""
    cx = cy = 100
    b = ['<circle cx="100" cy="100" r="94"/>',
         '<circle cx="100" cy="100" r="86"/>',
         ticks(cx, cy, 94, 72, 4, every=2),
         ticks(cx, cy, 86, 36, 3)]

    for i in range(8):
        a = math.radians(i*45 - 90)
        long = (i % 2 == 0)
        L = 80 if long else 52
        w = 7.5 if long else 5.5
        d = (math.cos(a), math.sin(a))
        p = (-d[1], d[0])
        tip = pt(cx, cy, a, L)
        base = pt(cx, cy, a, L*0.26)
        b1 = (base[0] + p[0]*w, base[1] + p[1]*w)
        b2 = (base[0] - p[0]*w, base[1] - p[1]*w)
        # the shaded flank, drawn first so the outline sits over it
        b.append('<path d="M%.2f %.2fL%.2f %.2fL%.2f %.2fZ" fill="currentColor" '
                 'stroke="none" opacity=".2"/>'
                 % (cx, cy, b2[0], b2[1], tip[0], tip[1]))
        b.append(poly([(cx, cy), b1, tip, b2]))

    b.append('<circle cx="100" cy="100" r="6"/>')
    b.append(ticks(cx, cy, 80, 8, 6))
    return svg("".join(b))


def wax_seal():
    """A seal pressed in red wax, carrying the first letter of the motto."""
    outer = wave(100, 100, 84, seed=1.7, wob=.055)
    b = ['<path d="%sZ" fill="currentColor" stroke="none" opacity=".28" '
         'transform="translate(100 100) scale(1.03) translate(-100 -100)"/>'
         % _path(outer),
         poly(outer),
         '<circle cx="100" cy="100" r="70" opacity=".7"/>',
         '<circle cx="100" cy="100" r="64" opacity=".45"/>',
         ticks(100, 100, 70, 60, 5, every=2)]
    # a cross-hatched press mark, offset like a real impression
    b.append(hatch(62, 62, 76, 76, gap=9, angle=38))
    b.append('<text x="100" y="122" text-anchor="middle" font-family="Fell SC, '
             'Georgia, serif" font-size="82" fill="currentColor" '
             'stroke="none" opacity=".55">A</text>')
    return svg("".join(b), cls="ornament seal-wax")


def _path(points, close=False):
    d = "M%.2f %.2f" % points[0] + "".join("L%.2f %.2f" % p for p in points[1:])
    return d + ("Z" if close else "")


# --- section dividers ------------------------------------------------------

def flourish(kind="vine"):
    """A rule to break a section. Three shapes, used in rotation."""
    if kind == "lozenge":
        b = ['<path d="M4 20h74M122 20h74"/>',
             poly([(100, 13), (107, 20), (100, 27), (93, 20)]),
             '<circle cx="84" cy="20" r="2.6"/>',
             '<circle cx="116" cy="20" r="2.6"/>']
        return svg("".join(b), vb="0 0 200 40")

    if kind == "wing":
        half = ('<path d="M100 20C88 7 68 2 50 6c13 6 20 9 24 14z"/>'
                '<path d="M92 18C84 10 72 6 62 5" opacity=".5"/>'
                '<path d="M96 20C88 14 76 10 66 9" opacity=".4"/>')
        a, b2 = mirror(half)
        b = [a, b2, '<circle cx="100" cy="20" r="2.4"/>',
             '<path d="M6 20h30M164 20h30" opacity=".5"/>']
        return svg("".join(b), vb="0 0 200 40")

    # vine: one stem drawn as a run of curves, then its reflection
    half = ('<path d="M100 20c-8 0-11-7-17-8s-9 7-16 7-9-8-16-6-9 5-15 3"/>'
            '<path d="M84 13c-2-5-1-8 3-10 1 4 0 7-3 10z"/>'
            '<path d="M68 19c-1 5 0 8 4 10 0-4-1-7-4-10z"/>')
    a, b2 = mirror(half)
    b = [a, b2, poly([(100, 16), (103.5, 20), (100, 24), (96.5, 20)])]
    return svg("".join(b), vb="0 0 200 40")


def corner():
    """A filigree bracket for the folio's corners."""
    b = ['<path d="M3 36V15a12 12 0 0 1 12-12h21"/>',
         '<path d="M3 24c9 0 14-5 15-14M24 3c0 10-5 15-15 15" opacity=".4"/>',
         '<circle cx="17" cy="17" r="2.2" opacity=".65"/>',
         '<circle cx="27" cy="11" r="1.5" opacity=".45"/>',
         '<circle cx="11" cy="27" r="1.5" opacity=".45"/>']
    return svg("".join(b), vb="0 0 40 40", cls="ornament corner")


# --- ink accidents ---------------------------------------------------------

def splatter(seed=0, n=14):
    """Blots and flicks, the kind a nib leaves. Placed in the page margins."""
    rnd = random.Random(seed * 977 + 13)
    b = []
    for i in range(n):
        x = rnd.uniform(12, 188)
        y = rnd.uniform(12, 188)
        r = rnd.uniform(.9, 4.6) * (2.2 if i % 5 == 0 else 1)
        b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="currentColor" '
                 'stroke="none" opacity=".32"/>' % (x, y, r))
        if i % 3 == 0:                       # a flick trailing off the blot
            b.append('<path d="M%.1f %.1fl%.1f %.1f" opacity=".3"/>'
                     % (x, y, rnd.uniform(-11, 11), rnd.uniform(-11, 11)))
    return svg("".join(b), cls="ornament splatter", stroke=1)


# --- notebook studies ------------------------------------------------------
#
# One construction drawing per committee: a figure of geometry and
# proportion, in the way a workshop notebook lays out a problem before
# solving it. Each is drawn in its own 200x200 frame.

def _figure():
    b = ['<path d="M14 186h172" opacity=".35"/>',
         '<path d="M14 196h172" opacity=".2"/>',
         ticks(100, 186, 86, 30, 4)]
    return b


def _study_circle():
    b = _figure()
    b += ['<circle cx="100" cy="96" r="62"/>',
          '<path d="M38 96h124" opacity=".3"/>',
          '<path d="M100 34v124" opacity=".3"/>']
    for k in range(8):
        a = math.radians(k*45 - 90)
        x, y = pt(100, 96, a, 62)
        b.append('<circle cx="%.1f" cy="%.1f" r="2.4"/>' % (x, y))
        b.append('<path d="M100 96L%.1f %.1f" opacity=".45"/>' % (x, y))
    b.append('<path d="M56 60c26-14 62-12 84 6" opacity=".25"/>')
    return b


def _study_square():
    b = _figure()
    b += ['<rect x="46" y="42" width="108" height="108"/>',
          '<rect x="66" y="62" width="68" height="68" opacity=".6"/>',
          '<path d="M46 42l128 108M174 42L46 150" opacity=".3"/>',
          '<path d="M46 150l32-32M174 42l-32 32" opacity=".5"/>']
    b.append(hatch(66, 62, 68, 68, gap=7, angle=-45))
    b.append('<circle cx="100" cy="96" r="4"/>')
    return b


def _study_pentagon():
    b = _figure()
    pts = [pt(100, 92, math.radians(-90 + k*72), 58) for k in range(5)]
    star = [pts[k] for k in (0, 2, 4, 1, 3)]
    b.append(poly(pts))
    b.append(poly(star))
    b.append(hatch(pts[3][0], pts[3][1], 40, 40, gap=6))
    for p in pts:
        b.append('<circle cx="%.1f" cy="%.1f" r="2.2"/>' % p)
    return b


def _study_figure():
    """A figure reduced to proportions and ruled into squares."""
    b = _figure()
    b += ['<rect x="76" y="24" width="48" height="150" opacity=".3"/>']
    for i in range(1, 4):
        y = 24 + i*150/4
        b.append('<path d="M70 %.1fH130" opacity=".45"/>' % y)
    b += ['<circle cx="100" cy="40" r="12"/>',
          '<path d="M100 52v50M100 102l-16 34M100 102l16 34"/>',
          '<path d="M100 62l-22 18M100 62l22 18"/>',
          '<path d="M92 74h16v28H92z" opacity=".55"/>']
    b.append(hatch(76, 24, 48, 37, gap=6))
    return b


def _study_vesica():
    b = _figure()
    b += ['<circle cx="74" cy="96" r="52"/>',
          '<circle cx="126" cy="96" r="52"/>',
          '<path d="M74 44a52 52 0 0 1 0 104M126 44a52 52 0 0 0 0 104" '
          'opacity=".4"/>',
          '<path d="M100 30v132" opacity=".3"/>',
          '<path d="M48 96h104" opacity=".3"/>']
    b.append('<path d="M74 44 126 148M126 44 74 148" opacity=".35"/>')
    return b


def _study_spiral():
    """A helix unwound — stairs drawn as the curve they make."""
    b = _figure()
    d = []
    for i in range(190):
        t = i/189
        a = t*math.pi*4.6
        r = 6 + t*76
        x, y = 100 + r*math.cos(a)*.92, 160 - t*132 + r*math.sin(a)*.30
        d.append((x, y))
    b.append('<path d="M%s" opacity=".8"/>' % " ".join(
        ("%.1f %.1f" % p) for p in d[::6]))
    b.append('<path d="M34 160h132" opacity=".3"/>')
    for k in range(9):
        y = 160 - k*16
        b.append('<path d="M100 %.1f h%.1f" opacity=".22"/>' % (y, 30 - k*2))
    return b


def _study_grid():
    """A plate of construction triangles, ruled and hatched."""
    b = _figure()
    b += ['<rect x="34" y="26" width="132" height="132" opacity=".35"/>']
    for i in range(1, 6):
        t = i/6
        b.append('<path d="M34 %.1f L166 %.1f" opacity=".28"/>'
                 % (26 + t*132, 26 + (1-t)*132))
    b += ['<path d="M34 26l132 132M166 26L34 158" opacity=".3"/>',
          '<circle cx="100" cy="92" r="46"/>']
    b.append(hatch(34, 92, 66, 66, gap=6, angle=45))
    b.append('<circle cx="100" cy="92" r="3"/>')
    return b


def _study_arc():
    """A dome and its construction: the ellipse under a rising vault."""
    b = _figure()
    b += ['<path d="M34 150a66 66 0 0 1 132 0"/>',
          '<ellipse cx="100" cy="150" rx="66" ry="17" opacity=".45"/>',
          '<path d="M34 150h132" opacity=".35"/>',
          '<path d="M100 24v126" opacity=".3"/>']
    for k in range(9):
        x = 34 + k*132/8
        b.append('<path d="M%.1f 150V%.1f" opacity=".2"/>'
                 % (x, 150 - math.sqrt(max(0, 1-((x-100)/66.0)**2))*66))
    b.append(hatch(34, 150, 132, 34, gap=7))
    return b


STUDIES = {
    "unga": _study_circle,
    "ecosoc": _study_square,
    "unhrc": _study_pentagon,
    "ipp": _study_grid,
    "ipj": _study_arc,
    "aippm": _study_figure,
    "unodc": _study_vesica,
    "crisis": _study_spiral,
}


def study(slug):
    draw = STUDIES.get(slug, _study_circle)
    return svg("".join(draw()), cls="ornament study")