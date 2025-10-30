import os, time
import praw

def fetch_reddit(subs, term='(title:"food" OR "food distribution" OR "pantry")', per_sub=30):
    cid = os.getenv("REDDIT_CLIENT_ID")
    csec = os.getenv("REDDIT_CLIENT_SECRET")
    ua = os.getenv("REDDIT_USER_AGENT","food-help-crawler/0.1")
    if not (cid and csec):
        return []
    r = praw.Reddit(client_id=cid, client_secret=csec, user_agent=ua)
    out = []
    for s in subs:
        try:
            for p in r.subreddit(s).search(term, limit=per_sub):
                out.append({
                    "platform":"reddit",
                    "external_id": p.id,
                    "author": str(p.author) if p.author else None,
                    "url": f"https://www.reddit.com{p.permalink}",
                    "content": (p.title or "") + "\n\n" + (p.selftext or ""),
                    "posted_at": p.created_utc,
                    "raw": {"subreddit": s}
                })
        except Exception as e:
            print(f"[reddit] error on r/{s}: {e}")
            time.sleep(1)
    return out
