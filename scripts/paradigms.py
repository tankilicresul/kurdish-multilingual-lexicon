#!/usr/bin/env python3
"""Kurmancî çekim tabloları (paradigmalar).

Çıktılar:
  data/kmr/db/verb-stems.tsv        her fiil için şimdiki ve geçmiş gövde + kaynağı
  data/kmr/db/verb-paradigms.jsonl.gz  her fiil için kurala göre üretilmiş tam çekim
  docs/dilbilgisi/paradigmalar.md    seçili isim ve fiillerin tabloları

Gövde kaynakları (öncelik sırası):
  1. data      verb-roots.tsv (Wîkîferheng "Rehê dema niha/borî ji lêkera X")
  2. rule-în   X-în  -> şimdiki gövde X        (nivîsîn -> nivîs)
     rule-andin X-andin -> şimdiki gövde X-în (kenandin -> kenîn)
  3. past stem her zaman mastardan kuralla: -in / -n düşer (kirin -> kir, çûn -> çû)
Kurala göre üretilen biçimler "generated" olarak işaretlenir; forms.tsv.gz içinde
aynı biçim varsa "attested" sayılır.

Kullanım: python scripts/paradigms.py
"""
import csv, gzip, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "kmr" / "db"
DOC = ROOT / "docs" / "dilbilgisi" / "paradigmalar.md"
csv.field_size_limit(sys.maxsize)

VOWELS = set("aeêiîouû")
PREVERBS = ["hil", "ve", "ra", "da", "der", "wer", "rû"]
PERSONS = ["ez", "tu", "ew", "em", "hûn", "ew (çoğul)"]

# Elle doğrulanmış düzensiz şimdiki gövdeler (Thackston 2006, Bedir Khan & Lescot 1970)
IRREGULAR_PRESENT = {
    "kirin": "k", "xwarin": "xw", "dîtin": "bîn", "çûn": "ç", "bûn": "b",
    "gotin": "bêj", "xwendin": "xwîn", "dan": "d", "anîn": "în", "birin": "b",
    "girtin": "gir", "ketin": "kev", "man": "mîn", "xwestin": "xwaz",
    "zanîn": "zan", "karîn": "kar", "rûniştin": "rûn", "hatin": "ê",
    "kuştin": "kuj", "avêtin": "avêj", "xistin": "x", "şûştin": "şo",
    "mirin": "mir", "kenîn": "ken", "razan": "raz", "hiştin": "hêl",
    "danîn": "tîn", "kirîn": "kir", "frotin": "firoş", "firotin": "firoş",
    "vexwarin": "vexw", "vekirin": "vek", "derketin": "derkev",
    "daketin": "dakev", "rabûn": "rab", "hilgirtin": "hilgir",
    "vegerîn": "veger", "gerîn": "ger", "nivîsîn": "nivîs",
    "bihîstin": "bihîz", "dizîn": "diz", "nêrîn": "nêr", "çêkirin": "çêk",
    "rêtin": "rêj", "nasîn": "nas", "şandin": "şîn", "pirsîn": "pirs",
}


def past_stem(inf):
    if inf.endswith("in"):
        return inf[:-2]
    if inf.endswith("n"):
        return inf[:-1]
    return None


KNOWN = set()


def preverb_of(inf):
    """Ön fiil yalnızca mastarın geri kalanı da bilinen bir fiilse kabul edilir (vekirin = ve + kirin)."""
    for p in PREVERBS:
        if inf.startswith(p) and inf[len(p):] in KNOWN:
            return p
    if inf == "rûniştin":
        return "rû"
    return ""


def pres_suffix(stem, idx):
    """idx 0..5: ez, tu, ew, em, hûn, ew(pl)"""
    v = stem[-1] in VOWELS
    if idx == 0:
        return "m" if v else "im"
    if idx == 1:
        return "yî" if v else "î"
    if idx == 2:
        return "" if v else "e"
    return "n" if v else "in"


def past_suffix(stem, idx):
    v = stem[-1] in VOWELS
    if idx == 0:
        return "m" if v else "im"
    if idx == 1:
        return "yî" if v else "î"
    if idx == 2:
        return ""
    return "n" if v else "in"


