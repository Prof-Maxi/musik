import subprocess,numpy as np,re,sys
from PIL import Image
from scipy.ndimage import binary_dilation
W,H=1024,592; FS=W*H
def grab(t):
    b=subprocess.run(['ffmpeg','-nostdin','-v','error','-i','hk.mov','-fps_mode','passthrough','-vf',f"select='gte(t\\,{t})',scale={W}:{H},format=gray",'-frames:v','1','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(H,W).astype(int)
a=grab(19.5); b=grab(20.78)
mask=(a>165)&(b>165)
zone=np.zeros((H,W),bool); zone[:int(H*.12)]=1; zone[int(H*.74):]=1; zone[int(H*.4):int(H*.6),int(W*.25):int(W*.75)]=1
mask&=zone
ring=binary_dilation(mask,iterations=4)&~binary_dilation(mask,iterations=1)
Image.fromarray((mask*255).astype(np.uint8)).save('uimask.png')
mi=np.flatnonzero(mask); ri=np.flatnonzero(ring)
p=subprocess.Popen(['ffmpeg','-nostdin','-i','hk.mov','-fps_mode','passthrough','-vf',f'scale={W}:{H},format=gray,showinfo','-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE,stderr=open('scan_info.txt','w'))
sc=[]
while True:
    buf=p.stdout.read(FS)
    if len(buf)<FS: break
    f=np.frombuffer(buf,np.uint8)
    sc.append(f[mi].mean()-f[ri].mean())
p.wait()
ts=np.array([float(x) for x in re.findall(r'pts_time:\s*([0-9.]+)',open('scan_info.txt').read())])[:len(sc)]
sc=np.array(sc); np.save('uiscore.npy',np.stack([ts,sc],1))
print('mask',len(mi),'frames',len(sc))
