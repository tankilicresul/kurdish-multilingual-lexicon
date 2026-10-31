# Kontrol Süreci / Review Process

Bu depodaki veri **otomatik** derlendi. Kullanıma açılmadan önce anadil konuşucuları tarafından kontrol edilmelidir.

## Kim kontrol eder?
- Her dil kolu için o kolun **anadil konuşucusu** (Kurmancî, Soranî, Güney Kürtçesi, Zazakî ayrı ayrı).
- Hedef dil (Türkçe / İngilizce / Almanca) için o dili iyi bilen biri.
- Tarih belgeleri için Kürt dili ve edebiyatı alanında akademik geçmişi olan biri.

## Nereden başlanır? (önem sırasıyla)
1. `data/themes/` (263 temel kavram, 4 lehçe): en çok kullanılacak, en hızlı kontrol edilecek liste
2. `data/learner/kmr-top3000.tsv` (en sık 3.000 kelime)
3. `data/games/kmr-5-harf.tsv` (kelime oyunları)
4. `data/core/kmr-tr.core.tsv` (5.519 satır, iki kaynağın onayladığı çiftler), ardından `-en` ve `-de`
5. `data/cross-dialect.tsv` (lehçeler arası eşleşmeler)
6. Diğer dosyalar

## Nasıl işaretlenir?
`review_status` sütunu şu değerlerden birini alır:

| Değer | Anlamı |
|---|---|
| `unverified` | Henüz bakılmadı (varsayılan) |
| `ok` | Doğru |
| `fixed` | Düzeltildi (`note` sütununa eski hâli yazılır) |
| `regional` | Doğru ama bölgesel/ağız kullanımı (`note`'ta bölge) |
| `rare` | Doğru ama nadir/eski/teknik |
| `wrong` | Yanlış, silinmeli |

`reviewer` sütununa kontrol edenin adı ya da kısaltması, `note` sütununa açıklama yazılır.

## Kurallar
1. Yazım **standart yazı diline** göre yapılır: Kurmancî için Hawar alfabesi, şapkalı harfler (ê î û) korunur.
2. Bölgesel biçim standart biçimin yerine konmaz; ayrı satır olarak `regional` işaretlenir.
3. Telifli sözlüklerden toplu kopyalama yapılmaz.
4. Tarih belgelerinde her iddia bir kaynağa bağlanır; kaynaksız iddia "kontrol edilecek" olarak kalır.
5. Siyasi yorum eklenmez; yalnızca kayıtlı olgular yazılır.

## Kontrol durumu

| Dosya | Kontrol eden | Durum |
|---|---|---|
| data/themes/*.tsv | — | Başlanmadı |
| data/learner/kmr-top3000.tsv | — | Başlanmadı |
| data/games/kmr-5-harf.tsv | — | Başlanmadı |
| data/alphabets/*.json | — | Başlanmadı |
| data/kmr/db/lemmas.tsv (sözcük türü, cinsiyet) | — | Başlanmadı |
| data/kmr/db/etymology.tsv | — | Başlanmadı (etimoloji uzmanı gerekir) |
| data/kmr/db/etymology-class.tsv (önce en sık 5.000 kelime) | — | Başlanmadı (etimoloji uzmanı gerekir; `borrowed-iranian` satırlarına öncelik) |
| docs/dilbilgisi/*.md (dil bilgisi kitabı) | — | Başlanmadı (Kurmancî öğretmeni ya da dilbilimci) |
| docs/dilbilgisi/07-lehce-karsilastirma.md (Soranî/Zazakî örnekleri) | — | Başlanmadı (Soranî ve Zazakî anadil konuşucusu) |
| data/kmr/db/verb-stems.tsv (şimdiki gövdeler, `rule-*` satırları) | — | Başlanmadı |
| data/kmr/db/proverbs-idioms.tsv | — | Başlanmadı |
| data/core/kmr-tr.core.tsv | — | Başlanmadı |
| data/core/kmr-en.core.tsv | — | Başlanmadı |
| data/core/kmr-de.core.tsv | — | Başlanmadı |
| data/cross-dialect.tsv | — | Başlanmadı |
| docs/tarih.md | — | Başlanmadı |
| docs/lehceler.md | — | Başlanmadı |
| docs/alfabeler.md | — | Başlanmadı |
| docs/oyun-gelistirici-rehberi.md | — | Başlanmadı |
| README.ku.md, README.de.md | — | Başlanmadı (çeviriler anadil kontrolü bekliyor) |
