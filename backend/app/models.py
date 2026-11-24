from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    alias = Column(String)
    streams = relationship("Stream", back_populates="campaign", cascade="all, delete-orphan")

class Stream(Base):
    __tablename__ = "streams"
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    name = Column(String, nullable=False)
    position = Column(Integer, default=0)
    has_offers = Column(Boolean, default=False)
    is_dirty = Column(Boolean, default=False)
    campaign = relationship("Campaign", back_populates="streams")
    offers = relationship("StreamOffer", back_populates="stream", cascade="all, delete-orphan")

class StreamOffer(Base):
    __tablename__ = "stream_offers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stream_id = Column(Integer, ForeignKey("streams.id"))
    offer_id = Column(Integer, nullable=False)
    offer_name = Column(String)
    share = Column(Float, default=0.0)
    is_pinned = Column(Boolean, default=False)
    status = Column(String, default="active")  # active | removed
    stream = relationship("Stream", back_populates="offers")