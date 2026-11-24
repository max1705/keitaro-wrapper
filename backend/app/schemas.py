from pydantic import BaseModel

class OfferOut(BaseModel):
    id: int
    offer_id: int
    offer_name: str | None = None
    share: float
    is_pinned: bool
    status: str

    class Config:
        from_attributes = True

class StreamOut(BaseModel):
    id: int
    name: str
    position: int
    has_offers: bool
    is_dirty: bool
    offers: list[OfferOut] = []

    class Config:
        from_attributes = True

class AddOfferRequest(BaseModel):
    offer_id: int

class CreateCampaignRequest(BaseModel):
    name: str
    geo: str          # например "AU"
    offer_id: int

class CampaignOut(BaseModel):
    id: int
    name: str
    alias: str | None = None

    class Config:
        from_attributes = True