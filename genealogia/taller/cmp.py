# -*- coding: utf-8 -*-
import json, re, pickle, unicodedata, difflib

pages = json.load(open('mypages.json', encoding='utf-8'))
idx   = json.load(open('indice_final.json', encoding='utf-8'))['pages']
exp   = pickle.load(open('exp.pkl','rb'))

def clean_page(i):
    # U+FFFE marca el punto de guionizacion suave que produjo un salto de
    # linea visible (silabas() en bookstyle_extraido.js); para comparar
    # contra el texto esperado (sin guionizar) se reune la palabra quitando
    # la marca, en vez de dejar un guion literal que rompe el token en dos.
    t = pages[i].replace('￾', '')
    L = [l for l in t.replace('\r\n','\n').split('\n') if l.strip()]
    meta = idx[i]
    if not meta['bleed']:
        if L: L = L[1:]                       # cornisa
        if L and meta.get('impreso'):
            # folio al pie
            if L and re.fullmatch(r'[ivxlcdm]+|\d+', L[-1].strip(), re.I):
                L = L[:-1]
    return L

act_tok = []   # (page, token)
for i in range(len(pages)):
    for l in clean_page(i):
        for w in l.split():
            act_tok.append((i, w))

exp_tok = []
for bi, s in exp:
    for w in s.split():
        exp_tok.append((bi, w))

def norm(w):
    w = unicodedata.normalize('NFC', w)
    w = w.replace('’',"'").replace('–','-').replace('—','-')
    return w

A = [norm(w) for _,w in exp_tok]
B = [norm(w) for _,w in act_tok]
print('exp tokens', len(A), 'act tokens', len(B))

sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
ops = sm.get_opcodes()
pickle.dump((exp_tok, act_tok, A, B, ops), open('align.pkl','wb'))
tot=0
for tag,i1,i2,j1,j2 in ops:
    if tag=='equal': continue
    tot+=1
print('opcodes no iguales:', tot)
for tag,i1,i2,j1,j2 in ops:
    if tag=='equal': continue
    print('---', tag, 'bloq', exp_tok[i1][0] if i1<len(exp_tok) else '?', 'pag', act_tok[j1][0] if j1<len(act_tok) else '?')
    print('  EXP:', ' '.join(A[max(0,i1-6):i1]), '<<<', ' '.join(A[i1:i2])[:300], '>>>', ' '.join(A[i2:i2+6]))
    print('  ACT:', ' '.join(B[max(0,j1-6):j1]), '<<<', ' '.join(B[j1:j2])[:300], '>>>', ' '.join(B[j2:j2+6]))
