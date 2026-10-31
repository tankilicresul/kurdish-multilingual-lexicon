# Veriyi Yeniden Üretme / Rebuild

Tüm `data/` klasörü açık dökümlerden betiklerle üretilir. Gerekenler: Python 3.9+, Node 18+ (yalnızca JS testleri için), ~1 GB boş disk.

```bash
mkdir -p raw && cd raw

# 1) Vikisözlük (Wiktextract / kaikki.org)
curl -o ku.jsonl.gz https://kaikki.org/dictionary/downloads/ku/ku-extract.jsonl.gz
curl -o tr.jsonl.gz https://kaikki.org/dictionary/downloads/tr/tr-extract.jsonl.gz
curl -o en-NorthernKurdish.jsonl "https://kaikki.org/dictionary/Northern%20Kurdish/kaikki.org-dictionary-NorthernKurdish.jsonl"
curl -o en-CentralKurdish.jsonl  "https://kaikki.org/dictionary/Central%20Kurdish/kaikki.org-dictionary-CentralKurdish.jsonl"
curl -o en-Zazaki.jsonl          "https://kaikki.org/dictionary/Zazaki/kaikki.org-dictionary-Zazaki.jsonl"
curl -s https://kaikki.org/dictionary/downloads/de/de-extract.jsonl.gz | python3 ../scripts/filter_de.py > de-kurdish.jsonl   # ~300 MB akış

# 2) Vikipedi (sıklık listeleri)
curl -o kuwiki.xml.bz2  https://dumps.wikimedia.org/kuwiki/latest/kuwiki-latest-pages-articles.xml.bz2
curl -o ckbwiki.xml.bz2 https://dumps.wikimedia.org/ckbwiki/latest/ckbwiki-latest-pages-articles.xml.bz2
curl -o diqwiki.xml.bz2 https://dumps.wikimedia.org/diqwiki/latest/diqwiki-latest-pages-articles.xml.bz2
cd ..

# 3) Üretim
python3 scripts/build.py raw data            # çiftler, lehçeler arası, pivot, STATS.md
python3 scripts/core.py data                 # çekirdek (2+ kaynak)
python3 scripts/frequency.py raw/kuwiki.xml.bz2  kmr data/frequency
python3 scripts/frequency.py raw/ckbwiki.xml.bz2 ckb data/frequency
python3 scripts/frequency.py raw/diqwiki.xml.bz2 zza data/frequency
python3 scripts/derive.py data               # multilingual, learner, themes, games
python3 scripts/build_db.py raw data         # dilbilimsel veritabanı (data/*/db/)

# 4) Kontrol
python3 scripts/validate.py data
python3 -m unittest tools/tests/test_kurdi.py
node tools/tests/test_kurdi.mjs
```

**İlk derlemede kullanılan dökümler:** kaikki.org verisi 31 Ekim 2026'da indirildi; Vikipedi dökümleri 1 Ekim 2026 tarihli (`latest`). Dökümler güncellendikçe sayılar değişir.

**Önemli:** İnsan kontrolüyle düzeltilmiş satırlar (`review_status ≠ unverified`) yeniden üretimde kaybolmamalıdır. Kontrol başladığında düzeltmeler ayrı bir dosyada (`data/reviews/`) tutulacak ve üretimden sonra üzerine uygulanacaktır (yapılacak).
