import json,sys
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
import subprocess,numpy as np
def load(p):
    b=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',p,'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout
    return np.frombuffer(b,np.float32)
out={}
for i in range(1,9):
    segs,_=m.transcribe(load(f'proc/s{i}.wav'),language='de',word_timestamps=True,beam_size=5)
    words=[dict(w=w.word.strip(),s=round(w.start,3),e=round(w.end,3)) for s in segs for w in s.words]
    out[i]=words; print(i,' '.join(w['w'] for w in words))
json.dump(out,open('words.json','w'),ensure_ascii=False,indent=0)
