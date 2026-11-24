import asyncio
from app.keitaro_client import get_offers, get_campaigns, get_campaign_streams

async def main():
    offers = await get_offers()
    print(f"Офферов: {len(offers)}")
    print("Первый оффер:", offers[0] if offers else "нет")

    campaigns = await get_campaigns()
    print(f"\nКампаний: {len(campaigns)}")
    for c in campaigns[:5]:
        print(f"  id={c['id']} name={c.get('name')}")

    if campaigns:
        cid = campaigns[0]["id"]
        streams = await get_campaign_streams(cid)
        print(f"\nПотоки кампании {cid}:")
        for s in streams:
            print(f"  id={s['id']} name={s.get('name')} offers={len(s.get('offers') or [])}")

asyncio.run(main())