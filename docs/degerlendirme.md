# Değerlendirme Yöntemi

Bir dil kaynağının akademik değeri, ne kadar doğru olduğunun **ölçülebilmesine** bağlıdır. Bu depo henüz anadil konuşucusu tarafından incelenmediği için kalite iki yolla ölçülür:
1. **Dış başvuru kaynaklarıyla otomatik karşılaştırma** (bu sayfa)
2. **İnsan incelemesi için örneklem** ([KONTROL.md](../KONTROL.md))

Güncel sonuçlar: **[degerlendirme-sonuclari.md](degerlendirme-sonuclari.md)** · makine okunur: [`data/EVAL.json`](../data/EVAL.json)

## Başvuru kaynakları
| Kaynak | İçerik | Lisans | Neden |
|---|---|---|---|
| **UniMorph kmr** (Batsuren vd. 2022) | 216 bin (lemma, biçim, özellik) üçlüsü | CC BY-SA 3.0 | Kurmancî çekimi için yayımlanmış tek büyük standart veri |
| **UD Kurmanji** ağaç bankası (Gökırmak & Tyers 2017) | Elle işaretlenmiş 10 bin sözcük birimi (lemma, UPOS, özellikler) | CC BY-SA 4.0 | Elle doğrulanmış, gerçek metin |

Başvuru kaynakları bu depoya **kopyalanmaz**. `scripts/evaluate.py` bunları ayrı bir klasöre indirir ve yalnızca karşılaştırır.

## Ölçütler
1. **Fiil çekimi doğruluğu:** `verb-paradigms.jsonl.gz` içindeki kuralla üretilmiş biçimler, UniMorph'ta aynı fiil ve aynı özellik kümesiyle kayıtlı biçimlerle karşılaştırılır. Uyuşmazlıklar türlere ayrılır.
2. **Örtüşme:** Veride geçen (lemma, biçim) çiftlerinden kaçının UniMorph'ta da bulunduğu.
3. **UD ağaç bankası üzerinde:**
   - *Kapsam:* Gerçek metindeki kelimelerin yüzde kaçı sözlükte ya da çekim tablosunda var?
   - *Kök bulma:* Çekimli bir biçim için doğru lemma, sözlüğün önerdiği adaylar arasında mı?
   - *Sözcük türü uyumu:* UD'nin elle verdiği UPOS, sözlükteki UPOS kümesinde mi?

## Sonuçları yorumlama
- **Doğruluk ölçüsü ham eşleşme oranıdır.** UniMorph da otomatik üretilmiş bir kaynaktır ve yazım sorunları içerir. Uyuşmazlıklar, görüldükten sonra tarafımızdan türlere ayrıldı. "Bu türler bizim lehimize sayılırsa" oranı yalnızca yargılanmamış bir **üst tahmin** olarak verilir. Uzman kararı için [`data/kmr/review/paradigms-vs-unimorph.tsv`](../data/kmr/review/paradigms-vs-unimorph.tsv) dosyasında `decision` sütunu bırakıldı. Planlanan yöntem şudur: her türden en az 50 rastgele satırı Kurmancî bilen bir dilbilimci etiketler; sınıflandırmanın isabeti ayrıca raporlanır.
- **Bağımsızlık ve sızıntı:** UniMorph kmr büyük olasılıkla Vikisözlük kaynaklıdır, yani tam bağımsız bir başvuru değildir. Elle girilen fiil gövdeleri (`curated`) ve bazı düzeltmeler karşılaştırma görüldükten sonra yapıldı. Ayrı bir test kümesi yoktur.
- UD ağaç bankası küçüktür (yaklaşık 10 bin sözcük) ve belirli metin türlerinden oluşur. Oranlar genel kullanımı **temsil etmeyen** tahminlerdir. Sapmanın yönü bilinmiyor.
- Sözcük türü uyumu iki biçimde verilir: küme ölçütü (iyimser) ve tek etiketli lemmalar (katı). İkisi de en sık etiket taban çizgisiyle karşılaştırılır.
- Kök bulma oranı düşüktür. Olası neden, `forms.tsv.gz` dosyasının yalnızca Wîkîferheng'de çekim tablosu olan kelimeleri içermesidir. Bu bir hipotezdir, sonraki sürümde ölçülecektir.

## Yeniden üretme
```bash
git clone --depth 1 https://github.com/unimorph/kmr.git ext/um-kmr
git clone --depth 1 https://github.com/UniversalDependencies/UD_Northern_Kurdish-Kurmanji.git ext/ud-kmr
python scripts/evaluate.py ext
```
