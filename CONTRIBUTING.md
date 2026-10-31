# Katkı Rehberi / Contributing / Alîkarî

Bu depo bir **taslaktır**. Kürtçenin herhangi bir kolunun (Kurmancî, Soranî, Güney Kürtçesi, Zazakî, Goranî) anadil konuşucusuysanız en değerli katkı **kontrol etmektir**.

## Katkı yolları
1. **Hata bildir:** *Issues → Düzeltme* şablonu. Yazılım bilgisi gerekmez.
2. **Satır kontrol et:** bir `.tsv` dosyasını (Excel, LibreOffice ya da Google Sheets ile açılır) indirin, [KONTROL.md](KONTROL.md)'deki kurallarla `review_status`, `reviewer` ve `note` sütunlarını doldurun, *Pull Request* ya da *Issue* ile gönderin.
3. **Kaynak öner:** açık lisanslı (CC0, CC BY, CC BY-SA, MIT…) bir sözlük, derlem ya da kelime listesi biliyorsanız *Issues → Yeni kaynak*.
4. **Kod:** `scripts/` ve `tools/` iyileştirmeleri. Göndermeden önce şunları çalıştırın:
   ```bash
   python3 scripts/validate.py data && python3 -m unittest tools/tests/test_kurdi.py && node tools/tests/test_kurdi.mjs
   ```

## Kurallar
- **Telifli kaynaklardan toplu kopyalama yapmayın** (basılı sözlükler, Ferheng.org, Enstîtuya Kurdî sözlükleri vb.). Tek tek kontrol için başvurulabilir.
- Standart yazı dilini esas alın (Kurmancî için Hawar alfabesi). Bölgesel biçimleri silmeyin, `regional` olarak işaretleyin.
- Belgelerde her tarihî iddiaya kaynak ekleyin. Siyasi yorum eklemeyin.
- Saygılı olun: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## English (short)
This is a draft dataset. The most valuable contribution is **review by native speakers**. Open an issue using the *Correction* template, or edit `review_status`/`reviewer`/`note` in any TSV following [KONTROL.md](KONTROL.md). Do not bulk-copy from copyrighted dictionaries. Run the validation and tests before opening a PR.

## Deutsch (kurz)
Dies ist ein Entwurf. Am wertvollsten ist die **Prüfung durch Muttersprachler**. Fehler bitte als Issue melden (Vorlage *Düzeltme/Correction*). Keine Massenübernahme aus urheberrechtlich geschützten Wörterbüchern.

## Kurmancî (kurt)
Ev depo reşnivîs e. Alîkariya herî bi qîmet **kontrolkirina** peyvan ji aliyê axêverên zikmakî ve ye. Şaşiyan bi şablona *Düzeltme* ragihîne.
