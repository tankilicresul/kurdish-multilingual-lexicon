import csv, os, unicodedata

D = r'C:\Users\resul\Desktop\kurdish-multilingual-lexicon\data'

JUNK_TRANSLATIONS = {
    'alümin', 'telliir', 'malı götürmek', 'yallah', 'hodri', 'osmometer', 'darlingly',
    'cock, penis', 'abaço', 'ciro', 'elhak', 'filhakika', 'belirtisiz takı',
    'paça', 'pati', 'peduncled', 'pawprint', 'uçlu', 'sessiz', 'kısa kulaklı hayvan'
}

FUNCTION_WORDS = {
    'ji': ('prep', '-den, -dan', 'from, of', 'von, aus', 'temel edat / ablative preposition'),
    'li': ('prep', '-de, -da', 'at, in, on', 'in, an, bei', 'temel edat / locative preposition'),
    'di': ('prep', 'içinde, -de', 'in, inside', 'in', 'temel edat (di...de) / preposition'),
    'bi': ('prep', 'ile, vasıtasıyla', 'with, by', 'mit', 'temel edat (bi...re) / instrumental preposition'),
    'de': ('postp', 'içinde (di...de)', 'in (with di...de)', 'in', 'sontakı / postposition'),
    'jî': ('adv', 'de, da, dahi', 'also, too', 'auch', 'bağlama ve pekiştirme edatı'),
    'ya': ('part', 'dişil tamlama eki / olan', 'feminine construct / which', 'die, welche', 'tamlayan parçacığı (dişil)'),
    'yê': ('part', 'eril tamlama eki / olan', 'masculine construct / which', 'der, welcher', 'tamlayan parçacığı (eril)'),
    'yên': ('part', 'çoğul tamlama eki / olanlar', 'plural construct / which', 'die, welche', 'tamlayan parçacığı (çoğul)'),
    'ku': ('conj', 'ki, -dığı', 'that, which', 'dass, welches', 'bağlaç / conjunction'),
    'xwe': ('pron', 'kendi', 'oneself, self, own', 'selbst, eigen', 'dönüşlü zamir / reflexive pronoun'),
    'an': ('conj', 'veya, ya da', 'or', 'oder', 'bağlaç / conjunction'),
    've': ('postp', 'doğru, beri (ji...ve)', 'towards, since', 'hin zu, seit', 'sontakı / postposition'),
    'bo': ('prep', 'için', 'for', 'für', 'edat / preposition'),
    're': ('postp', 'ile, birlikte (bi...re)', 'with, together with', 'mit', 'sontakı / postposition'),
    'ew': ('pron', 'o, onlar', 'he, she, it, they', 'er, sie, es', 'şahıs ve işaret zamiri'),
    'wî': ('pron', 'onu, ona (eril)', 'him (masc. oblique)', 'ihn, ihm', 'bükümlü şahıs zamiri (eril)'),
    'wê': ('pron', 'onu, ona (dişil) / o (dişil)', 'her (fem. oblique)', 'sie, ihr', 'bükümlü şahıs zamiri (dişil)'),
    'wan': ('pron', 'onları, onlara', 'them', 'sie, ihnen', 'bükümlü şahıs zamiri (çoğul)'),
    'ev': ('pron', 'bu, bunlar', 'this, these', 'dieser, diese', 'işaret zamiri'),
    'vî': ('pron', 'bunu, buna (eril)', 'this (masc. oblique)', 'diesen, diesem', 'bükümlü işaret zamiri (eril)'),
    'vê': ('pron', 'bunu, buna (dişil)', 'this (fem. oblique)', 'diese, dieser', 'bükümlü işaret zamiri (dişil)'),
    'van': ('pron', 'bunları, bunlara', 'these (oblique)', 'diese, diesen', 'bükümlü işaret zamiri (çoğul)'),
    'ez': ('pron', 'ben', 'I', 'ich', '1. tekil şahıs zamiri'),
    'tu': ('pron', 'sen', 'you', 'du', '2. tekil şahıs zamiri'),
    'em': ('pron', 'biz', 'we', 'wir', '1. çoğul şahıs zamiri'),
    'hûn': ('pron', 'siz', 'you (pl.)', 'ihr, Sie', '2. çoğul şahıs zamiri'),
    'min': ('pron', 'beni, bana, benim', 'me, my (oblique)', 'mich, mir, mein', '1. tekil bükümlü zamir'),
    'te': ('pron', 'seni, sana, senin', 'you, your (oblique)', 'dich, dir, dein', '2. tekil bükümlü zamir'),
    'me': ('pron', 'bizi, bize, bizim', 'us, our (oblique)', 'uns, unser', '1. çoğul bükümlü zamir'),
    'we': ('pron', 'sizi, size, sizin', 'you, your (pl. oblique)', 'euch, euer', '2. çoğul bükümlü zamir'),
    'lê': ('conj', 'ama, fakat, ancak', 'but, however', 'aber, jedoch', 'bağlaç / conjunction'),
    'û': ('conj', 've', 'and', 'und', 'bağlaç / conjunction'),
    'ne': ('adv', 'değil, hayır', 'not, no', 'nicht, nein', 'olumsuzluk edatı'),
    'erê': ('adv', 'evet', 'yes', 'ja', 'onay edatı'),
    'her': ('adj', 'her', 'every, each', 'jeder, jede, jedes', 'belgisiz sıfat'),
    'hemû': ('adj', 'bütün, hepsi, tüm', 'all, entire', 'alle, ganz', 'belgisiz sıfat'),
    'çend': ('adj', 'kaç, birkaç', 'how many, several', 'wie viele, einige', 'soru ve belgisiz sıfat'),
    'gelek': ('adv', 'çok, pek çok', 'many, very, a lot', 'viele, sehr', 'miktar zarfı'),
    'wek': ('prep', 'gibi', 'like, as', 'wie', 'benzetme edatı'),
    'heta': ('prep', 'kadar, dek', 'until, as far as', 'bis', 'zaman ve yer edatı'),
    'piştî': ('prep', 'sonra', 'after', 'nach', 'zaman edatı'),
    'berî': ('prep', 'önce', 'before', 'vor', 'zaman edatı'),
    'yek': ('num', 'bir', 'one', 'eins', 'sayı sıfatı'),
    'du': ('num', 'iki', 'two', 'zwei', 'sayı sıfatı'),
    'sê': ('num', 'üç', 'three', 'drei', 'sayı sıfatı'),
    'çar': ('num', 'dört', 'four', 'vier', 'sayı sıfatı'),
    'pênc': ('num', 'beş', 'five', 'fünf', 'sayı sıfatı'),
    'şeş': ('num', 'altı', 'six', 'sechs', 'sayı sıfatı'),
    'heft': ('num', 'yedi', 'seven', 'sieben', 'sayı sıfatı'),
    'heşt': ('num', 'sekiz', 'eight', 'acht', 'sayı sıfatı'),
    'neh': ('num', 'dokuz', 'nine', 'neun', 'sayı sıfatı'),
    'deh': ('num', 'on', 'ten', 'zehn', 'sayı sıfatı'),
    'sed': ('num', 'yüz', 'hundred', 'hundert', 'sayı sıfatı'),
    'hezar': ('num', 'bin', 'thousand', 'tausend', 'sayı sıfatı'),
    'milyon': ('num', 'milyon', 'million', 'Million', 'sayı sıfatı'),
    'dema': ('adv', 'zamanında, -dığı zaman', 'when, while', 'wenn, als', 'zaman zarfı'),
    'nav': ('noun', 'ad, isim / iç, ara', 'name / inside, middle', 'Name / Mitte, Innen', ''),
    'ser': ('noun', 'baş, kafa / tepe, üst', 'head / top, on', 'Kopf / Spitze, auf', ''),
    'dest': ('noun', 'el / başlangıç', 'hand / beginning', 'Hand / Anfang', ''),
    'kar': ('noun', 'iş, çalışma', 'work, job', 'Arbeit, Werk', ''),
    'sal': ('noun', 'yıl, sene', 'year', 'Jahr', ''),
    'roj': ('noun', 'gün / güneş', 'day / sun', 'Tag / Sonne', ''),
    'şev': ('noun', 'gece', 'night', 'Nacht', ''),
    'av': ('noun', 'su', 'water', 'Wasser', ''),
    'nan': ('noun', 'ekmek', 'bread', 'Brot', ''),
    'mal': ('noun', 'ev, aile', 'house, home, family', 'Haus, Familie', ''),
    'welat': ('noun', 'ülke, vatan', 'country, homeland', 'Land, Heimat', ''),
    'bajar': ('noun', 'şehir, kent', 'city, town', 'Stadt', ''),
    'gund': ('noun', 'köy', 'village', 'Dorf', ''),
    'çav': ('noun', 'göz', 'eye', 'Auge', ''),
    'dil': ('noun', 'kalp, gönül', 'heart', 'Herz', ''),
    'ziman': ('noun', 'dil, lisan', 'language, tongue', 'Sprache, Zunge', ''),
    'mirov': ('noun', 'insan, kişi', 'human, person', 'Mensch, Person', ''),
    'jin': ('noun', 'kadın / eş', 'woman / wife', 'Frau', ''),
    'mêr': ('noun', 'erkek / koca', 'man / husband', 'Mann', ''),
    'zarok': ('noun', 'çocuk', 'child, kid', 'Kind', ''),
    'dayik': ('noun', 'anne', 'mother', 'Mutter', ''),
    'bav': ('noun', 'baba', 'father', 'Vater', ''),
    'bira': ('noun', 'kardeş, erkek kardeş', 'brother', 'Bruder', ''),
    'xwişk': ('noun', 'kız kardeş', 'sister', 'Schwester', ''),
    'heval': ('noun', 'arkadaş, dost', 'friend, comrade', 'Freund, Begleiter', ''),
    'dost': ('noun', 'dost, arkadaş', 'friend, close companion', 'Freund', ''),
    'dijmin': ('noun', 'düşman', 'enemy', 'Feind', ''),
    'kirin': ('verb', 'yapmak, etmek', 'to do, to make', 'tun, machen', 'geçişli fiil'),
    'bûn': ('verb', 'olmak', 'to be, to become', 'sein, werden', 'geçişsiz fiil'),
    'hatin': ('verb', 'gelmek', 'to come', 'kommen', 'geçişsiz fiil'),
    'çûn': ('verb', 'gitmek', 'to go', 'gehen', 'geçişsiz fiil'),
    'dîtin': ('verb', 'görmek', 'to see', 'sehen', 'geçişli fiil'),
    'bihîstin': ('verb', 'duymak, işitmek', 'to hear', 'hören', 'geçişli fiil'),
    'gotin': ('verb', 'söylemek, demek', 'to say, to tell', 'sagen', 'geçişli fiil'),
    'axaftin': ('verb', 'konuşmak', 'to speak, to talk', 'sprechen', 'geçişsiz fiil'),
    'xwendin': ('verb', 'okumak / ders çalışmak', 'to read / to study', 'lesen / studieren', 'geçişli fiil'),
    'nivîsandin': ('verb', 'yazmak', 'to write', 'schreiben', 'geçişli fiil'),
    'zanîn': ('verb', 'bilmek', 'to know', 'wissen, kennen', 'geçişli fiil'),
    'xwestin': ('verb', 'istemek / dilemek', 'to want, to wish', 'wollen, wünschen', 'geçişli fiil'),
    'man': ('verb', 'kalmak', 'to stay, to remain', 'bleiben', 'geçişsiz fiil'),
    'dan': ('verb', 'vermek', 'to give', 'geben', 'geçişli fiil'),
    'girtin': ('verb', 'tutmak, almak / kapatmak', 'to take, to hold / to close', 'halten, nehmen / schließen', 'geçişli fiil'),
    'birin': ('verb', 'götürmek / kazanmak', 'to take away / to win', 'mitnehmen / gewinnen', 'geçişli fiil'),
    'xwarin': ('verb', 'yemek', 'to eat / food', 'essen / Essen', 'geçişli fiil'),
    'vexwarin': ('verb', 'içmek', 'to drink', 'trinken', 'geçişli fiil'),
    'kenîn': ('verb', 'gülmek', 'to laugh', 'lachen', 'geçişsiz fiil'),
    'girîn': ('verb', 'ağlamak', 'to cry, to weep', 'weinen', 'geçişsiz fiil'),
    'ketin': ('verb', 'düşmek / girmek', 'to fall / to enter', 'fallen / eintreten', 'geçişsiz fiil'),
    'rabûn': ('verb', 'kalkmak / uyanmak', 'to rise, to get up', 'aufstehen', 'geçişsiz fiil'),
    'mezin': ('adj', 'büyük', 'big, large, great', 'groß', ''),
    'biçûk': ('adj', 'küçük', 'small, little', 'klein', ''),
    'baş': ('adj', 'iyi, güzel', 'good, fine', 'gut, schön', ''),
    'xirab': ('adj', 'kötü, bozuk', 'bad, broken', 'schlecht, kaputt', ''),
    'rind': ('adj', 'güzel, iyi', 'beautiful, nice', 'schön, gut', ''),
    'nû': ('adj', 'yeni', 'new', 'neu', ''),
    'kevn': ('adj', 'eski', 'old (not new)', 'alt', ''),
    'pîr': ('adj', 'yaşlı, ihtiyar', 'old, elderly', 'alt, betagt', ''),
    'ciwan': ('adj', 'genç', 'young', 'jung', ''),
    'germ': ('adj', 'sıcak', 'warm, hot', 'warm, heiß', ''),
    'sar': ('adj', 'soğuk', 'cold', 'kalt', ''),
    'şêrîn': ('adj', 'tatlı, sevimli', 'sweet, cute', 'süß, lieblich', ''),
    'tal': ('adj', 'acı (tat)', 'bitter', 'bitter', ''),
    'spî': ('adj', 'beyaz, ak', 'white', 'weiß', ''),
    'reş': ('adj', 'siyah, kara', 'black', 'schwarz', ''),
    'sor': ('adj', 'kırmızı, al', 'red', 'rot', ''),
    'kesk': ('adj', 'yeşil', 'green', 'grün', ''),
    'şîn': ('adj', 'mavi', 'blue', 'blau', ''),
    'zer': ('adj', 'sarı', 'yellow', 'gelb', ''),
    'qehweyî': ('adj', 'kahverengi', 'brown', 'braun', ''),
    'gewr': ('adj', 'gri, boz', 'gray', 'grau', ''),
}

