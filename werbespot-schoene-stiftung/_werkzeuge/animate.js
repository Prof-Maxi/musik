// usage: node animate.js layout.json bg outdir fps duration timeline.json
const {chromium}=require('playwright');const fs=require('fs');
const [L,bg,out,fps,dur,tl]=[JSON.parse(fs.readFileSync(process.argv[2])),process.argv[3],process.argv[4],+process.argv[5],+process.argv[6],JSON.parse(fs.readFileSync(process.argv[7]))];
fs.mkdirSync(out,{recursive:true});
const R=400,SW=58,GAP=56,DOTY=230,DOTR=62;const a=GAP/2*Math.PI/180;
const m=L.mark,s=m.s;const T=(x,y)=>[m.x+x*s,m.y+y*s];
const bot=T(500,900),rt=T(500+R*Math.sin(a),500-R*Math.cos(a)),lt=T(500-R*Math.sin(a),500-R*Math.cos(a)),r=R*s;
const arcLen=r*(Math.PI-a); // each half
const html=`<html><body style="margin:0;background:${bg}"><svg xmlns="http://www.w3.org/2000/svg" width="${L.W}" height="${L.H}" viewBox="0 0 ${L.W} ${L.H}">
<rect width="100%" height="100%" fill="${bg}"/><g id="all">
<path id="hr" d="M${bot} A${r} ${r} 0 0 0 ${rt}" fill="none" stroke="${L.col}" stroke-width="${SW*s}" stroke-dasharray="${arcLen} ${arcLen*2}"/>
<path id="hl" d="M${bot} A${r} ${r} 0 0 1 ${lt}" fill="none" stroke="${L.col}" stroke-width="${SW*s}" stroke-dasharray="${arcLen} ${arcLen*2}"/>
<circle id="dot" cx="${m.x+500*s}" cy="${m.y+DOTY*s}" r="${DOTR*s}" fill="${L.col}"/>
${L.items.map((it,i)=>`<path class="g-${it.g}" data-op="${it.op||1}" d="${it.d}" fill="${L.col}"/>`).join('')}
</g></svg></body></html>`;
const ease=t=>t<0?0:t>1?1:(t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2);
const easeOut=t=>t<0?0:t>1?1:1-Math.pow(1-t,3);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:L.W,height:L.H}});await p.setContent(html);
const N=Math.round(fps*dur);
for(let f=0;f<N;f++){const t=f/fps;
 const st={ring:ease((t-tl.ring[0])/(tl.ring[1])), dot:easeOut((t-tl.dot[0])/tl.dot[1]), groups:{}, fadeAll: tl.out? 1-ease((t-tl.out[0])/tl.out[1]) : 1};
 for(const [g,[t0,d]] of Object.entries(tl.groups)) st.groups[g]=easeOut((t-t0)/d);
 await p.evaluate(({st,arcLen,s})=>{
  for(const id of ['hr','hl']){const e=document.getElementById(id);e.setAttribute('stroke-dashoffset',arcLen*(1-st.ring));e.style.opacity=st.ring>0.001?1:0;}
  const d=document.getElementById('dot');d.style.opacity=st.dot;d.setAttribute('transform',`translate(0 ${-(1-st.dot)*90*s})`);
  document.querySelectorAll('[class^=g-]').forEach(e=>{const g=e.getAttribute('class').slice(2);const v=st.groups[g]??0;e.style.opacity=v*(+e.dataset.op);e.setAttribute('transform',`translate(0 ${(1-v)*10})`);});
  document.getElementById('all').style.opacity=st.fadeAll;
 },{st,arcLen,s});
 await p.screenshot({path:`${out}/f${String(f).padStart(5,'0')}.png`});}
await b.close();})();
