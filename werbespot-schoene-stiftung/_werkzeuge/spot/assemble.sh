#!/bin/bash
# usage: assemble.sh <hongkong-video> <output.mp4>
set -e
HK="$1"; OUT="$2"; D=$(dirname "$0")
VF=3.0   # Bild-Abblende ins Schwarz (s)
AF=4.0   # Ausklingen der Musik (s)
GAP=0.8  # zusätzliches Schwarz; zusammen mit dem Schwarz am Kampagnenbeginn = ca. 2 s absolute Stille vor dem ersten Titel
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$HK")
I=$(ffmpeg -nostdin -i "$HK" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-16.0-($I),2))")
echo "Hongkong: ${DUR}s, ${I} LUFS -> Gain ${G} dB"
VS=$(python3 -c "print($DUR-$VF)"); AS=$(python3 -c "print($DUR-$AF)")
ffmpeg -nostdin -v error -y -i "$HK" -framerate 30 -i "$D/frames/f%05d.png" -i "$D/music_campaign.wav" -filter_complex "
[0:v]scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30,format=yuv420p,fade=t=out:st=$VS:d=$VF,tpad=stop_mode=add:stop_duration=$GAP:color=black[hv];
[1:v]format=yuv420p,noise=c0s=3:c0f=t,setsar=1[cv];
[hv][cv]concat=n=2:v=1:a=0[v];
[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=${G}dB,afade=t=out:st=$AS:d=$AF:curve=qsin,apad=pad_dur=$GAP[ha];
[2:a]aformat=channel_layouts=stereo[ca];
[ha][ca]concat=n=2:v=0:a=1,alimiter=limit=0.84:attack=2:release=60:level=false[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 17 -maxrate 14M -bufsize 28M -profile:v high -level 4.1 -pix_fmt yuv420p \
 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 30 -g 60 -c:a aac -b:a 320k -ar 48000 -movflags +faststart "$OUT"
