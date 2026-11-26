#!/bin/bash
set -e
HK=hk/hk.mov; CF=spot/frames; CM=spot/music_campaign.wav; OUT=$1
T0=0.70; T1=136.08              # Musikeinsatz bis Ende des natürlichen Ausklangs
LEN=$(python3 -c "print(round($T1-$T0,3))")
VF_ST=$(python3 -c "print(round(130.93-$T0-1.5,3))")   # Bild blendet 1,5 s weich in das Schwarz des Originals
AF_ST=$(python3 -c "print(round($LEN-0.6,3))")          # nur letzte 0,6 s Sicherheitsblende auf den schon verklungenen Ton
GAP=0.8
ffmpeg -nostdin -v error -y -i $HK -framerate 30 -start_number 500 -i hk/bridge/n%04d.png -framerate 30 -i $CF/f%05d.png -i $CM -filter_complex "
[0:v]trim=start=$T0:end=$T1,setpts=PTS-STARTPTS,fps=30,scale=1868:1080:flags=lanczos:in_range=pc:out_range=tv,format=yuv420p,pad=1920:1080:26:0:black,setsar=1[base];
[1:v]format=yuv420p,setsar=1,setpts=PTS-STARTPTS[br];
[base]split[b1][b2];
[b1]trim=start_frame=0:end_frame=500,setpts=PTS-STARTPTS[p1];
[b2]trim=start_frame=612,setpts=PTS-STARTPTS[p2];
[p1][br][p2]concat=n=3:v=1:a=0,fade=t=out:st=$VF_ST:d=1.5,tpad=stop_mode=add:stop_duration=$GAP:color=black[hv];
[2:v]format=yuv420p,noise=c0s=3:c0f=t,setsar=1[cv];
[hv][cv]concat=n=2:v=1:a=0[v];
[0:a]atrim=start=$T0:end=$T1,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=3dB,afade=t=out:st=$AF_ST:d=0.6,apad=pad_dur=$GAP[ha];
[3:a]aformat=channel_layouts=stereo,volume=0.5dB[ca];
[ha][ca]concat=n=2:v=0:a=1,alimiter=limit=0.84:attack=2:release=60:level=false[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -maxrate 8M -bufsize 16M -profile:v high -level 4.1 -pix_fmt yuv420p \
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -r 30 -g 60 -c:a aac -b:a 320k -ar 48000 -movflags +faststart "$OUT"
