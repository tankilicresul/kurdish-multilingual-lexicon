#!/usr/bin/env python3
"""
Kurdish multilingual lexicon builder.

Reads Wiktextract dumps published by kaikki.org (data from Wiktionary,
CC BY-SA 4.0 / GFDL) and writes Kurdish <-> English / German / Turkish word
pairs for four Kurdish varieties (plus Gorani/Hewrami where available).

Inputs (download into ./raw first, see README "Rebuild"):
  raw/ku.jsonl.gz                 Kurdish Wiktionary (Wîkîferheng) extract
  raw/tr.jsonl.gz                 Turkish Wiktionary (Vikisözlük) extract
  raw/de-kurdish.jsonl            German Wiktionary extract, pre-filtered to Kurdish
  raw/en-NorthernKurdish.jsonl    English Wiktionary, Northern Kurdish entries
  raw/en-CentralKurdish.jsonl     English Wiktionary, Central Kurdish entries
  raw/en-Zazaki.jsonl             English Wiktionary, Zazaki entries

Output: data/<variety>/<variety>-<en|de|tr>.tsv, data/cross-dialect.tsv,
        data/lexicon.jsonl, data/STATS.md
Every row keeps its source and review_status=unverified.
"""
import csv, gzip, json, os, re, sys, collections, urllib.parse

RAW = sys.argv[1] if len(sys.argv) > 1 else 'raw'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'data'

# Variety codes used in this repo (ISO 639-3)
VAR = {'kmr': 'Kurmancî (Northern Kurdish)', 'ckb': 'Soranî (Central Kurdish)',
       'sdh': 'Southern Kurdish (Kurdiya başûrî)', 'zza': 'Zazakî / Kirmanckî', 'hac': 'Goranî / Hewramî'}
# Source code -> repo code
MAP = {'ku': 'kmr', 'kmr': 'kmr', 'ckb': 'ckb', 'sdh': 'sdh', 'zza': 'zza', 'diq': 'zza', 'kiu': 'zza', 'hac': 'hac'}
TARGETS = ('en', 'de', 'tr')
ARABIC = re.compile(r'[؀-ۿ]')
BAD = re.compile(r'[\[\]{}<>|=#]|https?:')
# grammatical-form explanations are not translations
FORM = re.compile(r'çekimi|sözcüğünün|form of|plural of|Form von|Plural von|rewşa |formeke ', re.I)

# Kurdish-language definitions that are not words ("a boy's name", "a surname", ...)
NOTWORD = re.compile(r'\b(Nav[eê]k[îi]?|Paşnav|Navê|Nav[eê]\s)|\s(e|ye)$|,')
def is_word(w): return ok_word(w) and not NOTWORD.search(w)

def script_of(w): return 'arab' if ARABIC.search(w) else 'latn'
def norm(s):
    s = re.sub(r'\s+', ' ', (s or '').strip()).strip(' ,;:.')
    return s
def ok_word(w, maxw=4):
    return w and not BAD.search(w) and len(w) <= 60 and len(w.split()) <= maxw
def short_gloss(g, maxw=6):
    g = re.sub(r'\([^)]*\)', '', g or '')
    g = norm(g.split(';')[0])
    if FORM.search(g): return ''
    return g if ok_word(g, maxw) else ''
def wiki(lang, word): return f'https://{lang}.wiktionary.org/wiki/' + urllib.parse.quote(word.replace(' ', '_'))
def var_of(code, word):
    v = MAP.get(code)
    if code == 'ku' and script_of(word) == 'arab':
        v = 'ckb'   # generic "Kurdish" written in Arabic script is almost always Sorani
    return v

rows = []      # dicts
cross = []     # kmr <-> other varieties

def add(var, ku, pos, tgt_lang, tgt, note, src, url):
    ku, tgt = norm(ku), norm(tgt)
    if not (var in VAR and tgt_lang in TARGETS and is_word(ku) and ok_word(tgt, 6)):
        return
    rows.append(dict(kurdish=ku, variety=var, script=script_of(ku), pos=pos or '', lang=tgt_lang,
                     translation=tgt, sense=norm(note)[:120], source=src, source_url=url,
                     review_status='unverified'))

def senses(d):
    for s in d.get('senses', []) or []:
        for g in s.get('glosses', []) or []:
            yield g

