#!/usr/bin/env python3
"""
Linguistic database ("Ferheng DB") from Wiktionary.

For every Kurdish lemma: part of speech, grammatical gender, Kurdish definitions and
examples, etymology (Kurmancî text from ku.wiktionary + English text from en.wiktionary),
morpheme segmentation (e.g. "bê- + kar"), languages mentioned in the etymology,
pronunciation (IPA), hyphenation, synonyms/antonyms/derived/related words, other scripts
(Arabic, Cyrillic), best TR/EN/DE translations and Wikipedia frequency rank.
Plus: every inflected form mapped to its lemma with grammatical tags, affixes,
verb roots, proverbs, idioms and native-speaker audio recordings (Lingua Libre).

Usage: python3 scripts/build_db.py raw data
Inputs: raw/ku.jsonl.gz, raw/en-*.jsonl ; data/kmr/kmr-*.tsv ; data/frequency/*.tsv
"""
import csv, gzip, json, os, re, sys, collections, urllib.parse

RAW = sys.argv[1] if len(sys.argv) > 1 else 'raw'
D = sys.argv[2] if len(sys.argv) > 2 else 'data'
csv.field_size_limit(10**7)

VAR_OF = {'ku': 'kmr', 'ckb': 'ckb', 'zza': 'zza', 'sdh': 'sdh', 'hac': 'hac'}
EN_FILE = {'kmr': 'en-NorthernKurdish.jsonl', 'ckb': 'en-CentralKurdish.jsonl', 'zza': 'en-Zazaki.jsonl'}

# Kurmancî part-of-speech titles -> Universal Dependencies-style tags
UPOS = {'noun': 'NOUN', 'verb': 'VERB', 'adj': 'ADJ', 'adv': 'ADV', 'pron': 'PRON', 'num': 'NUM', 'prep': 'ADP',
        'postp': 'ADP', 'circumpos': 'ADP', 'conj': 'CCONJ', 'intj': 'INTJ', 'name': 'PROPN', 'article': 'DET',
        'particle': 'PART', 'prefix': 'AFFIX', 'suffix': 'AFFIX', 'infix': 'AFFIX', 'root': 'ROOT',
        'phrase': 'PHRASE', 'proverb': 'PROVERB', 'abbrev': 'ABBR', 'character': 'LETTER', 'symbol': 'SYM', 'unknown': 'X'}

# Kurmancî grammatical vocabulary in form descriptions -> tags
TERMS = [
    (r'\bnêr\b', 'masculine'), (r'\bmê\b', 'feminine'), (r'\byekjimar', 'singular'), (r'\bpir+jimar', 'plural'),
    (r'\bnebinavkirî', 'indefinite'), (r'(?<!ne)binavkirî', 'definite'), (r'çemandî', 'oblique'), (r'\bnavkî', 'direct'),
    (r'îzafeyî', 'ezafe'), (r'bangkirin|banglêker', 'vocative'),
    (r'kesê yekem', '1st-person'), (r'kesê duyem', '2nd-person'), (r'kesê sêyem', '3rd-person'),
    (r'dema niha', 'present'), (r'raboriya sade|dema borî', 'past'), (r'raboriya dûdar', 'past-perfect'),
    (r'berdest', 'progressive'), (r'dahatiya|dema bê', 'future'), (r'merciya', 'subjunctive'), (r'fermanî', 'imperative'),
    (r'neyînî', 'negative'), (r'komparatîv', 'comparative'), (r'sûperlatîv', 'superlative'),
]
TERMS = [(re.compile(p), t) for p, t in TERMS]

# Language names as they appear in Kurmancî etymologies -> ISO 639 / Wiktionary-style codes
LANG = {'erebî': 'ar', 'farisî': 'fa', 'tirkî': 'tr', 'osmanî': 'ota', 'tirkiya osmanî': 'ota', 'soranî': 'ckb',
        'zazakî': 'zza', 'hewramî': 'hac', 'goranî': 'hac', 'belûçî': 'bal', 'osetî': 'os', 'avestayî': 'ae',
        'pehlewî': 'pal', 'farisiya navîn': 'pal', 'farisiya kevn': 'peo', 'sanskrîtî': 'sa', 'ermenî': 'hy',
        'aramî': 'arc', 'siryanî': 'syc', 'suryanî': 'syc', 'yûnanî': 'el', 'yûnaniya kevn': 'grc', 'latînî': 'la',
        'fransî': 'fr', 'îngilîzî': 'en', 'almanî': 'de', 'rûsî': 'ru', 'îtalî': 'it', 'gurcî': 'ka', 'azerî': 'az',
        'proto-hindûewropî': 'ine-pro', 'proto-îranî': 'ira-pro', 'proto-hindûîranî': 'iir-pro', 'îbranî': 'he',
        'mongolî': 'mn', 'hindî': 'hi', 'akadî': 'akk', 'sumerî': 'sux', 'kurdî': 'ku', 'kurmancî': 'kmr'}
