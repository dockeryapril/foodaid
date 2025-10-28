TRUSTED_DOMAINS = [
    # "acfb.org",      # Atlanta Community Food Bank (confirm)
    # "feedwm.org"     # Feeding America West Michigan (confirm)
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
