import os
from typing import Any, Dict, Optional

from .db import get_client, upsert_post as sb_upsert_post, insert_event as sb_insert_event

class SupabaseSink:
    def __init__(self):
        self.sb = get_client()
    def upsert_post(self, post: Dict[str, Any]) -> Optional[int]:
        return sb_upsert_post(self.sb, post)
    def insert_event(self, ev: Dict[str, Any]) -> Optional[int]:
        return sb_insert_event(self.sb, ev)

import gspread
from gspread.exceptions import WorksheetNotFound

POSTS_HEADERS = ["id","platform","external_id","author","url","content","lang","posted_at"]
EVENTS_HEADERS = ["id","post_id","title","description","organizer","source_type","event_date_start","event_date_end","tz","address","city","state","postal_code","latitude","longitude","verified","verification_note","region","created_at"]

def _ensure_ws(sh, title, headers):
    try:
        ws = sh.worksheet(title)
    except WorksheetNotFound:
        ws = sh.add_worksheet(title=title, rows=2000, cols=len(headers)+2)
        ws.append_row(headers, value_input_option="USER_ENTERED")
    try:
        first_row = ws.row_values(1)
        if first_row != headers:
            ws.delete_rows(1)
            ws.insert_row(headers, 1, value_input_option="USER_ENTERED")
    except Exception:
        pass
    return ws

class GoogleSheetsSink:
    def __init__(self):
        doc_id = os.getenv("GOOGLE_SHEETS_DOC_ID")
        sa_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "./service_account.json")
        if not doc_id or not os.path.exists(sa_path):
            raise RuntimeError("Google Sheets sink requires GOOGLE_SHEETS_DOC_ID and GOOGLE_SERVICE_ACCOUNT_JSON")
        self.gc = gspread.service_account(filename=sa_path)
        self.sh = self.gc.open_by_key(doc_id)
        self.ws_posts = _ensure_ws(self.sh, "posts", POSTS_HEADERS)
        self.ws_events = _ensure_ws(self.sh, "events", EVENTS_HEADERS)
        self._post_row_map = {}
    def upsert_post(self, post: Dict[str, Any]) -> Optional[int]:
        key = f"{post.get('platform')}::{post.get('external_id')}"
        if key in self._post_row_map:
            return self._post_row_map[key]
        row = ["", post.get("platform"), post.get("external_id"), post.get("author"), post.get("url"), post.get("content"), post.get("lang","en"), post.get("posted_at")]
        self.ws_posts.append_row(row, value_input_option="USER_ENTERED", table_range="A1")
        row_count = len(self.ws_posts.get_all_values())
        rid = row_count
        self._post_row_map[key] = rid
        return rid
    def insert_event(self, ev: Dict[str, Any]) -> Optional[int]:
        row = ["", ev.get("post_id"), ev.get("title"), ev.get("description"), ev.get("organizer"), ev.get("source_type"), str(ev.get("event_date_start") or ""), str(ev.get("event_date_end") or ""), ev.get("tz"), ev.get("address"), ev.get("city"), ev.get("state"), ev.get("postal_code"), ev.get("latitude"), ev.get("longitude"), ev.get("verified"), ev.get("verification_note"), ev.get("region"), ""]
        self.ws_events.append_row(row, value_input_option="USER_ENTERED", table_range="A1")
        row_count = len(self.ws_events.get_all_values())
        return row_count

def get_sink():
    mode = os.getenv("SINK", "supabase").lower()
    if mode == "gsheets":
        return GoogleSheetsSink()
    return SupabaseSink()