LANG_RE = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, LANG), key=len, reverse=True)) + r')\b')
ORIGIN_RE = re.compile(r'^\s*(?:ji|bi eslê xwe ji|deyn ji|deynkirî ji)\s+(.{0,40})', re.I)
MORPH_RE = re.compile(r"((?:[^\s+(),.;:\"“”]+\s*\+\s*)+[^\s+(),.;:\"“”]+)")

def wiki(lang, w): return f'https://{lang}.wiktionary.org/wiki/' + urllib.parse.quote(w.replace(' ', '_'))
def clean(s, n=None):
    s = re.sub(r'\s+', ' ', (s or '')).strip()
    return s[:n] if n else s
def first(xs): return xs[0] if xs else ''

def tags_from(desc):
    d = desc.lower()
    return [t for p, t in TERMS if p.search(d)]

def lemma_from(sense, desc):
    fo = sense.get('form_of') or sense.get('alt_of')
    if fo: return fo[0].get('word', '')
    m = re.search(r"(?:\bya|\ba|lêkera|rengdêra|ji)\s+([^\s.]+)\.?\s*$", desc.strip())
    return m.group(1) if m else ''

def etym_info(texts, links):
    text = clean(' '.join(texts))
    morph = ''
    m = MORPH_RE.search(text[:300])
    if m and len(m.group(1)) < 80: morph = re.sub(r'\s*\+\s*', ' + ', m.group(1))
    origin = ''
    om = ORIGIN_RE.search(text)
    if om:
        lm = LANG_RE.search(om.group(1).lower())
        if lm: origin = LANG[lm.group(1)]
    langs = set()
    for _, target in links or []:
        if '#' in target:
            lm = LANG_RE.search(target.split('#', 1)[1].split(':')[0].lower())
            if lm: langs.add(LANG[lm.group(1)])
    for lm in LANG_RE.finditer(text.lower()[:600]):
        langs.add(LANG[lm.group(1)])
    return text, morph, origin, sorted(langs)

