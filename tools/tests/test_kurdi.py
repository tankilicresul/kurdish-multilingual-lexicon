import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))
from kurdi import upper, lower, normalize, sort_key, is_word, Lexicon

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

class T(unittest.TestCase):
    def test_case(self):
        self.assertEqual(upper('pisîk'), 'PISÎK')
        self.assertEqual(upper('silav'), 'SILAV')
        self.assertEqual(lower('KÛÇIK'), 'kûçik')
        self.assertEqual(lower('Îro'), 'îro')

    def test_typing(self):
        self.assertEqual(normalize('nézîk', fix_typing=True), 'nêzîk')
        self.assertEqual(normalize('pisìk', fix_typing=True), 'pisîk')
        self.assertEqual(normalize('  a   b '), 'a b')

    def test_sort(self):
        words = ['şev', 'sor', 'çav', 'cil', 'êvar', 'ezman']
        self.assertEqual(sorted(words, key=sort_key), ['cil', 'çav', 'ezman', 'êvar', 'sor', 'şev'])

    def test_is_word(self):
        self.assertTrue(is_word('Xwişk'))
        self.assertFalse(is_word('köpek'))

    def test_lexicon(self):
        lx = Lexicon(os.path.join(ROOT, 'data'))
        self.assertIn('kedi', lx.translate('pisîk', 'tr'))
        self.assertIn('pisîk', lx.find('cat', 'en'))

if __name__ == '__main__':
    unittest.main()
