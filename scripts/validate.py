#!/usr/bin/env python3
"""Checks every TSV in data/: header, required columns, UTF-8/NFC, empty cells, allowed review_status."""
import csv, glob, os, sys, unicodedata
csv.field_size_limit(10**7)
D = sys.argv[1] if len(sys.argv) > 1 else 'data'
STATUS = {'unverified', 'ok', 'fixed', 'regional', 'rare', 'wrong'}
errors = 0
for p in sorted(glob.glob(os.path.join(D, '**', '*.tsv'), recursive=True)):
    with open(p, encoding='utf-8') as f:
        rd = csv.DictReader(f, delimiter='\t')
        cols = rd.fieldnames or []
        n = 0
        for i, r in enumerate(rd, 2):
            n += 1
            if None in r:
                print(f'{p}:{i}: too many columns'); errors += 1; continue
            if 'review_status' in cols and r['review_status'] not in STATUS:
                print(f'{p}:{i}: bad review_status {r["review_status"]!r}'); errors += 1
            for c in ('kurdish', 'kmr', 'word'):
                if c in cols and c != 'kmr' and not r[c].strip():
                    print(f'{p}:{i}: empty {c}'); errors += 1
            line = '\t'.join(v or '' for v in r.values())
            if unicodedata.normalize('NFC', line) != line:
                print(f'{p}:{i}: text is not NFC-normalized'); errors += 1
            if errors > 50: sys.exit('too many errors')
    print(f'ok  {n:>7}  {p}')
sys.exit(1 if errors else 0)
