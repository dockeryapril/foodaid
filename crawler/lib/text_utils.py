import re
from dateutil import tz
import dateparser

EN_KEYWORDS = [
    "food distribution","free food","food pantry","mobile pantry",
    "produce giveaway","food box","community fridge","meal kit",
    "drive-thru","drive thru","first come","bring id","no id",
    "school meals","sun bucks","wic","ebt"
]

ES_KEYWORDS = [
    "comida gratis","despensa","reparto de alimentos","entrega de alimentos",
    "banquete móvil","caja de alimentos","sin identificación","primero en llegar",
    "comedor","alimentos escolares","wic","ebt"
]

CITY_STATE_PATTERN = re.compile(r'\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*),\s*([A-Z]{2})\b')
ZIP_PATTERN = re.compile(r'\b\d{5}(?:-\d{4})?\b')

def looks_like_resource(text: str) -> bool:
    s = text.lower()
    return any(k in s for k in EN_KEYWORDS) or any(k in s for k in ES_KEYWORDS)

def extract_dates(text: str, ref_tz: str = "America/New_York"):
    settings = {"PREFER_DATES_FROM": "future", "RELATIVE_BASE": None}
    candidates = re.split(r'[\n\.;]', text)
    wins = []
    for c in candidates:
        d = dateparser.parse(c, settings=settings)
        if d:
            wins.append(d)
    if not wins:
        return None, None
    tzinfo = tz.gettz(ref_tz)
    start = wins[0].replace(tzinfo=tzinfo)
    return start, None

def extract_city_state(text: str):
    m = CITY_STATE_PATTERN.search(text)
    if m:
        return m.group(1), m.group(2)
    return None, None

def extract_zip(text: str):
    m = ZIP_PATTERN.search(text)
    if m:
        return m.group(0)
    return None
