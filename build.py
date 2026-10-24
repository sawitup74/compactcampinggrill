import json,html,sys,os,re,glob,zlib
CDN="https://cdn.shopify.com/s/files/1/0721/8833/0172/files/"
IMG={k:CDN+v for k,v in dict(c07="compact-07.jpg?v=1792382833",c28="compact-28.jpg?v=1792382861",c08="compact-08.jpg?v=1792382834",c13="compact-13.jpg?v=1792382834",both16="both-16.jpg?v=1792382825",both02="both-02.jpg?v=1792382824",pl1="zz_Slot_Grill_Plancha_1.jpg?v=1792382973",pl2="zz_Slot_Grill_Plancha_2.jpg?v=1792382973",balm="seasoning-balm-main.jpg?v=1791978819",full01="full-size-01.jpg?v=1792382862").items()}
SG="https://slotgrill.com"
COMPACT=SG+"/products/slot-grill-compact-carbon-steel-free-shipping"
FULL=SG+"/products/slot-grill-carbon-steel-collapsible-bbq-grill"
GRID=SG+"/products/slot-grill-griddle-plancha"
BALM=SG+"/products/seasoning-balm-for-slot-grill"
THERMO=SG+"/products/slot-grill-instant-read-digital-meat-thermometer"
BUNDLE=SG+"/products/seasoning-balm-meat-thermometer-bundle"
DOMAIN="https://compactcampinggrill.com"
CSS="""
:root{--pine:#21392b;--moss:#4f6b3a;--sand:#efe6d2;--paper:#fbf8f0;--ember:#d9682b;--ink:#1f241e;--mute:#5d6458;--line:#d9d0b9}
*{box-sizing:border-box}body{margin:0;font:17px/1.7 Georgia,'Iowan Old Style',serif;color:var(--ink);background:var(--paper)}
h1,h2,h3,.brand,.tag,.btn,nav{font-family:'Trebuchet MS',Verdana,sans-serif}
a{color:var(--moss)}img{max-width:100%;height:auto;display:block;border-radius:6px}
.top{background:var(--pine);color:var(--sand);border-bottom:6px solid var(--ember)}
.top .in{max-width:1180px;margin:auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;padding:.8rem 1rem;gap:.6rem}
.brand{color:var(--sand);text-decoration:none;font-weight:900;font-size:1.25rem;letter-spacing:.04em;text-transform:uppercase}.brand b{color:var(--ember)}
nav a{color:var(--sand);text-decoration:none;margin-right:.9rem;font-size:.9rem;white-space:nowrap}
.wrap{max-width:1180px;margin:auto;padding:1rem;display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:2.2rem}
.wrap.full{grid-template-columns:1fr}
article h1{font-size:clamp(1.9rem,4.5vw,2.8rem);line-height:1.1;color:var(--pine);margin:.3rem 0 .6rem}
article h2{color:var(--pine);margin-top:2.2rem;border-bottom:2px dashed var(--line);padding-bottom:.2rem}
.lede{font-size:1.15rem;color:var(--mute);font-style:italic}
.crumbs{font:13px/1.4 'Trebuchet MS',sans-serif;color:var(--mute)}.crumbs a{color:var(--mute)}
.tag{display:inline-block;background:var(--moss);color:#fff;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;padding:.15rem .5rem;border-radius:3px}
aside .box{background:var(--sand);border:1px solid var(--line);border-radius:8px;padding:1rem;margin-bottom:1rem;position:sticky;top:1rem}
aside h3{margin:.1rem 0 .5rem;color:var(--pine)}aside ul{padding-left:1.1rem;margin:.3rem 0}aside li{font-size:.92rem}
.btn{display:inline-block;background:var(--ember);color:#fff!important;text-decoration:none;font-weight:700;padding:.65rem 1rem;border-radius:4px;margin:.3rem .4rem .3rem 0}
.btn.ghost{background:transparent;border:2px solid var(--pine);color:var(--pine)!important}
.callout{margin:2rem 0;border:3px solid var(--pine);border-radius:10px;overflow:hidden;background:#fff;display:grid;grid-template-columns:200px 1fr}
.callout img{border-radius:0;height:100%;object-fit:cover}.callout div{padding:1rem 1.2rem}.callout h3{margin:.1rem 0 .4rem;color:var(--pine);font-size:1.25rem}.callout .tag{background:var(--ember)}
.duo{margin:2rem 0;display:grid;grid-template-columns:1fr 1fr;gap:1rem}.duo a{background:var(--pine);color:var(--sand);text-decoration:none;border-radius:10px;padding:1rem;display:block}.duo img{aspect-ratio:4/3;object-fit:cover;margin-bottom:.5rem}.duo b{color:#fff;font-family:'Trebuchet MS',sans-serif}
.hero{background:linear-gradient(rgba(20,34,25,.78),rgba(20,34,25,.85)),url(__HERO__) center/cover;color:var(--sand);padding:4rem 1rem}
.hero .in{max-width:1180px;margin:auto}.hero h1{font-size:clamp(2.2rem,6vw,3.8rem);line-height:1.02;max-width:820px;margin:.4rem 0 1rem;color:#fff}.hero p{max-width:680px;font-size:1.15rem}
.cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.8rem;margin:1rem 0 2rem}.cats a{background:var(--sand);border-left:6px solid var(--moss);padding:.8rem 1rem;text-decoration:none;color:var(--ink);border-radius:4px}.cats b{display:block;color:var(--pine);font-family:'Trebuchet MS',sans-serif}
.list{list-style:none;padding:0}.list li{border-bottom:1px solid var(--line);padding:.7rem 0}.list a{font-weight:700;font-family:'Trebuchet MS',sans-serif;font-size:1.05rem;text-decoration:none;color:var(--pine)}.list span{display:block;color:var(--mute);font-size:.93rem}
table{border-collapse:collapse;width:100%;font-size:.93rem;background:#fff}td,th{border:1px solid var(--line);padding:.45rem .6rem;text-align:left;vertical-align:top}th{background:var(--sand)}
.tip{background:#eef3e6;border-left:5px solid var(--moss);padding:.8rem 1rem;border-radius:4px}
footer{background:var(--pine);color:#c9c3b1;margin-top:3rem;padding:2rem 1rem;font:14px/1.6 'Trebuchet MS',sans-serif}footer .in{max-width:1180px;margin:auto}footer a{color:var(--sand)}
@media(max-width:860px){.wrap{grid-template-columns:1fr}.callout{grid-template-columns:1fr}.callout img{max-height:220px}.duo{grid-template-columns:1fr}aside .box{position:static}}
"""
CATS={"gear":("camping-gear","Tents, Gear &amp; Checklists","Shelter, sleep systems, packing lists and backpacking basics."),
"water":("paddling-camps","Kayak &amp; Paddle Camping","River, lake and coastal trips where everything rides in a boat."),
"rv":("rv-and-car-camping","RVs, Trailers &amp; Car Camping","Campgrounds you drive to, from a hatchback to a travel trailer."),
"kitchen":("camp-kitchen","Camp Kitchen &amp; Recipes","Cooking outdoors on clean steel, menus, and camp recipes."),
"fire":("campfire-and-safety","Campfire, Safety &amp; Leave No Trace","Fire skills, fire rules, weather and low-impact habits."),
"family":("family-camping","Family &amp; Kids Camping","First trips, kid jobs, games and keeping everyone happy."),
"parks":("park-guides","Park &amp; Destination Guides","Texas state parks, the Gulf Coast, national parks and regional highlights.")}
PAGES=[]
def md(t):
    out=[];ul=None
    for blk in re.split(r"\n\s*\n",t.strip()):
        b=blk.strip()
        if b.startswith("<"): out.append(b);continue
        if b.startswith("## "): out.append(f"<h2>{b[3:]}</h2>");continue
        if b.startswith("### "): out.append(f"<h3>{b[4:]}</h3>");continue
        if b.startswith("- ") or b.startswith("1. "):
            tag="ol" if b.startswith("1. ") else "ul"
            items=[re.sub(r"^(- |\d+\. )","",x) for x in b.split("\n") if x.strip()]
            out.append(f"<{tag}>"+"".join(f"<li>{x}</li>" for x in items)+f"</{tag}>");continue
        if b.startswith("! "): out.append(f'<p class="tip">{b[2:]}</p>');continue
        out.append(f"<p>{b}</p>")
    h="\n".join(out)
    return re.sub(r"\*\*(.+?)\*\*",r"<b>\1</b>",h)
