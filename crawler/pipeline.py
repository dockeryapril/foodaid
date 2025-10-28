import os, yaml
from typing import List, Dict, Any
from tqdm import tqdm

from lib.sink import get_sink
from lib.classify import classify_and_extract
from lib.geo import geocode
from lib.verifier import verify

from connectors.bluesky_connector import fetch_bluesky
from connectors.mastodon_connector import fetch_mastodon
from connectors.reddit_connector import fetch_reddit
from connectors.youtube_connector import fetch_youtube
from connectors.rss_connector import fetch_rss

QUERY = '(food OR pantry OR "food distribution" OR "free groceries" OR "mobile pantry" OR "produce giveaway") (today OR Sat OR Sun OR Nov OR Dec)'

def load_sources(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def normalize_region_filter(regions_arg: str) -> List[str]:
    if not regions_arg:
        return []
    return [r.strip() for r in regions_arg.split(",") if r.strip()]

def run_pipeline(regions: List[str], sources_path: str):
    sink = get_sink()
    cfg = load_sources(sources_path)
    all_regions = cfg.get("regions", [])
    scope = [r for r in all_regions if (not regions) or (r["key"] in regions)]
    print(f"Regions in scope: {[r['key'] for r in scope]}")

    harvested = []

    for reg in scope:
        key = reg["key"]
        print(f"--- Harvesting for {key} ---")
        harvested += fetch_bluesky(QUERY)
        harvested += fetch_mastodon(QUERY)
        subs = reg.get("reddit_subs", [])
        if subs:
            harvested += fetch_reddit(subs)
        yq = reg.get("youtube_queries", [])
        if yq:
            harvested += fetch_youtube(yq)
        feeds = reg.get("rss_feeds", [])
        if feeds:
            harvested += fetch_rss(feeds)

    print(f"Harvested {len(harvested)} posts.")

    inserted = 0
    for post in tqdm(harvested, desc="Processing"):
        try:
            post_id = sink.upsert_post(post)
            if not post_id:
                continue
            attrs = classify_and_extract(post.get("content",""), region_hint=None)
            if not attrs:
                continue
            address_parts = []
            if attrs.get("city") and attrs.get("state"):
                address_parts.append(f"{attrs['city']}, {attrs['state']}")
            if attrs.get("postal_code"):
                address_parts.append(attrs["postal_code"])
            address = ", ".join(address_parts) or None
            lat = lon = None
            if address:
                geo = geocode(address)
                if geo:
                    lat, lon = geo["lat"], geo["lon"]
            verified, note = verify(post.get("url"), post.get("author"))
            event = {
                "post_id": post_id,
                "title": None,
                "description": post.get("content","")[:8000],
                "organizer": post.get("author"),
                "source_type": "social" if post.get("platform") != "rss" else "rss",
                "event_date_start": attrs.get("event_date_start"),
                "event_date_end": attrs.get("event_date_end"),
                "tz": None,
                "address": address,
                "city": attrs.get("city"),
                "state": attrs.get("state"),
                "postal_code": attrs.get("postal_code"),
                "latitude": lat,
                "longitude": lon,
                "verified": verified,
                "verification_note": note,
                "region": None
            }
            if sink.insert_event(event):
                inserted += 1
        except Exception as e:
            print("error:", e)

    print(f"Inserted {inserted} events.")
