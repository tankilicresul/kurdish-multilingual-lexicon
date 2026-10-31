# 2. İsim, İzafet ve Zamir (Navdêr, Îzafe û Cînav)

## 2.1 Cinsiyet (zayend)
Her isim ya **eril** (*nêr*) ya da **dişil** (*mê*) cinstendir. Canlılarda cinsiyet genellikle doğal cinsiyete uyar (*bav* "baba" eril, *dê* "anne" dişil). Cansız varlıklarda ezberlemek gerekir. Kurmancî'de cansız isimlerin çoğu dişildir.

| Eril | Dişil |
|---|---|
| *bav* (baba), *bira* (erkek kardeş), *kur* (oğul) | *dê* (anne), *xwişk* (kız kardeş), *keç* (kız) |
| *nan* (ekmek), *dest* (el) | *mal* (ev), *baran* (yağmur), *pisîk* (kedi) |

Cinsiyet en çok **izafet ekinde** ve **tekil bükümlü hâlde** görünür. Bir ismin cinsiyeti depoda: [`data/kmr/db/lemmas.tsv`](../../data/kmr/db/), `gender` sütunu.

**Ağız notu:** Cinsiyet bazı ağızlarda (ör. Batı ağızlarının bir kısmı) zayıflamıştır. Bir ismin cinsiyeti ağızdan ağıza değişebilir.

## 2.2 Belirlilik
Kurmancî'de belirli tanımlık yoktur. **Yalın isim belirlidir**, belirsizlik ek ile gösterilir.

| | Tekil | Çoğul |
|---|---|---|
| Belirli | *pisîk* (kedi) | *pisîk* (kediler) |
| Belirsiz | *pisîkek* (bir kedi) | *hin pisîk* / *pisîkin* (bazı kediler) |

Belirli çoğulun yalın hâli tekille aynıdır. Çoğulluk fiilden, izafet ekinden (*-ên*) ya da bükümlü ekten (*-an*) anlaşılır: *Pisîk hatin.* = Kediler geldi.

