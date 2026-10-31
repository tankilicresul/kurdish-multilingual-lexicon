# Etimoloji: Bir kelime nereden gelir?

> ⚠️ **Kontrol edilecek.** Bu sayfadaki sınıflandırma, Wîkîferheng (ku.wiktionary) ve İngilizce Vikisözlük'teki etimoloji kayıtlarından **otomatik** olarak çıkarıldı. Her satırda `confidence` (güven) ve `review_status` sütunları vardır. Hiçbir satır henüz bir etimolog tarafından onaylanmadı. Akademik bir çalışmada kullanmadan önce aşağıdaki kaynaklarla karşılaştırın.

Bu depo Nişanyan Sözlük'ün Türkçe için yaptığını Kurmancî için başlatmayı amaçlar: her kelimenin **nereden geldiğini**, hangi yolla dile girdiğini ve bu bilginin **dayanağını** göstermek.

Dosya: [`data/kmr/db/etymology-class.tsv`](../data/kmr/db/etymology-class.tsv) · Üreten betik: [`scripts/etymology_classify.py`](../scripts/etymology_classify.py) · Ham etimoloji metinleri: [`etymology.tsv`](../data/kmr/db/etymology.tsv)

## 1. Önce bir ilke: Alıntı kelime de Kürtçedir
"Bu kelime gerçekten Kürtçe mi?" sorusunun dilbilimdeki karşılığı "bu kelime **miras** mı, **alıntı** mı?" sorusudur. İkisi de Kürtçenin malıdır:
- Türkçedeki *kitap* Arapçadan, *masa* İtalyancadan gelir; ikisi de Türkçe kelimedir.
- Kurmancî'deki *kitêb* (Arapça) ve *pirtûk* (Kürtçe içinde türetilmiş) birlikte yaşar. Hangisinin "daha Kürtçe" olduğuna karar vermek dilbilimin değil, dil planlamasının işidir.

Bu depo **kelime ayıklamaz**, yalnızca kökeni kayıt altına alır. Dil arılaştırma (purizm) amacıyla kullanılacaksa bu sınırlılık akılda tutulmalıdır.

## 2. Sınıflar
| Sınıf | Anlamı | Örnek |
|---|---|---|
| `inherited` | **Miras.** Proto-İrani (ve daha eski Hint-Avrupa) kökten kesintisiz gelen kelime | *av* (su), *bajar* (şehir), *heval* (arkadaş), *ziman* (dil), *kevok* (güvercin) |
| `internal` | **İç türetme.** Kurmancî içinde ek, birleştirme veya ön fiille yapılmış kelime | *pirtûk*, *rojname* (< *roj* + *name*), *xwendekar* |
| `borrowed` | **Alıntı.** İran dışı bir dilden alınmış | *kitêb* (Arapça), *otomobîl* (Fransızca, Türkçe aracılığıyla), *çay* (Osmanlıca) |
| `borrowed-iranian` | **İran dillerinden alıntı.** Başka bir İran dilinden (çoğunlukla Farsça, Soranî) alınmış | *perwerde* (eğitim: Orta Farsça > Farsça > Kurmancî), *amade* (hazır) |
| `onomatopoeic` | **Yansıma.** Doğadaki sesi taklit eden kelime | *pisîk* (kedi), *kuxik* (öksürük), *çivîk* |
| `unknown` | Kaynaklarda etimoloji bilgisi yok | *dibistan* |

**Neden `inherited` ile `borrowed-iranian` ayrı?** Kurmancî ile Farsça ortak atadan geldiği için çok sayıda kelimeyi paylaşır (*av* ~ Farsça *âb*). Bunlar alıntı değil, kardeş kelimelerdir. Ancak bazı kelimeler sonradan Farsçadan ya da Soranî'den yazı yoluyla alınmıştır. Bu ikisini ayırmak İran dilleri etimolojisinin en zor problemidir. Bu depodaki `borrowed-iranian` etiketi yalnızca kaynakta açıkça "Farsçadan alıntı" (*deyn ji farisî*) yazıyorsa verilir. Yine de hatalı kayıtlar vardır (bkz. §6).

