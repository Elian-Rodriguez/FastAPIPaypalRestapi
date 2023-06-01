from datetime import datetime
from sqlalchemy.orm import Session
from models.payment import OrderCreated as orderCreatedModel
from models.payment import OrderCapture as OrderCaptureModel
from schemas.payment import  OrderCreated  as orderCreated
from schemas.payment import OrderCapture


class OrderCreated():
    
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_orders(self):
        result = self.db.query(orderCreatedModel).all()
        return result

    def get_order(self, id: str):
        result = self.db.query(orderCreatedModel).filter(orderCreatedModel.id == id).first()
        return result

    def create_order(self, order: orderCreated):
        new_order = orderCreatedModel(
            id=order.id,
            status=order.status,
            link=order.link,
            method=order.method,
            statusCode=order.statusCode,
            amount=order.amount,
            currency_code=order.currency_code,
            creationDate=datetime.utcnow(),
            user  = order.user,
            email= order.email,
            phone_number= order.phone_number,
            description  = order.description, 
        )
        self.db.add(new_order)
        self.db.commit()
        return

    def update_order(self, id: str, data: orderCreated):
        order = self.db.query(orderCreatedModel).filter(orderCreatedModel.id == id).first()
        order.status = data.status
        order.link = data.link
        order.method = data.method
        order.statusCode = data.statusCode
        order.amount = data.amount
        order.currency_code = data.currency_code
        order.creationDate = datetime.utcnow(),
        order.user  = data.user,
        order.email= data.email,
        order.phone_number= data.phone_number,
        order.description  = data.description, 
        self.db.commit()
        return

    def delete_order(self, id: str):
        self.db.query(orderCreatedModel).filter(orderCreatedModel.id == id).delete()
        self.db.commit()
        return



class OrderCapture():
    
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_orders(self):
        result = self.db.query(OrderCaptureModel).all()
        return result

    def get_order(self, id: str):
        result = self.db.query(OrderCaptureModel).filter(OrderCaptureModel.id == id).first()
        return result

    def create_order(self, order: OrderCapture):
        new_order = OrderCaptureModel(
            id=order.id,
            status=order.status,
            creationDate=datetime.utcnow(),
            email_address=order.email_address,
            account_id=order.account_id,
            given_name=order.given_name,
            surname=order.surname,
            country_code=order.country_code,
            admin_area_1=order.admin_area_1,
            postal_code=order.postal_code,
            currency_code=order.currency_code,
            value=order.value,
            commission=order.commission,
            currency_code_commission=order.currency_code_commission,
            net_amount=order.net_amount,
            net_currency_code_commission=order.net_currency_code_commission,
        )
        self.db.add(new_order)
        self.db.commit()
        return

    def update_order(self, id: str, data: OrderCapture):
        order = self.db.query(OrderCaptureModel).filter(OrderCaptureModel.id == id).first()
        order.status = data.status
        order.creationDate = datetime.utcnow()
        order.email_address = data.email_address
        order.account_id = data.account_id
        order.given_name = data.given_name
        order.surname = data.surname
        order.country_code = data.country_code
        order.admin_area_1 = data.admin_area_1
        order.postal_code = data.postal_code
        order.currency_code = data.currency_code
        order.value = data.value
        order.commission = data.commission
        order.currency_code_commission = data.currency_code_commission
        order.net_amount = data.net_amount
        order.net_currency_code_commission = data.net_currency_code_commission
        self.db.commit()
        return

    def delete_order(self, id: str):
        self.db.query(OrderCaptureModel).filter(OrderCaptureModel.id == id).delete()
        self.db.commit()
        return
