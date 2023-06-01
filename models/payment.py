from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,Float
from database.database import Base

class OrderCreated(Base):
    __tablename__ = "ordersCreated"

    id = Column(String(18), primary_key=True)
    status = Column(String(22))
    link = Column(String(100))
    method = Column(String(22))
    statusCode = Column(Integer)
    amount = Column(Float)
    currency_code = Column(String(10))
    creationDate = Column(DateTime, default=datetime.utcnow)
    user  = Column(String(100))
    email = Column(String(100))
    phone_number = Column(String(20))
    description  = Column(String(100) )

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "link": self.link,
            "method": self.method,
            "statusCode": self.statusCode,
            "creationDate": self.creationDate.strftime("%Y-%m-%d %H:%M:%S"),
            "user": self.user,
            "email": self.email,
            "phone_number" : self.phone_number,
            "description": self.description,
        }


class OrderCapture(Base):
    __tablename__ = "ordersCapture"

    id = Column(String(18), primary_key=True)
    status = Column(String(22))
    creationDate = Column(DateTime, default=datetime.utcnow)
    email_address= Column(String(250))
    account_id = Column(String(100))
    given_name = Column(String(100))
    surname = Column(String(100))
    country_code = Column(String(10))
    admin_area_1 = Column(String(50))
    postal_code = Column(Integer)
    currency_code = Column(String(10))
    value  = Column(Float)
    commission  = Column(Float)
    currency_code_commission = Column(String(10))
    net_amount  = Column(Float)
    net_currency_code_commission = Column(String(10))
  

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "creationDate": self.creationDate.strftime("%Y-%m-%d %H:%M:%S"),
            "email_address": self.email_address,
            "account_id": self.account_id,
            "given_name": self.given_name,
            "surname": self.surname,
            "country_code": self.country_code,
            "admin_area_1": self.admin_area_1,
            "postal_code": self.postal_code,
            "currency_code": self.currency_code,
            "value": self.value,
            "commission": self.commission,
            "currency_code_commission": self.currency_code_commission,
            "net_amount": self.net_amount,
            "net_currency_code_commission": self.net_currency_code_commission,
        }

