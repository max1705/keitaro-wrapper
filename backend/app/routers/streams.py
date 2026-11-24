from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Stream
from app.schemas import StreamOut, AddOfferRequest
from app.services import offers as offers_service
from app.services.push import push_stream, cancel_stream
from app.keitaro_client import get_offers

router = APIRouter(prefix="/streams", tags=["streams"])

def _get_stream(stream_id: int, db: Session) -> Stream:
    stream = db.query(Stream).filter(Stream.id == stream_id).first()
    if not stream:
        raise HTTPException(404, "stream not found")
    return stream

@router.get("/{stream_id}", response_model=StreamOut)
def get_stream(stream_id: int, db: Session = Depends(get_db)):
    return _get_stream(stream_id, db)

@router.get("/offers/catalog")
async def offers_catalog():
    return await get_offers()

@router.post("/{stream_id}/offers")
async def add_offer(stream_id: int, req: AddOfferRequest, db: Session = Depends(get_db)):
    stream = _get_stream(stream_id, db)
    await offers_service.add_offer(db, stream, req.offer_id)
    return {"ok": True}

@router.delete("/{stream_id}/offers/{offer_id}")
def remove_offer(stream_id: int, offer_id: int, db: Session = Depends(get_db)):
    stream = _get_stream(stream_id, db)
    offers_service.remove_offer(db, stream, offer_id)
    return {"ok": True}

@router.post("/{stream_id}/offers/{offer_id}/bring-back")
def bring_back(stream_id: int, offer_id: int, db: Session = Depends(get_db)):
    stream = _get_stream(stream_id, db)
    offers_service.bring_back(db, stream, offer_id)
    return {"ok": True}

@router.post("/{stream_id}/offers/{offer_id}/pin")
def toggle_pin(stream_id: int, offer_id: int, db: Session = Depends(get_db)):
    stream = _get_stream(stream_id, db)
    offers_service.toggle_pin(db, stream, offer_id)
    return {"ok": True}

@router.post("/{stream_id}/push")
async def push(stream_id: int, db: Session = Depends(get_db)):
    stream = _get_stream(stream_id, db)
    return await push_stream(db, stream)

@router.post("/{stream_id}/cancel")
async def cancel(stream_id: int, db: Session = Depends(get_db)):
    stream = _get_stream(stream_id, db)
    return await cancel_stream(db, stream)
    