import pprint

def pretty(result):
    return pprint.pformat(result)

#import logging
#LOG = logging.getLogger(__name__)

class PlaybookCallbacks(object):
    def __init__(self, ID):
        self.ID = ID

    def on_start(self):
        print('on start, id = %s' % self.ID)

    def on_notify(self, host, handler):
        print('on notify, host = %s handler = %s' % (host, handler))

    def on_no_hosts_matched(self):
        print('on no hosts matched')

    def on_no_hosts_remaining(self):
        print('on no hosts remaining')

    def on_task_start(self, name, is_conditional):
        print('on task start, name = %s, is_conditional = %s' % (name, is_conditional))

    def on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None,
                       confirm=False, salt_size=None, salt=None, default=None):
        print('on vars prompt, name = %s' % varname)

    def on_setup(self):
        print('setup')

    def on_import_for_host(self, host, imported_file):
        print('on import for host, host = %s file = %s' % (host, imported_file))

    def on_not_import_for_host(self, host, missing_file):
        print('on not import for host, host = %s missing = %s' % (host, missing_file))

    def on_play_start(self, name):
        print('on play start, name = %s' % name)

    def on_stats(self, stats):
        print('on stats, stats = %s' % stats)

class PlaybookRunnerCallbacks(object):
    def __init__(self, ID, stats):
        print('runner callbacks, ID = %s, stats = %s' % (ID, stats))
        self.stats = stats

    def on_unreachable(self, host, result):
        print('on unreachable, host = %s result = %s' % (host, pretty(result)))

    def on_failed(self, host, result, ignore_errors=False):
        print('on failed, host = %s result = %s ignore errors = %s' % (host, pretty(result), ignore_errors))

    def on_ok(self, host, result):
        print('on ok, host = %s result = %s' % (host, pretty(result)))

    def on_skipped(self, host, item=None):
        print('on skipped, host = %s item = %s' % (host, item))

    def on_no_hosts(self):
        print('on no hosts')

    def on_async_poll(self, host, result, jid, clock):
        print('on async poll, host = %s res = %s jid = %s clock = %s' % (host, pretty(result), jid, clock))

    def on_async_ok(self, host, result, jid):
        print('on async ok, host = %s res = %s jid = %s' % (host, pretty(result), jid))

    def on_async_failed(self, host, result, jid):
        print('on async failed, host = %s res = %s jid = %s' % (host, pretty(result), jid))

    def on_file_diff(self, host, diff):
        print('on file diff, host = %s diff = %s' % (host, diff))
