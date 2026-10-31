#!/usr/bin/env python3
"""Core subset: Kurmancî pairs confirmed by 2+ independent Wiktionary editions.
This is the recommended starting point for human review."""
import csv, os, sys
D = sys.argv[1] if len(sys.argv) > 1 else 'data'
os.makedirs(os.path.join(D, 'core'), exist_ok=True)
for l in ('en', 'de', 'tr'):
    src = os.path.join(D, 'kmr', f'kmr-{l}.tsv')
    with open(src, encoding='utf-8') as f:
        rows = [r for r in csv.DictReader(f, delimiter='\t') if int(r['sources_agree']) > 1]
    cols = ['kurdish', 'pos', 'translation', 'sources_agree', 'source', 'review_status', 'reviewer', 'note']
    with open(os.path.join(D, 'core', f'kmr-{l}.core.tsv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter='\t', extrasaction='ignore'); w.writeheader()
        for r in rows: r['reviewer'] = ''; r['note'] = ''; w.writerow(r)
    print(l, len(rows))
