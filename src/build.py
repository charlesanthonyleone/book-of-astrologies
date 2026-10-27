import re, os, json, html, glob, unicodedata
import markdown
from PIL import Image
SRC='/workspace/book_of_astrologies/'; D=SRC+'deep/'; OUT='docs/'
SCHOOLS=["Vedic","Hellenistic","Hebrew","Persian-Arabic","Babylonian","Egyptian","Zoroastrian","Tibetan","Chinese","Buddhist","Mesoamerican","Manichaean","Gnostic-Mandaean","Medieval-Renaissance","Hermetic / Picatrix","Rosicrucian","Golden Dawn","Thelema","Theosophy","Celtic-Norse","Tarot-Qabalah","Uranian","Modern Psychological","Western Sidereal","Jain","Sikh-Punjabi","Yoruba Ifá","Polynesian-Indigenous"]
def slugify(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')[:60] or 'x'
def imgname(p): return os.path.splitext(p[len(D):])[0].replace('/','__')+'.webp'
def human(p):
    b=os.path.splitext(os.path.basename(p))[0]; b=re.sub(r'^\d+_(?:art|chart|img|plate|g|p|c|d|body|being)?_?\d*[a-z]?_?','',b)
    b=b.replace('_',' ').strip(); return (b[:1].upper()+b[1:]) if b else 'Image'
def fixalt(a,p):
    return '' if re.search(r'\.(png|jpe?g)$',a.strip(),re.I) else a
def esc(s): return html.escape(s,quote=True)
def inline_md(s):
    h=markdown.markdown(re.sub(r'^(\d+)\.(\s)',r'\1\\.\2',s)); return re.sub(r'^<p>|</p>$','',h.strip())
def strip_md(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s); s=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',s)
    s=re.sub(r'[*_`#>]+','',s); s=s.replace('|',' · ')
    return re.sub(r'\s+',' ',s).strip(' ·')
SYMB=re.compile(r'symbolic|melothesia|purusha|microcosm|adam kadmon|zodiac man|homo signorum|body',re.I)
MON=r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
DATE=re.compile(r'\b(?:(\d{1,2})\s+)?('+MON+r')\.?\s+(?:(\d{1,2}),?\s+)?(20(?:2[6-9]|3[0-5]))\b|\b(20(?:2[6-9]|3[0-5]))-([01]\d)(?:-([0-3]\d))?\b')
MI={m:i+1 for i,m in enumerate(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])}
LABEL=re.compile(r'\[(Calculated|Calc|Source|Interpretation|Interp)([^\]<>\[]{0,90})\]')
def labelize(h):
    def r(m):
        k=m.group(1).lower(); k={'calc':'calculated','interp':'interpretation'}.get(k,k)
        if k=='source' and re.search(r'verif',m.group(2),re.I) and not re.search(r'verified',m.group(2),re.I): k='verify'
        return f'<span class="lbl lbl-{k}">{m.group(1)}{m.group(2)}</span>'
    h=re.sub(r'<strong>\s*(\[(?:Calculated|Calc|Source|Interpretation|Interp)[^\]<]{0,90}\])\s*</strong>',r'\1',h)
    return LABEL.sub(r,h)
def calloutize(h):
    def r(m):
        body=m.group(0)
        txt=re.sub('<[^>]+>','',body)[:160]
        if re.search(r'What this means for you',txt,re.I): return '<div class="callout">'+body+'</div>'
        if re.search(r'^\s*(?:\[[^\]]*\]\s*)?(?:Section )?synthesis\b',txt,re.I): return '<div class="callout callout-syn">'+body+'</div>'
        return body
    return re.sub(r'<p>.*?</p>',r,h,flags=re.S)
TPL=open('src/page.html').read()
def page(title,body,depth,active='',desc=''):
    pre='../'*depth
    return TPL.replace('{{title}}',esc(title)).replace('{{pre}}',pre).replace('{{body}}',body).replace('{{desc}}',esc(desc or "Charles Leone's Book of Astrologies: 28 schools, one sky.")).replace(f'data-nav="{active}"',f'data-nav="{active}" aria-current="page"')
