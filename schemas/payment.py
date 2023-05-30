from datetime import datetime
from pydantic import BaseModel , Field
from typing import Optional

class orderCreated(BaseModel):
    id: str
    status: str
    link: str
    method: str
    statusCode: int = Field(ge=99, le=600)
    amount: float
    currency_code: str
    creationDate: Optional[datetime]

    class Config:
        #orm_mode = True
        schema_extra = {
            "example": {
                "id": "1Y064474HN8349825",
                "status": "PAYER_ACTION_REQUIRED",
                "link": "https://www.sandbox.paypal.com/checkoutnow?token=1Y064474HN8349825",
                "method": "GET",
                "amount": 100.0,
                "statusCode": 200,
                "currency_code": "USD",
                "creationDate": "2023/05/30 6:42:15.491688"
                }
        }
