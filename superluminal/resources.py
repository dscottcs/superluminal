import falcon
import uuid
import importlib
from threading import Thread
import json

import ansible.playbook
import ansible.inventory
from ansible import utils
from ansible.callbacks import AggregateStats

from oslo.config import cfg
ansible_opts = [
    cfg.StrOpt('playbook_path',
               default='/etc/superluminal/playbooks',
               help='Ansible playbook library'),
    cfg.StrOpt('inventory_path',
               default='/etc/superluminal/inventory',
               help='Ansible inventory file'),
    cfg.StrOpt('callback_module',
               default='superluminal.plugins.callback_sample',
               help='Ansible callback module')
]
ansible_group = cfg.OptGroup(name='ansible', title='ansible')
cfg.CONF.register_group(ansible_group)
cfg.CONF.register_opts(ansible_opts, ansible_group)
cfg.CONF(args=[], project='superluminal')

PLAYBOOK_PATH = cfg.CONF.ansible.playbook_path
INVENTORY_PATH = cfg.CONF.ansible.inventory_path
CALLBACK_MODULE = cfg.CONF.ansible.callback_module

import logging
LOG = logging.getLogger(__name__)

CALLBACKS = importlib.import_module(CALLBACK_MODULE)

class PlaybookRunner(object):
    def __init__(self, playbook_id, password):
        self.playbook_id = playbook_id
        self.password = password

    def run(self, ID):
        playbook_file = '{0}/{1}.yml'.format(PLAYBOOK_PATH, self.playbook_id)
        stats = AggregateStats()
        playbook_cb = CALLBACKS.PlaybookCallbacks(ID)
        runner_cb = CALLBACKS.PlaybookRunnerCallbacks(ID, stats)
        inventory = ansible.inventory.Inventory(INVENTORY_PATH)
        def run_playbook():
            pb = ansible.playbook.PlayBook(playbook=playbook_file,
                                           remote_pass=self.password,
                                           stats=stats,
                                           inventory=inventory,
                                           callbacks=playbook_cb,
                                           runner_callbacks=runner_cb)
            LOG.info('Running playbook {0}'.format(playbook_file))
            results = pb.run()
            LOG.info('Results: {0}'.format(results))
        t = Thread(target=run_playbook, name='run_playbook')
        t.start()

class Run(object):
    def on_post(self, req, resp):
        playbook_id = req.get_param('playbook')
        password = req.get_param('password')
        ID = req.get_param('ID')
        runner = PlaybookRunner(playbook_id, password)
        runner.run(ID)
        body = {
            'ID': ID
        }
        resp.body = json.dumps(body)
        resp.status = falcon.HTTP_201
