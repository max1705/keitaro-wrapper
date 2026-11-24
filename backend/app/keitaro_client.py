import httpx
from app.config import settings

BASE = settings.keitaro_api_url.rstrip("/")
KEY = settings.keitaro_api_key

async def _req(method: str, path: str, **kwargs):
    async with httpx.AsyncClient() as client:
        r = await client.request(
            method,
            f"{BASE}{path}",
            headers={"Api-Key": KEY, "Content-Type": "application/json"},
            timeout=30,
            **kwargs,
        )
        r.raise_for_status()
        return r.json()

async def get_campaigns(offset: int = 0, limit: int = 50):
    return await _req("GET", f"/campaigns?offset={offset}&limit={limit}")

async def get_campaign_streams(campaign_id: int):
    return await _req("GET", f"/campaigns/{campaign_id}/streams")

async def get_stream(stream_id: int):
    return await _req("GET", f"/streams/{stream_id}")

async def get_offers():
    return await _req("GET", "/offers")

async def update_stream(stream_id: int, payload: dict):
    return await _req("PUT", f"/streams/{stream_id}", json=payload)