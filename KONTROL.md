# Kontrol Süreci / Review Process

Bu depodaki veri **otomatik** derlendi. Kullanıma açılmadan önce anadil konuşucuları tarafından kontrol edilmelidir.

## Kim kontrol eder?
- Her dil kolu için o kolun **anadil konuşucusu** (Kurmancî, Soranî, Güney Kürtçesi, Zazakî ayrı ayrı).
- Hedef dil (Türkçe / İngilizce / Almanca) için o dili iyi bilen biri.
- Tarih belgeleri için Kürt dili ve edebiyatı alanında akademik geçmişi olan biri.

## Nereden başlanır?
1. `data/core/kmr-tr.core.tsv` (5.523 satır, iki kaynağın onayladığı çiftler)
2. `data/core/kmr-en.core.tsv` ve `kmr-de.core.tsv`
3. `data/cross-dialect.tsv` (lehçeler arası eşleşmeler)
4. Diğer dosyalar

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
| data/core/kmr-tr.core.tsv | — | Başlanmadı |
| data/core/kmr-en.core.tsv | — | Başlanmadı |
| data/core/kmr-de.core.tsv | — | Başlanmadı |
| data/cross-dialect.tsv | — | Başlanmadı |
| docs/tarih.md | — | Başlanmadı |
| docs/lehceler.md | — | Başlanmadı |
| docs/alfabeler.md | — | Başlanmadı |
