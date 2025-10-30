import os, argparse
from supabase import create_client

def main():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not (url and key):
        raise SystemExit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
    sb = create_client(url, key)

    ap = argparse.ArgumentParser()
    ap.add_argument("--state", type=str, default=None)
    ap.add_argument("--city", type=str, default=None)
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()

    q = sb.table("submissions").select("*").order("created_at", desc=True).limit(args.limit)
    if args.state: q = q.eq("state", args.state)
    if args.city: q = q.eq("city", args.city)
    res = q.execute()
    rows = res.data or []

    for r in rows:
        ev = {
            "post_id": None,
            "title": r.get("title"),
            "description": r.get("description"),
            "organizer": r.get("organizer"),
            "source_type": "submission",
            "event_date_start": r.get("event_date_start"),
            "event_date_end": r.get("event_date_end"),
            "tz": None,
            "address": r.get("address"),
            "city": r.get("city"),
            "state": r.get("state"),
            "postal_code": r.get("postal_code"),
            "latitude": r.get("latitude"),
            "longitude": r.get("longitude"),
            "verified": False,
            "verification_note": "from public submission",
            "region": None
        }
        ins = sb.table("events").insert(ev).execute()
        print("Promoted:", ins.data)

if __name__ == "__main__":
    main()