# 1) Kurdish Wiktionary: Kurmancî entries -> translation tables; other entries -> Kurmancî glosses
with gzip.open(os.path.join(RAW, 'ku.jsonl.gz'), 'rt') as f:
    for line in f:
        d = json.loads(line); lc = d.get('lang_code'); w = d.get('word', ''); pos = d.get('pos', '')
        if lc == 'ku':
            for t in d.get('translations', []) or []:
                tl, tw = t.get('lang_code'), t.get('word', '')
                if tl in TARGETS:
                    add('kmr', w, pos, tl, tw, t.get('sense', ''), 'ku.wiktionary', wiki('ku', w))
                elif tl in MAP and MAP[tl] != 'kmr' and ok_word(tw):
                    cross.append(dict(kmr=norm(w), variety=MAP[tl], word=norm(tw), script=script_of(tw),
                                      source='ku.wiktionary', source_url=wiki('ku', w), review_status='unverified'))
        elif lc in TARGETS:   # foreign word explained in Kurmancî
            for g in senses(d):
                k = short_gloss(g, 3)
                if k: add('kmr', k, pos, lc, w, 'gloss', 'ku.wiktionary', wiki('ku', w))
        elif lc in MAP and MAP[lc] != 'kmr':  # Sorani/Zazaki/... word explained in Kurmancî
            for g in senses(d):
                k = short_gloss(g, 3)
                if k and ok_word(w):
                    cross.append(dict(kmr=k, variety=MAP[lc], word=norm(w), script=script_of(w),
                                      source='ku.wiktionary', source_url=wiki('ku', w), review_status='unverified'))

# 2) English Wiktionary: Kurdish entries with English glosses
for fn, var in (('en-NorthernKurdish.jsonl', 'kmr'), ('en-CentralKurdish.jsonl', 'ckb'), ('en-Zazaki.jsonl', 'zza')):
    p = os.path.join(RAW, fn)
    if not os.path.exists(p): continue
    for line in open(p, encoding='utf-8'):
        d = json.loads(line); w = d.get('word', '')
        for g in senses(d):
            e = short_gloss(g, 6)
            if e: add(var, w, d.get('pos'), 'en', e, '', 'en.wiktionary', wiki('en', w))

# 3) Turkish Wiktionary
with gzip.open(os.path.join(RAW, 'tr.jsonl.gz'), 'rt') as f:
    for line in f:
        if '"ku' not in line and '"kmr"' not in line and '"zza"' not in line and '"ckb"' not in line: continue
        d = json.loads(line); lc = d.get('lang_code'); w = d.get('word', '')
        if lc in MAP:   # Kurdish word with Turkish glosses
            v = var_of(lc, w)
            for g in senses(d):
                t = short_gloss(g, 6)
                if t: add(v, w, d.get('pos'), 'tr', t, '', 'tr.wiktionary', wiki('tr', w))
        elif lc == 'tr':
            for t in d.get('translations', []) or []:
                tl, tw = t.get('lang_code'), t.get('word', '')
                if tl in MAP:
                    add(var_of(tl, tw), tw, d.get('pos'), 'tr', w, t.get('sense', ''), 'tr.wiktionary', wiki('tr', w))

# 4) German Wiktionary (pre-filtered)
p = os.path.join(RAW, 'de-kurdish.jsonl')
if os.path.exists(p):
    for line in open(p, encoding='utf-8'):
        d = json.loads(line); lc = d.get('lang_code'); w = d.get('word', '')
        if lc == 'de':
            for t in d.get('translations', []) or []:
                tl, tw = t.get('lang_code'), t.get('word', '')
                if tl in MAP:
                    add(var_of(tl, tw), tw, d.get('pos'), 'de', w, t.get('sense', ''), 'de.wiktionary', wiki('de', w))
        elif lc in MAP:
            v = var_of(lc, w)
            for s in d.get('senses', []) or []:
                for g in s.get('glosses') or []:
                    t = short_gloss(g, 6)
                    if t: add(v, w, d.get('pos'), 'de', t, '', 'de.wiktionary', wiki('de', w))

# ---- de-duplicate, merge sources ----
merged = collections.OrderedDict()
for r in rows:
    k = (r['variety'], r['kurdish'].lower(), r['lang'], r['translation'].lower())
    if k in merged:
        m = merged[k]
        if r['source'] not in m['source'].split('+'):
            m['source'] += '+' + r['source']; m['source_url'] += ' ' + r['source_url']
        if not m['pos'] and r['pos']: m['pos'] = r['pos']
    else:
        merged[k] = dict(r)
rows = list(merged.values())
for r in rows:   # agreement of independent sources is the first confidence signal
    r['sources_agree'] = len(r['source'].split('+'))

xs = collections.OrderedDict()
for c in cross:
    k = (c['kmr'].lower(), c['variety'], c['word'].lower())
    xs.setdefault(k, c)
