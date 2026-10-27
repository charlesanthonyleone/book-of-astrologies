import asyncio,re,glob,os,sys
from playwright.async_api import async_playwright
B='http://localhost:8931/'
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await br.new_page(viewport={'width':1440,'height':900})
        errs=[]; pg.on('console',lambda m: m.type=='error' and errs.append(m.text)); pg.on('pageerror',lambda e: errs.append(str(e)))
        bad=0
        pages=['index.html','gallery.html','search.html','timeline.html']+['school/'+os.path.basename(f) for f in sorted(glob.glob('school/*.html'))]
        for u in pages:
            r=await pg.goto(B+u,wait_until='load'); 
            await pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
            await pg.wait_for_load_state('networkidle')
            await pg.wait_for_timeout(300)
            b=await pg.evaluate("[...document.querySelectorAll('img')].filter(i=>i.getAttribute('src')&&(!i.complete||i.naturalWidth==0)).map(i=>i.src)")
            n=await pg.evaluate("document.querySelectorAll('img').length")
            print(r.status,u,'imgs',n,'broken',len(b),b[:2]); bad+=len(b)
        print('TOTAL BROKEN',bad,'ERRORS',errs[:5])
        await br.close()
asyncio.run(main())
