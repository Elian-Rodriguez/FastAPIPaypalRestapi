from fastapi import FastAPI
from fastapi import Request
#from loguru import logger
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from config import appConfig, baseRoute, logMode, rotation , logger
from routers.payment import routerPayment
from database.database import engine, Base
import uuid

BASE_ROUTE = appConfig['base_route']
logger.info("STARTING SERVER OPERATION")

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

app.title = appConfig['name']
app.version = appConfig['verssion']
logger.info(f"{app.title} - {app.version}")


app.include_router(routerPayment)
@app.middleware("http")
async def add_request_id(request, call_next):
    # Genera un identificador único para cada solicitud
    request.state.request_id = str(uuid.uuid4())
    logger.info(f"START REQUEST {request.state.request_id}")
    response = await call_next(request)
    return response

Base.metadata.create_all(bind=engine)
logger.info("FINALIZED START")

@app.get('/', tags=['ping'])
def message(request: Request):
    correlation_id = request.headers.get("X-Correlation-ID")
    logger.info(f"{correlation_id} -  Processing request... ")
    response = {"body": "It is alive"}
    logger.info(f"{correlation_id} -  Response {response}")
    return JSONResponse(status_code=200, content=response)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=appConfig['port'])