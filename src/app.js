(()=>{
const pre=document.body.dataset.pre||'';const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
/* starfield */
(()=>{const c=$('#sky');if(!c)return;const x=c.getContext('2d');let W,H,D=Math.min(devicePixelRatio||1,2),st=[];
function init(){W=c.width=innerWidth*D;H=c.height=innerHeight*D;const n=Math.round(innerWidth*innerHeight/2600);st=[];for(let i=0;i<n;i++){const z=Math.random();st.push({x:Math.random()*W,y:Math.random()*H*1.6,r:(z*z*1.3+.25)*D,z,p:Math.random()*6.28,s:.4+Math.random()*1.2,h:Math.random()<.12?1:0})}}
let sy=0,t0=performance.now();
function draw(t){x.clearRect(0,0,W,H);const k=(t-t0)/1000;for(const s of st){let y=(s.y-sy*D*(.04+s.z*.18))%(H*1.6);if(y<0)y+=H*1.6;if(y>H)continue;const a=(.25+.6*s.z)*(RM?1:.65+.35*Math.sin(k*s.s+s.p));x.globalAlpha=a;x.fillStyle=s.h?'#f1dcaa':'#e8e6f2';x.beginPath();x.arc(s.x,y,s.r,0,6.283);x.fill()}x.globalAlpha=1;if(!RM)requestAnimationFrame(draw)}
init();addEventListener('resize',()=>{init();RM&&draw(0)});addEventListener('scroll',()=>{sy=scrollY;RM&&draw(0)},{passive:true});requestAnimationFrame(draw)})();
/* topbar + nav */
const tb=$('.topbar');const onS=()=>tb.classList.toggle('solid',scrollY>30);onS();addEventListener('scroll',onS,{passive:true});
const nt=$('.nav-toggle'),nv=$('#nav');nt.onclick=()=>{const o=nv.classList.toggle('open');nt.setAttribute('aria-expanded',o)};
/* reveal */
const io='IntersectionObserver'in window&&!RM?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -6% 0px'}):null;
const reveal=els=>els.forEach(e=>io?io.observe(e):e.classList.add('in'));reveal($$('.reveal'));
/* parallax chapter hero */
const bg=$('.ch-hero-bg');if(bg&&!RM)addEventListener('scroll',()=>{if(scrollY<innerHeight)bg.style.transform=`translate3d(0,${scrollY*.25}px,0) scale(1.05)`},{passive:true});
/* hero wheel: tropical positions from the Hellenistic chapter's table */
const w=$('#wheel');if(w){const ns='http://www.w3.org/2000/svg';const asc=350.65;
const P=[['Sun',200.33],['Moon',127.52],['Mercury',212.78],['Venus',196.13],['Mars',153.88],['Jupiter',349.70],['Saturn',30.95],['Node',148.58]];
const S=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
const ang=l=>(180+(l-asc))*Math.PI/180,pt=(l,r)=>[Math.cos(ang(l))*r,-Math.sin(ang(l))*r];
const el=(t,a,p)=>{const e=document.createElementNS(ns,t);for(const k in a)e.setAttribute(k,a[k]);(p||w).appendChild(e);return e};
const g=el('g',{class:'enter'}),outer=el('g',{class:'spin'},g),inner=el('g',{class:'spin-r'},g);
[288,262,232,150].forEach((r,i)=>el('circle',{r,class:'ring'+(i==3?' faint':'')},g));el('circle',{r:296,class:'ring faint'},outer);
for(let d=0;d<360;d+=1){const L=d%30==0?[232,262]:d%10==0?[252,262]:d%5==0?[256,262]:[259,262];const[a,b]=pt(d,L[0]),[c,e]=pt(d,L[1]);el('line',{x1:a,y1:b,x2:c,y2:e,class:'tick'+(d%30==0?' m':'')},g)}
S.forEach((s,i)=>{const[x,y]=pt(i*30+15,276);const t=el('text',{x,y,class:'sign',transform:`rotate(${(r=>{r=((r%360)+540)%360-180;return r>90?r-180:r<-90?r+180:r})(90-(180+(i*30+15-asc)))} ${x} ${y})`},g);t.textContent=s.toUpperCase().slice(0,3)});
for(let i=0;i<72;i++){const[x,y]=pt(i*5,296);el('circle',{cx:x,cy:y,r:i%6?0.8:1.6,fill:'rgba(217,183,121,.5)'},outer)}
const asp=[0,60,90,120,180];let n=0;for(let i=0;i<P.length;i++)for(let j=i+1;j<P.length;j++){let d=Math.abs(P[i][1]-P[j][1]);d=d>180?360-d:d;if(asp.slice(1).some(a=>Math.abs(d-a)<6)){const[a,b]=pt(P[i][1],150),[c,e]=pt(P[j][1],150);const len=Math.hypot(a-c,b-e);el('line',{x1:a,y1:b,x2:c,y2:e,class:'asp',style:`--len:${len};--dl:${.8+n++*.15}s`},g)}}
[[asc,'ASC'],[asc+180,'DSC'],[265,'MC'],[85,'IC']].forEach(([l,t])=>{const[a,b]=pt(l,150),[c,e]=pt(l,232);el('line',{x1:a,y1:b,x2:c,y2:e,class:'axis'},g);const[x,y]=pt(l,140);const tx=el('text',{x,y,class:'axl','text-anchor':'middle','dominant-baseline':'middle'},g);tx.textContent=t});
const used=[];P.forEach(([nm,l],i)=>{let r=200;for(const u of used)if(Math.abs(((l-u.l+540)%360)-180)<9)r=u.r==200?178:200;used.push({l,r});const[x,y]=pt(l,r);const gp=el('g',{class:'pl'},g);
 el('circle',{cx:x,cy:y,r:9,class:'h'},gp);const[a,b]=pt(l,232);el('circle',{cx:a,cy:b,r:2.4,class:'d'},gp);const t=el('text',{x,y,},gp);t.textContent=nm=='Node'?'☊︎':nm.slice(0,2);const ti=el('title',{},gp);ti.textContent=nm});
if(!RM)addEventListener('mousemove',e=>{const dx=(e.clientX/innerWidth-.5),dy=(e.clientY/innerHeight-.5);w.style.transform=`perspective(900px) rotateY(${dx*6}deg) rotateX(${-dy*6}deg)`;},{passive:true});w.style.transition='transform 1.2s cubic-bezier(.2,.7,.2,1)'}
/* lightbox */
const lb=$('#lb'),li=$('img',lb),cap=$('.lb-cap',lb),cnt=$('.lb-count',lb);let list=[],ix=0,last=null;
function show(i){ix=(i+list.length)%list.length;const it=list[ix];lb.classList.add('loading');li.classList.add('ld');const im=new Image();im.onload=()=>{li.src=im.src;li.alt=it.cap;lb.classList.remove('loading');requestAnimationFrame(()=>li.classList.remove('ld'))};im.src=pre+'img/full/'+it.f;cap.textContent=it.cap;cnt.textContent=(ix+1)+' / '+list.length;[1,-1].forEach(d=>{const n=list[(ix+d+list.length)%list.length];if(n)new Image().src=pre+'img/full/'+n.f})}
function open(l,i){list=l;last=document.activeElement;lb.hidden=false;requestAnimationFrame(()=>lb.classList.add('open'));document.documentElement.style.overflow='hidden';show(i);$('.lb-close',lb).focus()}
function close(){lb.classList.remove('open');setTimeout(()=>{lb.hidden=true;li.src=''},300);document.documentElement.style.overflow='';last&&last.focus()}
window.BOA_open=open;
$('.lb-close',lb).onclick=close;$('.lb-prev',lb).onclick=()=>show(ix-1);$('.lb-next',lb).onclick=()=>show(ix+1);
lb.addEventListener('click',e=>{if(e.target.classList.contains('lb-stage'))close()});
addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key=='Escape')close();else if(e.key=='ArrowRight')show(ix+1);else if(e.key=='ArrowLeft')show(ix-1);else if(e.key=='Tab'){const f=$$('button',lb),a=f.indexOf(document.activeElement);e.preventDefault();f[(a+(e.shiftKey?-1:1)+f.length)%f.length].focus()}});
let sx=null,sy0=null;const st=$('.lb-stage',lb);st.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;sy0=e.touches[0].clientY},{passive:true});
st.addEventListener('touchmove',e=>{if(sx==null)return;const dx=e.touches[0].clientX-sx;li.style.transform=`translateX(${dx*.6}px)`;li.style.transition='none'},{passive:true});
st.addEventListener('touchend',e=>{if(sx==null)return;const dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy0;li.style.transform='';li.style.transition='';sx=null;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))show(ix+(dx<0?1:-1));else if(dy>90)close()});
/* chapter page */
const data=$('#imgdata');if(data){const all=JSON.parse(data.textContent);const pos=f=>all.findIndex(x=>x.f==f);
 document.addEventListener('click',e=>{const b=e.target.closest('.prose .zoom');if(!b)return;const gl=b.closest('[data-gallery]');let l=all;if(gl){l=$$('.zoom',gl).map(z=>all[pos(z.dataset.f)]);open(l,l.findIndex(x=>x.f==b.dataset.f))}else open(l,pos(b.dataset.f))});
 const toc=$('.toc'),tt=$('.toc-toggle');tt.onclick=()=>{const o=toc.classList.toggle('open');tt.setAttribute('aria-expanded',o)};
 $$('.toc a').forEach(a=>a.addEventListener('click',()=>{toc.classList.remove('open');tt.setAttribute('aria-expanded',false)}));
 const links=new Map($$('.toc a').map(a=>[a.getAttribute('href').slice(1),a]));const heads=$$('.prose h2[id],.prose h3[id]').filter(h=>links.has(h.id));
 let cur=null;const spy=()=>{let h=heads[0];for(const x of heads){if(x.getBoundingClientRect().top<140)h=x;else break}if(!h||h===cur)return;cur=h;$$('.toc a.act,.toc li.open').forEach(x=>x.classList.remove('act','open'));const a=links.get(h.id);a.classList.add('act');let p=a.parentElement;while(p&&p!==toc){if(p.tagName=='LI')p.classList.add('open');p=p.parentElement}
  const ti=$('.toc-in');if(innerWidth>1000){const r=a.getBoundingClientRect(),R=toc.getBoundingClientRect();if(r.top<R.top+40||r.bottom>R.bottom-40)toc.scrollTop+=r.top-R.top-R.height/3}tt.textContent='Contents · '+a.textContent};
 addEventListener('scroll',()=>requestAnimationFrame(spy),{passive:true});spy()}
