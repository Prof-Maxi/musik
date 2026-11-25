const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const dir=process.argv[2];const sizes=JSON.parse(fs.readFileSync(dir+'/_sizes.json'));
const b=await chromium.launch();const p=await b.newPage();
for(const [n,[w,h]] of Object.entries(sizes)){const sc=Math.max(1,Math.round(3000/w*100)/100);
await p.setViewportSize({width:Math.ceil(w),height:Math.ceil(h)});
await p.setContent(`<html><body style="margin:0;background:transparent">${fs.readFileSync(dir+'/'+n+'.svg','utf8')}</body></html>`);
const pp=await b.newPage({deviceScaleFactor:sc,viewport:{width:Math.ceil(w),height:Math.ceil(h)}});
await pp.setContent(`<html><body style="margin:0;background:transparent">${fs.readFileSync(dir+'/'+n+'.svg','utf8')}</body></html>`);
await pp.screenshot({path:dir+'/'+n+'.png',omitBackground:true,clip:{x:0,y:0,width:w,height:h}});await pp.close();}
await b.close();})();
