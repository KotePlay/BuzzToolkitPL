# Instrukcja dla AI: pytania do polskiej paczki Buzz! Quiz World

## Dla Ciebie (człowieka)

1. Otwórz nowy czat z dowolnym AI.
2. Wklej całą sekcję **„Instrukcja dla AI”** poniżej (od nagłówka do końca pliku) albo załącz ten plik.
3. Dopisz pod spodem swoje zamówienie, np.:
   *„Temat: historia Polski. 100 pytań, mieszanka łatwych, średnich i trudnych.”*
4. Gotowy wynik AI wklej do Notatnika i zapisz jako np. `historia.txt` (kodowanie **UTF-8**,
   domyślne w Notatniku).
5. W Buzz Pack Studio: paczka z językiem **Polish (POL)** → krok **2 Questions** → przeciągnij plik
   na pole „Drop quiz files here” → **Import**. Studio pokaże, ile pytań przyjęło, a które
   odrzuciło i dlaczego.
6. **Sprawdź fakty.** AI potrafi się mylić z pełnym przekonaniem - przejrzyj odpowiedzi, zanim
   zagrasz ze znajomymi.

---

## Instrukcja dla AI

Przygotujesz pytania quizowe do gry **Buzz! Quiz World** (PlayStation 3) w języku polskim. Plik
zostanie wczytany automatycznie przez program, a potem pytania będą wyświetlane w grze i
**czytane na głos przez syntezator mowy** (głos prowadzącego). Trzymaj się ściśle poniższych zasad -
pytanie, które ich nie spełnia, zostanie odrzucone albo źle przeczytane.

### 1. Format pliku (dokładnie taki)

Zwykły tekst. Każde pytanie to blok: linia `Q:` z pytaniem, linia `A:` z **poprawną** odpowiedzią i
**dokładnie trzy** linie `- ` z odpowiedziami błędnymi. Bloki oddzielaj pustą linią.

```
Q: Która rzeka przepływa przez Kraków?
A: Wisła
- Odra
- Warta
- Bug

Q: W którym roku odbyła się bitwa pod Grunwaldem?
A: 1410
- 1385
- 1525
- 1569
```

- Pisz `Q:`, `A:` i `- ` dokładnie tak (z dwukropkiem/myślnikiem i spacją), każdą rzecz w osobnej linii.
- Poprawna odpowiedź jest **zawsze** w linii `A:` - gra sama tasuje kolejność odpowiedzi.
- Żadnej numeracji pytań, nagłówków, komentarzy, pogrubień, list Markdown ani tekstu przed i po
  pytaniach. Oddaj **wyłącznie** bloki pytań (najlepiej w jednym bloku kodu, żeby łatwo było
  skopiować).

### 2. Twarde limity (przekroczenie = pytanie odrzucone)

| Co | Limit |
|---|---|
| Pytanie | **maks. 93 znaki** łącznie ze spacjami i znakami interpunkcyjnymi |
| Każda odpowiedź | **maks. 30 znaków** łącznie ze spacjami |
| Odpowiedzi w pytaniu | dokładnie **4** (1 poprawna + 3 błędne), **wszystkie różne** (wielkość liter się nie liczy) |
| Pytania w pliku | każde inne - bez powtórek i bez pytań różniących się tylko szykiem słów |

Policz znaki przy dłuższych pytaniach. Lepiej krócej: gra wyświetla pytanie w kilku linijkach.

### 3. Ile pytań

- **Minimum 60**, a najlepiej **80-150** w jednej paczce. Paczka ma 60 miejsc na pytania; przy
  mniejszej liczbie pytania będą się powtarzać, a kilka rund (Pass the Bomb, Pie Fight, Over the
  Edge, Boiling Point, Final Countdown) potrzebuje co najmniej 30 pytań.
- Mieszaj trudność: ok. 40% łatwych, 40% średnich, 20% trudnych.

### 4. Znaki

- Polskie litery (ą ć ę ł ń ó ś ź ż) - **tak**, normalnie.
- Gra wyświetla wszystko WIELKIMI LITERAMI, więc nie opieraj niczego na wielkości liter
  (np. „pH” i „PH” wyglądają tak samo).
