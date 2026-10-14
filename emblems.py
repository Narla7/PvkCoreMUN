"""
emblems.py — one inked emblem per committee.

Each is a 64x64 line drawing, stroked in the current text colour so it takes
whatever the surrounding ink is. No fills, no gradients: these are meant to
read as pen-and-ink diagrams, not icons.
"""

_HEAD = ('<svg class="emblem" viewBox="0 0 64 64" aria-hidden="true" '
         'fill="none" stroke="currentColor" stroke-width="1.15" '
         'stroke-linecap="round" stroke-linejoin="round">')
_TAIL = "</svg>"


EMBLEMS = {
    # A globe on its axis: the plenary seen from anywhere.
    "unga": (
        '<circle cx="32" cy="32" r="21"/>'
        '<ellipse cx="32" cy="32" rx="8.5" ry="21"/>'
        '<path d="M11 25h42M11 39h42M11 32h42"/>'
    ),

    # Three rings interlocked.
    "ecosoc": (
        '<circle cx="21" cy="34" r="12.5"/>'
        '<circle cx="43" cy="34" r="12.5"/>'
        '<circle cx="32" cy="21" r="12.5"/>'
    ),

    # A balance, one pan already tipped.
    "unhrc": (
        '<path d="M32 13v41M23 54h18"/>'
        '<path d="M15 19h34"/>'
        '<path d="M20 19v11M44 19v11"/>'
        '<path d="M11 30a9 7 0 0 0 18 0"/>'
        '<path d="M35 30a9 7 0 0 0 18 0"/>'
        '<path d="M11 30a9 7 0 0 1 18 0M35 30a9 7 0 0 1 18 0"/>'
    ),

    # A pen, cut and ready.
    "ipp": (
        '<path d="M14 47 38 19"/>'
        '<path d="M38 19 47 8l8 7-11 12z"/>'
        '<path d="M38 19 46 27"/>'
        '<path d="M14 47a7 7 0 0 0 7 7"/>'
        '<path d="M11 58h18M11 52h9"/>'
    ),

    # A sheet, already ruled.
    "ipj": (
        '<path d="M17 10h30v44H17z"/>'
        '<path d="M17 10a4 4 0 0 0 0 8h4M47 10a4 4 0 0 1 0 8h-4"/>'
        '<path d="M17 46a4 4 0 0 1 0 8h4M47 46a4 4 0 0 0 0 8h-4"/>'
        '<path d="M23 24h18M23 31h18M23 38h11"/>'
    ),

    # Two columns and a pediment.
    "aippm": (
        '<path d="M9 18h46M12 22h40"/>'
        '<path d="M18 22v32M26 22v32M38 22v32M46 22v32"/>'
        '<path d="M14 54h36"/>'
        '<path d="M32 8v10"/>'
        '<circle cx="32" cy="6" r="2.5"/>'
    ),

    # A link pulled apart.
    "unodc": (
        '<path d="M29 19a11 11 0 1 0 0 26"/>'
        '<path d="M35 45a11 11 0 1 0 0-26"/>'
        '<path d="M26 26l4 4M38 38l-4-4"/>'
        '<path d="M10 15l6-3M54 15l-6-3"/>'
    ),

    # A disc already cracked.
    "crisis": (
        '<circle cx="32" cy="34" r="20"/>'
        '<path d="M32 14l-7 13 8 5-7 13"/>'
        '<path d="M25 27l-9-4M39 32l9 5M25 45l-8 5"/>'
    ),
}


def emblem(slug):
    """Return the inline SVG for a committee slug, or an empty string."""
    body = EMBLEMS.get(slug)
    return _HEAD + body + _TAIL if body else ""