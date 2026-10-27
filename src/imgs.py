import re,glob,os
from PIL import Image
from multiprocessing import Pool
D='/workspace/book_of_astrologies/deep/'
ps=sorted({m for f in glob.glob('/workspace/book_of_astrologies/ch/*.md') for m in re.findall(r'\]\((/workspace/book_of_astrologies/deep/[^)]+)\)',re.sub(r'\]\((?:\.\./|\./)?deep/','](/workspace/book_of_astrologies/deep/',open(f).read()))})
def name(p): return os.path.splitext(p[len(D):])[0].replace('/','__')+'.webp'
def conv(p):
    n=name(p); o='docs/img/full/'+n
    if os.path.exists(o): return
    
    if not os.path.exists(p): print('MISSING',p); return
    im=Image.open(p); im=im.convert('RGBA' if im.mode in('RGBA','LA','P') else 'RGB')
    a=im.copy(); a.thumbnail((1800,1800),Image.LANCZOS); a.save(o,'WEBP',quality=80,method=5)
    t=im.copy(); t.thumbnail((560,560),Image.LANCZOS); t.save('docs/img/thumb/'+n,'WEBP',quality=72,method=5)
if __name__=='__main__':
    with Pool(8) as pl: pl.map(conv,ps,chunksize=4)
    print(len(ps))
