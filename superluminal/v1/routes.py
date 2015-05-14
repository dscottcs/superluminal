from superluminal.resources import Run

class Routes(object):

    @classmethod
    def set_routes(cls, api):
        api.add_route('/v1/run', Run())
