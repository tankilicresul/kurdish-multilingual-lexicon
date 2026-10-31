#!/usr/bin/env python3
"""Zazakî diyalekt ayrımı (ISO 639-3: kiu vs diq vs shared).

Bu betik data/zza/ altındaki dosyaları morfolojik ve sözcüksel kurallarla
Kuzey Zazacası (kiu / Kırmanckî - Dersim), Güney Zazacası (diq / Dımıli - Siverek/Bingöl)
ve Ortak Zazaca (shared) olarak sınıflandırır.
"""
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'data', 'zza')

# Kuzey Zazacası (kiu / Kırmanckî) belirteçleri
KIU_LEXICON = {
    'lacek', 'pêro', 'pêrune', 'roce', 'roze', 'zon', 'dizik', 'xızır', 'waştiş',
    'kerdiş', 'werdiş', 'vaciş', 'zanayiş', 'biyayiş', 'şiyayiş', 'vateniş', 'mae',
    'bray', 'waye', 'kam', 'pî', 'torn', 'zewec', 'doman', 'heskerdiş', 'moriş',
    'berbiş', 'berdeniş', 'ameliş', 'rusnayiş', 'qeseykerdiş', 'kesk'
}

# Güney Zazacası (diq / Dımıli) belirteçleri
DIQ_LEXICON = {
    'bon', 'keyey', 'laj', 'piyer', 'bav', 'qic', 'tiz', 'waştene', 'kerdene',
    'werdene', 'vatene', 'biyene', 'şiyene', 'heskerdene', 'bermayiş', 'rusnayene',
    'vatenene', 'qali', 'zewac', 'domon', 'torin', 'bıra', 'daye', 'baba', 'kormişkan'
}

def classify(word, pos='', sense=''):
    w = word.lower().strip()
    s = (sense or '').lower()

    if any(k in s for k in ['dersim', 'varto', 'erzincan', 'kuzey', 'northern', 'kirmanjki', 'kırmanckî']):
        return 'kiu'
    if any(k in s for k in ['siverek', 'bingöl', 'çolig', 'güney', 'southern', 'dimli', 'dımıli', 'diyarbakır']):
        return 'diq'

    if w in KIU_LEXICON:
        return 'kiu'
    if w in DIQ_LEXICON:
        return 'diq'

    # Kuzey morfolojisi: -iş ile biten eylemlikler (Dersim standardı)
    if w.endswith(('iş', 'yiş')) and (pos in ('verb', 'noun') or len(w) > 4):
        return 'kiu'

    # Güney/Merkez morfolojisi: -ene veya -ayene ile biten eylemlikler (Dımıli standardı)
    if w.endswith('ene') and (pos in ('verb', 'noun') or len(w) > 5):
        return 'diq'

    if w.startswith('zon') or 'zon' in w:
        return 'kiu'

    return 'shared'

def process_file(fname):
    p = os.path.join(D, fname)
    if not os.path.exists(p): return
    with open(p, encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
        cols = list(rows[0].keys())

    if 'dialect' not in cols:
        cols.insert(cols.index('review_status'), 'dialect')

    counts = {}
    for r in rows:
        dia = classify(r['kurdish'], r.get('pos', ''), r.get('sense', ''))
        r['dialect'] = dia
        counts[dia] = counts.get(dia, 0) + 1

    with open(p, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter='\t')
        w.writeheader()
        w.writerows(rows)

    print(f"{fname}: {len(rows)} satır işlendi. Dağılım: {counts}")

def main():
    for fn in ['zza-tr.tsv', 'zza-en.tsv', 'zza-de.tsv']:
        process_file(fn)

    # İstatistik ve rehber dökümanı üret
    with open(os.path.join(D, 'DIALECTS.md'), 'w', encoding='utf-8') as f:
        f.write("""# Zazakî Diyalekt Ayrımı (ISO 639-3: kiu vs diq)

Bu depoda Zazakî verisi tek bir `zza` makro kodu altına hapsedilmemiş, uluslararası dilbilim standartlarına uygun olarak diyalekt düzeyinde etiketlenmiştir.

## Diyalekt Kodları
| Kod | Ad | Konuşulduğu Bölge | Temel Özellikler |
|---|---|---|---|
| `kiu` | Kuzey Zazacası (Kırmanckî) | Dersim, Erzincan, Varto, Sivas/Koçgiri | Eylemlik eki `-iş` (`kerdiş`, `werdiş`), `zon` fonetiği, Dersim söz varlığı |
| `diq` | Güney Zazacası (Dımıli) | Siverek, Bingöl (Çolig), Diyarbakır, Çermik, Gerger | Eylemlik eki `-ene` (`kerdene`, `werdene`), `keyey/bon`, `laj` söz varlığı |
| `shared` | Ortak Zazaca | Tüm Zaza coğrafyası | Her iki kolda da ortak kullanılan temel çekirdek söz varlığı (`dest`, `aw`, `nan`, `çım`) |

Kaynak: Paul (1998), Keskin (2008), Gippert (1996).
""")
    print("Oluşturuldu: data/zza/DIALECTS.md")

if __name__ == '__main__':
    main()
