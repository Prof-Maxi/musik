#!/usr/bin/env bash
# Baut die ZDF-Testsequenz: Motion Design (Canvas → Playwright-Frames), Tonmischung, H.264-Encoding.
set -euo pipefail
P=$(cd "$(dirname "$0")/../.." && pwd)
W=$P/_werkzeuge/test; R=$P/_render/test; SRC=$P/02_higgsfield/test
mkdir -p $R/frames $R/audio $P/05_final

# ---- Timeline (Sekunden) ----
VO1_T=0.90; A_END=4.30; VO2_T=4.75; DROP=6.45
CARD_IN=10.00; FOOT=11.55; LOGO_IN=12.85; TOTAL=15.20
cat > $R/timeline.json <<EOF
{"porsche_dir":"file://$R/porsche","porsche_frames":$(ls $R/porsche | wc -l),
 "vo1_t":$VO1_T,"a_end":$A_END,"drop":$DROP,"card_in":$CARD_IN,"footnote":$FOOT,"logo_in":$LOGO_IN,"total":$TOTAL,
 "vo1_words":[{"w":"Geld","s":0.0},{"w":"allein","s":0.30},{"w":"macht","s":0.68},{"w":"nicht","s":1.08},{"w":"glücklich.","s":1.38}]}
EOF
python3 - "$W/test_cd_template.html" "$R/timeline.json" "$R/page.html" <<'EOF'
import sys;import os;cd='file://'+os.path.abspath(os.path.dirname(sys.argv[1])+'/../../01_corporate-design');t=open(sys.argv[1]).read().replace('__TIMELINE__',open(sys.argv[2]).read()).replace('__CD__',cd);open(sys.argv[3],'w').write(t)
EOF

# ---- Frames ----
if [ "${SKIP_FRAMES:-0}" != 1 ]; then
rm -f $R/frames/*.png
node -e "
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://$R/page.html');await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>window.READY);
await p.evaluate(async()=>{for(const f of ['500 40px LS','600 40px LS','700 40px LS','800 40px LS','400 40px IN','500 40px IN'])await document.fonts.load(f)});
const N=Math.round($TOTAL*30);
for(let f=0;f<N;f++){await p.evaluate(t=>render(t),f/30);await p.screenshot({path:'$R/frames/f'+String(f).padStart(5,'0')+'.png'});}
await b.close();console.log('frames',N);})();"
fi

# ---- Ton ----
A=$R/audio
# Sprecher: etwas tiefer (Formanten erhalten), Wärme, Präsenz, Kompression
ffmpeg -v error -y -i $SRC/vo_A_sterling.mp3 -af "aresample=48000,rubberband=pitch=0.915:formant=preserved,highpass=f=70,equalizer=f=130:t=q:w=1:g=2.5,equalizer=f=3200:t=q:w=1.2:g=1.5,equalizer=f=7000:t=q:w=2:g=-1.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3dB" $A/vo_proc.wav
ffmpeg -v error -y -i $A/vo_proc.wav -af "atrim=0:2.25,asetpts=PTS-STARTPTS,afade=t=out:st=2.15:d=0.1" $A/vo1.wav
ffmpeg -v error -y -i $A/vo_proc.wav -af "atrim=2.30:3.95,asetpts=PTS-STARTPTS,afade=t=in:d=0.03" $A/vo2.wav
# Musik: ernster Teil 0–4.3 s, dann der Drop ab dem großen Aufschlag (Quelle 8.20 s)
ffmpeg -v error -y -i $SRC/musik_test.mp3 -af "aresample=48000,atrim=0:$A_END,asetpts=PTS-STARTPTS,afade=t=in:d=0.4,afade=t=out:st=$(echo "$A_END-0.28"|bc):d=0.28" $A/mus_a.wav
ffmpeg -v error -y -i $SRC/musik_test.mp3 -af "aresample=48000,atrim=8.20:16,asetpts=PTS-STARTPTS" $A/mus_drop.wav
ffmpeg -v error -y -i $SRC/musik_test.mp3 -af "aresample=48000,atrim=8.20:11.5,asetpts=PTS-STARTPTS,afade=t=out:st=2.3:d=1.0" $A/mus_logo.wav
ms(){ python3 -c "print(int(round(($1)*1000)))"; }
ffmpeg -v error -y \
 -i $A/mus_a.wav -i $A/vo1.wav -i $A/vo2.wav -i $A/mus_drop.wav -i $SRC/sfx/engine_boxer_pass.mp3 \
 -i $SRC/sfx/whoosh_airy.mp3 -i $A/mus_logo.wav -i $SRC/sfx/whoosh_big.mp3 -filter_complex "
 [0]volume=-7dB[ma];
 [1]adelay=$(ms $VO1_T)|$(ms $VO1_T)[v1];
 [2]adelay=$(ms $VO2_T)|$(ms $VO2_T)[v2];
 [3]volume=-4dB,adelay=$(ms "$DROP-0.12")|$(ms "$DROP-0.12")[md];
 [4]aresample=48000,atrim=2.7:9.6,asetpts=PTS-STARTPTS,highpass=f=40,volume=-3dB,afade=t=in:d=0.25,afade=t=out:st=4.6:d=1.4,adelay=$(ms "$DROP-0.35")|$(ms "$DROP-0.35")[en];
 [5]aresample=48000,volume=-6dB,adelay=$(ms "$CARD_IN-1.05")|$(ms "$CARD_IN-1.05")[w1];
 [6]volume=-6dB,adelay=$(ms "$LOGO_IN+0.05")|$(ms "$LOGO_IN+0.05")[ml];
 [7]aresample=48000,volume=-5dB,adelay=$(ms "$LOGO_IN-0.45")|$(ms "$LOGO_IN-0.45")[w2];
 [v1][v2]amix=inputs=2:normalize=0,apad=whole_dur=$TOTAL[vo];
 [vo]asplit=2[vo_a][vo_b];
 [ma][md][en][w1][ml][w2]amix=inputs=6:normalize=0,apad=whole_dur=$TOTAL[bed];
 [bed][vo_a]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=300[bedd];
 [bedd][vo_b]amix=inputs=2:normalize=0,atrim=0:$TOTAL,afade=t=out:st=$(echo "$TOTAL-0.4"|bc):d=0.4,
 loudnorm=I=-16:TP=-1.5:LRA=11[out]" -map "[out]" -ar 48000 -ac 2 $A/mix.wav

# ---- Encoding: Frames + leichtes Filmkorn + Ton ----
ffmpeg -v error -y -framerate 30 -i $R/frames/f%05d.png -i $A/mix.wav \
 -vf "noise=alls=3:allf=t,format=yuv420p" -c:v libx264 -profile:v high -preset slow -tune film -crf 20 -maxrate 16M -bufsize 32M -r 30 \
 -c:a aac -b:a 320k -ar 48000 -movflags +faststart -shortest $P/05_final/ZDF_Testsequenz_1080p30.mp4
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact $P/05_final/ZDF_Testsequenz_1080p30.mp4
