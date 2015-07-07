import falcon
import uuid
import importlib
from threading import Thread
import json
import os.path

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
               help='Ansible callback module'),
    cfg.StrOpt('callback_class',
               default='SampleCallbacks',
               help='Ansible callback class')
]
ansible_group = cfg.OptGroup(name='ansible', title='ansible')
cfg.CONF.register_group(ansible_group)
cfg.CONF.register_opts(ansible_opts, ansible_group)
cfg.CONF(args=[], project='superluminal')

PLAYBOOK_PATH = cfg.CONF.ansible.playbook_path
INVENTORY_PATH = cfg.CONF.ansible.inventory_path
CALLBACK_MODULE = cfg.CONF.ansible.callback_module
CALLBACK_CLASS = cfg.CONF.ansible.callback_class

import logging
LOG = logging.getLogger(__name__)

CALLBACKS = getattr(importlib.import_module(CALLBACK_MODULE), CALLBACK_CLASS)

class PlaybookRunner(object):
    def __init__(self, playbook_id, inventory, password=None):
        self.playbook_id = playbook_id
        self.inventory = inventory
        self.password = password

    def run(self, run_id):
        playbook_file = '{0}/{1}.yml'.format(PLAYBOOK_PATH, self.playbook_id)
        stats = AggregateStats()
        cb = CALLBACKS(run_id, stats)
        def run_playbook():
            pb = ansible.playbook.PlayBook(playbook=playbook_file,
                                           remote_pass=self.password,
                                           stats=stats,
                                           inventory=self.inventory,
                                           callbacks=cb,
                                           runner_callbacks=cb)
            LOG.info('Running playbook {0}'.format(playbook_file))
            results = pb.run()
            if hasattr(cb, 'superluminal_on_finish'):
                cb.on_finish(results)
        t = Thread(target=run_playbook, name='run_playbook')
        t.start()

class Run(object):
    def on_post(self, req, resp):
        try:
            raw_input = req.stream.read()
            req_body = json.loads(raw_input)
        except Exception, e:
            raise falcon.HTTPBadRequest('Invalid Input',
                                        'Request body is not valid JSON: %s' % e)
        playbook_id = req_body.get('playbook', None)
        if playbook_id is None:
            raise falcon.HTTPBadRequest('Invalid Input',
                                        'Playbook ID is required')
        run_id = req_body.get('run_id', None)
        if run_id is None:
            raise falcon.HTTPBadRequest('Invalid Input',
                                        'Run ID is required')
        inventory = req_body.get('inventory')
        if inventory is None and os.path.exists(INVENTORY_FILE):
            inventory = ansible.inventory.Inventory(INVENTORY_FILE)
        if inventory is None:
            raise falcon.HTTPBadRequest('Invalid Input',
                                        'No inventory has been defined')
        password = req.get_body('password', None)
        runner = PlaybookRunner(playbook_id, inventory, password)
        runner.run(run_id)
        body = {
            'run_id': run_id
        }
        resp.body = json.dumps(body)
        resp.status = falcon.HTTP_201
