"""Polish host lines: numbers, dates, years and units read the way a Polish host says them.

    python test_polish.py

Covers buzz_polish.say_numbers (what the voice is given) and the speech check's word comparison
for Polish (buzz_tts_verify.wer), where a transcript written with digits must still match.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import buzz_polish  # noqa: E402
import buzz_tts_verify  # noqa: E402

CARDINAL = [(0, "zero"), (7, "siedem"), (12, "dwanaście"), (21, "dwadzieścia jeden"),
            (100, "sto"), (215, "dwieście piętnaście"), (1000, "tysiąc"), (1966, "tysiąc dziewięćset sześćdziesiąt sześć"),
            (2000, "dwa tysiące"), (5000, "pięć tysięcy"), (12000, "dwanaście tysięcy"),
            (22000, "dwadzieścia dwa tysiące"), (1000000, "milion"), (3500000, "trzy miliony pięćset tysięcy")]

ORDINAL = [((1, "nom"), "pierwszy"), ((2, "gen"), "drugiego"), ((3, "loc"), "trzecim"),
           ((1966, "loc"), "tysiąc dziewięćset sześćdziesiątym szóstym"),
           ((1410, "gen"), "tysiąc czterysta dziesiątego"), ((966, "loc"), "dziewięćset sześćdziesiątym szóstym"),
           ((1900, "nom"), "tysiąc dziewięćsetny"), ((2000, "loc"), "dwutysięcznym"),
           ((2001, "gen"), "dwa tysiące pierwszego"), ((80, "loc_pl"), "osiemdziesiątych"), ((60, "nom_pl"), "sześćdziesiąte")]

SAY = [
    ("year, locative", "Kto wygrał mundial w 1966 roku?", "Kto wygrał mundial w tysiąc dziewięćset sześćdziesiątym szóstym roku?"),
    ("year, abbreviation", "Co się stało w 966 r.?", "Co się stało w dziewięćset sześćdziesiątym szóstym roku?"),
    ("year, genitive", "Od 1918 roku Polska jest wolna", "Od tysiąc dziewięćset osiemnastego roku Polska jest wolna"),
    ("w roku N", "W roku 2000 nic", "W roku dwutysięcznym nic"),
    ("date", "Co świętujemy 3 maja?", "Co świętujemy trzeciego maja?"),
    ("date with year", "Bitwa 15 lipca 1410 roku", "Bitwa piętnastego lipca tysiąc czterysta dziesiątego roku"),
    ("century, locative", "Kto żył w XIX wieku?", "Kto żył w dziewiętnastym wieku?"),
    ("century, abbreviation", "Malarz z XVII w.", "Malarz z siedemnastego wieku"),
    ("two centuries", "Na przełomie XIX i XX wieku", "Na przełomie dziewiętnastego i dwudziestego wieku"),
    ("century pair, slash", "Żył na przełomie XV/XVI w.", "Żył na przełomie piętnastego - szesnastego wieku"),
    ("century pair, dash", "Gotyk to XII-XV wiek", "Gotyk to dwunasty - piętnasty wiek"),
    ("not a century", "Formularz o płci i wieku", "Formularz o płci i wieku"),
    ("decade", "Hit z lat 80.", "Hit z lat osiemdziesiątych"),
    ("decade, locative", "W latach 90. grał", "W latach dziewięćdziesiątych grał"),
    ("unit plural 2-4", "Ma 3 km", "Ma trzy kilometry"),
    ("unit plural 5+", "Ma 25 km długości", "Ma dwadzieścia pięć kilometrów długości"),
    ("unit, thousands", "Ma 11 000 km", "Ma jedenaście tysięcy kilometrów"),
    ("percent", "Około 70% powierzchni", "Około siedemdziesiąt procent powierzchni"),
    ("decimal", "Ile to 3,14?", "Ile to trzy przecinek czternaście?"),
    ("decimal percent", "Wzrost o 2,5%", "Wzrost o dwa przecinek pięć procenta"),
    ("temperature", "Woda wrze w 100°C", "Woda wrze w sto stopni Celsjusza"),
    ("plain number", "Ile nóg ma 8 pająków?", "Ile nóg ma osiem pająków?"),
    ("not a unit", "Urodził się 5 marca", "Urodził się piątego marca"),
    ("abbreviation", "Np. Wisła, Odra itd.", "na przykład Wisła, Odra i tak dalej"),
    ("range", "Wojna 1939-1945", "Wojna tysiąc dziewięćset trzydzieści dziewięć - tysiąc dziewięćset czterdzieści pięć"),
    ("no numbers", "Która rzeka płynie przez Kraków?", "Która rzeka płynie przez Kraków?"),
]

# (spoken line given to the voice, what the recogniser wrote, expected word error rate)
WER = [
    ("Kto wygrał mundial w tysiąc dziewięćset sześćdziesiątym szóstym roku?",
     "Kto wygrał mundial w 1966 roku?", 0.0),
    ("Co świętujemy trzeciego maja?", "Co świętujemy 3 maja?", 0.0),
    ("Która rzeka płynie przez Kraków?", "która rzeka płynie przez kraków", 0.0),
    ("Która rzeka płynie przez Kraków?", "która rzeka płynie przez", 0.2),
]


def main():
    bad = 0

    def check(name, got, want):
        nonlocal bad
        ok = got == want
        bad += not ok
        print("  %-24s %-5s %s%s" % (name, "ok" if ok else "FAIL", got, "" if ok else "\n%37s %s" % ("want", want)))

    print("cardinal():")
    for n, want in CARDINAL:
        check(str(n), buzz_polish.cardinal(n), want)
    print("\nordinal():")
    for (n, case), want in ORDINAL:
        check("%d %s" % (n, case), buzz_polish.ordinal(n, case), want)
    print("\nsay_numbers():")
    for name, src, want in SAY:
        check(name, buzz_polish.say_numbers(src), want)
    print("\nspeech check (wer, pl):")
    for ref, heard, want in WER:
        check(heard, round(buzz_tts_verify.wer(ref, heard, "pl"), 3), want)

    print("\n%s (%d failure%s)" % ("PASS" if not bad else "FAIL", bad, "" if bad == 1 else "s"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
