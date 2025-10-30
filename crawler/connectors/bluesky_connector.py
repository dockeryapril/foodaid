import os
from atproto import Client
from datetime import datetime, timezone

def fetch_bluesky(query: str, limit: int = 40):
    handle = os.getenv("BLUESKY_HANDLE")
    app_pw = os.getenv("BLUESKY_APP_PASSWORD")
    if not (handle and app_pw):
        return []
    c = Client()
    c.login(handle, app_pw)
    res = c.app.bsky.feed.search_posts(query, limit=limit)
    posts = []
    for p in res.posts:
        uri = p.uri
        post_id = uri.split("/")[-1]
        url = f"https://bsky.app/profile/{p.author.handle}/post/{post_id}"
        posts.append({
            "platform":"bluesky",
            "external_id": post_id,
            "author": p.author.handle,
            "url": url,
            "content": p.record.text,
            "posted_at": datetime.fromisoformat(p.record.created_at.replace('Z','+00:00')).astimezone(timezone.utc).isoformat(),
            "raw": p.__dict__
        })
    return posts
