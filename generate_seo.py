import json, os, re, math

SITE_URL="https://insight-chronicles.com"
TPL=open("article_template.html",encoding="utf-8").read()
drafts=[json.load(open("drafts/"+f,encoding="utf-8")) for f in sorted(os.listdir("drafts")) if f.endswith(".json")]

def toc(html):
    items=re.findall(r"<h2>(.*?)</h2>",html)
    return "<ul>"+"".join(f"<li>{i}</li>" for i in items)+"</ul>"

def readtime(text):
    return f"{max(1,math.ceil(len(text.split())/200))} min read"

articles=[]

for i,d in enumerate(drafts):
    c=d["content_html"]
    html=TPL \
      .replace("{{TITLE}}",d["title"]) \
      .replace("{{DESCRIPTION}}",d["desc"]) \
      .replace("{{DATE}}",d["date"]) \
      .replace("{{CONTENT}}",c) \
      .replace("{{TOC}}",toc(c)) \
      .replace("{{READING_TIME}}",readtime(c)) \
      .replace("{{TOOLS}}","<a href='#'>Recommended Book</a><a href='#'>Useful Tool</a>") \
      .replace("{{SHARE_BUTTONS}}",f"<a href='https://wa.me/?text={SITE_URL}/{d['slug']}'>WhatsApp</a>") \
      .replace("{{PREV_ARTICLE}}", f"<a href='{drafts[i-1]['slug']}'>← Previous</a>" if i>0 else "") \
      .replace("{{NEXT_ARTICLE}}", f"<a href='{drafts[i+1]['slug']}'>Next →</a>" if i<len(drafts)-1 else "") \
      .replace("{{RECOMMENDED_ARTICLES}}","".join(
        f"<a href='{r['slug']}'>{r['title']}</a>" for r in drafts if r!=d
      ))

    open(d["slug"],"w",encoding="utf-8").write(html)
    articles.append({**d,"url":f"{SITE_URL}/{d['slug']}"})

json.dump(articles,open("articles.json","w"),indent=2)
print("✅ EVERYTHING GENERATED")