/* shared data pages */
const J=u=>fetch(pre+u).then(r=>r.json());
const fillSchools=(sel,s)=>s.forEach(x=>sel.insertAdjacentHTML('beforeend',`<option value="${x.n}">${String(x.n).padStart(2,'0')} · ${esc(x.school)}</option>`));
const qs=new URLSearchParams(location.search);
if($('#g-grid'))J('data/images.json').then(d=>{const S=Object.fromEntries(d.schools.map(s=>[s.n,s]));const sel=$('#g-school');fillSchools(sel,d.schools);let t='',items=[],shown=0;const grid=$('#g-grid');
 if(qs.get('school'))sel.value=qs.get('school');
 const TN={chart:'Chart',artwork:'Artwork',symbolic:'Symbolic body'};
 function apply(){const q=$('#g-q').value.trim().toLowerCase(),s=sel.value;items=d.imgs.filter(i=>(!s||i.school==s)&&(!t||i.type==t)&&(!q||i.cap.toLowerCase().includes(q)||S[i.school].school.toLowerCase().includes(q)));grid.innerHTML='';shown=0;more();$('#g-status').textContent=items.length+' of '+d.imgs.length+' images'}
 function more(){const end=Math.min(items.length,shown+40);let h='';for(let k=shown;k<end;k++){const i=items[k];h+=`<li style="animation-delay:${(k-shown)*25}ms"><button class="zoom" data-k="${k}" aria-label="Open: ${esc(i.cap)}"><img src="img/thumb/${i.f}" alt="${esc(i.cap)}" loading="lazy" decoding="async"></button><div class="meta"><span>${esc(i.cap.length>90?i.cap.slice(0,88)+'…':i.cap)}</span><a href="school/${S[i.school].slug}.html#${i.sec}">${esc(S[i.school].school)}</a></div></li>`}grid.insertAdjacentHTML('beforeend',h);shown=end}
 new IntersectionObserver(e=>{if(e[0].isIntersecting&&shown<items.length)more()},{rootMargin:'800px'}).observe($('#g-more'));
 grid.addEventListener('click',e=>{const b=e.target.closest('.zoom');if(b)open(items,+b.dataset.k)});
 $$('.chip').forEach(c=>c.onclick=()=>{$$('.chip').forEach(x=>x.classList.toggle('on',x===c));t=c.dataset.t;apply()});
 let tm;$('#g-q').oninput=()=>{clearTimeout(tm);tm=setTimeout(apply,180)};sel.onchange=apply;apply()});
