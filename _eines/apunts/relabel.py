# Reetiqueta els apartats dels quadres «Practica»: cada exercici numerat torna a començar per a).
# A la solució, les etiquetes passen a ser «1a)», «2b)»… (o «2)» si l'exercici té un sol apartat).
import re, sys

MARK = r'(?<![A-Za-z0-9\\{(À-ÿ·])%s\)'

def item_letters(li):
    body = re.sub(r'<span class="stars">.*?</span>', '', li)
    va = re.search(r'<span data-l="va">(.*?)</span>', body, re.S)
    txt = va.group(1) if va else body
    seen = []
    for m in re.finditer(MARK % '([a-p])', txt):
        if m.group(1) not in seen: seen.append(m.group(1))
    return seen

def fix_box(box, log):
    lis = re.findall(r'<li>.*?</li>', box, re.S)
    seqs = [item_letters(li) for li in lis]
    flat = [x for s in seqs for x in s]
    if not flat or len(flat) != len(set(flat)) or all(s[:1] in ([], ['a']) for s in seqs):
        log.append('skip ' + str(seqs)); return box
    lab = {}
    for i, s in enumerate(seqs):
        for j, g in enumerate(s):
            lab[g] = (i, 'abcdefghijklmnop'[j], len(s))
    for li, s in zip(lis, seqs):
        new = li
        for g in s:
            i, loc, n = lab[g]
            new = re.sub((MARK % g) + (r'\s*' if n == 1 else ''), '' if n == 1 else loc + ')', new)
        box = box.replace(li, new, 1)
    head, sol = box.split('<details class="sol">', 1)
    def tag(g):
        i, loc, n = lab[g]
        return '%d%s)' % (i + 1, loc if n > 1 else '')
    cnt = {}
    def rt(m): cnt[m.group(1)] = cnt.get(m.group(1), 0) + 1; return r'\text{%s}' % tag(m.group(1))
    def rp(m): cnt[m.group(1)] = cnt.get(m.group(1), 0) + 1; return tag(m.group(1))
    keys = ''.join(lab)
    sol = re.sub(r'\\text\{([%s])\)\}' % keys, rt, sol)
    sol = re.sub(MARK % ('([%s])' % keys), rp, sol)
    missing = [g for g in lab if g not in cnt]
    log.append('ok ' + str(seqs) + (' MISSING ' + str(missing) if missing else ''))
    return head + '<details class="sol">' + sol

def fix_file(path):
    s = open(path, encoding='utf-8').read()
    log = []
    s = re.sub(r'<div class="box pr">.*?</details>', lambda m: fix_box(m.group(0), log), s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)
    return log

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p.split('/')[-1]); print('\n'.join('  ' + l for l in fix_file(p)))
