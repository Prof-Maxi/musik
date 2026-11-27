# Schnittautomat: EDL -> Dokumentarteil (2591 Bilder, 30 fps, 1920x1080), einheitliche Farbkorrektur
import json,subprocess,sys,os
EDL=json.load(open(sys.argv[1])); OUT=sys.argv[2]; FPS=30; TOTAL=2591
GRADE="eq=contrast=1.05:saturation=0.80:gamma=0.98,colorbalance=rs=-0.015:bs=0.025:rh=0.01,vignette=angle=PI/6"
args=['ffmpeg','-nostdin','-v','error','-y']; fl=[]; labels=[]
t_prev=0
for i,s in enumerate(EDL):
    f0=round(s['t0']*FPS); f1=round(s['t1']*FPS) if i<len(EDL)-1 else TOTAL
    n=f1-f0; assert n>0,(i,s)
    if abs(f0-t_prev)>0: raise SystemExit(f'Lücke vor Shot {i}: {t_prev} vs {f0}')
    t_prev=f1
    args+=['-ss',str(max(0,s['in']-1.0)),'-t',str(n/FPS+2.5),'-i',s['src']]
    rng='in_range=pc:out_range=tv:' if s.get('full_range') else ''
    off=s['in']-max(0,s['in']-1.0)
    sp=s.get('speed',1.0)
    fl.append(f"[{i}:v]trim=start={off:.4f},setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos:{rng.rstrip(':')},crop=1920:1080,setsar=1,format=yuv420p,{GRADE},trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]".replace(':,',','))
    labels.append(f'[v{i}]')
fl.append(''.join(labels)+f'concat=n={len(labels)}:v=1:a=0,fade=t=in:st=0:d=0.01[v]')
args+=['-filter_complex',';'.join(fl),'-map','[v]','-c:v','libx264','-preset','medium','-crf','14','-pix_fmt','yuv420p','-r',str(FPS),OUT]
subprocess.run(args,check=True)
n=subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',OUT],capture_output=True,text=True).stdout.strip()
print('Bilder:',n,'Soll:',TOTAL)
