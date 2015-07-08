import pprint

def pretty(result):
    return pprint.pformat(result)

import logging
LOG = logging.getLogger(__name__)

class SampleCallbacks(object):
    def __init__(self, ID):
        self.ID = ID
        self.stats = stats

    def on_any(self, *args, **kwargs):
        LOG.info('on any, id = %s' % self.ID)

    # Playbook callbacks (by play)
    def playbook_on_start(self):
        LOG.info('playbook on start, id = %s' % self.ID)

    def playbook_on_notify(self, host, handler):
        LOG.info('playbook on notify, host = %s handler = %s' % (host, handler))

    def playbook_on_no_hosts_matched(self):
        LOG.info('playbook on no hosts matched')

    def playbook_on_no_hosts_remaining(self):
        LOG.info('playbook on no hosts remaining')

    def playbook_on_task_start(self, name, is_conditional):
        LOG.info('playbook on task start, name = %s, is_conditional = %s' % (name, is_conditional))

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None,
                       confirm=False, salt_size=None, salt=None, default=None):
        LOG.info('playbook on vars prompt, name = %s' % varname)

    def playbook_on_setup(self):
        LOG.info('playbook on setup')

    def playbook_on_import_for_host(self, host, imported_file):
        LOG.info('playbook on import for host, host = %s file = %s' % (host, imported_file))

    def playbook_on_not_import_for_host(self, host, missing_file):
        LOG.info('playbook on not import for host, host = %s missing = %s' % (host, missing_file))

    def playbook_on_play_start(self, name):
        LOG.info('playbook on play start, name = %s' % name)

    def playbook_on_stats(self, stats):
        LOG.info('playbook on stats, stats = %s' % stats)

    # runner callbacks (by host)
    def runner_on_failed(self, host, result, ignore_errors=False):
        LOG.info('runner on failed, host = %s result = %s ignore errors = %s' % (host, pretty(result), ignore_errors))

    def runner_on_ok(self, host, result):
        LOG.info('runner on ok, host = %s result = %s' % (host, pretty(result)))

    def runner_on_skipped(self, host, item=None):
        LOG.info('runner on skipped, host = %s item = %s' % (host, item))

    def runner_on_unreachable(self, host, result):
        LOG.info('runner on unreachable, host = %s result = %s' % (host, pretty(result)))

    def runner_on_no_hosts(self):
        LOG.info('runner on no hosts')

    def runner_on_async_poll(self, host, result, jid, clock):
        LOG.info('runner on async poll, host = %s res = %s jid = %s clock = %s' % (host, pretty(result), jid, clock))

    def runner_on_async_ok(self, host, result, jid):
        LOG.info('runner on async ok, host = %s res = %s jid = %s' % (host, pretty(result), jid))

    def runner_on_async_failed(self, host, result, jid):
        LOG.info('runner on async failed, host = %s res = %s jid = %s' % (host, pretty(result), jid))

    # Superluminal specific callbacks
    def superluminal_on_finish(self, results):
        LOG.info('on finish, results = %s' % results)