chapters=[]; allimgs=[]; timeline=[]; search=[]
for n in range(1,29):
    raw=re.sub(r'\]\((?:\.\./|\./)?deep/','](/workspace/book_of_astrologies/deep/',open(f'{SRC}ch/{n:02d}.md').read()); lines=raw.split('\n')
    title=next((l[2:].strip() for l in lines if l.startswith('# ')),'Uranian Astrology: the Hamburg School')
    title=re.sub(r'^Chapter \d+\s*[—:-]\s*','',title)
    slug=f'{n:02d}-{slugify(SCHOOLS[n-1])}'
    # split into h2 sections
    secs=[]; cur={'h':None,'lines':[]}
    for l in lines:
        if l.startswith('# ') : continue
        if l.startswith('## '): secs.append(cur); cur={'h':l[3:].strip(),'lines':[]}
        else: cur['lines'].append(l)
    secs.append(cur)
    imgs={}; order=[]; shown=set(); used_ids=set(); toc=[]; html_parts=[]; gallery_inserted=False
    def uid(s):
        b=slugify(s); i=b; k=2
        while i in used_ids: i=f'{b}-{k}'; k+=1
        used_ids.add(i); return i
    for si,sec in enumerate(secs):
        h=sec['h']; gz=bool(h and re.search(r'gallery|astrological being',h,re.I))
        proph=bool(h and re.search(r'prophec|kalki test|awaited figure',h,re.I) and not re.search(r'who am i',h,re.I))
        sid=uid(re.sub(r'\[[^\]]*\]','',h)) if h else 'intro'
        out=[]; sub=h or ''; subid=sid; cur_h3=''; L=sec['lines']; i=0
        h3s=[]
        while i<len(L):
            l=L[i]
            m=re.match(r'^\s*!\[((?:[^\[\]]|\[[^\]]*\])*)\]\((/workspace/book_of_astrologies/deep/[^)]+)\)\s*$',l)
            if l.startswith('### ') or l.startswith('#### '):
                lvl=3 if l.startswith('### ') else 4; t=l.lstrip('#').strip(); cur_h3=t; hid=uid(re.sub(r'\[[^\]]*\]','',t))
                if lvl==3: h3s.append((hid,t))
                out.append(f'\n<h{lvl} id="{hid}">{labelize(inline_md(t))}</h{lvl}>\n'); subid=hid; i+=1; continue
            if m:
                alt,p=m.group(1),m.group(2); alt=fixalt(alt,p); cap=alt or human(p)
                j=i+1
                while j<len(L) and not L[j].strip(): j+=1
                if j<len(L) and re.match(r'^\*[^*].*\*\s*$',L[j].strip()):
                    c=L[j].strip()[1:-1].strip()
                    if c: cap=c
                    if j<len(L): L=L[:j]+L[j+1:]
                if p not in imgs:
                    ctx=' '.join([alt,cap,cur_h3 if gz else ''])
                    typ='symbolic' if SYMB.search(ctx) else ('artwork' if p.lower().endswith(('.jpg','.jpeg')) else 'chart')
                    w,hh=Image.open(OUT+'img/full/'+imgname(p)).size
                    rec={'f':imgname(p),'cap':cap,'school':n,'type':typ,'sec':subid,'w':w,'h':hh}
                    imgs[p]=rec; order.append(p)
                if not gz and p not in shown:
                    shown.add(p); r=imgs[p]
                    out.append(f'\n<figure class="fig reveal"><button class="zoom" data-f="{r["f"]}" aria-label="Enlarge: {esc(r["cap"])}"><img src="../img/thumb/{r["f"]}" data-full="../img/full/{r["f"]}" alt="{esc(alt)}" width="{r["w"]}" height="{r["h"]}" loading="lazy" decoding="async"></button><figcaption>{esc(r["cap"])}</figcaption></figure>\n')
                i+=1; continue
            if '](/workspace/book_of_astrologies/deep/' in l:
                rest=strip_md(re.sub(r'!\[(?:[^\[\]]|\[[^\]]*\])*\]\([^)]*\)','',l)); rest=re.sub(r'^\d+\.\s*','',rest)
                def rep(mm):
                    alt,p=mm.group(1),mm.group(2); alt=fixalt(alt,p)
                    cap=alt if len(alt)>14 else (rest[:240]+('…' if len(rest)>240 else '') if rest else alt or human(p))
                    if p not in imgs:
                        ctx=' '.join([alt,cap,cur_h3 if gz else ''])
                        typ='symbolic' if SYMB.search(ctx) else ('artwork' if p.lower().endswith(('.jpg','.jpeg')) else 'chart')
                        w,hh=Image.open(OUT+'img/full/'+imgname(p)).size
                        imgs[p]={'f':imgname(p),'cap':cap,'school':n,'type':typ,'sec':subid,'w':w,'h':hh}; order.append(p)
                    if gz or p in shown: return ''
                    shown.add(p); r=imgs[p]
                    return f'<button class="zoom ifig" data-f="{r["f"]}" aria-label="Enlarge: {esc(r["cap"])}"><img src="../img/thumb/{r["f"]}" alt="{esc(alt or r["cap"])}" loading="lazy" decoding="async"></button>'
                l=re.sub(r'!\[((?:[^\[\]]|\[[^\]]*\])*)\]\((/workspace/book_of_astrologies/deep/[^)]+)\)',rep,l)
            # timeline
            if l.strip() and not l.strip().startswith('|---'):
                for sent in re.split(r'(?<=[.;!?])\s+(?=[A-Z(\[*])',l) if not l.strip().startswith('|') else [l]:
                    for dm in DATE.finditer(sent):
                        if dm.group(4): y=int(dm.group(4)); mo=MI[dm.group(2)[:3].lower()]; d=int(dm.group(1) or dm.group(3) or 0)
                        else: y=int(dm.group(5)); mo=int(dm.group(6)); d=int(dm.group(7) or 0)
                        if not 1<=mo<=12 or d>31: continue
                        t=strip_md(sent)
                        if len(t)>360:
                            k=max(0,t.find(dm.group(0))-160); t=('… ' if k else '')+t[k:k+340]+' …'
                        timeline.append({'y':y,'m':mo,'d':d,'ds':dm.group(0),'school':n,'sec':subid,'t':t,'h':strip_md(re.sub(r'\[[^\]]*\]','',sub if not cur_h3 else cur_h3))})
            out.append(l); i+=1
        md='\n'.join(out)
        body=markdown.markdown(md,extensions=['tables','sane_lists'])
        body=re.sub(r'<table>',r'<div class="table-wrap"><table>',body).replace('</table>','</table></div>')
        body=calloutize(labelize(body))
        txt=re.sub(r'<[^>]+>',' ',body); txt=html.unescape(re.sub(r'\s+',' ',txt)).strip()
        if txt: search.append({'s':n,'id':sid,'h':strip_md(re.sub(r'\[[^\]]*\]','',h or 'Introduction')),'t':txt})
        cls='sec'+(' prophecy' if proph else '')+(' gal-sec' if gz else '')
        head=''
        if h:
            head=f'<h2 id="{sid}" class="reveal">{labelize(inline_md(h))}</h2>'
            if proph: head='<div class="proph-badge">Prophecy markers</div>'+head
        gal=''
        if gz and not gallery_inserted:
            gallery_inserted=True; gal='%%GALLERIES%%'
        if h: toc.append((sid,re.sub(r'\s*\[[^\]]*\]','',h),h3s,proph,gz))
        html_parts.append(f'<section class="{cls}" aria-labelledby="{sid}">{head}{gal}{body}</section>' if h else f'<section class="sec intro">{body}</section>')
    recs=[imgs[p] for p in order]; allimgs+=recs
    charts=[r for r in recs if r['type']=='chart']; being=[r for r in recs if r['type']!='chart']
    def grid(rs,gid,label):
        if not rs: return ''
        items=''.join(f'<li class="reveal"><button class="zoom" data-f="{r["f"]}" aria-label="Open: {esc(r["cap"])}"><img src="../img/thumb/{r["f"]}" alt="{esc(r["cap"])}" loading="lazy" decoding="async"></button>{"<span class=tag>Symbolic body</span>" if r["type"]=="symbolic" else ""}</li>' for r in rs)
        return f'<div class="gallery" id="{gid}"><div class="gal-head"><h3>{label}</h3><span class="count">{len(rs)}</span></div><ul class="gal-grid" data-gallery="{gid}">{items}</ul></div>'
    gals=grid(charts,'g-charts','Charts')+grid(being,'g-being','Your Astrological Being')
    bodyhtml=''.join(html_parts)
    if '%%GALLERIES%%' in bodyhtml: bodyhtml=bodyhtml.replace('%%GALLERIES%%',gals,1)
    else:
        bodyhtml+=f'<section class="sec gal-sec"><h2 id="galleries">Galleries</h2>{gals}</section>'; toc.append(('galleries','Galleries',[],False,True))
    arts=[r for r in recs if r['type']=='artwork']
    cover=(arts or being or recs)[0]['f'] if recs else None
    intro_m=re.search(r'^\*(.+?)\*\s*$',raw,re.M)
    sub=strip_md(intro_m.group(1)) if intro_m else ''
    chapters.append({'n':n,'slug':slug,'school':SCHOOLS[n-1],'title':title,'cover':cover,'sub':sub,'nimg':len(recs),'nch':len(charts),'nbe':len(being),'toc':toc,'body':bodyhtml,'imgs':recs})
