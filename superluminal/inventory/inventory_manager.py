import importlib
from oslo.config import cfg
import json
import pprint

inventory_opts = [
    cfg.StrOpt('inventory_module',
               default='superluminal.sample.inventory_sample',
               help='Ansible dynamic inventory module'),
    cfg.StrOpt('inventory_class',
               default='SampleDynamicInventory',
               help='Ansible dynamic inventory class')
]
inventory_group = cfg.OptGroup(name='dynamic_inventory', title='dynamic_inventory')
cfg.CONF.register_group(inventory_group)
cfg.CONF.register_opts(inventory_opts, inventory_group)
cfg.CONF(args=[], project='superluminal')

INVENTORY_MODULE = cfg.CONF.dynamic_inventory.inventory_module
INVENTORY_CLASS = cfg.CONF.dynamic_inventory.inventory_class

class InventoryManager(object):

    __inv_mgr__ = None
    
    @classmethod
    def getManager(cls):
        if cls.__inv_mgr__ is None:
            cls.__inv_mgr__ = InventoryManager()
        return cls.__inv_mgr__

    def __init__(self):
        inv_cls = getattr(importlib.import_module(INVENTORY_MODULE), INVENTORY_CLASS)
        self.inv = inv_cls()

    def get_inventory(self):
        if not hasattr(self.inv, 'get_inventory'):
            return None
        inventory = self.inv.get_inventory()
        return inventory

