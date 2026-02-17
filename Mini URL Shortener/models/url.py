from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

Base = declarative_base()

def get_ist_time():
    """Get current time in IST timezone"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

class URLMapping(Base):
    __tablename__ = "url_mappings"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(2048), unique=True, index=True)
    short_code = Column(String(10), unique=True, index=True)
    created_at = Column(DateTime, default=get_ist_time)
    click_count = Column(Integer, default=0)

    class Config:
        from_attributes = True