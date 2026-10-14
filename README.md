# pvkcoremun

Source for the **PVKcoreMUN** site — *Ars Imperii, Ars Diplomatica*.

Hand-written HTML and CSS over a Python generator, with no framework, no
bundler and no dependencies. `build.py` turns `config.py` and one template into
the folder that gets uploaded. Standard library only: it runs on any Python 3.

```bash
python3 build.py            # build into out/
python3 build.py --check    # build, then verify every internal link resolves
python3 build.py --serve    # build, then serve out/ on http://localhost:8080
```

`out/` is self-contained and static — upload the folder to any host and it
works. Nothing is fetched at runtime: the fonts are committed under
`theme/fonts/` and served from the same origin, so there is no third-party
dependency and no CSP to fight.

## Layout

```
build.py                  the generator
config.py                 all content: committees, epigraphs, programme, rules
emblems.py                one inline-SVG emblem per committee
ornaments.py              every drawing: rose, seal, flourishes, studies, ink
templates/shell.html      the page shell, as one template
theme/style.css           the whole look — palette, ornament, ornament rules
theme/site.js             the only script: reveals sections as you read
theme/fonts/*.woff2       self-hosted, latin subset (Fell, Fell SC, Garamond, Caveat)
theme/textures/*.png      aged-paper layers, generated (see below)
theme/seal.svg            favicon
out/                      build output — exactly what gets uploaded
```

Total `out/` is about 620K, of which 280K is fonts — cached once, then free.
The markup itself is 25K for the longest page.

## Editing content

Almost everything lives in `config.py`; nothing needs editing by hand.

| to change | edit |
| --- | --- |
| dates, venue link, contact | the top of `config.py` |
| a committee's name, mandate, epigraph | its entry in `COMMITTEES` |
| the nav bar | `NAV` |
| the two-day programme | `PROGRAMME` |
| rules & procedure | `RULES` |
| what a sealed page says | `SEALED` |
| a committee's emblem | `emblems.py` |
| a new drawing or flourish | `ornaments.py` |

A build that finds a broken internal link aborts before anything is uploaded.

## The drawings

There are no image files for the artwork. Every ornament is inline SVG generated
by `ornaments.py`, so it scales, recolours with the text, and costs no request.
Geometry is computed rather than hand-typed — compass points, the wobble on the
wax seal and the hatching clip all come out of the same few helpers.

| piece | where it appears |
| --- | --- |
| `compass_rose()` | ruled faintly behind the motto |
| `wax_seal()` | pressed into the rule under the wordmark |
| `flourish(kind)` | between folio sections — `vine`, `lozenge`, `wing`, in rotation |
| `corner()` | the folio's four corners |
| `splatter(seed)` | ink accidents in the outer margins |
| `study(slug)` | one construction plate per committee leaf |

The three paper textures are the only real images, 28K in total:

| file | what it is | size on screen |
| --- | --- | --- |
| `foxing.png` | sparse rusty age spots, alpha | 560px tile, 17% |
| `mottle.png` | uneven pulp, value noise | 260px tile, soft-light |
| `fibre.png` | laid lines | 128px tile, soft-light |

They were made by writing greyscale PGM masks in Python and letting ImageMagick
colour them — noise thresholding through ImageMagick alone flattened to nothing
at the settings these wanted. Each is small, so the 560px tile repeats without
the repeat reading as a pattern.

## The design decisions

**Gruvbox, dark by default.** The full palette, unmodified, over `#282828`
with the folio floating on `#1d2021`.

**Decoration carries the meaning, not labels.** Section headings are small
caps in IM Fell English SC; the committee marks are pen-and-ink SVG diagrams;
the marginalia in the gutter are handwritten (Caveat) and deliberately
awkward to read. What a visitor has to act on — dates, the venue link, the
contact address — stays plain and legible, because a site that can't be
navigated isn't a site.

**The period is never named.** No heading, no alt text, no meta description
says what era the site is drawing on. The forms do the work alone. There is a
test for this: `grep -ric renaissance out/` must print nothing.

**Machiavelli throughout.** Every committee carries an epigraph, set in Fell
Italic and hung off a gold rule. Chapter references are given only where the
citation is certain; otherwise just the work. If you replace any, keep them
real — the conceit collapses the moment a quotation is wrong.

**Nothing is hidden behind a script.** The entrance animation is opt-in: a
one-line script in `<head>` adds `has-js` to the document, and only then does
the CSS hide the unrevealed sections. With JavaScript off, blocked by a
strict CSP, or erroring, the folio is simply a page of text. There is a
one-second fallback in `site.js` in case an observer callback goes missing.

**"Coming soon" is a stamp.** The five unreleased sections are real pages, so
no nav link ever 404s, and each carries a rotated double-ruled rubric stamp.
That is the one place the decoration rule yields to literal text, because a
visitor has to be told the thing does not exist yet.

## Constraints

- **Absolute internal URLs** (`/committees/unga/`), so the output works on any
  host. This does mean it needs to be served — opening `out/index.html` off
  the filesystem will not resolve its stylesheet. Use `--serve`.
- **`--check` covers links and anchors**, not contrast or semantics.
- **No build service, no runtime dependencies.** If it runs, it runs.