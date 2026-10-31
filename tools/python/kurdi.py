"""
kurdi.py — small, dependency-free helpers for Kurdish text (Kurmancî / Zazakî Latin, Soranî Arabic).

    from kurdi import upper, lower, normalize, sort_key, is_word, Lexicon

Why: Kurmancî uses the Hawar alphabet. Generic or Turkish-locale case mapping breaks it
(e.g. Turkish rules turn "i" into "İ"), and many people type é/ë/ì/ù instead of ê/î/û.
"""
import csv, os, unicodedata

KMR_ALPHABET = list('abcçdeêfghiîjklmnopqrsştuûvwxyz')            # Hawar, 31 letters
ZZA_ALPHABET = list('abcçdeêfgğhıiîjklmnopqrsştuûvwxyz')            # common Zazakî orthography (to be reviewed)
_ORDER = {c: i for i, c in enumerate(KMR_ALPHABET)}

# Frequent keyboard substitutes -> Hawar letters (only applied when normalize(..., fix_typing=True))
TYPING_FIXES = {
    'é': 'ê', 'è': 'ê', 'ë': 'ê', 'É': 'Ê', 'È': 'Ê', 'Ë': 'Ê',
    'í': 'î', 'ì': 'î', 'ï': 'î', 'Í': 'Î', 'Ì': 'Î', 'Ï': 'Î',
    'ú': 'û', 'ù': 'û', 'ü': 'û', 'Ú': 'Û', 'Ù': 'Û', 'Ü': 'Û',
    'ı': 'i', 'İ': 'I',      # Turkish dotless/dotted i do not exist in Kurmancî
}

def lower(s: str) -> str:
    """Kurdish lower case: I -> i (never ı), İ -> i."""
    return unicodedata.normalize('NFC', s.replace('İ', 'i').replace('I', 'i')).lower()

def upper(s: str) -> str:
    """Kurdish upper case: i -> I (never İ), î -> Î."""
    return unicodedata.normalize('NFC', s.replace('i', 'I').replace('ı', 'I')).upper()

def normalize(s: str, fix_typing: bool = False) -> str:
    """NFC + trimmed whitespace; optionally map common keyboard substitutes to Hawar letters."""
    s = unicodedata.normalize('NFC', ' '.join(s.split()))
    if fix_typing:
        s = ''.join(TYPING_FIXES.get(c, c) for c in s)
    return s

def sort_key(word: str):
    """Sort Kurmancî words in Hawar alphabet order (c < ç, e < ê, i < î, s < ş, u < û)."""
    return [_ORDER.get(c, 100 + ord(c)) for c in lower(word)]

def is_word(s: str, alphabet=KMR_ALPHABET) -> bool:
    """True if s contains only letters of the given alphabet (case-insensitive)."""
    a = set(alphabet)
    return bool(s) and all(c in a for c in lower(s))

class Lexicon:
    """Tiny loader for the TSV files in data/.

        lx = Lexicon('data')
        lx.translate('pisîk', 'tr')        -> ['kedi', ...]
        lx.find('kedi', 'tr')              -> ['pisîk', ...]
    """
    def __init__(self, data_dir='data', variety='kmr'):
        self.pairs = {}
        for lang in ('en', 'de', 'tr'):
            p = os.path.join(data_dir, variety, f'{variety}-{lang}.tsv')
            if not os.path.exists(p):
                continue
            with open(p, encoding='utf-8') as f:
                for r in csv.DictReader(f, delimiter='\t'):
                    self.pairs.setdefault(lang, []).append(r)

    def translate(self, word, lang):
        w = lower(word)
        rows = [r for r in self.pairs.get(lang, []) if lower(r['kurdish']) == w]
        rows.sort(key=lambda r: -int(r['sources_agree']))
        return list(dict.fromkeys(r['translation'] for r in rows))

    def find(self, target, lang):
        t = target.lower()
        rows = [r for r in self.pairs.get(lang, []) if r['translation'].lower() == t]
        rows.sort(key=lambda r: -int(r['sources_agree']))
        return list(dict.fromkeys(r['kurdish'] for r in rows))
