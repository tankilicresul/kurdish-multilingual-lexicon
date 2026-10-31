#!/usr/bin/env python3
"""Dış başvuru kaynaklarına karşı nicel değerlendirme.

Başvuru kaynakları (depoya KOPYALANMAZ, yalnızca karşılaştırma için indirilir):
  - UniMorph kmr   https://github.com/unimorph/kmr          (CC BY-SA 3.0)
  - UD Kurmanji-MG https://github.com/UniversalDependencies/UD_Northern_Kurdish-Kurmanji (eski adı UD_Kurmanji-MG; CC BY-SA 4.0)

Kullanım:
  git clone --depth 1 https://github.com/unimorph/kmr.git            ext/um-kmr
  git clone --depth 1 https://github.com/UniversalDependencies/UD_Northern_Kurdish-Kurmanji.git ext/ud-kmr
  python scripts/evaluate.py ext
Çıktı: data/EVAL.json, docs/degerlendirme-sonuclari.md
"""
import csv, gzip, json, re, sys, random
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "kmr" / "db"
csv.field_size_limit(sys.maxsize)
sys.path.insert(0, str(ROOT / "scripts"))
from standards import slot_features, SLOT_UM  # noqa: E402


def load_unimorph(path):
    um = defaultdict(lambda: defaultdict(set))  # lemma -> featset -> forms
    pairs = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 3:
                continue
            um[p[0]][frozenset(p[2].split(";"))].add(p[1])
            pairs.add((p[0], p[1]))
    return um, pairs


