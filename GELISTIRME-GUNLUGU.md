# Geliştirme Günlüğü ve Devir Teslim Notu

**Son güncelleme:** 1 Kasım 2026 · **Sürüm:** v0.4.0 · **Proje sahibi:** Resul Tankılıç (GameVan Studio)
**Hazırlayan:** Claude (Anthropic). Antigravity ve diğer geliştiriciler için yazıldı.

> Bu depoyla çalışmaya başlamadan önce bu dosyayı, [README.md](README.md), [DATASHEET.md](DATASHEET.md) ve [KONTROL.md](KONTROL.md) dosyalarını okuyun. Yapılan her önemli değişikliği gerekçesiyle bu dosyaya ekleyin, [CHANGELOG.md](CHANGELOG.md) dosyasını güncelleyin ve sürümü artırın.

## 1. Bu depo ne için var?
- **Ana amaç:** GameVan Studio'nun Kürtçe oyunlarına (önce **Peyv** uygulaması) veri temeli sağlamak. Oyunlar ile bu sözlük **birlikte** düşünülmelidir. Oyunların kelime listeleri, temaları, Wordle kelimeleri ve ileride yazım denetimi bu depodan beslenecek.
- **İkinci amaç:** Kürtçe proje yapmak isteyen herkese açık, akademik standartlarda bir kaynak sunmak (sözlük, dil bilgisi, etimoloji).
- **Kapsam:**
  - Kurmancî (ana): sözlük, dil bilgisi ve etimoloji.
  - Diğer çeşitler: Soranî, Güney Kürtçesi, Zazakî ve Goranî (daha küçük veri).
  - Karşılık dilleri: Türkçe, İngilizce, Almanca.
- **Önemli:** Hiçbir satır henüz anadil konuşucusu ya da dilbilimci tarafından kontrol edilmedi. Her satırda `review_status = unverified` yazar.

## 2. Sürüm geçmişi (ne zaman ne yapıldı, neden)
| Sürüm | Tarih | Ne yapıldı | Neden |
|---|---|---|---|
| v0.1.0 | 31.10.2026 | Vikisözlük'ün dört sürümünden kelime çiftleri; çekirdek küme; lehçeler arası tablo; Vikipedi sıklık listeleri; öğrenici, oyun (3–7 harf) ve tema listeleri; Python ve JS yardımcıları | Oyunlar için hızlı, lisansı temiz bir başlangıç verisi |
| v0.2.0 | 31.10.2026 | Dilbilimsel veritabanı: sözcük türü, cinsiyet, tanımlar, örnek, etimoloji metni, 330 bin çekimli biçim, ekler, fiil kökleri, atasözleri, ses kayıtları | Resul'un talebi: her kelimenin türü, kökü, eki, çekimli ve çekimsiz hâli |
| v0.3.0 | 31.10.2026 | Türkçe dil bilgisi kitabı (önce YKS tarzı), köken sınıflandırması (miras, alıntı, iç türetme, yansıma), 3.982 fiilin kurallı çekimi | Resul'un talebi: "kelime gerçekten Kürtçe mi" sorusu (Nişanyan benzeri) ve tek repoda sözlük ile dil bilgisi |
| v0.4.0 | 01.11.2026 | Akademik standartlar: CLDF Dictionary dışa aktarımı, UD ve UniMorph etiketleri, ISO 639-3 ve Glottolog kodları; dil bilgisi Leipzig glosslu betimleyici başvuru dil bilgisine dönüştürüldü, YKS soruları `docs/ogretim/` altına taşındı; UniMorph ve UD Kurmanji'ye karşı nicel değerlendirme; DATASHEET, kaynakça, Zenodo meta verisi | Resul'un talebi: "YKS benim fikrimdi, dilbilimcilerin kullandığı standart düzen olsun" |
| v0.5.0 | 01.11.2026 | Kademeli Mimari (Tier-1 Doğrulanmış Çekirdek, Tier-2 Araştırma Arşivi); Pivot dosyalarının `data/experimental/pivots/` altında izole edilmesi; `kmr-top3000` listesinin sıfır boşluklu ve temizlenmiş olarak yeniden inşası; `data/games/` sözlüklerinin audit ve hata düzeltmesi | Google AI denetim eleştirileri ve solo indie geliştirici optimizasyonu |

v0.4.0 bağımsız inceleme zincirinden geçti: kör karşı görüş (Ege) ve Doğrulayıcı. İlk turda ikisi de RED verdi, düzeltmelerden sonra ikisi de ONAY verdi. Düzeltilen ana noktalar:
- %98,5 oranı artık doğruluk sayılmıyor. Asıl ölçü ham %77,4.
- WALS tablosu, WALS'ın kendi değer listesine uyduruldu.
- Glosslardaki etiket hataları düzeltildi.
- Kişisel veri beyanı düzeltildi.
- Bir künye hatası düzeltildi.