def A(slug,title,desc,cat,img,body,faq=None): PAGES.append((slug,title,desc,cat,IMG.get(img,img),body,faq or []))
# product call-outs: all facts from slotgrill.com product pages
CALLS=[
("Portable fire pit","Love campfires? Bring your own clean one.","The Slot Grill Compact burns charcoal or cooking wood in a raised steel box with a 2⅞\" air gap underneath, so where fires are allowed it doubles as a tidy personal fire pit after supper. Set up by hand in 30 to 60 seconds, no tools.",IMG["c28"],COMPACT,"See the Compact · $79.97"),
("Portable camping grill","Love camping? Check out the Slot Grill Compact.","12-gauge carbon steel, about 14 lb, a 16.25\" × 9\" cooking area for one to three campers, and it packs down to roughly an inch thick for a trunk, kayak, RV or camp box. Made in Texas, free shipping in the lower 48.",IMG["c07"],COMPACT,"Shop the Compact"),
("Flat-pack grill","Packs flat. Cooks like it means it.","Tab-and-slot steel plates, no hinges, no loose hardware to lose in the leaves. The Full Size packs to about 1.25\" and the Compact to about 1\". Both are strong enough for cast iron.",IMG["both16"],FULL,"See the Full Size · $139.97"),
("Feeding the whole camp","Cooking for the family? Go Full Size.","10-gauge carbon steel, a 20.5\" × 11.25\" cooking area (231 sq in) and a 3⅝\" air gap for truck beds, tables and boat decks. Plenty of space for thick steaks, a skillet, and supper for the whole crew.",IMG["full01"],FULL,"Shop the Full Size"),
("Camp griddle","Pancakes, eggs and smash burgers at camp","The Slot Grill Griddle (Plancha) add-on is built from the same thick carbon steel, comes in half or full griddle configurations, and flat-stacks with your Slot Grill. Grill not included.",IMG["pl1"],GRID,"See the griddle add-on"),
("Keep it trail-ready","Raw steel likes a little care","Slot Grill Seasoning Balm is an avocado oil and beeswax blend for carbon steel and cast iron. Wipe on a very thin coat, bake at 400°F for an hour, repeat to build up a protective, non-stick layer.",IMG["balm"],BALM,"Seasoning Balm · $8.97"),
("Done means done","No guessing in the dark","The Slot Grill Instant-Read Digital Meat Thermometer reads in about 3 seconds, has a backlit display for night cooks and a fold-away probe. Or grab it bundled with Seasoning Balm.",IMG["c13"],THERMO,"Thermometer · $19.97"),
]
def callout(i):
    t,h,p,img,url,cta=CALLS[i%len(CALLS)]
    return f'<div class="callout"><img src="{img}" alt="{html.escape(h)}" loading="lazy"><div><span class="tag">{t}</span><h3>{h}</h3><p>{p}</p><a class="btn" href="{url}">{cta}</a></div></div>'
