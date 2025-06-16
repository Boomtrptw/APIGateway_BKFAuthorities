from datetime import datetime
from sqlalchemy import Column, Date, Double, Integer, String, Boolean, TIMESTAMP
from utility.database.database import Base

class SystemList(Base):
    __tablename__ = "system_list"
    
    id = Column(String, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    seq = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)