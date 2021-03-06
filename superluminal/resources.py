import falcon
import importlib
import json
import pprint
import os, os.path
import sys
from multiprocessing import Process
import contextlib
import StringIO
from superluminal.forward.listener import ForwardListener

from oslo.config import cfg
ansible_opts = [
    cfg.StrOpt('playbook_path',
               default='/etc/superluminal/playbooks',
               help='Ansible playbook library'),
    cfg.StrOpt('inventory_path',
               default='/etc/superluminal/inventory',
               help='Ansible inventory file')
]
ansible_group = cfg.OptGroup(name='ansible', title='ansible')
cfg.CONF.register_group(ansible_group)
cfg.CONF.register_opts(ansible_opts, ansible_group)
cfg.CONF(args=[], project='superluminal')

PLAYBOOK_PATH = cfg.CONF.ansible.playbook_path
INVENTORY_PATH = cfg.CONF.ansible.inventory_path
TMP_DIR = '/tmp'

import logging
LOG = logging.getLogger(__name__)

@contextlib.contextmanager
def stdout_redirect(where):
    sys.stdout = where
    sys.stderr = where
    try:
        yield where
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

class PlaybookRunner(object):

    def __init__(self, playbook_id, run_id, inventory, password=None):

        self.playbook_id = playbook_id
        self.run_id = run_id 
        self.inventory = inventory
        self.password = password
        self.tags = None
        self.skip_tags = []

    def run(self):

        import ansible.playbook
        import ansible.inventory
        from ansible import utils
        from ansible.callbacks import AggregateStats, PlaybookCallbacks, PlaybookRunnerCallbacks

        playbook_file = '{}/{}.yml'.format(PLAYBOOK_PATH, self.playbook_id)
        playbook_cb = PlaybookCallbacks(verbose=utils.VERBOSITY)
        stats = AggregateStats()
        runner_cb = PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        inventory = ansible.inventory.Inventory(self.inventory)
        def run_playbook(run_id, playbook_id):
            os.chdir(cfg.CONF.ansible.playbook_path)
            # Initialize the environment for this process for the Ansible callback plugin,
            # which uses the same listener.
            os.environ['PLAYBOOK_ID'] = playbook_id
            os.environ['RUN_ID'] = run_id
            listener = ForwardListener.getListener()
            pb = ansible.playbook.PlayBook(playbook=playbook_file,
                                           only_tags=self.tags,
                                           skip_tags=self.skip_tags,
                                           remote_pass=self.password,
                                           stats=stats,
                                           inventory=inventory,
                                           callbacks=playbook_cb,
                                           runner_callbacks=runner_cb)
            listener.on_start()
            with stdout_redirect(StringIO.StringIO()) as temp_stdout:
                results = pb.run()
            temp_stdout.seek(0)
            output = temp_stdout.read()
            output_list = [line for line in temp_stdout.read().split('\n') if line]
            data = {
                'ansible_results': results,
                'ansible_output': output
            }
            listener.on_finish(data)
        p = Process(target=run_playbook, args=(self.run_id, self.playbook_id))
        p.start()

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
        runner = PlaybookRunner(playbook_id, run_id, inv, password)
        runner.run()
        body = {
            'id': run_id
        }
        resp.body = json.dumps(body)
        resp.status = falcon.HTTP_201
