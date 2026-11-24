import asyncio
from app.keitaro_client import _req

async def main():
    # 1. кампания
    campaign = await _req("POST", "/campaigns", json={
        "name": "Test AU Campaign",
        "domain_id": 1813,
        "group_id": 10332,
        "traffic_source_id": 836,
    })
    cid = campaign["id"]
    print("campaign id:", cid)

    # 2. поток geo -> google
    s1 = await _req("POST", "/streams", json={
        "campaign_id": cid,
        "name": "Geo AU",
        "type": "regular",
        "schema": "redirect",
        "action_type": "http",
        "action_payload": "https://google.com",
        "filters": [{"name": "country", "mode": "accept", "payload": ["AU"]}],
    })
    print("stream1:", s1["id"])

    # 3. поток офферов (fallback)
    s2 = await _req("POST", "/streams", json={
        "campaign_id": cid,
        "name": "Offers",
        "type": "default",
        "schema": "landings",
        "offers": [{"offer_id": 18001, "share": 100, "state": "active"}],
    })
    print("stream2:", s2["id"])

asyncio.run(main())