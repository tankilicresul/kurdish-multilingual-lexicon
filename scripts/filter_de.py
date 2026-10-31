#!/usr/bin/env python3
"""Stream the German Wiktionary extract and keep only entries related to Kurdish.
Usage: curl -s https://kaikki.org/dictionary/downloads/de/de-extract.jsonl.gz | python3 scripts/filter_de.py > raw/de-kurdish.jsonl"""
import gzip, json, sys
KEYS = ('ku', 'kmr', 'ckb', 'sdh', 'zza', 'diq', 'kiu', 'hac', 'lki')
for line in gzip.open(sys.stdin.buffer, 'rt'):
    if not any(f'"{k}"' in line for k in KEYS): continue
    d = json.loads(line); lc = d.get('lang_code')
    tr = [t for t in d.get('translations', []) or [] if t.get('lang_code') in KEYS]
    if lc in KEYS or tr:
        print(json.dumps({'word': d.get('word'), 'lang_code': lc, 'lang': d.get('lang'), 'pos': d.get('pos'),
                          'senses': [{'glosses': s.get('glosses')} for s in d.get('senses', [])][:6],
                          'translations': tr}, ensure_ascii=False))
