import falcon
import uuid
import importlib
from threading import Thread
import json
import pprint
import os.path

from oslo.config import cfg
ansible_opts = [
    cfg.StrOpt('playbook_path',
               default='/etc/superluminal/playbooks',
               help='Ansible playbook library'),
    cfg.StrOpt('inventory_path',
               default='/etc/superluminal/inventory',
               help='Ansible inventory file'),
    cfg.StrOpt('callback_module',
               default='superluminal.samples.callback_sample',
               help='Ansible callback module'),
    cfg.StrOpt('callback_class',
               default='SampleCallbacks',
               help='Ansible callback class'),
]
ansible_group = cfg.OptGroup(name='ansible', title='ansible')
cfg.CONF.register_group(ansible_group)
cfg.CONF.register_opts(ansible_opts, ansible_group)
cfg.CONF(args=[], project='superluminal')

PLAYBOOK_PATH = cfg.CONF.ansible.playbook_path
INVENTORY_PATH = cfg.CONF.ansible.inventory_path
CALLBACK_MODULE = cfg.CONF.ansible.callback_module
CALLBACK_CLASS = cfg.CONF.ansible.callback_class
TMP_DIR = '/tmp'

import logging
LOG = logging.getLogger(__name__)

CALLBACKS = getattr(importlib.import_module(CALLBACK_MODULE), CALLBACK_CLASS)

class PlaybookRunner(object):
    def __init__(self, playbook_id, tags, skip_tags, inventory, password=None):

        self.playbook_id = playbook_id
        self.tags = tags
        self.skip_tags = skip_tags
        self.inventory = inventory
        self.password = password

    def run(self, run_id):

        import ansible.playbook
        import ansible.inventory
        from ansible import utils
        from ansible.callbacks import AggregateStats

        playbook_file = '{0}/{1}.yml'.format(PLAYBOOK_PATH, self.playbook_id)
        stats = AggregateStats()
        cb = CALLBACKS(run_id, stats)
        inventory = ansible.inventory.Inventory(self.inventory)
        def run_playbook():
            os.chdir(cfg.CONF.ansible.playbook_path)
            pb = ansible.playbook.PlayBook(playbook=playbook_file,
                                           only_tags=self.tags,
                                           skip_tags=self.skip_tags,
                                           remote_pass=self.password,
                                           stats=stats,
                                           inventory=inventory,
                                           callbacks=cb,
                                           runner_callbacks=cb)
            print 'running %s' % pprint.pformat(pb.__dict__)
            LOG.info('Running playbook {0} with tags {1} skip_tags {2}'.format(playbook_file, self.tags, self.skip_tags))
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
        playbook_id = req_body.get('playbook_id', None)
        if playbook_id is None:
            raise falcon.HTTPBadRequest('Invalid Input',
                                        'Playbook ID is required')
        run_id = req_body.get('run_id', None)
        if run_id is None:
            raise falcon.HTTPBadRequest('Invalid Input',
                                        'Run ID is required')
        tags = req_body.get('tags', None)
        skip_tags = req_body.get('skip_tags', None)
        if os.path.exists(INVENTORY_PATH):
            inv = INVENTORY_PATH
        else:
            inv = '/usr/bin/superluminal_inventory.py'
        password = req_body.get('password', None)
        runner = PlaybookRunner(playbook_id, tags, skip_tags, inv, password)
        runner.run(run_id)
        body = {
            'id': run_id
        }
        resp.body = json.dumps(body)
        resp.status = falcon.HTTP_201
