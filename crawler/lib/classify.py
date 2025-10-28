from typing import Optional
from .text_utils import looks_like_resource, extract_dates, extract_city_state, extract_zip

def classify_and_extract(text: str, region_hint: str = None):
    if not looks_like_resource(text):
        return None
    start, end = extract_dates(text)
    city, state = extract_city_state(text)
    zc = extract_zip(text)
    result = {
        "event_date_start": start,
        "event_date_end": end,
        "city": city,
        "state": state,
        "postal_code": zc
    }
    if region_hint and not (city or state):
        result["region"] = region_hint
    return result
