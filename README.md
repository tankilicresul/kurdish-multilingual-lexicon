# Ferhenga Pirzimanî · Kurdish Multilingual Lexicon

**Sözlük veritabanı · Betimleyici dil bilgisi · Etimoloji** · Kürtçe ↔ Türkçe · İngilizce · Almanca
Kurmancî · Soranî · Güney Kürtçesi · Zazakî (+ Goranî/Hewramî)

[English](README.en.md) · [Deutsch](README.de.md) · [Kurmancî](README.ku.md) · **Türkçe**

> ⚠️ **DURUM: TASLAK (v0.4). İnsan kontrolünden geçmedi.**
> Verinin tamamı açık kaynaklardan (Vikisözlük, Vikipedi) otomatik derlendi. Her satırda `review_status = unverified` yazar.
> Anadil konuşucularının katkısıyla kontrol edilecek: bkz. [KONTROL.md](KONTROL.md) · [CONTRIBUTING.md](CONTRIBUTING.md)

Kürtçe ile çalışan araştırmacılar, geliştiriciler, öğretmenler ve çevirmenler için açık lisanslı bir kaynak. Kaynağı her satırda izlenebilir. Uluslararası standartlara bağlıdır:
- **Sözlük veritabanı:** 5 Kürtçe çeşidi; Türkçe, İngilizce ve Almanca karşılıklar.
- **CLDF Dictionary** biçiminde dışa aktarım.
- **UD ve UniMorph** biçimbilim etiketleri.
- **Betimleyici Kurmancî dil bilgisi:** Türkçe, Leipzig glosslu örneklerle.
- **Köken sınıflandırması.**
- **Nicel değerlendirme:** UniMorph ve UD Kurmanji ağaç bankasına karşı.

