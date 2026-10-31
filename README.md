# Ferhenga Pirzimanî · Kurdish Multilingual Lexicon

**Kürtçe ↔ Türkçe · Kürtçe ↔ İngilizce · Kürtçe ↔ Almanca**
Kurmancî · Soranî · Güney Kürtçesi · Zazakî (+ Goranî/Hewramî)

[English](README.en.md) · [Deutsch](README.de.md) · [Kurmancî](README.ku.md) · **Türkçe**

> ⚠️ **DURUM: TASLAK (v0.1). İnsan kontrolünden geçmedi.**
> Verinin tamamı açık kaynaklardan (Vikisözlük, Vikipedi) otomatik derlendi. Her satırda `review_status = unverified` yazar.
> Anadil konuşucularının katkısıyla kontrol edilecek: bkz. [KONTROL.md](KONTROL.md) · [CONTRIBUTING.md](CONTRIBUTING.md)

Kürtçe ile proje yapmak isteyen geliştiriciler, öğretmenler, çevirmenler ve araştırmacılar için **açık lisanslı, kaynağı her satırda izlenebilen**, dört dilli bir sözlük verisi ve araç seti. Amaç Kürtçe oyun, uygulama, eğitim materyali ve dil teknolojisi üretmeyi kolaylaştırmak.

---

## Neye ihtiyacın var? Buradan başla

| İhtiyacın | Dosya |
|---|---|
| Kurmancî kelimenin Türkçe, İngilizce ve Almanca karşılığını tek satırda görmek | [`data/multilingual/kmr-tr-en-de.tsv`](data/multilingual/) (32 bin kelime, sıklık sırasıyla) |
| En çok kullanılan kelimelerle başlamak (dil öğrenme, eğitim) | [`data/learner/kmr-top3000.tsv`](data/learner/) |
| Kelime oyunu (Wordle tarzı) için 3-7 harfli kelimeler | [`data/games/kmr-5-harf.tsv`](data/games/) vb. |
| Konulara göre kelime listesi (renkler, hayvanlar, aile, yiyecek, fiiller...) dört lehçede | [`data/themes/`](data/themes/) (17 konu, `themes.json`) |
| Lehçeler arası karşılıklar (Kurmancî ↔ Soranî, Zazakî, Güney Kürtçesi, Goranî) | [`data/cross-dialect.tsv`](data/cross-dialect.tsv) |
| En güvenilir çiftler (iki bağımsız kaynağın onayladığı) | [`data/core/`](data/core/) |
| Tüm ham çiftler | [`data/kmr/`](data/kmr/), [`data/ckb/`](data/ckb/), [`data/zza/`](data/zza/), [`data/sdh/`](data/sdh/), [`data/hac/`](data/hac/) |
| Kelime sıklığı (Kürtçe Vikipedi'den) | [`data/frequency/`](data/frequency/) (Kurmancî, Soranî, Zazakî; 50'şer bin kelime) |
| Alfabe, harf tabloları, ekran klavyesi düzenleri (JSON) | [`data/alphabets/`](data/alphabets/) |
| Kod: doğru büyük/küçük harf, sıralama, yazım düzeltme | [`tools/python/kurdi.py`](tools/python/kurdi.py), [`tools/js/kurdi.js`](tools/js/kurdi.js) |
| Oyun ya da uygulama geliştiriyorsan | [`docs/oyun-gelistirici-rehberi.md`](docs/oyun-gelistirici-rehberi.md) |
| Kürt dilinin tarihi, lehçeler, alfabeler | [`docs/tarih.md`](docs/tarih.md) · [`docs/lehceler.md`](docs/lehceler.md) · [`docs/alfabeler.md`](docs/alfabeler.md) |

## Kapsam ve sayılar

| Lehçe (ISO 639-3) | Yazı | Türkçe | İngilizce | Almanca |
|---|---|---:|---:|---:|
| Kurmancî `kmr` | Latin (Hawar) | 141.086 | 179.651 | 71.981 |
| Kurmancî, **çekirdek** (2+ kaynak) | | 5.519 | 1.456 | 2.120 |
| Soranî `ckb` | Arap kökenli | 91 + 929* | 1.628 + 738* | 246 + 908* |
| Zazakî `zza` | Latin | 9.936 + 779* | 1.231 + 564* | 495 + 769* |
| Güney Kürtçesi `sdh` | Arap kökenli | 358* | 323* | 371* |
| Goranî/Hewramî `hac` | Arap kökenli | 160* | 148* | 181* |

\* Kurmancî üzerinden türetilmiş (`.pivot.tsv`), en düşük güven. Ayrıntı: [`data/STATS.md`](data/STATS.md)

Ayrıca: 32.443 satırlık dört dilli tablo · 3.000 kelimelik öğrenici listesi · 6.686 oyun kelimesi (3-7 harf) · 17 konuda 263 kavram · 6.778 lehçeler arası eşleşme · 3 × 50.000 sıklık listesi.

