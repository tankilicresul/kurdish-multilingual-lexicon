#!/usr/bin/env python3
"""
Derived, developer-friendly tables built from data/ (run after build.py, core.py, frequency.py):

  data/multilingual/kmr-tr-en-de.tsv   one row per Kurmancî headword: best TR / EN / DE
                                       translations + Soranî / Zazakî / Southern Kurdish / Goranî
                                       equivalents + Wikipedia frequency rank
  data/learner/kmr-top3000.tsv         the 3,000 most frequent Kurmancî words that have a translation
  data/themes/*.tsv, themes.json       thematic word lists (colors, animals, food ...) in
                                       Kurmancî, Soranî, Zazakî, Southern Kurdish + TR/EN/DE

Nothing here is invented: every Kurdish form is taken from data/ and keeps review_status=unverified.
"""
import csv, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from themes_seed import THEMES

D = sys.argv[1] if len(sys.argv) > 1 else 'data'
csv.field_size_limit(10**7)

def read(p):
    with open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def low(s): return s.replace('I', 'i').replace('Î', 'î').lower().strip()

# ---------- load ----------
tr = collections.defaultdict(list)          # (kmr, lang) -> [(translation, agree, from_gloss)]
gloss_n = collections.Counter()
pos_of = {}
rev = collections.defaultdict(lambda: collections.defaultdict(list))   # lang -> target(lower) -> [(kmr, agree)]
for lang in ('tr', 'en', 'de'):
    for r in read(os.path.join(D, 'kmr', f'kmr-{lang}.tsv')):
        k = r['kurdish']; a = int(r['sources_agree'])
        g = r['sense'] == 'gloss' and a == 1          # derived from a foreign word's Kurmancî gloss
        if g: gloss_n[(k, lang)] += 1
        native = f'{lang}.wiktionary' in r['source']   # the target-language dictionary describes the Kurdish word
        tr[(k, lang)].append((r['translation'], a, g, native))
        pos_of.setdefault(k, r['pos'])
        rev[lang][low(r['translation'])].append((k, a))

freq = {}
for v in ('kmr', 'ckb', 'zza'):
    p = os.path.join(D, 'frequency', f'{v}-wikipedia-frequency.tsv')
    freq[v] = {r['word']: int(r['rank']) for r in read(p)} if os.path.exists(p) else {}

cross = collections.defaultdict(lambda: collections.defaultdict(list))  # kmr -> variety -> [word]
for r in read(os.path.join(D, 'cross-dialect.tsv')):
    lst = cross[low(r['kmr'])][r['variety']]
    if r['word'] not in lst: lst.append(r['word'])

direct = collections.defaultdict(lambda: collections.defaultdict(list))   # variety -> en(lower) -> [word]
for v in ('ckb', 'zza'):
    p = os.path.join(D, v, f'{v}-en.tsv')
    if os.path.exists(p):
        for r in read(p):
            direct[v][low(r['translation'])].append(r['kurdish'])

def best(k, lang, n=3):
    xs = tr.get((k, lang), [])
    if gloss_n[(k, lang)] > 8:     # particles/prepositions glossed by hundreds of foreign entries
        xs = [x for x in xs if not x[2]]
    if len({x[0] for x in xs}) > 15 and not any(x[1] > 1 for x in xs):   # noisy particle: trust only native entries
        xs = [x for x in xs if x[3]]
    xs = sorted(xs, key=lambda x: (-x[1], not x[3], x[2]))
    out = []
    for t, a, g, nat in xs:
        if t not in out: out.append(t)
    return out[:n]

def rank(k): return freq['kmr'].get(low(k), 999999)

