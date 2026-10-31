# Veri Belgesi (Datasheet)

Gebru vd. (2021) *Datasheets for Datasets* ve Bender & Friedman (2018) *Data Statements* çerçevelerine göre hazırlanmıştır.

## 1. Amaç
- **Neden oluşturuldu?** Kürtçe için açık lisanslı, makine okunur ve kaynağı izlenebilir bir sözlük ve dil bilgisi kaynağı sağlamak. Hedef kullanıcılar: Kürtçe eğitim materyali, oyun, uygulama ve dil teknolojisi geliştirenler; dilbilim araştırmacıları.
- **Kim oluşturdu?** GameVan Studio (Resul Tankılıç). İlk derleme bir yapay zekâ asistanıyla (Anthropic Claude) yapıldı.
- **Finansman:** Yok.

## 2. İçerik
| Bileşen | Kurmancî | Diğer çeşitler |
|---|---:|---|
| Madde başı (sözcük türüyle) | 158.393 | Soranî 7.232 · Zazakî 3.314 · Güney 819 · Goranî 167 |
| Çekimli biçim (veride geçen) | 329.942 | çok az |
| Kuralla üretilen fiil çekimi | 3.982 fiil / 254.848 biçim | – |
| Köken sınıfı | 156.692 | – |
| Türkçe / İngilizce / Almanca karşılık çifti | 141.086 / 179.651 / 71.981 | [STATS.md](data/STATS.md) |
| Atasözü ve deyim | 21.009 | – |

- **Birim:** madde başı (kelime + sözcük türü). Aynı yazımlı farklı sözcük türleri ayrı satırdır.
- **Etiketler:** UPOS, cinsiyet, UD ve UniMorph özellikleri, köken sınıfı, `review_status`.
- **Eksik bilgi:** Maddelerin yaklaşık %57'sinde köken bilgisi yok. Güney Kürtçesi ve Goranî verisi çok küçüktür. Bu iki çeşitte çeviri çiftlerinin bir kısmı Kurmancî üzerinden türetilmiştir (`.pivot.tsv`).
- **Kişisel veri:** Sınırlı olarak **vardır**. `audio.tsv` dosyasında ses kaydı yapan konuşucuların Wikimedia Commons kullanıcı adları (takma ad) ve beyan ettikleri bölge yer alır. Bu bilgiler kaynağın lisansındaki atıf yükümlülüğü için tutulur ve Commons'ta zaten kamuya açıktır. Kaldırma isteği için: [CONTRIBUTING.md § Kişisel veri](CONTRIBUTING.md#kişisel-veri-ve-kaldırma-isteği).
- **Hassas içerik:** Atasözleri ve deyimler arasında kaba ya da eski dönem değerlerini yansıtan ifadeler olabilir. Çocuklara yönelik ürünlerde süzülmeden kullanılmamalıdır.

## 3. Toplama süreci
- **Kaynaklar:**
  - Wîkîferheng (ku.wiktionary)
  - İngilizce, Türkçe ve Almanca Vikisözlük: Wiktextract ile ayrıştırıldı (Ylonen 2022; kaikki.org dökümleri, Ekim 2026)
  - Kurmancî, Soranî ve Zazakî Vikipedi dökümleri: sıklık listeleri için
  - Lingua Libre ses kayıtları: yalnızca bağlantılar
- **Yöntem:** Tamamen otomatik. Kural tabanlı süzme, eşleme ve sınıflandırma. Betikler `scripts/` içindedir. Bütün veri [yeniden üretilebilir](docs/yeniden-uretim.md).
- **Zaman aralığı:** Kaynak dökümleri Ekim 2026 tarihlidir.

## 4. Dil durumu (Data Statement)
- **Çeşitler:** Kurmancî (`kmr`, nort2641), Soranî (`ckb`, cent1972), Güney Kürtçesi (`sdh`, sout2640), Zazakî (`zza`, zaza1246), Goranî (`hac`, gura1251).
- **Yazı dili:** Ağırlıklı olarak standart yazı dili. Wîkîferheng katkıcılarının bölgesel biçimleri de vardır (`(devokî)` ve bölge etiketleri). Ağız bilgisi sistematik değildir.
- **Metin türü (sıklık listeleri):** Ansiklopedi metni. Gündelik konuşma kelimeleri olduğundan daha nadir görünür.
- **Katkıcılar:** Wîkîferheng gönüllüleri. Demografik bilgi yoktur.

