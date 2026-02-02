import json

articles = json.load(open("articles.json"))

# ARCHIVE
html = "<h1>Archive</h1><ul>"
for a in articles:
    html += f'<li><a href="{a["slug"]}">{a["title"]}</a></li>'
html += "</ul>"

open("archive.html", "w").write(html)

# SEARCH INDEX
json.dump(
    [{"title": a["title"], "url": a["slug"]} for a in articles],
    open("search-index.json", "w"),
    indent=2
)

print("✅ Archive + search index built")
