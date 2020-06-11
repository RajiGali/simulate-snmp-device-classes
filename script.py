#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
import fnmatch
import itertools
from faker import Faker
import socket
from itertools import chain
import conf
import subprocess

my_dir = conf.data
host = conf.host


class simulate_snmp_devices:
    '''Class to simulate snmp devices'''

    def available_templates(self, *args):
        print('************Available device templates to use found in data directory********')

        for (root_dir_path, files) in os.walk(my_dir):

            if files:
                tag = os.path.relpath(root_dir_path, my_dir)

                for file in files:
                    
                    sub_folder = os.path.basename(tag)

                    print((sub_folder if sub_folder else ''), '--->', file)

        print('************End********')

    def parse_args(self):
        "This function is used to input the templates chosen by the user"

        # Initialize parser

        parser = argparse.ArgumentParser(description='SNMP Simulator.')

        # Adding optional argument

        parser.add_argument('-d', '--devices', required=False, nargs='+',
                            help="Enter the file names using '-d' option Ex:- -d xp.snmprec ubuntu.snmprec  ... ", default=False)
        parser.add_argument('-p', '--Print', required=False, action='store_true',
                            help=" type '-p' and hit 'Enter' to :show available device templates to use...")
        # Read arguments from command line
        args = parser.parse_args()
        return args

    def find_dev_template(self, *args):
        "To find the device template path in data directory."

        my_dir = './/data'
        dev_templates = list(itertools.chain(*args))
        template_path = []
        for (root_dir_path,files) in os.walk(my_dir):

            if files:
                tag = os.path.relpath(root_dir_path, my_dir)
                for device in dev_templates:
                    for file in files:
                        tag_parent = os.path.dirname(tag)
                        sub_folder = os.path.basename(tag)
                        if fnmatch.fnmatch(file, device):
                            template_path.append(os.path.normpath(
                                os.path.join(my_dir, tag_parent, sub_folder)))

        return template_path

    def get_open_port(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

    def create_snmp(self, *args):
        path = list(itertools.chain(*args))
        num_devices = len(path)

        faker = Faker()
        port_list = []
        path_list = []
        for i in range(num_devices):
            try:
                port = self.get_open_port(host)
                port_list.append(port)
                path_list.append(path[i])
                print(i + 1, path[i].split('/')[-1], port)

                subprocess.run('snmpsimd.py --v3-engine-id=010203040505060880 --v3-user=qxf2 --data-dir=%s --agent-udpv4-endpoint=127.0.0.1:%s --logging-method=file:./data/snmp_logs.txt:10m --log-level=debug & ' % (path[i], port))
            except OSError:
                raise ValueError(
                    "error in running the snmp device 'snmpsimd.py' command")

        return (port_list, path_list)

    def snmpwalk_dev_templates(self, *args):
        "snmpwalk the chosen device templates"

        port_path = list(itertools.chain(*args))
        (port_list, path_list) = map(list, zip(port_path))
        path_list = list(chain.from_iterable(path_list))
        port_list = list(chain.from_iterable(port_list))
        no_device = len(port_list)
        device_name = []
        device_port = []
        for (path_list, port_list) in zip(path_list, port_list):
            if '\\' in path_list:
                device_name.append(path_list.split('\\')[-1])
            else:
                device_name.append(path_list.split('/')[-1])
            device_port.append(port_list)

        for i in range(no_device):
            try:
                print('snmpwalk -v2c -c %s 127.0.0.1:%s 1.3.6 ' %(device_name[i], device_port[i]))
            except OSError:
                raise ValueError('error in running the snmpwalk')


if __name__ == '__main__':
    devices = simulate_snmp_devices()
    args = devices.parse_args()
    if args.Print is True:
        devices.available_templates(args.Print)
    elif args.devices is not False:
        template_path = devices.find_dev_template(args.devices)
        if template_path is not None:
            snmpwalk_list = devices.create_snmp(template_path)
            if snmpwalk_list is not None:
                devices.snmpwalk_dev_templates(snmpwalk_list)
