from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class OrderCreated(BaseModel):
    id: str = Field(max_length=18)
    status: str = Field(max_length=22)
    link: str = Field(max_length=100)
    method: str = Field(max_length=22)
    statusCode: int = Field(ge=99, le=600)
    amount: float = Field(ge=0, le=1200)
    currency_code: str = Field(max_length=10)
    creationDate: Optional[datetime]
    user : str = Field(min_length=5 ,max_length=100)
    email: str = Field(min_length=5, max_length=100)
    phone_number: str = Field(min_length=10, max_length=20)
    description : str = Field(min_length=5 , max_length=100) 


    class Config:
        schema_extra = {
            "example": {
                "id": "1Y064474HN8349825",
                "status": "PAYER_ACTION_REQUIRED",
                "link": "https://www.sandbox.paypal.com/checkoutnow?token=1Y064474HN8349825",
                "method": "GET",
                "amount": 100.0,
                "statusCode": 200,
                "currency_code": "USD",
                "creationDate": "2023-05-30 06:42:15.491688",
                "user": "Someone Unknown",
                "email": "Unknown@gmail.com",
                "phone_number" : "33333333333",
                "description": "Business Bets"
            }
        }



class RequestOrderCreated(BaseModel):
    amount: float = Field(ge=0, le=1200)
    currency_code: str = Field(max_length=10)
    user : str = Field(min_length=5 ,max_length=100)
    email: str = Field(min_length=5, max_length=100)
    phone_number: str = Field(min_length=10, max_length=20)
    description : str = Field(min_length=5 , max_length=100) 


    class Config:
        schema_extra = {
            "example": {
                "amount": 100.0,
                "currency_code": "USD",
                "user": "Someone Unknown",
                "email": "Unknown@gmail.com",
                "phone_number" : "33333333333",
                "description": "Business Bets"
            }
        }