# ---------- 1) multilingual table ----------
heads = sorted({k for (k, _) in tr}, key=lambda k: (rank(k), low(k)))
os.makedirs(os.path.join(D, 'multilingual'), exist_ok=True)
cols = ['kmr', 'pos', 'freq_rank', 'tr', 'en', 'de', 'ckb', 'zza', 'sdh', 'hac', 'confidence', 'review_status']
n_multi = 0
with open(os.path.join(D, 'multilingual', 'kmr-tr-en-de.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter='\t'); w.writeheader()
    for k in heads:
        langs = {l: best(k, l) for l in ('tr', 'en', 'de')}
        have = sum(1 for l in langs if langs[l])
        r = rank(k)
        if have < 2 and r > 50000: continue
        strong = sum(1 for l in ('tr', 'en', 'de') if any(x[1] > 1 for x in tr.get((k, l), [])))
        conf = 'high' if strong >= 2 else 'medium' if strong == 1 or have == 3 else 'low'
        c = cross.get(low(k), {})
        w.writerow(dict(kmr=k, pos=pos_of.get(k, ''), freq_rank='' if r == 999999 else r,
                        tr=' | '.join(langs['tr']), en=' | '.join(langs['en']), de=' | '.join(langs['de']),
                        ckb=' | '.join(c.get('ckb', [])[:3]), zza=' | '.join(c.get('zza', [])[:3]),
                        sdh=' | '.join(c.get('sdh', [])[:3]), hac=' | '.join(c.get('hac', [])[:3]),
                        confidence=conf, review_status='unverified'))
        n_multi += 1

# ---------- 2) learner list ----------
os.makedirs(os.path.join(D, 'learner'), exist_ok=True)
by_low = collections.defaultdict(list)
for k in heads: by_low[low(k)].append(k)
n_learn = 0
with open(os.path.join(D, 'learner', 'kmr-top3000.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t'); w.writerow(['rank', 'kmr', 'pos', 'tr', 'en', 'de', 'note', 'review_status'])
    for word, r in sorted(freq['kmr'].items(), key=lambda x: x[1]):
        ks = by_low.get(word)
        if not ks: continue
        k = ks[0]
        t, e, d = best(k, 'tr', 2), best(k, 'en', 2), best(k, 'de', 2)
        if not (t or e): continue
        n_learn += 1
        note = 'işlev sözcüğü / function word: çeviriler bağlama göre değişir, güvenilir değil' if pos_of.get(k, '') in ('prep', 'postp', 'conj', 'particle', 'circumpos') else ''
        w.writerow([n_learn, k, pos_of.get(k, ''), ' | '.join(t), ' | '.join(e), ' | '.join(d), note, 'unverified'])
        if n_learn >= 3000: break

# ---------- 3) themes ----------
os.makedirs(os.path.join(D, 'themes'), exist_ok=True)
allthemes = {}
miss = 0
for theme, items in THEMES.items():
    slug = theme.split('/')[0]
    rows = []
    for en, trl, de in items:
        cands = collections.Counter()
        keys = [low(en)] + ([low(en)[3:]] if low(en).startswith('to ') else [])
        for k, a in [x for kk in keys for x in rev['en'].get(kk, [])]:
            score = a * 10
            if low(trl) in [low(x[0]) for x in tr.get((k, 'tr'), [])]: score += 25   # Turkish agrees
            if low(de) in [low(x[0]) for x in tr.get((k, 'de'), [])]: score += 15    # German agrees
            if ' ' not in k: score += 3
            score += max(0, 10 - rank(k) / 2000)                                      # common words first
            cands[k] = max(cands[k], score)
        ranked = [k for k, _ in cands.most_common()]
        kmr = ranked[0] if ranked else ''
        if not kmr: miss += 1
        c = cross.get(low(kmr), {}) if kmr else {}
        ckb = c.get('ckb', [])[:2] or [x for kk in keys for x in direct['ckb'].get(kk, [])][:2]
        zza = c.get('zza', [])[:2] or [x for kk in keys for x in direct['zza'].get(kk, [])][:2]
        sdh = c.get('sdh', [])[:2]
        top = cands.most_common(1)[0][1] if cands else 0
        conf = 'high' if top >= 45 else 'medium' if top >= 25 else 'low' if kmr else 'missing'
        rows.append(dict(en=en, tr=trl, de=de, kmr=kmr, kmr_alternatives=' | '.join(ranked[1:4]),
                         ckb=' | '.join(ckb), zza=' | '.join(zza), sdh=' | '.join(sdh),
                         confidence=conf, review_status='unverified'))
    with open(os.path.join(D, 'themes', f'{slug}.tsv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter='\t'); w.writeheader(); w.writerows(rows)
    allthemes[theme] = rows
with open(os.path.join(D, 'themes', 'themes.json'), 'w', encoding='utf-8') as f:
    json.dump({'note': 'Automatically derived from Wiktionary data. review_status=unverified. TR/DE labels are concept labels, not translations of the Kurdish word.',
               'license': 'CC BY-SA 4.0', 'themes': allthemes}, f, ensure_ascii=False, indent=1)
# ---------- 4) word-game lists (Wordle-style): lemma-like words of length 3-7, ranked by frequency ----------
ALPHA = set('abcçdeêfghiîjklmnopqrsştuûvwxyz')
os.makedirs(os.path.join(D, 'games'), exist_ok=True)
nouns = {low(k) for k in heads if pos_of.get(k) in ('noun', 'adj', 'verb', 'adv', 'num')}
games = collections.Counter()
for L in range(3, 8):
    with open(os.path.join(D, 'games', f'kmr-{L}-harf.tsv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t'); w.writerow(['word', 'pos', 'freq_rank', 'tr', 'en', 'de', 'review_status'])
        for word, r in sorted(freq['kmr'].items(), key=lambda x: x[1]):
            if len(word) != L or not set(word) <= ALPHA or word not in nouns: continue
            k = by_low[word][0]
            t = best(k, 'tr', 2)
            e = best(k, 'en', 3)
            if not t or any(re.search(r'person|singular|plural|past |present |imperative|form of|participle', x) for x in e): continue
            w.writerow([word, pos_of.get(k, ''), r, ' | '.join(t), ' | '.join(best(k, 'en', 2)), ' | '.join(best(k, 'de', 2)), 'unverified'])
            games[L] += 1

print('games', dict(games))
print('multilingual', n_multi, 'learner', n_learn, 'themes', sum(len(v) for v in allthemes.values()), 'missing', miss)
