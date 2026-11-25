import numpy as np, json, subprocess
from scipy.signal import fftconvolve, butter, sosfilt
SR=48000; T=json.load(open('timeline.json')); S={int(k):v for k,v in T['start'].items()}; K=T['kw']; TOT=T['TOTAL']; LOGO=T['LOGO']
N=int(TOT*SR)+SR; L=np.zeros(N); Rr=np.zeros(N)
rng=np.random.default_rng(3)
A4=440; NOTE={n:i for i,n in enumerate(['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B'])}
def hz(n): name,o=n[:-1],int(n[-1]); return A4*2**((NOTE[name]+12*(o+1)-69)/12)
def pad_voice(f,dur):
    t=np.arange(int(dur*SR))/SR; y=np.zeros_like(t)
    for det in (-0.0023,0.0021):
        ph=rng.random()*6.28
        for n in range(1,10):
            y+= (1/n**1.9)*np.sin(2*np.pi*f*(1+det)*n*t+ph*n)
    y*=1+0.08*np.sin(2*np.pi*0.13*t+rng.random()*6)   # langsames Atmen
    return y
def env(n,a,r):
    e=np.ones(n); A=int(a*SR); R_=int(r*SR)
    e[:A]=np.sin(np.linspace(0,np.pi/2,A))**2; e[-R_:]*=np.cos(np.linspace(0,np.pi/2,R_))**2; return e
def add(sig,t0,gain,pan=0.0):
    i=int(t0*SR); n=min(len(sig),N-i); l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    L[i:i+n]+=sig[:n]*gain*l; Rr[i:i+n]+=sig[:n]*gain*r
def chord(notes,t0,t1,gain=0.05,a=2.2,r=2.6):
    dur=t1-t0+r
    for j,nn in enumerate(notes):
        f=hz(nn); y=pad_voice(f,dur); y*=env(len(y),a,r)
        add(y,t0,gain*(1.0 if f<300 else 0.75 if f<600 else 0.5),pan=[-0.35,0.3,-0.15,0.4,0][j%5])
def piano(nn,t0,vel=0.12,pan=0.0):
    f=hz(nn); dur=6.0; t=np.arange(int(dur*SR))/SR; y=np.zeros_like(t); B=0.0004
    tau=2.8*(261/f)**0.5
    for n in range(1,12):
        fn=f*n*np.sqrt(1+B*n*n)
        if fn>12000: break
        y+=(1/n**1.4)*np.exp(-t/(tau/(1+0.35*(n-1))))*np.sin(2*np.pi*fn*t)
    y*=1-np.exp(-t/0.004); add(y,t0,vel,pan)
# ---- Komposition ----
piano('D2',3.4,0.20); piano('D3',3.4,0.12); piano('A3',3.45,0.06)
chord(['D2','A2','F3','E4'],6.6,13.0,a=3.0)
chord(['Bb1','F2','D3','A3'],S[3]-0.2,S[4]-0.2)
chord(['G1','D2','Bb2','A3'],S[4]-0.2,S[5]-0.2)
chord(['A1','F2','C3','A3'],S[5]-0.2,S[6]-0.2)
chord(['F1','C2','A2','G3'],S[6]-0.2,S[7]-0.2)
chord(['Bb1','F2','D3','C4'],S[7]-0.2,K['s7_frei']-0.3)
chord(['F1','C2','A2','F3','E4'],K['s7_frei']-0.3,K['s7_wuerde']-0.3)
chord(['C2','G2','D3','F3'],K['s7_wuerde']-0.3,S[8]-0.3)
chord(['Bb1','F2','D3','A3'],S[8]-0.3,LOGO+0.4)
chord(['F1','C2','A2','E3','G3','C4'],LOGO+0.3,TOT+0.5,gain=0.055,a=2.6,r=3.2)
piano('A4',K['s2_traum']+0.1,0.05,0.3); piano('F4',S[4]-0.1,0.05,-0.3)
piano('C5',K['s6_grenzen']+0.3,0.045,0.35); piano('D5',K['s7_wuerde']+0.1,0.04,-0.2)
piano('A4',S[8]-0.05,0.05,0.2); piano('F3',LOGO+0.6,0.09,-0.1); piano('C4',LOGO+0.62,0.06,0.1)
piano('A4',LOGO+2.7,0.06,0.15); piano('E5',LOGO+5.4,0.035,-0.25); piano('G4',LOGO+8.3,0.035,0.25)
# ---- Raum (Hall) ----
ir_t=np.arange(int(4.2*SR))/SR
def ir(): x=rng.standard_normal(len(ir_t))*np.exp(-ir_t/0.85); return sosfilt(butter(2,5500,'lp',fs=SR,output='sos'),x)
irL,irR=ir(),ir(); irL/=np.sqrt((irL**2).sum()); irR/=np.sqrt((irR**2).sum())
wetL=fftconvolve(L,irL)[:N]; wetR=fftconvolve(Rr,irR)[:N]
mL=0.62*L+0.55*wetL; mR=0.62*Rr+0.55*wetR
sos=butter(2,[40,7000],'bp',fs=SR,output='sos'); mL=sosfilt(sos,mL); mR=sosfilt(sos,mR)
m=np.stack([mL,mR],1)[:int(TOT*SR)]
m[:int(3.35*SR)]=0
fo=int(0.7*SR); m[-fo:]*=np.cos(np.linspace(0,np.pi/2,fo))[:,None]**2
m/=np.abs(m).max()*1.12
import wave
def wav(p,x):
    x=np.clip(x,-1,1); b=(x*32767).astype('<i2').tobytes()
    with wave.open(p,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(b)
wav('music.wav',m)
# ---- Sprecher-Spur ----
v=np.zeros(int(TOT*SR))
for i in range(1,9):
    b=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',f'../tts/proc/s{i}.wav','-f','f64le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
    y=np.frombuffer(b,np.float64); a=int(S[i]*SR); v[a:a+len(y)]+=y
wav('vo.wav',np.stack([v,v],1)*0.9)
print('ok')
