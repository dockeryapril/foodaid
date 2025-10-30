TRUSTED_DOMAINS = [
    "acfb.org",     # Atlanta Community Food Bank
    "feedwm.org",   # Feeding America West Michigan
    "211.org", "211la.org", "211sandiego.org", "211wisconsin.org"  # 211 network (sample)
]

def verify(url: str, organizer: str = None):
    if not url: return False, None
    try:
        host = url.split("/")[2]
    except Exception:
        return False, None
    for d in TRUSTED_DOMAINS:
        if d and d in host:
            return True, f"Trusted domain: {d}"
    return False, None
