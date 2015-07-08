import json

SAMPLE_INV = {
    'foobar': [
        '1.2.3.4',
        '5.6.7.8'
    ]
}

class SampleDynamicInventory(object):

    def get_inventory(self):
        return json.dumps(SAMPLE_INV)
