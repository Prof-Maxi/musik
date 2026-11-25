import json
F='/tmp/claude-0/-home-user/6281bc19-abf7-5120-8af0-6085bfbd0df3/scratchpad/fonts/'
T=json.load(open('timeline.json')); L=json.load(open('logo_layout.json'))
html=open('spot_template.html').read().replace('__T__',json.dumps(T)).replace('__L__',json.dumps(L)).replace('__F__',F)
open('spot.html','w').write(html)
