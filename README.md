# Food Help Crawler (GA + West MI first)
Find and surface real-time **food assistance posts** (food distributions, pantries, mutual-aid drops, school meals) from open platforms and official sources. Store normalized events in **Supabase** or **Google Sheets**, and show them on a **Next.js** map with filters.

## Quickstart Overview
1) Create a Supabase project → run `supabase/schema.sql`.
2) Choose output sink in `.env` (`SINK=supabase` or `SINK=gsheets`).
3) Run the crawler (Python) to populate data.
4) Start the web app (Next.js) to view a map/list of events.
5) Public submissions: `/submit` writes to `public.submissions` for moderation.

## Regions
Seeded for **Georgia** and **Grand Rapids/West Michigan, MI** via `crawler/config/sources.yaml`.

### Verifier & Sources
- Trusted domains live in `crawler/lib/verifier.py`. Matches on host substring; add your local partners here for instant “Verified”.
- Region seeds & feeds live in `crawler/config/sources.yaml`. Add official food bank RSS and city 211 pages.

### Google Sheets mode
- Set `SINK=gsheets` and provide `GOOGLE_SHEETS_DOC_ID` + `GOOGLE_SERVICE_ACCOUNT_JSON`.
- In CI we auto-write `service_account.json` from the GitHub Secret if provided.

## ToS & Legal
- No scraping of forbidden platforms. APIs/RSS only.
- Respect geocoding provider rate limits.

## Output options
- **Supabase** (default) — full DB with web map.
- **Google Sheets** — quick-and-shareable. Enable Sheets API, create a service account, share the sheet with it, and set `SINK=gsheets` with `GOOGLE_SHEETS_DOC_ID` + `GOOGLE_SERVICE_ACCOUNT_JSON` path.

