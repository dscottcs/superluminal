from superluminal.forward.listener import ForwardListener
import pprint
import os

import logging
LOG = logging.getLogger(__name__)

def pretty(s):
    return pprint.pformat(s)

class CallbackModule(object):

    def __init__(self):
        self.listener = ForwardListener.getListener()

    def on_any(self, *args, **kwargs):
        data = {
            'args': args,
            'kwargs': kwargs
        }
        #self.listener.accept('any', data)

    # runner callbacks (by host)
    def runner_on_failed(self, host, result, ignore_errors=False):
        self.listener.accept('run_failed', result, host)

    def runner_on_ok(self, host, result):
        self.listener.accept('run_ok', result, host)

    def runner_on_skipped(self, host, item=None):
        self.listener.accept('run_skipped',
                        {
                            'item': item
                        },
                        host)

    def runner_on_unreachable(self, host, result):
        self.listener.accept('run_unreachable', result, host)

    def runner_on_no_hosts(self):
        self.listener.accept('run_no hosts')

    def runner_on_async_poll(self, host, result, jid, clock):
        self.listener.accept('run_async_poll', result, host)

    def runner_on_async_ok(self, host, result, jid):
        self.listener.accept('run_async_ok', result, host)

    def runner_on_async_failed(self, host, result, jid):
        self.listener.accept('run_async_failed', result, host)

    # Playbook callbacks (by play)
    def playbook_on_start(self):
        self.listener.accept('pbk_start')

    def playbook_on_notify(self, host, handler):
        self.listener.accept('pbk_notify',
                        {
                            'handler': handler
                        },
                        host)

    def playbook_on_no_hosts_matched(self):
        self.listener.accept('pbk_no_hosts_matched')

    def playbook_on_no_hosts_remaining(self):
        self.listener.accept('pbk_no_hosts_remaining')

    def playbook_on_task_start(self, name, is_conditional):
        self.listener.accept('pbk_task_start',
                        {
                            'name': name,
                            'is_conditional': is_conditional
                        })

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None,
                       confirm=False, salt_size=None, salt=None, default=None):
        self.listener.accept('pbk_vars_prompt',
                        {
                            'varname': varname,
                            'private': private,
                            'prompt': prompt,
                            'encrypt': encrypt,
                            'confirm': confirm,
                            'salt_size': salt_size,
                            'salt': salt,
                            'default': default
                        })

    def playbook_on_setup(self):
        self.listener.accept('pbk_setup')

    def playbook_on_import_for_host(self, host, imported_file):
        self.listener.accept('pbk_import_for_host',
                        {
                            'file': imported_file
                        },
                        host)

    def playbook_on_not_import_for_host(self, host, missing_file):
        self.listener.accept('pbk_not_import_for_host',
                        {
                            'file': missing_file
                        },
                        host)

    def playbook_on_play_start(self, name):
        self.listener.accept('pbk_play_start',
                        {
                            'name': name
                        })

    def playbook_on_stats(self, stats):
        self.listener.accept('pbk_stats',
                        {
                            'stats': stats
                        })