def conjugate(inf, pres, past):
    pv = preverb_of(inf)
    pres_core = pres[len(pv):] if pv and pres.startswith(pv) else pres
    past_core = past[len(pv):] if pv and past.startswith(pv) else past
    if inf == "danîn":
        pv, pres_core, past_core = "da", "tîn", "nî"
    out = {}
    hatin = inf == "hatin"

    def P(prefix, idx, stem=pres_core):
        return pv + prefix + stem + pres_suffix(stem, idx)

    # şimdiki/geniş zaman
    if hatin:
        out["present"] = ["têm", "têyî", "tê", "tên", "tên", "tên"]
        out["present_negative"] = ["nayêm", "nayî", "nayê", "nayên", "nayên", "nayên"]
        out["subjunctive"] = ["werim", "werî", "were", "werin", "werin", "werin"]
        out["subjunctive_negative"] = ["neyêm", "neyî", "neyê", "neyên", "neyên", "neyên"]
        out["imperative"] = ["were", "werin"]
        out["imperative_negative"] = ["neyê", "neyên"]
    else:
        neg = "ni" if inf in ("zanîn", "karîn") else "na"
        out["present"] = [P("di", i) for i in range(6)]
        out["present_negative"] = [P(neg, i) for i in range(6)]
        bi = "" if pv else "bi"
        out["subjunctive"] = [P(bi, i) for i in range(6)]
        out["subjunctive_negative"] = [P("ne", i) for i in range(6)]
        imp_sg = pv + bi + pres_core + ("" if pres_core[-1] in VOWELS else "e")
        imp_pl = pv + bi + pres_core + ("n" if pres_core[-1] in VOWELS else "in")
        out["imperative"] = [imp_sg, imp_pl]
        out["imperative_negative"] = [pv + "me" + pres_core + ("" if pres_core[-1] in VOWELS else "e"),
                                      pv + "me" + pres_core + ("n" if pres_core[-1] in VOWELS else "in")]
    out["future"] = [f"{p} ê {f}" if p != "tu" else f"{p} yê {f}"
                     for p, f in zip(["ez", "tu", "ew", "em", "hûn", "ew"], out["subjunctive"])]
    # geçmiş zamanlar (geçişsiz fiil kişi ekleri; geçişli fiilde ek NESNEYE uyar)
    pc = past_core
    out["past"] = [pv + pc + past_suffix(pc, i) for i in range(6)]
    out["past_negative"] = [pv + "ne" + pc + past_suffix(pc, i) for i in range(6)]
    out["past_progressive"] = [pv + "di" + pc + past_suffix(pc, i) for i in range(6)]
    v = pc[-1] in VOWELS
    perf = (["me", "yî", "ye", "ne", "ne", "ne"] if v else ["ime", "iyî", "iye", "ine", "ine", "ine"])
    out["present_perfect"] = [pv + pc + s for s in perf]
    plu = "bû" if v else "ibû"
    out["past_perfect"] = [pv + pc + plu + s for s in ["m", "yî", "", "n", "n", "n"]]
    # yazım kuralı: uzun î, y'den önce kısalır (derî -> deriyê; zanî -> zaniyî)
    return {k: [x.replace("îy", "iy") for x in v] for k, v in out.items()}


LABELS = [
    ("present", "Geniş/şimdiki zaman"), ("present_negative", "Olumsuz"),
    ("subjunctive", "Dilek kipi"), ("future", "Gelecek zaman"),
    ("past", "Di'li geçmiş"), ("past_negative", "Olumsuz geçmiş"),
    ("past_progressive", "Sürekli geçmiş"), ("present_perfect", "Miş'li geçmiş"),
    ("past_perfect", "Miş'li geçmişin hikâyesi"),
]


