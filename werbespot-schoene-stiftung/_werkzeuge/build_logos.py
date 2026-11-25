import os,sys
sys.path.insert(0,'.')
from brand import *
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
files={}
def save(name,W,H,body,bg=None):
    open(f'{out}/{name}.svg','w').write(svg(W,H,body,bg)); files[name]=(W,H)
for nm,col,bg in [('navy',NAVY,None),('schwarz',BLACK,None),('weiss',WHITE,None)]:
    save(f'bildzeichen_{nm}_transparent',1000,1000,mark_svg(0,0,1,col))
    W,H,b=horizontal(col); save(f'wortbildmarke_horizontal_{nm}_transparent',W,H,b)
    W,H,b=stacked(col); save(f'wortbildmarke_gestapelt_{nm}_transparent',W,H,b)
    W,H,b=horizontal(col,line1='DR. WOLF DIETER SCHÖNE',line2='FOUNDATION'); save(f'wortbildmarke_international_{nm}_transparent',W,H,b)
W,H,b=horizontal(WHITE); save('wortbildmarke_horizontal_auf_nachtblau',W,H,b,NAVY)
W,H,b=horizontal(NAVY); save('wortbildmarke_horizontal_auf_weiss',W,H,b,WHITE)
W,H,b=horizontal(WHITE); save('wortbildmarke_horizontal_auf_schwarz',W,H,b,BLACK)
W,H,b=stacked(WHITE,tag='Für Freiheit. Für Würde. Für Menschen.'); save('wortbildmarke_gestapelt_claim_auf_nachtblau',W,H,b,NAVY)
W,H,b=stacked(NAVY,tag='Für Freiheit. Für Würde. Für Menschen.'); save('wortbildmarke_gestapelt_claim_auf_papier',W,H,b,PAPER)
import json; json.dump(files,open(f'{out}/_sizes.json','w'))
