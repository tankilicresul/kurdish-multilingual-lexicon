#!/usr/bin/env python3
"""Build one queryable SQLite file (not committed; ~100 MB): python3 scripts/to_sqlite.py data kurdish_lexicon.sqlite

    SELECT translation FROM pairs WHERE kurdish='pisîk' AND lang='tr' ORDER BY sources_agree DESC;
    SELECT * FROM multilingual WHERE tr LIKE '%kedi%';
"""
import csv, glob, os, sqlite3, sys
csv.field_size_limit(10**7)
D, OUT = (sys.argv[1:3] + ['data', 'kurdish_lexicon.sqlite'][len(sys.argv[1:3]):])
if os.path.exists(OUT): os.remove(OUT)
db = sqlite3.connect(OUT)
def load(table, files):
    rows = []
    cols = None
    for p in files:
        with open(p, encoding='utf-8') as f:
            rd = csv.DictReader(f, delimiter='\t'); cols = cols or rd.fieldnames
            rows += [[r.get(c, '') for c in cols] for r in rd]
    db.execute(f'CREATE TABLE {table} ({", ".join(c + " TEXT" for c in cols)})')
    db.executemany(f'INSERT INTO {table} VALUES ({",".join("?" * len(cols))})', rows)
    print(table, len(rows))
load('pairs', sorted(glob.glob(os.path.join(D, '*', '*-??.tsv'))))
load('pivot', sorted(glob.glob(os.path.join(D, '*', '*.pivot.tsv'))))
load('cross_dialect', [os.path.join(D, 'cross-dialect.tsv')])
load('multilingual', [os.path.join(D, 'multilingual', 'kmr-tr-en-de.tsv')])
for v in ('kmr', 'ckb', 'zza'):
    load(f'freq_{v}', [os.path.join(D, 'frequency', f'{v}-wikipedia-frequency.tsv')])
db.execute('CREATE INDEX ix_pairs_ku ON pairs(kurdish)'); db.execute('CREATE INDEX ix_pairs_tr ON pairs(translation)')
db.commit(); db.close(); print('->', OUT)
