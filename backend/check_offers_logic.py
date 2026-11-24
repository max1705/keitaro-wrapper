import asyncio
from app.database import SessionLocal
from app.models import Stream
from app.services.offers import add_offer, remove_offer, bring_back, toggle_pin

async def main():
    db = SessionLocal()
    stream = db.query(Stream).filter(Stream.id == 340).first()

    print("before:", [(l.offer_id, l.share, l.status) for l in stream.offer_links])

    # добавим второй оффер
    await add_offer(db, stream, 18002)
    print("after add:", [(l.offer_id, l.share, l.status) for l in stream.offer_links])
    print("dirty:", stream.is_dirty)

    # запиним первый
    toggle_pin(db, stream, 18001)
    print("after pin:", [(l.offer_id, l.share, l.is_pinned) for l in stream.offer_links])

    # удалим второй
    remove_offer(db, stream, 18002)
    print("after remove:", [(l.offer_id, l.share, l.status) for l in stream.offer_links])

    # вернём
    bring_back(db, stream, 18002)
    print("after bring back:", [(l.offer_id, l.share, l.status) for l in stream.offer_links])

asyncio.run(main())