| Standart | Kullanım | Ayrıntı |
|---|---|---|
| ISO 639-3 · Glottolog | dil kimlikleri | [standartlar.md](docs/standartlar.md#dil-kodları) |
| UD UPOS + özellikler · UniMorph | sözcük türü ve çekim etiketleri | [standartlar.md](docs/standartlar.md) |
| CLDF Dictionary | sözlüğün makine okunur, doğrulanmış dışa aktarımı | [`cldf/`](cldf/) |
| Leipzig Glossing Rules · WALS | dil bilgisi örnekleri ve tipolojik profil | [dil bilgisi §0](docs/dilbilgisi/00-giris-ve-yontem.md) |
| Datasheets for Datasets · FAIR · CFF | veri belgesi, atıf, arşivleme | [DATASHEET.md](DATASHEET.md) · [CITATION.cff](CITATION.cff) |

**Otomatik ölçümler** (insan doğrulaması yok; [yöntem ve sınırlılıklar](docs/degerlendirme.md) · [sonuçlar](docs/degerlendirme-sonuclari.md)):
- UD Kurmanji ağaç bankası (n = 8.729 sözcük birimi): kelimelerin **%82,7**'si sözlükte bulunuyor.
- Sözcük türü uyumu: sözlükte tek sözcük türü olan lemmalarda **%89,2** (n = 3.991). En sık etiket taban çizgisi %30,7.
- Kural tabanlı fiil çekimi, UniMorph kmr ile ham **%77,4** eşleşiyor (147 fiil, 3.872 hücre). Uyuşmazlıkların çoğu ön incelemede UniMorph yazımından kaynaklanıyor görünüyor; bu sınıflandırma uzman kararını bekliyor.

---

## Neye ihtiyacın var? Buradan başla

| İhtiyacın | Dosya |
|---|---|
| **Betimleyici Kurmancî dil bilgisi** (Türkçe; kaynaklı, Leipzig glosslu örnekler, tipolojik profil, terim karşılıkları) | [`docs/dilbilgisi/`](docs/dilbilgisi/README.md) |
| Öğretim materyali (alıştırmalar ve cevap anahtarı) | [`docs/ogretim/`](docs/ogretim/README.md) |
| **Sözlüğü CLDF olarak** (pycldf, R, CLLD uygulamaları) | [`cldf/`](cldf/) |
| Çekim verisini **UniMorph** biçiminde (biçimbilim modelleri için) | [`data/kmr/unimorph/`](data/kmr/unimorph/) |
| **Bir kelime Kürtçe mi, nereden gelmiş?** Miras / iç türetme / alıntı (hangi dilden, hangi yoldan) / yansıma | [`data/kmr/db/etymology-class.tsv`](data/kmr/db/etymology-class.tsv) · [etimoloji rehberi](docs/etimoloji.md) |
| Fiil çekimleri (9 zaman × 6 kişi, olumsuz, emir) | [`verb-paradigms.jsonl.gz`](data/kmr/db/verb-paradigms.jsonl.gz) (3.982 fiil) · [`verb-stems.tsv`](data/kmr/db/verb-stems.tsv) · [örnek tablolar](docs/dilbilgisi/paradigmalar.md) |
| Kurmancî kelimenin Türkçe, İngilizce ve Almanca karşılığını tek satırda görmek | [`data/multilingual/kmr-tr-en-de.tsv`](data/multilingual/) (32 bin kelime, sıklık sırasıyla) |
| En çok kullanılan kelimelerle başlamak (dil öğrenme, eğitim) | [`data/learner/kmr-top3000.tsv`](data/learner/) |
| Kelime oyunu (Wordle tarzı) için 3-7 harfli kelimeler | [`data/games/kmr-5-harf.tsv`](data/games/) vb. |
| Konulara göre kelime listesi (renkler, hayvanlar, aile, yiyecek, fiiller...) dört lehçede | [`data/themes/`](data/themes/) (17 konu, `themes.json`) |
| Lehçeler arası karşılıklar (Kurmancî ↔ Soranî, Zazakî, Güney Kürtçesi, Goranî) | [`data/cross-dialect.tsv`](data/cross-dialect.tsv) |
| En güvenilir çiftler (iki bağımsız kaynağın onayladığı) | [`data/core/`](data/core/) |
| **Dilbilimsel veritabanı:** her kelimenin sözcük türü (isim, fiil, sıfat, zarf...), cinsiyeti, tanımları, örnek cümleleri, etimolojisi, ek-kök ayrımı, okunuşu (IPA), hecelemesi, eş/zıt anlamlıları | [`data/kmr/db/lemmas.tsv`](data/kmr/db/) (158 bin madde) · [veritabanı rehberi](docs/veritabani.md) |
| Çekimli biçimler → kök + dil bilgisi etiketleri (hâl, sayı, kişi, zaman...) | [`data/kmr/db/forms.tsv.gz`](data/kmr/db/) (330 bin biçim) |
| Etimoloji (köken) | [`data/*/db/etymology.tsv`](data/kmr/db/) (Kurmancî 86.916 madde) |
| Ekler ve fiil gövdeleri | [`affixes.tsv`](data/kmr/db/), [`verb-roots.tsv`](data/kmr/db/) |
| Atasözleri ve deyimler | [`data/kmr/db/proverbs-idioms.tsv`](data/kmr/db/) (21.009) |
| Anadil konuşucularının ses kayıtları (bağlantı) | [`data/kmr/db/audio.tsv`](data/kmr/db/) (3.099 kayıt) |
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

**Dilbilimsel veritabanı** ([ayrıntı](docs/veritabani.md)):

| | Kurmancî | Soranî | Zazakî | Güney | Goranî |
|---|---:|---:|---:|---:|---:|
| Madde başı (sözcük türüyle) | 158.393 | 7.232 | 3.314 | 819 | 167 |
| Çekimli biçim → kök | 329.942 | 49 | 89 | – | – |
| Etimolojisi olan | 86.916 | 1.201 | 675 | 353 | 21 |
| Ek / fiil gövdesi | 561 / 531 | 41 / 2 | 20 / 1 | 6 / – | 5 / – |
| Atasözü ve deyim | 21.009 | 15 | 2 | 3 | 1 |
| Ses kaydı | 3.099 | 3 | 35 | 4 | – |
| Köken sınıfı (etimoloji) | 156.692 | – | – | – | – |
| Fiil çekim tablosu | 3.982 fiil / 254.848 biçim | – | – | – | – |

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
  kmr/db/ ckb/db/ zza/db/ sdh/db/ hac/db/  dilbilimsel veritabanı (madde, çekim, etimoloji, ek, kök, atasözü, ses)
  kmr/unimorph/                            UniMorph biçiminde çekimler (veride geçen + kuralla üretilen)
  kmr/review/                              insan kararı bekleyen karşılaştırma listeleri
  DB-STATS.json · EVAL.json
cldf/            CLDF Dictionary (entries, senses, examples, languages, sources.bib)
docs/dilbilgisi/ betimleyici Kurmancî dil bilgisi (§0–7 + terimler + paradigmalar)
docs/ogretim/    alıştırmalar
docs/            standartlar · değerlendirme · etimoloji · kaynakca.bib · tarih · lehçeler · alfabeler · veritabanı · oyun geliştirici rehberi · sıklık yöntemi
tools/           python/kurdi.py · js/kurdi.js · tests/
scripts/         build · build_db · etymology_classify · paradigms · standards · evaluate · core · frequency · derive · validate · to_sqlite · filter_de
```

## Yeniden üretme
Bütün veri betiklerle baştan üretilebilir: [`docs/yeniden-uretim.md`](docs/yeniden-uretim.md)

## Bilinen sınırlar
- Vikisözlük gönüllüler tarafından yazılır: hatalı, eksik, bölgesel ya da argo karşılıklar vardır (ör. *pisîk* için alakasız bir anlamdan gelen karşılıklar).
- Edat ve bağlaç gibi işlev sözcüklerinin çevirileri bağlama bağlıdır; öğrenici listesinde not düşülmüştür.
- Güney Kürtçesi ve Goranî için açık kaynak çok azdır; dosyaları yalnızca türetmedir.
- Sıklık listeleri ansiklopedi metninden çıkarıldı: günlük konuşma kelimeleri olduğundan daha nadir görünür.
- Köken sınıflandırması otomatiktir: maddelerin %57'sinde kaynakta köken bilgisi yok (`unknown`). Bazı ortak İrani kelimeler yanlışlıkla Farsça alıntı görünür ([ayrıntı](docs/etimoloji.md#6-bilinen-sorunlar)).
- Fiil çekimleri kuralla üretildi. Yalnızca kalın gösterilen biçimler veride de geçer. Düzensiz fiillerde hata olabilir.
- Dil bilgisi standart yazı dilini anlatır. Ağız farkları yalnızca notlarla belirtildi. Bölümler ikincil bir derlemedir, yeni bir dilbilimsel iddia içermez.
- Zazakî verisi `zza` makro kodu altındadır. Kirmancki (`kiu`) ve Dimilî (`diq`) ayrımı kaynakta yapılmadığı için korunamadı.
- Hiçbir satır henüz anadil konuşucusu tarafından kontrol edilmedi.

## Lisans
- **Veri ve belgeler** (`data/`, `docs/`): **CC BY-SA 4.0**. Vikisözlük ve Vikipedi'den türetilmiştir. Kullanırken kaynak gösterin, türetilmiş veriyi aynı lisansla paylaşın: [DATA-LICENSE.md](DATA-LICENSE.md)
- **Kod** (`scripts/`, `tools/`): **MIT**: [LICENSE](LICENSE)
- Atıf: [CITATION.cff](CITATION.cff) (GitHub'da "Cite this repository" düğmesi). Kaynakça: [docs/kaynakca.bib](docs/kaynakca.bib)

## Katkı
Kürtçenin herhangi bir kolunun anadil konuşucusuysanız en değerli katkı **kontroldür**. Bkz. [CONTRIBUTING.md](CONTRIBUTING.md). Hata bildirmek için *Issues → Düzeltme* şablonunu kullanın.

Bu depo [GameVan Studio](https://github.com/tankilicresul) tarafından, Kürtçe oyun ve eğitim projelerine açık bir temel sağlamak amacıyla başlatıldı. İlk derleme bir yapay zekâ asistanı (Claude) ile yapıldı.