# pages
def tochtml(c):
    o=[]
    for sid,t,h3s,pr,gz in c['toc']:
        sub=''.join(f'<li><a href="#{a}">{esc(strip_md(re.sub(r"\[[^\]]*\]","",b)))}</a></li>' for a,b in h3s)
        o.append(f'<li class="{"t-proph" if pr else ""}{" t-gal" if gz else ""}"><a href="#{sid}">{esc(strip_md(t))}</a>{f"<ul>{sub}</ul>" if sub else ""}</li>')
    return '<ol>'+''.join(o)+'</ol>'
os.makedirs(OUT+'school',exist_ok=True)
for i,c in enumerate(chapters):
    prv=chapters[i-1] if i else None; nxt=chapters[i+1] if i<27 else None
    pager=f'<nav class="pager" aria-label="Chapters">{f"<a class=prev href={prv["slug"]}.html><small>Previous</small>{esc(prv["school"])}</a>" if prv else "<span></span>"}{f"<a class=next href={nxt["slug"]}.html><small>Next</small>{esc(nxt["school"])}</a>" if nxt else "<span></span>"}</nav>'
    hero=f'<header class="ch-hero">{f"<div class=ch-hero-bg style=\"background-image:url(../img/full/{c["cover"]})\"></div>" if c["cover"] else ""}<div class="ch-hero-in wrap"><p class="eyebrow">School {c["n"]:02d} of 28</p><h1>{esc(c["school"])}</h1><p class="ch-title">{esc(c["title"])}</p><p class="ch-meta"><a href="#g-charts">{c["nch"]} charts</a><span>·</span><a href="#g-being">{c["nbe"]} images of you</a></p></div></header>'
    data=json.dumps([{'f':r['f'],'cap':r['cap']} for r in c['imgs']],ensure_ascii=False).replace('</','<\\/')
    body=f'{hero}<div class="ch-layout wrap"><aside class="toc" aria-label="Contents"><button class="toc-toggle" aria-expanded="false">Contents</button><div class="toc-in"><p class="toc-k">Contents</p>{tochtml(c)}</div></aside><article class="prose" data-school="{c["n"]}">{c["body"]}{pager}</article></div><script type="application/json" id="imgdata">{data}</script>'
    open(f'{OUT}school/{c["slug"]}.html','w').write(page(c['school']+' · Book of Astrologies',body,1,'schools',c['sub'][:200]))
