from fastapi import APIRouter, Response
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import requests
import base64
import json
import uuid
from config import appConfig, paypal_config, logger
from database.database import Session
from services.payment import OrderCreated as orderCreatedService
from models.payment import OrderCreated as orderCreatedModel
from schemas.payment import OrderCreated as orderCreated
from schemas.payment import RequestOrderCreated as RequestOrderCreated
from datetime import datetime
#from loguru import logger


HOST = str(appConfig['host'])
logger.debug(HOST)
BASE_ROUTE = appConfig['base_route']
PAYPAL_API_URL = paypal_config['paypal_api']
PAYPAL_CLIENT_ID = paypal_config['client_id']
PAYPAL_CLIENT_SECRET = paypal_config['client_secret']

routerPayment = APIRouter()


async def get_access_token():
    credentials = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }

    payload = 'grant_type=client_credentials'

    urlAccessToken = PAYPAL_API_URL + "/v1/oauth2/token"

    response = requests.post(urlAccessToken, headers=headers, data=payload)

    logger.warning(f"RESPONSE {response.status_code}")
    if 200 <= response.status_code <= 299:
        data = response.json()
        access_token = data.get('access_token')
        logger.warning("ACCESS TOKEN GENERATED")
        return access_token




@routerPayment.post("/create-order" , tags=['Create Order'], response_model=dict, status_code=201)
async def create_order(requestOrderCreated: RequestOrderCreated ) -> dict:
    logger.info(f"Start of the Request create-order")
    requestOrderCreated = requestOrderCreated.dict()
    logger.info(f"{requestOrderCreated}")
    access_token = await get_access_token()
    request_id = str(uuid.uuid4())
    monto = requestOrderCreated['amount']
    currency_code = requestOrderCreated['currency_code']
    paypal_api_url = f"{PAYPAL_API_URL}/v2/checkout/orders"
    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id': request_id,
        'Authorization': f'Bearer {access_token}',
    }
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": currency_code,
                    "value": monto
                }
            }
        ],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "return_url": f"{HOST}/capture-order",
                    "cancel_url": f"{HOST}/cancel-payment"
                }
            }
        }
    }

    response = requests.post(paypal_api_url, headers=headers, json=data)
    logger.info(response.status_code)
    data = response.json()
    logger.debug(f"{data} - {type(data)}")
    if 200 <= response.status_code <= 299:
        db = Session()
        rpta = {
            "id": data['id'],
            "status": data["status"],
            "link": data["links"][1]["href"],
            "method": data["links"][1]["method"],
            "amount": monto,
            "statusCode": response.status_code,
            "currency_code": currency_code,
            "user": requestOrderCreated['user'],
            "email": requestOrderCreated['email'],
            "phone_number" : requestOrderCreated['phone_number'],
            "description": requestOrderCreated['description']
        }
        order_created = orderCreatedModel(**rpta)
        orderCreatedService(db).create_order(order_created)
        logger.info(f"End  of the Request create-order")
        return JSONResponse(status_code=201, content=rpta)
    
    
@routerPayment.get('/capture-order', tags=['Capture Order'], response_model=dict, status_code=201)
async def capture_order(token: str, PayerID: str) -> dict:
    logger.info("Start Request capture-order")
    request_id = str(uuid.uuid4())
    access_token = await get_access_token()
    headers = {
        'PayPal-Request-Id': request_id,
        'Authorization':  f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    paypalUrlCapture = str(PAYPAL_API_URL) + "/v2/checkout/orders/" + str(token) + "/capture"
    logger.info(f"HEADERS - {headers} - {type(headers)}")
    logger.info(f"URL : {paypalUrlCapture}")

    try:
        response = requests.post(paypalUrlCapture,headers=headers)
        data = response.json()
        logger.info(response.status_code)
        logger.info(f"Response of Capture Order -- {data}")
        return JSONResponse(status_code=201, content=data)
    
    except requests.exceptions.RequestException as error:
        print(error)
        raise HTTPException(status_code=500, detail="Internal Server Error")