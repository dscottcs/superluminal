import gunicorn.app.base
from gunicorn.six import iteritems

from superluminal.app import Superluminal

from oslo.config import cfg, types
PortType = types.Integer(1, 65535)

gunicorn_opts = [
    cfg.IntOpt('workers',
               default=1,
               help='Server worker processes'),
    cfg.StrOpt('user',
               default='superluminal',
               help='User to run worker processes as'),
    cfg.StrOpt('group',
               default='superluminal',
               help='Group to run worker processes as'),
    cfg.StrOpt('bind_host',
               default='127.0.0.1',
               help='Interface to bind on'),
    cfg.Opt('bind_port',
            type=PortType,
            default=9002,
            help='Port to listen on'),
    cfg.StrOpt('log_dir',
               default='/var/log/superluminal/gunicorn',
               help='Directory to contain access and error logs'),
    cfg.StrOpt('access_log_file',
               default='access.log',
               help='Access log file'),
    cfg.StrOpt('error_log_file',
               default='error.log',
               help='Error log file'),
    cfg.StrOpt('log_level',
               default='info',
               help='Log level (one of "debug","info","warning","error", or "critical"'),
    cfg.IntOpt('keep_alive',
               default=5,
               help='Seconds to keep HTTP connections open for successive requests'),
    cfg.StrOpt('wd',
               default='/opt/playbooks',
               help='Working directory for superluminal app (should be playbooks directory)'),
    cfg.ListOpt('environment',
                default='',
                help='Environment settings ([key1=val1,key2=val2;...])')
]
gunicorn_group = cfg.OptGroup(name='gunicorn', title='gunicorn')
cfg.CONF.register_group(gunicorn_group)
cfg.CONF.register_opts(gunicorn_opts, gunicorn_group)
cfg.CONF(args=[], project='superluminal')

class GunicornSuperluminalApp(gunicorn.app.base.BaseApplication):

    def __init__(self, app):
        self.application = app
        gun_conf = cfg.CONF.gunicorn
        access_log = '{0}/{1}'.format(gun_conf.log_dir, gun_conf.access_log_file)
        error_log = '{0}/{1}'.format(gun_conf.log_dir, gun_conf.error_log_file)
        bind = '{0}:{1}'.format(gun_conf.bind_host, gun_conf.bind_port)
        self.options = {
            'workers': gun_conf.workers,
            'user': gun_conf.user,
            'group': gun_conf.group,
            'bind': bind,
            'accesslog': access_log,
            'errorlog': error_log,
            'loglevel': gun_conf.log_level,
            'keepalive': gun_conf.keep_alive,
            'raw_env': gun_conf.environment,
        }
        super(GunicornSuperluminalApp, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
    app = Superluminal.getApp()
    gun_app = GunicornSuperluminalApp(app.wsgi)
    gun_app.run()
