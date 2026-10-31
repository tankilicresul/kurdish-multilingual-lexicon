# 0. Giriş, Kapsam ve Gösterim

## 0.1 Kapsam
Bu bölüm **betimleyici bir başvuru dil bilgisi** taslağıdır. Bir öğretim kitabı değildir; öğretim amaçlı alıştırmalar ayrı tutulur: [`docs/ogretim/`](../ogretim/README.md).

- **Dil çeşidi:** Standart yazılı Kurmancî (Kuzey Kürtçesi; ISO 639-3 `kmr`, Glottocode `nort2641`). Hawar alfabesi ve Bedirxan & Lescot (1970) geleneği esas alındı.
- **Ağız farklılıkları:** Yalnızca belirgin oldukları yerde "Ağız notu" olarak belirtilir. Kurmancî ağızlarının sınıflandırması için Öpengin & Haig (2014)'e bakılmalıdır.
- **Yöntem:** Kurallar aşağıdaki standart başvuru eserlerden derlendi. Örnekler depodaki sözlük verisiyle (`data/kmr/db/`) ve Rastnivîs yazım denetimiyle karşılaştırıldı. Yeni bir dilbilimsel iddia ileri sürülmez.
- **Atıfların ayrıntı düzeyi:** Kaynak atıfları eser düzeyindedir. Bir kuralın kaynakta hangi sayfada geçtiği henüz tek tek doğrulanmadı. Sayfa ya da paragraf numaralı atıflar uzman incelemesiyle eklenecek.
- **Yapay zekâ kullanımı:** Bu bölümün ilk taslağı, insan gözetiminde bir yapay zekâ asistanıyla (Anthropic Claude) hazırlandı. Kurallar kaynaklardan derlendi. Örneklerin yazımı otomatik yazım denetiminden geçirildi.
- **Durum:** Henüz uzman incelemesinden geçmedi (bkz. [KONTROL.md](../../KONTROL.md)).

## 0.2 Temel kaynaklar
| Kısaltma | Eser |
|---|---|
| BL 1970 | Bedir Khan, C. & R. Lescot. 1970. *Grammaire kurde (dialecte kurmandji)*. Paris: Maisonneuve. |
| Th 2006 | Thackston, W. M. 2006. *Kurmanji Kurdish: A Reference Grammar with Selected Readings*. Harvard University. |
| HÖ 2018 | Haig, G. & E. Öpengin. 2018. Kurmanji Kurdish in Turkey: Structure, varieties, and status. In C. Bulut (ed.), *Linguistic Minorities in Turkey and Turkic-speaking Minorities of the Periphery*, 157–229. (Turcologica 111.) Wiesbaden: Harrassowitz. |
| ÖH 2014 | Öpengin, E. & G. Haig. 2014. Regional variation in Kurmanji: A preliminary classification of dialects. *Kurdish Studies* 2(2), 143–176. |
| Haig 2008 | Haig, G. 2008. *Alignment Change in Iranian Languages: A Construction Grammar Approach*. Berlin: Mouton de Gruyter. |
| McK 1961 | MacKenzie, D. N. 1961–62. *Kurdish Dialect Studies* I–II. London: Oxford University Press. |

Tam kaynakça BibTeX biçiminde: [`docs/kaynakca.bib`](../kaynakca.bib).

## 0.3 Tipolojik profil
Bu tablo, WALS (*World Atlas of Language Structures*, Dryer & Haspelmath 2013) **özellik tanımlarını** kullanarak standart Kurmancî'yi betimler. Ayrı tutulan iki sütun vardır:
- **WALS değer adı:** WALS'ın kapalı değer listesinden bizim seçtiğimiz değer.
- **Not:** Değerin yetmediği yerde betimleyici açıklama.

Bu değerler WALS veri tabanındaki Kürtçe kayıtlarından alınmadı ve onlarla karşılaştırılmadı. Bu yazarların sınıflandırmasıdır.

| WALS özelliği | WALS değer adı (bizim sınıflandırmamız) | Not | Türkçe |
|---|---|---|---|
| 81A Order of Subject, Object and Verb | SOV | Hedef ve yön tümleçleri genellikle fiilden sonra gelir (bkz. §6.1) | SOV |
| 85A Order of Adposition and Noun Phrase | Prepositions | Ayrıca çevre edatlar yaygındır (*di … de*, *ji … re*); WALS bunları ayrı bir değer olarak saymaz | Postpositions |
| 86A Order of Genitive and Noun | Noun-Genitive | İzafet ile | Genitive-Noun |
| 87A Order of Adjective and Noun | Noun-Adjective | İzafet ile | Adjective-Noun |
| 30A Number of Genders | Two | Eril / dişil; bazı ağızlarda zayıflamış | None |
| 37A Definite Articles | No definite, but indefinite article | | No definite, but indefinite article |
| 38A Indefinite Articles | Indefinite affix | *-ek* | Indefinite word same as 'one' |
| 49A Number of Cases | 2 cases | Yalın ve bükümlü; seslenme biçimleri sayılmadı | 6–7 cases |
| 98A Alignment of Case Marking of Full NPs | Tek değere indirgenemez | Zamana göre bölünmüş: şimdiki zamanda yalın/bükümlü karşıtlığı nominatif-akuzatif gibi, geçişli geçmişte ergatif örüntü. Hâl işaretlemesi eril tekil isimlerde çoğu zaman görünmez (Haig 2008) | Nominative-accusative |
| 100A Alignment of Verbal Person Marking | Tek değere indirgenemez | Şimdiki zamanda fiil özneye, geçişli geçmişte nesneye uyar (Haig 2008) | Accusative |
| 112A Negative Morphemes | Negative affix | *na-*, *ne-*, *me-*, *ni-* | Negative affix |
| 116A Polar Questions | Belirlenmedi | Tonlama esas; *gelo*, *ma* gibi sözcükler isteğe bağlı | Question particle |

