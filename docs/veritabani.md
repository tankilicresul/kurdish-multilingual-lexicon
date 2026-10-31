# Dilbilimsel Veritabanı (Ferheng DB)

> ⚠️ Taslak. Tamamı Vikisözlük'ten (ku.wiktionary ve en.wiktionary) otomatik çıkarıldı. `review_status = unverified`.

Her lehçe için `data/<lehçe>/db/` klasöründe:

| Dosya | İçerik | Kurmancî | Soranî | Zazakî | Güney | Goranî |
|---|---|---:|---:|---:|---:|---:|
| `lemmas.tsv` / `lemmas.jsonl.gz` | Madde başları (kökler/sözlük biçimleri) ve tüm bilgileri | 158.393 | 7.232 | 3.314 | 819 | 167 |
| `forms.tsv.gz` | Çekimli biçim → kök + dil bilgisi etiketleri | 329.942 | 49 | 89 | – | – |
| `etymology.tsv` | Köken bilgisi olan maddeler | 86.916 | 1.201 | 675 | 353 | 21 |
| `affixes.tsv` | Ön ekler, son ekler, iç ekler | 561 | 41 | 20 | 6 | 5 |
| `verb-roots.tsv` | Fiil gövdeleri (şimdiki ve geçmiş zaman kökleri) | 531 | 2 | 1 | – | – |
| `proverbs-idioms.tsv` | Atasözleri ve deyimler | 21.009 | 15 | 2 | 3 | 1 |
| `audio.tsv` | Anadil konuşucularının ses kayıtları (bağlantı) | 3.099 | 3 | 35 | 4 | – |

Kurmancî maddelerin 61.491'inde ek-kök ayrımı (ör. `bê- + kar`), 27.240'ında IPA okunuşu var. Özet sayılar: [`data/DB-STATS.json`](../data/DB-STATS.json)

## 1. `lemmas.tsv` sütunları

