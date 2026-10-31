# UniMorph ve Fiil Çekimi Uyuşmazlık Analizi

Bu dizindeki `paradigms-vs-unimorph.tsv` tablosu (874 satır), kural tabanlı çekim motorumuz ile uluslararası UniMorph Kurmanji (kmr) veri kümesi arasındaki uyuşmazlıkları listeler.

Detaylı inceleme sonucunda uyuşmazlıkların dağılımı ve dilbilimsel gerekçeleri şöyledir:

| Kategori | Satır | Bizim Çekim (Ours) | UniMorph (um) | Dilbilimsel Açıklama |
|---|---:|---|---|---|
| `um-i-orthography` | 356 | `aniyê`, `anîn` | `anîyê`, `anîin` | Hawar alfabesinde `î` sesinden sonra kaynaştırma `y` harfinin yazımı ve çift sesli yazım varyantları |
| `um-final-i` | 182 | `afirand` | `afirandi` | Geçişli fiillerin geçmiş zaman 3. tekil şahsında (3sg) standart dilde sıfır ek (zero morpheme) esastır; UniMorph bölgesel/katkıcı kaynaklı son `-i` eki içerir |
| `um-preverb-order` | 144 | `hilnedam`, `hilneda` | `nehildam`, `nehilda` | **Ön-fiil (Preverb) Kuralı:** Kurmancî dilbilgisinde (`hil-`, `ve-`, `ra-`, `da-`) olumsuzluk eki `ne-`, ön-fiil ile kök arasına girer (`hil-ne-dam`). UniMorph'taki `nehildam` biçimi kural dışıdır |
| `um-yi-after-consonant` | 132 | `diberiqî`, `neberiqî` | `diberiqyê`, `neberiqyê` | 2. tekil şahıs ekinde standart `-î` eki yerine diftong yazımı |
| `other` (Düzensizler) | 60 | `tînim`, `tînî`, `tîne` | `dianim`, `dianyê`, `dian` | **Düzensiz Fiil Gövdeleri:** *anîn* fiilinin şimdiki zamanı düzensizdir (*ez tînim*). UniMorph hatalı olarak düzenli kabul edip `dianim` üretmiştir; bizim çekimimiz yaşayan dili yansıtır |

Bu tablo, UniMorph uyuşmazlığının rastgele bir halüsinasyon olmadığını; aksine standart Hawar dilbilgisi kuralları ile UniMorph'un otomatik derleme kusurları arasındaki bilinen farkları belgelemektedir.
