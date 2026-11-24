from sqlalchemy.orm import Session
from app.models import Stream, StreamOffer
from app.keitaro_client import get_offers

def recalc_shares(stream: Stream):
    """Пересчёт весов: pinned сохраняют share, остальные делят остаток до 100."""
    active = [o for o in stream.offers if o.status == "active"]
    removed = [o for o in stream.offers if o.status == "removed"]

    for o in removed:
        o.share = 0.0

    pinned = [o for o in active if o.is_pinned]
    unpinned = [o for o in active if not o.is_pinned]

    pinned_sum = sum(o.share for o in pinned)
    remaining = max(0.0, 100.0 - pinned_sum)

    if not unpinned:
        return

    if remaining <= 0:
        for o in unpinned:
            o.share = 0.0
        return

    base = int(remaining // len(unpinned))
    shares = [base] * len(unpinned)
    diff = int(remaining) - sum(shares)
    for i in range(diff):
        shares[i] += 1

    for o, s in zip(unpinned, shares):
        o.share = float(s)

def _find_link(stream: Stream, offer_id: int) -> StreamOffer | None:
    return next((l for l in stream.offers if l.offer_id == offer_id), None)

async def add_offer(db: Session, stream: Stream, offer_id: int):
    existing = _find_link(stream, offer_id)
    if existing:
        if existing.status == "removed":
            existing.status = "active"
        else:
            return
    else:
        offers = await get_offers()
        name = next((o["name"] for o in offers if o["id"] == offer_id), str(offer_id))
        db.add(StreamOffer(stream_id=stream.id, offer_id=offer_id,
                           offer_name=name, status="active", share=0.0))
        db.flush()
        db.refresh(stream)

    recalc_shares(stream)
    stream.is_dirty = True
    db.commit()

def remove_offer(db: Session, stream: Stream, offer_id: int):
    link = _find_link(stream, offer_id)
    if not link:
        return
    link.status = "removed"
    link.share = 0.0
    db.flush()
    recalc_shares(stream)
    stream.is_dirty = True
    db.commit()

def toggle_pin(db: Session, stream: Stream, offer_id: int):
    link = _find_link(stream, offer_id)
    if not link or link.status != "active":
        return
    link.is_pinned = not link.is_pinned
    db.flush()
    recalc_shares(stream)
    stream.is_dirty = True
    db.commit()

def bring_back(db: Session, stream: Stream, offer_id: int):
    link = _find_link(stream, offer_id)
    if not link or link.status != "removed":
        return
    link.status = "active"
    db.flush()
    recalc_shares(stream)
    stream.is_dirty = True
    db.commit()