| Sütun | Açıklama | Örnek (`bêkar`) |
|---|---|---|
| `word` | Madde başı | bêkar |
| `upos` | Sözcük türü ([Universal Dependencies](https://universaldependencies.org/u/pos/) etiketleri) | ADJ |
| `pos_ku` | Sözcük türünün Kurmancî adı | Rengdêr |
| `gender` | Dil bilgisel cinsiyet (`feminine`, `masculine`, ikisi de) | |
| `gloss_ku` | İlk Kurmancî tanım | betal, bêşol, bêked, bêxebat |
| `gloss_en` | İlk İngilizce tanım (en.wiktionary) | |
| `tr` / `en` / `de` | En iyi 3 çeviri | işsiz / unemployed / arbeitslos |
| `morphemes` | Ek-kök ayrımı | bê- + kar |
| `origin` | Köken dili tahmini (etimoloji "Ji X..." diye başlıyorsa) | |
| `etymology_mentions` | Etimolojide **adı geçen** diller (köken değil; akraba diller de dahil) | kmr |
| `ipa` | Okunuş | /ˈbeː'kʰɑːɾ/ |
| `hyphenation` | Hece bölümü | |
| `arabic_script` | Arap harfli yazımı | بێكار |
| `freq_rank` | Kurmancî Vikipedi sıklık sırası | |
| `review_status` | İnsan kontrolü | unverified |

`lemmas.jsonl.gz` aynı kayıtların tam hâlidir: tüm tanımlar, örnek cümleler, tam etimoloji metni (Kurmancî ve İngilizce), eş anlamlılar, zıt anlamlılar, türetilmiş ve ilgili kelimeler, Kiril/Arap yazımları ve kaynak bağlantısı.

```python
import gzip, json
for line in gzip.open('data/kmr/db/lemmas.jsonl.gz', 'rt', encoding='utf-8'):
    r = json.loads(line)
    if r['word'] == 'baran':
        print(r['upos'], r['gender'], r['etymology_ku'][:80], r['synonyms'])
```

## 2. Sözcük türleri (UPOS)

| UPOS | Kurmancî | Türkçe | Kurmancî madde |
|---|---|---|---:|
| NOUN | Navdêr | İsim | 90.596 |
| ADJ | Rengdêr | Sıfat | 27.080 |
| VERB | Lêker | Fiil | 26.083 |
| ADV | Hoker | Zarf | 3.918 |
| PROPN | Serenav | Özel isim | 3.493 |
| NUM | Hejmar | Sayı | 388 |
| ADP | Daçek, Pêşdaçek, Paşdaçek, Bazinedaçek | Edat (ön, son, çevre edat) | 358 |
| PRON | Cînav | Zamir | 284 |
| INTJ | Baneşan | Ünlem | 133 |
| CCONJ | Girêdek | Bağlaç | 84 |
| AFFIX | Pêşgir, Paşgir, Navgir | Ek | 623 (561'i `affixes.tsv` içinde; İngilizce Vikisözlük'ten gelen 62'si `lemmas.tsv` içinde) |
| ROOT | Rehekî lêkerê | Fiil gövdesi | 531 |
| PROVERB / PHRASE | Gotineke pêşiyan / Biwêj | Atasözü / Deyim | 11.191 / 9.823 |
| X | Mane (belirsiz) | Sınıflandırılmamış | 5.733 |

## 3. Çekimli biçimler: `forms.tsv.gz`

| form | lemma | upos | tags | description_ku |
|---|---|---|---|---|
| baranekê | baran | NOUN | feminine,singular,indefinite,oblique | Rewşa çemandî ya mê ya yekjimar a nebinavkirî ya baran. |
| baranên | baran | NOUN | feminine,plural,definite,ezafe | Rewşa îzafeyî ya binavkirî ya pirjimar ya mê ya baran. |
| bike | kirin | VERB | singular,3rd-person,future | Kesê sêyem yekjimar dema bê ji lêkera kirin (tewandin). |

**Etiketler** Kurmancî tanımlardan otomatik çevrildi:

| Etiket | Kurmancî terim | Türkçe |
|---|---|---|
| masculine / feminine | nêr / mê | eril / dişil |
| singular / plural | yekjimar / pirjimar | tekil / çoğul |
| definite / indefinite | binavkirî / nebinavkirî | belirli / belirsiz |
| direct / oblique | navkî / çemandî | yalın / bükümlü hâl |
| ezafe | îzafeyî | izafet (tamlama) |
| vocative | bangkirin | seslenme |
| 1st/2nd/3rd-person | kesê yekem/duyem/sêyem | 1./2./3. kişi |
| present / past / future | dema niha / borî / bê | şimdiki / geçmiş / gelecek |
| progressive, past-perfect | berdest, raboriya dûdar | sürekli, miş'li geçmiş |
| subjunctive / imperative | merciya / fermanî | dilek-şart / emir |
| negative | neyînî | olumsuz |
| comparative / superlative | komparatîv / sûperlatîv | karşılaştırma / üstünlük |

**Oyun ve yazım denetimi için kullanım:** Oyuncu `baranê` yazarsa bu dosyada arayıp "geçerli kelime, kökü *baran*" diyebilirsiniz.

## 4. Etimoloji: `etymology.tsv`
- `etymology_ku`: Kürtçe Vikisözlük'teki köken metni (çoğu zaman Proto-Hint-Avrupa ve Proto-İrani biçimleri, akraba diller ve akademik kaynaklarla, ör. Cheung 2007, Chyet 2003).
- `etymology_en`: İngilizce Wiktionary'deki köken metni.
- `origin`: yalnızca metin "Ji erebî…", "Ji farisî…" gibi açık bir ifadeyle başlıyorsa doldurulur. Kurmancî'de en sık görülen köken dilleri: Arapça (2.761), Fransızca (523), İngilizce (442), Türkçe (286), Farsça (250).

> Etimoloji tartışmalı bir alandır. Bu metinler Vikisözlük katkıcılarının yazdıklarıdır; akademik kaynakla doğrulanmadan kesin bilgi olarak sunulmamalıdır.

### 4a. Köken sınıfı: `etymology-class.tsv`
Her madde için tek satırlık özet: miras mı (`inherited`), Kürtçe içinde mi türetilmiş (`internal`), hangi dilden alınmış (`borrowed`, `borrowed-iranian`), yansıma mı (`onomatopoeic`). Ayrıca kaynak dil, dil ailesi, köken yolu (`ar > kmr`), kanıt türü ve güven düzeyi. Yöntem ve sınırlar: [etimoloji.md](etimoloji.md).

### 4b. Fiil çekimleri: `verb-stems.tsv`, `verb-paradigms.jsonl.gz`
3.982 fiil için şimdiki ve geçmiş gövde (kaynağıyla: `curated`, `data`, `rule-în`, `rule-andin`) ve 9 zamanın 6 kişideki biçimleri. `attested` alanı, kuralla üretilen biçimlerden hangilerinin `forms.tsv.gz` içinde de geçtiğini gösterir. Örnek tablolar: [dilbilgisi/paradigmalar.md](dilbilgisi/paradigmalar.md).

## 5. Ses: `audio.tsv`
[Lingua Libre](https://lingualibre.org) projesinde anadil konuşucularının okuduğu kelimelerin Wikimedia Commons bağlantıları ve konuşucunun bölgesi (ör. Wan/Van, Bitlis, Amed/Diyarbakır). Ses dosyaları depoya **eklenmedi**, yalnızca bağlantıları var. Her dosyanın lisansı kendi Commons sayfasında yazar; çoğu CC BY-SA 4.0'dır. Uygulamada kullanırken konuşucuyu ve lisansı belirtin.

## 6. Atasözleri ve deyimler
21.009 Kurmancî atasözü ve deyim, Kurmancî açıklamaları ve örnekleriyle. "Atasözünü tamamla" türü oyunlar ve kültür içerikleri için kaynak olabilir. İçerik kontrol edilmeden çocuklara yönelik ürünlerde kullanılmamalı; bazıları kaba ya da eski dönem değerlerini yansıtabilir.

## 7. Bilinen sınırlar
- Soranî, Zazakî, Güney Kürtçesi ve Goranî için çekim tabloları neredeyse yok (Vikisözlük'te bu lehçelerin çekimleri girilmemiş).
- `morphemes` sütunu etimoloji metnindeki `x + y` kalıbından çıkarıldı. Bazı satırlarda ek-kök ayrımı değil, tarihsel birleşim gösterilir.
- `X` (Mane) etiketli maddelerin türü kaynakta belirtilmemiş.
- Fiil gövdeleri yalnızca 531 tanedir; Kurmancî'nin tüm fiilleri için değil.
