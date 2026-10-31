#!/usr/bin/env python3
"""
Etymological classification of Kurmancî lemmas ("is this word inherited, borrowed or built inside Kurdish?").

Classes
  inherited          kalıt / miras: comes down from Proto-Iranian (and earlier) through Kurdish's own history
  borrowed           alıntı: taken from a non-Iranian language (Arabic, Turkish, French, Armenian, Aramaic ...)
  borrowed-iranian   akraba dilden alıntı: taken from another Iranian language (Persian, Sorani ...)
  internal           Kürtçe içi türetme / bileşik: built in Kurdish from Kurdish parts (bê- + kar)
  onomatopoeic       yansıma
  unknown            no usable etymology

A loanword is still a Kurdish word. "borrowed" says where a word came from, not whether it belongs to Kurdish.

Evidence, in this order:
  1. etymology tree in ku.wiktionary ("Dara etîmolojiyê": language chain, 'deyn.' = borrowed, 'drş.' = derived)
  2. etymology templates in en.wiktionary (inh / bor / der / af)
  3. phrases in the Kurmancî etymology text ("Deyn ji erebî", "ji zimanên îranî", "bê- + kar", "onomatopoetîk")
Usage regions come from regional labels on senses/synonyms and from the home region of Lingua Libre speakers.

Usage: python3 scripts/etymology_classify.py raw data
"""
import csv, gzip, json, os, re, sys, collections

RAW = sys.argv[1] if len(sys.argv) > 1 else 'raw'
D = sys.argv[2] if len(sys.argv) > 2 else 'data'

NAMES = {  # Kurmancî language names -> code
 'kurmancî': 'kmr', 'kurdî': 'ku', 'soranî': 'ckb', 'zazakî': 'zza', 'hewramî': 'hac', 'goranî': 'hac', 'farisî': 'fa',
 'farisiya navîn': 'pal', 'pehlewî': 'pal', 'farisiya kevn': 'peo', 'hexamenişî': 'peo', 'avestayî': 'ae', 'partî': 'xpr',
 'medî': 'xme', 'proto-îranî': 'ira-pro', 'proto-hindûîranî': 'iir-pro', 'proto-hindûewropî': 'ine-pro', 'belûçî': 'bal',
 'osetî': 'os', 'peştûyî': 'ps', 'sanskrîtî': 'sa', 'erebî': 'ar', 'aramî': 'arc', 'suryanî': 'syc', 'siryanî': 'syc',
 'îbranî': 'he', 'akadî': 'akk', 'sumerî': 'sux', 'proto-samî': 'sem-pro', 'proto-samiya rojavayî': 'sem-wes-pro',
 'tirkî': 'tr', 'tirkiya osmanî': 'ota', 'osmanî': 'ota', 'azerî': 'az', 'proto-tirkî': 'trk-pro', 'çaxatayî': 'chg',
 'tirkmenî': 'tk', 'mongolî': 'mn', 'ermenî': 'hy', 'ermeniya kevn': 'xcl', 'gurcî': 'ka', 'yûnanî': 'el',
 'yûnaniya kevn': 'grc', 'yûnaniya bîzansî': 'gkm', 'latînî': 'la', 'fransî': 'fr', 'îngilîzî': 'en', 'almanî': 'de',
 'rûsî': 'ru', 'îtalî': 'it', 'spanî': 'es', 'portugalî': 'pt', 'hindî': 'hi', 'urdûyî': 'ur', 'çînî': 'zh'}
NAME_RE = re.compile(r'^(' + '|'.join(sorted(map(re.escape, NAMES), key=len, reverse=True)) + r')$', re.I)
TEXT_LANG_RE = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, NAMES), key=len, reverse=True)) + r')\b', re.I)

ANCESTOR = {'ine-pro', 'iir-pro', 'ira-pro', 'ae', 'peo', 'pal', 'xpr', 'xme'}   # Kurdish's own lineage
IRANIAN = {'fa', 'ckb', 'zza', 'hac', 'bal', 'os', 'ps', 'ku'}                    # sister languages
FAMILY = {}
for c in ('ar', 'arc', 'syc', 'he', 'akk', 'sem-pro', 'sem-wes-pro'): FAMILY[c] = 'Semitic / Sami'
for c in ('tr', 'ota', 'az', 'trk-pro', 'chg', 'tk', 'mn'): FAMILY[c] = 'Turkic-Mongolic / Türk-Moğol'
for c in ('fr', 'en', 'de', 'ru', 'it', 'es', 'pt', 'la', 'el', 'grc', 'gkm'): FAMILY[c] = 'European / Avrupa'
for c in ('hy', 'xcl', 'ka'): FAMILY[c] = 'Caucasian-Armenian / Kafkas-Ermeni'
for c in IRANIAN | ANCESTOR: FAMILY[c] = 'Iranian / İrani'
for c in ('sa', 'hi', 'ur'): FAMILY[c] = 'Indic / Hint'

