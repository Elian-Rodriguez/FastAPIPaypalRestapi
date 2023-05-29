from fastapi import FastAPI
from fastapi import Request
from loguru import logger
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
import uvicorn
from config import appConfig, baseRoute, logMode, rotation, logger
from routers.payment import routerPayment


BASE_ROUTE = appConfig['base_route']
logger.info("STARTING SERVER OPERATION")

# Crear la instancia de la aplicación FastAPI
app = FastAPI()
# Agregar el middleware ErrorHandler
#app.add_middleware(ErrorHandler)
app.include_router(routerPayment)




@app.get(BASE_ROUTE+'/', tags=['ping'])
def message(request: Request):
    correlation_id = request.headers.get("X-Correlation-ID")
    logger.info(f"{correlation_id} -  Processing request... ")
    response = {"body": "It is alive"}
    logger.info(f"{correlation_id} -  Response {response}")
    return JSONResponse(status_code=200, content=response)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=appConfig['port'])