# ---------- translations + frequency (from earlier build steps) ----------
best_tr = collections.defaultdict(lambda: collections.defaultdict(list))
for lang in ('tr', 'en', 'de'):
    p = os.path.join(D, 'kmr', f'kmr-{lang}.tsv')
    if not os.path.exists(p): continue
    with open(p, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['sense'] != 'gloss':
                lst = best_tr[r['kurdish']][lang]
                if len(lst) < 3 and r['translation'] not in lst: lst.append(r['translation'])
freq = {}
p = os.path.join(D, 'frequency', 'kmr-wikipedia-frequency.tsv')
if os.path.exists(p):
    with open(p, encoding='utf-8') as f:
        freq = {r['word']: int(r['rank']) for r in csv.DictReader(f, delimiter='\t')}

# ---------- English Wiktionary etymologies ----------
en_ety = collections.defaultdict(dict)   # variety -> (word,pos) -> text ; also glosses
en_gloss = collections.defaultdict(dict)
for v, fn in EN_FILE.items():
    p = os.path.join(RAW, fn)
    if not os.path.exists(p): continue
    for line in open(p, encoding='utf-8'):
        d = json.loads(line); k = (d['word'], d.get('pos', ''))
        if d.get('etymology_text'): en_ety[v][k] = clean(d['etymology_text'], 800)
        gl = [g for s in d.get('senses', []) for g in s.get('glosses', [])][:4]
        if gl: en_gloss[v][k] = gl

# ---------- main pass over Kurdish Wiktionary ----------
lemmas = collections.defaultdict(list); forms = collections.defaultdict(list)
affixes = collections.defaultdict(list); roots = collections.defaultdict(list)
proverbs = collections.defaultdict(list); audio = collections.defaultdict(list)
stats = collections.defaultdict(collections.Counter)

with gzip.open(os.path.join(RAW, 'ku.jsonl.gz'), 'rt') as f:
    for line in f:
        d = json.loads(line); v = VAR_OF.get(d.get('lang_code'))
        if not v: continue
        w, pos, pt = d['word'], d.get('pos', 'unknown'), d.get('pos_title', '')
        senses = d.get('senses') or []
        tags = d.get('tags') or []
        gender = '/'.join(t for t in ('feminine', 'masculine') if t in tags) or ('feminine-usually' if 'feminine-usually' in tags else '')
        sounds = d.get('sounds') or []
        ipa = [s['ipa'] for s in sounds if s.get('ipa')]
        hyph = ['-'.join(p for p in h.get('parts', []) if p) for h in d.get('hyphenations') or []]
        for s in sounds:
            if s.get('audio') and (s.get('ogg_url') or s.get('mp3_url')):
                audio[v].append(dict(word=w, region=' '.join(s.get('tags', []) + s.get('raw_tags', [])),
                                     ogg_url=s.get('ogg_url', ''), mp3_url=s.get('mp3_url', ''),
                                     file=s['audio'], license='see Wikimedia Commons file page (usually CC BY-SA 4.0)'))
        is_form = pt.startswith('Formeke') or 'form-of' in tags
        if is_form:
            for s in senses:
                desc = first(s.get('glosses') or [])
                lem = lemma_from(s, desc)
                forms[v].append(dict(form=w, lemma=lem, upos=UPOS.get(pos, 'X'), tags=','.join(tags_from(desc)),
                                     description_ku=clean(desc, 160)))
            stats[v]['forms'] += 1
            continue
        glosses = [clean(g, 400) for s in senses for g in (s.get('glosses') or [])]
        examples = [clean(e.get('text', ''), 300) for s in senses for e in (s.get('examples') or [])][:5]
        ety_text, morph, origin, langs = etym_info(d.get('etymology_texts') or [], d.get('etymology_links'))
        scripts = {}
        for fm in d.get('forms') or []:
            for t in fm.get('tags') or []:
                if t in ('Kurdish-Arabic', 'Kurdish-Cyrillic', 'Arabic', 'Cyrillic', 'Latin'):
                    scripts.setdefault(t.replace('Kurdish-', '').lower(), fm['form'])
        variants = [fm['form'] for fm in d.get('forms') or [] if not fm.get('tags')][:6]
        rec = dict(word=w, variety=v, upos=UPOS.get(pos, 'X'), pos=pos, pos_ku=pt, gender=gender,
                   glosses_ku=glosses[:8], examples=examples,
                   glosses_en=en_gloss[v].get((w, pos), []),
                   etymology_ku=clean(ety_text, 1200), etymology_en=en_ety[v].get((w, pos), ''),
                   morphemes=morph, origin=origin, etymology_mentions=langs,
                   ipa=ipa[:3], hyphenation=hyph[:1], scripts=scripts, variants=variants,
                   synonyms=[x['word'] for x in d.get('synonyms') or []][:10],
                   antonyms=[x['word'] for x in d.get('antonyms') or []][:10],
                   derived=[x['word'] for x in d.get('derived') or []][:20],
                   related=[x['word'] for x in d.get('related') or [] if len(x['word']) > 1][:10],
                   translations={l: best_tr[w][l] for l in ('tr', 'en', 'de') if best_tr[w][l]} if v == 'kmr' else {},
                   freq_rank=freq.get(w.lower()) if v == 'kmr' else None,
                   source_url=wiki('ku', w), review_status='unverified')
        if pos == 'root':
            roots[v].append(rec)
        elif pos in ('prefix', 'suffix', 'infix') or 'morpheme' in tags:
            affixes[v].append(rec)
        elif pos in ('proverb', 'phrase'):
            proverbs[v].append(rec)
        else:
            lemmas[v].append(rec)
        stats[v][rec['upos']] += 1
        if rec['etymology_ku'] or rec['etymology_en']: stats[v]['_with_etymology'] += 1
        if morph: stats[v]['_with_morphemes'] += 1
        if ipa: stats[v]['_with_ipa'] += 1

# Varieties that only exist in en.wiktionary for some words: add en-only lemmas
for v, fn in EN_FILE.items():
    have = {(r['word'], r['pos']) for r in lemmas[v]}
    p = os.path.join(RAW, fn)
    if not os.path.exists(p): continue
    for line in open(p, encoding='utf-8'):
        d = json.loads(line); k = (d['word'], d.get('pos', ''))
        if k in have or any('form_of' in s for s in d.get('senses', [])): continue
        ety = clean(d.get('etymology_text', ''), 800)
        _, morph, origin, langs = etym_info([ety], d.get('etymology_links'))
        lemmas[v].append(dict(word=d['word'], variety=v, upos=UPOS.get(d.get('pos'), 'X'), pos=d.get('pos'), pos_ku='',
            gender='', glosses_ku=[], examples=[], glosses_en=en_gloss[v].get(k, []), etymology_ku='', etymology_en=ety,
            morphemes=morph, origin=origin, etymology_mentions=langs,
            ipa=[s['ipa'] for s in d.get('sounds', []) if s.get('ipa')][:3], hyphenation=[], scripts={}, variants=[],
            synonyms=[], antonyms=[], derived=[], related=[], translations={}, freq_rank=None,
            source_url=wiki('en', d['word']), review_status='unverified'))
        stats[v][UPOS.get(d.get('pos'), 'X')] += 1

# ---------- write ----------
FLAT = ['word', 'upos', 'pos_ku', 'gender', 'gloss_ku', 'gloss_en', 'tr', 'en', 'de', 'morphemes', 'origin',
        'etymology_mentions', 'ipa', 'hyphenation', 'arabic_script', 'freq_rank', 'review_status']
def flat(r):
    t = r.get('translations') or {}
    return dict(word=r['word'], upos=r['upos'], pos_ku=r['pos_ku'], gender=r['gender'],
                gloss_ku=clean(first(r['glosses_ku']), 200), gloss_en=clean(first(r['glosses_en']), 200),
                tr=' | '.join(t.get('tr', [])), en=' | '.join(t.get('en', [])), de=' | '.join(t.get('de', [])),
                morphemes=r['morphemes'], origin=r['origin'], etymology_mentions=','.join(r['etymology_mentions']),
                ipa=first(r['ipa']), hyphenation=first(r['hyphenation']), arabic_script=r['scripts'].get('arabic', ''),
                freq_rank=r['freq_rank'] or '', review_status='unverified')

def write_tsv(path, rows, cols):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'wt', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter='\t', extrasaction='ignore'); w.writeheader(); w.writerows(rows)

