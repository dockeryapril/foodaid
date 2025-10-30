import os
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def geocode(address: str):
    provider = os.getenv("GEOCODER_PROVIDER","nominatim").lower()
    if provider == "nominatim":
        geolocator = Nominatim(user_agent="food-help-crawler")
        geocode_fn = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        loc = geocode_fn(address)
        if not loc:
            return None
        return {"lat": loc.latitude, "lon": loc.longitude, "formatted": loc.address}
    return None
