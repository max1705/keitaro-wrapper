from sqlalchemy.orm import Session
from app.models import Stream
from app.keitaro_client import get_stream, update_stream

async def push_stream(db: Session, stream: Stream):
    if not stream.has_offers:
        return {"ok": False, "reason": "not an offers stream"}

    active = [l for l in stream.offers if l.status == "active"]
    payload = {
        "offers": [
            {"offer_id": l.offer_id, "share": l.share, "state": "active"}
            for l in active
        ]
    }
    await update_stream(stream.id, payload)
    stream.is_dirty = False
    db.commit()
    return {"ok": True}

async def cancel_stream(db: Session, stream: Stream):
    remote = await get_stream(stream.id)
    remote_offers = remote.get("offers", [])
    remote_ids = {o["offer_id"] for o in remote_offers}

    # удалить локальные привязки, которых нет в Keitaro
    for link in list(stream.offers):
        if link.offer_id not in remote_ids:
            db.delete(link)

    # восстановить/обновить из remote
    for ro in remote_offers:
        link = next((l for l in stream.offers
                     if l.offer_id == ro["offer_id"]), None)
        if link:
            link.status = "active"
            link.share = ro.get("share", 0)
        else:
            db.add(StreamOffer(stream_id=stream.id, offer_id=ro["offer_id"],
                               share=ro.get("share", 0), status="active"))

    stream.is_dirty = False
    db.commit()
    return {"ok": True}