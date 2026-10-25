# Buzz Toolkit PL

> **Credits.** This project is a fork of **[Handylemons/BuzzToolkit](https://github.com/Handylemons/BuzzToolkit)**.
> Almost everything here – the pack builder, the PKG/EDAT writer, the ATRAC3 encoder, the
> host-voice trainer, the self-hosted online server and Buzz Pack Studio itself – is
> **Handylemons'** work, and all credit for building such a solid base goes to them. This fork
> adds Polish support on top of it. It is maintained separately and is not affiliated with or
> endorsed by the original author: problems in this fork are ours, not theirs.

> 🇵🇱 **Po polsku:** pełna instrukcja krok po kroku – od płyty do własnej paczki z polskim
> prowadzącym – jest w [INSTRUKCJA_PL.md](INSTRUKCJA_PL.md).

Make your own quiz packs for **Buzz! Quiz World** (PS3) and play them on RPCS3, with the questions
read aloud by **the game's own host – trained from your disc, in your language**. This fork is
built around the Polish disc (`BCES00647`): Polish packs with a trained Polish host voice, made
and played on the disc as it is, with no game update.

Two halves, one app (**Buzz Pack Studio**):

* **Pack generator (offline).** Add questions and pictures, choose the language, switch the
  host's voice on or off, press **Generate**, get a `.pkg`. Packs install like real DLC and play
  with no network at all.
* **Online server (self-hosted).** Your own replacement for the old Buzz! servers: MyBuzz online
  quizzes, leaderboards and buddies. The app sets up online play on `BCES00645` with update 01.02
  only (see the table below).

The toolkit ships **no game files**. Everything it needs from the game (the key packs are encrypted
with, the round plans, the host's voice) is read from **your own copy** during setup.

## What this fork adds

* **Host voice in any language the voice model speaks**, trained from that language's own lines
  on your disc (`voice_trainer.run --lang POL`), on Chatterbox's multilingual model. A trained voice
  is picked automatically for packs in its language. Measured on the Polish host: speaker
  similarity 0.979 (the real host's own clips: 0.978), word errors 5.2% (untrained: 10.9%).
* **Polish read the way a Polish host says it:** numbers, dates, years, centuries, decades and
  units in words with the right grammatical form ("w 1966 roku", "3 maja", "XIX wieku", "25 km").
* **Training on smaller and older cards:** fp32 on cards before the RTX 30 series, micro-batches
  on cards with less than 12 GB (tested on a GTX 1070 Ti, 8 GB). An interrupted step is redone,
  not skipped.
* **Buzz Pack Studio fixes:** packs made in the Studio get the host voice (they were always built
  silent before); new packs start in the disc's language; parts that only exist for `BCES00645`
  are hidden on the other discs; the game keys can be read from any of the three discs.
* **Polish guides:** [INSTRUKCJA_PL.md](INSTRUKCJA_PL.md) (the whole process, step by step) and
  [examples/INSTRUKCJA_PYTANIA_DLA_AI.md](examples/INSTRUKCJA_PYTANIA_DLA_AI.md) (instructions for
  an AI writing question files the importer and the host voice handle well).

Details: [RELEASE_NOTES.md](RELEASE_NOTES.md).

## Which disc, which features

All three are European releases of Buzz! Quiz World. Use your own copy; version 1.00 is fine.

| | `BCES00647` (Pl, Ru, El, Hr, Cs) | `BCES00645` (En, Es, Pt) | `BCES00644` (En, Fr, De, It, Nl) |
|---|---|---|---|
| Custom packs | ✓ | ✓ | ✓ |
| Trained host voice | ✓ Polish (tested); Russian, Greek (untested) | ✓ English (tested); Spanish, Portuguese (untested) | ✓ English (tested); French, German, Italian, Dutch (untested) |
| Game update needed | no | only for the two rows below | no |
| Custom running orders (Pack Game) | – | ✓ with update 01.02 | – |
| One-click online setup | – | ✓ with update 01.02 | – |
| 60 FPS patch (manual import, see Online server) | ✓ | ✓ | ✓ |

Czech and Croatian packs build, but have no host voice: the voice model does not speak them.
Without custom running orders, the game's *Pack Game* menu plays its own round order.

## What you need

* A Windows 10 or 11 PC
* **RPCS3** with one of the discs above set up in it
* **Python 3.11** (step 1)
* For the host voice: an **NVIDIA graphics card**, 8 GB or more recommended. Without one, packs
  still build, just without the host reading the questions.
* Disk space: about 1 GB for the toolkit; for the host voice about 6 GB more, plus about 5 GB of
  models downloaded on first use (to `C:\Users\<you>\.cache` – keep **at least 10 GB free on
  C:**), plus about 3 GB of working files while training.

## Getting started

You only do this once.

### 1. Install Python 3.11

Download **Python 3.11** from
[python.org/downloads/release/python-3119](https://www.python.org/downloads/release/python-3119/)
(scroll down to *Files* and pick **Windows installer (64-bit)**). Run it and, on the first
screen, tick **Add python.exe to PATH** and **Use admin privileges when installing py.exe**, then
click **Install Now**. Check it in PowerShell: `py -3.11 --version`.

Use 3.11 even if you already have a newer Python: the host voice only works on 3.11. The two can
sit side by side.

### 2. Get the toolkit

With [Git](https://git-scm.com/):

```
git clone https://github.com/KotePlay/BuzzToolkitPL.git
```

or on GitHub press **Code → Download ZIP** and unzip it. Put it somewhere with space, for example
`H:\BuzzToolkitPL`, not inside a OneDrive or other synced folder. To update later: `git pull` in
that folder (your voices and packs stay).

### 3. Run Install.bat

Double-click **Install.bat** in the toolkit folder. It:

* sets up the app in its own folder (`tools\venv`), so it doesn't touch anything else on your PC
* downloads **ffmpeg** (a free audio/video tool the app uses)
* asks whether to install the **host voice**. Answer **Y** for the voice (about 6 GB, takes a while)
  or **N** to skip it; you can run Install.bat again later to add it.

If Windows shows "Windows protected your PC", click **More info → Run anyway**.

### 4. Find your game's EBOOT and decrypt it

The app reads the key it needs from your own copy of the game, from a file called `EBOOT.BIN`.

1. **If your game is an `.iso` file, extract it first.** Install [7-Zip](https://www.7-zip.org/)
   (free), right-click the `.iso` → **7-Zip → Extract to "Buzz Quiz World\"**. You get a normal
   folder. (If your game is already a folder, skip this.)
2. **Open the game folder, then `PS3_GAME`, then `USRDIR`.** `EBOOT.BIN` is in there.
3. **Decrypt it:** in RPCS3 open **Utilities → Decrypt PS3 Binaries**, pick that `EBOOT.BIN` and
   let it finish. A new file, `EBOOT.elf`, appears in the same `USRDIR` folder.
4. **Copy the folder's path:** in the `USRDIR` window, click the address bar at the top (the path
   turns blue) and press **Ctrl+C**. It looks like
   `H:\Games\Buzz! Quiz World (Europe) (Pl,Ru,El,Hr,Cs)\PS3_GAME\USRDIR`. You'll paste it in the
   next step, as it is, with no quotes.

### 5. Open the app and finish setup

Double-click **Start Buzz Pack Studio.bat**. The app opens in your web browser at
`http://127.0.0.1:8765`. Keep the black window open while you use the app; closing it stops the
app.

In the app's **Setup** box (left-hand side):

1. **RPCS3 folder:** open the folder that has `rpcs3.exe` in it, click its address bar, press
   **Ctrl+C**, paste it into the box (**Ctrl+V**) and press **Save folder**. A green label names the
   disc the app found.
2. **Your decrypted EBOOT:** paste the `USRDIR` path from step 4 and press **Read game keys**.
   A green **Game keys read from your EBOOT** label confirms it.
3. **`BCES00645` only** (the Studio hides these on the other discs):
   * **Game update 01.02**, needed for custom running orders and online setup. Press **Download
     update from Sony** (the official 22 MB update, straight from Sony's PS3 update server; the
     toolkit never includes Sony's files), close RPCS3, press **Install update into RPCS3**, then
     **Save folder** again; the label turns green. (Or install it yourself: RPCS3 → **File →
     Install Packages/Raps/Edats** and pick the file in `tools\downloads`.)
   * Optional: **Turn on custom running orders**, so each pack plays its own rounds in the
     game's *Pack Game* menu. It changes one game script and keeps a backup.

The app never installs a game update unless you press those buttons.

Next: train the host voice (see **Host voice**) if you want packs read aloud, then make packs.
From now on, just double-click **Start Buzz Pack Studio.bat**.

## Make a pack

1. **Create** a pack (name on the left).
2. **Pack**: channel, language, "made by", pack number, host voice on/off. New packs start in your
   disc's language (Polish on `BCES00647`); *Plays on* shows which disc the language belongs to.
3. **Questions**: drop in files (CSV, text, Moodle XML, Buzz online XML, JSON), pull from
   Open Trivia DB / OpenTriviaQA / The Trivia API (English), or write your own (picture questions
   and Point Stealer picture answers included). The app checks the game's limits
   (93 characters per question, 30 per answer). Text files must be UTF-8. For Polish questions
   written by an AI, see [examples/INSTRUKCJA_PYTANIA_DLA_AI.md](examples/INSTRUKCJA_PYTANIA_DLA_AI.md).
4. **Rounds**: the running order used with custom running orders (`BCES00645`). The **Question
   coverage** box underneath is only a check: it shows how many of your questions each round can
   use. If a round shows *repeats* or *none*, add more questions of that kind.
5. **Generate**: builds the pack and a `.pkg`. With the host voice on, every question is read
   aloud, checked by speech recognition and re-made if words are wrong; the first build of 100
   questions takes a few tens of minutes, rebuilds are quick. Install it in RPCS3 with **File →
   Install Packages/Raps/Edats** (or press *Copy straight into RPCS3*).

### Pack numbers

Every pack has a number (1 to 999), and **no two packs can share one**. The game keeps each pack in
a folder named after its number, so installing a pack **replaces any other pack with the same
number**, including official DLC. That happens whether you use *Copy straight into RPCS3* or
RPCS3's *File → Install Packages*.

The app protects you from this:

* A new pack gets a free number automatically, skipping numbers already installed in RPCS3 or used
  by your other packs. **Set your RPCS3 folder first**, so it can see what's installed.
* You can change the number in step 1. Numbers that are already taken are refused, and the app
  suggests a free one.
* **Generate** and **Copy straight into RPCS3** refuse to go ahead if a *different* pack with that
  number is installed. Rebuilding and reinstalling the *same* pack is fine; the app recognises it.

If you install a PKG by hand, check its number first. The file name ends in it, for example
`PubQuiz_GBR_PACK0096.pkg` is pack 96.

Example question files are in `examples/`. A `.buzz.txt` file is the easiest way to share a pack
as plain text (see `examples/pub_quiz.buzz.txt`).

## Rounds and running orders

On `BCES00645` with update 01.02, every pack can have its own running order for the game's
**Pack Game** menu: any of the game's rounds, in any order, with optional random picks, ending
with the Final Countdown. It needs the one-time **Turn on custom running orders** step in the
app's Setup box. On the other discs the *Pack Game* menu plays the game's own round order.

## Host voice

With the voice switched on, the host reads every question. Voices are made from your own game,
once per language; after that, voicing a pack takes minutes. Type the commands in a PowerShell
window opened in the toolkit folder.

* **Trained (recommended):** learns the host's voice and delivery from every line in that language
  on your disc. `--disc` is the extracted game folder (the one that holds `PS3_GAME`), `--lang` the
  pack language, `--work` a scratch folder (one per language):
  ```
  .\tools\clone_venv\Scripts\python.exe -m voice_trainer.run --disc "<game folder>" --work "<scratch folder>" --lang POL
  ```
  It saves the voice as `voice_models\buzz_host_<LANG>` (`buzz_host` for English), and packs in
  that language use it. For English, leave out `--lang` (or use `--lang GBR`). Add
  `--preset best` for a longer run; in the original author's tests it sounded no better than the
  default.
* **Quick (a few minutes):** clones the host from a short sample instead of training. Less close
  to the real host; a trained voice in the same language is preferred over it.
  ```
  .\tools\venv\Scripts\python.exe make_host_reference.py <game folder>\PS3_GAME\USRDIR\PACK0100\POLPACK0100.PAK --out voice_models\buzz_host_POL_quick\reference.wav --lang POL
  ```

How long training takes:

| Card | Language | Time |
|---|---|---|
| RTX 3060 (12 GB) | English | about 1 hour |
| GTX 1070 Ti (8 GB) | Polish | about 2-3 hours (11,500 clips; fp32 and micro-batches) |

The trainer adapts to the card by itself; CPU-only training is not practical. While it runs,
close games, browsers, Discord, Steam and code editors (they use the card's memory), run it in its
own PowerShell window rather than an editor's terminal, switch off sleep, and keep at least 10 GB
free on C:. If it is interrupted, run the same command again: finished steps are skipped and an
unfinished one starts over. It ends with two result lines (`base` and `trained`: speaker
similarity, higher is better; word error rate, lower is better) and listening samples in
`<scratch folder>\eval\`.

Every generated line is checked with speech recognition and re-made if words are wrong. To fix a
word the voice says wrong, add a `voice` block to the pack's
`content\projects\<pack>\pack.json` (with the Studio closed): `"pronounce"` respells a word in
every question, `"say"` replaces the whole spoken line of one question (key = the question exactly
as shown on screen):

```json
"voice": {"pronounce": {"WITCHER": "łiczer"},
          "say": {"KTO STWORZYŁ GRĘ WIEDŹMIN 3?": "Kto stworzył grę Wiedźmin trzy?"}},
```

Only the changed questions are re-made on the next **Generate**.

## Online server

**The server is optional.** Your packs play offline without it.

The app's one-click setup (**Set up this PC for online play**) is written for `BCES00645` with
update 01.02; on the other discs the Studio says so and hides it. If you've run it and the
server isn't running, the game shows a "can't connect" message when it starts; press the button
to close it and carry on playing offline. Start the server only when you want MyBuzz online
quizzes.

Open **Online server** in the app.

1. **Start server** (first time: give it your `EBOOT.elf` if you haven't already).
2. **Set up this PC for online play**: applies the login fix to your game scripts, enables the RPCS3
   patch the server needs and sets RPCS3's network options. The host uses `127.0.0.1`.
3. **Friends**: each friend installs the toolkit, does the one-time setup, and runs
   *Set up this PC for online play* with **your** IP address (shown on the page). Over the internet,
   forward TCP ports **10060, 10071 and 10075** to the host and use its public IP.
   Everyone needs a free **RPCN** account (RPCS3 → Configuration → RPCN).
4. **Publish to MyBuzz** on any pack puts its questions on your server as online quizzes.

The RPCS3 patches are also in the toolkit as a file of their own,
`rpcs3_patches\buzz_toolkit_patches.yml`, with entries for all three discs: open RPCS3's
**Manage → Game Patches** window, drag the file onto it, choose **Import**, then tick the patches
for Buzz! Quiz World. They contain only the toolkit's own changes to the game code, no game data:

* **Online: logged in when connected to the server**: lets the menus go online with the toolkit's
  server, and lets the game carry on offline when the server isn't running.
* **60 FPS**: runs the game at 60 frames per second instead of 30 (optional; works on every disc).

What works online today: the MyBuzz menus (online quizzes, leaderboards, buddies). Live online
matches against remote players are not supported yet (see the roadmap).

## Question sources and licences

* **Open Trivia DB** and **OpenTriviaQA**: CC BY-SA 4.0. The pack's credits page is filled in
  automatically; keep it if you share the pack.
* **The Trivia API** (free tier): CC BY-NC 4.0, **non-commercial use only**.
* Your own questions and pictures: share only what you have the right to share.

## Known issues

* **Real PS3 consoles** (HEN / CFW) are untested; packs are confirmed on RPCS3 (PKG install via
  *File → Install Packages/Raps/Edats* and *Copy straight into RPCS3*).
* **Online:** the app sets up online play on `BCES00645` with update 01.02 only. Live online
  matches against remote players are not supported (MyBuzz quizzes, leaderboards and buddies are).
* **Trained voices** are tested in English (original toolkit) and Polish (this fork); other
  languages train the same way but have not been listened to.
* **Polish numbers** after words that change their case ("około", "ilu", "po") are read in the
  plain form; write such numbers in words, or fix the line with `"say"`.

## Licence

Buzz Toolkit is released under the [MIT licence](LICENSE) (copyright Handylemons); this fork's
changes are released under the same licence. The licence covers the toolkit's own code and
documentation only; it grants no rights to Buzz! Quiz World or any other game content, which
belongs to its owners and is not included. Third-party parts keep their own licences; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Disclaimer

**Use at your own risk.** Buzz Toolkit is provided **as is**, without warranty of any kind,
express or implied, including fitness for a particular purpose. You use it entirely at your own
risk. The authors are not responsible for any damage, data loss, corrupted saves or game
installs, account problems or any other issue arising from its use or misuse, including errors
in the toolkit itself. The toolkit changes files in your RPCS3 installation and keeps backups
of what it changes, but you should keep your own backups too.

**Fan project.** This is an unofficial, non-commercial fan project. It is not affiliated with,
endorsed, sponsored or approved by Sony Interactive Entertainment, Relentless Software or any
other rights holder. "Buzz!", "PlayStation" and "PS3" are trademarks of their respective owners
and are used here only to describe what the toolkit works with.

**Your own copy only.** You need your own legally obtained copy of Buzz! Quiz World. The toolkit
contains no game files, keys or recordings; it reads what it needs from your copy, on your
machine. The game update is downloaded from Sony's own servers, not from this project. Don't use
the toolkit to share or distribute game content or trained voice models, and only share packs
made from questions and pictures you have the right to share.
