# Buzz! Quiz World po polsku – własne paczki pytań z polskim prowadzącym

> Ten projekt to fork **[Handylemons/BuzzToolkit](https://github.com/Handylemons/BuzzToolkit)** –
> cała baza (generator paczek, szyfrowanie, trener głosu, serwer, Buzz Pack Studio) to praca
> Handylemons. Ten fork dodaje do niej polską wersję.

Ta instrukcja prowadzi krok po kroku od zera do zagrania we własną paczkę pytań, w której
**pytania czyta głos polskiego prowadzącego z gry**, wytrenowany na Twoim komputerze z Twojej
kopii płyty. Opisuje dokładnie tę drogę, którą przeszliśmy, razem z pułapkami, na które po drodze
trafiliśmy – żebyś Ty już nie musiał.

Całość zajmuje jedno popołudnie, z czego większość to czekanie: instalacja i trening głosu idą
same, a Ty tylko patrzysz na postęp.

---

## Spis treści

1. [Czego potrzebujesz](#1-czego-potrzebujesz)
2. [Gra w RPCS3 po polsku](#2-gra-w-rpcs3-po-polsku)
3. [Python 3.11](#3-python-311)
4. [Pobranie toolkitu](#4-pobranie-toolkitu)
5. [Instalacja (Install.bat)](#5-instalacja-installbat)
6. [Pierwsze uruchomienie Buzz Pack Studio](#6-pierwsze-uruchomienie-buzz-pack-studio)
7. [Trening polskiego głosu](#7-trening-polskiego-głosu)
8. [Pierwsza paczka pytań](#8-pierwsza-paczka-pytań)
9. [Poprawianie wymowy](#9-poprawianie-wymowy)
10. [Gdy coś nie działa](#10-gdy-coś-nie-działa)
11. [Najczęstsze pytania](#11-najczęstsze-pytania)

---

## 1. Czego potrzebujesz

| Co | Uwagi |
|---|---|
| **Komputer z Windows 10 lub 11** | |
| **Karta graficzna NVIDIA, min. 8 GB pamięci** | Sprawdzone na GTX 1070 Ti (8 GB). Starsze i mniejsze karty działają, tylko wolniej – toolkit sam się do nich dopasowuje. Bez karty NVIDIA paczki da się robić, ale **bez głosu**. |
| **Własna polska płyta Buzz! Quiz World – `BCES00647`** | Wydanie europejskie (Pl, Ru, El, Hr, Cs), wersja 1.00 wystarczy. Tylko na tej płycie jest polski prowadzący. Toolkit nie zawiera żadnych plików gry – wszystko czyta z Twojej kopii. |
| **RPCS3** (emulator PS3) | https://rpcs3.net |
| **Wolne miejsce na dysku** | Łącznie ok. **30 GB**, z czego **co najmniej 10 GB na dysku C:** (tam trafiają pobierane modele). Za mało miejsca na C: potrafi zamrozić cały komputer w trakcie treningu – sprawdź to przed startem. |
| **Internet** | Instalacja i pierwszy trening pobierają łącznie ok. 12 GB. Konta nigdzie nie trzeba zakładać. |
| **Git** (zalecany) | https://git-scm.com – ułatwia pobranie i aktualizowanie toolkitu. Da się bez niego (ZIP), ale z nim jest prościej. |

---

## 2. Gra w RPCS3 po polsku

1. **Zrób kopię swojej płyty.** Najprościej: PS3 z HEN/CFW i menedżer plików (multiMAN, webMAN),
   albo komputerowy napęd Blu-ray i program **PS3 Disc Dumper** (opis w przewodniku RPCS3,
   *Quickstart → Dumping games*). Dostaniesz folder z podfolderem `PS3_GAME`.
   Jeśli masz plik `.iso`, wypakuj go 7-Zipem (prawy przycisk → *7-Zip → Wypakuj do…*).
2. **Ustaw polski w RPCS3:** *Configuration → System → Console Language → Polish*.
3. **Dodaj grę do RPCS3** (*File → Add Games*) i uruchom ją. Menu powinno być po polsku.
4. **Odszyfruj plik EBOOT** (toolkit czyta z niego klucz do szyfrowania paczek):
   w RPCS3 *Utilities → Decrypt PS3 Binaries* → wskaż plik
   `…\PS3_GAME\USRDIR\EBOOT.BIN`. Obok pojawi się **`EBOOT.elf`**.

> **Nie instaluj żadnej aktualizacji gry.** Na polskiej płycie w wersji 1.00 wszystko działa bez
> niej – Studio pokaże *No game update needed*.

---

## 3. Python 3.11

Głos działa **tylko na Pythonie 3.11** – nawet jeśli masz już nowszego (np. 3.13). Obie wersje
mogą być zainstalowane jednocześnie i sobie nie przeszkadzają.

1. Pobierz **Python 3.11.9**: https://www.python.org/downloads/release/python-3119/
   (sekcja *Files* → **Windows installer (64-bit)**).
2. W instalatorze zaznacz **Add python.exe to PATH** oraz **Use admin privileges when installing
   py.exe**, potem **Install Now**.
3. Sprawdź w PowerShellu (menu Start → wpisz *PowerShell*):
   ```
   py -3.11 --version
   ```
   Ma pokazać `Python 3.11.9`. To, że `python --version` pokazuje inną wersję, nie szkodzi.

---

## 4. Pobranie toolkitu

Wybierz folder **poza OneDrive** i z dużą ilością miejsca, np. `H:\Buzz`.

**Z Gitem (zalecane):**
```
cd H:\Buzz
git clone https://github.com/KotePlay/BuzzToolkitPL.git
cd BuzzToolkitPL
```

**Bez Gita:** otwórz https://github.com/KotePlay/BuzzToolkitPL → **Code → Download ZIP** →
wypakuj.

---

## 5. Instalacja (Install.bat)

1. W folderze toolkitu uruchom **`Install.bat`** (dwuklik). Jeśli Windows pokaże „System Windows
   ochronił ten komputer”: *Więcej informacji → Uruchom mimo to*.
2. Na pytanie **„Install the host voice? [Y/N]”** odpowiedz **Y**. Pobierze się ok. 6 GB – to
   chwilę potrwa.
3. Na końcu zobaczysz *„Setup finished”*.

Jeśli instalator napisze, że potrzebuje Pythona 3.11 – wróć do kroku 3.

---

## 6. Pierwsze uruchomienie Buzz Pack Studio

1. Uruchom **`Start Buzz Pack Studio.bat`**. Otworzy się przeglądarka z aplikacją
   (`http://127.0.0.1:8765`). **Czarnego okna nie zamykaj** – to ono jest aplikacją.
2. W ramce **Setup** po lewej:
   - **RPCS3 folder:** wklej ścieżkę folderu z `rpcs3.exe` (w Eksploratorze kliknij pasek adresu,
     Ctrl+C) → **Save folder**. Pojawi się zielona etykieta *Buzz!: Quiz World (Pl, Ru, El, Hr, Cs)*.
   - **Your decrypted EBOOT (.elf):** wklej ścieżkę folderu, w którym leży `EBOOT.elf`, np.
     ```
     H:\Gry\Buzz! Quiz World (Europe) (Pl,Ru,El,Hr,Cs)\PS3_GAME\USRDIR
     ```
     (bez cudzysłowów) → **Read game keys**. Pole zniknie, a pojawi się zielone
     *Game keys read from your EBOOT*. To robisz tylko raz.
   - Niżej zobaczysz *No game update needed* i *Pack Game plays the game's own round order* – tak
     ma być, na polskiej płycie nic więcej nie trzeba ustawiać.

Studio możesz teraz zamknąć – do treningu nie jest potrzebne.

---

## 7. Trening polskiego głosu

Program uczy się głosu polskiego prowadzącego ze wszystkich jego nagrań na płycie (ok. 11,5 tys.
nagrań, z czego do nauki zostaje ok. 7 godzin czystego głosu). Robisz to raz.

### Przygotowanie – to naprawdę ma znaczenie

- **Zamknij VS Code, przeglądarki, Discorda, Steama i gry.** Każdy z tych programów zajmuje pamięć
  karty graficznej. Trening uruchomiony w terminalu VS Code potrafi zamrozić VS Code, a razem z nim
  przerwać trening.
- **Wyłącz usypianie:** *Ustawienia → System → Zasilanie → Uśpij: Nigdy*. Uśpiony komputer
  wstrzymuje trening.
- **Sprawdź miejsce na dysku C:** – co najmniej 10 GB wolnego.

### Uruchomienie

Otwórz **zwykłe okno PowerShella** (menu Start → *PowerShell*) i wpisz (ścieżki zmień na swoje):
```
cd H:\Buzz\BuzzToolkitPL
.\tools\clone_venv\Scripts\python.exe -m voice_trainer.run --disc "H:\Gry\Buzz! Quiz World (Europe) (Pl,Ru,El,Hr,Cs)" --work "H:\buzz_trening_pl" --lang POL
```
- `--disc` to folder, w którym leży `PS3_GAME` (bez `\PS3_GAME\USRDIR` na końcu).
- `--work` to folder roboczy na ok. 3 GB plików treningu – utworzy się sam.
- Cudzysłowy są potrzebne (spacje, nawiasy i wykrzyknik w nazwie).

### Co zobaczysz i ile to trwa

Czasy z GTX 1070 Ti (8 GB):

| Etap | Co widać | Czas |
|---|---|---|
| `=== 1 corpus` | znalezione pliki płyty, liczniki `400/...` | kilka minut |
| `=== 2 features` | pobieranie modelu (ok. 3 GB, tylko raz), potem liczniki `500/11539` | do ok. godziny |
| `=== 3 s3gen` | linia z nazwą karty, np. `GTX 1070 Ti, fp32: 600 speech tokens x 4 micro-batches per step`, potem `step 50 … step 1500` | ok. 30 min |
| `=== 4 t3` | `step 50 … step 500` | ok. 20 min |
| `exported …\voice_models\buzz_host_POL` | **głos gotowy** | chwila |
| `=== 6 evaluate` | pobranie Whispera (1,5 GB, tylko raz), dwie linie z wynikami | 10–20 min |

Żółte ostrzeżenia (`symlinks`, `HF_TOKEN`, `FutureWarning`, `deprecated`) są nieszkodliwe –
ignoruj je.

### Koniec i wynik

Trening skończył się, gdy wróci znak zachęty `PS H:\…>`, a przed nim są dwie linie, np.:
```
{"label": "base",    "speaker_sim": 0.9707, "real_ceiling": 0.9776, "wer": 0.1087, "n": 12}
{"label": "trained", "speaker_sim": 0.9788, "real_ceiling": 0.9776, "wer": 0.0524, "n": 12}
```
- `speaker_sim` – podobieństwo do prawdziwego prowadzącego (wyżej = lepiej; `real_ceiling` to
  wynik jego własnych nagrań).
- `wer` – odsetek źle wypowiedzianych słów (niżej = lepiej).

Powyżej jest nasz wynik: głos po treningu brzmi dla komputera tak samo jak prawdziwy prowadzący,
a błędów jest o połowę mniej niż przed treningiem. Posłuchaj sam: próbki przed treningiem są w
`H:\buzz_trening_pl\eval\base\`, po treningu w `H:\buzz_trening_pl\eval\trained\`.

Studio pokaże teraz w Setup: **Host voices: POL (trained)**.

---

## 8. Pierwsza paczka pytań

### Pytania

Najwygodniej poprosić AI o plik z pytaniami. Gotowa instrukcja dla AI jest w
[`examples/INSTRUKCJA_PYTANIA_DLA_AI.md`](examples/INSTRUKCJA_PYTANIA_DLA_AI.md) – wklej ją do
czatu z dowolnym AI, dopisz temat i liczbę pytań (najlepiej 80–150), a wynik zapisz w Notatniku
jako `.txt` (kodowanie UTF-8). Format wygląda tak:
```
Q: Która rzeka przepływa przez Kraków?
A: Wisła
- Odra
- Warta
- Bug
```
Pytanie maks. 93 znaki, odpowiedź maks. 30. **Sprawdź fakty** – AI potrafi się pomylić.

### W Buzz Pack Studio

1. Uruchom **`Start Buzz Pack Studio.bat`**.
2. Po lewej wpisz nazwę paczki → **Create**.
3. **Krok 1 Pack:** sprawdź, czy **Language** to **Polish (POL)** (przy polskiej płycie nowa
   paczka jest polska od razu) oraz:
   - *Plays on: Buzz!: Quiz World (Pl, Ru, El, Hr, Cs)*,
   - *Host reads the questions aloud* – włączone, z Twoim polskim głosem.
4. **Krok 2 Questions:** przeciągnij plik `.txt` na pole *Drop quiz files here* → **Import**.
   Studio pokaże, ile pytań przyjęło i które odrzuciło (z powodem).
5. **Krok 3 Rounds:** zostaw jak jest. Na polskiej płycie gra sama układa rundy w *Pack Game*.
   „Point Stealer: none” jest w porządku – ta runda wymaga obrazków.
6. **Krok 4 Generate:** zamknij programy obciążające kartę i kliknij **Generate PKG**. Pierwsza
   linia ma brzmieć *„…, host voice voice_models/buzz_host_POL)”*, a na końcu
   *„100 voiced lines”* (tyle, ile masz pytań). Przy 100 pytaniach trwa to kilkadziesiąt minut –
   każde pytanie jest czytane, sprawdzane przez rozpoznawanie mowy i w razie potrzeby nagrywane
   ponownie. Kolejne generowanie tej samej paczki jest szybkie.
7. **Copy straight into RPCS3**, uruchom grę → **Pack Game** → Twoja paczka. Gotowe!

---

## 9. Poprawianie wymowy

Polskie liczby, daty, lata i wieki („w 1966 roku”, „3 maja”, „XIX wieku”, „25 km”) program sam
czyta poprawnie. Najczęściej trzeba poprawić **obce nazwy** (gry, studia, ludzie).

**Które pytania brzmią podejrzanie** – to polecenie pokaże nagrania, w których rozpoznawanie mowy
usłyszało coś innego niż tekst (uruchom w folderze toolkitu):
```
Get-ChildItem voice_cache\clone_*.json | ForEach-Object { $j = Get-Content $_ -Raw | ConvertFrom-Json; if ($j.wer -gt 0.15) { "{0:N2}  {1}`n      usłyszał: {2}" -f $j.wer, $j.text, $j.heard } }
```
Same nagrania można odsłuchać w `voice_cache\clone_*.wav`.

**Jak poprawić:** zamknij Studio i otwórz w Notatniku plik paczki
`content\projects\<nazwa paczki>_<numer>\pack.json`. Dopisz zaraz po pierwszej klamrze `{` blok
`"voice"`:
```json
{
 "voice": {
  "pronounce": {"WITCHER": "łiczer", "BLIZZARD": "blizard"},
  "say": {"KTO STWORZYŁ GRĘ WIEDŹMIN 3?": "Kto stworzył grę Wiedźmin trzy?"}
 },
 "pack_number": 99,
 ...reszta pliku bez zmian...
```
- **`pronounce`** – zamienia pojedyncze słowo we wszystkich pytaniach na to, jak ma brzmieć
  (zapis fonetyczny po polsku). Wielkość liter nie ma znaczenia.
- **`say`** – zamienia całe czytane zdanie jednego pytania. Klucz musi być **dokładnie** taki jak
  pytanie na ekranie, czyli WIELKIMI LITERAMI (skopiuj je z `pack.json` niżej w tym samym pliku).
- Pilnuj przecinków i cudzysłowów – to format JSON. Po zapisie uruchom Studio i kliknij **Generate
  PKG**: nagrają się od nowa tylko zmienione pytania.

---

## 10. Gdy coś nie działa

| Objaw | Co zrobić |
|---|---|
| **„Install the host voice” kończy się błędem o Pythonie 3.11** | Zainstaluj Pythona 3.11 (krok 3) i uruchom `Install.bat` ponownie. |
| **Read game keys – błąd** | Upewnij się, że w podanym folderze jest `EBOOT.elf` (krok 2.4), a nie tylko `EBOOT.BIN`. |
| **VS Code / cały komputer „nie odpowiada” w trakcie treningu** | Karta albo dysk C: są przepełnione. Nie zamykaj okna z treningiem, kliknij „Czekaj”. Na przyszłość: trening w zwykłym PowerShellu, zamknięte inne programy, min. 10 GB wolnego na C:. |
| **`CUDA out of memory`** | Uruchom przerwany etap osobno z mniejszymi porcjami, a potem jeszcze raz główną komendę z kroku 7 (pominie skończone etapy):<br>`.\tools\clone_venv\Scripts\python.exe -m voice_trainer.train_s3gen --work "H:\buzz_trening_pl" --max-frames 1200`<br>albo dla etapu 4:<br>`.\tools\clone_venv\Scripts\python.exe -m voice_trainer.train_t3 --work "H:\buzz_trening_pl" --max-frames 800` |
| **Trening się przerwał** (błąd, zamknięte okno, uśpienie) | Uruchom tę samą komendę jeszcze raz. Skończone etapy zostaną pominięte, a przerwany zacznie się od nowa. |
| **Trener pisze, że nie znalazł `POLPACK*.PAK`** | `--disc` musi wskazywać folder z `PS3_GAME` polskiej płyty. Trener wypisze, jakie pliki faktycznie znalazł. |
| **Generate: „0 voiced lines · no POL host voice”** | Sprawdź, czy język paczki to Polish i czy Studio pokazuje *Host voices: POL (trained)*. Po aktualizacji toolkitu zamknij Studio całkowicie (czarne okno + ewentualne `python.exe` w Menedżerze zadań) i uruchom od nowa. |
| **Paczka nie pojawia się w grze** | Język konsoli w RPCS3 musi być polski (krok 2.2), a paczka musi mieć język Polish. |

---

## 11. Najczęstsze pytania

**Czy muszę aktualizować grę?**
Nie. Polska płyta w wersji 1.00 wystarcza do paczek i głosu. Toolkit nigdy sam nie instaluje
aktualizacji.

**A gra online (MyBuzz)?**
Na polskiej płycie aplikacja nie ustawia gry online – ta funkcja jest napisana pod płytę BCES00645
z aktualizacją. Paczki działają offline i serwer nie jest do nich potrzebny. Łatkę 60 FPS można
za to włączyć na każdej płycie: w RPCS3 *Manage → Game Patches* zaimportuj plik
`rpcs3_patches\buzz_toolkit_patches.yml` i zaznacz *60 FPS*.

**Czym jest Hugging Face, o którym piszą ostrzeżenia?**
To serwis z modelami AI (jak GitHub dla modeli). Toolkit pobiera stamtąd automatycznie model
głosu Chatterbox (twórcy: Resemble AI). Konto nie jest potrzebne. Pliki trafiają do
`C:\Users\<Ty>\.cache\huggingface`; jeśli brakuje miejsca na C:, przed treningiem wpisz w tym samym
oknie PowerShella `$env:HF_HOME = "H:\hf_cache"`.

**Czy mogę wybrać własną kolejność rund?**
Na polskiej płycie nie – ta funkcja wymaga płyty BCES00645 z aktualizacją. Gra układa rundy sama.

**Jak zaktualizować toolkit?**
W folderze toolkitu: `git pull`, potem uruchom Studio od nowa. (Jeśli pobrałeś toolkit wcześniej z
gałęzi `polish-voice`, przełącz się raz na główną: `git checkout main`, potem `git pull`.) Wytrenowany głos
(`voice_models\buzz_host_POL`) i Twoje paczki (`content\projects`) zostają.

**Jak przenieść wszystko na inny komputer?**
- **Samo granie:** skopiuj folder RPCS3 (zainstalowane paczki są w jego `dev_hdd0`) i folder gry.
  Toolkit nie jest do tego potrzebny. Jeśli gra leży na nowym komputerze pod inną ścieżką, dodaj
  ją w RPCS3 jeszcze raz (*File → Add Games*).
- **Robienie paczek z głosem:** zainstaluj Pythona 3.11 (krok 3), skopiuj folder toolkitu **bez**
  `tools\venv` i `tools\clone_venv` (te dwa działają tylko na komputerze, na którym powstały) i
  uruchom `Install.bat` z odpowiedzią **Y**. Najważniejszy jest folder
  `voice_models\buzz_host_POL` – to Twój wytrenowany głos, zrób jego kopię zapasową. Warto też
  skopiować `voice_cache` (gotowe nagrania), a `buzz_trening_pl` jest potrzebny tylko do
  ponownego treningu. W Studio ustaw jeszcze raz folder RPCS3.
- **Karta graficzna:** z kartą NVIDIA głos generuje się szybko. Na komputerze z kartą AMD (albo
  bez karty) działa na procesorze – wolniej, orientacyjnie kilkadziesiąt sekund na pytanie
  (zależnie od procesora; nie mierzyliśmy). Trening głosu wymaga karty NVIDIA.
- **Karta NVIDIA z małą pamięcią (4 GB i mniej):** jeśli Generate kończy się `CUDA out of memory`,
  uruchom Studio na procesorze – w PowerShellu w folderze toolkitu:
  ```
  $env:CUDA_VISIBLE_DEVICES = "-1"
  .\tools\venv\Scripts\python.exe -m buzz_engine studio
  ```

**Czy mogę udostępniać paczki?**
Tak, ale tylko z pytaniami i obrazkami, do których masz prawa. Paczka zawiera wygenerowane nagrania
głosu prowadzącego – udostępniaj ją znajomym prywatnie, nie publikuj masowo. Nie udostępniaj plików
gry ani wytrenowanego modelu głosu.

**Ile pytań powinna mieć paczka?**
Minimum 60, najlepiej 80–150. Przy mniejszej liczbie pytania będą się powtarzać.