if($('#s-res'))J('data/search.json').then(d=>{const S=Object.fromEntries(d.schools.map(s=>[s.n,s]));const sel=$('#s-school');fillSchools(sel,d.schools);const docs=d.docs.map(x=>({...x,l:x.t.toLowerCase(),hl:x.h.toLowerCase()}));const inp=$('#s-q');
 if(qs.get('q'))inp.value=qs.get('q');
 function run(){const q=inp.value.trim().toLowerCase(),s=sel.value;const out=$('#s-res');if(q.length<2){out.innerHTML='';$('#s-status').textContent='Type at least two letters. '+docs.length+' sections across 28 chapters.';return}
  const terms=q.split(/\s+/).filter(Boolean);const res=[];for(const x of docs){if(s&&x.s!=s)continue;let sc=0,ok=true;for(const w of terms){let c=0,p=-1;while((p=x.l.indexOf(w,p+1))>-1&&c<50)c++;if(!c&&!x.hl.includes(w)){ok=false;break}sc+=c+(x.hl.includes(w)?20:0)}if(ok)res.push([sc,x])}
  res.sort((a,b)=>b[0]-a[0]);const re=new RegExp('('+terms.map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','gi');
  out.innerHTML=res.slice(0,80).map(([sc,x])=>{const p=Math.max(0,x.l.indexOf(terms[0])-120);const snip=(p?'… ':'')+x.t.slice(p,p+300)+' …';return `<li><a href="school/${S[x.s].slug}.html#${x.id}"><span class="rs">${String(x.s).padStart(2,'0')} · ${esc(S[x.s].school)}</span><h3>${esc(x.h).replace(re,'<mark>$1</mark>')}</h3><p>${esc(snip).replace(re,'<mark>$1</mark>')}</p></a></li>`}).join('');
  $('#s-status').textContent=res.length?res.length+' matching sections'+(res.length>80?' (showing the top 80)':''):'No matches.';history.replaceState(null,'','?q='+encodeURIComponent(inp.value))}
 let tm;inp.oninput=()=>{clearTimeout(tm);tm=setTimeout(run,200)};sel.onchange=run;run()});
if($('#t-list'))J('data/timeline.json').then(d=>{const S=Object.fromEntries(d.schools.map(s=>[s.n,s]));const sel=$('#t-school');fillSchools(sel,d.schools);let yr='';const M=['','January','February','March','April','May','June','July','August','September','October','November','December'];
 const ys=[...new Set(d.events.map(e=>e.y))];$('#t-years').innerHTML='<button class="chip on" data-y="">All years</button>'+ys.map(y=>`<button class="chip" data-y="${y}">${y}</button>`).join('');
 $$('#t-years .chip').forEach(c=>c.onclick=()=>{$$('#t-years .chip').forEach(x=>x.classList.toggle('on',x===c));yr=c.dataset.y;apply()});let ev=[],shown=0;
 function apply(){const q=$('#t-q').value.trim().toLowerCase(),s=sel.value;ev=d.events.filter(e=>(!s||e.school==s)&&(!yr||e.y==yr)&&(!q||e.t.toLowerCase().includes(q)||e.h.toLowerCase().includes(q)));shown=0;$('#t-list').innerHTML='';more();$('#t-status').textContent=ev.length+' dated passages'}
 function more(){const end=Math.min(ev.length,shown+120);let h='',prevY=shown?ev[shown-1].y:null;for(let k=shown;k<end;k++){const e=ev[k];if(e.y!==prevY){h+=`<div class="tl-year"><h2>${e.y}</h2></div>`;prevY=e.y}
  h+=`<article class="ev"><div class="ev-top"><span class="ev-date">${(e.d?e.d+' ':'')+M[e.m]} ${e.y}</span><a class="ev-school" href="school/${S[e.school].slug}.html#${e.sec}">${esc(S[e.school].school)}</a><span class="ev-sec">${esc(e.h)}</span></div><p>${esc(e.t)}</p></article>`}
  $('#t-list').insertAdjacentHTML('beforeend',h);shown=end;$('#t-list .more')?.remove();if(shown<ev.length){$('#t-list').insertAdjacentHTML('beforeend','<button class="more">Show more</button>');$('#t-list .more').onclick=more}}
 let tm;$('#t-q').oninput=()=>{clearTimeout(tm);tm=setTimeout(apply,180)};sel.onchange=apply;apply()});
})();
