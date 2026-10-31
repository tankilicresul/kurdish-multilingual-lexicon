# Değerlendirme Sonuçları

> `scripts/evaluate.py` tarafından otomatik üretilir. Yöntem: [degerlendirme.md](degerlendirme.md).

## 1. Kural tabanlı fiil çekimi ↔ UniMorph kmr

UniMorph'ta da bulunan **147** fiil, **3,872** çekim hücresi. Ham eşleşme: **77.4%**. Bir hücrede UniMorph birden fazla biçim veriyorsa, bizim biçimimizin bunlardan **herhangi biri** olması eşleşme sayılır.

> **Sınırlılıklar.** (1) Bağımsızlık sınırlı: UniMorph kmr de büyük olasılıkla Vikisözlük kaynaklıdır. (2) Örneklem yanlı: 3.982 fiilden yalnızca UniMorph'ta da bulunanlar (çoğu sık ve düzensiz fiiller) ölçülür. (3) Bağımsız test kümesi yok: elle girilen gövdeler (`curated`) ve *anîn* düzeltmesi bu karşılaştırma görüldükten sonra yapıldı. (4) Miş'li geçmiş ve hikâyesindeki %100 uyum beklenen bir sonuçtur: bu yuvalar geçmiş gövdeye düzenli ek eklenerek kurulur; UniMorph'ta da büyük olasılıkla aynı kuralla üretilmiştir (doğrulanmadı). Kuralın doğruluğundan çok iki kaynağın aynı kuralı izlediğini gösterebilir.

| Yuva | Eşleşen | Eşleşmeyen | Oran |
|---|---:|---:|---:|
| present | 467 | 114 | 80.4% |
| present_negative | 532 | 56 | 90.5% |
| subjunctive | 270 | 24 | 91.8% |
| subjunctive_negative | 197 | 90 | 68.6% |
| past | 156 | 207 | 43.0% |
| past_negative | 145 | 218 | 39.9% |
| past_progressive | 349 | 165 | 67.9% |
| present_perfect | 294 | 0 | 100.0% |
| past_perfect | 588 | 0 | 100.0% |

Eşleşmeyenlerin gövde kaynağına göre dağılımı: `rule-în` 391, `curated` 245, `data` 150, `rule-andin` 88

**Uyuşmazlıkların ön sınıflandırması.** Aşağıdaki türler, uyuşmazlıklar görüldükten **sonra**, standart yazım kurallarına (BL 1970; Th 2006) dayanarak tarafımızdan tanımlandı. İlk dört türde bizim değerlendirmemize göre UniMorph biçimi standart yazıma uymuyor. Bu sınıflandırma **henüz bir uzman tarafından yargılanmadı**:

| Tür | Sayı | Açıklama |
|---|---:|---|
| `um-final-i` | 182 | UniMorph geçmiş zaman 3. tekilde sonda *-i* veriyor (*xwendi*; standart yazımda beklenen *xwend*) |
| `um-i-orthography` | 356 | *î* + *y* yazımı (*zivirîyî*; bizim kuralımız *ziviriyî*. Uzun *î*'nin *y*'den önce kısalması, kaynakta sayfa düzeyinde doğrulanmadı) |
| `um-yi-after-consonant` | 132 | Ünsüzden sonra *-yî* (*nenalyî*; standart yazımda beklenen *nenalî*) |
| `um-preverb-order` | 144 | Ön fiilli fiillerde ek sırası (*dihilgirî*; standart yazımda beklenen *hildigirî*) |
| `other` | 60 | Elle incelenmeli (aşağıda örnekler) |

Bu dört tür bizim lehimize sayılırsa uyum **98.5%** olur. Bu bir doğruluk ölçüsü değil, yargılanmamış bir **üst tahmindir**. Doğruluk ölçüsü olarak ham oran kullanılmalıdır. Uzman kararı, her türden rastgele örneklem üzerinde `decision` sütununa girilecek (bkz. KONTROL.md). Tüm uyuşmazlıklar karar sütunuyla birlikte: [`data/kmr/review/paradigms-vs-unimorph.tsv`](../data/kmr/review/paradigms-vs-unimorph.tsv).

