# Ferhenga Pirzimanî · Kurdish Multilingual Lexicon

**Kürtçe ↔ İngilizce · Kürtçe ↔ Almanca · Kürtçe ↔ Türkçe**
Kurmancî · Soranî · Güney Kürtçesi · Zazakî (+ Goranî/Hewramî)

> ⚠️ **DURUM: TASLAK. İnsan kontrolünden geçmedi.**
> Bu depodaki tüm kelime çiftleri açık kaynaklardan (Vikisözlük) otomatik olarak derlendi.
> Her satırda `review_status = unverified` yazar. Kontrol süreci için bkz. [KONTROL.md](KONTROL.md).
> Status: **draft, not human-reviewed.** Every row is marked `unverified`.

---

## Türkçe

### Bu depo nedir?
Kürtçenin dört ana kolu için İngilizce, Almanca ve Türkçe karşılıklı kelime listeleri, lehçeler arası eşleştirme tablosu ve Kürt dilinin tarihine dair kaynaklı bir özet. Amaç oyun, eğitim ve dil teknolojisi projelerinde kullanılabilecek, kaynağı her satırda izlenebilen açık bir sözlük verisi.

### Kapsanan diller (ISO 639-3)

| Kod | Ad | Yazı | Bu depodaki durum |
|---|---|---|---|
| `kmr` | Kurmancî (Kuzey Kürtçesi) | Latin (Hawar) | Geniş: EN, DE, TR doğrudan çiftler |
| `ckb` | Soranî (Orta Kürtçe) | Arap kökenli Kürt alfabesi | Orta: doğrudan EN/DE/TR + Kurmancî üzerinden türetilmiş |
| `sdh` | Güney Kürtçesi (Kelhurî, Feylî, Lekî vb.) | Arap kökenli | Az: yalnızca Kurmancî üzerinden türetilmiş |
| `zza` | Zazakî / Kirmanckî / Dimilî | Latin | Orta: doğrudan TR ağırlıklı + türetilmiş |
| `hac` | Goranî / Hewramî (ek) | Arap kökenli | Az: türetilmiş |

Zazakî ve Goranî'nin "Kürtçenin lehçesi" mi yoksa ayrı diller mi olduğu dilbilimde tartışmalıdır; ayrıntı için bkz. [docs/lehceler.md](docs/lehceler.md).

### Sayılar
Güncel sayılar: [data/STATS.md](data/STATS.md). Özet (ilk derleme):

| | EN | DE | TR |
|---|---:|---:|---:|
| Kurmancî doğrudan | ~221 bin | ~85 bin | ~166 bin |
| Kurmancî, 2+ kaynağın onayladığı **çekirdek** | 1.456 | 2.121 | 5.523 |
| Soranî doğrudan / türetilmiş | 1.628 / 738 | 246 / 908 | 91 / 929 |
| Zazakî doğrudan / türetilmiş | 1.231 / 564 | 495 / 769 | 9.937 / 780 |
| Güney Kürtçesi türetilmiş | 323 | 371 | 358 |

Lehçeler arası (Kurmancî ↔ diğerleri): Soranî 5.104 · Zazakî 2.860 · Güney Kürtçesi 1.028 · Goranî 265 eşleşme.

> Kurmancî sayıları yüksek görünür çünkü bir kelimenin birden fazla anlamı ve eş anlamlısı ayrı satır olur, ve kaynaklar teknik terimleri de içerir. Kontrole **çekirdek** dosyalardan başlanmalı.

### Klasör yapısı
```
data/
  core/          kmr-en/de/tr.core.tsv  → 2+ bağımsız kaynağın onayladığı çiftler (kontrole buradan başla)
  kmr/           kmr-en.tsv, kmr-de.tsv, kmr-tr.tsv
  ckb/ zza/      <kod>-<dil>.tsv (doğrudan) ve <kod>-<dil>.pivot.tsv (Kurmancî üzerinden türetilmiş)
  sdh/ hac/      yalnızca .pivot.tsv
  cross-dialect.tsv   Kurmancî ↔ Soranî / Güney / Zazakî / Goranî
  lexicon.jsonl.gz    tüm doğrudan çiftler tek dosyada
  STATS.md
docs/            tarih.md · lehceler.md · alfabeler.md
scripts/         build.py (veriyi kaynaklardan yeniden üretir) · core.py
KAYNAKLAR.md     tüm kaynaklar ve lisansları
KONTROL.md       insan kontrolü süreci ve kuralları
```

