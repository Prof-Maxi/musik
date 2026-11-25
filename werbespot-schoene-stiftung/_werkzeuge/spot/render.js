const {chromium}=require('playwright');const fs=require('fs');
const [page_,out,fps,from,to]=[process.argv[2],process.argv[3],+process.argv[4],+(process.argv[5]||0),process.argv[6]];
fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.addInitScript(()=>{window.__RENDER__=true});
await p.goto('file://'+require('path').resolve(page_));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const T=await p.evaluate(()=>T.TOTAL);const N=Math.round((to?+to:T)*fps);
for(let f=Math.round(from*fps);f<N;f++){await p.evaluate(t=>render(t),f/fps);await p.screenshot({path:`${out}/f${String(f).padStart(5,'0')}.png`});}
await b.close();console.log('frames',N);})();
