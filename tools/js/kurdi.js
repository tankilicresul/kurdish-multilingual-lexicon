/**
 * kurdi.js — dependency-free helpers for Kurdish text in the browser or Node.
 * Kurmancî (Hawar Latin) case mapping, typing fixes, alphabet sorting, word check.
 *
 *   import { upper, lower, normalize, compare, isWord } from './kurdi.js';
 *   upper('pisîk')  // "PISÎK"  (not "PİSÎK" as with the Turkish locale)
 */
export const KMR_ALPHABET = [...'abcçdeêfghiîjklmnopqrsştuûvwxyz'];
const ORDER = new Map(KMR_ALPHABET.map((c, i) => [c, i]));

export const TYPING_FIXES = {
  'é': 'ê', 'è': 'ê', 'ë': 'ê', 'É': 'Ê', 'È': 'Ê', 'Ë': 'Ê',
  'í': 'î', 'ì': 'î', 'ï': 'î', 'Í': 'Î', 'Ì': 'Î', 'Ï': 'Î',
  'ú': 'û', 'ù': 'û', 'ü': 'û', 'Ú': 'Û', 'Ù': 'Û', 'Ü': 'Û',
  'ı': 'i', 'İ': 'I'
};

/** Kurdish lower case: I → i (never ı). */
export const lower = s => s.replace(/İ/g, 'i').replace(/I/g, 'i').toLowerCase().normalize('NFC');

/** Kurdish upper case: i → I (never İ). Do NOT use toLocaleUpperCase('tr') for Kurmancî. */
export const upper = s => s.replace(/i/g, 'I').replace(/ı/g, 'I').toUpperCase().normalize('NFC');

/** NFC + single spaces; optionally fix é/ì/ù style typing to ê/î/û. */
export function normalize(s, fixTyping = false) {
  s = s.normalize('NFC').trim().replace(/\s+/g, ' ');
  return fixTyping ? [...s].map(c => TYPING_FIXES[c] ?? c).join('') : s;
}

/** Comparator for Array.prototype.sort in Hawar alphabet order. */
export function compare(a, b) {
  const x = [...lower(a)], y = [...lower(b)];
  for (let i = 0; i < Math.min(x.length, y.length); i++) {
    const p = ORDER.has(x[i]) ? ORDER.get(x[i]) : 100 + x[i].codePointAt(0);
    const q = ORDER.has(y[i]) ? ORDER.get(y[i]) : 100 + y[i].codePointAt(0);
    if (p !== q) return p - q;
  }
  return x.length - y.length;
}

/** True if the word uses only Kurmancî letters. */
export const isWord = (s, alphabet = KMR_ALPHABET) => !!s && [...lower(s)].every(c => alphabet.includes(c));

/** Parse a TSV file's text (e.g. fetched data/games/kmr-5-harf.tsv) into objects. */
export function parseTSV(text) {
  const [head, ...lines] = text.trim().split(/\r?\n/);
  const cols = head.split('\t');
  return lines.map(l => Object.fromEntries(l.split('\t').map((v, i) => [cols[i], v])));
}