Türkçe değerleri WALS'taki Türkçe kaydından aktarılmadı. Genel kabul gören betimlemelere dayanır, kontrol edilmelidir.

## 0.4 Örneklerin gösterimi: Leipzig glossing kuralları
Glosslu örnekler **Leipzig Glossing Rules** (Comrie, Haspelmath & Bickel 2008) ile yazılır. Bu kurallar dilbilimde yaygın kullanılan bir standarttır:

```
(a) Min      tu       dît-î.
    1SG.OBL  2SG.DIR  see.PST-2SG
    'Seni gördüm.'
```

- 1. satır: Kurmancî. Biçimbirimler kısa çizgiyle (`-`) ayrılır.
- 2. satır: Biçimbirim biçimbirim karşılık. Dilbilgisel anlamlar BÜYÜK harfli kısaltmayla gösterilir. Bir biçimbirimin birden fazla anlamı nokta (`.`) ile ayrılır. Kelime anlamları uluslararası kullanım için İngilizce verilir.
- 3. satır: Türkçe çeviri.

Bölümlerdeki tablolar genel bakış içindir. Kesin çözümleme için glosslu örneklere başvurun.

## 0.5 Kısaltmalar
Leipzig standart listesindeki kısaltmalar ve bu çalışmaya özgü olanlar (*):

| Kısaltma | Anlam | Kurmancî örnek |
|---|---|---|
| 1, 2, 3 | birinci, ikinci, üçüncü kişi | |
| SG, PL | tekil, çoğul | |
| M, F | eril, dişil | |
| DIR* | yalın hâl (direct) | *ez*, *mal* |
| OBL | bükümlü hâl (oblique) | *min*, *malê* |
| VOC | seslenme hâli | *Kurdo!* |
| EZ* | izafet | *-ê*, *-a*, *-ên* |
| INDF | belirsizlik | *-ek* |
| IPFV | bitmemişlik (şimdiki zamanda ve sürekli geçmişte *di-*) | *di-* |
| SBJV | dilek kipi (*bi-*) | *bi-* |
| IMP | emir | *bike!* |
| FUT | gelecek zaman parçacığı | *dê*, *ê* |
| PRS, PST | şimdiki ve geçmiş zaman gövdesi | *-k-* / *kir* |
| PRF | miş'li geçmiş (perfect) | *-iye* |
| PTCP | ortaç (*-i*, geçmiş gövdeden; miş'li geçmiş ve hikâyesinde) | *hat-i-bû-m* |
| NEG | olumsuzluk | *na-*, *ne-* |
| PROH | olumsuz emir | *me-* |
| COP | ek-fiil | *im*, *e*, *in* |
| INF | mastar | *-in* |
| PV* | ön fiil (preverb) | *ve-*, *ra-* |
| CAUS | ettirgen | *-and-* |
| CMPR | karşılaştırma | *-tir* |
| REFL | dönüşlülük | *xwe* |
| COMP | tamamlayıcı bağlacı (ör. *bilmek* fiilinin tümcesi) | *ku* |
| REL | ilgi cümlesi işaretleyicisi | *ku* |
| ADD* | "de, da" (ekleme parçacığı) | *jî* |

Kişi uyumu sıfır biçimbirimle gösterildiğinde (3. tekil geçmiş zaman gibi) gloss satırında parantez kullanılır: `eat.PST(3SG)`. Bu, Leipzig kural 6'daki örtük kategori gösterimidir.

## 0.6 Terim karşılıkları
Türkçe, Kurmancî ve İngilizce terimlerin tam listesi: [terimler.md](terimler.md).

## 0.7 Bu bölümden alıntı yapma
> GameVan Studio ve katkıcılar. 2026. *Kurmancî Başvuru Dil Bilgisi (taslak)*. Kurdish Multilingual Lexicon, sürüm 0.4. https://github.com/tankilicresul/kurdish-multilingual-lexicon

Bir kuralın birincil kaynağına atıf yapılacaksa yukarıdaki eserler kullanılmalıdır. Bu taslak ikincil bir derlemedir.
