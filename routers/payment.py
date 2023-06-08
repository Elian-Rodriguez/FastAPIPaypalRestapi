from fastapi import APIRouter, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import requests
import base64
import json
import uuid
from config import appConfig, paypal_config, logger
from database.database import Session
from services.payment import OrderCreated as orderCreatedService
from services.payment import OrderCapture as OrderCapturerService
from models.payment import OrderCreated as orderCreatedModel
from models.payment import OrderCapture as OrderCaptureModel
from schemas.payment import OrderCreated as orderCreated
from schemas.payment import RequestOrderCreated as RequestOrderCreated
from schemas.payment import OrderCapture as schemasOrderCapture
from datetime import datetime
from typing import Dict, Any, Union
from fastapi import Request

HOST = str(appConfig['host'])
logger.debug(HOST)
BASE_ROUTE = appConfig['base_route']
PAYPAL_API_URL = paypal_config['paypal_api']
PAYPAL_CLIENT_ID = paypal_config['client_id']
PAYPAL_CLIENT_SECRET = paypal_config['client_secret']

routerPayment = APIRouter()


async def get_access_token(idRequest):
    logger.info(f" [{idRequest}] STARTING ACCESS TOKEN GENERATION")
    credentials = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}'
    }

    payload = 'grant_type=client_credentials'

    urlAccessToken = PAYPAL_API_URL + "/v1/oauth2/token"

    response = requests.post(urlAccessToken, headers=headers, data=payload)

    logger.warning(f" [{idRequest}] RESPONSE {response.status_code}")
    if 200 <= response.status_code <= 299:
        data = response.json()
        access_token = data.get('access_token')
        logger.warning(f" [{idRequest}] ACCESS TOKEN GENERATED")
        logger.info(f" [{idRequest}]  END ACCESS TOKEN GENERATION")
        return access_token


@routerPayment.post("/create-order", tags=['Create Order'], response_model=dict, status_code=201)
async def create_order(requestOrderCreated: RequestOrderCreated, request: Request) -> dict:
    logger.info(f" [{request.state.request_id}] Start of the Request create-order")
    requestOrderCreated = requestOrderCreated.dict()
    logger.info(f"{requestOrderCreated}")
    access_token = await get_access_token(request.state.request_id)
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
    logger.info(f" [{request.state.request_id}]  RESPONSE CODE : {response.status_code}")
    data = response.json()
    logger.info(f" [{request.state.request_id}] RESPONSE BODY {data} - {type(data)}")
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
            "phone_number": requestOrderCreated['phone_number'],
            "description": requestOrderCreated['description']
        }
        order_created = orderCreatedModel(**rpta)
        insert = orderCreatedService(db).create_order(order_created)
        logger.info(f" [{request.state.request_id}]  End  of the Request create-order {insert} {type(insert)}")
        return JSONResponse(status_code=201, content=rpta)


@routerPayment.get('/capture-order', tags=['Capture Order'], response_model=Union[schemasOrderCapture, Dict[str, Any]], status_code=201)
async def capture_order(token: str, PayerID: str, request: Request) -> Union[schemasOrderCapture, Dict[str, Any]]:
    logger.info(" [{request.state.request_id}] Start Request capture-order")
    request_id = str(uuid.uuid4())
    access_token = await get_access_token(request.state.request_id)
    headers = {
        'PayPal-Request-Id': request_id,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    paypalUrlCapture = str(PAYPAL_API_URL) + "/v2/checkout/orders/" + str(token) + "/capture"
    logger.info(f" [{request.state.request_id}] HEADERS - {headers} - {type(headers)}")
    logger.info(f" [{request.state.request_id}] URL : {paypalUrlCapture}")

    try:
        response = requests.post(paypalUrlCapture, headers=headers)
        data = response.json()
        logger.info(f" [{request.state.request_id}] Response Code of Capture Order -- {response.status_code}")
        logger.info(f" [{request.state.request_id}] Response of Capture Order -- {data}")
        if 200 <= response.status_code <= 299:
            db = Session()
            rta = {
                "id": data["id"],
                "status": data["status"],
                "email_address": data["payer"]["email_address"],
                "account_id": data["payer"]["payer_id"],
                "given_name": data["payer"]["name"]["given_name"],
                "surname": data["payer"]["name"]["surname"],
                "country_code": data["payer"]["address"]["country_code"],
                "admin_area_1": data["purchase_units"][0]["shipping"]["address"]["admin_area_1"],
                "postal_code": data["purchase_units"][0]["shipping"]["address"]["postal_code"],
                "currency_code": data["purchase_units"][0]["payments"]["captures"][0]["amount"]["currency_code"],
                "value": data["purchase_units"][0]["payments"]["captures"][0]["amount"]["value"],
                "commission": data["purchase_units"][0]["payments"]["captures"][0]["seller_receivable_breakdown"]["paypal_fee"]["value"],
                "currency_code_commission": data["purchase_units"][0]["payments"]["captures"][0]["seller_receivable_breakdown"]["paypal_fee"]["currency_code"],
                "net_amount": data["purchase_units"][0]["payments"]["captures"][0]["seller_receivable_breakdown"]["net_amount"]["value"],
                "net_currency_code_commission": data["purchase_units"][0]["payments"]["captures"][0]["seller_receivable_breakdown"]["net_amount"]["currency_code"]
                }

            ordercapturer = OrderCaptureModel(**rta)
            logger.info(f" [{request.state.request_id}] Generating Insert")
            OrderCapturerService(db).create_order(ordercapturer)
            logger.info(f" [{request.state.request_id}] Validating Insert")
            result = OrderCapturerService(db).get_order(data["id"])
            logger.info(f" [{request.state.request_id}] Response {result}")

            logger.info(f" [{request.state.request_id}] End Request capture-order")

            return JSONResponse(status_code=201, content=jsonable_encoder(result))
        
        else:
            logger.info(f" [{request.state.request_id}] End Request capture-order")
            return JSONResponse(status_code=response.status_code , content=data)

    except requests.exceptions.RequestException as error:
        logger.error(f" [{request.state.request_id}]  ERROR IN CAPTURE ORDER {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@routerPayment.get('/cancel-payment', tags=['Cancel Order'], response_model=dict, status_code=201)
async def Cancel_order(token: str, request: Request) -> dict:
    logger.info(f" [{request.state.request_id}] Start Request ancel-payment-order")
    logger.info(f" [{request.state.request_id}] Failed Transaction Customer Canceled Transaction Token : {token} ")
    logger.info(f"  [{request.state.request_id}] RESPONSE IN CANCEL ORDER : message: Failed Transaction Customer Canceled Transaction")
    logger.info(f" [{request.state.request_id}] Start Request ancel-payment-order")
    return JSONResponse(status_code=401, content={"message": "Failed Transaction Customer Canceled Transaction"})
