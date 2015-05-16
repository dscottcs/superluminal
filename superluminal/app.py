import falcon
import logging
from superluminal.v1.routes import Routes

from oslo.config import cfg
default_opts = [
    cfg.StrOpt('log_dir',
               default='/var/log/superluminal',
               help='Log directory for superluminal log files'),
    cfg.StrOpt('log_file',
               default='superluminal.log',
               help='Main superluminal log file'),
    cfg.StrOpt('log_level',
               default='INFO',
               help='Log level for main superluminal log file')
]
cfg.CONF.register_opts(default_opts)
cfg.CONF(args=[], project='superluminal')

logpath = '{0}/{1}'.format(cfg.CONF.log_dir, cfg.CONF.log_file)
logging.basicConfig(filename=logpath,
                    level=logging.INFO)
LOG = logging.getLogger(__name__)

class Superluminal(object):
    __app__ = None
    @classmethod
    def getApp(cls):
        if cls.__app__ is None:
            cls.__app__ = Superluminal()
        return cls.__app__

    def __init__(self):
        wsgi = falcon.API(
            # include appropriate falcon parameters here
        )
        self.wsgi = wsgi
        Routes.set_routes(wsgi)
