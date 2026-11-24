import asyncio
from app.database import SessionLocal
from app.services.sync import fetch_streams

async def main():
    db = SessionLocal()
    await fetch_streams(db, campaign_id=180)  # замени на реальный ID, когда создашь кампанию
    print("sync ok")

asyncio.run(main())