summary = {}
for v in ('kmr', 'ckb', 'zza', 'sdh', 'hac'):
    out = os.path.join(D, v, 'db')
    L = sorted(lemmas[v], key=lambda r: (r['freq_rank'] or 10**9, r['word'].lower()))
    if not L and not forms[v]: continue
    os.makedirs(out, exist_ok=True)
    with gzip.open(os.path.join(out, 'lemmas.jsonl.gz'), 'wt', encoding='utf-8') as f:
        for r in L: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    write_tsv(os.path.join(out, 'lemmas.tsv'), [flat(r) for r in L], FLAT)
    if forms[v]:
        write_tsv(os.path.join(out, 'forms.tsv.gz'), sorted(forms[v], key=lambda r: (r['lemma'], r['form'])),
                  ['form', 'lemma', 'upos', 'tags', 'description_ku'])
    for name, rows in (('affixes', affixes[v]), ('verb-roots', roots[v]), ('proverbs-idioms', proverbs[v])):
        if rows:
            write_tsv(os.path.join(out, f'{name}.tsv'),
                      [dict(flat(r), type=r['pos'], examples=' | '.join(r['examples'][:3]),
                            etymology_ku=clean(r['etymology_ku'], 300)) for r in sorted(rows, key=lambda r: r['word'])],
                      ['word', 'type', 'pos_ku', 'gloss_ku', 'gloss_en', 'examples', 'morphemes', 'etymology_ku', 'review_status'])
    ety = [dict(word=r['word'], upos=r['upos'], morphemes=r['morphemes'], origin=r['origin'],
                etymology_mentions=','.join(r['etymology_mentions']), etymology_ku=clean(r['etymology_ku'], 600),
                etymology_en=clean(r['etymology_en'], 600), source_url=r['source_url'], review_status='unverified')
           for r in L if r['etymology_ku'] or r['etymology_en']]
    if ety: write_tsv(os.path.join(out, 'etymology.tsv'), ety, list(ety[0].keys()))
    if audio[v]:
        seen = set(); au = []
        for a in audio[v]:
            if a['file'] not in seen: seen.add(a['file']); au.append(a)
        write_tsv(os.path.join(out, 'audio.tsv'), sorted(au, key=lambda a: a['word']), ['word', 'region', 'ogg_url', 'mp3_url', 'file', 'license'])
    s = stats[v]
    summary[v] = dict(lemmas=len(L), forms=len(forms[v]), affixes=len(affixes[v]), verb_roots=len(roots[v]),
                      proverbs_idioms=len(proverbs[v]), with_etymology=len(ety), with_morphemes=s['_with_morphemes'],
                      with_ipa=s['_with_ipa'], audio_files=len({a['file'] for a in audio[v]}),
                      by_upos={k: c for k, c in s.most_common() if not k.startswith('_') and k != 'forms'})
with open(os.path.join(D, 'DB-STATS.json'), 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
