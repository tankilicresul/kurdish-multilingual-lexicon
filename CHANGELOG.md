# Değişiklik Günlüğü / Changelog

## v0.4.0 · 31.10.2026 · Akademik standartlar ve değerlendirme (kontrol edilmedi)
- **CLDF Dictionary** dışa aktarımı (`cldf/`): 169.925 madde, 190.232 anlam, 14.416 örnek; ISO 639-3 ve Glottolog kodlarıyla; `cldf validate` ile doğrulandı
- `forms.tsv.gz` dosyasına **UD** (`ud_feats`) ve **UniMorph** (`unimorph`) sütunları; `data/<v>/unimorph/` dosyaları (veride geçen 293.013 + kuralla üretilen 143.352 satır)
- **Nicel değerlendirme** (`scripts/evaluate.py`, `docs/degerlendirme*.md`, `data/EVAL.json`): UniMorph kmr ve UD Kurmanji ağaç bankasına karşı; uyuşmazlık listesi `data/kmr/review/`
- Dil bilgisi **betimleyici başvuru dil bilgisine** dönüştürüldü: giriş ve yöntem bölümü, WALS tipolojik profili, Leipzig glossing ile 24 numaralı örnek, kısaltma listesi, terim karşılıkları (TR/KU/EN)
- Alıştırmalar öğretim ekine taşındı (`docs/ogretim/`)
- `DATASHEET.md` (Datasheets for Datasets / Data Statements), `docs/standartlar.md`, `docs/kaynakca.bib` (BibTeX), `.zenodo.json`, CITATION.cff özeti
- Düzeltme: *anîn* fiilinin düzensiz şimdiki zaman ve dilek kipi biçimleri (*tînim*, *bînim*)

## v0.3.0 · 31.10.2026 · Dil bilgisi kitabı ve etimoloji (kontrol edilmedi)
- `docs/dilbilgisi/`: Türkçe yazılmış Kurmancî dil bilgisi kitabı. 8 bölüm: ses ve yazım, isim/izafet/zamir, sıfat/sayı/edat, fiil (tüm zamanlar, ergatiflik), kelime yapımı, cümle ve soru, lehçe karşılaştırması, 30 soruluk YKS tarzı test ve cevap anahtarı. Örnekler Rastnivîs (mazdek) yazım denetiminden geçirildi.
- `docs/dilbilgisi/paradigmalar.md`: isim ve fiil çekim tabloları (otomatik)
- `data/kmr/db/etymology-class.tsv`: 156.692 madde için köken sınıfı (miras, iç türetme, alıntı, İran dillerinden alıntı, yansıma), kaynak dil, dil ailesi, köken yolu, kanıt türü, güven düzeyi
- `data/kmr/db/verb-stems.tsv` ve `verb-paradigms.jsonl.gz`: 3.982 fiil için gövde ve tam çekim (254.848 biçim; 9.335'i veride de geçiyor)
- `docs/etimoloji.md`: yöntem, sınıflar, istatistikler, tarihî ve akademik kaynaklar
- `scripts/etymology_classify.py`, `scripts/paradigms.py`

## v0.2.0 · 31.10.2026 · Dilbilimsel veritabanı (kontrol edilmedi)
- `data/<lehçe>/db/`: madde başları sözcük türü (UPOS), cinsiyet, Kurmancî ve İngilizce tanımlar, örnek cümleler, etimoloji (Kurmancî + İngilizce), ek-kök ayrımı, köken dili, IPA, heceleme, Arap/Kiril yazımları, eş/zıt/türetilmiş/ilgili kelimeler, çeviriler, sıklık sırasıyla
- Kurmancî: 158.393 madde, 329.942 çekimli biçim (kök + hâl/sayı/kişi/zaman etiketleri), 86.916 etimoloji, 561 ek, 531 fiil gövdesi, 21.009 atasözü/deyim, 3.099 ses kaydı bağlantısı
- Soranî, Zazakî, Güney Kürtçesi, Goranî için aynı yapıda (daha küçük) veritabanları
- `scripts/build_db.py`, `docs/veritabani.md`, `data/DB-STATS.json`

## v0.1.0 · 31.10.2026 · İlk taslak (kontrol edilmedi)
- Kurmancî, Soranî, Zazakî, Güney Kürtçesi ve Goranî ↔ Türkçe / İngilizce / Almanca kelime çiftleri (Vikisözlük'ün dört sürümünden, Wiktextract ile)
- Çekirdek küme: iki bağımsız kaynağın onayladığı çiftler
- Lehçeler arası eşleştirme tablosu ve Kurmancî üzerinden türetilmiş (pivot) dosyalar
- Kürtçe Vikipedilerden sıklık listeleri (Kurmancî, Soranî, Zazakî)
- Türetilmiş tablolar: dört dilli ana tablo, öğrenici listesi (3.000), oyun listeleri (3-7 harf), 17 konuda tema listeleri
- Alfabe ve ekran klavyesi JSON dosyaları
- Python ve JavaScript yardımcıları (Kurdî büyük/küçük harf, Hawar sıralaması, yazım düzeltme) ve testleri
- Doğrulama betiği, GitHub Actions, sorun ve PR şablonları
- Belgeler: Kürt dili tarihi, lehçeler, alfabeler, oyun geliştirici rehberi, sıklık yöntemi, yeniden üretim
- Dört dilde README (Türkçe, İngilizce, Almanca, Kurmancî)
