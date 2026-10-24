"""Post-build pass (link trim v3, Keith Oct 24 2026): on every page keep ONE working button/CTA
link to slotgrill.com (class 'btn'; the preferred one if PREF is set), plus the hand-picked contextual
text links in KEEP (page slug -> anchor texts). Every other slotgrill.com link becomes plain text
(buttons become <span> with the same class). Set LINKCUT=0 to disable and build the full-link version."""
import re, glob, os
A_RE = re.compile(r'<a\b([^>]*?)href=(["\'])(https?://(?:www\.)?slotgrill\.com[^"\']*)\2([^>]*)>(.*?)</a>', re.S)
CLS = re.compile(r'class=(["\'])([^"\']*)\1')
def _t(i): return re.sub(r'<[^>]+>','',i).strip()
def cut(src, rules, pref=None):
    pend=list(rules); nb=[0]; nk=[0]; first=[True]
    has=pref and any(_t(m.group(5))==pref and 'btn' in (CLS.search(m.group(1)+m.group(4)) or [0,0,''])[2].split() for m in A_RE.finditer(src))
    def rep(m):
        pre,post,inner=m.group(1),m.group(4),m.group(5)
        c=CLS.search(pre+post)
        if c and 'btn' in c.group(2).split() and first[0] and (not has or _t(inner)==pref): first[0]=False; nb[0]+=1; return m.group(0)
        t=_t(inner)
        if t in pend: pend.remove(t); nk[0]+=1; return m.group(0)
        if c and '<img' not in inner: return f'<span class="{c.group(2)}">{inner}</span>'
        return inner
    return A_RE.sub(rep,src), nb[0], nk[0]
def run(keep, pref=None, enabled=True):
    if not enabled: return
    B=K=0
    for f in sorted(glob.glob('*.html')):
        s=open(f,encoding='utf-8').read()
        o,b,k=cut(s,keep.get(f[:-5],[]),pref); B+=b; K+=k
        if o!=s: open(f,'w',encoding='utf-8').write(o)
    print(f'linkcut v3: {B} buttons + {K} contextual slotgrill.com links kept')
