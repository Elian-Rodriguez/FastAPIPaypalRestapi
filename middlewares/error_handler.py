from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from config import logger
from datetime import datetime
import random
import threading
import string
from starlette.datastructures import Headers

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        logger.info("Request initiated")
        correlation_id = request.headers.get("X-Correlation-ID")
        logger.info(f"{request.url.path}")
        if not correlation_id:
            if 'doc' not in str(request.url.path) :
                logger.error("Did not send Transaction ID ")
                return JSONResponse(status_code=400, content={'Error': 'Did not send Transaction ID '})
            else :
                correlation_id = 525
                response = await call_next(request)
                return response



        logger.info(f"{correlation_id} - API Invoked: {request.url.path}")
        logger.info(f"{correlation_id} - Request Headers : {request.headers}")


        try:
            body = await request.body()
            body_str = body.decode()
            logger.info(f"{correlation_id} - Request Body: {body_str}")
            

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            response = JSONResponse(status_code=500, content={'error': str(e)})


        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            response = JSONResponse(status_code=500, content={'error': str(e)})

        return response

