def bar_straight(x,w,top,bot): return f'M{x-w/2} {top} H{x+w/2} V{bot} H{x-w/2} Z'
def bar_bow(x,w,top,bot,dx,y0,y1):
    # Stab, der zwischen y0 und y1 um dx seitlich ausweicht (glatte kubische Kurven)
    h=(y1-y0)
    def side(off):
        return [(x+off,top),(x+off,y0),(x+off,y0+h*0.28),(x+off+dx,y0+h*0.22),(x+off+dx,y0+h*0.5),(x+off+dx,y0+h*0.78),(x+off,y1-h*0.28),(x+off,y1),(x+off,bot)]
    l=side(-w/2); r=side(w/2)
    def path(pts):
        p=pts; return f'L{p[0][0]} {p[0][1]} L{p[1][0]} {p[1][1]} C{p[2][0]} {p[2][1]} {p[3][0]} {p[3][1]} {p[4][0]} {p[4][1]} C{p[5][0]} {p[5][1]} {p[6][0]} {p[6][1]} {p[7][0]} {p[7][1]} L{p[8][0]} {p[8][1]}'
    rr=list(reversed(r))
    d=f'M{l[0][0]} {l[0][1]} '+path(l)[1:].replace('L','L',1)
    d=f'M{l[0][0]} {l[0][1]} L{l[1][0]} {l[1][1]} C{l[2][0]} {l[2][1]} {l[3][0]} {l[3][1]} {l[4][0]} {l[4][1]} C{l[5][0]} {l[5][1]} {l[6][0]} {l[6][1]} {l[7][0]} {l[7][1]} L{l[8][0]} {l[8][1]} '
    d+=f'L{r[8][0]} {r[8][1]} L{r[7][0]} {r[7][1]} C{r[6][0]} {r[6][1]} {r[5][0]} {r[5][1]} {r[4][0]} {r[4][1]} C{r[3][0]} {r[3][1]} {r[2][0]} {r[2][1]} {r[1][0]} {r[1][1]} L{r[0][0]} {r[0][1]} Z'
    return d
def mark(v,col):
    top,bot=140,860; w=46
    if v=='p1':   # 4 Stäbe, die beiden mittleren biegen sich auseinander, Mensch in der Öffnung
        xs=[230,410,590,770]; out=''
        out+=f'<path fill="{col}" d="{bar_straight(xs[0],w,top,bot)}"/>'
        out+=f'<path fill="{col}" d="{bar_bow(xs[1],w,top,bot,-95,290,760)}"/>'
        out+=f'<path fill="{col}" d="{bar_bow(xs[2],w,top,bot,95,290,760)}"/>'
        out+=f'<path fill="{col}" d="{bar_straight(xs[3],w,top,bot)}"/>'
        out+=f'<circle cx="500" cy="470" r="62" fill="{col}"/>'
        return out
    if v=='p2':   # 3 Stäbe, mittlere beiden ausgewichen; Kreisrahmen? nein: nur zwei Stäbe + Mensch, minimal
        out=f'<path fill="{col}" d="{bar_bow(380,w,top,bot,-110,260,780)}"/><path fill="{col}" d="{bar_bow(620,w,top,bot,110,260,780)}"/>'
        out+=f'<circle cx="500" cy="455" r="66" fill="{col}"/>'
        return out
    if v=='p3':   # 5 Stäbe, mittlerer Stab fehlt im oberen Teil, an seiner Stelle steigt der Mensch auf (Punkt)
        xs=[180,340,500,660,820]; out=''
        for i,x in enumerate(xs):
            if i==1: out+=f'<path fill="{col}" d="{bar_bow(x,w,top,bot,-70,240,700)}"/>'
            elif i==3: out+=f'<path fill="{col}" d="{bar_bow(x,w,top,bot,70,240,700)}"/>'
            elif i==2: out+=f'<path fill="{col}" d="{bar_straight(x,w,640,bot)}"/>'
            else: out+=f'<path fill="{col}" d="{bar_straight(x,w,top,bot)}"/>'
        out+=f'<circle cx="500" cy="420" r="58" fill="{col}"/>'
        return out
