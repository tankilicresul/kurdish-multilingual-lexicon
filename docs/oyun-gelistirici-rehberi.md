# Kürtçe Oyun ve Uygulama Geliştirici Rehberi

> ⚠️ Taslak. GameVan Studio'nun Kürtçe kelime oyunlarını (Peyv) geliştirirken karşılaştığı sorunlardan derlendi.

## 1. Harfler ve fontlar
- **Kurmancî (Latin):** `ê î û ç ş` ve büyükleri `Ê Î Û Ç Ş` mutlaka görünmeli. Fontu bu harflerle test edin. Sorunsuz örnekler: Noto Sans, Baloo 2, Inter, Roboto.
- **Soranî / Güney Kürtçesi / Goranî (Arap kökenli):** `ڵ ڕ ۆ ێ ڤ ھ ە` harflerini destekleyen bir font kullanın (ör. Noto Naskh Arabic, Noto Sans Arabic, Vazirmatn) ve arayüzü `dir="rtl"` yapın.
- **Benzer görünen karakterler:** `ک` (U+06A9) ile `ك` (U+0643), `ی` (U+06CC) ile `ي` (U+064A), `ھ` (U+06BE) ile `ه` (U+0647) farklı kod noktalarıdır. Kelime karşılaştırmadan önce normalleştirin.
- **Yazı tipini uygulamaya gömün.** Çevrimdışı çalışır ve kullanıcının IP adresi üçüncü taraf font sunucularına gitmez (KVKK/GDPR açısından da daha güvenli).

## 2. Büyük ve küçük harf (en sık yapılan hata)
Türkçe yerel ayarı Kurmancî için **yanlıştır**:

| Kod | Sonuç | Doğru mu? |
|---|---|---|
| `'pisîk'.toLocaleUpperCase('tr')` | `PİSÎK` | ❌ |
| `'pisîk'.toUpperCase()` | `PISÎK` | ✅ (çoğu ortamda) |
| `upper('pisîk')` ([tools/js/kurdi.js](../tools/js/kurdi.js)) | `PISÎK` | ✅ her ortamda |

Aynı şekilde küçültmede `I → i` olmalı, `ı` değil.

## 3. Klavye
- Ekran klavyesi düzenleri: [`data/alphabets/keyboards.json`](../data/alphabets/keyboards.json). Kurmancî düzeninde 31 harfin hepsi basılı tutmadan erişilebilir.
- Kullanıcılar telefonda çoğu zaman `é, ì, ù` ya da Türkçe `ı, ü` yazar. Girdiyi `normalize(text, fixTyping=true)` ile düzeltin ve kullanıcıya doğru biçimi gösterin.

## 4. Sıralama
Hawar alfabesi sırası: `a b c ç d e ê f g h i î j k l m n o p q r s ş t u û v w x y z`.
Türkçe sıralama (`localeCompare(…, 'tr')`) Kurmancî için yanlıştır. `compare()` ya da `sort_key()` kullanın.

## 5. Kelime listesi seçimi
- **Kelime oyunu (Wordle tarzı):** `data/games/kmr-5-harf.tsv`. Sıklık sırasıyla gelir; en üstteki birkaç yüz kelime günlük bulmaca için uygundur.
- **"Gerçek kelime mi?" kontrolü:** aynı listedeki tüm kelimeleri izin listesi olarak kullanın, ya da `data/kmr/kmr-tr.tsv` içindeki tüm başlık kelimelerini.
- **Eğitim ve quiz:** `data/themes/` (konulara göre) ve `data/learner/kmr-top3000.tsv` (sıklığa göre).
- **Çekimli biçimlerden kaçının:** `bayek` (bir rüzgâr), `jinek` (bir kadın), `dihat` (geliyordu) gibi biçimler kelime oyunlarında kafa karıştırır. `data/games/` listeleri bu tür biçimleri büyük ölçüde ayıklar.
- **Kişi adlarına dikkat:** `Rojda`, `Şevîn`, `Agirî` gibi kelimeler aynı zamanda kişi ya da yer adıdır.

## 6. Lehçe seçimi
- Türkiye, Suriye ve Avrupa diasporası için ana kitle çoğunlukla **Kurmancî**dir.
- Irak Kürdistan Bölgesi ve İran'ın bir kısmı için **Soranî**.
- Dersim, Bingöl ve çevresi için **Zazakî**.
- Uygulamada lehçeyi açıkça yazın (ör. "Kurmancî"). Sadece "Kürtçe" yazmak kullanıcıyı yanıltabilir.

## 7. Ses
- Kurmancî için açık ve yüksek kaliteli bir metinden sese (TTS) motoru sınırlıdır. Türkçe TTS ile Kürtçe kelime okutmak yanlış telaffuz üretir.
- En iyi çözüm, anadil konuşucusuna kelimeleri kaydettirmektir (izinli ve açık lisansla).

## 8. İçerik kontrolü (yayından önce zorunlu)
1. Kelime ↔ anlam çiftini **anadil konuşucusu** onaylasın.
2. Otomatik ön kontrol için yazım denetleyiciler (ör. Rastnivîs/mazdek, Kurdish-Tech yazım denetleyicisi) ve iki bağımsız sözlük kullanılabilir. Ancak bunlar insan kontrolünün yerini tutmaz.
3. Argo, kaba ya da siyasi çağrışımlı kelimeleri çocuklara yönelik içerikten çıkarın. Vikisözlük argo anlamları da içerir.

## 9. Lisans
Bu depodaki kelimeleri oyununuzda kullanabilirsiniz (CC BY-SA 4.0). Yapmanız gerekenler:
- Uygulamada (ör. ayarlar ya da hakkında ekranında) **kaynak gösterin**: "Kelime verisi: Ferhenga Pirzimanî / Wiktionary, CC BY-SA 4.0".
- Kelime listesini değiştirip **yeniden dağıtıyorsanız** aynı lisansla paylaşın.

Oyunun kodu bundan etkilenmez; yalnızca kelime verisinin kendisi CC BY-SA kapsamındadır. Ticari kullanımda kesin değerlendirme için bir hukukçuya danışın.
