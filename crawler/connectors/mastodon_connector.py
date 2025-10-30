import os
from mastodon import Mastodon

def fetch_mastodon(query: str, limit: int = 40):
    base = os.getenv("MASTODON_BASE_URL","https://mastodon.social")
    token = os.getenv("MASTODON_ACCESS_TOKEN")
    if not token:
        return []
    m = Mastodon(access_token=token, api_base_url=base)
    res = m.search_v2(query, types=['statuses'], limit=limit)
    posts = []
    for s in res.get('statuses', []):
        url = s.get('url')
        posts.append({
            "platform":"mastodon",
            "external_id": str(s.get('id')),
            "author": s.get('account',{}).get('acct'),
            "url": url,
            "content": s.get('content',''),
            "posted_at": s.get('created_at'),
            "raw": s
        })
    return posts
