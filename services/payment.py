from datetime import datetime
from sqlalchemy.orm import Session
from models.payment import orderCreated as orderCreatedModel
from schemas.payment import orderCreated


class orderCreatedService():
    
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
            creationDate=datetime.utcnow()
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
        order.creationDate = datetime.utcnow()
        self.db.commit()
        return

    def delete_order(self, id: str):
        self.db.query(orderCreatedModel).filter(orderCreatedModel.id == id).delete()
        self.db.commit()
        return
