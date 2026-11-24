from sqlalchemy.orm import Session
from app.models import Campaign, Stream, StreamOffer
from app.keitaro_client import get_campaign_streams

async def fetch_streams(db: Session, campaign_id: int):
    remote_streams = await get_campaign_streams(campaign_id)

    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        campaign = Campaign(id=campaign_id, name=f"Campaign {campaign_id}")
        db.add(campaign)

    for rs in remote_streams:
        stream = db.query(Stream).filter(Stream.id == rs["id"]).first()
        if not stream:
            stream = Stream(id=rs["id"], campaign_id=campaign_id,
                            name=rs["name"], position=rs.get("position", 0),
                            has_offers=bool(rs.get("offers")))
            db.add(stream)
            db.flush()

        # Всегда обновляем флаг has_offers
        stream.has_offers = bool(rs.get("offers"))
        
        # Если в Keitaro офферы есть, remote_ids будет списком ID
        # Если офферов нет, remote_ids будет пустым множеством
        remote_offers = rs.get("offers") or []
        remote_ids = {o["offer_id"] for o in remote_offers}

        # 1. Помечаем как removed всё, что было активным локально, но пропало в Keitaro
        for link in stream.offers:
            if link.status == "active" and link.offer_id not in remote_ids:
                link.status = "removed"
                link.share = 0.0

        # 2. Добавляем/обновляем то, что пришло из Keitaro
        for ro in remote_offers:
            link = next((l for l in stream.offers
                         if l.offer_id == ro["offer_id"]), None)
            if link:
                link.status = "active"
                link.share = ro.get("share", 0)
            else:
                db.add(StreamOffer(stream_id=stream.id, offer_id=ro["offer_id"],
                                   share=ro.get("share", 0), status="active"))

    db.commit()