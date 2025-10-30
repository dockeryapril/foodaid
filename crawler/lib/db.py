import os
from typing import Optional, Dict, Any
from supabase import create_client, Client

def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
    return create_client(url, key)

def upsert_post(sb: Client, post: Dict[str, Any]) -> Optional[int]:
    res = sb.table("posts").upsert({
        "platform": post["platform"],
        "external_id": post["external_id"],
        "author": post.get("author"),
        "url": post.get("url"),
        "content": post.get("content"),
        "lang": post.get("lang","en"),
        "posted_at": post.get("posted_at"),
        "raw": post.get("raw")
    }, on_conflict="platform,external_id").execute()
    data = res.data
    if data:
        return data[0]["id"]
    sel = sb.table("posts").select("id").eq("platform", post["platform"]).eq("external_id", post["external_id"]).execute()
    if sel.data:
        return sel.data[0]["id"]
    return None

def insert_event(sb: Client, ev: Dict[str, Any]) -> Optional[int]:
    res = sb.table("events").insert(ev).execute()
    if res.data:
        return res.data[0]["id"]
    return None