## 3. Sütunlar
| Sütun | Açıklama |
|---|---|
| `word`, `pos` | Kelime ve sözcük türü |
| `class` | Yukarıdaki sınıflar |
| `source_lang` | Kelimenin doğrudan alındığı ya da miras geldiği dil (ISO 639 / Vikisözlük kodu: `ar` Arapça, `fa` Farsça, `ira-pro` Proto-İrani, `ine-pro` Proto-Hint-Avrupa, `ota` Osmanlıca...) |
| `source_family` | Kaynak dilin ailesi (Sami, Avrupa, Türk-Moğol, İrani, Kafkas-Ermeni, Hint) |
| `ancestor` | Zincirdeki en eski dil |
| `path` | Kelimenin izlediği yol: `sem-wes-pro > ar > kmr` (Batı Sami > Arapça > Kurmancî) |
| `evidence` | Sınıflandırmanın dayanağı: `ku-tree` (Wîkîferheng etimoloji ağacı), `ku-text` (Wîkîferheng açıklama metni), `en-template` (İngilizce Vikisözlük şablonları: `inh`, `bor`, `der`), `morphemes` (ek çözümlemesi) |
| `confidence` | `high` (açık ve tutarlı kayıt), `medium` (tek kaynak), `low` (kayıt yok ya da çelişkili) |
| `regions` | Kaynakta kelimeyle birlikte anılan yer etiketleri. **Dikkat:** Bunlar çoğunlukla ses kaydının ya da örneğin yapıldığı yerdir. Kelimenin yalnızca orada kullanıldığı anlamına gelmez. |
| `freq_rank` | Kurmancî Vikipedi derlemindeki sıklık sırası |
| `review_status` | `unverified` / `verified` |

## 4. Rakamlar (v0.3)
Toplam **156.692** madde (kelime + sözcük türü):

| Sınıf | Tüm sözlük | En sık 5.000 kelime (bilinenler) |
|---|---|---|
| internal (iç türetme) | 62.176 | 714 |
| inherited (miras) | 1.180 | 406 |
| borrowed (İran dışı alıntı) | 3.214 | 211 |
| borrowed-iranian | 216 | 47 |
| onomatopoeic (yansıma) | 131 | 1 |
| unknown (kayıt yok) | 89.775 | – |

**Alıntıların kaynak dilleri:** Arapça 1.658 · Fransızca 608 · İngilizce 405 · Türkçe 230 · Farsça 128 · Soranî 84 · Yunanca 69 · Ermenice 63 · Osmanlıca 45 · Latince 29 · Aramice 24.

**Bu rakamlar nasıl okunmalı?**
- Sözlükteki "internal" sayısının büyüklüğü, Wîkîferheng'in çok sayıda türetilmiş kelimeyi ayrı madde olarak almasından kaynaklanır.
- **Temel söz varlığında miras kelimeler ağır basar:** en sık kelimeler arasında miras kelime sayısı alıntılardan fazladır. Bu, diğer İran dilleri için de bilinen bir durumdur.
- Fransızca ve İngilizce alıntıların çoğu bilim ve teknik terimdir (*kîmya*, *otomobîl*). Gündelik dildeki ağırlıkları düşüktür.
- "unknown" sınıfının büyüklüğü bilgi eksikliğidir, kelimenin yabancı olduğu anlamına gelmez. Katkıya en açık alan burasıdır.

## 5. Yöntem
`scripts/etymology_classify.py` her kelime için kanıtları şu sırayla dener ve ilk güçlü kanıtta durur:
1. **Wîkîferheng etimoloji ağacı** (*Dara etîmolojiyê*): `deyn.` işareti alıntıyı, `drş.` türetmeyi gösterir. Zincirde Kurmancî'den önceki ilk dil kaynak dil sayılır.
2. **Wîkîferheng açıklama metni:** *"deyn ji erebî"* (Arapçadan alıntı), *"ji proto-îranî"*, *"onomatopeya"* gibi açık ifadeler.
3. **İngilizce Vikisözlük şablonları:** `{{inh|kmr|ira-pro|...}}` miras, `{{bor|kmr|ar|...}}` alıntı.
4. **Morfem çözümlemesi:** *roj + name* gibi "+" ile ayrılmış kayıt varsa `internal`.

Bu sırayı değiştirmek ya da yeni bir kanıt kaynağı eklemek için betikteki `classify_tree`, `classify_text`, `classify_en` ve `classify_morph` fonksiyonlarına bakın. Her satırın `evidence` sütunu hangi adımın kullanıldığını gösterir. Böylece her karar izlenebilir.