REGIONS = ['Wan', 'Bidlîs', 'Bitlis', 'Amed', 'Diyarbekir', 'Mêrdîn', 'Botan', 'Cizîr', 'Serhed', 'Serheda Jorîn', 'Serhedî',
 'Behdînan', 'Badînî', 'Dihok', 'Zaxo', 'Hekarî', 'Colemêrg', 'Şingal', 'Efrîn', 'Kobanî', 'Amûdê', 'Qamişlo', 'Cizîra Botan',
 'Riha', 'Sirûc', 'Sêwreg', 'Qerejdax', 'Semsûr', 'Meletî', 'Elbistan', 'Dîlok', 'Mereş', 'Dêrsim', 'Qers', 'Agirî', 'Erzirom',
 'Mûş', 'Sêrt', 'Bismil', 'Stewr', 'Qoser', 'Xorasan', 'Ûrmiye', 'Qefqasya', 'Ermenistan', 'Reşwî', 'Aldûş', 'Tirkmancî', 'Hewlêr']
REG_RE = re.compile(r'\b(' + '|'.join(map(re.escape, sorted(REGIONS, key=len, reverse=True))) + r')\b')

def code(name): return NAMES.get(name.strip().lower(), name.strip().lower())

def classify_tree(text, lemma):
    """Parse 'Dara etîmolojiyê' language chain."""
    lines = [l.strip() for l in text.split('\n')]
    if not lines or not lines[0].lower().startswith('dara etîmolojiyê'): return None
    chain = []           # [(lang_code, marker)]
    for i, l in enumerate(lines[1:], 1):
        if NAME_RE.match(l):
            chain.append([code(l), ''])
            if code(l) == 'kmr' and i + 1 < len(lines) and lines[i + 1].startswith(lemma):
                break
        elif chain:
            m = re.search(r'(deyn|drş|bnr|kalq)\.\s*$', l)
            if m: chain[-1][1] = m.group(1)
    if len(chain) < 1 or chain[-1][0] != 'kmr': return None
    before = chain[:-1]
    if not before:
        return None          # tree shows only the word itself: no evidence
    src, mark = before[-1]
    path = ' > '.join(c for i, (c, _) in enumerate(chain) if i == 0 or chain[i - 1][0] != c)
    anc = before[0][0]
    if src == 'kmr':
        if '+' not in text: return None   # e.g. a pronoun form pointing to its base form, not a compound
        return dict(cls='internal', src='', anc=anc, path=path, how='ku-tree')
    if src in ANCESTOR and mark != 'deyn':
        return dict(cls='inherited', src=src, anc=anc, path=path, how='ku-tree')
    if src in IRANIAN:
        return dict(cls='borrowed-iranian', src=src, anc=anc, path=path, how='ku-tree')
    return dict(cls='borrowed', src=src, anc=anc, path=path, how='ku-tree')

def classify_text(text):
    t = text.lower()
    m = re.search(r'deyn ji ([^\s,.\[(]+(?: [^\s,.\[(]+)?)', t) or re.search(r'^\s*ji ([^\s,.\[(]+(?: [^\s,.\[(]+)?) \[peyv', t) \
        or re.search(r'bi rêya ([^\s,.\[(]+)', t)
    if m:
        lm = TEXT_LANG_RE.search(m.group(1))
        if lm:
            c = code(lm.group(1)); maybe = 'ihtimal' in t[:60]
            if c in ANCESTOR: return dict(cls='inherited', src=c, anc='', path='', how='ku-text')
            return dict(cls='borrowed-iranian' if c in IRANIAN else 'borrowed', src=c, anc='', path='', how='ku-text' + ('?' if maybe else ''))
    if re.search(r'ji zimanên îranî|ji proto-îranî|ji proto-hindûewropî|ji proto-hindûîranî', t[:120]):
        anc = [code(m.group(1)) for m in TEXT_LANG_RE.finditer(t[:160]) if code(m.group(1)) in ANCESTOR]
        c = anc[0] if anc else 'ira-pro'
        return dict(cls='inherited', src=c, anc=c, path='', how='ku-text')
    if 'onomatopo' in t[:200]:
        return dict(cls='onomatopoeic', src='', anc='', path='', how='ku-text')
    return None

def classify_morph(text):
    if re.search(r"^\s*(ji\s+)?[^\s+]+\s*\+\s*[^\s+]+", text.lower()):
        return dict(cls='internal', src='', anc='', path='', how='ku-text')
    return None

def classify_en(templates):
    inh = [t['args'].get('2') for t in templates if t.get('name') in ('inh', 'inh+')]
    bor = [t['args'].get('2') for t in templates if t.get('name') in ('bor', 'bor+', 'lbor')]
    der = [t['args'].get('2') for t in templates if t.get('name') in ('der', 'der+')]
    af = [t for t in templates if t.get('name') in ('af', 'affix', 'prefix', 'suffix', 'compound', 'com')]
    onom = [t for t in templates if t.get('name') in ('onom', 'onomatopoeic')]
    if bor:
        c = bor[0]; return dict(cls='borrowed-iranian' if c in IRANIAN else 'borrowed', src=c, anc='', path='', how='en-template')
    if inh:
        return dict(cls='inherited', src=inh[0], anc=inh[-1], path=' > '.join(reversed(inh)), how='en-template')
    if af: return dict(cls='internal', src='', anc='', path='', how='en-template')
    if onom: return dict(cls='onomatopoeic', src='', anc='', path='', how='en-template')
    if der:
        c = der[0]
        if c in ANCESTOR: return dict(cls='inherited', src=c, anc=der[-1], path='', how='en-template')
        return dict(cls='borrowed-iranian' if c in IRANIAN else 'borrowed', src=c, anc='', path='', how='en-template?')
    return None

