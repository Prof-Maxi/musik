import sys,json,math
sys.path.insert(0,'.')
from brand import *
def layout(col, W=1920,H=1080, cy=None, m=250, extra=()):
    """returns dict for animation: mark params and list of text items (path, color, group)"""
    L={'W':W,'H':H,'col':col}
    s1=46; tr1=0.10; s2=38; tr2=0.5
    l1='DR. WOLF-DIETER-SCHÖNE'; l2='STIFTUNG'
    w1=width(l1,'semibold',s1,tr1); w2=width(l2,'light',s2,tr2)
    y0=(cy if cy else 250)
    L['mark']=dict(x=(W-m)/2,y=y0,s=m/1000)
    y=y0+m+78
    items=[]
    d,_=text_path(l1,'semibold',s1,(W-w1)/2,y+0.727*s1,tr1); items.append(dict(d=d,g='wm')); y+=0.727*s1+32
    d,_=text_path(l2,'light',s2,(W-w2)/2,y+0.727*s2,tr2); items.append(dict(d=d,g='wm')); y+=0.727*s2+62
    for (txt,k,size,g,op) in extra:
        w=width(txt,k,size); asc=0.66*size if k.startswith('serif') else 0.727*size
        d,_=text_path(txt,k,size,(W-w)/2,y+asc); items.append(dict(d=d,g=g,op=op)); y+=asc+size*0.95
    L['items']=items
    return L
if __name__=='__main__':
    mode=sys.argv[1]; col=sys.argv[2]
    extra=[('Für Freiheit. Für Würde. Für Menschen.','serifi',40,'claim',1.0)] if mode=='logo' else []
    json.dump(layout(col,extra=extra,cy=280 if mode=='logo' else 250),open(sys.argv[3],'w'))