## 2.3 Hâl (rewş): yalın ve bükümlü
Kurmancî'de iki temel hâl vardır:
- **Yalın hâl** (*rewşa xwerû*): cümlenin öznesi (geçmiş zamanda geçişsiz fiillerle), şimdiki zamanda özne.
- **Bükümlü hâl** (*rewşa çemandî*): edatlardan sonra; şimdiki zamanda nesne; geçişli fiilin geçmiş zamanında özne (bkz. [ergatiflik](04-fiil.md#47-ergatiflik)).

| | Eril tekil | Dişil tekil | Çoğul |
|---|---|---|---|
| Yalın, belirli | *bajar* | *mal* | *mal* |
| Bükümlü, belirli | *bajêr* / *bajarî* | *malê* | *malan* |
| Yalın, belirsiz | *bajarek* | *malek* | *hin mal* |
| Bükümlü, belirsiz | *bajarekî* | *malekê* | *malinan* |

Örnekler:
- *Ez li **malê** me.* = Evdeyim. (*li* edatından sonra dişil bükümlü *-ê*)
- *Ez ji **hevalan** re dinivîsim.* = Arkadaşlara yazıyorum. (çoğul bükümlü *-an*)

**Eril tekil bükümlü hâl** ağızlara göre değişir. Bazı ağızlarda *-î* eki (*bavî*), bazılarında kök ünlüsünün değişmesi (*bajar* → *bajêr*) kullanılır. Birçok konuşmada ise eril isim bükümlü hâlde değişmez. Ancak işaret sıfatından sonra genellikle görünür: *vî bajarî* (bu şehri/bu şehirde).

## 2.4 Seslenme hâli
| Eril | Dişil | Çoğul |
|---|---|---|
| *-o*: *Kurdo!* (Ey Kürt!) | *-ê*: *Keçê!* (Kızım! / Ey kız!) | *-(i)no*: *Hevalno!* (Arkadaşlar!) |

## 2.5 İzafet (îzafe): tamlama ve sıfat bağlama
İzafet, Kurmancî'nin en önemli yapısıdır. İsim tamlamalarında ve sıfatlarda **önce ana isim gelir**, izafet eki alır, sonra tamlayan gelir. Türkçe dizilişin **tersidir**.

| | Eril tekil | Dişil tekil | Çoğul |
|---|---|---|---|
| Belirli | **-ê** | **-a** | **-ên** |
| Belirsiz | **-ekî** | **-eke** | **-ine** |
| Ünlüden sonra | *-yê* | *-ya* | *-yên* |

| Kurmancî | Kelime kelime | Türkçe |
|---|---|---|
| *bavê min* | baba-ı ben | babam |
| *diya min* | anne-sı ben | annem |
| *hevalên me* | arkadaş-ları biz | arkadaşlarımız |
| *mala Resûl* | ev-i Resul | Resul'ün evi |
| *keça baş* | kız-ı iyi | iyi kız |
| *bajarekî mezin* | bir şehir-i büyük | büyük bir şehir |
| *deriyê malê* | kapı-sı ev-in | evin kapısı |

**Zincirleme izafet:** *pirtûka mamosteyê nû* = yeni öğretmenin kitabı (kitap-ı öğretmen-i yeni).

**Dikkat:** İzafet ekinin cinsiyeti ve sayısı **ana ismin**, yani ilk ismin cinsiyetine göre seçilir: *bavê keçê* (kızın babası: *bav* eril, *-ê*), *diya kurî* (oğlun annesi: *dê* dişil, *-ya*).

## 2.6 Kişi zamirleri
| Kişi | Yalın | Bükümlü | Türkçe |
|---|---|---|---|
| 1. tekil | *ez* | *min* | ben / beni, bana |
| 2. tekil | *tu* | *te* | sen / seni, sana |
| 3. tekil eril | *ew* | *wî* | o (erkek) |
| 3. tekil dişil | *ew* | *wê* | o (kadın) |
| 1. çoğul | *em* | *me* | biz |
| 2. çoğul | *hûn* | *we* | siz |
| 3. çoğul | *ew* | *wan* | onlar |

- **Yalın** şekil şimdiki ve gelecek zamanda özne olur: *Ez diçim.* (Gidiyorum.)
- **Bükümlü** şekil şu durumlarda kullanılır:
  - edatlardan sonra: *ji min re* (bana)
  - iyelikte: *mala min* (evim)
  - geçişli fiilin geçmiş zamanında özne olarak: *Min dît.* (Gördüm.)

## 2.7 İşaret zamirleri ve sıfatları
| | Yalın | Bükümlü eril | Bükümlü dişil | Bükümlü çoğul |
|---|---|---|---|---|
| bu | *ev* | *vî* | *vê* | *van* |
| şu/o | *ew* | *wî* | *wê* | *wan* |

İşaret sıfatı olarak ismin önüne gelir ve bükümlü hâlde isme ek getirir: *ev pirtûk* (bu kitap), *li vê malê* (bu evde), *ji van zarokan* (bu çocuklardan).

## 2.8 Dönüşlülük ve iyelik: *xwe*
**xwe** "kendi"dir. Özne ile iyelik sahibi aynı kişiyse kişi zamiri yerine *xwe* kullanılır:
- *Ez diçim mala **xwe**.* = Evime (kendi evime) gidiyorum. (*mala min* değil)
- *Ew pirtûka **xwe** dixwîne.* = O, kendi kitabını okuyor.
- *Ew pirtûka **wî** dixwîne.* = O, (başka bir erkeğin) kitabını okuyor.

## 2.9 Diğer zamirler
| Kurmancî | Türkçe |
|---|---|
| *kî* | kim |
| *çi* | ne |
| *kîjan* | hangisi |
| *her kes* | herkes |
| *tu kes* | hiç kimse (olumsuz fiille) |
| *tiştek* | bir şey |
| *hin* | bazı |
| *hemû* | hepsi, bütün |
| *hev* | birbiri: *Em hev dibînin.* (Birbirimizi görüyoruz.) |

## Glosslu örnekler
Gösterim ve kısaltmalar: [0.4–0.5](00-giris-ve-yontem.md#04-örneklerin-gösterimi-leipzig-glossing-kuralları).


```
(1) mal-a       min
    house-EZ.F  1SG.OBL
    'evim'
```
İzafet eki ana ismin cinsiyetini taşır (§2.5). Kaynak: BL 1970; Th 2006.

```
(2) bav-ê        min
    father-EZ.M  1SG.OBL
    'babam'
```

```
(3) heval-ên      me
    friend-EZ.PL  1PL.OBL
    'arkadaşlarımız'
```

```
(4) bajar-ek-î      mezin
    city-INDF-EZ.M  big
    'büyük bir şehir'
```
Belirsizlik eki izafetten önce gelir.

```
(5) Ez       li  mal-ê        me.
    1SG.DIR  in  house-OBL.F  COP.1SG
    'Evdeyim.'
```
Ön edattan sonra bükümlü hâl (§2.3).

```
(6) Ez       di-ç-im          mal-a       xwe.
    1SG.DIR  IPFV-go.PRS-1SG  house-EZ.F  REFL
    'Kendi evime gidiyorum.'
```
Özneyle aynı kişiye gönderme yapan iyelikte *xwe* (§2.8); hedef fiilden sonra (§6.1).

## Depodaki ilgili veri
- İsimlerin bütün çekimli biçimleri (yalın/bükümlü, belirli/belirsiz, izafet, seslenme): [`data/kmr/db/forms.tsv.gz`](../../data/kmr/db/). Örnek: *baran* için 12 biçim.
- Cinsiyet bilgisi: `lemmas.tsv`, `gender` sütunu.
