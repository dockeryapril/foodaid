import os
from googleapiclient.discovery import build

def fetch_youtube(queries, max_res=20):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key: return []
    yt = build("youtube","v3", developerKey=api_key)
    out = []
    for q in queries:
        req = yt.search().list(part="snippet", q=q, maxResults=max_res, order="date")
        res = req.execute()
        for item in res.get("items", []):
            if item["id"]["kind"] != "youtube#video":
                continue
            vid = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={vid}"
            snippet = item["snippet"]
            text = snippet.get("title","") + "\n\n" + snippet.get("description","")
            out.append({
                "platform":"youtube",
                "external_id": vid,
                "author": snippet.get("channelTitle"),
                "url": url,
                "content": text,
                "posted_at": snippet.get("publishedAt"),
                "raw": item
            })
    return out
