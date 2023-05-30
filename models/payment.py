from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,Float
from database.database import Base

class orderCreated(Base):
    __tablename__ = "ordersCreated"

    id = Column(String(18), primary_key=True)
    status = Column(String(22))
    link = Column(String(100))
    method = Column(String(22))
    statusCode = Column(Integer)
    amount = Column(Float)
    currency_code = Column(String(10))
    creationDate = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "link": self.link,
            "method": self.method,
            "statusCode": self.statusCode,
            "creationDate": self.creationDate.strftime("%Y-%m-%d %H:%M:%S")
        }