### Sütunlar
`kurdish` · `variety` · `script` (latn/arab) · `pos` · `lang` (en/de/tr) · `translation` · `sense` · `sources_agree` (kaç bağımsız kaynak aynı çifti veriyor) · `source` · `source_url` · `review_status`

**Güven sırası:** `sources_agree ≥ 2` > tek kaynak > `.pivot` (iki adımlı türetme, en düşük güven).

### Bilinen sınırlar
- Vikisözlük gönüllüler tarafından yazılır; hatalı, eksik ya da bölgesel çiftler vardır.
- Bir kelimenin farklı anlamları ayrı ayrı gelir (ör. *pisîk* → *kedi* doğru, ama başka bir anlamdan gelen alakasız karşılıklar da olabilir).
- Güney Kürtçesi ve Goranî için doğrudan kaynak çok azdır; dosyalar yalnızca türetmedir.
- Soranî için Latin harfli yazımlar ve Arap harfli yazımlar karışık gelebilir.
- Hiçbir satır anadil konuşucusu tarafından kontrol edilmemiştir.

### Yeniden üretme
```bash
mkdir raw && cd raw
curl -O https://kaikki.org/dictionary/downloads/ku/ku-extract.jsonl.gz && mv ku-extract.jsonl.gz ku.jsonl.gz
curl -O https://kaikki.org/dictionary/downloads/tr/tr-extract.jsonl.gz && mv tr-extract.jsonl.gz tr.jsonl.gz
curl -o en-NorthernKurdish.jsonl "https://kaikki.org/dictionary/Northern%20Kurdish/kaikki.org-dictionary-NorthernKurdish.jsonl"
curl -o en-CentralKurdish.jsonl "https://kaikki.org/dictionary/Central%20Kurdish/kaikki.org-dictionary-CentralKurdish.jsonl"
curl -o en-Zazaki.jsonl "https://kaikki.org/dictionary/Zazaki/kaikki.org-dictionary-Zazaki.jsonl"
curl -s https://kaikki.org/dictionary/downloads/de/de-extract.jsonl.gz | python3 ../scripts/filter_de.py > de-kurdish.jsonl   # ~300 MB akış, yalnızca Kürtçe satırlar saklanır
cd .. && python3 scripts/build.py raw data && python3 scripts/core.py data
```

### Lisans
- **Veri** (`data/`): Vikisözlük'ten türetildiği için **CC BY-SA 4.0** (ve GFDL). Kullananlar kaynak göstermeli ve türetilmiş veriyi aynı lisansla paylaşmalıdır. Bkz. [DATA-LICENSE.md](DATA-LICENSE.md).
- **Kod** (`scripts/`): **MIT**. Bkz. [LICENSE](LICENSE).
- **Belgeler** (`docs/`): CC BY-SA 4.0.

---

## English

A multilingual Kurdish lexicon (Kurdish ↔ English / German / Turkish) for Kurmanji (`kmr`), Sorani (`ckb`), Southern Kurdish (`sdh`) and Zazaki (`zza`), plus Gorani/Hewrami (`hac`), compiled automatically from Wiktionary via [Wiktextract/kaikki.org](https://kaikki.org/). Each row keeps its source URL and a review status. **Nothing has been human-reviewed yet.** Start reviewing from `data/core/` (pairs confirmed by two independent Wiktionary editions). Data: CC BY-SA 4.0. Code: MIT. A sourced summary of the history of the Kurdish language is in `docs/tarih.md` (Turkish).

## Deutsch

Mehrsprachiges kurdisches Wörterbuch (Kurdisch ↔ Englisch / Deutsch / Türkisch) für Kurmandschi, Sorani, Südkurdisch und Zazaki, automatisch aus dem Wiktionary erstellt. **Entwurf, noch nicht von Muttersprachlern geprüft.** Daten: CC BY-SA 4.0, Code: MIT.

## Kurmancî

Ferhengeke pirzimanî ya kurdî (Kurdî ↔ Îngilîzî / Almanî / Tirkî) ji bo Kurmancî, Soranî, Kurdiya başûrî û Zazakî. Hemû dane ji Wîkîferhengê bi awayekî xweber hatine berhevkirin. **Reşnivîs e; hîn ji aliyê axêverên zikmakî ve nehatiye kontrolkirin.**

> Kurmancî ve Almanca bölümler kontrol edilmeden yazılmıştır; anadil konuşucusu tarafından düzeltilmelidir.