# Load lemmas
lemmas = {}
with open(os.path.join(D, 'kmr', 'db', 'lemmas.tsv'), encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        lemmas[r['word']] = r

# Load translations
tr_map = {}
with open(os.path.join(D, 'kmr', 'kmr-tr.tsv'), encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        w = r['kurdish']
        t = r['translation'].strip()
        if t and t.lower() not in JUNK_TRANSLATIONS and len(t) > 1:
            tr_map.setdefault(w, []).append(t)

en_map = {}
with open(os.path.join(D, 'kmr', 'kmr-en.tsv'), encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        w = r['kurdish']
        t = r['translation'].strip()
        if t and t.lower() not in JUNK_TRANSLATIONS and len(t) > 1:
            en_map.setdefault(w, []).append(t)

de_map = {}
with open(os.path.join(D, 'kmr', 'kmr-de.tsv'), encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        w = r['kurdish']
        t = r['translation'].strip()
        if t and t.lower() not in JUNK_TRANSLATIONS and len(t) > 1:
            de_map.setdefault(w, []).append(t)

# Load frequency
freq = []
with open(os.path.join(D, 'frequency', 'kmr-wikipedia-frequency.tsv'), encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        freq.append(r['word'])

seen = set()
clean_rows = []

# First process high priority verified function words and core words in frequency order
for word in freq:
    w = word.strip()
    w_low = w.lower()

    if w_low in seen:
        continue

    if w_low in FUNCTION_WORDS:
        pos, tr_val, en_val, de_val, note = FUNCTION_WORDS[w_low]
        clean_rows.append(dict(
            kmr=w_low, pos=pos, tr=tr_val, en=en_val, de=de_val, note=note, review_status='ok'
        ))
        seen.add(w_low)
        continue

    # Look up lemma
    target = None
    if w in lemmas: target = w
    elif w_low in lemmas: target = w_low

    if not target or target.lower() in seen:
        continue

    info = lemmas[target]
    upos = info.get('upos', '')
    pos = info.get('pos', '')

    # Skip punctuation, symbols, affixes
    if upos in ('PUNCT', 'SYM') or pos in ('suffix', 'prefix'):
        continue

    # Filter out typical construct or inflected words if they don't have proper dictionary headword forms
    if target.endswith(('ên', 'ekî', 'ekê', 'anî')) and pos == 'noun':
        # likely inflected construct or oblique plural unless recognized lemma
        pass

    trs = [t for t in tr_map.get(target, []) if t.lower() not in JUNK_TRANSLATIONS]
    ens = [t for t in en_map.get(target, []) if t.lower() not in JUNK_TRANSLATIONS]
    des = [t for t in de_map.get(target, []) if t.lower() not in JUNK_TRANSLATIONS]

    # Must have both TR and EN
    if not trs or not ens:
        continue

    tr_clean = list(dict.fromkeys(trs))[:2]
    en_clean = list(dict.fromkeys(ens))[:2]
    de_clean = list(dict.fromkeys(des))[:2]

    # Clean display
    tr_str = ' | '.join(tr_clean)
    en_str = ' | '.join(en_clean)
    de_str = ' | '.join(de_clean)

    # Determine review_status
    # If sources agree >= 2 in core or high frequency
    rev_st = 'unverified'

    clean_rows.append(dict(
        kmr=target,
        pos=pos or upos.lower(),
        tr=tr_str,
        en=en_str,
        de=de_str,
        note='',
        review_status=rev_st
    ))
    seen.add(target.lower())

    if len(clean_rows) >= 3000:
        break

# Write out with sequential rank
out_path = os.path.join(D, 'learner', 'kmr-top3000.tsv')
cols = ['rank', 'kmr', 'pos', 'tr', 'en', 'de', 'note', 'review_status']

with open(out_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter='\t')
    w.writeheader()
    for i, r in enumerate(clean_rows, 1):
        r['rank'] = i
        # Ensure NFC normalization
        for k in r:
            if isinstance(r[k], str):
                r[k] = unicodedata.normalize('NFC', r[k])
        w.writerow(r)

print(f"Successfully generated {len(clean_rows)} clean rows in {out_path}.")
