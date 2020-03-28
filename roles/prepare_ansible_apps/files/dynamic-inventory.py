#!/usr/bin/env python

import os
import sys
import argparse
import pymysql
try:
    import json
except ImportError:
    import simplejson as json

class AnsibleInventory:
    """
      Connect to MYSQL
    """
    def __init__(self, db_server='localhost', db_port=3306, db_name=os.getenv('MYSQL_NAME', ''), db_user=os.getenv('MYSQL_USER', ''), db_password=os.getenv('MYSQL_PASSWORD', '')):
        self.db_server = db_server
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.inventory = {}
        self.read_cli_args()
        
        if self.args.list:
            self.inventory = self.example_inventory()
            # Called with `--host [hostname]`.
        elif self.args.host:
            host = self.args.host
            self.inventory = self.empty_inventory()
            # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()
 
        print(json.dumps(self.inventory));
    
    def connect(self):
        self.connection = pymysql.connect(host=self.db_server, port=self.db_port,
                                          user=self.db_user, passwd=self.db_password, db=self.db_name)

    def example_inventory(self):
        # connect to db to build this json lis
        self.connect()
        cur = self.connection.cursor()
        cur.execute(
            "SELECT `vm_group`, `vm_ip_address`  FROM ansible_rest_wrapper_vms ORDER BY `vm_ip_address`")
        for row in cur.fetchall():
            group = row[0]
            if group is None:
                group = 'do_vms'

            if group not in self.inventory:
                self.inventory[group] = {
                    'hosts': [],
                }

            self.inventory[group]['hosts'].append(row[1])

        #print(self.inventory)
        cur.close()
        self.connection.close()

        return self.inventory

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
AnsibleInventory()
