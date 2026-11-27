import hashlib,urllib.request,urllib.parse,urllib.error,sys,os,time
UA='SchoolMusicVideoProject/1.0 (educational, non-commercial)'
def tr(name,q):
    n=name.replace(' ','_'); h=hashlib.md5(n.encode()).hexdigest(); e=urllib.parse.quote(n)
    return f'https://upload.wikimedia.org/wikipedia/commons/transcoded/{h[0]}/{h[:2]}/{e}/{e}.{q}'
jobs=[l.strip().split('|') for l in open(sys.argv[1]) if l.strip()]
VAR=['1080p.vp9.webm','720p.vp9.webm','720p.webm','480p.vp9.webm']
def head(u):
    for k in range(8):
        try:
            r=urllib.request.Request(u,headers={'User-Agent':UA},method='HEAD'); urllib.request.urlopen(r,timeout=60); return 200
        except urllib.error.HTTPError as e:
            if e.code==404: return 404
            time.sleep(min(int(e.headers.get('retry-after','30') or 30),120))
    return 0
for name,q in jobs:
    if q=='auto':
        for v in VAR:
            if head(tr(name,v))==200: q=v; break
        else: print('keine Fassung',name,flush=True); continue
    out='src/'+name.replace(' ','_')+'.'+q
    if os.path.exists(out) and os.path.getsize(out)>100000: print('vorhanden',name,flush=True); continue
    for k in range(10):
        try:
            r=urllib.request.Request(tr(name,q),headers={'User-Agent':UA})
            with urllib.request.urlopen(r,timeout=300) as f, open(out+'.part','wb') as o:
                while True:
                    b=f.read(1<<20)
                    if not b: break
                    o.write(b)
            os.rename(out+'.part',out); print('ok',os.path.getsize(out)//1048576,'MB',name,flush=True); break
        except urllib.error.HTTPError as e:
            ra=int(e.headers.get('retry-after','30') or 30); w=min(max(ra,20),180); print('HTTP',e.code,'warte',w,'s',name,flush=True); time.sleep(w)
        except Exception as e:
            print('Fehler',e,flush=True); time.sleep(20)
    time.sleep(8)
print('FERTIG',flush=True)
