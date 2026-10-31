#!/usr/bin/env python3
"""Veritabanını uluslararası standart biçimlere dönüştürür.

  1. UD (Universal Dependencies) özellikleri ve UniMorph etiketleri:
       data/<v>/db/forms.tsv.gz  -> ud_feats, unimorph sütunları eklenir
       data/<v>/unimorph/<v>.tsv           (lemma, form, özellikler; veride geçen)
       data/kmr/unimorph/kmr.generated.tsv (kurala göre üretilen fiil çekimleri)
  2. CLDF Dictionary veri kümesi: cldf/  (pycldf ile doğrulanır)

Etiket eşlemesi UD_Kurmanji-MG ağaç bankası (Gökırmak & Tyers 2017) ve UniMorph kmr
veri kümesindeki kullanımı izler:
  yalın (direct) -> Case=Nom / NOM, bükümlü (oblique) -> Case=Acc / ACC,
  izafet (ezafe) -> Case=Con / LGSPEC1, seslenme -> Case=Voc / VOC.

Kullanım: python scripts/standards.py
"""
import csv, gzip, json, re, sys, shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
csv.field_size_limit(sys.maxsize)

LANGS = {
    # id: (ad, ISO 639-3, Glottocode, yazı)
    "kmr": ("Northern Kurdish (Kurmanji)", "kmr", "nort2641", "Latn"),
    "ckb": ("Central Kurdish (Sorani)", "ckb", "cent1972", "Arab"),
    "sdh": ("Southern Kurdish", "sdh", "sout2640", "Arab"),
    "zza": ("Zazaki", "zza", "zaza1246", "Latn"),
    "hac": ("Gorani (Gurani)", "hac", "gura1251", "Arab"),
}

UD = {
    "masculine": ("Gender", "Masc"), "feminine": ("Gender", "Fem"),
    "singular": ("Number", "Sing"), "plural": ("Number", "Plur"),
    "definite": ("Definite", "Def"), "indefinite": ("Definite", "Ind"),
    "direct": ("Case", "Nom"), "oblique": ("Case", "Acc"),
    "ezafe": ("Case", "Con"), "vocative": ("Case", "Voc"),
    "1st-person": ("Person", "1"), "2nd-person": ("Person", "2"), "3rd-person": ("Person", "3"),
    "present": ("Tense", "Pres"), "past": ("Tense", "Past"), "future": ("Tense", "Fut"),
    "past-perfect": ("Tense", "Pqp"), "progressive": ("Aspect", "Prog"),
    "subjunctive": ("Mood", "Sub"), "imperative": ("Mood", "Imp"),
    "negative": ("Polarity", "Neg"),
    "comparative": ("Degree", "Cmp"), "superlative": ("Degree", "Sup"),
}
UM = {
    "masculine": "MASC", "feminine": "FEM", "singular": "SG", "plural": "PL",
    "definite": "DEF", "indefinite": "INDF", "direct": "NOM", "oblique": "ACC",
    "ezafe": "LGSPEC1", "vocative": "VOC",
    "1st-person": "1", "2nd-person": "2", "3rd-person": "3",
    "present": "PRS", "past": "PST", "future": "FUT", "past-perfect": "PST;PRF",
    "progressive": "PROG", "subjunctive": "SBJV", "imperative": "IMP",
    "negative": "NEG", "comparative": "CMPR", "superlative": "SPRL",
}
UPOS2UM = {"NOUN": "N", "PROPN": "PROPN", "VERB": "V", "ADJ": "ADJ", "ADV": "ADV",
           "PRON": "PRO", "NUM": "NUM", "DET": "DET", "ADP": "ADP"}


def ud_feats(tags, upos):
    feats = {}
    for t in tags:
        if t in UD:
            k, v = UD[t]
            feats[k] = v if k not in feats else ",".join(sorted({*feats[k].split(","), v}))
    if upos == "VERB":
        feats.setdefault("VerbForm", "Fin")
        if "Mood" not in feats and feats.get("Tense") in ("Pres", "Past", "Pqp"):
            feats["Mood"] = "Ind"
        if "Polarity" not in feats and any(t in tags for t in ("present", "past", "future", "subjunctive", "imperative")):
            feats["Polarity"] = "Pos"
    return "|".join(f"{k}={feats[k]}" for k in sorted(feats)) or "_"


