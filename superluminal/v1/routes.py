from v1.resources import Run

class routes(object):

    @classmethod
    def set_routes(cls, api):
        api.add_route('v1/run', Run())