`other` türünden rastgele 25 örnek:

| Fiil | Yuva | Kişi | Bizim | UniMorph | Gövde kaynağı |
|---|---|---|---|---|---|
| anîn | present | 1sg | tînim | dianim / dianm | curated |
| anîn | present | 2sg | tînî | dianyî | curated |
| anîn | present_negative | 1sg | nayînim | naanim / naanm | curated |
| anîn | present_negative | 3sg | nayîne | naan / naane | curated |
| anîn | present_negative | pl | nayînin | naanin / naann | curated |
| anîn | subjunctive | 1sg | bînim | bianim / bianm | curated |
| dan | past_negative | pl | nedan | nedain | curated |
| firotin | present | 1sg | difiroşim | difirosim | curated |
| firotin | present | 3sg | difiroşe | difirose | curated |
| firotin | present | pl | difiroşin | difirosin | curated |
| firotin | subjunctive_negative | 1sg | nefiroşim | nefirosim | curated |
| hatin | present | 2sg | têyî | dihayî / dihaî | curated |
| hatin | present | 3sg | tê | diha / dihae | curated |
| hatin | present_negative | 1sg | nayêm | nahaim / naham | curated |
| hatin | present_negative | 2sg | nayî | nahayî / nahaî | curated |
| hatin | subjunctive_negative | 1sg | neyêm | nehaim / neham | curated |
| hêlan | past | pl | hêlan | hêlain | data |
| karîn | present_negative | 2sg | nikarî | nakaryî / nakarî | curated |
| mirin | present | 3sg | dimire | dime | curated |
| mirin | present_negative | 1sg | namirim | namim | curated |
| mirin | present_negative | 2sg | namirî | namî | curated |
| mirin | present_negative | pl | namirin | namin | curated |
| mirin | subjunctive_negative | 1sg | nemirim | nemim | curated |
| mirin | subjunctive_negative | 2sg | nemirî | nemî | curated |
| zanîn | present_negative | 1sg | nizanim | nazanim / nazanm | curated |

## 2. Veride geçen çekimli biçimler ↔ UniMorph kmr

Bizim (lemma, biçim) çiftimiz: 254,895 · UniMorph: 216,370 · ortak: 42,110. İki kaynak büyük ölçüde farklı kelimeleri kapsıyor; birbirini tamamlıyor.

## 3. UD Kurmanji-MG ağaç bankası

10,259 sözcük birimi (8,729 tanesi noktalama, sayı, simge ve X dışı).

| Ölçüt | Değer | n |
|---|---:|---:|
| Sözlük kapsamı (biçim sözlükte ya da çekim tablosunda var) | 82.7% | 8,729 |
| Kök bulma (çekimli biçim için doğru lemma adaylar arasında) | 59.2% | 2,975 |
| Sözcük türü uyumu (UD UPOS, sözlükteki UPOS kümesinde) | 89.0% | 8,315 |
| ↳ yalnızca sözlükte tek UPOS'u olan lemmalar | 89.2% | 3,991 |
| ↳ karşılaştırma: en sık UPOS'u her yere atayan taban çizgisi | 30.7% | 8,315 |

> Bir lemmanın sözlükte birden fazla sözcük türü olabildiği için küme ölçütü iyimserdir; tek etiketli satır daha katı bir ölçüdür. Uyuşmazlıkların bir kısmı hata değil şema farkıdır: ör. UD işaret sözcüklerini isim önünde DET olarak etiketler, Wîkîferheng ise *ev*, *ew* gibi sözcükleri zamir (PRON) olarak kaydeder. Ağaç bankası küçüktür ve belirli metin türlerinden oluşur; bu oranlar genel kullanımı temsil etmez.

En sık sözcük türü uyuşmazlıkları (UD → sözlük): SCONJ → ADV/CCONJ/PRON: 147; DET → PRON: 134; ADP → PART/PRON/X: 101; PART → ADV/NOUN: 95; VERB → NOUN: 83; DET → ADV/PRON: 46; SCONJ → ADV: 35; ADJ → NOUN: 30