def main():
    # 1. veri gövdeleri
    data_pres, data_past = defaultdict(set), defaultdict(set)
    with open(DB / "verb-roots.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            m = re.search(r"Rehê dema (niha|borî) ji lêker(?:a|ên) ([^ (.,]+)", r["gloss_ku"])
            if not m or "devokî" in r["gloss_ku"]:
                continue
            stem = r["word"].replace("-", "")
            (data_pres if m.group(1) == "niha" else data_past)[m.group(2)].add(stem)

    verbs, gloss = [], {}
    with open(DB / "lemmas.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["upos"] == "VERB" and re.fullmatch(r"[a-zçêîşû]+", r["word"]) and r["word"].endswith("n"):
                verbs.append(r["word"])
                gloss[r["word"]] = (r.get("tr") or "").split(" | ")[0]
    verbs = sorted(set(verbs))
    KNOWN.update(verbs)

    attested = defaultdict(set)
    with gzip.open(DB / "forms.tsv.gz", "rt", encoding="utf-8") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3:
                attested[p[1]].add(p[0])

    stems_rows, n_par, n_att, n_gen = [], 0, 0, 0
    out_par = gzip.open(DB / "verb-paradigms.jsonl.gz", "wt", encoding="utf-8")
    paradigms = {}
    for inf in verbs:
        pa = past_stem(inf)
        if inf in IRREGULAR_PRESENT:
            pr, src = IRREGULAR_PRESENT[inf], "curated"
        elif inf in data_pres and len(data_pres[inf]) == 1:
            pr, src = next(iter(data_pres[inf])), "data"
        elif inf.endswith("andin"):
            pr, src = inf[:-5] + "în", "rule-andin"
        elif inf.endswith("în") and len(inf) > 4:
            pr, src = inf[:-2], "rule-în"
        else:
            stems_rows.append([inf, "", pa or "", "unknown-present", gloss.get(inf, "")])
            continue
        if inf in data_past and pa not in data_past[inf]:
            pa = sorted(data_past[inf])[0]
        stems_rows.append([inf, pr, pa, src, gloss.get(inf, "")])
        par = conjugate(inf, pr, pa)
        forms = {k: v for k, v in par.items()}
        att = sorted({w for v in par.values() for w in v} & attested.get(inf, set()))
        n_att += len(att)
        n_gen += sum(len(v) for v in par.values())
        out_par.write(json.dumps({"verb": inf, "present_stem": pr, "past_stem": pa,
                                  "stem_source": src, "forms": forms, "attested": att,
                                  "review_status": "generated"}, ensure_ascii=False) + "\n")
        paradigms[inf] = (pr, pa, src, par, set(att))
        n_par += 1
    out_par.close()

    with open(DB / "verb-stems.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["infinitive", "present_stem", "past_stem", "stem_source", "tr"])
        w.writerows(stems_rows)

    # 2. dokümantasyon
    md = ["# Çekim Tabloları (Paradigmalar)", "",
          "> Bu sayfa `scripts/paradigms.py` tarafından **otomatik** üretilir; elle düzenlemeyin.",
          "> İsim tabloları doğrudan Wîkîferheng'den alınan çekimli biçimlerdir (`forms.tsv.gz`).",
          "> Fiil tabloları [4. bölümdeki](04-fiil.md) kurallarla üretilir. **Kalın** biçimler veride de geçer (attested), diğerleri kural çıktısıdır ve kontrol edilmelidir.",
          "> Geçişli fiillerde geçmiş zaman kişi ekleri **nesneye** uyar (bkz. [ergatiflik](04-fiil.md#47-ergatiflik)); tabloda kişi sütunu bu durumda nesnenin kişisidir.",
          "", f"Toplam: {n_par:,} fiil için tam çekim, {n_gen:,} biçim; bunların {n_att:,} tanesi veride de var.", "",
          "## İsimler", ""]
    nouns = ["baran", "mal", "heval", "pisîk", "bajar", "dar", "keç", "kur"]
    noun_forms = defaultdict(dict)
    with gzip.open(DB / "forms.tsv.gz", "rt", encoding="utf-8") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 4 and p[1] in nouns and p[2] == "NOUN":
                t = set(p[3].split(","))
                num = "plural" if "plural" in t else "singular"
                det = "indefinite" if "indefinite" in t else "definite"
                case = next((c for c in ("direct", "oblique", "ezafe", "vocative") if c in t), None)
                if case:
                    gen = "f" if "feminine" in t else ("m" if "masculine" in t else "")
                    noun_forms[p[1]].setdefault((case, det, num), set()).add(p[0])
    rows = [("direct", "Yalın"), ("oblique", "Bükümlü"), ("ezafe", "İzafet"), ("vocative", "Seslenme")]
    for n in nouns:
        if n not in noun_forms:
            continue
        md += [f"### {n}", "", "| Hâl | Belirli tekil | Belirsiz tekil | Belirli çoğul | Belirsiz çoğul |", "|---|---|---|---|---|"]
        for c, lab in rows:
            cells = []
            for det, num in [("definite", "singular"), ("indefinite", "singular"), ("definite", "plural"), ("indefinite", "plural")]:
                v = noun_forms[n].get((c, det, num))
                if not v and c == "direct" and det == "definite":
                    v = {n}
                if not v and c == "vocative":
                    v = noun_forms[n].get((c, "definite", num))
                cells.append(" / ".join(sorted(v)) if v else "–")
            md.append(f"| {lab} | " + " | ".join(cells) + " |")
        md.append("")
    md += ["## Fiiller", ""]
    for inf in ["bûn", "kirin", "xwarin", "dîtin", "çûn", "hatin", "gotin", "xwendin", "nivîsîn",
                "zanîn", "vekirin", "rûniştin", "kenandin"]:
        if inf not in paradigms:
            continue
        pr, pa, src, par, att = paradigms[inf]
        md += [f"### {inf} ({gloss.get(inf, '')})", "",
               f"Şimdiki gövde: `{pr}` · Geçmiş gövde: `{pa}` · Gövde kaynağı: `{src}`", "",
               "| Zaman | " + " | ".join(PERSONS) + " |", "|---|" + "---|" * 6]
        for k, lab in LABELS:
            md.append(f"| {lab} | " + " | ".join(f"**{x}**" if x in att else x for x in par[k]) + " |")
        md.append(f"| Emir (tekil / çoğul) | {par['imperative'][0]} / {par['imperative'][1]} | olumsuz: {par['imperative_negative'][0]} | | | | |")
        md.append("")
    md += ["## Bütün fiiller", "",
           "- Gövdeler: [`data/kmr/db/verb-stems.tsv`](../../data/kmr/db/verb-stems.tsv)",
           "- Tam çekimler (JSON Lines): [`data/kmr/db/verb-paradigms.jsonl.gz`](../../data/kmr/db/verb-paradigms.jsonl.gz)", ""]
    DOC.write_text("\n".join(md), encoding="utf-8")
    print(f"verbs={len(verbs)} paradigms={n_par} forms={n_gen} attested={n_att}")
    from collections import Counter
    print(Counter(r[3] for r in stems_rows))


if __name__ == "__main__":
    main()
