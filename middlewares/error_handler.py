from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from datetime import datetime
import random
import threading
import string

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID")
        if not correlation_id:
            correlation_id = self.generate_correlation_id()

        logger.bind(correlation_id=correlation_id)
        logger.info(f"SE CREA CORRELATION ID PARA LA TX : {correlation_id}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            response = JSONResponse(status_code=500, content={'error': str(e)})

        return response

    def generate_correlation_id(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        thread_id = threading.current_thread().ident
        random_digits = "".join(random.choices(string.digits, k=4))
        correlation_id = f"{timestamp}_{thread_id}_{random_digits}"
        return correlation_id