> Kurmancî sayıları yüksek görünür, çünkü bir kelimenin her anlamı ve eş anlamlısı ayrı satır olur ve kaynaklar teknik terimler de içerir. Gerçek kullanım için `multilingual`, `learner`, `themes` ve `core` dosyalarıyla başlayın.

## Güven düzeyleri
Her dosyada güveni gösteren bir sütun vardır:
- `sources_agree`: aynı çifti kaç bağımsız Vikisözlük sürümü veriyor (2 ve üstü = daha güvenilir).
- `confidence` (`high` / `medium` / `low`): türetilmiş tablolarda kaynak uyumuna göre hesaplanır.
- `.pivot.tsv`: iki adımlı türetme (Soranî → Kurmancî → Türkçe gibi); en düşük güven.
- `review_status`: insan kontrolünün sonucu. Şu an hepsi `unverified`.

## Hızlı kullanım

**Python**
```python
import sys; sys.path.insert(0, 'tools/python')
from kurdi import Lexicon, upper, sort_key
lx = Lexicon('data')
lx.translate('pisîk', 'tr')   # ['kedi', ...]
lx.find('cat', 'en')          # ['pisîk', ...]
upper('pisîk')                # 'PISÎK'  (Türkçe kuralıyla 'PİSÎK' olurdu, yanlış)
```

**JavaScript**
```js
import { upper, compare, parseTSV } from './tools/js/kurdi.js';
const words = parseTSV(await (await fetch('data/games/kmr-5-harf.tsv')).text());
```

**SQLite** (tek dosyada sorgulanabilir veritabanı, ~75 MB; depoya eklenmez, üretilir)
```bash
python3 scripts/to_sqlite.py data kurdish_lexicon.sqlite
```

## Klasör yapısı
```
data/
  multilingual/  kmr-tr-en-de.tsv          dört dilli ana tablo
  learner/       kmr-top3000.tsv           en sık 3.000 kelime
  games/         kmr-3..7-harf.tsv         kelime oyunları için
  themes/        *.tsv, themes.json        konulu listeler (4 lehçe + TR/EN/DE)
  core/          kmr-*.core.tsv            2+ kaynağın onayladığı çiftler
  kmr/ ckb/ zza/ sdh/ hac/                 tüm çiftler (+ .pivot.tsv)
  cross-dialect.tsv                        lehçeler arası
  frequency/                               Vikipedi sıklık listeleri
  alphabets/                               alfabe ve klavye JSON'ları
  lexicon.jsonl.gz                         tüm doğrudan çiftler tek dosyada
docs/            tarih · lehçeler · alfabeler · oyun geliştirici rehberi · sıklık yöntemi
tools/           python/kurdi.py · js/kurdi.js · tests/
scripts/         build · core · frequency · derive · validate · to_sqlite · filter_de
```

## Yeniden üretme
Bütün veri betiklerle baştan üretilebilir: [`docs/yeniden-uretim.md`](docs/yeniden-uretim.md)

## Bilinen sınırlar
- Vikisözlük gönüllüler tarafından yazılır: hatalı, eksik, bölgesel ya da argo karşılıklar vardır (ör. *pisîk* için alakasız bir anlamdan gelen karşılıklar).
- Edat ve bağlaç gibi işlev sözcüklerinin çevirileri bağlama bağlıdır; öğrenici listesinde not düşülmüştür.
- Güney Kürtçesi ve Goranî için açık kaynak çok azdır; dosyaları yalnızca türetmedir.
- Sıklık listeleri ansiklopedi metninden çıkarıldı: günlük konuşma kelimeleri olduğundan daha nadir görünür.
- Hiçbir satır henüz anadil konuşucusu tarafından kontrol edilmedi.

## Lisans
- **Veri ve belgeler** (`data/`, `docs/`): **CC BY-SA 4.0**. Vikisözlük ve Vikipedi'den türetilmiştir. Kullanırken kaynak gösterin, türetilmiş veriyi aynı lisansla paylaşın: [DATA-LICENSE.md](DATA-LICENSE.md)
- **Kod** (`scripts/`, `tools/`): **MIT**: [LICENSE](LICENSE)
- Atıf: [CITATION.cff](CITATION.cff)

## Katkı
Kürtçenin herhangi bir kolunun anadil konuşucusuysanız en değerli katkı **kontroldür**. Bkz. [CONTRIBUTING.md](CONTRIBUTING.md). Hata bildirmek için *Issues → Düzeltme* şablonunu kullanın.

Bu depo [GameVan Studio](https://github.com/tankilicresul) tarafından, Kürtçe oyun ve eğitim projelerine açık bir temel sağlamak amacıyla başlatıldı. İlk derleme bir yapay zekâ asistanı (Claude) ile yapıldı.
