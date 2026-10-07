import re,os,subprocess,sys,json
root='lean'
def path(m): return os.path.join(root,*m.split('.'))+'.lean'
def imports(p):
    out=[]
    for line in open(p,encoding='utf-8'):
        s=line.strip()
        if s.startswith('import '):
            out+= s.split()[1:]
        elif s and not s.startswith('--') and not s.startswith('module') and not s.startswith('public') and not s.startswith('/-') and not s.startswith('prelude') and not s.startswith('import'):
            # Lean imports must come first; stop at first non-import line
            if not s.startswith('meta') : break
    return out
start='OAI.NumberTheory.DirichletL.Nonvanishing'
seen=set(); missing=set(); ext=set(); stack=[start]
while stack:
    m=stack.pop()
    if m in seen: continue
    if not m.startswith('OAI'):
        ext.add(m.split('.')[0]); continue
    p=path(m)
    if not os.path.exists(p): missing.add(m); continue
    seen.add(m)
    stack+=imports(p)
json.dump({'seen':sorted(seen),'missing':sorted(missing),'ext':sorted(ext)},open('../closure.json','w'))
print(len(seen),len(missing),sorted(ext))
print(sorted({'/'.join(m.split('.')[:3]) for m in missing})[:50])