cards=''.join(f'<li class="card reveal" style="--d:{(c["n"]-1)%4}"><a href="school/{c["slug"]}.html"><div class="card-img">{f"<img src=img/thumb/{c["cover"]} alt=\"\" loading=lazy decoding=async>" if c["cover"] else ""}</div><div class="card-body"><span class="num">{c["n"]:02d}</span><h3>{esc(c["school"])}</h3><p>{esc(c["title"][:110])}</p><span class="card-meta">{c["nimg"]} images</span></div></a></li>' for c in chapters)
idx=open('src/home.html').read().replace('{{cards}}',cards).replace('{{nimg}}',str(len(allimgs))).replace('{{nev}}','%%NEV%%')
# timeline dedupe
seen=set(); tl=[]
for e in sorted(timeline,key=lambda e:(e['y'],e['m'],e['d'],e['school'])):
    k=(e['school'],e['y'],e['m'],e['d'],e['t'][:120])
    if k in seen: continue
    seen.add(k); tl.append(e)
idx=idx.replace('%%NEV%%',str(len(tl)))
open(OUT+'index.html','w').write(page('Book of Astrologies · Charles Leone',idx,0,'home'))
for name,act,t in [('gallery','gallery','Gallery'),('search','search','Search'),('timeline','timeline','Timeline 2026–2035')]:
    open(f'{OUT}{name}.html','w').write(page(t+' · Book of Astrologies',open(f'src/{name}.html').read(),0,act))
meta=[{'n':c['n'],'slug':c['slug'],'school':c['school']} for c in chapters]
os.makedirs(OUT+'data',exist_ok=True)
json.dump({'schools':meta,'imgs':[{k:r[k] for k in ('f','cap','school','type','sec')} for r in allimgs]},open(OUT+'data/images.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump({'schools':meta,'docs':search},open(OUT+'data/search.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump({'schools':meta,'events':tl},open(OUT+'data/timeline.json','w'),ensure_ascii=False,separators=(',',':'))
css=open('src/fonts.css').read()+'\n'+open('src/style.css').read()
open(OUT+'assets/style.css','w').write(css)
import shutil; shutil.copy('src/app.js',OUT+'assets/app.js')
open(OUT+'.nojekyll','w').write('')
print('images',len(allimgs),'events',len(tl),'search docs',len(search))
