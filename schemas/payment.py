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

class OrderCapture(BaseModel):
    id: str = Field(max_length=18)
    status: str = Field(max_length=22)
    creationDate: Optional[datetime]
    email_address: str = Field(max_length=250)
    account_id: str = Field(max_length=100)
    given_name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    country_code: str = Field(max_length=10)
    admin_area_1: str = Field(max_length=50)
    postal_code: int
    currency_code: str = Field(max_length=10)
    value: float
    commission: float
    currency_code_commission: str = Field(max_length=10)
    net_amount: float
    net_currency_code_commission: str = Field(max_length=10)

    class Config:
        schema_extra = {
            "example": {
                "id": "39U70013RT093303F",
                "status": "COMPLETED",
                "creationDate": "2023-05-31 12:34:56",
                "email_address": "sb-mlyaw26105024@personal.example.com",
                "account_id": "BZDWAA48R8P56",
                "given_name": "John",
                "surname": "Doe",
                "country_code": "CO",
                "admin_area_1": "Bogota",
                "postal_code": 110111,
                "currency_code": "USD",
                "value": 100.0,
                "commission": 5.74,
                "currency_code_commission": "USD",
                "net_amount": 1134.90,
                "net_currency_code_commission": "USD"
            }
        }