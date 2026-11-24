from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Campaign, Stream
from app.schemas import StreamOut, CampaignOut, CreateCampaignRequest
from app.services.sync import fetch_streams
from app.keitaro_client import _req, get_campaigns

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("", response_model=list[CampaignOut])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()

@router.post("/sync")
async def sync_campaigns(db: Session = Depends(get_db)):
    remote = await get_campaigns()
    for rc in remote:
        c = db.query(Campaign).filter(Campaign.id == rc["id"]).first()
        if not c:
            db.add(Campaign(id=rc["id"], name=rc.get("name", f"Campaign {rc['id']}"),
                            alias=rc.get("alias")))
    db.commit()
    return {"ok": True, "count": len(remote)}

@router.post("/{campaign_id}/fetch")
async def fetch(campaign_id: int, db: Session = Depends(get_db)):
    await fetch_streams(db, campaign_id)
    return {"ok": True}

@router.get("/{campaign_id}/streams", response_model=list[StreamOut])
def get_streams(campaign_id: int, db: Session = Depends(get_db)):
    streams = (db.query(Stream)
               .filter(Stream.campaign_id == campaign_id)
               .order_by(Stream.position)
               .all())
    # Поток с офферами — первым
    return sorted(streams, key=lambda s: (not s.has_offers, s.position))

@router.post("/create")
async def create_campaign(req: CreateCampaignRequest, db: Session = Depends(get_db)):
    # 1. Создаём кампанию в Keitaro
    campaign = await _req("POST", "/campaigns", json={
        "name": req.name,
        "domain_id": 1813,
        "group_id": 10332,
        "traffic_source_id": 836,
    })
    cid = campaign["id"]

    # 2. Разбираем гео (например, "MX,AU,RO" -> ["MX", "AU", "RO"])
    geo_list = [g.strip() for g in req.geo.split(",") if g.strip()]

    # 3. Первый поток: гео -> Google
    await _req("POST", "/streams", json={
        "campaign_id": cid,
        "name": f"Geo {req.geo}",
        "type": "regular",
        "schema": "redirect",
        "action_type": "http",
        "action_payload": "https://google.com",
        "filters": [{"name": "country", "mode": "accept", "payload": geo_list}],
    })

    # 4. Второй поток: офферы
    await _req("POST", "/streams", json={
        "campaign_id": cid,
        "name": "Offers",
        "type": "default",
        "schema": "landings",
        "offers": [{"offer_id": req.offer_id, "share": 100, "state": "active"}],
    })

    # 5. Подтягиваем созданные потоки в нашу локальную БД
    await fetch_streams(db, cid)

    return {"ok": True, "campaign_id": cid}