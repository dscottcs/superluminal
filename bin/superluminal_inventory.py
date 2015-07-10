#!/usr/bin/env python

#from __future__ import print_function
import sys
import json
import pprint

from superluminal.inventory.inventory_manager import InventoryManager

if "--list" in sys.argv:
    inv_mgr = InventoryManager.getManager()
    inventory = inv_mgr.get_inventory()
    print(inventory)
else:
    print('{}')
