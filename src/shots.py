import asyncio
from playwright.async_api import async_playwright
B='http://localhost:8931/'; O='/workspace/site_shots/'
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await br.new_page(viewport={'width':1440,'height':900})
        async def go(u,name,scroll=None,sel=None,wait=2600):
            await pg.goto(B+u,wait_until='networkidle')
            if sel: await pg.locator(sel).first.scroll_into_view_if_needed(); await pg.evaluate("scrollBy(0,-90)")
            elif scroll: await pg.evaluate(f"scrollTo(0,{scroll})")
            await pg.wait_for_timeout(wait); await pg.screenshot(path=O+name)
        await go('index.html','01_home_hero.png',wait=3500)
        await go('index.html','02_home_schools.png',sel='#schools')
        await go('school/01-vedic.html','03_school_top.png',wait=2000)
        await go('school/01-vedic.html','04_school_callout.png',sel='.callout')
        await go('school/01-vedic.html','05_school_prophecy.png',sel='.prophecy h2')
        await go('school/01-vedic.html','06_school_gallery.png',sel='#g-being')
        await pg.locator('#g-being .zoom').first.click(); await pg.wait_for_timeout(1500); await pg.screenshot(path=O+'07_lightbox.png')
        await go('gallery.html','08_gallery.png')
        await go('timeline.html','09_timeline.png')
        await go('search.html?q=saturn%20return','10_search.png')
        m=await br.new_page(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=m
        await go('index.html','11_mobile_home.png',wait=3000)
        await go('school/27-yoruba-ifa.html','12_mobile_school.png',scroll=1400)
        await br.close()
asyncio.run(main())
