#!/usr/bin/env python

import os
import sys
import argparse
try:
    import json
except ImportError:
    import simplejson as json

class ExampleInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.example_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            host = self.args.host
            print(host)
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory));

    # Example inventory for testing.
    def example_inventory(self):
        return {
            "do_vms": {
                "hosts": [
                    "167.99.100.240",
                    "157.245.174.66"
                ],
            },
            "_meta": {
                "hostvars": {
                    "167.99.100.240": {
                        "host_specific_var": "do-test01"
                    },
                    "157.245.174.66": {
                        "host_specific_var": "do-test02"
                    }
                }
            }
        }
    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()
    
################################################################################ 
# Run the script
ExampleInventory()
