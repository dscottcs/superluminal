import requests
import json

import logging
LOG = logging.getLogger(__name__)

class Forwarder(object):
    def __init__(self):
        this.fwd_url = 'http://localhost:9999/forward'

    def forward(self, reason, host=None, data=None):
        body = {
            'reason': reason
        }
        if host is not None:
            body['host'] = host
        if data is not None:
            body['data'] = data
        resp = requests.post(this.fwd_url,
                             body=json.dumps(body))
