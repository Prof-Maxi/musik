const {chromium}=require('playwright');
(async()=>{const times=process.argv.slice(3).map(Number);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.addInitScript(()=>{window.__RENDER__=true});await p.goto('file://'+require('path').resolve(process.argv[2]));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
for(const t of times){await p.evaluate(t=>render(t),t);await p.screenshot({path:`st_${t.toFixed(2)}.png`});}await b.close();})();
