#!/bin/bash
# Werbespot v2: eine durchgehende Originaltonspur, Bild = gekürztes Hongkong-Bild + Stiftungssequenz (stumm)
set -e
HK=hk/hk.mov; CF=spot/frames; OUT=$1
NC=$(ls $CF | wc -l)                                   # Bilder der Stiftungssequenz (1492)
AD=$(ffprobe -v error -select_streams a -show_entries stream=duration -of csv=p=0 $HK)
NT=$(python3 -c "import math;print(math.ceil($AD*30-1e-6))")   # Gesamtbilder passend zur Tonspur
NH=$((NT-NC))                                          # Hongkong-Bilder
echo "Ton ${AD}s | Gesamt $NT Bilder | Hongkong $NH Bilder | Stiftung $NC Bilder"
FST=$(python3 -c "print(round($NH/30-1.0,4))")         # 1 s Abblende der Hongkong-Bilder ins Schwarz
ffmpeg -nostdin -v error -y -i $HK -framerate 30 -start_number 500 -i hk/bridge/n%04d.png -framerate 30 -i $CF/f%05d.png -filter_complex "
[0:v]fps=30,scale=1868:1080:flags=lanczos:in_range=pc:out_range=tv,format=yuv420p,pad=1920:1080:26:0:black,setsar=1,split[b1][b2];
[b1]trim=start_frame=0:end_frame=521,setpts=PTS-STARTPTS[p1];
[1:v]format=yuv420p,setsar=1,setpts=PTS-STARTPTS[br];
[b2]trim=start_frame=633:end_frame=$NH,setpts=PTS-STARTPTS[p2];
[p1][br][p2]concat=n=3:v=1:a=0,fade=t=out:st=$FST:d=1.0[hv];
[2:v]format=yuv420p,noise=c0s=3:c0f=t,setsar=1[cv];
[hv][cv]concat=n=2:v=1:a=0,trim=end_frame=$NT[v];
[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=3dB,alimiter=limit=0.84:attack=2:release=60:level=false,apad=whole_dur=$(python3 -c "print($NT/30)")[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -maxrate 8M -bufsize 16M -profile:v high -level 4.1 -pix_fmt yuv420p \
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -r 30 -g 60 -c:a aac -b:a 320k -ar 48000 -movflags +faststart "$OUT"