def unimorph(tags, upos):
    out = [UPOS2UM.get(upos, upos)]
    for t in tags:
        if t in UM:
            out.extend(UM[t].split(";"))
    if upos == "VERB":
        if "NEG" not in out:
            out.append("POS")
        if "PRS" in out and "SBJV" not in out and "IMP" not in out:
            out += ["IND", "IPFV"]
    return ";".join(sorted(set(out), key=out.index))


# Üretilen fiil paradigması yuvaları -> UniMorph özellikleri (UniMorph kmr ile aynı ayrım)
SLOT_UM = {
    "present": "IND;POS;PRS;IPFV", "present_negative": "IND;NEG;PRS;IPFV",
    "subjunctive": "POS;PRS;SBJV", "subjunctive_negative": "NEG;PRS;SBJV",
    "past": "IND;PFV;POS;PST", "past_negative": "IND;NEG;PFV;PST",
    "past_progressive": "IND;POS;PST;PROG", "present_perfect": "IND;POS;PRF;PRS",
    "past_perfect": "IND;POS;PRF;PST",
}
PERSON_UM = ["1;SG", "2;SG", "3;SG", "1;2;3;PL"]


def slot_features():
    """(yuva, kişi indeksi) -> UniMorph özellik kümesi (frozenset)."""
    m = {}
    for slot, f in SLOT_UM.items():
        for i in range(6):
            p = PERSON_UM[min(i, 3)]
            m[(slot, i)] = frozenset(("V;" + f + ";" + p).split(";"))
    return m


