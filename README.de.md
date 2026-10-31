# Mehrsprachiges kurdisches Wörterbuch (Ferhenga Pirzimanî)

**Kurdisch ↔ Deutsch · Kurdisch ↔ Englisch · Kurdisch ↔ Türkisch**
Kurmandschi · Sorani · Südkurdisch · Zazaki (+ Gorani/Hewrami)

[Türkçe](README.md) · [English](README.en.md) · **Deutsch** · [Kurmancî](README.ku.md)

> ⚠️ **STATUS: ENTWURF (v0.4), noch nicht von Muttersprachlern geprüft.**
> Alle Daten wurden automatisch aus offenen Quellen (Wiktionary, Wikipedia) zusammengestellt. Jede Zeile trägt `review_status = unverified`.

Ein offen lizenzierter Wortschatz mit Quellenangabe in jeder Zeile sowie Werkzeuge für alle, die Spiele, Apps, Lehrmaterial oder Sprachtechnologie auf Kurdisch entwickeln.

## Einstieg

| Sie möchten … | Datei |
|---|---|
| Ein Kurmandschi-Wort mit deutscher, englischer und türkischer Entsprechung in einer Zeile | `data/multilingual/kmr-tr-en-de.tsv` (32.000 Stichwörter, nach Häufigkeit) |
| Die häufigsten Wörter (Unterricht, Lern-Apps) | `data/learner/kmr-top3000.tsv` |
| Wörter für Wortspiele (3–7 Buchstaben) | `data/games/` |
| Thematische Listen (Farben, Tiere, Familie, Essen, Verben …) in vier Varietäten | `data/themes/` |
| Entsprechungen zwischen den Dialekten | `data/cross-dialect.tsv` |
| Die zuverlässigsten Paare (von zwei unabhängigen Wiktionary-Ausgaben bestätigt) | `data/core/` |
| Worthäufigkeit aus kurdischen Wikipedias | `data/frequency/` |
| Alphabete und Bildschirmtastaturen (JSON) | `data/alphabets/` |
| **Akademische Standards:** CLDF-Dictionary-Export, UD- und UniMorph-Merkmale, ISO 639-3 + Glottocodes, Grammatik mit Leipzig-Glossierung, Evaluation gegen UniMorph und UD-Kurmanji-Baumbank, Datasheet | `cldf/`, `docs/standartlar.md`, `DATASHEET.md` |
| **Deskriptive Referenzgrammatik des Kurmancî** (auf Türkisch; Leipzig-glossierte Beispiele, WALS-Profil) | `docs/dilbilgisi/` |
| **Ist ein Wort ererbt oder entlehnt?** Herkunftsklasse, Quellsprache, Weg, Beleg, Konfidenz (156.000 Einträge) | `data/kmr/db/etymology-class.tsv` · `docs/etimoloji.md` |
| Vollständige Verbkonjugation für 3.982 Verben | `data/kmr/db/verb-paradigms.jsonl.gz` |
| **Linguistische Datenbank:** Wortart, Genus, Definitionen, Beispiele, Etymologie, Morphemzerlegung, IPA, Silbentrennung | `data/kmr/db/lemmas.tsv` (158.000 Lemmata) |
| Flexionsformen → Lemma + grammatische Merkmale | `data/kmr/db/forms.tsv.gz` (330.000 Formen) |
| Etymologie, Affixe, Verbstämme, Sprichwörter (21.000), Audioaufnahmen (3.100) | `data/*/db/` |
| Code für korrekte Groß-/Kleinschreibung und Sortierung | `tools/python/kurdi.py`, `tools/js/kurdi.js` |

## Umfang (Deutsch)
Kurmandschi–Deutsch: 71.981 Paare (2.120 im geprüften Kern mit 2+ Quellen) · Sorani: 246 direkt + 908 abgeleitet · Zazaki: 495 + 769 · Südkurdisch: 371 abgeleitet · Gorani: 181 abgeleitet. Die deutschen Einträge stammen aus dem deutschen und dem kurdischen Wiktionary (dort „Kurmandschi“, „Sorani“, „Zazaki“, „Dimli“).

## Hinweise für Entwickler
- Kurmandschi nie mit türkischer Locale in Großbuchstaben umwandeln: `i → I`, `î → Î` (nicht `İ`).
- Schriftarten müssen `ê î û ç ş` bzw. kurdisch-arabische Buchstaben (Sorani, von rechts nach links) unterstützen.
- Alle Wörter gelten als Entwurf, bis Muttersprachler sie geprüft haben.

## Lizenz
Daten und Dokumentation: **CC BY-SA 4.0** (abgeleitet aus Wiktionary/Wikipedia). Code: **MIT**.

> Dieser deutsche Text wurde nicht von einem Muttersprachler geprüft.
