import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { upper, lower, normalize, compare, isWord, parseTSV } from '../js/kurdi.js';

assert.equal(upper('pisîk'), 'PISÎK');
assert.equal(upper('silav'), 'SILAV');
assert.equal(lower('KÛÇIK'), 'kûçik');
assert.equal(normalize('nézîk', true), 'nêzîk');
assert.deepEqual(['şev', 'sor', 'çav', 'cil', 'êvar', 'ezman'].sort(compare), ['cil', 'çav', 'ezman', 'êvar', 'sor', 'şev']);
assert.ok(isWord('Xwişk'));
assert.ok(!isWord('köpek'));
const rows = parseTSV(readFileSync(new URL('../../data/games/kmr-5-harf.tsv', import.meta.url), 'utf8'));
assert.ok(rows.length > 500 && rows.every(r => [...r.word].length === 5));
console.log('kurdi.js: all tests passed');
