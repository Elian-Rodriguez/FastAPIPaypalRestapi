from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Response
import requests
from config import appConfig, logger, paypal_config
import base64
import json
import uuid


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

    urlAccesToken = PAYPAL_API_URL + "/v1/oauth2/token"

    response = requests.post(urlAccesToken, headers=headers, data=payload)

    logger.warning(f"RESPONSE {response.status_code}")
    if response.status_code >= 200 and response.status_code <= 299:
        data = response.json()
        access_token = data.get('access_token')
        logger.warning("ACCES TOKEN GENERADO ")
        return access_token



@routerPayment.post("/create-order")
async def create_order(response: Response):
    access_token = await get_access_token()
    request_id = str(uuid.uuid4())
    paypal_api_url = f"{PAYPAL_API_URL}/v2/checkout/orders"
    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id': request_id,
        'Authorization': f'Bearer {access_token}',
        }
    data = """
{
  "intent": "CAPTURE",
  "purchase_units": [
    {
      
      "amount": {
        "currency_code": "USD",
        "value": "100.00"
      }
    }
  ],
  "payment_source": {
    "paypal": {
      "experience_context": {
    
        "return_url": "https://example.com/returnUrl",
        "cancel_url": "https://example.com/cancelUrl"
      }
    }
  }
}
"""

    response = requests.post(paypal_api_url, headers=headers, data=data)
    logger.info(response.status_code)
    if response.status_code >= 200 and response.status_code <= 299:
        data = response.json()
        logger.debug(f"{data}")
   