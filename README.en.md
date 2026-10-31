# Kurdish Multilingual Lexicon (Ferhenga Pirzimanî)

**Kurdish ↔ English · Kurdish ↔ German · Kurdish ↔ Turkish**
Kurmanji · Sorani · Southern Kurdish · Zazaki (+ Gorani/Hewrami)

[Türkçe](README.md) · **English** · [Deutsch](README.de.md) · [Kurmancî](README.ku.md)

> ⚠️ **STATUS: DRAFT (v0.4), not yet reviewed by native speakers.**
> All data was compiled automatically from open sources (Wiktionary, Wikipedia). Every row carries `review_status = unverified`. See [KONTROL.md](KONTROL.md) (review process, Turkish) and [CONTRIBUTING.md](CONTRIBUTING.md).

An openly licensed, source-traceable lexicon and toolkit for anyone building games, apps, teaching material or language technology in Kurdish.

## Start here

| You want… | File |
|---|---|
| A Kurmanji word with its Turkish, English and German equivalents in one row | `data/multilingual/kmr-tr-en-de.tsv` (32k headwords, ranked by frequency) |
| The most frequent words (teaching, learning apps) | `data/learner/kmr-top3000.tsv` |
| Words for word games (Wordle-style), 3–7 letters | `data/games/kmr-5-harf.tsv` etc. |
| Thematic lists (colors, animals, family, food, verbs…) across four varieties | `data/themes/` (17 themes, `themes.json`) |
| Cross-dialect equivalents (Kurmanji ↔ Sorani, Zazaki, Southern Kurdish, Gorani) | `data/cross-dialect.tsv` |
| The most reliable pairs (confirmed by two independent Wiktionary editions) | `data/core/` |
| Word frequency from Kurdish Wikipedias | `data/frequency/` (Kurmanji, Sorani, Zazaki; 50k each) |
| Alphabets, letter tables, on-screen keyboard layouts (JSON) | `data/alphabets/` |
| Code: correct Kurdish casing, Hawar alphabet sorting, typing fixes | `tools/python/kurdi.py`, `tools/js/kurdi.js` |
| **Academic standards:** CLDF Dictionary export (validated), UD and UniMorph feature columns, ISO 639-3 + Glottocodes, Leipzig-glossed reference grammar, evaluation against UniMorph and the UD Kurmanji treebank, datasheet | `cldf/`, `docs/standartlar.md`, `docs/degerlendirme-sonuclari.md`, `DATASHEET.md` |
| **Descriptive reference grammar of Kurmanji** (in Turkish; Leipzig-glossed examples, WALS typological profile, TR/KU/EN terminology); exercises in `docs/ogretim/` | `docs/dilbilgisi/` |
| **Is a word native Kurdish or borrowed?** Etymology class (inherited / internal / borrowed / Iranian loan / onomatopoeic), source language, path, evidence, confidence for 156k entries | `data/kmr/db/etymology-class.tsv` · `docs/etimoloji.md` |
| Full verb conjugation (9 tenses × 6 persons, negatives, imperative) for 3,982 verbs | `data/kmr/db/verb-paradigms.jsonl.gz`, `verb-stems.tsv` |
| **Linguistic database:** part of speech, gender, definitions, examples, etymology, morpheme segmentation, IPA, hyphenation, synonyms for every lemma | `data/kmr/db/lemmas.tsv` (158k Kurmanji lemmas; also Sorani 7.2k, Zazaki 3.3k, Southern 819, Gorani 167) · `docs/veritabani.md` |
| Inflected forms → lemma + grammatical tags | `data/kmr/db/forms.tsv.gz` (330k forms) |
| Etymology, affixes, verb stems, proverbs & idioms (21k), native-speaker audio links (3.1k) | `data/*/db/` |
| Building a game or app | `docs/oyun-gelistirici-rehberi.md` (Turkish; key points below) |

## Coverage

| Variety (ISO 639-3) | Script | Turkish | English | German |
|---|---|---:|---:|---:|
| Kurmanji `kmr` | Latin (Hawar) | 141,086 | 179,651 | 71,981 |
| Kurmanji **core** (2+ sources) | | 5,519 | 1,456 | 2,120 |
| Sorani `ckb` | Arabic-based | 91 + 929* | 1,628 + 738* | 246 + 908* |
| Zazaki `zza` | Latin | 9,936 + 779* | 1,231 + 564* | 495 + 769* |
| Southern Kurdish `sdh` | Arabic-based | 358* | 323* | 371* |
| Gorani/Hewrami `hac` | Arabic-based | 160* | 148* | 181* |

\* derived through Kurmanji (`.pivot.tsv`), lowest confidence.

## Key points for developers
- **Casing:** never use the Turkish locale for Kurmanji. `i → I`, `î → Î` (not `İ`). Use `upper()` from `tools/`.
- **Letters:** Kurmanji needs `ê î û ç ş` (and capitals). Check your font. Sorani needs Kurdish Arabic letters (`ڵ ڕ ۆ ێ ڤ`) and right-to-left layout.
- **Sorting:** Hawar order puts `ç` after `c`, `ê` after `e`, `î` after `i`, `ş` after `s`, `û` after `u`.
- **Review:** treat every word as a draft until a native speaker has checked it.

## Rebuild
Everything is reproducible from public dumps with the scripts in `scripts/` (see `docs/yeniden-uretim.md`).

## License
Data and docs: **CC BY-SA 4.0** (derived from Wiktionary/Wikipedia; attribution + share-alike), see `DATA-LICENSE.md`. Code: **MIT**. Citation: `CITATION.cff`.

Started by GameVan Studio to give Kurdish games and learning projects an open foundation. First compilation done with an AI assistant (Claude).
