import falcon
import uuid
import importlib

import ansible.playbook
import ansible.inventory
from ansible import utils
from ansible.callbacks import AggregateStats

# These need to go into oslo.config
PLAYBOOK_PATH='/etc/bedrock/playbooks'
INVENTORY_PATH='/etc/bedrock/playbooks/test-inventory'
CALLBACK_MODULE='superluminal.plugins.callback_sample'

import logging
LOG = logging.getLogger(__name__)

CALLBACKS = importlib.import_module(CALLBACK_MODULE)

class Run(object):
    def on_post(self, req, resp):
        playbook = req.get_param('playbook')
        ID = uuid.uuid4()
        playbook_file = '{0}/{1}.yml'.format(PLAYBOOK_PATH, playbook)
        stats = AggregateStats()
        playbook_cb = CALLBACKS.PlaybookCallbacks(ID)
        runner_cb = CALLBACKS.PlaybookRunnerCallbacks(ID, stats)
        inventory = ansible.inventory.Inventory(INVENTORY_PATH)
        def run_playbook():
            pb = ansible.playbook.PlayBook(playbook=playbook_file,
                                           stats=stats,
                                           inventory=inventory,
                                           callbacks=playbook_cb,
                                           runner_callbacks=runner_cb)
            results = pb.run()
            LOG.info('RESULTS = %s' % results)
        t = Thread(target=run_playbook, name='run_playbook')
        t.start()
        body = {
            'ID': ID
        }
        resp.body = json.dumps(body)
        resp.status = falcon.HTTP_201
