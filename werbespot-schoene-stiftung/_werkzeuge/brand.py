import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
F='/tmp/claude-0/-home-user/6281bc19-abf7-5120-8af0-6085bfbd0df3/scratchpad/fonts/'
FONTS={'semibold':'/usr/share/fonts/opentype/inter/Inter-SemiBold.otf','medium':'/usr/share/fonts/opentype/inter/Inter-Medium.otf',
 'regular':'/usr/share/fonts/opentype/inter/Inter-Regular.otf','light':'/usr/share/fonts/opentype/inter/Inter-Light.otf',
 'serif':F+'SourceSerif4-latin-400-normal.ttf','serifi':F+'SourceSerif4-latin-400-italic.ttf','serifl':F+'SourceSerif4-latin-300-normal.ttf'}
_c={}
def font(k):
    if k not in _c: _c[k]=TTFont(FONTS[k])
    return _c[k]
def text_path(txt,k,size,x,y,track=0.0):
    """returns (svg path d, advance width). y = baseline"""
    f=font(k); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; s=size/upm
    hm=f['hmtx']; out=[]; cx=x
    for ch in txt:
        g=cmap.get(ord(ch)); 
        if g is None: raise ValueError(ch)
        pen=SVGPathPen(gs); tp=TransformPen(pen,(s,0,0,-s,cx,y)); gs[g].draw(tp)
        out.append(pen.getCommands()); cx+=hm[g][0]*s+track*size
    return ' '.join(out), cx-x-track*size
def width(txt,k,size,track=0.0): return text_path(txt,k,size,0,0,track)[1]

NAVY='#0E2040'; BLACK='#0B0B0C'; WHITE='#FFFFFF'; PAPER='#F4F2EE'; GREY='#8A8F98'
# mark geometry in a 1000 box
GAP=56; R=400; SW=58; DOTY=230; DOTR=62
def mark_svg(ox,oy,scale,col):
    a=math.radians(GAP/2); x1=500+R*math.sin(a); y1=500-R*math.cos(a); x0=1000-x1
    t=lambda x,y:(ox+x*scale, oy+y*scale)
    p0=t(x1,y1); p1=t(x0,y1); r=R*scale
    return (f'<path d="M{p0[0]:.2f} {p0[1]:.2f} A{r:.2f} {r:.2f} 0 1 1 {p1[0]:.2f} {p1[1]:.2f}" fill="none" stroke="{col}" stroke-width="{SW*scale:.2f}"/>'
            f'<circle cx="{ox+500*scale:.2f}" cy="{oy+DOTY*scale:.2f}" r="{DOTR*scale:.2f}" fill="{col}"/>')
def svg(w,h,body,bg=None):
    b=f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{body}</svg>'

def horizontal(col,sub_col=None,line1='DR. WOLF-DIETER-SCHÖNE',line2='STIFTUNG'):
    sub_col=sub_col or col
    m=200  # mark size
    s1=58; s2=58; tr1=0.10; tr2=0.42
    w1=width(line1,'semibold',s1,tr1); w2=width(line2,'light',s2,tr2)
    gapx=70; pad=40
    tx=pad+m+gapx; W=int(tx+max(w1,w2)+pad); H=m+2*pad
    # cap height of Inter ~0.727em; center two lines on mark
    ch=0.727*s1; lg=40; block=ch*2+lg; top=pad+(m-block)/2
    d1,_=text_path(line1,'semibold',s1,tx,top+ch,tr1); d2,_=text_path(line2,'light',s2,tx,top+2*ch+lg,tr2)
    body=mark_svg(pad,pad,m/1000,col)+f'<path d="{d1}" fill="{col}"/><path d="{d2}" fill="{sub_col}"/>'
    # divider rule
    return W,H,body
def stacked(col,sub_col=None,line1='DR. WOLF-DIETER-SCHÖNE',line2='STIFTUNG',tag=None):
    sub_col=sub_col or col
    m=360; s1=64; s2=52; tr1=0.10; tr2=0.5
    w1=width(line1,'semibold',s1,tr1); w2=width(line2,'light',s2,tr2)
    pad=60; W=int(max(w1,w2,m)+2*pad); y=pad
    body=mark_svg((W-m)/2,y,m/1000,col); y+=m+90
    d1,_=text_path(line1,'semibold',s1,(W-w1)/2,y+0.727*s1,tr1); y+=0.727*s1+44
    d2,_=text_path(line2,'light',s2,(W-w2)/2,y+0.727*s2,tr2); y+=0.727*s2
    body+=f'<path d="{d1}" fill="{col}"/><path d="{d2}" fill="{sub_col}"/>'
    if tag:
        y+=70; ts=40; wt=width(tag,'serifi',ts)
        dt,_=text_path(tag,'serifi',ts,(W-wt)/2,y+0.66*ts); y+=0.66*ts
        body+=f'<path d="{dt}" fill="{sub_col}"/>'
    return W,int(y+pad),body