## 5. Ön işleme ve temizlik
- Unicode NFC normalleştirme ve Kurdî büyük/küçük harf kuralları (`tools/`).
- Ad, soyad ve "bir tür …" gibi çeviri sayılamayacak tanımlar süzüldü.
- Çekimli biçimler ana listelerden ayrıldı.
- Ham dökümler depoya eklenmedi. İndirme ve yeniden üretme komutları belgelendi.

## 6. Kalite
- **İnsan incelemesi:** Henüz yapılmadı. Her satırda `review_status = unverified` yazar.
- **Otomatik değerlendirme:** UniMorph kmr ve UD Kurmanji ağaç bankasına karşı ölçüldü: [degerlendirme-sonuclari.md](docs/degerlendirme-sonuclari.md). Bu ölçümde:
  - UD metinlerinin %82,7'si sözlükte bulunuyor.
  - UD'nin elle verdiği sözcük türü, sözlükteki türlerle %89,0 oranında uyumlu (küme ölçütü). Sözlükte tek sözcük türü olan lemmalarda uyum %89,2 (n = 3.991); en sık etiket taban çizgisi %30,7.
  - Kurallı fiil çekimi UniMorph ile ham olarak %77,4 oranında eşleşiyor. Uyuşmazlıkların ön sınıflandırması uzman kararını bekliyor; UniMorph tam bağımsız bir kaynak değil.
  - Hiçbir ölçüm insan doğrulamasına dayanmıyor.
- **Bilinen hata türleri:** [README § Bilinen sınırlar](README.md#bilinen-sınırlar), [etimoloji.md § 6](docs/etimoloji.md#6-bilinen-sorunlar).

## 7. Kullanım
- **Uygun kullanımlar:**
  - Sözlük ve öğrenme uygulamaları
  - Kelime oyunları
  - Yazım denetimi ve biçimbilim araçları için başlangıç verisi
  - Sözcük türü etiketleme ve kök bulma için sözlük özelliği
  - Dilbilim araştırmasında ön tarama
- **Uygun olmayan kullanımlar:**
  - İnceleme yapılmadan resmî belge çevirisi ya da hukuki ve tıbbi çeviri
  - Etimoloji sınıflarını tek başına dil arılaştırma (purizm) ya da "gerçek Kürtçe / değil" yargısı için kullanmak (bkz. [etimoloji.md § 1](docs/etimoloji.md#1-önce-bir-ilke-alıntı-kelime-de-kürtçedir))
  - Değerlendirme verisi olarak kullanmak: veri otomatik olduğu için test kümesi olarak uygun değildir
- **Önyargılar:**
  - Kurmancî verisi diğer çeşitlerden çok daha büyük. Soranî gibi büyük bir çeşit olması gerekenden zayıf temsil ediliyor.
  - Teknik terimler (Fransızca ve İngilizce alıntılar) Wîkîferheng'in ağırlığından dolayı fazla temsil ediliyor.

## 8. Dağıtım ve bakım
- **Lisans:** Veri ve belgeler CC BY-SA 4.0 (Vikisözlük ve Vikipedi'den türetildiği için). Kod MIT.
- **Erişim:** https://github.com/tankilicresul/kurdish-multilingual-lexicon · CLDF: `cldf/`
- **Sürümleme:** Anlamsal sürümleme ([CHANGELOG.md](CHANGELOG.md)). Zenodo arşivi ve DOI için meta veri hazır: [`.zenodo.json`](.zenodo.json). Arşiv henüz oluşturulmadı, DOI yok.
- **Hata bildirimi ve düzeltme:** GitHub Issues (Düzeltme şablonu), [CONTRIBUTING.md](CONTRIBUTING.md).
- **Bakım:** GameVan Studio. Anadil konuşucusu ve dilbilimci katkıcılar aranıyor.
