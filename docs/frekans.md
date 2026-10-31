# Sıklık Listeleri: Yöntem ve Sınırlar

Dosyalar: `data/frequency/{kmr,ckb,zza}-wikipedia-frequency.tsv` (her biri en sık 50.000 kelime)

| Lehçe | Kaynak | Kullanılan madde | Farklı kelime |
|---|---|---:|---:|
| Kurmancî | Kürtçe Vikipedi (ku) | 5.796 | 202.236 |
| Soranî | Soranî Vikipedi (ckb) | 13.031 | 424.680 |
| Zazakî | Zazaca Vikipedi (diq) | 727 | 61.769 |

## Yöntem
- Yalnızca ana ad alanındaki maddeler kullanıldı; yönlendirmeler atlandı.
- Viki biçimlendirmesi (şablonlar, tablolar, kaynakçalar, kategori ve dosya bağlantıları) kaba bir temizlikle çıkarıldı.
- Temizlikten sonra 1.200 karakterden kısa maddeler atlandı. Kürtçe Vikipedilerde botların ürettiği çok sayıda kısa taslak madde var ve bunlar sayımı çarpıtır.
- Sıralama **belge sıklığına** göre yapıldı: bir kelimenin kaç farklı maddede geçtiği. Bu ölçü, uzun ve tekrarlı maddelere karşı ham sayımdan daha dayanıklıdır.
- Kurmancî küçük harfe çevirme kuralı: `I → i`, `Î → î`.

## Sınırlar
- **Ansiklopedi metni günlük dili yansıtmaz.** Örneğin *sal* (yıl) 155. sırada iken *av* (su) 613., *heval* (arkadaş) 1.996., *pisîk* (kedi) ise 11.460. sırada.
- Zazaca Vikipedi küçüktür (727 madde); liste güvenilir değildir.
- Özel adlar, yer adları ve yabancı kelimeler listede yer alır.
- Konuşma diline daha yakın bir liste için açık lisanslı bir derlemle (ör. KurdishCorpus-clean, OSCAR) yeniden hesaplanması önerilir.
