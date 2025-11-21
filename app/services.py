# app/services.py
import os

import httpx
from dotenv import load_dotenv

from app.cache import get_cached, set_cached

API_URL = "https://currate.ru/api/"

load_dotenv()
API_KEY = os.getenv("CURRATE_API_KEY")
client = httpx.AsyncClient(timeout=10.0)


async def get_rate(from_curr: str, to_curr: str):
    pair = f"{from_curr}{to_curr}"
    cached = get_cached(pair)
    if cached:
        return cached

    params = {"get": "rates", "pairs": pair, "key": API_KEY}

    try:
        resp = await client.get(API_URL, params=params)
        resp.raise_for_status()
    except Exception:
        return None

    data = resp.json()
    if "data" not in data or pair not in data["data"]:
        return None

    rate = float(data["data"][pair])
    set_cached(pair, rate)
    return rate


async def get_currency_list():
    params = {"get": "currency_list", "key": API_KEY}
    resp = await client.get(API_URL, params=params)
    data = resp.json()
    return data.get("data", [])
