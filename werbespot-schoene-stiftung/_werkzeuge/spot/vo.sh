set -e
LS=${1:-1.24}; PITCH=${2:-0.944}
rm -rf raw proc; mkdir raw proc
mapfile -t L < lines.txt
for i in "${!L[@]}"; do n=$((i+1))
 echo "${L[$i]}" | python3 -m piper -m de_DE-thorsten-high.onnx --length-scale $LS --noise-scale 0.55 --noise-w-scale 0.6 -f raw/s$n.wav 2>/dev/null
 ffmpeg -nostdin -v error -y -i raw/s$n.wav -af "aresample=48000,rubberband=pitch=$PITCH:formant=preserved:pitchq=quality,highpass=f=65,equalizer=f=170:t=q:w=0.9:g=2.5,equalizer=f=420:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1.5:g=1.2,deesser=i=0.35,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse" -c:a pcm_s24le proc/s$n.wav
 printf "s$n %.2f\n" $(ffprobe -v error -show_entries format=duration -of csv=p=0 proc/s$n.wav)
done