- **Nie używaj:** emoji, symboli (€ ™ © → ← ★ ♪ itp.), liter z innych alfabetów (ř, ğ, ß, cyrylica,
  greka), indeksów (H₂O → pisz „H2O”).
- Cudzysłowy „” i myślniki – — są dozwolone (program zamieni je na proste odpowiedniki).

### 5. Pytanie będzie czytane na głos - pisz tak, jak się mówi

Syntezator czyta **tylko pytanie** (odpowiedzi są tylko na ekranie). Dlatego pytanie:

- To **pełne, naturalne zdanie** po polsku, zakończone znakiem zapytania.
- **Bez nawiasów, ukośników i skrótów-zagadek** w rodzaju „(ok.)”, „i/lub”, „ww.”, „r.”, „wg”, „tzw.”.
  Dozwolone skróty (program je rozwinie): np., itd., itp., m.in., tzn., tj., ok., nr, prof., dr.
- **Liczby** - program sam zamienia je na słowa we właściwej formie, ale tylko w tych układach:
  - rok z „roku”: „w 1966 roku”, „od 1918 roku”, „w roku 2004” (nie samo „w 1966”);
  - data: „3 maja”, „15 lipca 1410 roku”;
  - wiek rzymską liczbą z „wieku/wiek/w.”: „w XIX wieku”, „XVII w.”, „na przełomie XIX i XX wieku”;
  - dekada: „w latach 80.”, „z lat 90.”;
  - jednostki zaraz po liczbie: km, m, cm, mm, kg, %, °C, zł („25 km”, „70%”, „100°C”);
  - ułamki z przecinkiem: „3,14”.
  W innych sytuacjach, gdy liczba musi się odmienić (np. „ilu”, „około”, „po”, „z”), **napisz ją
  słowami we właściwej formie**: „Ilu zawodników liczy drużyna siatkówki?” zamiast „…6 zawodników…”;
  „około dwóch tysięcy” zamiast „około 2000”.
- **Obce nazwy:** jeśli istnieje spolszczona forma, użyj jej („Szekspir”, „Waszyngton”, „Paryż”) i
  unikaj długich obcojęzycznych tytułów w pytaniu. Jeśli obca nazwa jest konieczna, wstaw ją
  raczej do odpowiedzi (odpowiedzi nie są czytane).
- **Bez symboli matematycznych** w pytaniu (+ − × ÷ = < >). Pisz słowami: „Ile to jest siedem razy
  osiem?”.

### 6. Jakość pytań

- **Jedna jednoznacznie poprawna odpowiedź.** Żadna z błędnych nie może być „też trochę dobra”.
- Błędne odpowiedzi **wiarygodne i z tej samej kategorii** (jeśli poprawna to rok - wszystkie to
  lata z podobnego okresu; jeśli miasto - wszystkie to miasta). Podobna długość i forma
  gramatyczna jak poprawna.
- Pytanie **nie zdradza odpowiedzi** (żadnych słów z poprawnej odpowiedzi w treści pytania).
- **Tylko sprawdzone fakty**, które się nie zmieniają. Unikaj „obecny prezes / aktualny mistrz /
  najnowszy” i rzeczy spornych. Jeśli nie jesteś pewien faktu - pomiń to pytanie.
- Bez „Która z poniższych…”, „Żadna z powyższych”, „Wszystkie odpowiedzi są poprawne” - odpowiedzi
  są wyświetlane osobno i w losowej kolejności.
- Różnorodność: nie zaczynaj kolejnych pytań tak samo, nie powtarzaj tych samych odpowiedzi w wielu
  pytaniach.

### 7. Kontrola przed oddaniem

Zanim oddasz wynik, sprawdź każde pytanie:

1. Blok ma `Q:`, `A:` i dokładnie trzy linie `- `.
2. Pytanie ≤ 93 znaki, każda odpowiedź ≤ 30 znaków.
3. Cztery odpowiedzi są różne.
4. Poprawna odpowiedź jest w `A:` i jest naprawdę poprawna.
5. Pytanie czyta się na głos naturalnie (liczby zgodnie z punktem 5, bez nawiasów i symboli).
6. Brak powtórzonych pytań w całym pliku.

Pytania, które nie przechodzą kontroli, popraw albo usuń. Oddaj tylko bloki pytań.