en_tpl = {}
for line in open(os.path.join(RAW, 'en-NorthernKurdish.jsonl'), encoding='utf-8'):
    d = json.loads(line)
    if d.get('etymology_templates'): en_tpl.setdefault(d['word'], d['etymology_templates'])

freq = {}
p = os.path.join(D, 'frequency', 'kmr-wikipedia-frequency.tsv')
if os.path.exists(p):
    with open(p, encoding='utf-8') as f: freq = {r['word']: r['rank'] for r in csv.DictReader(f, delimiter='\t')}

rows = {}; regions = collections.defaultdict(set)
with gzip.open(os.path.join(RAW, 'ku.jsonl.gz'), 'rt') as f:
    for line in f:
        d = json.loads(line)
        if d.get('lang_code') != 'ku': continue
        w = d['word']
        tags = [r for s in d.get('senses') or [] for r in (s.get('raw_tags') or [])]
        tags += [r for s in d.get('synonyms') or [] for r in (s.get('raw_tags') or [])]
        tags += [r for s in d.get('sounds') or [] for r in (s.get('raw_tags') or []) + (s.get('tags') or [])]
        for t in tags:
            for m in REG_RE.finditer(t): regions[w].add(m.group(1))
        if d.get('pos_title', '').startswith('Formeke') or 'form-of' in (d.get('tags') or []): continue
        if d.get('pos') in ('proverb', 'phrase', 'character', 'symbol', 'abbrev'): continue
        texts = d.get('etymology_texts') or []
        res = None
        for tx in texts:
            res = classify_tree(tx, w) or res
        en = classify_en(en_tpl.get(w, []))
        if not res:
            for tx in texts:
                res = classify_text(tx)
                if res: break
        if not res and en: res = en
        if not res:
            for tx in texts:
                res = classify_morph(tx)
                if res: break
        if not res and 'onomatopoeic' in [t for s in d.get('senses') or [] for t in s.get('tags') or []]:
            res = dict(cls='onomatopoeic', src='', anc='', path='', how='ku-tag')
        if not res:
            res = dict(cls='unknown', src='', anc='', path='', how='')
        agree = en and res['how'] != 'en-template' and en['cls'] == res['cls']
        conf = 'high' if agree else 'low' if res['how'].endswith('?') or res['cls'] == 'unknown' else 'medium'
        k = (w, d.get('pos'))
        if k in rows and rows[k]['class'] != 'unknown': continue
        rows[k] = dict(word=w, pos=d.get('pos'), **{'class': res['cls']}, source_lang=res['src'],
                       source_family=FAMILY.get(res['src'], '') if res['cls'] != 'inherited' else 'Iranian / İrani',
                       ancestor=res['anc'], path=res['path'], evidence=res['how'].rstrip('?'), confidence=conf,
                       freq_rank=freq.get(w.lower(), ''), review_status='unverified')

out = sorted(rows.values(), key=lambda r: (int(r['freq_rank']) if r['freq_rank'] else 10**9, r['word'].lower()))
for r in out: r['regions'] = ', '.join(sorted(regions.get(r['word'], [])))
cols = ['word', 'pos', 'class', 'source_lang', 'source_family', 'ancestor', 'path', 'evidence', 'confidence', 'regions', 'freq_rank', 'review_status']
with open(os.path.join(D, 'kmr', 'db', 'etymology-class.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter='\t'); w.writeheader(); w.writerows(out)

# stats
st = collections.Counter(r['class'] for r in out)
known = [r for r in out if r['class'] != 'unknown']
top = [r for r in known if r['freq_rank'] and int(r['freq_rank']) <= 5000]
src = collections.Counter(r['source_lang'] for r in out if r['class'] in ('borrowed', 'borrowed-iranian'))
fam = collections.Counter(r['source_family'] for r in out if r['class'] in ('borrowed', 'borrowed-iranian'))
summary = dict(total=len(out), by_class=dict(st.most_common()), with_known_etymology=len(known),
               top5000_by_class=dict(collections.Counter(r['class'] for r in top).most_common()),
               loan_sources=dict(src.most_common(20)), loan_families=dict(fam.most_common()),
               by_confidence=dict(collections.Counter(r['confidence'] for r in out).most_common()),
               with_regions=sum(1 for r in out if r['regions']))
json.dump(summary, open(os.path.join(D, 'kmr', 'db', 'etymology-class.stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
