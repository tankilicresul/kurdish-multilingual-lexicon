#!/usr/bin/env python3
"""
Word-frequency lists from Wikipedia dumps (Kurmancî: kuwiki, Soranî: ckbwiki, Zazakî: diqwiki).

Usage:
  curl -O https://dumps.wikimedia.org/kuwiki/latest/kuwiki-latest-pages-articles.xml.bz2
  python3 scripts/frequency.py kuwiki-latest-pages-articles.xml.bz2 kmr data/frequency

Method (kept simple and reproducible):
  * only main-namespace articles, redirects skipped
  * crude wikitext cleanup (templates, tables, refs, links, tags, URLs)
  * articles shorter than MIN_CHARS after cleanup are skipped, because Kurdish
    Wikipedias contain many bot-generated stubs that would distort the counts
  * ranking uses document frequency (in how many articles a word occurs),
    which is more robust than raw counts against long repetitive pages
Limits: Wikipedia is encyclopedic text; everyday words (greetings, food, family)
are under-represented compared with speech. See docs/frekans.md.
"""
import bz2, re, sys, os, collections, unicodedata
import xml.etree.ElementTree as ET

MIN_CHARS = 1200
TOP = 50000

LATIN = "a-zçêîûşàáâäéèëíìïóòôöúùüxqwı"
ARAB = "ء-ي٠-٩ٱ-ۓەۺ-ۿژڤگۆێڕڵچپ"
TOKEN = {
    'kmr': re.compile(rf"[{LATIN}]+(?:['’][{LATIN}]+)?"),
    'zza': re.compile(rf"[{LATIN}]+(?:['’][{LATIN}]+)?"),
    'ckb': re.compile(rf"[{ARAB}]+"),
}

def clean(t):
    t = re.sub(r'<!--.*?-->', ' ', t, flags=re.S)
    t = re.sub(r'<ref[^>]*/>', ' ', t)
    t = re.sub(r'<ref.*?</ref>', ' ', t, flags=re.S)
    for _ in range(3):  # nested templates
        t = re.sub(r'\{\{[^{}]*\}\}', ' ', t)
    t = re.sub(r'\{\|.*?\|\}', ' ', t, flags=re.S)                 # tables
    t = re.sub(r'\[\[[^\]|:]+:[^\]]*\]\]', ' ', t)                  # [[Kategorî:..]], [[Wêne:..]], interwiki
    t = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', t)         # [[a|b]] -> b
    t = re.sub(r'\[https?://[^\s\]]*\s?([^\]]*)\]', r'\1', t)
    t = re.sub(r'https?://\S+', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r"'{2,}", '', t)
    t = re.sub(r'^[=*#:;|!].*$', ' ', t, flags=re.M)               # headings, lists of metadata, table rows
    return t

def lower_ku(s):
    # Kurdish Latin: I -> i, Î -> î (not Turkish dotless/dotted rules)
    return unicodedata.normalize('NFC', s.replace('I', 'i').replace('Î', 'î').lower())

def main(dump, variety, outdir):
    tok = TOKEN[variety]
    df, cnt = collections.Counter(), collections.Counter()
    pages = used = 0
    ns = text = None; redirect = False
    for ev, el in ET.iterparse(bz2.open(dump), events=('end',)):
        tag = el.tag.rsplit('}', 1)[-1]
        if tag == 'ns': ns = el.text
        elif tag == 'redirect': redirect = True
        elif tag == 'text': text = el.text or ''
        elif tag == 'page':
            pages += 1
            if ns == '0' and not redirect and text and not text.lstrip().lower().startswith('#'):
                c = clean(text)
                if len(c) >= MIN_CHARS:
                    used += 1
                    words = tok.findall(lower_ku(c))
                    words = [w for w in words if 1 < len(w) < 30 and w not in ('thumb', 'px', 'jpg', 'png')]
                    cnt.update(words); df.update(set(words))
            ns = text = None; redirect = False
            el.clear()
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, f'{variety}-wikipedia-frequency.tsv')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('rank\tword\tdoc_freq\tcount\n')
        for i, (w, d) in enumerate(sorted(df.items(), key=lambda x: (-x[1], -cnt[x[0]], x[0]))[:TOP], 1):
            f.write(f'{i}\t{w}\t{d}\t{cnt[w]}\n')
    print(variety, 'pages', pages, 'used', used, 'types', len(df), '->', out)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'data/frequency')
