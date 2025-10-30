# GitHub Actions Secrets (required)
For **Web CI**:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

For **Crawler**:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- (optional) `BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD`
- (optional) `MASTODON_BASE_URL`, `MASTODON_ACCESS_TOKEN`
- (optional) `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`
- (optional) `YOUTUBE_API_KEY`
- (optional, if SINK=gsheets) `GOOGLE_SHEETS_DOC_ID`, `GOOGLE_SERVICE_ACCOUNT_JSON` (JSON string or a base64 path—see note)
> Tip: If you plan to use Google Sheets, store the **entire service account JSON** as a single secret named `GOOGLE_SERVICE_ACCOUNT_JSON` and in the workflow write it to a file before running (we can add that in Step 6 if needed).
