import feedparser

def fetch_rss(feeds):
    out = []
    for url in feeds:
        try:
            d = feedparser.parse(url)
            for e in d.entries:
                out.append({
                    "platform":"rss",
                    "external_id": e.get('id') or e.get('link'),
                    "author": e.get('author'),
                    "url": e.get('link'),
                    "content": (e.get('title','') + "\n\n" + e.get('summary','')).strip(),
                    "posted_at": e.get('published') or e.get('updated'),
                    "raw": {"feed": url}
                })
        except Exception as ex:
            print(f"[rss] error on {url}: {ex}")
    return out
