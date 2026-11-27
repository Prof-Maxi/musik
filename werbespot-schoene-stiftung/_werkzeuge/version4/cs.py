import sys,json,urllib.request,urllib.error,urllib.parse,re,html
UA='SchoolMusicVideoProject/1.0 (educational, non-commercial)'
API='https://commons.wikimedia.org/w/api.php'
def api(**p):
    p.update(format='json',formatversion=2)
    import time
    for k in range(12):
        r=urllib.request.Request(API+'?'+urllib.parse.urlencode(p),headers={'User-Agent':UA})
        try:
            out=json.load(urllib.request.urlopen(r,timeout=30)); time.sleep(6); return out
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(8+6*k); continue
            raise
    raise RuntimeError('rate limited')
def strip(s): return html.unescape(re.sub('<[^>]+>','',s or '')).strip()
def search(q,n=15):
    d=api(action='query',generator='search',gsrsearch=f'filetype:video {q}',gsrnamespace=6,gsrlimit=n,prop='imageinfo|videoinfo',
          iiprop='url|size|extmetadata|mime',viprop='derivatives',iiextmetadatafilter='LicenseShortName|Artist|ImageDescription|DateTimeOriginal|Credit')
    out=[]
    for pg in d.get('query',{}).get('pages',[]):
        ii=pg.get('imageinfo',[{}])[0]; m=ii.get('extmetadata',{})
        g=lambda k: strip(m.get(k,{}).get('value',''))
        out.append(dict(title=pg['title'],w=ii.get('width'),h=ii.get('height'),dur=ii.get('duration'),size=ii.get('size'),
            lic=g('LicenseShortName'),artist=g('Artist')[:60],date=g('DateTimeOriginal')[:20],desc=g('ImageDescription')[:110],url=ii.get('url'),page=ii.get('descriptionurl')))
    return out
if __name__=='__main__':
    for q in sys.argv[1:]:
        print('###',q)
        try: res=search(q)
        except Exception as e: print("  (übersprungen:",e,")"); continue
        for r in res:
            if (r['h'] or 0)>=720:
                print(f"{r['w']}x{r['h']} {r['dur'] and round(r['dur'])}s | {r['lic']} | {r['artist']} | {r['date']} | {r['title'][5:80]}\n     {r['desc']}")