def convert_forms():
    stats = {}
    for v in LANGS:
        src = DATA / v / "db" / "forms.tsv.gz"
        if not src.exists():
            continue
        rows = []
        with gzip.open(src, "rt", encoding="utf-8") as f:
            r = csv.DictReader(f, delimiter="\t")
            for row in r:
                tags = [t for t in row["tags"].split(",") if t]
                row["ud_feats"] = ud_feats(tags, row["upos"])
                row["unimorph"] = unimorph(tags, row["upos"])
                rows.append(row)
        cols = ["form", "lemma", "upos", "tags", "ud_feats", "unimorph", "description_ku"]
        with gzip.open(src, "wt", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n", extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        out = DATA / v / "unimorph"
        out.mkdir(exist_ok=True)
        seen = set()
        with open(out / f"{v}.tsv", "w", encoding="utf-8") as f:
            for row in rows:
                if not row["lemma"] or not row["tags"]:
                    continue
                key = (row["lemma"], row["form"], row["unimorph"])
                if key in seen:
                    continue
                seen.add(key)
                f.write("\t".join(key) + "\n")
        stats[v] = len(seen)
    # üretilen fiiller
    par = DATA / "kmr" / "db" / "verb-paradigms.jsonl.gz"
    sf = slot_features()
    n = 0
    with gzip.open(par, "rt", encoding="utf-8") as f, \
            open(DATA / "kmr" / "unimorph" / "kmr.generated.tsv", "w", encoding="utf-8") as out:
        for line in f:
            d = json.loads(line)
            seen = set()
            for slot in SLOT_UM:
                for i, form in enumerate(d["forms"][slot]):
                    feats = ";".join(sorted(sf[(slot, i)]))
                    if (form, feats) in seen:
                        continue
                    seen.add((form, feats))
                    out.write(f"{d['verb']}\t{form}\t{feats}\n")
                    n += 1
    stats["kmr.generated"] = n
    return stats


def build_cldf():
    from pycldf import Dictionary
    from pycldf.sources import Source
    target = ROOT / "cldf"
    if target.exists():
        shutil.rmtree(target)
    ds = Dictionary.in_dir(target)
    ds.add_component("LanguageTable")
    ds.add_component("ExampleTable")
    ds.add_columns("EntryTable",
                   {"name": "Gender", "datatype": "string"},
                   {"name": "IPA", "datatype": "string"},
                   {"name": "Etymology", "datatype": "string"},
                   {"name": "Etymology_Class", "datatype": "string"},
                   {"name": "Freq_Rank", "datatype": "integer"},
                   {"name": "Source_URL", "datatype": "anyURI"},
                   {"name": "Review_Status", "datatype": "string"})
    ds.add_columns("SenseTable",
                   {"name": "Description_Language", "datatype": "string"},
                   {"name": "Translations_tr", "datatype": "string"},
                   {"name": "Translations_de", "datatype": "string"})
    ds.add_sources(Source("misc", "wiktionary_ku", title="Wîkîferheng (Kurdish Wiktionary)",
                          howpublished="https://ku.wiktionary.org", note="Extracted with Wiktextract (Ylonen 2022), dump 2026-10"),
                   Source("misc", "wiktionary_en", title="English Wiktionary",
                          howpublished="https://en.wiktionary.org", note="Extracted with Wiktextract (Ylonen 2022)"))

    ec = {}
    p = DATA / "kmr" / "db" / "etymology-class.tsv"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                ec.setdefault((r["word"], r["pos"]), r["class"])

    languages = [dict(ID=k, Name=n, ISO639P3code=iso, Glottocode=g) for k, (n, iso, g, _) in LANGS.items()]
    entries, senses, examples = [], [], []
    for v in LANGS:
        path = DATA / v / "db" / "lemmas.jsonl.gz"
        if not path.exists():
            continue
        with gzip.open(path, "rt", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                d = json.loads(line)
                eid = f"{v}-{i}"
                ety = (d.get("etymology_en") or d.get("etymology_ku") or "")[:500]
                entries.append(dict(
                    ID=eid, Language_ID=v, Headword=d["word"], Part_Of_Speech=d["upos"],
                    Gender=d.get("gender", ""), IPA=" ; ".join(d.get("ipa", [])),
                    Etymology=ety, Etymology_Class=ec.get((d["word"], d.get("pos", "")), "") if v == "kmr" else "",
                    Freq_Rank=d.get("freq_rank") or None, Source_URL=d.get("source_url", ""),
                    Review_Status=d.get("review_status", "unverified"),
                    Source=["wiktionary_en" if "en.wiktionary" in d.get("source_url", "") else "wiktionary_ku"]))
                tr = d.get("translations", {})
                n = 0
                for lang, glosses in (("ku", d.get("glosses_ku", [])), ("en", d.get("glosses_en", []))):
                    for g in glosses:
                        n += 1
                        senses.append(dict(ID=f"{eid}-s{n}", Entry_ID=eid, Description=g,
                                           Description_Language=lang,
                                           Translations_tr=" | ".join(tr.get("tr", [])) if n == 1 else "",
                                           Translations_de=" | ".join(tr.get("de", [])) if n == 1 else ""))
                if n == 0 and any(tr.get(k) for k in ("en", "tr", "de")):
                    senses.append(dict(ID=f"{eid}-s1", Entry_ID=eid,
                                       Description=" | ".join(tr.get("en", [])) or "_",
                                       Description_Language="en",
                                       Translations_tr=" | ".join(tr.get("tr", [])),
                                       Translations_de=" | ".join(tr.get("de", []))))
                for j, ex in enumerate(d.get("examples", [])[:3], 1):
                    examples.append(dict(ID=f"{eid}-x{j}", Language_ID=v, Primary_Text=ex[:1000],
                                         Analyzed_Word=[], Gloss=[], Translated_Text=""))
    # senses -> example links CLDF'de isteğe bağlı; burada atlanır
    ds.write(LanguageTable=languages, EntryTable=entries, SenseTable=senses, ExampleTable=examples)
    ds.properties["dc:title"] = "Kurdish Multilingual Lexicon (Ferhenga Pirzimanî)"
    ds.properties["dc:license"] = "https://creativecommons.org/licenses/by-sa/4.0/"
    ds.properties["dc:description"] = ("Kurdish (Kurmanji, Sorani, Southern Kurdish, Zazaki, Gorani) lexical database "
                                       "with POS, gender, glosses, Turkish/English/German translations, etymology. "
                                       "Derived automatically from Wiktionary; not yet expert-reviewed.")
    ds.write_metadata()
    ds.validate()
    # büyük tabloları sıkıştır (pycldf zip'li tabloları okuyabilir)
    import zipfile
    for name in ("entries.csv", "senses.csv", "examples.csv"):
        fp = target / name
        with zipfile.ZipFile(fp.with_suffix(".csv.zip"), "w", zipfile.ZIP_DEFLATED) as z:
            z.write(fp, name)
        fp.unlink()
    return dict(entries=len(entries), senses=len(senses), examples=len(examples))


if __name__ == "__main__":
    print("forms:", convert_forms())
    print("cldf:", build_cldf())
