import json
W=json.load(open('words.json')); dur={}
import subprocess
for i in range(1,9):
    dur[i]=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'../tts/proc/s{i}.wav']))
VO0=7.2
gaps=[0,0.8,0.95,0.95,0.55,0.55,1.05,0.95]   # pause before sentence i (i>=2)
t=VO0; start={}
for i in range(1,9):
    if i>1: t+=gaps[i-1]
    start[i]=round(t,3); t+=dur[i]
vo_end=t
LOGO=round(vo_end+0.55+1.0,3)   # visuals fade, then black, then logo
TOTAL=round(LOGO+12.0,3)
def w(i,word,n=0):
    hits=[x for x in W[str(i)] if word.lower() in x['w'].lower()]
    return round(start[i]+hits[n]['s'],3)
T=dict(start=start,dur=dur,vo_end=round(vo_end,3),LOGO=LOGO,TOTAL=TOTAL,
 kw={'s2_viele':w(2,'viele'),'s2_uner':w(2,'unerf'),'s2_traum':w(2,'Traum'),
     's3_kaempfen':w(3,'kämpfen'),'s3_rechte':w(3,'Rechte'),
     's4_wuerde':w(4,'Menschenwürde'),'s4_nicht':w(4,'nicht'),
     's5_frei':w(5,'Freiheit'),'s5_kein':w(5,'kein'),
     's6_hoff':w(6,'Hoffnung'),'s6_grenzen':w(6,'Grenzen'),
     's7_doktor':w(7,'Doktor'),'s7_welt':w(7,'Welt'),'s7_frei':w(7,'frei'),'s7_sicher':w(7,'sicher'),'s7_wuerde':w(7,'Würde'),
     's8_gem':w(8,'Gemeinsam'),'s8_koennen':w(8,'können'),'s8_veraendern':w(8,'verändern')})
json.dump(T,open('timeline.json','w'),indent=1)
print(json.dumps(T,indent=1))
