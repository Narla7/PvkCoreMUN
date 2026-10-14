"""
config.py — PVKcoreMUN

Everything the build needs to know. Edit here, run build.py.
"""

SITE = {
    "name":        "PVKcoreMUN",
    "title":       "PVKcoreMUN — Ars Imperii, Ars Diplomatica",
    "description": "PVKcoreMUN. Two days, eight committees. Ars Imperii, "
                   "Ars Diplomatica. 6–7 November.",
    "url":         "",   # set to the deployed origin when you have one
}

# --- the event -------------------------------------------------------------

DATES = "6–7 November"
VENUE_URL = "https://maps.app.goo.gl/oHJX6wiGXzLsZWcn9"
CONTACT_EMAIL = "pvkcoremun@gmail.com"

SLOGAN = {
    "first":  "ARS IMPERII,",
    "second": "ARS DIPLOMATICA",
    "latin":  "ars imperii, ars diplomatica",
    "gloss":  "the art of rule, the art of diplomacy",
}

# The period itself is never named on the site. Only its forms are borrowed.

# --- navigation (label, path) ----------------------------------------------

NAV = [
    ("front",        "/"),
    ("committees",   "/#committees"),
    ("programme",    "/#programme"),
    ("delegation",   "/#delegation"),
    ("rules",        "/#rules"),
    ("secretariat",  "/secretariat/"),
    ("chairs",       "/chairs/"),
    ("brochure",     "/brochure/"),
    ("register",     "/registrations/"),
    ("matrix",       "/country-matrix/"),
]

# --- committees ------------------------------------------------------------
#
# Each carries an epigraph from Machiavelli. Chapter references are given only
# where the citation is certain; otherwise just the work.

COMMITTEES = [
    {
        "slug": "unga",
        "abbr": "UNGA",
        "name": "General Assembly",
        "mandate": "The plenary chamber. All of it, at once.",
        "epigraph": "A prince ought to have no other object, or thought, or "
                    "study, but war and its rules.",
        "source": "The Prince, XIV",
    },
    {
        "slug": "ecosoc",
        "abbr": "ECOSOC",
        "name": "Economic and Social Council",
        "mandate": "Development, trade, and the long accounting of nations.",
        "epigraph": "Men who seek to gain the good will of others in order to "
                    "make their own position secure are moved by a vain glory.",
        "source": "Discourses, II.2",
    },
    {
        "slug": "unhrc",
        "abbr": "UNHRC",
        "name": "Human Rights Council",
        "mandate": "What is owed to a person, and who is made to answer for it.",
        "epigraph": "It is not titles that make honour, but the things "
                    "themselves that are done.",
        "source": "The Prince, XVIII",
    },
    {
        "slug": "ipp",
        "abbr": "IPP",
        "name": "International Press Programme",
        "mandate": "The fourth estate in session. Report it as it happens.",
        "epigraph": "It is necessary to be a great robber, for one cannot be "
                    "called a robber in any other way.",
        "source": "The Prince, XV",
    },
    {
        "slug": "ipj",
        "abbr": "IPJ",
        "name": "International Press Journal",
        "mandate": "The paper of record, written after the room empties.",
        "epigraph": "Wise men do not obey the commands of one who is not "
                    "obeyed by his own people.",
        "source": "Discourses, I.46",
    },
    {
        "slug": "aippm",
        "abbr": "AIPPM",
        "name": "All-Party Parliamentary Forum",
        "mandate": "Cabinet, coalition, and the arithmetic of getting a majority.",
        "epigraph": "Fortuna favors the bold.",
        "source": "The Prince, XXV — fortuna agli adversi amica",
    },
    {
        "slug": "unodc",
        "abbr": "UNODC",
        "name": "Office on Drugs and Crime",
        "mandate": "Contraband, convention, and the paper trail between them.",
        "epigraph": "Whoever seeks to deceive may find him who will let himself "
                    "be deceived, but he will never find one who wishes to be "
                    "deceived.",
        "source": "The Prince, VII",
    },
    {
        "slug": "crisis",
        "abbr": "CRISIS",
        "name": "Crisis Committee",
        "mandate": "It has already started. There is no roll call.",
        "epigraph": "A wise and prudent prince should have both his own arms and "
                    "the loyalty of his subjects.",
        "source": "The Prince, VI",
    },
]

# --- the folio sections ----------------------------------------------------

INTRO = (
    "Two days. Eight committees. Delegates seated, gavel down, and the "
    "business of the world put to the question."
)

# Provisional shape of the two days. Exact gavel times ride with the brochure,
# so leave the times as None and the build prints a rule instead.
PROGRAMME = [
    ("Day One", "6 November", [
        ("Registration and Credentials", "committee rooms"),
        ("Opening Plenary", "great hall"),
        ("Committee Session I", "all committees"),
        ("Gaffer's Caucus", "committee rooms"),
        ("Committee Session II", "all committees"),
        ("Reports Drafted", "secretariat"),
    ]),
    ("Day Two", "7 November", [
        ("Committee Session III", "all committees"),
        ("Gaffer's Caucus", "committee rooms"),
        ("Final Committee Session", "all committees"),
        ("Closing Plenary", "great hall"),
    ]),
]

DELEGATION = (
    "Countries are allotted by the matrix, not by preference alone. Each "
    "delegation receives its allocation when registrations open."
)

RULES = [
    ("The gavel", "The chair recognises, the chair rules. A point of "
                  "procedural order is made in the form the chair has given."),
    ("Debate", "Speeches are timed and cut off. Interventions are made from "
               "the floor between recognitions."),
    ("The caucus", "Consultation in caucus is where the actual work of a "
                   "resolution is done, and it is done in smaller numbers."),
    ("Points", "Scored on clarity of position, drafting, and conduct. Not on "
               "speaking longest."),
    ("Decorum", "Doors close. Phones down. Decorum is a scored category."),
]

# --- pages still sealed ----------------------------------------------------
#
# Each of these exists as a real page so the link in the nav never 404s, and
# each carries the seal rather than an empty space.

SEALED = [
    {
        "slug": "secretariat",
        "title": "The Secretariat",
        "note": "Names, roles, and the people actually running the gavel. "
                "Being composed now.",
    },
    {
        "slug": "chairs",
        "title": "The Chairs",
        "note": "Who will preside over each committee, and what they will "
                "rule on. Being appointed.",
    },
    {
        "slug": "brochure",
        "title": "Brochure",
        "note": "The full programme, committee mandates, topics and rules, in "
                "one document. At the printers.",
    },
    {
        "slug": "registrations",
        "title": "Registrations",
        "note": "Delegate applications, the fee, and the closing date. "
                "Opening soon.",
    },
    {
        "slug": "country-matrix",
        "title": "Country Matrix",
        "note": "Which delegation receives which permanent seat, and by what "
                "rule. Revealing soon.",
    },
]