def duo():
    return f'<div class="duo"><a href="{COMPACT}"><img src="{IMG["c08"]}" alt="Slot Grill Compact" loading="lazy"><b>Compact · $79.97</b><br>About 14 lb, 146 sq in, 1 to 3 people, packs about 1" thick.</a><a href="{FULL}"><img src="{IMG["full01"]}" alt="Slot Grill Full Size" loading="lazy"><b>Full Size · $139.97</b><br>About 27.6 lb, 231 sq in, family-size, packs about 1.25" thick.</a></div>'
def faqld(faq):
    if not faq: return ""
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})+'</script>'
def crumbld(items):
    return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":html.unescape(n),"item":DOMAIN+u} for i,(n,u) in enumerate(items)]})+'</script>'
NAV="".join(f'<a href="/{c[0]}.html">{html.unescape(c[1]).split(",")[0].split(" &")[0]}</a>' for c in CATS.values())+'<a href="/faq.html">FAQ</a>'
def shell(title,desc,slug,inner,img=None,extra="",full=False,side=""):
    canon=DOMAIN+("/" if slug=="index" else f"/{slug}.html")
    ld={"@context":"https://schema.org","@type":"WebSite" if slug=="index" else "Article","name":title,"headline":title,"url":canon,"image":img or IMG["c28"],"publisher":{"@type":"Organization","name":"Compact Camping Grill"}}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{canon}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{img or IMG['c28']}">
