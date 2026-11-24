from app.database import SessionLocal
from app.models import Campaign, Stream, StreamOffer

db = SessionLocal()
for c in db.query(Campaign).all():
    print(f"Campaign {c.id} {c.name}")
    for s in c.streams:
        print(f"  Stream {s.id} {s.name} has_offers={s.has_offers} dirty={s.is_dirty}")
        for l in s.offers:
            print(f"    offer {l.offer_id} share={l.share} status={l.status} pinned={l.is_pinned}")