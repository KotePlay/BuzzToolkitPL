"""Polish text as the host should say it: numbers, dates, years, centuries and units in words.

    say_numbers("W 1966 roku, 1 maja.")   -> "W tysiąc dziewięćset sześćdziesiątym szóstym roku,
                                              pierwszego maja."

The multilingual voice model reads digits badly or in English, and Polish numbers change form
with their context ("w 1966 roku" is an ordinal in the locative, "1 maja" an ordinal in the
genitive, "5 km" needs the plural that agrees with five). This covers the forms quiz questions
actually use; anything else falls back to the plain cardinal, and a pack can still give an exact
spoken line with "say".

Used on both sides of the speech check (buzz_tts_verify), so a line the recogniser writes with
digits compares equal to the same line spoken in words.
"""
import re

_ONES = ["zero", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć"]
_TEENS = ["dziesięć", "jedenaście", "dwanaście", "trzynaście", "czternaście", "piętnaście",
          "szesnaście", "siedemnaście", "osiemnaście", "dziewiętnaście"]
_TENS = ["", "", "dwadzieścia", "trzydzieści", "czterdzieści", "pięćdziesiąt", "sześćdziesiąt",
         "siedemdziesiąt", "osiemdziesiąt", "dziewięćdziesiąt"]
_HUNDREDS = ["", "sto", "dwieście", "trzysta", "czterysta", "pięćset", "sześćset", "siedemset",
             "osiemset", "dziewięćset"]
_BIG = [(10 ** 6, ("milion", "miliony", "milionów")), (1000, ("tysiąc", "tysiące", "tysięcy"))]

# ordinals, masculine nominative singular; other forms come from _inflect
_O_ONES = ["", "pierwszy", "drugi", "trzeci", "czwarty", "piąty", "szósty", "siódmy", "ósmy",
           "dziewiąty"]
_O_TEENS = ["dziesiąty", "jedenasty", "dwunasty", "trzynasty", "czternasty", "piętnasty",
            "szesnasty", "siedemnasty", "osiemnasty", "dziewiętnasty"]
_O_TENS = ["", "", "dwudziesty", "trzydziesty", "czterdziesty", "pięćdziesiąty", "sześćdziesiąty",
           "siedemdziesiąty", "osiemdziesiąty", "dziewięćdziesiąty"]
_O_HUNDREDS = ["", "setny", "dwusetny", "trzechsetny", "czterechsetny", "pięćsetny", "sześćsetny",
               "siedemsetny", "osiemsetny", "dziewięćsetny"]
_O_THOUSANDS = ["", "", "dwu", "trzy", "cztero", "pięcio", "sześcio", "siedmio", "ośmio",
                "dziewięcio"]

_MONTHS = ("stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia",
           "września", "października", "listopada", "grudnia")

# unit after a number: (1, 2-4, 5+, fractions)
_UNITS = {"%": ("procent", "procent", "procent", "procenta"),
          "km": ("kilometr", "kilometry", "kilometrów", "kilometra"),
          "m": ("metr", "metry", "metrów", "metra"),
          "cm": ("centymetr", "centymetry", "centymetrów", "centymetra"),
          "mm": ("milimetr", "milimetry", "milimetrów", "milimetra"),
          "kg": ("kilogram", "kilogramy", "kilogramów", "kilograma"),
          "zł": ("złoty", "złote", "złotych", "złotego"),
          "°c": ("stopień Celsjusza", "stopnie Celsjusza", "stopni Celsjusza", "stopnia Celsjusza")}

_ABBREV = [("m.in.", "między innymi"), ("np.", "na przykład"), ("itd.", "i tak dalej"),
           ("itp.", "i tym podobne"), ("tzn.", "to znaczy"), ("tj.", "to jest"), ("ok.", "około"),
           ("nr", "numer"), ("prof.", "profesor"), ("dr", "doktor")]


def _below_1000(n):
    out = [_HUNDREDS[n // 100]]
    r = n % 100
    if 10 <= r < 20:
        out.append(_TEENS[r - 10])
    else:
        out += [_TENS[r // 10], _ONES[r % 10] if r % 10 else ""]
    return " ".join(w for w in out if w)


def plural(n):
    """Index of the Polish plural form for n: 0 = one, 1 = 2-4 (not 12-14), 2 = many."""
    if n == 1:
        return 0
    return 1 if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else 2


def cardinal(n):
    if n == 0:
        return "zero"
    if n >= 10 ** 9:
        return str(n)
    parts = []
    for value, forms in _BIG:
        k, n = divmod(n, value)
        if k:
            parts += [forms[0]] if k == 1 else [_below_1000(k), forms[plural(k)]]
    if n:
        parts.append(_below_1000(n))
    return " ".join(parts)


def _inflect(word, case):
    """Masculine ordinal adjective from the nominative singular to `case`. Hard stems end in -y
    (pierwszy -> pierwszego, pierwszym, pierwsze, pierwszych), soft ones in -i (drugi -> drugiego,
    drugim, drugie, drugich)."""
    hard = word.endswith("y")
    stem = word[:-1] if hard else word
    return {"nom": word, "gen": stem + "ego", "loc": word + "m", "nom_pl": stem + "e",
            "gen_pl": stem + ("ych" if hard else "ch"), "loc_pl": stem + ("ych" if hard else "ch")}[case]


def ordinal(n, case="nom"):
    """Ordinal in words; in a compound only the last components change form, as Polish does
    ("tysiąc dziewięćset sześćdziesiąty szósty", "dwa tysiące pierwszy", "dwutysięczny")."""
    if not 0 < n < 10000:
        return cardinal(n)
    r = n % 100
    if r:
        head = n - r
        if 10 <= r < 20:
            tail = [_O_TEENS[r - 10]]
        else:
            tail = [w for w in (_O_TENS[r // 10], _O_ONES[r % 10]) if w]
    elif n % 1000:
        head, tail = n - n % 1000, [_O_HUNDREDS[n % 1000 // 100]]
    else:
        head, tail = 0, [_O_THOUSANDS[n // 1000] + "tysięczny"]
    return " ".join(([cardinal(head)] if head else []) + [_inflect(w, case) for w in tail])


_ROMAN = re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")


def roman(s):
    """Value of a Roman numeral, or None if `s` is not one."""
    s = s.upper()
    if not s or not _ROMAN.match(s):
        return None
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for a, b in zip(s, s[1:] + " "):
        v = vals[a]
        total += -v if b != " " and vals[b] > v else v
    return total


def _fraction(digits):
    """Digits after the decimal comma: leading zeros are read one by one ("05" -> "zero pięć")."""
    zeros = len(digits) - len(digits.lstrip("0"))
    rest = digits[zeros:]
    return " ".join(["zero"] * zeros + ([cardinal(int(rest))] if rest else []))


def _number(s):
    """'1 000' / '1966' / '3,14' -> words (cardinal)."""
    s = s.replace(" ", "")
    if "," in s:
        a, b = s.split(",", 1)
        return cardinal(int(a)) + " przecinek " + _fraction(b)
    return cardinal(int(s))


_W = r"(?<![\w])"             # word start that also works before digits
_E = r"(?![\w])"              # word end
_NUM = r"\d{1,3}(?: \d{3})+(?:,\d+)?|\d+(?:,\d+)?"      # "1 000 000", "1966", "3,14"


def say_numbers(text):
    s = text
    I = re.IGNORECASE

    # number + unit ("5 km", "3,5%", "20°C")
    def unit(m):
        num, u = m.group(1), m.group(2).lower()
        forms = _UNITS[u]
        if "," in num:
            return _number(num) + " " + forms[3]
        return _number(num) + " " + forms[plural(int(num.replace(" ", "")))]
    s = re.sub(_W + r"(" + _NUM + r")\s*(%|km|cm|mm|kg|m|zł|°c)(?![^\W\d_])", unit, s, flags=I)

    # dates: "1 maja [1966 [roku|r.]]"
    def date(m):
        out = ordinal(int(m.group(1)), "gen") + " " + m.group(2)
        if m.group(3):
            out += " " + ordinal(int(m.group(3)), "gen")
            if m.group(4):
                out += " roku"
        return out
    s = re.sub(_W + r"(\d{1,2})\s+(%s)(?:\s+(\d{3,4})(\s+(?:roku" % "|".join(_MONTHS) + _E + r"|r\.))?)?" + _E,
               date, s, flags=I)

    # years: "w 1966 roku", "w roku 1966", "od 1966 r.", "roku 1966"
    s = re.sub(_W + r"(w|we)\s+(\d{3,4})\s+(?:roku" + _E + r"|r\.)",
               lambda m: m.group(1) + " " + ordinal(int(m.group(2)), "loc") + " roku", s, flags=I)
    s = re.sub(_W + r"(w|we)\s+roku\s+(\d{3,4})" + _E,
               lambda m: m.group(1) + " roku " + ordinal(int(m.group(2)), "loc"), s, flags=I)
    s = re.sub(_W + r"(\d{3,4})\s+(?:roku" + _E + r"|r\.)",
               lambda m: ordinal(int(m.group(1)), "gen") + " roku", s, flags=I)
    s = re.sub(_W + r"(roku)\s+(\d{3,4})" + _E,
               lambda m: m.group(1) + " " + ordinal(int(m.group(2)), "gen"), s, flags=I)

    # decades: "w latach 80.", "lata 60-te", "z lat 90."
    def decade(m):
        case = {"ach": "loc_pl", "a": "nom_pl"}.get((m.group(2) or "").lower(), "gen_pl")
        return "lat" + (m.group(2) or "") + " " + ordinal(int(m.group(3)), case)
    s = re.sub(_W + r"(lat(ach|a)?)\s+([2-9]0)(?:\.|-?tych|-?te)", decade, s, flags=I)
    s = re.sub(_W + r"(lat(ach))\s+([2-9]0)" + _E, decade, s, flags=I)

    # centuries: "w XX wieku", "XIX w.", "na przełomie XIX i XX wieku"
    def century(m):
        prep, r1, r2, word = m.group(1), m.group(2), m.group(3), m.group(4).lower()
        vals = [roman(r) for r in (r1, r2) if r]
        if None in vals or not all(1 <= v <= 30 for v in vals) or (vals[0] == 1 and not prep and not r2):
            return m.group(0)                  # "i wieku" is "and age", not "1st century"
        case = "nom" if word == "wiek" else ("loc" if prep else "gen")
        said = " i ".join(ordinal(v, case) for v in vals) + (" wiek" if word == "wiek" else " wieku")
        return (prep + " " if prep else "") + said
    s = re.sub(_W + r"(?:(w|we)\s+)?([ivxlcdm]+)(?:\s+i\s+([ivxlcdm]+))?\s+(wieku|wiek|w\.)" + r"(?![^\W\d_])",
               century, s, flags=I)

    # ranges "1939-1945": read with a pause
    s = re.sub(r"(\d)\s*[-–]\s*(\d)", r"\1 - \2", s)
    # everything else: thousands separated by spaces, decimal comma, plain integers
    s = re.sub(_W + "(?:" + _NUM + ")" + _E, lambda m: _number(m.group(0)), s)

    for short, full in _ABBREV:
        s = re.sub(_W + re.escape(short) + (_E if not short.endswith(".") else ""), full, s, flags=I)
    return re.sub(r"\s+", " ", s).strip()