## 3. Klasör haritası (kısa)
| Yol | İçerik |
|---|---|
| `data/multilingual/kmr-tr-en-de.tsv` | **Oyunlar için ana tablo:** 32 bin Kurmancî kelime, TR/EN/DE karşılık, sıklık sırası |
| `data/learner/kmr-top3000.tsv` | En sık 3.000 kelime (seviye ve ilerleme tasarımı için) |
| `data/games/kmr-3..7-harf.tsv` | Wordle ve kelime oyunları için harf sayısına göre listeler |
| `data/themes/*.tsv`, `themes.json` | 17 konu (renkler, hayvanlar, aile, yiyecek, yerler…), 4 lehçe |
| `data/kmr/db/` | Dilbilimsel veritabanı: `lemmas.tsv`, `forms.tsv.gz` (çekimli biçim → kök), `etymology-class.tsv`, `verb-paradigms.jsonl.gz`, `proverbs-idioms.tsv`, `audio.tsv` |
| `data/kmr/unimorph/` | UniMorph biçiminde çekimler |
| `cldf/` | CLDF Dictionary (dilbilim yazılımları için) |
| `docs/dilbilgisi/` | Betimleyici Kurmancî dil bilgisi (§0–7, terimler, paradigmalar) |
| `docs/ogretim/` | Alıştırmalar (oyunlarda soru bankası olarak kullanılabilir) |
| `docs/oyun-gelistirici-rehberi.md` | **Oyun geliştirirken okunacak rehber** |
| `tools/python/kurdi.py`, `tools/js/kurdi.js` | Kurdî büyük/küçük harf (*i → I*, *î → Î*), Hawar sıralaması, yazım düzeltme, sözlük arama |
| `scripts/` | Bütün verinin yeniden üretimi (bkz. `docs/yeniden-uretim.md`) |

## 4. Oyunlarda kullanırken dikkat
1. **Büyük harf:** Türkçe yerel ayarı kullanılmamalı. `toUpperCase('tr')` *i* harfini İ yapar, oysa Kurmancî'de doğrusu I'dır. `kurdi.js` içindeki `upper()` kullanılmalı.
2. **Wordle ve kelime listeleri:** `data/games/` içindeki listeler çekimli biçimlerden ve özel adlardan süzüldü, ama elle kontrol edilmedi. Günlük kelimeler yayına girmeden önce bir anadil konuşucusuna gösterilmeli.
3. **Çeviriler:** Edat ve bağlaç gibi işlev sözcüklerinin çevirisi bağlama bağlıdır. Oyunda tek kelimelik karşılık gösterirken `core/` dosyalarındaki ya da `confidence = high` olan çiftler tercih edilmeli.
4. **Atasözleri:** Bazıları kaba ya da eski değerleri yansıtıyor olabilir. Çocuklara yönelik içerikte süzülmeden kullanılmamalı.
5. **Lisans:** Veri CC BY-SA 4.0 lisanslı. Oyunda kullanılırsa uygulamanın "Hakkında" ya da "Lisanslar" ekranında Vikisözlük katkıcılarına atıf yapılmalı. Kod MIT lisanslı.
6. **Ses kayıtları:** `audio.tsv` yalnızca Wikimedia Commons bağlantılarını içerir. Her kaydın lisansı ve konuşucu atfı ayrı ayrı korunmalı.

## 5. Ortam ve araçlar
- **Repo:** https://github.com/tankilicresul/kurdish-multilingual-lexicon (public). Masaüstü kopyası: `Desktop/kurdish-multilingual-lexicon`.
- **Otomatik kontroller (GitHub Actions):** veri doğrulama, CLDF doğrulaması, Python ve JS testleri. Her push'ta çalışır.
- **Yazım denetimi:** Kurmancî örnekler mazdek AI bağlayıcısının Rastnivîs denetiminden geçirildi. Denetim ücretsiz; çeviri işlemleri aylık kotadan düşer.
- **Değerlendirme:** `scripts/evaluate.py`. Dış veriler (UniMorph kmr, UD Kurmanji) depoya kopyalanmaz, `ext/` klasörüne indirilir.

## 6. Açık işler (öncelik sırasıyla)
1. **Uzman kontrolü:** Kontrol edilecek dosyalar ve öncelik sırası `KONTROL.md` dosyasında. İlk iş: fiil çekimi uyuşmazlık listesinde (`data/kmr/review/paradigms-vs-unimorph.tsv`) `decision` sütununun bir Kurmancî dilbilimcisi tarafından doldurulması.
2. **Kalıcı DOI:** Zenodo hesabını GitHub'a bağlayıp bir sürüm (release) yayımlamak. Meta veri `.zenodo.json` dosyasında hazır. Arşivlenen sürüm geri alınamaz, karar Resul'un.
3. **Kök bulma oranını artırmak:** Kurallı çekimleri `forms.tsv.gz` ile birleştirip UD üzerinde yeniden ölçmek (şu an %59,2).
4. **Soranî verisini büyütmek:** Şu an zayıf. Kaynak olarak ckb.wiktionary ve açık Soranî derlemleri araştırılabilir.
5. **Seviye çerçevesi:** Öğrenici listesini CEFR A1–C2 ile eşleştirmek (oyunlardaki ilerleme sistemi için).
6. **Sayfa düzeyinde atıflar:** Dil bilgisindeki kuralların kaynaklardaki sayfa numaralarıyla doğrulanması.

## 7. Bilinen teknik notlar
- Masaüstü kopyası 1 Kasım 2026'da yarım güncellendi. Bağlantı koptu ve kilit dosyaları kaldı. Çözüm, klasörde şunları çalıştırmak:
  ```
  del .git\index.lock .git\objects\maintenance.lock
  git fetch origin
  git reset --hard origin/main
  ```
- Büyük tablolar: `cldf/*.csv.zip` sıkıştırılmış saklanır (pycldf doğrudan okur). `forms.tsv.gz` ve `lemmas.jsonl.gz` gzip dosyalarıdır.
- `scripts/standards.py`, `forms.tsv.gz` dosyasını yerinde yeniden yazar (`ud_feats` ve `unimorph` sütunlarını ekler). `build_db.py` çalıştırıldıktan sonra `standards.py` de yeniden çalıştırılmalıdır.
