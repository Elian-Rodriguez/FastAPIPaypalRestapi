import yaml
from loguru import logger
import sys 
def get_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

config = get_config()

# Configuración de las bases de datos
mysql_config = config.get('mysql', {})

# Configuración de la API de PayPal
paypal_config = config.get('paypal', {})

# Configuración de la aplicación
appConfig = config.get('app', {})
logMode = appConfig.get('log_mode')
rotation = appConfig.get('rotation')
version = appConfig.get('version')
port = appConfig.get('port')
baseRoute = appConfig.get('base_route')
appName = appConfig.get('name')



# Configurar el modo del log
logger.remove()  # Eliminar cualquier configuración anterior
logger.add(sys.stdout, level=logMode, format=" {time} - {level} - {message} - {module} - {function}")  # Agregar un manipulador para stdout en nivel logMode
logger.add(
    sink="logs/development.log",
    level=logMode,
    rotation=rotation,
    format=" {time} - {level} - {message} - {module} - {function}"
)