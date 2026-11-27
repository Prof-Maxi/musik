#!/bin/bash
set -e
HK=hk/hk.mov; DOC=intl/doc_part.mp4; CF=spot/frames_v4; OUT=$1
NC=$(ls $CF | wc -l); NH=2591; NT=$((NH+NC))
AD=$(ffprobe -v error -select_streams a -show_entries stream=duration -of csv=p=0 $HK)
echo "Ton ${AD}s | Gesamt $NT Bilder | Doku $NH | Stiftung $NC"
ffmpeg -nostdin -v error -y -i $DOC -framerate 30 -i $CF/f%05d.png -i $HK -filter_complex "
[0:v]format=yuv420p,setsar=1,fade=t=out:st=$(python3 -c "print(round($NH/30-1.0,4))"):d=1.0[hv];
[1:v]format=yuv420p,noise=c0s=3:c0f=t,setsar=1[cv];
[hv][cv]concat=n=2:v=1:a=0,trim=end_frame=$NT[v];
[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=3dB,alimiter=limit=0.84:attack=2:release=60:level=false,apad=whole_dur=$(python3 -c "print($NT/30)")[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -maxrate 9M -bufsize 18M -profile:v high -level 4.1 -pix_fmt yuv420p \
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -r 30 -g 60 -c:a aac -b:a 320k -ar 48000 -movflags +faststart "$OUT"
