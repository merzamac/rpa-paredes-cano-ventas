from configparser import ConfigParser
from .core.logger import set_logger
from .core.router import Route

cp: ConfigParser = ConfigParser()
cp.read("config/config.ini")

routes: Route = Route.config(__file__, cp)

set_logger(routes.LOGS_DIR)
set_logger(routes.LOGS_DIR)