## 6. Bilinen sorunlar
- **Ortak İrani kökler Farsça alıntı olarak işaretlenmiş olabilir.** Örnekler: *gotin* ve *kevn*. Bu kelimeler büyük olasılıkla mirastır. Kaynak metin "Farsçadaki gibi" ile "Farsçadan" ayrımını her zaman yapmıyor.
- **Eş yazımlı kelimeler.** *lê* "ama" ile *lê* "ona" farklı kökenlidir. Sözcük türü (`pos`) sütunu bu ayrımı kısmen yapar.
- **Aracı dil.** *otomobîl* Fransızca kökenlidir, ama Kurmancî'ye Türkçe aracılığıyla girmiştir. `path` sütunu aracı dili yalnızca kaynak belirtmişse gösterir.
- **Proto-İrani kök biçimleri** (*\*Hap-* gibi) bu tabloda tutulmaz. Bunlar ham kaynak metinde, [`etymology.tsv`](../data/kmr/db/etymology.tsv) dosyasında yer alır.

## 7. Tarihî ve akademik kaynaklar
Kökeni doğrulamak için başvurulacak eserler. Bu depo bunlardan **veri kopyalamaz**. Kaynakların telif durumu farklıdır. Kontrol eden kişi bunları karşılaştırma için kullanmalıdır:

| Eser | Önemi |
|---|---|
| Johnny Cheung, *Etymological Dictionary of the Iranian Verb*, Brill, 2007 | İran dillerindeki fiil köklerinin standart etimoloji sözlüğü. Kurmancî fiillerinin Proto-İrani kökleri için temel kaynak |
| Garnik Asatrian, "Prolegomena to the Study of the Kurds", *Iran and the Caucasus* 13, 2009 | Kürtçenin İran dilleri içindeki yeri ve tarihî kaynaklar |
| Garnik Tsabolov, *Etimologičeskij slovar' kurdskogo jazyka* (Kürtçe etimoloji sözlüğü), 2 cilt, Moskova, 2001 | Kurmancî'ye özel tek kapsamlı etimoloji sözlüğü (Rusça) |
| Auguste Jaba & Ferdinand Justi, *Dictionnaire kurde-français*, St. Petersburg, 1879 | 19. yüzyıl kaydı. Kelimelerin 150 yıl önceki biçimlerini gösterir (kamu malı) |
| D. N. MacKenzie, *Kurdish Dialect Studies* I-II, 1961-62 | Lehçe karşılaştırması ve tarihî ses değişimleri |
| Michael L. Chyet, *Kurdish-English Dictionary*, Yale, 2003 | Etimoloji notları ve Ermenice, Aramice, Türkçe alıntılar için kaynak gösterimi |
| Celadet Bedir Khan & Roger Lescot, *Grammaire kurde*, 1970 | Standart yazı dilinin dayanağı |
| Ehmedê Xanî, *Mem û Zîn*, 1692 | Klasik Kurmancî metin. Bir kelimenin 17. yüzyılda kullanılıp kullanılmadığını gösterir |
| Ehmedê Xanî, *Nûbihara Biçûkan*, 1683 | Bilinen ilk Kurmancî-Arapça manzum sözlük |

**Kaynak dilin tarihî katmanları (genel çerçeve):**
1. **Miras katmanı:** Proto-Hint-Avrupa, Proto-İrani ve Batı İrani üzerinden. Temel söz varlığı: beden, aile, doğa, sayılar, temel fiiller.
2. **Eski komşuluk katmanı:** Ermenice, Aramice/Süryanice, Yunanca. Tarım, zanaat ve yer adlarında.
3. **İslam dönemi katmanı:** Arapça, Farsça. Din, hukuk, yönetim, soyut kavramlar.
4. **Osmanlı ve modern katman:** Türkçe, Osmanlıca. Yönetim ve gündelik eşya.
5. **Modern katman:** Fransızca, İngilizce, Rusça. Teknik ve bilim terimleri. Soranî ile yazı dili alışverişi.

## 8. Nasıl katkı yapılır?
Bir kelimenin kökenini düzeltmek için `etymology-class.tsv` satırını düzenleyin, `evidence` sütununa kaynağı yazın (ör. `Cheung 2007: 152`) ve `review_status` değerini `verified` yapın. Ayrıntılar: [CONTRIBUTING.md](../CONTRIBUTING.md) ve [KONTROL.md](../KONTROL.md).
