import importlib
import os
import sys
import requests
import json

from oslo.config import cfg
fwd_opts = [
    cfg.StrOpt('forward_location',
               default='/etc/superluminal/plugins',
               help='Location of forwarding module (None if already in sys.path'),
    cfg.StrOpt('forward_module',
               default='forward',
               help='Forwarding module name'),
    cfg.StrOpt('forward_class',
               default='Forward',
               help='Forwarding class name'),
    cfg.StrOpt('forward_url',
               default=None,
               help='Forwarding URL')
]
fwd_group = cfg.OptGroup(name='forward', title='forward')
cfg.CONF.register_group(fwd_group)
cfg.CONF.register_opts(fwd_opts, fwd_group)
cfg.CONF(args=[], project='superluminal')

import logging
LOG = logging.getLogger(__name__)

# The default forwarder uses a URL to communicate
# results to a waiting controller of some kind
# (presumably the same controller that invoked
# the playbook run in the first place)
class URLForwarder(object):

    def __init__(self, playbook_id, run_id):
        # Find forwarding URL from configuration
        self.fwd_url = cfg.CONF.forward.forward_url
        self.playbook_id = playbook_id
        self.run_id = run_id

    def forward(self, msg_type, data=None, host=None):
        payload = {
            'playbook_id': self.playbook_id,
            'run_id': self.run_id,
            'msg_type': msg_type,
        }
        if data is not None:
            payload['data'] = data
        if host is not None:
            payload['host'] = host
        headers = {
            'content-type': 'application/json'
        }
        resp = requests.post(self.fwd_url,
                             data=json.dumps(payload),
                             headers=headers)
        resp.raise_for_status()

class ForwardListener(object):

    __listener__ = None

    @classmethod
    def getListener(cls):
        if cls.__listener__ is None:
            playbook_id = os.environ['PLAYBOOK_ID']
            run_id = os.environ['RUN_ID']
            cls.__listener__ = ForwardListener(playbook_id, run_id)
        return cls.__listener__
        
    def __init__(self, playbook_id, run_id):
        # Find forwarding class through configuration
        #fwd_location = cfg.CONF.forward.forward_location
        #if fwd_location is not None:
        #    sys.path.append(fwd_location)
        #FWD_MODULE = cfg.CONF.forward.forward_module
        #FWD_CLASS = cfg.CONF.forward.forward_class
        # Import configured forwarding class, instantiate forwarding object
        #self.forwarder = getattr(importlib.import_module(FWD_MODULE), FWD_CLASS)()
        self.run_id = run_id
        self.playbook_id = playbook_id
        self.forwarder = URLForwarder(playbook_id, run_id)

    def accept(self, msg_type, data=None, host=None):
        if hasattr(self.forwarder, 'forward'):
            self.forwarder.forward(msg_type, data, host)

    def on_start(self):
        self.forwarder.forward('start')

    def on_finish(self, results):
        self.forwarder.forward('finish', results)