def eval_paradigms(um):
    sf = slot_features()
    by_slot = defaultdict(Counter)
    disagreements = []
    verbs = 0
    with gzip.open(DB / "verb-paradigms.jsonl.gz", "rt", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            ref = um.get(d["verb"])
            if not ref:
                continue
            hit_any = False
            for slot in SLOT_UM:
                for i, form in enumerate(d["forms"][slot]):
                    if i > 3:
                        break  # çoğul kişiler aynı biçim
                    gold = ref.get(sf[(slot, i)])
                    if not gold:
                        continue
                    hit_any = True
                    ok = form in gold
                    by_slot[slot]["match" if ok else "mismatch"] += 1
                    if not ok:
                        disagreements.append((d["verb"], slot, i, form, " / ".join(sorted(gold)), d["stem_source"]))
            verbs += hit_any
    tot = Counter()
    for c in by_slot.values():
        tot.update(c)
    src = Counter(x[5] for x in disagreements)
    return verbs, by_slot, tot, disagreements, src


def mismatch_category(form, gold):
    """Uyuşmazlığın türü. İlk dört tür, UniMorph kmr'deki sistematik yazım sorunlarıdır:
    standart yazımda (Bedirxan; Thackston 2006) bu biçimler bizimkisi gibi yazılır."""
    g = gold.split(" / ")
    if any(x == form + "i" for x in g):
        return "um-final-i"          # *xwendi*, *nehati*: geçmiş 3. tekilde fazladan -i
    if any(x.replace("îy", "iy").replace("îin", "în").replace("îi", "î") == form for x in g):
        return "um-i-orthography"    # *zivirîyî*: î, y'den önce kısalır (ziviriyî)
    if any(re.sub(r"(?<=[^aeêiîouû])yî$", "î", x) == form for x in g):
        return "um-yi-after-consonant"  # *nenalyî* (nenalî)
    for x in g:
        x0 = x[:-1] if x.endswith("i") and not form.endswith("i") else x
        for pv in ("hil", "ve", "ra", "da", "der", "wer", "rû"):
            pre = x0[:2]
            if pre in ("di", "na", "ne", "bi") and x0[2:].startswith(pv):
                if form == pv + pre + x0[2 + len(pv):] or (pre == "bi" and form == x0[2:]):
                    return "um-preverb-order"  # *dihilgirî* (hildigirî): ek ön fiilden sonra gelir
    return "other"


def eval_attested(um_pairs):
    ours = set()
    with gzip.open(DB / "forms.tsv.gz", "rt", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["lemma"]:
                ours.add((r["lemma"], r["form"]))
    inter = ours & um_pairs
    return len(ours), len(um_pairs), len(inter)


def load_ud(d):
    toks = []
    for fp in sorted(Path(d).glob("*.conllu")):
        for line in open(fp, encoding="utf-8"):
            p = line.rstrip("\n").split("\t")
            if len(p) == 10 and p[0].isdigit():
                toks.append((p[1], p[2], p[3]))
    return toks


def eval_ud(toks):
    lem_upos = defaultdict(set)
    with open(DB / "lemmas.tsv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            lem_upos[r["word"].lower()].add(r["upos"])
    form_lem = defaultdict(set)
    with gzip.open(DB / "forms.tsv.gz", "rt", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["lemma"]:
                form_lem[r["form"].lower()].add(r["lemma"].lower())
    content = [t for t in toks if t[2] not in ("PUNCT", "NUM", "SYM", "X")]
    covered = sum(1 for f, l, u in content if f.lower() in lem_upos or f.lower() in form_lem)
    # lemmatizasyon: biçim tabloda varsa, UD lemması adaylar arasında mı?
    lem_tot = lem_ok = 0
    for f, l, u in content:
        fl = f.lower()
        cands = set(form_lem.get(fl, set()))
        if fl in lem_upos:
            cands.add(fl)
        if cands and fl != l.lower():
            lem_tot += 1
            lem_ok += l.lower() in cands
    # sözcük türü: UD lemması sözlükte varsa, UD'nin UPOS'u sözlüğün UPOS kümesinde mi?
    pos_tot = pos_ok = 0
    single_tot = single_ok = 0
    pos_conf = Counter()
    for f, l, u in content:
        s = lem_upos.get(l.lower())
        if s:
            pos_tot += 1
            if len(s) == 1:
                single_tot += 1
                single_ok += (u in s or (u == "PROPN" and "NOUN" in s) or (u == "AUX" and "VERB" in s))
            if u in s or (u == "PROPN" and "NOUN" in s) or (u == "AUX" and "VERB" in s):
                pos_ok += 1
            else:
                pos_conf[(u, "/".join(sorted(s)))] += 1
    return dict(tokens=len(toks), content_tokens=len(content), coverage=covered / len(content),
                lemma_eval_n=lem_tot, lemma_acc=lem_ok / max(lem_tot, 1),
                pos_eval_n=pos_tot, pos_acc=pos_ok / max(pos_tot, 1),
                pos_single_n=single_tot, pos_single_acc=single_ok / max(single_tot, 1),
                pos_majority_baseline=Counter(u for f, l, u in content if lem_upos.get(l.lower())).most_common(1)[0][1] / max(pos_tot, 1),
                pos_confusions=[f"{a} → {b}: {n}" for (a, b), n in pos_conf.most_common(8)])


def pct(x):
    return f"{100 * x:.1f}%"


def main(ext):
    ext = Path(ext)
    um, um_pairs = load_unimorph(ext / "um-kmr" / "kmr")
    verbs, by_slot, tot, dis, src = eval_paradigms(um)
    n_ours, n_um, n_inter = eval_attested(um_pairs)
    ud = eval_ud(load_ud(ext / "ud-kmr"))
    cats = Counter(mismatch_category(x[3], x[4]) for x in dis)
    rev = ROOT / "data" / "kmr" / "review"
    rev.mkdir(exist_ok=True)
    with open(rev / "paradigms-vs-unimorph.tsv", "w", encoding="utf-8") as f:
        f.write("verb\tslot\tperson\tours\tunimorph\tstem_source\tcategory\tdecision\n")
        for v, slot, i, form, gold, s in sorted(dis):
            f.write(f"{v}\t{slot}\t{['1sg', '2sg', '3sg', 'pl'][i]}\t{form}\t{gold}\t{s}\t{mismatch_category(form, gold)}\t\n")
    random.seed(1)
    other = [x for x in dis if mismatch_category(x[3], x[4]) == "other"]
    sample = random.sample(other, min(25, len(other)))
    res = dict(
        paradigms_vs_unimorph=dict(verbs=verbs, cells=sum(tot.values()), match=tot["match"],
                                   acc=tot["match"] / max(sum(tot.values()), 1),
                                   by_slot={k: dict(v) for k, v in by_slot.items()},
                                   mismatches_by_stem_source=dict(src),
                                   mismatches_by_category=dict(cats),
                                   acc_excluding_unimorph_artifacts=(tot["match"] + sum(v for k, v in cats.items() if k != "other")) / max(sum(tot.values()), 1)),
        attested_vs_unimorph=dict(ours=n_ours, unimorph=n_um, overlap=n_inter),
        ud_kurmanji_mg=ud,
    )
    (ROOT / "data" / "EVAL.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    md = ["# Değerlendirme Sonuçları", "",
          "> `scripts/evaluate.py` tarafından otomatik üretilir. Yöntem: [degerlendirme.md](degerlendirme.md).", "",
          "## 1. Kural tabanlı fiil çekimi ↔ UniMorph kmr", "",
          f"UniMorph'ta da bulunan **{verbs:,}** fiil, **{sum(tot.values()):,}** çekim hücresi. "
          f"Ham eşleşme: **{pct(res['paradigms_vs_unimorph']['acc'])}**. "
          "Bir hücrede UniMorph birden fazla biçim veriyorsa, bizim biçimimizin bunlardan **herhangi biri** olması eşleşme sayılır.", "",
          "> **Sınırlılıklar.** (1) Bağımsızlık sınırlı: UniMorph kmr de büyük olasılıkla Vikisözlük kaynaklıdır. "
          "(2) Örneklem yanlı: 3.982 fiilden yalnızca UniMorph'ta da bulunanlar (çoğu sık ve düzensiz fiiller) ölçülür. "
          "(3) Bağımsız test kümesi yok: elle girilen gövdeler (`curated`) ve *anîn* düzeltmesi bu karşılaştırma görüldükten sonra yapıldı. "
          "(4) Miş'li geçmiş ve hikâyesindeki %100 uyum beklenen bir sonuçtur: bu yuvalar geçmiş gövdeye düzenli ek eklenerek kurulur; UniMorph'ta da büyük olasılıkla "
          "aynı kuralla üretilmiştir (doğrulanmadı). Kuralın doğruluğundan çok iki kaynağın aynı kuralı izlediğini gösterebilir.", "",
          "| Yuva | Eşleşen | Eşleşmeyen | Oran |", "|---|---:|---:|---:|"]
    for k in SLOT_UM:
        c = by_slot.get(k, Counter())
        n = c["match"] + c["mismatch"]
        if n:
            md.append(f"| {k} | {c['match']:,} | {c['mismatch']:,} | {pct(c['match'] / n)} |")
    md += ["", "Eşleşmeyenlerin gövde kaynağına göre dağılımı: " +
           ", ".join(f"`{k}` {v:,}" for k, v in src.most_common()), "",
           "**Uyuşmazlıkların ön sınıflandırması.** Aşağıdaki türler, uyuşmazlıklar görüldükten **sonra**, standart yazım kurallarına (BL 1970; Th 2006) "
           "dayanarak tarafımızdan tanımlandı. İlk dört türde bizim değerlendirmemize göre UniMorph biçimi standart yazıma uymuyor. "
           "Bu sınıflandırma **henüz bir uzman tarafından yargılanmadı**:", "",
           "| Tür | Sayı | Açıklama |", "|---|---:|---|",
           f"| `um-final-i` | {cats['um-final-i']:,} | UniMorph geçmiş zaman 3. tekilde sonda *-i* veriyor (*xwendi*; standart yazımda beklenen *xwend*) |",
           f"| `um-i-orthography` | {cats['um-i-orthography']:,} | *î* + *y* yazımı (*zivirîyî*; bizim kuralımız *ziviriyî*. Uzun *î*'nin *y*'den önce kısalması, kaynakta sayfa düzeyinde doğrulanmadı) |",
           f"| `um-yi-after-consonant` | {cats['um-yi-after-consonant']:,} | Ünsüzden sonra *-yî* (*nenalyî*; standart yazımda beklenen *nenalî*) |",
           f"| `um-preverb-order` | {cats['um-preverb-order']:,} | Ön fiilli fiillerde ek sırası (*dihilgirî*; standart yazımda beklenen *hildigirî*) |",
           f"| `other` | {cats['other']:,} | Elle incelenmeli (aşağıda örnekler) |", "",
           f"Bu dört tür bizim lehimize sayılırsa uyum **{pct(res['paradigms_vs_unimorph']['acc_excluding_unimorph_artifacts'])}** olur. "
           "Bu bir doğruluk ölçüsü değil, yargılanmamış bir **üst tahmindir**. Doğruluk ölçüsü olarak ham oran kullanılmalıdır. "
           "Uzman kararı, her türden rastgele örneklem üzerinde `decision` sütununa girilecek (bkz. KONTROL.md). "
           "Tüm uyuşmazlıklar karar sütunuyla birlikte: [`data/kmr/review/paradigms-vs-unimorph.tsv`](../data/kmr/review/paradigms-vs-unimorph.tsv).", "",
           "`other` türünden rastgele 25 örnek:", "",
           "| Fiil | Yuva | Kişi | Bizim | UniMorph | Gövde kaynağı |", "|---|---|---|---|---|---|"]
    for v, slot, i, form, gold, s in sorted(sample):
        md.append(f"| {v} | {slot} | {['1sg', '2sg', '3sg', 'pl'][i]} | {form} | {gold} | {s} |")
    md += ["", "## 2. Veride geçen çekimli biçimler ↔ UniMorph kmr", "",
           f"Bizim (lemma, biçim) çiftimiz: {n_ours:,} · UniMorph: {n_um:,} · ortak: {n_inter:,}. "
           "İki kaynak büyük ölçüde farklı kelimeleri kapsıyor; birbirini tamamlıyor.", "",
           "## 3. UD Kurmanji-MG ağaç bankası", "",
           f"{ud['tokens']:,} sözcük birimi ({ud['content_tokens']:,} tanesi noktalama, sayı, simge ve X dışı).", "",
           "| Ölçüt | Değer | n |", "|---|---:|---:|",
           f"| Sözlük kapsamı (biçim sözlükte ya da çekim tablosunda var) | {pct(ud['coverage'])} | {ud['content_tokens']:,} |",
           f"| Kök bulma (çekimli biçim için doğru lemma adaylar arasında) | {pct(ud['lemma_acc'])} | {ud['lemma_eval_n']:,} |",
           f"| Sözcük türü uyumu (UD UPOS, sözlükteki UPOS kümesinde) | {pct(ud['pos_acc'])} | {ud['pos_eval_n']:,} |",
           f"| ↳ yalnızca sözlükte tek UPOS'u olan lemmalar | {pct(ud['pos_single_acc'])} | {ud['pos_single_n']:,} |",
           f"| ↳ karşılaştırma: en sık UPOS'u her yere atayan taban çizgisi | {pct(ud['pos_majority_baseline'])} | {ud['pos_eval_n']:,} |",
           "", "> Bir lemmanın sözlükte birden fazla sözcük türü olabildiği için küme ölçütü iyimserdir; tek etiketli satır daha katı bir ölçüdür. "
           "Uyuşmazlıkların bir kısmı hata değil şema farkıdır: ör. UD işaret sözcüklerini isim önünde DET olarak etiketler, Wîkîferheng ise *ev*, *ew* gibi sözcükleri zamir (PRON) olarak kaydeder. "
           "Ağaç bankası küçüktür ve belirli metin türlerinden oluşur; bu oranlar genel kullanımı temsil etmez.",
           "", "En sık sözcük türü uyuşmazlıkları (UD → sözlük): " + "; ".join(ud["pos_confusions"]), ""]
    (ROOT / "docs" / "degerlendirme-sonuclari.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1)[:2500])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ext")