<link rel="stylesheet" href="/style.css"><script type="application/ld+json">{json.dumps(ld)}</script>{extra}</head><body>
<header class="top"><div class="in"><a class="brand" href="/">Compact<b>Camping</b>Grill</a><nav>{NAV}</nav></div></header>
{inner if slug=="index" else f'<div class="wrap{" full" if full else ""}"><article>{inner}</article>{side}</div>'}
<footer><div class="in"><p><b>Compact Camping Grill</b> is an independent camping resource published by the makers of Slot Grill. No ads, no tracking. Slot Grill® is a registered trademark of Precision Cut Metals LLC.</p><p>Every product link on this site goes to <a href="{SG}">SlotGrill.com</a>, the only place to buy a genuine Slot Grill direct from the maker. Park details change; check with the managing agency before you go and follow posted fire rules.</p><p>{" · ".join(f'<a href="/{c[0]}.html">{c[1]}</a>' for c in CATS.values())} · <a href="/faq.html">FAQ</a></p></div></footer></body></html>'''
def sidebar(slug,cat):
    rel=[p for p in DONE if p[3]==cat and p[0]!=slug][:8]
    c=CATS[cat]
    return f'<aside><div class="box"><h3>More in {c[1]}</h3><ul>'+"".join(f'<li><a href="/{p[0]}.html">{html.escape(p[1])}</a></li>' for p in rel)+f'</ul><p><a href="/{c[0]}.html">All {c[1]} →</a></p><hr><h3>The camp cooker</h3><p style="font-size:.92rem">One steel box: grill at supper, fire pit after. No mystery fire ring required.</p><a class="btn" href="{COMPACT}">Compact</a><a class="btn ghost" href="{FULL}">Full Size</a></div></aside>'
def wc(h): return len(re.sub("<[^>]+>"," ",h).split())
def article(slug,title,desc,cat,img,body,faq):
    c=CATS[cat]; h=md(body); n=zlib.crc32(slug.encode())
    parts=h.split("<h2>")
    if len(parts)>4: h="<h2>".join(parts[:3])+callout(n)+"<h2>"+"<h2>".join(parts[3:])
    else: h+=callout(n)
    if len(parts)>8: h=h.replace("<h2>"+parts[7],callout(n+5)+"<h2>"+parts[7],1)
    fq=('<h2>Questions campers ask</h2>'+"".join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q,a in faq)) if faq else ""
    inner=f'<p class="crumbs"><a href="/">Home</a> › <a href="/{c[0]}.html">{c[1]}</a> › {html.escape(title)}</p><span class="tag">{c[1]}</span><h1>{html.escape(title)}</h1><p class="lede">{html.escape(desc)}</p><img src="{img}" alt="Slot Grill at camp: {html.escape(title)}">{h}{fq}{callout(n+3)}{duo()}'
    return shell(title,desc,slug,inner,img,faqld(faq)+crumbld([("Home","/"),(c[1],f"/{c[0]}.html"),(title,f"/{slug}.html")]),side=sidebar(slug,cat)),wc(h+fq)
EXTRA={}; XFAQ={}
for f in sorted(glob.glob("content_*.py")): exec(open(f).read())
PAGES=[(a,b,c,d,e,f+"\n\n"+EXTRA.get(a,""),g+XFAQ.get(a,[])) for a,b,c,d,e,f,g in PAGES]
open("style.css","w").write(CSS.replace("__HERO__",IMG["c28"]))
DONE=list(PAGES); WC={}
for p in PAGES:
    s,w=article(*p); open(p[0]+".html","w").write(s); WC[p[0]]=w
for i,(k,c) in enumerate(CATS.items()):
    ps=[p for p in DONE if p[3]==k]
    if not ps: continue
    inner=f'<p class="crumbs"><a href="/">Home</a> › {c[1]}</p><h1>{c[1]}</h1><p class="lede">{c[2]}</p><ul class="list">'+"".join(f'<li><a href="/{p[0]}.html">{html.escape(p[1])}</a><span>{html.escape(p[2])}</span></li>' for p in ps)+'</ul>'+callout(i)+duo()
    open(c[0]+".html","w").write(shell(html.unescape(c[1])+" | Compact Camping Grill",html.unescape(c[2]),c[0],inner,extra=crumbld([("Home","/"),(c[1],f"/{c[0]}.html")]),full=True))
if "FAQ" in globals():
    inner='<p class="crumbs"><a href="/">Home</a> › FAQ</p><h1>Camping &amp; Slot Grill FAQ</h1>'+"".join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q,a in FAQ)+callout(1)+duo()
    open("faq.html","w").write(shell("Camping FAQ | Compact Camping Grill","Straight answers about camp cooking, campfires, gear, and the Slot Grill Compact and Full Size.","faq",inner,extra=faqld(FAQ)+crumbld([("Home","/"),("FAQ","/faq.html")]),full=True))
latest="".join(f'<li><a href="/{p[0]}.html">{html.escape(p[1])}</a><span>{html.escape(p[2])}</span></li>' for p in DONE[-12:][::-1])
cats="".join(f'<a href="/{c[0]}.html"><b>{c[1]}</b>{c[2]}</a>' for k,c in CATS.items() if any(p[3]==k for p in DONE))
idx=f'''<section class="hero"><div class="in"><span class="tag">Field notes for people who sleep outside</span><h1>Camp better. Cook on steel you trust.</h1><p>Tents, paddling trips, trailers, park guides, campfire know-how and camp recipes. And one simple idea: bring your own clean fire instead of inheriting whatever happened in the campground ring last night.</p><a class="btn" href="{COMPACT}">Meet the Slot Grill Compact</a><a class="btn ghost" style="color:#fff!important;border-color:#fff" href="/camp-kitchen.html">Camp recipes</a></div></section>
<div class="wrap full"><article><h2>Pick your trail</h2><div class="cats">{cats}</div>{callout(0)}<h2>Fresh from camp</h2><ul class="list">{latest}</ul>{duo()}{callout(3)}</article></div>'''
open("index.html","w").write(shell("Compact Camping Grill: Camping Guides, Park Picks & Camp Cooking","A camping resource: tents, kayak camping, RVs, park guides, campfire safety and camp recipes cooked on the Slot Grill.","index",idx))
open("404.html","w").write(shell("Trail not found","That page wandered off.","404",'<h1>Trail not found</h1><p>That page wandered off. Head back to <a href="/">base camp</a>.</p>',full=True))
urls=["/"]+[f"/{c[0]}.html" for k,c in CATS.items() if any(p[3]==k for p in DONE)]+(["/faq.html"] if "FAQ" in globals() else [])+[f"/{p[0]}.html" for p in DONE]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>2026-10-23</lastmod></url>\n" for u in urls)+"</urlset>\n")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
json.dump(WC,open("/tmp/ccg_wc.json","w"))
print(len(DONE),"articles", sum(WC.values()),"words")
