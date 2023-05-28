from fastapi import FastAPI
from loguru import logger
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
import uvicorn
import sys
from config import appConfig, baseRoute, logMode, rotation

# Configurar el modo del log
logger.remove()  # Eliminar cualquier configuración anterior
logger.add(sys.stdout, level=logMode, format=" {time} - {level} - {message} - {module} - {function}")  # Agregar un manipulador para stdout en nivel logMode
logger.add(
    sink="logs/development.log",
    level=logMode,
    rotation=rotation,
    format=" {time} - {level} - {message} - {module} - {function}"
)

logger.info("STARTING SERVER OPERATION")

# Crear la instancia de la aplicación FastAPI
app = FastAPI(base_route=baseRoute)
# Agregar el middleware ErrorHandler
app.add_middleware(ErrorHandler)

logger.info("FINISHING SERVER START-UP")



@app.get('/', tags=['ping'])
def message():
    logger.info("Processing request...")
    response = {"body": "It is alive"}
    return JSONResponse(status_code=200, content=response)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=appConfig['port'])