cross = [c for c in xs.values() if is_word(c['kmr']) and is_word(c['word'])]

# ---- write ----
cols = ['kurdish', 'variety', 'script', 'pos', 'lang', 'translation', 'sense', 'sources_agree', 'source', 'source_url', 'review_status']
stats = collections.Counter()
by = collections.defaultdict(list)
for r in rows: by[(r['variety'], r['lang'])].append(r)
for (v, l), rs in sorted(by.items()):
    rs.sort(key=lambda r: (-r['sources_agree'], r['kurdish'].lower()))
    os.makedirs(os.path.join(OUT, v), exist_ok=True)
    with open(os.path.join(OUT, v, f'{v}-{l}.tsv'), 'w', encoding='utf-8', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=cols, delimiter='\t', extrasaction='ignore'); wr.writeheader(); wr.writerows(rs)
    stats[(v, l)] = len(rs)
with open(os.path.join(OUT, 'cross-dialect.tsv'), 'w', encoding='utf-8', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=['kmr', 'variety', 'word', 'script', 'source', 'source_url', 'review_status'], delimiter='\t')
    wr.writeheader(); wr.writerows(sorted(cross, key=lambda c: (c['variety'], c['kmr'].lower())))
with gzip.open(os.path.join(OUT, 'lexicon.jsonl.gz'), 'wt', encoding='utf-8') as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')

# ---- pivot: other varieties -> EN/DE/TR through Kurmancî (only Kurmancî pairs confirmed by 2+ sources) ----
strong = collections.defaultdict(list)
for r in rows:
    if r['variety'] == 'kmr' and r['sources_agree'] > 1:
        strong[r['kurdish'].lower()].append(r)
pivot = collections.Counter()
for v in VAR:
    if v == 'kmr': continue
    out = collections.defaultdict(dict)
    for c in cross:
        if c['variety'] != v: continue
        for r in strong.get(c['kmr'].lower(), []):
            k = (c['word'].lower(), r['translation'].lower())
            out[r['lang']].setdefault(k, dict(kurdish=c['word'], variety=v, script=c['script'], via_kmr=c['kmr'],
                lang=r['lang'], translation=r['translation'], source='pivot:' + c['source'] + '>' + r['source'],
                review_status='unverified'))
    for l, d in out.items():
        os.makedirs(os.path.join(OUT, 'experimental', 'pivots'), exist_ok=True)
        with open(os.path.join(OUT, 'experimental', 'pivots', f'{v}-{l}.pivot.tsv'), 'w', encoding='utf-8', newline='') as f:
            wr = csv.DictWriter(f, fieldnames=['kurdish', 'variety', 'script', 'via_kmr', 'lang', 'translation', 'source', 'review_status'], delimiter='\t')
            wr.writeheader(); wr.writerows(sorted(d.values(), key=lambda x: x['kurdish'].lower()))
        pivot[(v, l)] = len(d)

xc = collections.Counter(c['variety'] for c in cross)
agree = collections.Counter((r['variety'], r['lang']) for r in rows if r['sources_agree'] > 1)
with open(os.path.join(OUT, 'STATS.md'), 'w', encoding='utf-8') as f:
    f.write('# Statistics / İstatistik\n\nGenerated by `scripts/build.py`. All rows: `review_status = unverified`.\n\n')
    f.write('| Variety | EN | DE | TR | Pairs confirmed by 2+ sources |\n|---|---:|---:|---:|---:|\n')
    for v in VAR:
        f.write(f"| {VAR[v]} (`{v}`) | {stats[(v,'en')]} | {stats[(v,'de')]} | {stats[(v,'tr')]} | {sum(agree[(v,l)] for l in TARGETS)} |\n")
    f.write('\n## Pivot files (via Kurmancî, lower confidence) / Kurmancî üzerinden türetilmiş\n\n| Variety | EN | DE | TR |\n|---|---:|---:|---:|\n')
    for v in VAR:
        if v != 'kmr': f.write(f"| {VAR[v]} (`{v}`) | {pivot[(v,'en')]} | {pivot[(v,'de')]} | {pivot[(v,'tr')]} |\n")
    f.write('\n## Cross-dialect (Kurmancî ↔ other varieties)\n\n| Variety | Pairs |\n|---|---:|\n')
    for v in VAR:
        if v != 'kmr': f.write(f'| {VAR[v]} (`{v}`) | {xc[v]} |\n')
print(dict(stats)); print('cross', dict(xc)); print('total', len(rows)); print('pivot', dict(pivot))
