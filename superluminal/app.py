import falcon
import logging
from v1 import routes

# configure logging as you wish
logpath = '/var/log/subluminal/subluminal.log'
logging.basicConfig(filename=logpath,
                    level=logging.INFO)
LOG = logging.getLogger(__name__)

class SubluminalApp(object):
    __app__ = None
    @classmethod
    def getApp(cls):
        if cls.__app__ is None:
            cls.__app__ = SubluminalApp()
        return cls.__app__

    def __init__(self):
        wsgi = falcon.API(
            # include appropriate falcon parameters here
        )
        routes.set_routes(wsgi)
