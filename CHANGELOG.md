# Değişiklik Günlüğü / Changelog

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
