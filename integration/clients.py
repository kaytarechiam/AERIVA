"""Read-only partner clients. URLs and contracts require partner confirmation."""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen


class PartnerError(Exception):
    pass


def _get(base, path, params=None, key=None, timeout=10):
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Base URL mitra harus HTTPS")
    url = base.rstrip("/") + path
    if params:
        url += "?" + urlencode({k: v for k, v in params.items() if v is not None})
    headers = {"Accept": "application/json", "User-Agent": "AERIVA-Integration/0.1"}
    if key:
        headers["X-API-Key"] = key
    try:
        with urlopen(Request(url, headers=headers), timeout=timeout) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        raise PartnerError("Layanan mitra tidak tersedia atau respons bukan JSON") from exc


def list_events(**filters):
    return _get(os.getenv("LOCALLOOP_BASE_URL", "https://localloop.stei.fun"), "/api/public/events", filters, os.getenv("LOCALLOOP_API_KEY"))


def list_facilities(**filters):
    return _get(os.getenv("COURTSLOT_BASE_URL", "https://courtslot.stei.fun"), "/api/public/facilities", filters, os.getenv("COURTSLOT_API_KEY"))


def facility_availability(facility_id, start, end):
    return _get(os.getenv("COURTSLOT_BASE_URL", "https://courtslot.stei.fun"), "/api/public/facilities/" + quote(str(facility_id), safe="") + "/availability", {"start": start, "end": end}, os.getenv("COURTSLOT_API_KEY"))
