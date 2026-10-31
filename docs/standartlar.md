# Uyulan Standartlar

Bu depo, verinin başka araç ve projelerle doğrudan kullanılabilmesi için dilbilimde ve dil teknolojisinde yerleşik standartlara uyar.

| Alan | Standart | Depoda nerede |
|---|---|---|
| Dil kimliği | **ISO 639-3** ve **Glottolog** kodları | [`cldf/languages.csv`](../cldf/languages.csv), aşağıdaki tablo |
| Sözcük türü | **Universal Dependencies UPOS** (17 etiket) | `lemmas.tsv`: `upos` |
| Çekim özellikleri | **UD morfolojik özellikleri**. Değerler UD Kurmanji ağaç bankasıyla (Gökırmak & Tyers 2017) aynı | `forms.tsv.gz`: `ud_feats` |
| Çekim özellikleri | **UniMorph şeması** (Batsuren vd. 2022) | `forms.tsv.gz`: `unimorph`; `data/<v>/unimorph/*.tsv` |
| Sözlük veri modeli | **CLDF Dictionary** (Cross-Linguistic Data Formats; Forkel vd. 2018) | [`cldf/`](../cldf/) |
| Glosslu örnekler | **Leipzig Glossing Rules** (Comrie, Haspelmath & Bickel 2008) | [dil bilgisi](dilbilgisi/00-giris-ve-yontem.md#04-örneklerin-gösterimi-leipzig-glossing-kuralları) |
| Tipolojik karşılaştırma | **WALS** özellik tanımları | [dil bilgisi §0.3](dilbilgisi/00-giris-ve-yontem.md#03-tipolojik-profil) |
| Veri belgeleme | **Datasheets for Datasets** (Gebru vd. 2021), **Data Statements** (Bender & Friedman 2018) | [DATASHEET.md](../DATASHEET.md) |
| Erişilebilirlik | **FAIR** ilkeleri (Wilkinson vd. 2016) | açık lisans, makine okunur meta veri, sürüm, atıf ([CITATION.cff](../CITATION.cff)), DOI için [`.zenodo.json`](../.zenodo.json) |
| Yazı ve karakter | Unicode NFC, Hawar Latin alfabesi (Kurmancî, Zazakî); Arap tabanlı alfabe (Soranî, Güney, Goranî) | [alfabeler.md](alfabeler.md) |

## Dil kodları
| Kimlik | Ad | ISO 639-3 | Glottocode | Not |
|---|---|---|---|---|
| `kmr` | Kurmancî (Kuzey Kürtçesi) | kmr | nort2641 | |
| `ckb` | Soranî (Orta Kürtçe) | ckb | cent1972 | |
| `sdh` | Güney Kürtçesi | sdh | sout2640 | |
| `zza` | Zazakî | zza | zaza1246 | `zza` bir makro dil kodudur. Alt kodları: `kiu` (Kuzey/Kırmanckî), `diq` (Güney/Dımıli). Veri kümesinde her satır morfolojik ve sözcüksel kurallarla `kiu` / `diq` / `shared` olarak etiketlenmiştir (bkz. `data/zza/DIALECTS.md`). |
| `hac` | Goranî (Hewramî) | hac | gura1251 | Glottocode, Gurani alt grubunun tamamını kapsıyor. |

## Hâl etiketlerinin eşlemesi
Kurmancî'nin iki temel hâli için uluslararası kaynaklarda farklı adlar kullanılır. Bu depoda kaynak verinin (Wîkîferheng) etiketleri korunur ve iki standarda eşlenir:

| Wîkîferheng (`tags`) | Kurmancî terim | UD (`ud_feats`) | UniMorph | Dil bilgisi gloss |
|---|---|---|---|---|
| `direct` | rewşa xwerû | `Case=Nom` | `NOM` | DIR |
| `oblique` | rewşa çemandî | `Case=Acc` | `ACC` | OBL |
| `ezafe` | îzafe | `Case=Con` | `LGSPEC1` | EZ |
| `vocative` | rewşa bangkirinê | `Case=Voc` | `VOC` | VOC |

> Kanıt: UD Kurmanji ağaç bankasının özellik belgesi bükümlü hâli `Acc` ("labeled oblique"), izafeti `Con` (construct) olarak tanımlar (universaldependencies.org/kmr/feat/Case.html). UniMorph kmr verisinde izafet biçimleri `LGSPEC1` ile işaretlidir (ör. *bêdengîa* `DEF;LGSPEC1;N;SG`). UniMorph'ta `LGSPEC1` dile özgü serbest bir etikettir; anlamı veri setinden çıkarılmıştır. UniMorph kmr ayrıca `LGSPEC2` etiketini de kullanır (bükümlü ve seslenme biçimlerinde); bu depo bu etiketi üretmez.

> Not: UD ve UniMorph'taki `Nom`/`Acc` adları Kurmancî için tam doğru değildir. Bükümlü hâl yalnızca nesneyi değil, edat tümlecini, iyelik sahibini ve ergatif yapıda özneyi de işaretler. Bu adlar yalnızca araçlar arası uyum için kullanılır. Dil bilgisinde *yalın* ve *bükümlü* terimleri esastır.

## CLDF kullanımı
```python
from pycldf import Dataset
ds = Dataset.from_metadata("cldf/Dictionary-metadata.json")
for e in ds.iter_rows("EntryTable", "id", "headword", "partOfSpeech", "languageReference"):
    ...
```
Doğrulama: `cldf validate cldf/Dictionary-metadata.json`. Büyük tablolar `.csv.zip` olarak saklanır; `pycldf` bunları doğrudan okur.
