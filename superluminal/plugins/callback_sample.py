import pprint

def pretty(result):
    return pprint.pformat(result)

import logging
LOG = logging.getLogger(__name__)

class PlaybookCallbacks(object):
    def __init__(self, ID):
        self.ID = ID

    def on_start(self):
        LOG.info('on start, id = %s' % self.ID)

    def on_notify(self, host, handler):
        LOG.info('on notify, host = %s handler = %s' % (host, handler))

    def on_no_hosts_matched(self):
        LOG.info('on no hosts matched')

    def on_no_hosts_remaining(self):
        LOG.info('on no hosts remaining')

    def on_task_start(self, name, is_conditional):
        LOG.info('on task start, name = %s, is_conditional = %s' % (name, is_conditional))

    def on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None,
                       confirm=False, salt_size=None, salt=None, default=None):
        LOG.info('on vars prompt, name = %s' % varname)

    def on_setup(self):
        LOG.info('setup')

    def on_import_for_host(self, host, imported_file):
        LOG.info('on import for host, host = %s file = %s' % (host, imported_file))

    def on_not_import_for_host(self, host, missing_file):
        LOG.info('on not import for host, host = %s missing = %s' % (host, missing_file))

    def on_play_start(self, name):
        LOG.info('on play start, name = %s' % name)

    def on_stats(self, stats):
        LOG.info('on stats, stats = %s' % stats)

class PlaybookRunnerCallbacks(object):
    def __init__(self, ID, stats):
        LOG.info('runner callbacks, ID = %s, stats = %s' % (ID, stats))
        self.stats = stats

    def on_unreachable(self, host, result):
        LOG.info('on unreachable, host = %s result = %s' % (host, pretty(result)))

    def on_failed(self, host, result, ignore_errors=False):
        LOG.info('on failed, host = %s result = %s ignore errors = %s' (host, pretty(result), ignore_errors))

    def on_ok(self, host, result):
        LOG.info('on ok, host = %s result = %s' % (host, pretty(result)))

    def on_skipped(self, host, item=None):
        LOG.info('on skipped, host = %s item = %s' % (host, item))

    def on_no_hosts(self):
        LOG.info('on no hosts')

    def on_async_poll(self, host, result, jid, clock):
        LOG.info('on async poll, host = %s res = %s jid = %s clock = %s' % (host, pretty(result), jid, clock))

    def on_async_ok(self, host, result, jid):
        LOG.info('on async ok, host = %s res = %s jid = %s' % (host, pretty(result), jid))

    def on_async_failed(self, host, result, jid):
        LOG.info('on async failed, host = %s res = %s jid = %s' % (host, pretty(result), jid))

    def on_file_diff(self, host, diff):
        LOG.info('on file diff, host = %s diff = %s' % (host, diff))
